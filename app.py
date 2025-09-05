import io
from pathlib import Path
from datetime import datetime

import streamlit as st
from PIL import Image
import requests

from mscen.image_gen import generate_scene_image
from mscen.music_gen import generate_music_from_theme
from mscen.image_to_music import generate_music_from_image
from mscen.lighting import (
    generate_lighting_from_theme,
    generate_lighting_from_image,
    save_lighting_program,
)
from mscen.music_to_lighting import generate_lighting_from_wav
from mscen.core.config import load_config
from mscen.core.cache import SimpleDiskCache
from mscen.core.logger import JsonlLogger
from mscen.connectors.image_backend import ImageBackend, Txt2ImgParams
from mscen.connectors.music_backend import MusicBackend, MusicGenParams
from mscen.connectors.voice_backend import VoiceBackend, STTParams
from mscen.wled import save_wled_preset
from mscen.connectors.sd_webui_backend import SDWebUIBackend, SDWebUIParams
from mscen.agents.orchestrator import Orchestrator, OrchestratorConfig
from mscen.projects.project import Project, Room, compile_project
from mscen.video import compose_image_music_to_mp4
from mscen.agents.langgraph_orchestrator import build_graph
from mscen.devices.hue_controller import HueController
from mscen.devices.wled_controller import WLEDController
from mscen.agents.conversation_memory import ConversationMemory
from mscen.agents.feedback_learner import FeedbackLearner, FeedbackEntry
from mscen.optimization.model_optimizer import ModelOptimizer
from mscen.plugins.base import PluginManager
from mscen.personalization.user_profile import PersonalizationEngine
from mscen.ui.smart_components import SmartUI
from mscen.collaboration.sharing import SharingManager
from datetime import datetime
from mscen.ui.wizard import onboarding_wizard
from mscen.tasks.queue import TaskQueue, TaskStatus
from mscen.connectors.registry import BackendRegistry, BackendProfile
from mscen.enterprise.license_server import LicenseServer
from mscen.enterprise.security import SecurityManager, AccessContext
import json


BASE_DIR = Path(__file__).parent
cfg = load_config(BASE_DIR)
OUTPUTS_DIR = cfg.outputs_dir
cache = SimpleDiskCache(BASE_DIR / ".cache")
logger = JsonlLogger(BASE_DIR / "logs", name="app")
img_backend = ImageBackend(cfg.endpoints.image_txt2img_url, cache, logger) if cfg.endpoints.image_txt2img_url else None
sd_backend = SDWebUIBackend(cfg.endpoints.sdwebui_url, cache, logger) if cfg.endpoints.sdwebui_url else None
music_backend = MusicBackend(cfg.endpoints.music_gen_url, cache, logger) if cfg.endpoints.music_gen_url else None
voice_backend = VoiceBackend(cfg.endpoints.stt_url, cfg.endpoints.tts_url, cache, logger)

# Device controllers
hue_controller = None
if cfg.devices.hue_bridge_ip and cfg.devices.hue_username:
    hue_controller = HueController(cfg.devices.hue_bridge_ip, cfg.devices.hue_username, logger)

wled_controller = None
if cfg.devices.wled_ip:
    wled_controller = WLEDController(cfg.devices.wled_ip, logger)

# Memory and learning
memory = ConversationMemory(BASE_DIR / "memory")
feedback_learner = FeedbackLearner(BASE_DIR / "feedback")

# Plugin system and optimization
plugin_manager = PluginManager(BASE_DIR / "plugins", logger)
model_optimizer = ModelOptimizer(logger, cache)

# Personalization and collaboration
personalization_engine = PersonalizationEngine(BASE_DIR / "user_profiles")
smart_ui = SmartUI(personalization_engine)
sharing_manager = SharingManager(BASE_DIR / "shared")

license_server = LicenseServer(BASE_DIR)
security = SecurityManager(BASE_DIR)
backend_registry = BackendRegistry(logger)

# Register backends for profiling
if cfg.endpoints.sdwebui_url:
    backend_registry.register("sdwebui", BackendProfile(name="Stable Diffusion WebUI", kind="image", endpoint=cfg.endpoints.sdwebui_url, cost_per_call_usd=0))
