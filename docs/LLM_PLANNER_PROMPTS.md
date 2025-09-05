## LLM 规划器 Prompts 与工具描述

### 系统 Prompt
位置：`mscen/agents/llm_planner.py`

核心要素：
- 角色定位：多模态内容创作规划师
- 可用工具：image/music/lighting/video/wled/voice_tts
- 安全约束：拒绝暴力/仇恨/成人/版权争议内容
- 输出格式：JSON（safe/plan/theme/reasoning）

### 工具清单
- `image`: 生成场景图片（文本→图片）
- `music`: 生成背景音乐（主题→音乐）
- `lighting`: 生成灯光节目（主题→RGB帧序列）
- `video`: 合成视频（图片+音乐→MP4）
- `wled`: 导出WLED预设（灯光帧→WLED JSON）
- `voice_tts`: 语音播报（文本→音频）

### 规划策略
- 基础流程：image → music → lighting → video
- 条件分支：根据用户需求调整工具顺序
- 错误处理：LLM 失败时降级到启发式规划

### 优化方向
- 增加工具：STT/设备控制/剪辑/字幕
- 多轮对话：用户反馈驱动的迭代优化
- 上下文学习：基于历史成功案例的少样本学习
