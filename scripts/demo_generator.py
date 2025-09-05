#!/usr/bin/env python3
"""
Demo Content Generator for GitHub Showcase

This script generates impressive demo content to showcase the project's capabilities.
Run this to create example outputs for README and documentation.
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from mscen.image_gen import generate_scene_image
from mscen.music_gen import generate_music_for_theme
from mscen.lighting import generate_lighting_program
from mscen.video import compose_image_music_to_mp4


def create_demo_content():
    """Generate impressive demo content for GitHub showcase."""
    
    print("🎬 Generating Demo Content for GitHub...")
    print("=" * 50)
    
    # Create demo output directory
    demo_dir = Path("demo_outputs")
    demo_dir.mkdir(exist_ok=True)
    
    # Demo themes that showcase different capabilities
    demo_themes = [
        {
            "name": "cozy_christmas",
            "prompt": "Cozy Christmas living room with fireplace, warm lighting, and snow outside",
            "description": "Perfect for holiday ambiance"
        },
        {
            "name": "cyberpunk_city",
            "prompt": "Futuristic cyberpunk cityscape with neon lights and rain",
            "description": "High-tech urban vibes"
        },
        {
            "name": "sunset_beach",
            "prompt": "Peaceful sunset over tropical beach with palm trees",
            "description": "Relaxing natural scene"
        },
        {
            "name": "space_station",
            "prompt": "Advanced space station interior with cosmic views",
            "description": "Sci-fi workspace ambiance"
        }
    ]
    
    results = []
    
    for i, theme in enumerate(demo_themes, 1):
        print(f"\n🎨 Creating Demo {i}/4: {theme['name']}")
        print(f"Theme: {theme['description']}")
        
        try:
            # Generate image
            print("  📸 Generating image...")
            image = generate_scene_image(theme["prompt"])
            image_path = demo_dir / f"{theme['name']}_image.png"
            image.save(image_path)
            
            # Generate music
            print("  🎵 Generating music...")
            music_path = generate_music_for_theme(theme["prompt"], duration=30)
            demo_music_path = demo_dir / f"{theme['name']}_music.wav"
            if music_path and music_path.exists():
                import shutil
                shutil.copy2(music_path, demo_music_path)
            
            # Generate lighting
            print("  💡 Generating lighting...")
            lighting_program = generate_lighting_program(theme["prompt"])
            lighting_path = demo_dir / f"{theme['name']}_lighting.json"
            
            import json
            with open(lighting_path, 'w') as f:
                json.dump(lighting_program, f, indent=2)
            
            # Generate video (if both image and music exist)
            print("  🎬 Generating video...")
            if demo_music_path.exists():
                video_path = compose_image_music_to_mp4(
                    str(image_path), 
                    str(demo_music_path), 
                    str(demo_dir / f"{theme['name']}_video.mp4")
                )
            
            results.append({
                "theme": theme,
                "image": image_path,
                "music": demo_music_path if demo_music_path.exists() else None,
                "lighting": lighting_path,
                "video": demo_dir / f"{theme['name']}_video.mp4"
            })
            
            print(f"  ✅ Demo {i} completed!")
            
        except Exception as e:
            print(f"  ❌ Error in demo {i}: {e}")
            continue
    
    # Generate demo showcase HTML
    create_demo_showcase(results, demo_dir)
    
    # Generate statistics
    create_demo_stats(results, demo_dir)
    
    print(f"\n🎉 Demo generation completed!")
    print(f"📁 Files saved to: {demo_dir.absolute()}")
    print(f"🌐 View showcase: {demo_dir / 'index.html'}")
    
    return results


def create_demo_showcase(results, demo_dir):
    """Create an HTML showcase page for the demos."""
    
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-Modal AI Orchestrator - Demo Showcase</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        .demo-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }
        .demo-card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s ease;
        }
        .demo-card:hover {
            transform: translateY(-5px);
        }
        .demo-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 10px;
            margin-bottom: 15px;
        }
        .demo-title {
            font-size: 1.4em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .demo-description {
            opacity: 0.8;
            margin-bottom: 15px;
        }
        .demo-links {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .demo-link {
            padding: 5px 10px;
            background: rgba(255,255,255,0.2);
            border-radius: 20px;
            text-decoration: none;
            color: white;
            font-size: 0.9em;
            transition: background 0.3s ease;
        }
        .demo-link:hover {
            background: rgba(255,255,255,0.3);
        }
        .stats {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
        }
        .stats h2 {
            margin-bottom: 20px;
        }
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
        }
        .stat-item {
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            display: block;
        }
        .stat-label {
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌟 Multi-Modal AI Orchestrator</h1>
            <p>Experience the future of AI-powered creativity</p>
        </div>
        
        <div class="demo-grid">
"""
    
    for result in results:
        if not result:
            continue
            
        theme = result["theme"]
        html_content += f"""
            <div class="demo-card">
                <img src="{result['image'].name}" alt="{theme['name']}" class="demo-image">
                <div class="demo-title">{theme['name'].replace('_', ' ').title()}</div>
                <div class="demo-description">{theme['description']}</div>
                <div class="demo-links">
                    <a href="{result['image'].name}" class="demo-link">🖼️ Image</a>
                    {f'<a href="{result["music"].name}" class="demo-link">🎵 Music</a>' if result.get("music") else ""}
                    <a href="{result['lighting'].name}" class="demo-link">💡 Lighting</a>
                    {f'<a href="{result["video"].name}" class="demo-link">🎬 Video</a>' if result.get("video") else ""}
                </div>
            </div>
        """
    
    html_content += """
        </div>
        
        <div class="stats">
            <h2>📊 Demo Statistics</h2>
            <div class="stat-grid">
                <div class="stat-item">
                    <span class="stat-number">4</span>
                    <span class="stat-label">Unique Themes</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">16</span>
                    <span class="stat-label">Generated Assets</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">100%</span>
                    <span class="stat-label">AI Generated</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">∞</span>
                    <span class="stat-label">Possibilities</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    with open(demo_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)


def create_demo_stats(results, demo_dir):
    """Create a statistics file for the demo."""
    
    import json
    from datetime import datetime
    
    stats = {
        "generated_at": datetime.now().isoformat(),
        "total_themes": len(results),
        "successful_generations": len([r for r in results if r]),
        "files_created": sum([
            1,  # image
            1 if r.get("music") else 0,  # music
            1,  # lighting
            1 if r.get("video") else 0   # video
        ] for r in results if r),
        "themes": [r["theme"] if r else None for r in results]
    }
    
    with open(demo_dir / "stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)


if __name__ == "__main__":
    create_demo_content()
