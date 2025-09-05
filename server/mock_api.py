from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import Response

from PIL import Image

from mscen.image_gen import generate_scene_image
from mscen.music_gen import generate_music_from_theme


app = FastAPI(title="Mock Model API")


@app.post("/txt2img")
async def txt2img(prompt: str, seed: Optional[int] = None, width: int = 896, height: int = 512, guidance: float = 5.0):
    img = generate_scene_image(prompt, size=(width, height), seed=seed)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return Response(content=buf.getvalue(), media_type="image/png")


@app.post("/musicgen")
async def musicgen(prompt: str, duration: float = 20.0, style: Optional[str] = None):
    tmp = Path("/tmp")
    tmp.mkdir(parents=True, exist_ok=True)
    out_path = tmp / "mock_music.wav"
    wav_path = generate_music_from_theme(prompt, duration_s=duration, out_dir=tmp)
    return Response(content=wav_path.read_bytes(), media_type="audio/wav")


@app.post("/stt")
async def stt(file: UploadFile = File(...), language: Optional[str] = Form(None)):
    # 模拟转写
    return {"text": "这是一个语音转写示例。"}


@app.post("/tts")
async def tts(text: str, voice: Optional[str] = None):
    # 生成 1 秒 440Hz 正弦波作为占位
    import numpy as np
    from scipy.io import wavfile
    sr = 22050
    t = np.arange(int(sr * 1.0)) / sr
    audio = (0.2 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)
    buf = BytesIO()
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        wavfile.write(f.name, sr, (audio * 32767).astype('int16'))
        data = Path(f.name).read_bytes()
    return Response(content=data, media_type="audio/wav")


