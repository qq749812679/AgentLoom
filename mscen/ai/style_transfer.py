"""
AI-powered style transfer and enhancement engine
Supports image-to-image, audio-to-image, and cross-modal style transfer
"""

from __future__ import annotations

import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from PIL import Image, ImageFilter, ImageEnhance
import json
from datetime import datetime

from ..core.logger import JsonlLogger
from ..core.cache import SimpleDiskCache


class StyleTransferEngine:
    """Advanced style transfer engine with multi-modal capabilities"""

    def __init__(self, cache: SimpleDiskCache, logger: JsonlLogger):
        self.cache = cache
        self.logger = logger
        self.style_presets = self._load_style_presets()

    def _load_style_presets(self) -> Dict[str, Dict[str, Any]]:
        """Load pre-defined style presets"""
        return {
            "cyberpunk": {
                "color_palette": ["#FF00FF", "#00FFFF", "#FF6600", "#9900FF"],
                "saturation": 1.5,
                "contrast": 1.3,
                "brightness": 0.9,
                "blur_radius": 0,
                "edge_enhance": True,
                "neon_glow": True
            },
            "vintage": {
                "color_palette": ["#D2691E", "#F4A460", "#DEB887", "#BC8F8F"],
                "saturation": 0.7,
                "contrast": 0.9,
                "brightness": 0.8,
                "blur_radius": 0.5,
                "sepia": True,
                "vignette": True
            },
            "minimalist": {
                "color_palette": ["#FFFFFF", "#F5F5F5", "#E0E0E0", "#CCCCCC"],
                "saturation": 0.3,
                "contrast": 1.1,
                "brightness": 1.2,
                "blur_radius": 0,
                "high_contrast": True,
                "clean_lines": True
            },
            "nature": {
                "color_palette": ["#228B22", "#32CD32", "#90EE90", "#98FB98"],
                "saturation": 1.2,
                "contrast": 1.1,
                "brightness": 1.0,
                "blur_radius": 0,
                "nature_enhance": True,
                "warm_tone": True
            },
            "cinematic": {
                "color_palette": ["#1C1C1C", "#2F4F4F", "#4682B4", "#B0C4DE"],
                "saturation": 0.8,
                "contrast": 1.4,
                "brightness": 0.7,
                "blur_radius": 0,
                "film_grain": True,
                "color_grade": True
            }
        }

    def apply_style_preset(self, image: Image.Image, style_name: str) -> Image.Image:
        """Apply a predefined style preset to an image"""
        if style_name not in self.style_presets:
            self.logger.log({"event": "style_transfer.unknown_preset", "style": style_name})
            return image

        style = self.style_presets[style_name]
        return self._apply_style_transforms(image, style)

    def _apply_style_transforms(self, image: Image.Image, style: Dict[str, Any]) -> Image.Image:
        """Apply style transformations to an image"""
        img = image.copy()

        # Basic adjustments
        if "brightness" in style:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(style["brightness"])

        if "contrast" in style:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(style["contrast"])

        if "saturation" in style:
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(style["saturation"])

        # Blur effects
        if style.get("blur_radius", 0) > 0:
            img = img.filter(ImageFilter.GaussianBlur(radius=style["blur_radius"]))

        # Edge enhancement
        if style.get("edge_enhance"):
            img = img.filter(ImageFilter.EDGE_ENHANCE)

        # Special effects
        if style.get("sepia"):
            img = self._apply_sepia(img)

        if style.get("neon_glow"):
            img = self._apply_neon_glow(img)

        if style.get("vignette"):
            img = self._apply_vignette(img)

        # Color palette mapping
        if "color_palette" in style:
            img = self._apply_color_palette(img, style["color_palette"])

        self.logger.log({
            "event": "style_transfer.applied",
            "style_params": style,
            "image_size": img.size
        })

        return img

    def _apply_sepia(self, image: Image.Image) -> Image.Image:
        """Apply sepia tone effect"""
        pixels = np.array(image)

        # Sepia transformation matrix
        sepia_matrix = np.array([
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131]
        ])

        # Apply sepia transformation
        sepia_pixels = pixels @ sepia_matrix.T
        sepia_pixels = np.clip(sepia_pixels, 0, 255).astype(np.uint8)

        return Image.fromarray(sepia_pixels)

    def _apply_neon_glow(self, image: Image.Image) -> Image.Image:
        """Apply neon glow effect"""
        # Create a glowing edge effect
        edge = image.filter(ImageFilter.FIND_EDGES)
        edge = edge.filter(ImageFilter.GaussianBlur(radius=2))

        # Enhance the edges and blend with original
        enhancer = ImageEnhance.Brightness(edge)
        bright_edge = enhancer.enhance(2.0)

        # Blend using screen mode simulation
        result = Image.blend(image, bright_edge, 0.3)
        return result

    def _apply_vignette(self, image: Image.Image) -> Image.Image:
        """Apply vignette effect"""
        width, height = image.size

        # Create radial gradient mask
        center_x, center_y = width // 2, height // 2
        max_radius = min(width, height) // 2

        mask = Image.new('L', (width, height), 0)
        mask_pixels = np.array(mask)

        for y in range(height):
            for x in range(width):
                distance = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                vignette_strength = min(1.0, distance / max_radius)
                mask_pixels[y, x] = int(255 * (1 - vignette_strength * 0.6))

        mask = Image.fromarray(mask_pixels, 'L')

        # Apply vignette
        darkened = Image.new('RGB', image.size, (0, 0, 0))
        result = Image.composite(image, darkened, mask)

        return result

    def _apply_color_palette(self, image: Image.Image, palette: List[str]) -> Image.Image:
        """Map image colors to a specific palette"""
        # Convert palette to RGB tuples
        rgb_palette = []
        for color in palette:
            if color.startswith('#'):
                rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
                rgb_palette.append(rgb)

        if not rgb_palette:
            return image

        # Convert image to numpy array
        pixels = np.array(image)
        original_shape = pixels.shape
        pixels = pixels.reshape(-1, 3)

        # Map each pixel to closest palette color
        new_pixels = np.zeros_like(pixels)
        for i, pixel in enumerate(pixels):
            distances = [np.linalg.norm(pixel - np.array(color)) for color in rgb_palette]
            closest_color_idx = np.argmin(distances)
            new_pixels[i] = rgb_palette[closest_color_idx]

        # Reshape back and create image
        new_pixels = new_pixels.reshape(original_shape).astype(np.uint8)
        return Image.fromarray(new_pixels)

    def create_style_from_reference(self, reference_image: Image.Image, name: str) -> Dict[str, Any]:
        """Analyze a reference image and create a style preset"""
        # Analyze image characteristics
        pixels = np.array(reference_image)

        # Extract dominant colors
        reshaped_pixels = pixels.reshape(-1, 3)
        from scipy.cluster.vq import kmeans2

        try:
            centroids, _ = kmeans2(reshaped_pixels.astype(float), 4)
            dominant_colors = ['#{:02x}{:02x}{:02x}'.format(int(r), int(g), int(b))
                             for r, g, b in centroids]
        except:
            # Fallback if clustering fails
            dominant_colors = ["#808080", "#A0A0A0", "#606060", "#C0C0C0"]

        # Calculate image statistics
        brightness = np.mean(pixels) / 255.0
        contrast = np.std(pixels) / 128.0

        # Estimate saturation
        hsv_pixels = np.array(reference_image.convert('HSV'))
        saturation = np.mean(hsv_pixels[:, :, 1]) / 255.0

        style = {
            "color_palette": dominant_colors,
            "brightness": max(0.5, min(2.0, brightness * 1.2)),
            "contrast": max(0.5, min(2.0, contrast * 1.2)),
            "saturation": max(0.3, min(2.0, saturation * 1.2)),
            "blur_radius": 0,
            "custom_style": True,
            "reference_analyzed": True
        }

        # Save the custom style
        self.style_presets[name] = style

        self.logger.log({
            "event": "style_transfer.custom_style_created",
            "style_name": name,
            "style_params": style
        })

        return style

    def cross_modal_style_transfer(self, image: Image.Image, audio_features: Dict[str, float]) -> Image.Image:
        """Apply style based on audio characteristics"""
        # Map audio features to visual style
        style = {
            "brightness": 0.7 + (audio_features.get("energy", 0.5) * 0.6),
            "contrast": 0.8 + (audio_features.get("danceability", 0.5) * 0.8),
            "saturation": 0.6 + (audio_features.get("valence", 0.5) * 0.8),
            "blur_radius": max(0, (1 - audio_features.get("acousticness", 0.5)) * 2),
        }

        # Tempo-based effects
        tempo = audio_features.get("tempo", 120)
        if tempo > 140:  # Fast tempo
            style["edge_enhance"] = True
            style["neon_glow"] = True
        elif tempo < 80:  # Slow tempo
            style["sepia"] = True
            style["vignette"] = True

        # Mood-based color palette
        valence = audio_features.get("valence", 0.5)
        energy = audio_features.get("energy", 0.5)

        if valence > 0.7 and energy > 0.7:  # Happy and energetic
            style["color_palette"] = ["#FFD700", "#FF6347", "#32CD32", "#FF69B4"]
        elif valence < 0.3:  # Sad
            style["color_palette"] = ["#2F4F4F", "#696969", "#4682B4", "#708090"]
        elif energy > 0.7:  # Energetic but not necessarily happy
            style["color_palette"] = ["#FF4500", "#DC143C", "#FF6600", "#FF1493"]
        else:  # Calm/neutral
            style["color_palette"] = ["#E6E6FA", "#D3D3D3", "#B0C4DE", "#F0F8FF"]

        return self._apply_style_transforms(image, style)

    def batch_style_transfer(self, images: List[Image.Image], style_name: str,
                           output_dir: Path) -> List[Path]:
        """Apply style transfer to multiple images"""
        output_paths = []

        for i, image in enumerate(images):
            styled_image = self.apply_style_preset(image, style_name)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = output_dir / f"styled_{style_name}_{i}_{timestamp}.png"
            styled_image.save(output_path)
            output_paths.append(output_path)

        self.logger.log({
            "event": "style_transfer.batch_completed",
            "style": style_name,
            "image_count": len(images),
            "output_paths": [str(p) for p in output_paths]
        })

        return output_paths

    def get_style_preview(self, style_name: str, sample_size: Tuple[int, int] = (200, 200)) -> Image.Image:
        """Generate a preview of what a style looks like"""
        if style_name not in self.style_presets:
            # Create a basic gray preview
            return Image.new('RGB', sample_size, (128, 128, 128))

        # Create a test gradient image
        gradient = Image.new('RGB', sample_size, (255, 255, 255))
        pixels = np.array(gradient)

        # Create a radial gradient
        center_x, center_y = sample_size[0] // 2, sample_size[1] // 2
        max_radius = min(sample_size) // 2

        for y in range(sample_size[1]):
            for x in range(sample_size[0]):
                distance = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                intensity = max(0, min(255, int(255 * (1 - distance / max_radius))))
                pixels[y, x] = [intensity, intensity, intensity]

        gradient = Image.fromarray(pixels.astype(np.uint8))

        # Apply the style to the gradient
        styled_preview = self.apply_style_preset(gradient, style_name)

        return styled_preview

    def export_style_preset(self, style_name: str, file_path: Path) -> bool:
        """Export a style preset to a JSON file"""
        if style_name not in self.style_presets:
            return False

        preset_data = {
            "name": style_name,
            "parameters": self.style_presets[style_name],
            "created_at": datetime.now().isoformat(),
            "version": "1.0"
        }

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(preset_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.logger.log({"event": "style_transfer.export_failed", "error": str(e)})
            return False

    def import_style_preset(self, file_path: Path) -> Optional[str]:
        """Import a style preset from a JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                preset_data = json.load(f)

            name = preset_data["name"]
            parameters = preset_data["parameters"]

            self.style_presets[name] = parameters

            self.logger.log({
                "event": "style_transfer.preset_imported",
                "style_name": name
            })

            return name
        except Exception as e:
            self.logger.log({"event": "style_transfer.import_failed", "error": str(e)})
            return None