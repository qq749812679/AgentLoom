"""
Professional video generation engine with advanced effects
Supports transitions, multi-track editing, and real-time effects
"""

from __future__ import annotations

import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from dataclasses import dataclass
from datetime import datetime
import json
import math

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

from ..core.logger import JsonlLogger
from ..core.cache import SimpleDiskCache


@dataclass
class VideoClip:
    """Represents a video clip with metadata"""
    id: str
    source_path: Optional[Path]
    source_image: Optional[Image.Image]
    duration: float
    start_time: float
    effects: List[Dict[str, Any]]
    audio_path: Optional[Path] = None
    z_index: int = 0


@dataclass
class Transition:
    """Video transition between clips"""
    type: str
    duration: float
    parameters: Dict[str, Any]


@dataclass
class VideoTrack:
    """A video track containing multiple clips"""
    id: str
    name: str
    clips: List[VideoClip]
    enabled: bool = True
    opacity: float = 1.0


class EffectsLibrary:
    """Library of video effects"""

    @staticmethod
    def fade_in(image: Image.Image, progress: float) -> Image.Image:
        """Fade in effect"""
        alpha = int(255 * progress)
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        # Create alpha mask
        alpha_mask = Image.new('L', image.size, alpha)
        image.putalpha(alpha_mask)
        return image

    @staticmethod
    def fade_out(image: Image.Image, progress: float) -> Image.Image:
        """Fade out effect"""
        alpha = int(255 * (1 - progress))
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        alpha_mask = Image.new('L', image.size, alpha)
        image.putalpha(alpha_mask)
        return image

    @staticmethod
    def zoom_in(image: Image.Image, progress: float, max_zoom: float = 1.5) -> Image.Image:
        """Zoom in effect"""
        zoom_factor = 1 + (max_zoom - 1) * progress
        width, height = image.size

        new_width = int(width * zoom_factor)
        new_height = int(height * zoom_factor)

        zoomed = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Center crop
        left = (new_width - width) // 2
        top = (new_height - height) // 2
        cropped = zoomed.crop((left, top, left + width, top + height))

        return cropped

    @staticmethod
    def slide_left(image: Image.Image, progress: float) -> Image.Image:
        """Slide left transition"""
        width, height = image.size
        offset = int(width * progress)

        result = Image.new('RGB', (width, height), (0, 0, 0))
        result.paste(image, (-offset, 0))

        return result

    @staticmethod
    def slide_right(image: Image.Image, progress: float) -> Image.Image:
        """Slide right transition"""
        width, height = image.size
        offset = int(width * progress)

        result = Image.new('RGB', (width, height), (0, 0, 0))
        result.paste(image, (offset, 0))

        return result

    @staticmethod
    def crossfade(image1: Image.Image, image2: Image.Image, progress: float) -> Image.Image:
        """Crossfade between two images"""
        return Image.blend(image1, image2, progress)

    @staticmethod
    def wipe_left(image1: Image.Image, image2: Image.Image, progress: float) -> Image.Image:
        """Wipe transition from left to right"""
        width, height = image1.size
        split_point = int(width * progress)

        result = image1.copy()

        # Paste the second image from left up to split point
        if split_point > 0:
            crop = image2.crop((0, 0, split_point, height))
            result.paste(crop, (0, 0))

        return result

    @staticmethod
    def circle_reveal(image1: Image.Image, image2: Image.Image, progress: float) -> Image.Image:
        """Circular reveal transition"""
        width, height = image1.size
        center_x, center_y = width // 2, height // 2
        max_radius = math.sqrt(center_x**2 + center_y**2)
        current_radius = max_radius * progress

        # Create circular mask
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)

        if current_radius > 0:
            draw.ellipse([
                center_x - current_radius, center_y - current_radius,
                center_x + current_radius, center_y + current_radius
            ], fill=255)

        # Composite images using mask
        result = Image.composite(image2, image1, mask)
        return result

    @staticmethod
    def pixelate(image: Image.Image, progress: float, max_pixel_size: int = 20) -> Image.Image:
        """Pixelate effect"""
        pixel_size = int(max_pixel_size * (1 - progress)) + 1

        width, height = image.size

        # Downsample
        small_width = max(1, width // pixel_size)
        small_height = max(1, height // pixel_size)

        small_image = image.resize((small_width, small_height), Image.Resampling.NEAREST)

        # Upsample back
        pixelated = small_image.resize((width, height), Image.Resampling.NEAREST)

        return pixelated

    @staticmethod
    def blur_to_sharp(image: Image.Image, progress: float, max_blur: float = 5.0) -> Image.Image:
        """Blur to sharp transition"""
        blur_radius = max_blur * (1 - progress)

        if blur_radius > 0.1:
            return image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

        return image

    @staticmethod
    def color_shift(image: Image.Image, progress: float, target_color: Tuple[int, int, int] = (255, 100, 100)) -> Image.Image:
        """Shift image colors"""
        if image.mode != 'RGB':
            image = image.convert('RGB')

        pixels = np.array(image)
        target = np.array(target_color)

        # Blend towards target color
        shifted_pixels = pixels * (1 - progress) + target * progress
        shifted_pixels = np.clip(shifted_pixels, 0, 255).astype(np.uint8)

        return Image.fromarray(shifted_pixels)


class ProfessionalVideoEngine:
    """Professional-grade video generation engine"""

    def __init__(self, cache: SimpleDiskCache, logger: JsonlLogger):
        self.cache = cache
        self.logger = logger
        self.effects_library = EffectsLibrary()

        # Video parameters
        self.default_fps = 30
        self.default_resolution = (1920, 1080)

    def create_video_project(self, name: str, fps: int = 30,
                           resolution: Tuple[int, int] = (1920, 1080)) -> Dict[str, Any]:
        """Create a new video project"""
        project = {
            "id": f"video_project_{int(datetime.now().timestamp())}",
            "name": name,
            "fps": fps,
            "resolution": resolution,
            "tracks": [],
            "created_at": datetime.now().isoformat(),
            "metadata": {
                "total_duration": 0.0,
                "clip_count": 0,
                "effects_count": 0
            }
        }

        return project

    def add_track(self, project: Dict[str, Any], track_name: str) -> str:
        """Add a new track to the project"""
        track_id = f"track_{len(project['tracks'])}"

        track = VideoTrack(
            id=track_id,
            name=track_name,
            clips=[]
        )

        project["tracks"].append(track)

        self.logger.log({
            "event": "video.track_added",
            "project_id": project["id"],
            "track_id": track_id,
            "track_name": track_name
        })

        return track_id

    def add_image_clip(self, project: Dict[str, Any], track_id: str,
                      image: Image.Image, duration: float,
                      start_time: float = 0.0) -> str:
        """Add an image clip to a track"""
        clip_id = f"clip_{len([c for track in project['tracks'] for c in track.clips])}"

        # Resize image to project resolution
        image_resized = self._resize_image_to_fit(image, project["resolution"])

        clip = VideoClip(
            id=clip_id,
            source_path=None,
            source_image=image_resized,
            duration=duration,
            start_time=start_time,
            effects=[]
        )

        # Find track and add clip
        for track in project["tracks"]:
            if track.id == track_id:
                track.clips.append(clip)
                break

        # Update metadata
        project["metadata"]["clip_count"] += 1
        project["metadata"]["total_duration"] = max(
            project["metadata"]["total_duration"],
            start_time + duration
        )

        self.logger.log({
            "event": "video.clip_added",
            "project_id": project["id"],
            "track_id": track_id,
            "clip_id": clip_id,
            "duration": duration
        })

        return clip_id

    def add_effect_to_clip(self, project: Dict[str, Any], clip_id: str,
                          effect_type: str, parameters: Dict[str, Any] = None) -> bool:
        """Add an effect to a specific clip"""
        if parameters is None:
            parameters = {}

        effect = {
            "type": effect_type,
            "parameters": parameters,
            "enabled": True
        }

        # Find clip and add effect
        for track in project["tracks"]:
            for clip in track.clips:
                if clip.id == clip_id:
                    clip.effects.append(effect)
                    project["metadata"]["effects_count"] += 1

                    self.logger.log({
                        "event": "video.effect_added",
                        "project_id": project["id"],
                        "clip_id": clip_id,
                        "effect_type": effect_type
                    })

                    return True

        return False

    def add_transition(self, project: Dict[str, Any], track_id: str,
                      transition_type: str, duration: float,
                      between_clips: Tuple[str, str]) -> bool:
        """Add a transition between two clips"""
        clip1_id, clip2_id = between_clips

        # Find the clips
        track = None
        clip1, clip2 = None, None

        for t in project["tracks"]:
            if t.id == track_id:
                track = t
                break

        if not track:
            return False

        for clip in track.clips:
            if clip.id == clip1_id:
                clip1 = clip
            elif clip.id == clip2_id:
                clip2 = clip

        if not (clip1 and clip2):
            return False

        # Add transition effect to the second clip
        transition_effect = {
            "type": f"transition_{transition_type}",
            "parameters": {
                "duration": duration,
                "previous_clip_id": clip1_id
            },
            "enabled": True
        }

        clip2.effects.insert(0, transition_effect)  # Transitions go first

        self.logger.log({
            "event": "video.transition_added",
            "project_id": project["id"],
            "track_id": track_id,
            "transition_type": transition_type,
            "duration": duration
        })

        return True

    def render_video(self, project: Dict[str, Any], output_path: Path,
                    quality: str = "high") -> bool:
        """Render the video project to a file"""
        try:
            fps = project["fps"]
            resolution = tuple(project["resolution"])
            total_duration = project["metadata"]["total_duration"]

            # Calculate total frames
            total_frames = int(total_duration * fps)

            if not CV2_AVAILABLE:
                # Fallback to image sequence
                return self._render_image_sequence(project, output_path, total_frames)

            # Setup video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(str(output_path), fourcc, fps, resolution)

            if not out.isOpened():
                self.logger.log({
                    "event": "video.render_failed",
                    "error": "Could not open video writer",
                    "output_path": str(output_path)
                })
                return False

            # Render frame by frame
            for frame_idx in range(total_frames):
                current_time = frame_idx / fps
                frame = self._render_frame(project, current_time)

                if frame:
                    # Convert PIL Image to OpenCV format
                    frame_cv = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
                    out.write(frame_cv)

                # Log progress
                if frame_idx % (fps * 5) == 0:  # Every 5 seconds
                    progress = frame_idx / total_frames
                    self.logger.log({
                        "event": "video.render_progress",
                        "project_id": project["id"],
                        "progress": progress,
                        "frame": frame_idx
                    })

            out.release()

            self.logger.log({
                "event": "video.render_completed",
                "project_id": project["id"],
                "output_path": str(output_path),
                "total_frames": total_frames
            })

            return True

        except Exception as e:
            self.logger.log({
                "event": "video.render_failed",
                "project_id": project["id"],
                "error": str(e)
            })
            return False

    def _render_frame(self, project: Dict[str, Any], current_time: float) -> Optional[Image.Image]:
        """Render a single frame at the given time"""
        resolution = tuple(project["resolution"])
        frame = Image.new('RGB', resolution, (0, 0, 0))

        # Render all tracks
        for track in project["tracks"]:
            if not track.enabled:
                continue

            track_frame = self._render_track_frame(track, current_time, resolution)
            if track_frame:
                # Blend with opacity
                if track.opacity < 1.0:
                    track_frame = self._apply_opacity(track_frame, track.opacity)

                frame = Image.alpha_composite(
                    frame.convert('RGBA'),
                    track_frame.convert('RGBA')
                ).convert('RGB')

        return frame

    def _render_track_frame(self, track: VideoTrack, current_time: float,
                           resolution: Tuple[int, int]) -> Optional[Image.Image]:
        """Render a frame for a specific track"""
        # Find active clip at current time
        active_clip = None
        for clip in track.clips:
            if clip.start_time <= current_time < clip.start_time + clip.duration:
                active_clip = clip
                break

        if not active_clip or not active_clip.source_image:
            return None

        # Calculate progress within the clip
        clip_time = current_time - active_clip.start_time
        clip_progress = clip_time / active_clip.duration

        # Start with the source image
        frame = active_clip.source_image.copy()

        # Apply effects
        for effect in active_clip.effects:
            if not effect.get("enabled", True):
                continue

            frame = self._apply_effect(frame, effect, clip_progress, track, current_time)

        return frame

    def _apply_effect(self, image: Image.Image, effect: Dict[str, Any],
                     progress: float, track: VideoTrack, current_time: float) -> Image.Image:
        """Apply a single effect to an image"""
        effect_type = effect["type"]
        params = effect.get("parameters", {})

        try:
            if effect_type == "fade_in":
                duration = params.get("duration", 1.0)
                fade_progress = min(1.0, progress * (1.0 / duration))
                return self.effects_library.fade_in(image, fade_progress)

            elif effect_type == "fade_out":
                duration = params.get("duration", 1.0)
                fade_start = 1.0 - duration
                if progress >= fade_start:
                    fade_progress = (progress - fade_start) / duration
                    return self.effects_library.fade_out(image, fade_progress)

            elif effect_type == "zoom_in":
                max_zoom = params.get("max_zoom", 1.5)
                return self.effects_library.zoom_in(image, progress, max_zoom)

            elif effect_type == "slide_left":
                return self.effects_library.slide_left(image, progress)

            elif effect_type == "slide_right":
                return self.effects_library.slide_right(image, progress)

            elif effect_type == "pixelate":
                max_pixel_size = params.get("max_pixel_size", 20)
                return self.effects_library.pixelate(image, progress, max_pixel_size)

            elif effect_type == "blur_to_sharp":
                max_blur = params.get("max_blur", 5.0)
                return self.effects_library.blur_to_sharp(image, progress, max_blur)

            elif effect_type == "color_shift":
                target_color = params.get("target_color", (255, 100, 100))
                return self.effects_library.color_shift(image, progress, target_color)

            elif effect_type.startswith("transition_"):
                return self._apply_transition_effect(image, effect, progress, track, current_time)

        except Exception as e:
            self.logger.log({
                "event": "video.effect_error",
                "effect_type": effect_type,
                "error": str(e)
            })

        return image

    def _apply_transition_effect(self, image: Image.Image, effect: Dict[str, Any],
                               progress: float, track: VideoTrack, current_time: float) -> Image.Image:
        """Apply transition effects between clips"""
        transition_type = effect["type"].replace("transition_", "")
        transition_duration = effect["parameters"].get("duration", 1.0)
        previous_clip_id = effect["parameters"].get("previous_clip_id")

        # Only apply transition at the beginning of the clip
        if progress > transition_duration:
            return image

        # Find the previous clip
        previous_clip = None
        for clip in track.clips:
            if clip.id == previous_clip_id:
                previous_clip = clip
                break

        if not previous_clip or not previous_clip.source_image:
            return image

        # Calculate transition progress
        transition_progress = progress / transition_duration
        previous_image = previous_clip.source_image

        # Apply transition
        if transition_type == "crossfade":
            return self.effects_library.crossfade(previous_image, image, transition_progress)
        elif transition_type == "wipe_left":
            return self.effects_library.wipe_left(previous_image, image, transition_progress)
        elif transition_type == "circle_reveal":
            return self.effects_library.circle_reveal(previous_image, image, transition_progress)

        return image

    def _resize_image_to_fit(self, image: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
        """Resize image to fit target size while maintaining aspect ratio"""
        target_width, target_height = target_size

        # Calculate scaling factor
        scale_x = target_width / image.width
        scale_y = target_height / image.height
        scale = min(scale_x, scale_y)

        # Resize image
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)
        resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Center the image on target canvas
        result = Image.new('RGB', target_size, (0, 0, 0))
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2
        result.paste(resized, (x_offset, y_offset))

        return result

    def _apply_opacity(self, image: Image.Image, opacity: float) -> Image.Image:
        """Apply opacity to an image"""
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        # Apply opacity to alpha channel
        alpha = image.split()[-1]
        alpha = alpha.point(lambda p: int(p * opacity))
        image.putalpha(alpha)

        return image

    def _render_image_sequence(self, project: Dict[str, Any], output_dir: Path,
                             total_frames: int) -> bool:
        """Fallback: render as image sequence when video encoding is not available"""
        output_dir.mkdir(parents=True, exist_ok=True)

        fps = project["fps"]

        for frame_idx in range(total_frames):
            current_time = frame_idx / fps
            frame = self._render_frame(project, current_time)

            if frame:
                frame_path = output_dir / f"frame_{frame_idx:06d}.png"
                frame.save(frame_path)

        # Create a simple video info file
        info_path = output_dir / "video_info.json"
        info = {
            "fps": fps,
            "total_frames": total_frames,
            "resolution": project["resolution"],
            "note": "Video encoded as image sequence. Use ffmpeg to create video file."
        }

        with open(info_path, 'w') as f:
            json.dump(info, f, indent=2)

        self.logger.log({
            "event": "video.image_sequence_rendered",
            "project_id": project["id"],
            "output_dir": str(output_dir),
            "total_frames": total_frames
        })

        return True

    def create_slideshow(self, images: List[Image.Image], durations: List[float],
                        transitions: List[str], output_path: Path,
                        background_music: Optional[Path] = None) -> bool:
        """Create a slideshow video from images"""
        # Create project
        project = self.create_video_project("Slideshow")
        track_id = self.add_track(project, "Main Track")

        current_time = 0.0

        # Add clips
        for i, (image, duration) in enumerate(zip(images, durations)):
            clip_id = self.add_image_clip(project, track_id, image, duration, current_time)

            # Add fade effects
            self.add_effect_to_clip(project, clip_id, "fade_in", {"duration": 0.5})
            self.add_effect_to_clip(project, clip_id, "fade_out", {"duration": 0.5})

            # Add transition to next clip
            if i < len(images) - 1 and i < len(transitions):
                next_clip_id = f"clip_{i + 1}"
                self.add_transition(project, track_id, transitions[i], 1.0, (clip_id, next_clip_id))

            current_time += duration

        return self.render_video(project, output_path)

    def get_available_effects(self) -> List[Dict[str, Any]]:
        """Get list of available effects with descriptions"""
        return [
            {
                "name": "fade_in",
                "description": "Fade in from black",
                "parameters": ["duration"]
            },
            {
                "name": "fade_out",
                "description": "Fade out to black",
                "parameters": ["duration"]
            },
            {
                "name": "zoom_in",
                "description": "Zoom into the image",
                "parameters": ["max_zoom"]
            },
            {
                "name": "slide_left",
                "description": "Slide image to the left",
                "parameters": []
            },
            {
                "name": "slide_right",
                "description": "Slide image to the right",
                "parameters": []
            },
            {
                "name": "pixelate",
                "description": "Pixelate effect",
                "parameters": ["max_pixel_size"]
            },
            {
                "name": "blur_to_sharp",
                "description": "Blur to sharp transition",
                "parameters": ["max_blur"]
            },
            {
                "name": "color_shift",
                "description": "Shift image colors",
                "parameters": ["target_color"]
            }
        ]

    def get_available_transitions(self) -> List[Dict[str, Any]]:
        """Get list of available transitions"""
        return [
            {
                "name": "crossfade",
                "description": "Cross-fade between images"
            },
            {
                "name": "wipe_left",
                "description": "Wipe transition from left to right"
            },
            {
                "name": "circle_reveal",
                "description": "Circular reveal transition"
            }
        ]