import argparse
from pathlib import Path
from mscen.image_gen import generate_scene_image
from mscen.music_gen import generate_music_from_theme
from mscen.video import compose_image_music_to_mp4
from mscen.core.config import load_config


def main():
    parser = argparse.ArgumentParser(prog="mscen", description="Multi-Modal Orchestrator CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    gen = sub.add_parser("gen", help="根据文本生成图像与音乐，并可合成视频")
    gen.add_argument("prompt", type=str, help="文本提示")
    gen.add_argument("--video", action="store_true", help="是否合成视频")

    ls = sub.add_parser("list", help="列出输出目录下的生成内容")

    args = parser.parse_args()
    cfg = load_config(Path(__file__).resolve().parents[2])
    outputs = cfg.outputs_dir

    if args.cmd == "gen":
        image_path = generate_scene_image(args.prompt)
        music_path = generate_music_from_theme(args.prompt)
        print(f"Image: {image_path}\nMusic: {music_path}")
        if args.video:
            video_path = compose_image_music_to_mp4(image_path, music_path, outputs / "videos")
            print(f"Video: {video_path}")
    elif args.cmd == "list":
        for p in sorted(outputs.rglob("*")):
            if p.is_file():
                print(p.relative_to(outputs))


if __name__ == "__main__":
    main() 