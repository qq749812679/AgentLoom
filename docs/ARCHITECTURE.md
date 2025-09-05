## 架构概览

MVP 由前端 UI（Streamlit）和若干 Python 模块组成：

- `app.py`: 前端交互，编排调用
- `mscen/image_gen.py`: 主题→合成图片（可替换为扩散模型推理）
- `mscen/music_gen.py`: 主题→合成音乐（可替换为音乐大模型）
- `mscen/image_to_music.py`: 图片→合成音乐（依据亮度、对比度映射）
- `mscen/lighting.py`: 主题/图片→灯光节目（后续扩展至 DMX/WLED）
- `mscen/utils/*`: 通用工具

数据流：
1. 文本/语音输入（语音暂留接口）解析为主题字符串
2. 主题驱动图片、音乐与灯光生成；或图片驱动音乐与灯光
3. 结果落盘到 `outputs/` 并支持下载

可替换点：
- 图片：接入 `Flux/SDXL`，以 REST/gRPC 或本地引擎推理
- 音乐：接入 `MusicGen/AudioLDM/Omni` 推理
- 语音：Whisper/Edge STT；Edge TTS 合成播报
- 灯光：接入 Hue/Yeelight/DMX/WLED 实设备控制