if cfg.endpoints.image_txt2img_url:
    backend_registry.register("img_http", BackendProfile(name="HTTP Image Gen", kind="image", endpoint=cfg.endpoints.image_txt2img_url))
if cfg.endpoints.music_gen_url:
    backend_registry.register("music_http", BackendProfile(name="HTTP Music Gen", kind="music", endpoint=cfg.endpoints.music_gen_url))

# Onboarding wizard: write .env on first run
if "onboarding_completed" not in st.session_state:
    if onboarding_wizard(BASE_DIR) is False:
        st.stop()


def save_pil_image(img: Image.Image, out_dir: Path, filename_prefix: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    img_path = out_dir / f"{filename_prefix}_{timestamp}.png"
    img.save(img_path)
    return img_path


def render_lighting_preview(frames, width: int = 480, height: int = 36) -> Image.Image:
    if not frames:
        return Image.new("RGB", (width, height), (0, 0, 0))
    num = len(frames)
    seg_w = max(1, width // num)
    canvas = Image.new("RGB", (seg_w * num, height), (0, 0, 0))
    for idx, frame in enumerate(frames):
        color = (frame["r"], frame["g"], frame["b"])  # type: ignore
        for x in range(idx * seg_w, (idx + 1) * seg_w):
            for y in range(height):
                canvas.putpixel((x, y), color)
    return canvas


st.set_page_config(page_title="Multi-Scene Lights AI", layout="centered")

# Check if onboarding is needed
if not smart_ui.onboarding_guide():
    st.stop()

st.title("🌟 智能多模态创作平台")
st.caption("AI 驱动的个性化内容创作 | 图片·音乐·视频·灯光·协作")

# Smart tips in sidebar
smart_ui.smart_tips_panel()

with st.sidebar:
    st.markdown("### 📊 后端画像")
    if st.button("探测后端延迟"):
        try:
            if cfg.endpoints.sdwebui_url:
                backend_registry.probe_latency("sdwebui", lambda: requests.get(cfg.endpoints.sdwebui_url, timeout=1))
            if cfg.endpoints.image_txt2img_url:
                backend_registry.probe_latency("img_http", lambda: requests.get(cfg.endpoints.image_txt2img_url, timeout=1))
            if cfg.endpoints.music_gen_url:
                backend_registry.probe_latency("music_http", lambda: requests.get(cfg.endpoints.music_gen_url, timeout=1))
        except Exception as e:
            st.warning(f"探测时发生异常: {e}")
    profiles = backend_registry.list()
    if profiles:
        for k, p in profiles.items():
            st.caption(f"{p.name} | 成本: {p.cost_per_call_usd or '-'} USD | 延迟: {p.avg_latency_ms and int(p.avg_latency_ms)} ms | 成功率: {p.success_rate and round(p.success_rate*100,1)}%")

    st.markdown("### 🏢 企业功能")
    st.caption("License 控制企业版特性")
    edition = "企业版" if license_server.is_enterprise() else "社区版"
    st.info(f"当前版本：{edition}")

# Personal analytics
smart_ui.usage_analytics_widget()

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "🎨 智能创作", "🖼️ 图片驱动", "🎵 音乐驱动", "🤖 AI编排", 
    "🏠 多房间", "🎬 视频合成", "🧠 LangGraph", "⚡ 设备控制", 
    "🔧 插件优化", "🤝 分享协作"
])

