from typing import List, Tuple
from PIL import Image


Palette = List[Tuple[int, int, int]]


THEME_TO_PALETTE = {
    "睡眠": [(10, 20, 60), (30, 40, 90), (60, 70, 120)],
    "sleep": [(10, 20, 60), (30, 40, 90), (60, 70, 120)],
    "圣诞节": [(180, 0, 0), (0, 140, 0), (220, 220, 220)],
    "christmas": [(180, 0, 0), (0, 140, 0), (220, 220, 220)],
    "打雷": [(10, 10, 20), (30, 30, 50), (200, 200, 220)],
    "thunder": [(10, 10, 20), (30, 30, 50), (200, 200, 220)],
    "浪漫": [(120, 0, 60), (220, 80, 140), (255, 180, 200)],
    "romance": [(120, 0, 60), (220, 80, 140), (255, 180, 200)],
    "派对": [(255, 60, 0), (0, 160, 255), (80, 0, 255)],
    "party": [(255, 60, 0), (0, 160, 255), (80, 0, 255)],
    "禅修": [(0, 60, 50), (40, 120, 100), (200, 255, 230)],
    "zen": [(0, 60, 50), (40, 120, 100), (200, 255, 230)],
}


def palette_for_theme(theme: str) -> Palette:
    key = theme.strip().lower()
    if key in THEME_TO_PALETTE:
        return THEME_TO_PALETTE[key]
    for k, v in THEME_TO_PALETTE.items():
        if k.lower() in key:
            return v
    return [(40, 40, 40), (90, 90, 90), (160, 160, 160)]


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f"#{r:02x}{g:02x}{b:02x}"


def hex_to_rgb(h: str) -> Tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore


def horizontal_gradient(size: Tuple[int, int], colors: Palette) -> Image.Image:
    width, height = size
    img = Image.new("RGB", (width, height))
    n = max(2, len(colors))
    for x in range(width):
        t = x / (width - 1 if width > 1 else 1)
        pos = t * (n - 1)
        i = int(pos)
        f = pos - i
        c0 = colors[min(i, n - 1)]
        c1 = colors[min(i + 1, n - 1)]
        r = int(c0[0] * (1 - f) + c1[0] * f)
        g = int(c0[1] * (1 - f) + c1[1] * f)
        b = int(c0[2] * (1 - f) + c1[2] * f)
        for y in range(height):
            img.putpixel((x, y), (r, g, b))
    return img



