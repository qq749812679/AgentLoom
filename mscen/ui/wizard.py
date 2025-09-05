from __future__ import annotations

from pathlib import Path
import streamlit as st
from ..core.env_writer import update_env


def onboarding_wizard(base_dir: Path) -> bool:
    st.markdown("## 🧭 首次使用向导")
    st.caption("一键配置 API 与设备参数，推荐默认值即可开始体验")

    tabs = st.tabs(["模型与API", "设备与连接", "确认与保存"])

    with tabs[0]:
        st.subheader("模型与API 配置")
        col1, col2 = st.columns(2)
        with col1:
            openai_api_key = st.text_input("OpenAI API Key", type="password")
            image_http = st.text_input("图片生成(HTTP)", value="http://localhost:8000/txt2img")
            sdwebui = st.text_input("Stable Diffusion WebUI", value="http://localhost:7860")
        with col2:
            music_http = st.text_input("音乐生成(HTTP)", value="http://localhost:8000/musicgen")
            stt_url = st.text_input("语音识别(STT)", value="http://localhost:8000/stt")
            tts_url = st.text_input("语音合成(TTS)", value="http://localhost:8000/tts")

        st.session_state._wiz_api = dict(
            OPENAI_API_KEY=openai_api_key or "",
            IMAGE_TXT2IMG_URL=image_http or "",
            SDWEBUI_URL=sdwebui or "",
            MUSIC_GEN_URL=music_http or "",
            STT_URL=stt_url or "",
            TTS_URL=tts_url or "",
        )

    with tabs[1]:
        st.subheader("设备与连接")
        col1, col2, col3 = st.columns(3)
        with col1:
            hue_ip = st.text_input("Hue Bridge IP", placeholder="192.168.x.x")
            hue_user = st.text_input("Hue 用户名")
        with col2:
            wled_ip = st.text_input("WLED IP", placeholder="192.168.x.x")
        with col3:
            debug = st.checkbox("调试模式", value=True)
            cache_enabled = st.checkbox("启用缓存", value=True)

        st.session_state._wiz_dev = dict(
            HUE_BRIDGE_IP=hue_ip or "",
            HUE_USERNAME=hue_user or "",
            WLED_IP=wled_ip or "",
            DEBUG="true" if debug else "false",
            CACHE_ENABLED="true" if cache_enabled else "false",
            LOG_LEVEL="INFO",
        )

    with tabs[2]:
        st.subheader("确认与保存")
        st.write("请确认以下配置：")
        st.json({**st.session_state.get("_wiz_api", {}), **st.session_state.get("_wiz_dev", {})})
        if st.button("写入 .env 并开始使用", type="primary"):
            kv = {**st.session_state.get("_wiz_api", {}), **st.session_state.get("_wiz_dev", {})}
            update_env(base_dir, kv)
            st.session_state.onboarding_completed = True
            st.success("已写入 .env，正在进入主界面...")
            st.rerun()

    return False 