with tab1:
    st.markdown("### 🎯 智能创作工作台")
    
    # Smart theme selection
    theme = smart_ui.smart_theme_selector("tab1_theme")
    
    # Smart parameter panel
    params = smart_ui.smart_parameter_panel("tab1_params")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        duration = st.slider("音乐时长 (秒)", min_value=5, max_value=60, value=20, step=5)
        
        # Backend selection (simplified for smart UI)
        use_remote_img = st.checkbox("远程图片模型", value=bool(img_backend))
        use_remote_music = st.checkbox("远程音乐模型", value=bool(music_backend))
        use_sd = st.checkbox("使用SD WebUI", value=bool(sd_backend))
        
        gen = st.button("🚀 开始创作", type="primary")
    
    with col2:
        st.markdown("**🎤 语音输入**")
        wav_in = st.file_uploader("上传语音 (wav)", type=["wav"], key="stt_upload")
        if st.button("识别语音") and wav_in is not None:
            try:
                text = voice_backend.stt(wav_in.read(), STTParams(language="zh"))
                st.session_state["tab1_theme_value"] = text
                st.success("✅ 语音识别成功")
            except Exception as e:
                smart_ui.smart_error_handler(e, {"context": "语音识别"})

        # 企业功能示例：仅企业版显示审计导出按钮
        if license_server.is_enterprise():
            if st.button("导出审计日志"):
                try:
                    data = (BASE_DIR / "logs" / "audit.jsonl").read_text(encoding="utf-8")
                    st.download_button("下载审计日志", data=data, file_name="audit.jsonl")
                except Exception as e:
                    st.warning(f"导出失败：{e}")

    if gen and theme.strip():
        st.session_state["generation_timestamp"] = datetime.now().isoformat()
        
        # Progress tracking
        steps = ["图片生成", "音乐创作", "灯光设计", "完成"]
        progress_container = st.container()
        
        result_data = {"theme": theme}
        
        # 图片生成
        try:
            if use_sd and sd_backend:
                try:
                    img = sd_backend.txt2img(SDWebUIParams(prompt=theme, negative_prompt=negative, seed=None if seed == -1 else int(seed), steps=int(steps), cfg_scale=float(guidance), width=896, height=512))
                except Exception as e:
                    st.warning(f"SD WebUI 失败，尝试远程HTTP：{e}")
                    if use_remote_img and img_backend:
                        try:
                            img = img_backend.txt2img(Txt2ImgParams(prompt=theme, width=896, height=512, guidance=guidance))
                        except Exception as e2:
                            st.warning(f"远程HTTP失败，使用本地合成：{e2}")
                            img = generate_scene_image(theme, size=(896, 512))
                    else:
                        img = generate_scene_image(theme, size=(896, 512))
            elif use_remote_img and img_backend:
                try:
                    img = img_backend.txt2img(Txt2ImgParams(prompt=theme, width=896, height=512, guidance=guidance))
                except Exception as e:
                    st.warning(f"远程图片生成失败，使用本地合成：{e}")
                    img = generate_scene_image(theme, size=(896, 512))
            else:
                img = generate_scene_image(theme, size=(896, 512))
            st.subheader("场景图片")
            st.image(img, use_column_width=True)
            img_path = save_pil_image(img, OUTPUTS_DIR, "scene")
            st.download_button("下载图片", data=img_path.read_bytes(), file_name=img_path.name)
        except Exception as e:
            smart_ui.smart_error_handler(e, {"context": "图片生成"})
            img = generate_scene_image(theme, size=(896, 512))

        # 音乐生成
        st.subheader("背景音乐")
        if use_remote_music and music_backend:
            try:
                out_path = OUTPUTS_DIR / f"music_{abs(hash((theme, duration))) % 10**8}_remote.wav"
                wav_path = music_backend.generate(MusicGenParams(prompt=theme, duration_s=float(duration)), out_path)
            except Exception as e:
                st.warning(f"远程音乐生成失败，使用本地合成：{e}")
                wav_path = generate_music_from_theme(theme, duration_s=float(duration), out_dir=OUTPUTS_DIR)
        else:
            wav_path = generate_music_from_theme(theme, duration_s=float(duration), out_dir=OUTPUTS_DIR)
        st.audio(str(wav_path))
        st.download_button("下载音乐", data=wav_path.read_bytes(), file_name=wav_path.name)

        st.subheader("灯光节目")
        frames = generate_lighting_from_theme(theme)
        preview = render_lighting_preview(frames)
        st.image(preview, caption="色带预览（按顺序显示颜色与时长）", use_column_width=True)
        program_path = save_lighting_program(frames, OUTPUTS_DIR)
        st.download_button("下载灯光程序(JSON)", data=program_path.read_bytes(), file_name=program_path.name)
        wled_path = save_wled_preset(frames, OUTPUTS_DIR)
        st.download_button("下载WLED预设(JSON)", data=wled_path.read_bytes(), file_name=wled_path.name)

        # 结果反馈与自动调参
        fb = smart_ui.feedback_collector({"theme": theme, "image": str(img_path), "music": str(wav_path)})
        if fb:
            try:
                # 将评分馈送给个性化与优化器，生成调参建议
                suggestions = feedback_learner.suggest_improvements(theme)
                target = {"latency_ms": 1500, "throughput_rps": 1.0, "quality_score": 0.85, "memory_usage_mb": 2000}
                tune = model_optimizer.auto_tune(lambda x: x, [1,2,3], target, model_name="pipeline")
                st.success(f"已记录反馈，总改进建议：{len(tune['optimizations_tested'])}，预计提升 {tune['improvement_percentage']:.1f}%")
                with st.expander("查看优化建议"):
                    st.json(tune)
            except Exception as e:
                st.warning(f"自动调参建议生成失败：{e}")

