from __future__ import annotations

# Minimal MCP-like scaffold via FastAPI exposing tools endpoints
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from mscen.image_gen import generate_scene_image
from mscen.music_gen import generate_music_from_theme
from mscen.lighting import generate_lighting_from_theme, save_lighting_program
from mscen.wled import save_wled_preset
from mscen.video import compose_image_music_to_mp4


app = FastAPI(title="MCP Tools Server")
BASE_DIR = Path(__file__).resolve().parents[1]
OUT = BASE_DIR / "outputs"
OUT.mkdir(parents=True, exist_ok=True)


class Txt2ImgReq(BaseModel):
    prompt: str
    width: int = 896
    height: int = 512


@app.post("/tools/txt2img")
def tool_txt2img(req: Txt2ImgReq):
    img = generate_scene_image(req.prompt, size=(req.width, req.height))
    path = OUT / f"mcp_img_{abs(hash(req.prompt)) % 10**8}.png"
    img.save(path)
    return JSONResponse({"ok": True, "path": str(path)})


class MusicReq(BaseModel):
    prompt: str
    duration: float = 20.0


@app.post("/tools/music")
def tool_music(req: MusicReq):
    path = generate_music_from_theme(req.prompt, duration_s=float(req.duration), out_dir=OUT)
    return JSONResponse({"ok": True, "path": str(path)})


class LightingReq(BaseModel):
    prompt: str


@app.post("/tools/lighting")
def tool_lighting(req: LightingReq):
    frames = generate_lighting_from_theme(req.prompt)
    path = save_lighting_program(frames, OUT, filename=f"mcp_lighting_{abs(hash(req.prompt)) % 10**8}.json")
    return JSONResponse({"ok": True, "frames": frames, "path": str(path)})


@app.post("/tools/wled")
def tool_wled(req: LightingReq):
    frames = generate_lighting_from_theme(req.prompt)
    path = save_wled_preset(frames, OUT, filename=f"mcp_wled_{abs(hash(req.prompt)) % 10**8}.json")
    return JSONResponse({"ok": True, "path": str(path)})


class VideoReq(BaseModel):
    image_path: str
    audio_path: str
    fps: int = 30


@app.post("/tools/video")
def tool_video(req: VideoReq):
    out_path = OUT / f"mcp_video_{abs(hash((req.image_path, req.audio_path))) % 10**8}.mp4"
    result_path = compose_image_music_to_mp4(Path(req.image_path), Path(req.audio_path), out_path, fps=req.fps)
    return JSONResponse({"ok": True, "path": str(result_path)})


class TTSReq(BaseModel):
    text: str
    voice: str = "zh-CN-XiaoxiaoNeural"


@app.post("/tools/voice_tts")
def tool_voice_tts(req: TTSReq):
    # Mock TTS - returns path to generated audio
    out_path = OUT / f"mcp_tts_{abs(hash(req.text)) % 10**8}.mp3"
    # In real implementation, call TTS and save to out_path
    out_path.write_text(f"TTS placeholder for: {req.text}")
    return JSONResponse({"ok": True, "path": str(out_path), "text": req.text})


