import os
from pathlib import Path

try:
    from cairosvg import svg2png
except Exception as e:
    raise SystemExit("Please install cairosvg: pip install cairosvg")

ROOT = Path(__file__).resolve().parents[1]
FRONT_PUBLIC = ROOT / 'frontend' / 'public'
DOCS_ASSETS = ROOT / 'docs' / 'assets'

TASKS = [
    # (source_svg, output_png, width, height)
    (FRONT_PUBLIC / 'logo-agentloom.svg', FRONT_PUBLIC / 'logo-agentloom.png', 512, 512),
    (FRONT_PUBLIC / 'social-preview.svg', FRONT_PUBLIC / 'social-preview.png', 1200, 630),
    (DOCS_ASSETS / 'logo-agentloom.svg', DOCS_ASSETS / 'logo-agentloom.png', 512, 512),
    (DOCS_ASSETS / 'social-preview.svg', DOCS_ASSETS / 'social-preview.png', 1200, 630),
]

def ensure_dirs():
    for _, out_path, _, _ in TASKS:
        out_path.parent.mkdir(parents=True, exist_ok=True)

def convert_all():
    ensure_dirs()
    for src, dst, w, h in TASKS:
        if not src.exists():
            print(f"[WARN] missing: {src}")
            continue
        print(f"[GEN] {dst} ({w}x{h}) from {src}")
        svg2png(url=str(src), write_to=str(dst), output_width=w, output_height=h)

if __name__ == '__main__':
    convert_all() 