with tab2:
    up = st.file_uploader("上传图片 (png/jpg)", type=["png", "jpg", "jpeg"]) 
    duration2 = st.slider("音乐时长 (秒)", min_value=5, max_value=60, value=20, step=5, key="dur2")
    run2 = st.button("从图片生成音乐与灯光")
    if run2 and up is not None:
        img = Image.open(io.BytesIO(up.read())).convert("RGB")
        st.subheader("上传图片")
        st.image(img, use_column_width=True)

        st.subheader("音乐（依据颜色情绪映射）")
        wav_path = generate_music_from_image(img, duration_s=float(duration2), out_dir=OUTPUTS_DIR)
        st.audio(str(wav_path))
        st.download_button("下载音乐", data=wav_path.read_bytes(), file_name=wav_path.name)

        st.subheader("灯光节目（依据主色调/对比度）")
        frames = generate_lighting_from_image(img)
        preview = render_lighting_preview(frames)
        st.image(preview, caption="色带预览", use_column_width=True)
        program_path = save_lighting_program(frames, OUTPUTS_DIR)
        st.download_button("下载灯光程序(JSON)", data=program_path.read_bytes(), file_name=program_path.name)
        wled_path = save_wled_preset(frames, OUTPUTS_DIR)
        st.download_button("下载WLED预设(JSON)", data=wled_path.read_bytes(), file_name=wled_path.name)

with tab3:
    up_wav = st.file_uploader("上传音乐 (WAV)", type=["wav"], key="wav_up")
    run3 = st.button("从音乐生成灯光")
    if run3 and up_wav is not None:
        wav_bytes = up_wav.read()
        wav_path = OUTPUTS_DIR / f"{Path(up_wav.name).stem}_uploaded.wav"
        wav_path.write_bytes(wav_bytes)
        try:
            frames = generate_lighting_from_wav(wav_path)
            preview = render_lighting_preview(frames)
            st.image(preview, caption="色带预览（音乐驱动）", use_column_width=True)
            json_name = f"lighting_from_{Path(up_wav.name).stem}.json"
            program_path = save_lighting_program(frames, OUTPUTS_DIR, filename=json_name)
            st.download_button("下载灯光程序(JSON)", data=program_path.read_bytes(), file_name=program_path.name)
            wled_path = save_wled_preset(frames, OUTPUTS_DIR, filename=f"wled_{Path(up_wav.name).stem}.json")
            st.download_button("下载WLED预设(JSON)", data=wled_path.read_bytes(), file_name=wled_path.name)
        except Exception as e:
            st.error(f"分析失败: {e}")

