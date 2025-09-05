## 外部集成设计

### 图像生成
- 本地或远程 REST 服务：`POST /txt2img`，参数 prompt/seed/size
- 返回 PNG/JPEG；失败回退到合成版

### 音乐生成
- 远程服务：`POST /musicgen`，参数 prompt/duration/style
- 返回 WAV/MP3；失败回退到合成器

### 语音
- 识别：Whisper/Edge STT，本地/云端均可
- 播报：Edge TTS（SSML 控制情感/语速）

### 灯光控制
- Hue：REST/Bridge；Yeelight：局域网协议；WLED：HTTP/JSON 或 UDP 实时
- DMX/sACN：通过 Python 库（ola/pyartnet）或自实现协议
- 导出格式：
  - JSON（当前）
  - CSV（时间、R、G、B）
  - WLED Preset JSON
  - DMX Cue List（后续）


