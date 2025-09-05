from __future__ import annotations

from typing import Dict, Any, List, Optional, Callable
import streamlit as st
from pathlib import Path


class SmartUI:
    def __init__(self, personalization_engine=None):
        self.personalization_engine = personalization_engine
        self.user_id = self._get_user_id()
    
    def _get_user_id(self) -> str:
        """Get or create user ID for session"""
        if "user_id" not in st.session_state:
            import uuid
            st.session_state.user_id = str(uuid.uuid4())[:8]
        return st.session_state.user_id
    
    def smart_theme_selector(self, key: str = "theme") -> str:
        """Smart theme selector with personalized recommendations"""
        if self.personalization_engine:
            recommendations = self.personalization_engine.get_recommendations(self.user_id)
            suggested_themes = [r["theme"] for r in recommendations.get("themes", [])]
            
            if suggested_themes:
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown("**🎯 为您推荐**")
                    selected_rec = st.selectbox(
                        "基于您的使用习惯推荐",
                        suggested_themes,
                        key=f"{key}_recommended"
                    )
                    if st.button("使用推荐", key=f"{key}_use_rec"):
                        st.session_state[f"{key}_value"] = selected_rec
                        return selected_rec
                
                with col2:
                    st.markdown("**💡 推荐理由**")
                    for rec in recommendations["themes"][:3]:
                        if rec["theme"] == selected_rec:
                            st.caption(f"🔥 {rec['reason']}")
                            st.progress(rec["confidence"])
                            break
        
        # Standard theme selector
        st.markdown("**🎨 主题选择**")
        all_themes = ["睡眠", "圣诞节", "打雷", "浪漫", "派对", "禅修", "现代简约", "自然风光", "科技未来"]
        
        # Show frequently used themes first
        if self.personalization_engine:
            config = self.personalization_engine.get_adaptive_ui_config(self.user_id)
            quick_themes = config.get("quick_access_themes", [])
            if quick_themes:
                st.markdown("**⚡ 常用主题**")
                cols = st.columns(min(len(quick_themes), 5))
                for i, theme in enumerate(quick_themes):
                    with cols[i]:
                        if st.button(theme, key=f"{key}_quick_{i}"):
                            st.session_state[f"{key}_value"] = theme
                            return theme
        
        selected = st.selectbox("选择主题", all_themes, key=f"{key}_main")
        st.session_state[f"{key}_value"] = selected
        return selected
    
    def smart_parameter_panel(self, key: str = "params") -> Dict[str, Any]:
        """Smart parameter panel that adapts to user skill level"""
        params = {}
        
        # Get user config
        show_advanced = False
        if self.personalization_engine:
            config = self.personalization_engine.get_adaptive_ui_config(self.user_id)
            show_advanced = config.get("show_advanced_options", False)
        
        if not show_advanced:
            # Simplified interface for beginners
            st.markdown("**⚙️ 基础设置**")
            quality = st.select_slider(
                "质量偏好", 
                options=["快速", "平衡", "高质量"], 
                value="平衡",
                key=f"{key}_quality"
            )
            
            params["quality_mode"] = quality
            
            # Auto-configure based on quality choice
            if quality == "快速":
                params.update({"steps": 15, "guidance": 3.0, "resolution": 512})
            elif quality == "平衡":
                params.update({"steps": 25, "guidance": 5.0, "resolution": 768})
            else:  # 高质量
                params.update({"steps": 35, "guidance": 7.0, "resolution": 1024})
            
        else:
            # Advanced interface for experienced users
            st.markdown("**🔧 高级参数**")
            col1, col2 = st.columns(2)
            
            with col1:
                params["steps"] = st.slider("生成步数", 10, 50, 25, key=f"{key}_steps")
                params["guidance"] = st.slider("引导强度", 1.0, 12.0, 5.0, key=f"{key}_guidance")
            
            with col2:
                params["resolution"] = st.selectbox("分辨率", [512, 768, 1024], index=1, key=f"{key}_res")
                params["seed"] = st.number_input("随机种子", value=-1, key=f"{key}_seed")
        
        return params
    
    def progress_tracker(self, steps: List[str], current_step: int = 0) -> None:
        """Enhanced progress tracker with ETA"""
        progress_container = st.container()
        
        with progress_container:
            # Progress bar
            progress_value = (current_step + 1) / len(steps)
            st.progress(progress_value)
            
            # Current step info
            if current_step < len(steps):
                st.markdown(f"**正在执行:** {steps[current_step]} ({current_step + 1}/{len(steps)})")
            
            # Steps visualization
            cols = st.columns(len(steps))
            for i, step in enumerate(steps):
                with cols[i]:
                    if i < current_step:
                        st.success(f"✅ {step}")
                    elif i == current_step:
                        st.info(f"🔄 {step}")
                    else:
                        st.gray(f"⏳ {step}")
    
    def smart_error_handler(self, error: Exception, context: Dict[str, Any] = None) -> None:
        """User-friendly error handling with suggestions"""
        error_type = type(error).__name__
        error_msg = str(error)
        
        # User-friendly error messages
        friendly_messages = {
            "ConnectionError": "🌐 网络连接问题，请检查网络设置",
            "TimeoutError": "⏰ 请求超时，服务器可能繁忙，请稍后重试",
            "FileNotFoundError": "📁 文件未找到，请检查文件路径",
            "ValueError": "❗ 输入参数有误，请检查输入内容",
            "RuntimeError": "⚠️ 运行时错误，请尝试调整参数重新生成"
        }
        
        friendly_msg = friendly_messages.get(error_type, f"❌ 发生错误: {error_msg}")
        
        with st.error(friendly_msg):
            # Error details in expander
            with st.expander("🔍 错误详情"):
                st.code(f"{error_type}: {error_msg}")
                if context:
                    st.json(context)
            
            # Suggestions
            suggestions = self._get_error_suggestions(error_type, context)
            if suggestions:
                st.markdown("**💡 建议解决方案:**")
                for suggestion in suggestions:
                    st.markdown(f"• {suggestion}")
    
    def _get_error_suggestions(self, error_type: str, context: Dict[str, Any] = None) -> List[str]:
        """Get contextual error suggestions"""
        suggestions = []
        
        if error_type == "ConnectionError":
            suggestions = [
                "检查网络连接是否正常",
                "确认服务器地址配置正确",
                "尝试使用本地生成模式"
            ]
        elif error_type == "TimeoutError":
            suggestions = [
                "降低生成质量设置以减少处理时间",
                "稍后重试，避开服务器繁忙时段",
                "检查网络稳定性"
            ]
        elif error_type == "ValueError":
            suggestions = [
                "检查输入文本是否包含特殊字符",
                "确认参数值在有效范围内",
                "尝试使用默认参数设置"
            ]
        elif error_type == "RuntimeError":
            suggestions = [
                "尝试重新启动应用程序",
                "清理缓存文件后重试",
                "检查系统资源是否充足"
            ]
        
        return suggestions
    
    def feedback_collector(self, result_data: Dict[str, Any], key: str = "feedback") -> Optional[Dict[str, Any]]:
        """Collect user feedback on results"""
        st.markdown("---")
        st.markdown("**📝 您的反馈很重要**")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            rating = st.select_slider(
                "整体满意度",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: "⭐" * x,
                value=3,
                key=f"{key}_rating"
            )
            
            aspects = st.multiselect(
                "哪些方面表现良好？",
                ["图片质量", "音乐匹配", "灯光效果", "生成速度", "整体创意"],
                key=f"{key}_aspects"
            )
            
            comments = st.text_area(
                "其他建议或意见",
                placeholder="告诉我们如何改进...",
                key=f"{key}_comments"
            )
        
        with col2:
            st.markdown("**🎁 反馈奖励**")
            st.info("提供反馈可获得:\n• 个性化推荐优化\n• 优先体验新功能\n• 专属创作模板")
            
            if st.button("提交反馈", key=f"{key}_submit"):
                feedback_data = {
                    "rating": rating,
                    "positive_aspects": aspects,
                    "comments": comments,
                    "result_data": result_data,
                    "timestamp": st.session_state.get("generation_timestamp"),
                    "user_id": self.user_id
                }
                
                # Learn from feedback
                if self.personalization_engine:
                    self.personalization_engine.learn_from_interaction(
                        self.user_id, 
                        {**result_data, "rating": rating}
                    )
                
                st.success("✅ 感谢您的反馈！我们会持续改进。")
                return feedback_data
        
        return None
    
    def onboarding_guide(self) -> bool:
        """Interactive onboarding for new users"""
        if "onboarding_completed" in st.session_state:
            return True
        
        st.markdown("## 🎉 欢迎使用多模态 AI 创作平台！")
        
        # Progress indicator
        if "onboarding_step" not in st.session_state:
            st.session_state.onboarding_step = 0
        
        steps = [
            "了解功能", "选择偏好", "体验创作", "连接设备"
        ]
        
        current_step = st.session_state.onboarding_step
        self.progress_tracker(steps, current_step)
        
        if current_step == 0:
            st.markdown("### 🌟 平台功能概览")
            
            features = [
                ("🎨 图片生成", "根据文字描述生成精美场景图片"),
                ("🎵 音乐创作", "智能匹配主题的背景音乐"),
                ("💡 灯光设计", "同步的智能灯光节目"),
                ("🎬 视频合成", "图片+音乐自动合成视频"),
                ("🏠 多房间控制", "批量管理多个空间的灯光"),
                ("🤖 AI 助手", "智能规划和个性化推荐")
            ]
            
            for feature, desc in features:
                st.markdown(f"**{feature}**: {desc}")
            
            if st.button("下一步：设置偏好", key="onboarding_next_0"):
                st.session_state.onboarding_step = 1
                st.rerun()
        
        elif current_step == 1:
            st.markdown("### ⚙️ 个性化设置")
            
            col1, col2 = st.columns(2)
            with col1:
                preferred_themes = st.multiselect(
                    "您感兴趣的主题",
                    ["派对聚会", "温馨家居", "工作专注", "休息放松", "节日庆典"],
                    key="onboarding_themes"
                )
                
                experience_level = st.selectbox(
                    "技术使用经验",
                    ["新手", "一般", "熟练"],
                    key="onboarding_experience"
                )
            
            with col2:
                quality_preference = st.selectbox(
                    "生成偏好",
                    ["速度优先", "平衡", "质量优先"],
                    key="onboarding_quality"
                )
                
                device_types = st.multiselect(
                    "拥有的智能设备",
                    ["Hue 灯具", "WLED 灯带", "投影仪", "智能音响"],
                    key="onboarding_devices"
                )
            
            col3, col4 = st.columns(2)
            with col3:
                if st.button("上一步", key="onboarding_prev_1"):
                    st.session_state.onboarding_step = 0
                    st.rerun()
            with col4:
                if st.button("下一步：体验创作", key="onboarding_next_1"):
                    # Save preferences
                    if self.personalization_engine:
                        for theme in preferred_themes:
                            self.personalization_engine.update_preference(self.user_id, "theme", theme, 0.8)
                        
                        profile = self.personalization_engine.get_or_create_profile(self.user_id)
                        profile.preferred_speed = {"速度优先": "fast", "平衡": "balanced", "质量优先": "quality"}[quality_preference]
                        profile.quality_threshold = {"速度优先": 0.6, "平衡": 0.8, "质量优先": 0.9}[quality_preference]
                    
                    st.session_state.onboarding_step = 2
                    st.rerun()
        
        elif current_step == 2:
            st.markdown("### 🎯 快速体验")
            st.markdown("让我们创作您的第一个作品！")
            
            demo_theme = st.selectbox(
                "选择一个主题开始体验",
                ["温馨家居", "派对庆典", "禅意空间"],
                key="onboarding_demo_theme"
            )
            
            if st.button("生成示例作品", key="onboarding_generate"):
                with st.spinner("正在为您生成..."):
                    # Mock generation
                    st.success("🎉 生成完成！")
                    st.markdown("这就是您的第一个 AI 创作作品。您可以:")
                    st.markdown("• 调整参数重新生成")
                    st.markdown("• 下载保存到本地")
                    st.markdown("• 发送到智能设备")
                    
                    col5, col6 = st.columns(2)
                    with col5:
                        if st.button("重新生成", key="onboarding_regenerate"):
                            st.info("🔄 正在重新生成...")
                    with col6:
                        if st.button("完成体验", key="onboarding_next_2"):
                            st.session_state.onboarding_step = 3
                            st.rerun()
        
        elif current_step == 3:
            st.markdown("### 🏁 设置完成")
            st.markdown("🎊 恭喜！您已经掌握了基本使用方法。")
            
            st.markdown("**接下来您可以：**")
            st.markdown("• 📱 在各个功能页签中探索更多能力")
            st.markdown("• ⚙️ 在设置中连接您的智能设备")
            st.markdown("• 💡 查看个性化推荐获得灵感")
            st.markdown("• 🔄 通过反馈帮助我们改进")
            
            if st.button("开始使用", key="onboarding_complete"):
                st.session_state.onboarding_completed = True
                st.balloons()
                st.rerun()
        
        return False
    
    def smart_tips_panel(self) -> None:
        """Context-aware tips panel"""
        if self.personalization_engine:
            profile = self.personalization_engine.get_or_create_profile(self.user_id)
            opportunities = self.personalization_engine._identify_growth_opportunities(profile)
            
            if opportunities:
                with st.sidebar:
                    st.markdown("### 💡 智能提示")
                    for tip in opportunities[:3]:
                        st.info(tip)
    
    def usage_analytics_widget(self) -> None:
        """Personal usage analytics"""
        if not self.personalization_engine:
            return
        
        profile = self.personalization_engine.get_or_create_profile(self.user_id)
        insights = self.personalization_engine.export_insights(self.user_id)
        
        with st.expander("📊 我的创作统计"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "总创作数", 
                    profile.usage_stats.get("total_generations", 0)
                )
            
            with col2:
                st.metric(
                    "用户等级", 
                    insights["user_segment"].replace("_", " ").title()
                )
            
            with col3:
                engagement = insights["engagement_score"]
                st.metric(
                    "活跃度", 
                    f"{engagement:.1%}",
                    delta=f"+{engagement*10:.0f}%" if engagement > 0.5 else None
                )
            
            # Preferences breakdown
            if profile.preferences:
                st.markdown("**🎨 偏好分布**")
                categories = {}
                for pref in profile.preferences:
                    if pref.category not in categories:
                        categories[pref.category] = 0
                    categories[pref.category] += pref.confidence
                
                for category, score in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                    st.progress(min(1.0, score/5), text=f"{category}: {score:.1f}")