with tab4:
    st.subheader("多Agent编排（MVP）")
    mode = st.radio("选择工作流", ["文本→图片/音乐/灯光", "图片→音乐/灯光"])
    orch = Orchestrator(OrchestratorConfig(outputs_dir=OUTPUTS_DIR), logger, cache)
    if mode.startswith("文本"):
        t_prompt = st.text_input("输入主题/描述", value="睡眠")
        dur = st.slider("音乐时长 (秒)", 5, 60, 20, 5, key="orch_dur")
        if st.button("运行编排"):
            try:
                res = orch.run_from_text(t_prompt, music_seconds=float(dur))
                st.image(str(res["image"]))
                st.audio(str(res["music"]))
                st.download_button("下载灯光(JSON)", data=res["lighting"].read_bytes(), file_name=res["lighting"].name)
            except Exception as e:
                st.error(f"编排失败：{e}")

with tab5:
    st.subheader("多房间项目（v3 功能）")
    pname = st.text_input("项目名", value="demo")
    theme = st.text_input("主题", value="派对")
    num_rooms = st.number_input("房间数量", min_value=1, max_value=10, value=2, step=1)
    rooms: list[Room] = []
    for i in range(int(num_rooms)):
        st.markdown(f"房间 {i+1}")
        col1, col2, col3 = st.columns(3)
        with col1:
            rname = st.text_input(f"房间名_{i}", value=f"Room{i+1}")
        with col2:
            bri = st.slider(f"亮度_{i}", 0.0, 1.0, 1.0, 0.05)
        with col3:
            dly = st.number_input(f"初始延时(ms)_{i}", min_value=0, max_value=60000, value=0, step=100)
        rooms.append(Room(name=rname, brightness=float(bri), delay_ms=int(dly)))
    if st.button("编译并导出"):
        proj = Project(name=pname, theme=theme, rooms=rooms)
        per_room = compile_project(proj)
        st.success("已生成每个房间的节目")
        for rname, frames in per_room.items():
            preview = render_lighting_preview(frames)
            st.image(preview, caption=f"{rname} 预览", use_column_width=True)
            json_name = f"{pname}_{rname}_lighting.json"
            program_path = save_lighting_program(frames, OUTPUTS_DIR, filename=json_name)
            st.download_button(f"下载 {rname} 节目", data=program_path.read_bytes(), file_name=program_path.name)

with tab6:
    st.subheader("图片+音乐→视频 (MP4)")
    colv1, colv2 = st.columns(2)
    with colv1:
        up_img = st.file_uploader("上传图片", type=["png", "jpg", "jpeg"], key="v_img")
    with colv2:
        up_wav2 = st.file_uploader("上传音频 (wav/mp3)", type=["wav", "mp3"], key="v_aud")
    fps = st.slider("帧率", 15, 60, 30, 5)
    if st.button("合成视频") and up_img is not None and up_wav2 is not None:
        img_path = OUTPUTS_DIR / f"vid_{Path(up_img.name).name}"
        aud_path = OUTPUTS_DIR / f"vid_{Path(up_wav2.name).name}"
        img_path.write_bytes(up_img.read())
        aud_path.write_bytes(up_wav2.read())
        out_path = OUTPUTS_DIR / f"video_{Path(up_img.name).stem}_{Path(up_wav2.name).stem}.mp4"
        try:
            compose_image_music_to_mp4(img_path, aud_path, out_path, fps=int(fps))
            st.video(str(out_path))
            st.download_button("下载视频(MP4)", data=out_path.read_bytes(), file_name=out_path.name)
        except Exception as e:
            st.error(f"合成失败：{e}")

