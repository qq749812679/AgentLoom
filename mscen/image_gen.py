import random
from typing import Tuple
from PIL import Image, ImageDraw

from .utils.colors import palette_for_theme, horizontal_gradient


def _draw_sleep(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    cx, cy, r = int(width * 0.8), int(height * 0.25), int(min(width, height) * 0.12)
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 200))
    draw.ellipse((cx - r + 18, cy - r, cx + r + 18, cy + r), fill=None, outline=None)
    for _ in range(60):
        x = random.randint(0, width - 1)
        y = random.randint(0, int(height * 0.6))
        s = random.randint(1, 2)
        draw.rectangle((x, y, x + s, y + s), fill=(240, 240, 240))


def _draw_christmas(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    tree_w = int(width * 0.18)
    tree_h = int(height * 0.45)
    x0 = int(width * 0.15)
    y0 = int(height * 0.45)
    draw.polygon([(x0, y0 + tree_h), (x0 + tree_w // 2, y0), (x0 + tree_w, y0 + tree_h)], fill=(0, 140, 0))
    draw.rectangle((x0 + tree_w // 2 - 10, y0 + tree_h, x0 + tree_w // 2 + 10, y0 + tree_h + 40), fill=(120, 70, 0))
    for _ in range(25):
        x = random.randint(x0 + 10, x0 + tree_w - 10)
        y = random.randint(y0 + 10, y0 + tree_h - 10)
        draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(220, 0, 0))
    for _ in range(200):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        draw.point((x, y), fill=(240, 240, 255))


def _draw_thunder(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    for _ in range(3):
        x = random.randint(int(width * 0.6), int(width * 0.95))
        y = 0
        segments = []
        while y < height:
            dx = random.randint(-15, 15)
            dy = random.randint(24, 48)
            nx = max(0, min(width - 1, x + dx))
            ny = min(height - 1, y + dy)
            segments.append((x, y, nx, ny))
            x, y = nx, ny
        for (x0, y0, x1, y1) in segments:
            draw.line((x0, y0, x1, y1), fill=(240, 240, 255), width=3)


def generate_scene_image(theme: str, size: Tuple[int, int] = (768, 512), seed: int | None = 1234) -> Image.Image:
    if seed is not None:
        random.seed(seed)
    palette = palette_for_theme(theme)
    base = horizontal_gradient(size, palette)
    draw = ImageDraw.Draw(base)
    theme_l = theme.lower()
    if "睡" in theme or "sleep" in theme_l:
        _draw_sleep(draw, base.width, base.height)
    elif "圣诞" in theme or "christmas" in theme_l:
        _draw_christmas(draw, base.width, base.height)
    elif "雷" in theme or "thunder" in theme_l:
        _draw_thunder(draw, base.width, base.height)
    return base


