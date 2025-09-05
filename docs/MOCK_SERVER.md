## 模型 Mock Server（FastAPI）

用于本地演示与联调连接器（图片/音乐/STT/TTS）。

### 启动
```bash
cd multi-scen
uvicorn server.mock_api:app --reload --port 8001
```

### 配置 .env
```
IMAGE_TXT2IMG_URL=http://localhost:8001
MUSIC_GEN_URL=http://localhost:8001
STT_URL=http://localhost:8001
TTS_URL=http://localhost:8001
```

### 接口
- POST /txt2img: 返回基于主题的合成 PNG
- POST /musicgen: 返回简单合成的 WAV
- POST /stt: 返回示例文本
- POST /tts: 返回 1 秒 beep 的 WAV