with tab7:
    st.subheader("LangGraph 编排（升级版）")
    goal = st.text_input("目标(主题)", value="派对")
    dur_lg = st.slider("音乐时长 (秒)", 5, 60, 20, 5, key="lgdur")
    use_llm = st.checkbox("启用 LLM 规划（需要 OpenAI API Key）", value=False)
    
    if st.button("执行 LangGraph"):
        with st.spinner("执行中..."):
            graph = build_graph(OUTPUTS_DIR, logger)
            state = graph.invoke({"goal": goal, "duration": float(dur_lg), "use_llm": use_llm})
            
            if "reasoning" in state:
                st.info(f"规划说明: {state['reasoning']}")
            
            if state.get("image_path"):
                st.subheader("生成图片")
                st.image(str(state["image_path"]))
                
            if state.get("music_path"):
                st.subheader("生成音乐")
                st.audio(str(state["music_path"]))
                
            if state.get("video_path"):
                st.subheader("合成视频")
                st.video(str(state["video_path"]))
                st.download_button("下载视频(MP4)", data=state["video_path"].read_bytes(), file_name=state["video_path"].name)
                
            col1, col2 = st.columns(2)
            with col1:
                lp = state.get("lighting_path")
                if lp:
                    st.download_button("下载灯光(JSON)", data=lp.read_bytes(), file_name=lp.name)
            with col2:
                wp = state.get("wled_path")
                if wp:
                    st.download_button("下载WLED(JSON)", data=wp.read_bytes(), file_name=wp.name)

with tab8:
    st.subheader("实时设备控制 + 用户反馈")
    
    # Device status
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Hue 控制器**")
        if hue_controller:
            st.success("已连接")
            if st.button("获取灯具列表"):
                lights = hue_controller.get_lights()
                st.json(lights)
        else:
            st.warning("未配置 (需要 HUE_BRIDGE_IP + HUE_USERNAME)")
    
    with col2:
        st.markdown("**WLED 控制器**")
        if wled_controller:
            st.success("已连接")
            if st.button("获取设备信息"):
                info = wled_controller.get_info()
                st.json(info)
            if st.button("紧急停止", type="secondary"):
                wled_controller.emergency_stop()
                st.success("已停止")
        else:
            st.warning("未配置 (需要 WLED_IP)")
    
    # Device control section
    st.markdown("**快速控制**")
    col3, col4, col5 = st.columns(3)
    with col3:
        r = st.slider("红色", 0, 255, 128, key="device_r")
    with col4:
        g = st.slider("绿色", 0, 255, 128, key="device_g")
    with col5:
        b = st.slider("蓝色", 0, 255, 128, key="device_b")
    
    col6, col7 = st.columns(2)
    with col6:
        if st.button("发送到 Hue") and hue_controller:
            # Send to first available light
            lights = hue_controller.get_lights()
            if lights:
                first_light = next(iter(lights.keys()))
                success = hue_controller.set_light_color(first_light, r, g, b)
                if success:
                    st.success("已发送到 Hue")
                else:
                    st.error("发送失败")
    with col7:
        if st.button("发送到 WLED") and wled_controller:
            success = wled_controller.set_color(r, g, b)
            if success:
                st.success("已发送到 WLED")
            else:
                st.error("发送失败")
    
    # Feedback section
    st.markdown("**用户反馈与学习**")
    feedback_stats = feedback_learner.get_feedback_stats()
    st.metric("总反馈数", feedback_stats["total"])
    st.metric("平均评分", f"{feedback_stats['avg_rating']:.2f}")
    
    # Feedback form
    with st.form("feedback_form"):
        user_input_fb = st.text_input("用户输入")
        rating = st.slider("评分", 1, 5, 3)
        comments = st.text_area("评论")
        submitted = st.form_submit_button("提交反馈")
        
        if submitted and user_input_fb:
            entry = FeedbackEntry(
                user_input=user_input_fb,
                system_output={"rating": rating},
                rating=rating,
                comments=comments,
                timestamp=datetime.utcnow().isoformat()
            )
            feedback_learner.record_feedback(entry)
            memory.add_turn(user_input_fb, {"rating": rating}, {"rating": rating, "comments": comments})
            st.success("反馈已记录")
    
    # Show suggestions
    if st.button("获取改进建议"):
        current_input = st.session_state.get("prompt_text", "睡眠")
        suggestions = feedback_learner.suggest_improvements(current_input)
        if suggestions["suggestions"]:
            st.markdown("**基于历史的建议:**")
            for i, sug in enumerate(suggestions["suggestions"]):
                st.markdown(f"{i+1}. 相似输入: '{sug['similar_input']}' (评分: {sug['rating']}, 相似度: {sug['similarity']:.2f})")
        else:
            st.info("暂无相关建议")

with tab9:
    st.subheader("插件系统 + 模型优化")
    
    # Plugin section
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**插件管理**")
        available_plugins = ["party_director", "content_workshop", "healing_space"]
        selected_plugin = st.selectbox("选择插件", available_plugins)
        
        if st.button("加载插件"):
            config = {
                "venue_type": "home",
                "guest_count": 20,
                "brand_guidelines": {"color_palette": ["#FF6B6B", "#4ECDC4"], "tone_of_voice": "友好专业"},
                "target_platforms": ["instagram", "tiktok"]
            }
            # Mock plugin loading
            st.success(f"插件 {selected_plugin} 加载成功")
            st.json({"plugin": selected_plugin, "status": "loaded", "capabilities": ["party_orchestration", "content_generation"]})
    
    with col2:
        st.markdown("**插件执行**")
        if selected_plugin == "party_director":
            if st.button("生成派对方案"):
                st.json({
                    "theme": "生日派对",
                    "phases": ["预热", "高潮", "收尾"],
                    "equipment": ["音响", "灯光", "投影"],
                    "timeline": "3小时"
                })
        elif selected_plugin == "content_workshop":
            if st.button("生成内容计划"):
                st.json({
                    "content_items": 10,
                    "platforms": ["instagram", "tiktok"],
                    "themes": ["产品展示", "用户故事"],
                    "posting_schedule": "7天计划"
                })
    
    # Model optimization section
    st.markdown("**模型性能优化**")
    col3, col4 = st.columns(2)
    with col3:
        target_latency = st.slider("目标延迟 (ms)", 100, 5000, 1000)
        target_quality = st.slider("目标质量分数", 0.5, 1.0, 0.8, 0.05)
    
    with col4:
        if st.button("性能分析"):
            # Mock performance analysis
            current_metrics = {
                "latency_ms": 1500,
                "throughput_rps": 0.8,
                "quality_score": 0.75,
                "memory_usage_mb": 1200
            }
            st.json(current_metrics)
        
        if st.button("自动优化"):
            # Mock optimization
            optimization_result = {
                "applied_strategies": ["dynamic_batching", "cache_optimization"],
                "improvement": "35%",
                "new_latency_ms": 975,
                "new_quality_score": 0.82
            }
            st.success("优化完成!")
            st.json(optimization_result)
    
    # Performance report
    if st.button("生成性能报告"):
        performance_report = model_optimizer.get_performance_report()
        if "error" not in performance_report:
            st.markdown("**性能报告**")
            st.json(performance_report)
        else:
            st.info("暂无性能数据，请先运行一些模型推理")
    
    # Available capabilities
    st.markdown("**系统能力清单**")
    capabilities = [
        "多模态生成 (图片/音乐/视频/灯光)",
        "LLM 智能规划与编排",
        "实时设备控制 (Hue/WLED)",
        "用户反馈学习",
        "插件化扩展",
        "性能监控与优化",
        "多房间项目管理",
        "对话记忆与上下文"
    ]
    for cap in capabilities:
        st.checkbox(cap, value=True, disabled=True)

with tab10:
    st.subheader("🤝 分享与协作")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📤 分享项目**")
        
        if st.button("分享当前作品"):
            # Mock sharing current work
            share_id = sharing_manager.share_project(
                creator_id=smart_ui.user_id,
                creator_name="用户",
                title=f"AI创作 - {theme if 'theme' in locals() else '未命名'}",
                content={"type": "multi_modal", "theme": theme if 'theme' in locals() else ""},
                description="通过AI创作的多模态内容",
                tags=["AI创作", "多模态"],
                is_public=True
            )
            st.success(f"✅ 项目已分享! ID: {share_id}")
            share_link = sharing_manager.generate_share_link(share_id)
            st.code(share_link)
        
        # Project export
        st.markdown("**💾 导出项目**")
        export_format = st.selectbox("导出格式", ["JSON", "ZIP包", "云端链接"])
        if st.button("导出"):
            st.download_button(
                "下载项目文件",
                data=json.dumps({"format": export_format, "exported_at": datetime.now().isoformat()}),
                file_name=f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        st.markdown("**🌟 热门作品**")
        
        # Browse shared projects
        trending_tags = sharing_manager.get_trending_tags(5)
        if trending_tags:
            st.markdown("**🔥 热门标签**")
            for tag_info in trending_tags:
                st.badge(f"{tag_info['tag']} ({tag_info['count']})")
        
        # Mock shared projects
        mock_projects = [
            {"title": "温馨家居灯光", "creator": "设计师小王", "likes": 128, "tags": ["家居", "温馨"]},
            {"title": "派对狂欢套装", "creator": "活动策划", "likes": 95, "tags": ["派对", "音乐"]},
            {"title": "禅意冥想空间", "creator": "瑜伽教练", "likes": 76, "tags": ["禅修", "冥想"]}
        ]
        
        for project in mock_projects:
            with st.container():
                st.markdown(f"**{project['title']}**")
                st.caption(f"👤 {project['creator']} | ❤️ {project['likes']} | 🏷️ {', '.join(project['tags'])}")
                col_view, col_like = st.columns(2)
                with col_view:
                    if st.button("查看", key=f"view_{project['title']}"):
                        st.info("正在加载项目详情...")
                with col_like:
                    if st.button("👍", key=f"like_{project['title']}"):
                        st.success("已点赞!")
    
    # Collaboration section
    st.markdown("---")
    st.markdown("**👥 实时协作**")
    
    col3, col4 = st.columns(2)
    with col3:
        session_id = st.text_input("协作会话ID", placeholder="输入或创建新会话")
        if st.button("创建协作会话"):
            new_session = sharing_manager.create_collaboration_session("demo_project", smart_ui.user_id)
            st.success(f"✅ 协作会话已创建: {new_session}")
            st.session_state["collab_session"] = new_session
    
    with col4:
        if st.button("加入协作会话") and session_id:
            success = sharing_manager.join_collaboration_session(session_id, smart_ui.user_id)
            if success:
                st.success("✅ 已加入协作会话")
                st.session_state["collab_session"] = session_id
            else:
                st.error("❌ 无法加入会话")
    
    # Mock collaboration interface
    if "collab_session" in st.session_state:
        st.markdown(f"**🔗 当前协作会话: {st.session_state['collab_session']}**")
        
        # Chat interface
        chat_msg = st.text_input("团队聊天", placeholder="在这里输入消息...")
        if st.button("发送") and chat_msg:
            sharing_manager.update_collaboration_state(
                st.session_state['collab_session'],
                smart_ui.user_id,
                {"chat_message": chat_msg}
            )
            st.success("消息已发送")
        
        # Shared state
        st.markdown("**🔄 共享状态**")
        shared_theme = st.text_input("共享主题", value="")
        if st.button("更新共享状态"):
            sharing_manager.update_collaboration_state(
                st.session_state['collab_session'],
                smart_ui.user_id,
                {"current_theme": shared_theme}
            )
            st.success("状态已更新")
    else:
        upi = st.file_uploader("上传图片", type=["png", "jpg", "jpeg"], key="orch_img")
        dur2 = st.slider("音乐时长 (秒)", 5, 60, 20, 5, key="orch_dur2")
        if st.button("运行编排(图片)") and upi is not None:
            try:
                img = Image.open(io.BytesIO(upi.read())).convert("RGB")
                res = orch.run_from_image(img, music_seconds=float(dur2))
                st.audio(str(res["music"]))
                st.download_button("下载灯光(JSON)", data=res["lighting"].read_bytes(), file_name=res["lighting"].name)
            except Exception as e:
                st.error(f"编排失败：{e}")

# Add Tasks tab at the end
extra_tab = st.tabs(["📦 任务队列"])[0]
with extra_tab:
    tq = TaskQueue(BASE_DIR)
    def _submit_cb(t):
        logger.log({"event": "task.submitted", "id": t.id, "kind": t.kind})
    from mscen.ui.tasks_panel import tasks_panel
    tasks_panel(BASE_DIR, _submit_cb)



