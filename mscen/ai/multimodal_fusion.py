"""
🌈 Multi-Modal Fusion Engine
Advanced cross-modal generation with coherence optimization
"""

from __future__ import annotations

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import json
import asyncio
from datetime import datetime

from ..core.logger import JsonlLogger


@dataclass
class FusionRequest:
    """Multi-modal fusion request"""
    source_modalities: Dict[str, Any]  # image: path, audio: path, text: str
    target_modalities: List[str]       # ['image', 'music', 'lighting', 'video']
    fusion_style: str = "harmonious"   # harmonious, contrasting, adaptive
    coherence_weight: float = 0.8
    creativity_boost: float = 0.6
    temporal_sync: bool = True
    user_preferences: Optional[Dict] = None


@dataclass
class ModalityVector:
    """Vector representation of a modality"""
    modality_type: str
    features: np.ndarray
    metadata: Dict[str, Any]
    confidence: float
    timestamp: datetime


class CrossModalMapper:
    """🔀 Cross-modal feature mapping and translation"""

    def __init__(self, logger: JsonlLogger):
        self.logger = logger

        # Cross-modal mapping matrices (simplified)
        self.mapping_matrices = {
            ('text', 'image'): np.random.randn(512, 768),      # Text -> Image space
            ('text', 'audio'): np.random.randn(512, 1024),     # Text -> Audio space
            ('image', 'audio'): np.random.randn(768, 1024),    # Image -> Audio space
            ('audio', 'image'): np.random.randn(1024, 768),    # Audio -> Image space
            ('image', 'lighting'): np.random.randn(768, 256),  # Image -> Lighting space
            ('audio', 'lighting'): np.random.randn(1024, 256), # Audio -> Lighting space
        }

        # Modality-specific feature extractors
        self.feature_extractors = {
            'text': self._extract_text_features,
            'image': self._extract_image_features,
            'audio': self._extract_audio_features,
            'lighting': self._extract_lighting_features
        }

    def extract_modality_vector(self, modality_type: str, data: Any) -> ModalityVector:
        """Extract feature vector from modality data"""
        if modality_type not in self.feature_extractors:
            raise ValueError(f"Unsupported modality: {modality_type}")

        features, metadata = self.feature_extractors[modality_type](data)

        return ModalityVector(
            modality_type=modality_type,
            features=features,
            metadata=metadata,
            confidence=0.8,  # Could be learned
            timestamp=datetime.utcnow()
        )

    def map_between_modalities(self, source_vector: ModalityVector,
                             target_modality: str) -> ModalityVector:
        """Map features from source to target modality"""
        key = (source_vector.modality_type, target_modality)
        reverse_key = (target_modality, source_vector.modality_type)

        if key in self.mapping_matrices:
            mapping_matrix = self.mapping_matrices[key]
        elif reverse_key in self.mapping_matrices:
            # Use transpose for reverse mapping
            mapping_matrix = self.mapping_matrices[reverse_key].T
        else:
            # Create identity-like mapping for unknown pairs
            source_dim = len(source_vector.features)
            target_dim = 512  # Default target dimension
            mapping_matrix = np.random.randn(source_dim, target_dim) * 0.1

        # Apply mapping
        mapped_features = np.dot(source_vector.features, mapping_matrix)

        # Normalize
        mapped_features = mapped_features / (np.linalg.norm(mapped_features) + 1e-8)

        return ModalityVector(
            modality_type=target_modality,
            features=mapped_features,
            metadata={
                **source_vector.metadata,
                'mapped_from': source_vector.modality_type,
                'mapping_confidence': source_vector.confidence * 0.8
            },
            confidence=source_vector.confidence * 0.8,
            timestamp=datetime.utcnow()
        )

    def _extract_text_features(self, text: str) -> Tuple[np.ndarray, Dict]:
        """Extract features from text"""
        # Simple text feature extraction (in practice, use transformers)
        words = text.lower().split()

        # Create basic feature vector
        features = np.zeros(512)

        # Word-based features
        features[0] = len(words)  # Length
        features[1] = len(set(words))  # Vocabulary size
        features[2] = sum(len(word) for word in words) / len(words) if words else 0  # Avg word length

        # Sentiment approximation
        positive_words = ['happy', 'bright', 'beautiful', 'amazing', 'wonderful', 'joyful']
        negative_words = ['sad', 'dark', 'terrible', 'awful', 'horrible', 'depressing']

        positive_score = sum(1 for word in words if word in positive_words)
        negative_score = sum(1 for word in words if word in negative_words)
        features[3] = (positive_score - negative_score) / len(words) if words else 0

        # Topic features (simplified)
        topic_keywords = {
            'nature': ['tree', 'forest', 'ocean', 'mountain', 'flower', 'sky'],
            'urban': ['city', 'building', 'street', 'car', 'office', 'modern'],
            'abstract': ['concept', 'idea', 'abstract', 'theoretical', 'philosophical'],
            'emotional': ['love', 'fear', 'anger', 'joy', 'sadness', 'surprise']
        }

        for i, (topic, keywords) in enumerate(topic_keywords.items()):
            if i < 508:  # Leave room for other features
                topic_score = sum(1 for word in words if word in keywords)
                features[4 + i] = topic_score / len(words) if words else 0

        # Hash-based features for remaining dimensions
        for i in range(50, min(512, len(words) + 50)):
            if i - 50 < len(words):
                features[i] = hash(words[i - 50]) % 1000 / 1000.0

        metadata = {
            'word_count': len(words),
            'character_count': len(text),
            'sentiment_score': features[3],
            'dominant_topics': [topic for topic, keywords in topic_keywords.items()
                              if sum(1 for word in words if word in keywords) > 0]
        }

        return features, metadata

    def _extract_image_features(self, image_path: Path) -> Tuple[np.ndarray, Dict]:
        """Extract features from image"""
        try:
            from PIL import Image
            image = Image.open(image_path)

            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Resize for consistent processing
            image = image.resize((224, 224))

            # Extract basic color features
            img_array = np.array(image)

            features = np.zeros(768)

            # Color statistics
            features[0:3] = np.mean(img_array, axis=(0, 1)) / 255.0  # Mean RGB
            features[3:6] = np.std(img_array, axis=(0, 1)) / 255.0   # Std RGB

            # Brightness and contrast
            gray = np.mean(img_array, axis=2)
            features[6] = np.mean(gray) / 255.0
            features[7] = np.std(gray) / 255.0

            # Edge density
            edges_x = np.abs(np.diff(gray, axis=1))
            edges_y = np.abs(np.diff(gray, axis=0))
            features[8] = np.mean(edges_x) / 255.0
            features[9] = np.mean(edges_y) / 255.0

            # Color distribution (histogram features)
            for channel in range(3):
                hist, _ = np.histogram(img_array[:, :, channel], bins=16, range=(0, 256))
                hist = hist / np.sum(hist)  # Normalize
                start_idx = 10 + channel * 16
                features[start_idx:start_idx + 16] = hist

            # Texture features (simplified)
            for i in range(100):
                if 58 + i < 768:
                    x, y = np.random.randint(0, 224, 2)
                    features[58 + i] = img_array[y, x, i % 3] / 255.0

            metadata = {
                'width': image.width,
                'height': image.height,
                'mean_brightness': features[6],
                'contrast': features[7],
                'dominant_colors': features[0:3].tolist(),
                'edge_density': (features[8] + features[9]) / 2
            }

            return features, metadata

        except Exception as e:
            # Fallback to random features
            features = np.random.randn(768) * 0.1
            metadata = {'error': str(e), 'fallback': True}
            return features, metadata

    def _extract_audio_features(self, audio_path: Path) -> Tuple[np.ndarray, Dict]:
        """Extract features from audio"""
        try:
            from ..utils.audio_features import AudioFeatureExtractor

            # Use existing audio feature extractor
            extractor = AudioFeatureExtractor()

            # Load audio data (simplified)
            import scipy.io.wavfile as wavfile
            sample_rate, audio_data = wavfile.read(audio_path)

            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)

            # Normalize
            if np.max(np.abs(audio_data)) > 0:
                audio_data = audio_data.astype(np.float32) / np.max(np.abs(audio_data))

            # Extract comprehensive features
            audio_features = extractor.extract_comprehensive_features(audio_data)

            # Convert to fixed-size vector
            features = np.zeros(1024)

            # Map audio features to vector
            feature_idx = 0
            for category, category_features in audio_features.items():
                if isinstance(category_features, dict):
                    for key, value in category_features.items():
                        if isinstance(value, (int, float)) and feature_idx < 1024:
                            features[feature_idx] = float(value)
                            feature_idx += 1

            # Fill remaining with spectral features
            if len(audio_data) > 0:
                fft = np.fft.fft(audio_data[:min(len(audio_data), 2048)])
                magnitude = np.abs(fft)[:min(1024 - feature_idx, len(fft)//2)]
                features[feature_idx:feature_idx + len(magnitude)] = magnitude / (np.max(magnitude) + 1e-8)

            metadata = {
                'duration': len(audio_data) / sample_rate,
                'sample_rate': sample_rate,
                'rms_energy': audio_features.get('basic', {}).get('rms_energy', 0),
                'tempo': audio_features.get('temporal', {}).get('tempo_estimated', 120),
                'spectral_centroid': audio_features.get('spectral', {}).get('spectral_centroid', 1000)
            }

            return features, metadata

        except Exception as e:
            # Fallback features
            features = np.random.randn(1024) * 0.1
            metadata = {'error': str(e), 'fallback': True}
            return features, metadata

    def _extract_lighting_features(self, lighting_data: List[Dict]) -> Tuple[np.ndarray, Dict]:
        """Extract features from lighting program"""
        features = np.zeros(256)

        if not lighting_data:
            return features, {'frame_count': 0}

        # Extract color features
        colors = np.array([[frame['r'], frame['g'], frame['b']] for frame in lighting_data])

        # Basic statistics
        features[0:3] = np.mean(colors, axis=0) / 255.0
        features[3:6] = np.std(colors, axis=0) / 255.0
        features[6] = len(lighting_data)  # Number of frames

        # Color transitions
        if len(colors) > 1:
            transitions = np.diff(colors, axis=0)
            features[7:10] = np.mean(np.abs(transitions), axis=0) / 255.0
            features[10] = np.mean(np.linalg.norm(transitions, axis=1)) / 255.0

        # Duration features
        if 'duration_ms' in lighting_data[0]:
            durations = [frame.get('duration_ms', 250) for frame in lighting_data]
            features[11] = np.mean(durations)
            features[12] = np.std(durations)

        # Color wheel analysis
        for i, color in enumerate(colors[:min(50, len(colors))]):
            base_idx = 13 + i * 3
            if base_idx + 2 < 256:
                features[base_idx:base_idx + 3] = color / 255.0

        metadata = {
            'frame_count': len(lighting_data),
            'total_duration_ms': sum(frame.get('duration_ms', 250) for frame in lighting_data),
            'color_variance': np.mean(np.std(colors, axis=0)),
            'dominant_color': np.mean(colors, axis=0).tolist()
        }

        return features, metadata


class MultiModalFusionEngine:
    """🌊 Advanced multi-modal fusion with coherence optimization"""

    def __init__(self, logger: JsonlLogger):
        self.logger = logger
        self.mapper = CrossModalMapper(logger)
        self.fusion_history: List[Dict] = []

    async def fuse_modalities(self, request: FusionRequest) -> Dict[str, Any]:
        """Perform advanced multi-modal fusion"""
        start_time = datetime.utcnow()

        # Extract vectors from source modalities
        source_vectors = {}
        for modality, data in request.source_modalities.items():
            try:
                vector = self.mapper.extract_modality_vector(modality, data)
                source_vectors[modality] = vector
            except Exception as e:
                self.logger.log({
                    "event": "fusion.extraction_failed",
                    "modality": modality,
                    "error": str(e)
                })
                continue

        if not source_vectors:
            raise ValueError("No valid source modalities provided")

        # Create fusion space
        fusion_space = self._create_fusion_space(source_vectors, request.fusion_style)

        # Generate target modalities
        results = {}
        for target_modality in request.target_modalities:
            try:
                result = await self._generate_target_modality(
                    target_modality, fusion_space, request
                )
                results[target_modality] = result
            except Exception as e:
                self.logger.log({
                    "event": "fusion.generation_failed",
                    "target_modality": target_modality,
                    "error": str(e)
                })

        # Calculate coherence metrics
        coherence_score = self._calculate_fusion_coherence(source_vectors, results)

        # Store fusion history
        fusion_record = {
            'timestamp': start_time.isoformat(),
            'source_modalities': list(request.source_modalities.keys()),
            'target_modalities': request.target_modalities,
            'fusion_style': request.fusion_style,
            'coherence_score': coherence_score,
            'generation_time_ms': (datetime.utcnow() - start_time).total_seconds() * 1000
        }
        self.fusion_history.append(fusion_record)

        self.logger.log({
            "event": "fusion.completed",
            "source_count": len(source_vectors),
            "target_count": len(results),
            "coherence_score": coherence_score
        })

        return {
            'results': results,
            'coherence_score': coherence_score,
            'fusion_metadata': fusion_record,
            'source_analysis': {
                modality: {
                    'confidence': vector.confidence,
                    'feature_dim': len(vector.features),
                    'metadata': vector.metadata
                }
                for modality, vector in source_vectors.items()
            }
        }

    def _create_fusion_space(self, source_vectors: Dict[str, ModalityVector],
                           fusion_style: str) -> np.ndarray:
        """Create unified fusion space from source vectors"""
        if fusion_style == "harmonious":
            # Average all source vectors in common space
            common_vectors = []
            for vector in source_vectors.values():
                # Map to common 512-dimensional space
                if len(vector.features) != 512:
                    # Pad or truncate to 512 dimensions
                    common_vector = np.zeros(512)
                    min_len = min(512, len(vector.features))
                    common_vector[:min_len] = vector.features[:min_len]
                else:
                    common_vector = vector.features.copy()

                # Weight by confidence
                common_vector *= vector.confidence
                common_vectors.append(common_vector)

            # Weighted average
            fusion_space = np.mean(common_vectors, axis=0)

        elif fusion_style == "contrasting":
            # Emphasize differences between modalities
            common_vectors = []
            for vector in source_vectors.values():
                common_vector = np.zeros(512)
                min_len = min(512, len(vector.features))
                common_vector[:min_len] = vector.features[:min_len]
                common_vectors.append(common_vector)

            if len(common_vectors) > 1:
                # Amplify differences
                mean_vector = np.mean(common_vectors, axis=0)
                fusion_space = np.zeros(512)
                for vector in common_vectors:
                    diff = vector - mean_vector
                    fusion_space += diff * 1.5  # Amplify differences
                fusion_space /= len(common_vectors)
            else:
                fusion_space = common_vectors[0]

        else:  # adaptive
            # Adaptive fusion based on modality strengths
            weights = {}
            total_confidence = sum(v.confidence for v in source_vectors.values())

            for modality, vector in source_vectors.items():
                weights[modality] = vector.confidence / total_confidence

            fusion_space = np.zeros(512)
            for modality, vector in source_vectors.items():
                common_vector = np.zeros(512)
                min_len = min(512, len(vector.features))
                common_vector[:min_len] = vector.features[:min_len]
                fusion_space += common_vector * weights[modality]

        # Normalize fusion space
        fusion_space = fusion_space / (np.linalg.norm(fusion_space) + 1e-8)

        return fusion_space

    async def _generate_target_modality(self, target_modality: str,
                                      fusion_space: np.ndarray,
                                      request: FusionRequest) -> Dict[str, Any]:
        """Generate specific target modality from fusion space"""
        # Create target vector by mapping fusion space
        target_vector = ModalityVector(
            modality_type=target_modality,
            features=fusion_space,
            metadata={'generated_from_fusion': True},
            confidence=0.8,
            timestamp=datetime.utcnow()
        )

        # Generate content based on target modality
        if target_modality == "image":
            return await self._generate_fused_image(target_vector, request)
        elif target_modality == "music":
            return await self._generate_fused_music(target_vector, request)
        elif target_modality == "lighting":
            return await self._generate_fused_lighting(target_vector, request)
        elif target_modality == "video":
            return await self._generate_fused_video(target_vector, request)
        else:
            raise ValueError(f"Unsupported target modality: {target_modality}")

    async def _generate_fused_image(self, vector: ModalityVector,
                                  request: FusionRequest) -> Dict[str, Any]:
        """Generate image from fusion vector"""
        # Convert vector features to image generation parameters
        features = vector.features

        # Map features to prompt elements
        prompt_elements = []

        # Color mapping
        if features[0] > 0.5:
            prompt_elements.append("vibrant colors")
        elif features[0] < 0.3:
            prompt_elements.append("muted tones")

        # Mood mapping
        if features[1] > 0.5:
            prompt_elements.append("bright mood")
        else:
            prompt_elements.append("moody atmosphere")

        # Style mapping
        style_score = np.mean(features[2:5])
        if style_score > 0.6:
            style = "artistic"
        elif style_score < 0.3:
            style = "photographic"
        else:
            style = "realistic"

        prompt = "fusion generated image, " + ", ".join(prompt_elements)

        # Generate using existing image backend
        from ..connectors.image_backend import ImageBackend, Txt2ImgParams

        params = Txt2ImgParams(
            prompt=prompt,
            width=1024,
            height=1024,
            guidance=7.5 + features[5] * 2.0  # Dynamic guidance
        )

        # This would integrate with actual image generation
        result = {
            'type': 'image',
            'prompt': prompt,
            'style': style,
            'parameters': params.__dict__,
            'fusion_influence': np.mean(np.abs(features)),
            'generation_method': 'fusion_guided'
        }

        return result

    async def _generate_fused_music(self, vector: ModalityVector,
                                  request: FusionRequest) -> Dict[str, Any]:
        """Generate music from fusion vector"""
        features = vector.features

        # Map features to musical parameters
        tempo = 60 + (features[0] + features[1]) * 120  # 60-180 BPM
        key_brightness = features[2] - features[3]  # -1 to 1
        rhythm_complexity = features[4]

        # Generate musical description
        if tempo > 140:
            tempo_desc = "fast"
        elif tempo < 80:
            tempo_desc = "slow"
        else:
            tempo_desc = "moderate"

        if key_brightness > 0.3:
            mood_desc = "bright and uplifting"
        elif key_brightness < -0.3:
            mood_desc = "dark and moody"
        else:
            mood_desc = "balanced"

        music_prompt = f"fusion generated music, {tempo_desc} tempo, {mood_desc}"

        result = {
            'type': 'music',
            'prompt': music_prompt,
            'tempo': tempo,
            'key_brightness': key_brightness,
            'rhythm_complexity': rhythm_complexity,
            'duration_s': 30,
            'fusion_influence': np.std(features),
            'generation_method': 'fusion_guided'
        }

        return result

    async def _generate_fused_lighting(self, vector: ModalityVector,
                                     request: FusionRequest) -> Dict[str, Any]:
        """Generate lighting from fusion vector"""
        features = vector.features

        # Map features to lighting parameters
        num_frames = int(20 + features[0] * 30)  # 20-50 frames

        frames = []
        for i in range(num_frames):
            # Use features to determine colors
            hue = (features[i % len(features)] + 1) / 2 * 360  # 0-360
            saturation = 0.5 + features[(i + 1) % len(features)] * 0.5  # 0.5-1.0
            brightness = 0.3 + features[(i + 2) % len(features)] * 0.7  # 0.3-1.0

            # Convert HSV to RGB
            from ..utils.audio_features import hsv_to_rgb
            rgb = hsv_to_rgb(hue / 360.0, saturation, brightness)

            frames.append({
                "r": int(rgb[0] * 255),
                "g": int(rgb[1] * 255),
                "b": int(rgb[2] * 255),
                "duration_ms": 250,
                "transition": "smooth"
            })

        result = {
            'type': 'lighting',
            'frames': frames,
            'total_duration_ms': len(frames) * 250,
            'color_complexity': np.std(features[:10]),
            'fusion_influence': np.mean(features),
            'generation_method': 'fusion_guided'
        }

        return result

    async def _generate_fused_video(self, vector: ModalityVector,
                                  request: FusionRequest) -> Dict[str, Any]:
        """Generate video from fusion vector"""
        features = vector.features

        # Video generation would combine image and music fusion
        result = {
            'type': 'video',
            'duration_s': 15,
            'fps': 24,
            'style': 'fusion_generated',
            'complexity_score': np.std(features),
            'fusion_influence': np.mean(np.abs(features)),
            'generation_method': 'fusion_guided',
            'requires_assets': ['image', 'music']  # Dependencies
        }

        return result

    def _calculate_fusion_coherence(self, source_vectors: Dict[str, ModalityVector],
                                  results: Dict[str, Any]) -> float:
        """Calculate coherence score for fusion result"""
        if not source_vectors or not results:
            return 0.0

        # Simple coherence calculation based on feature similarity
        coherence_scores = []

        # Check consistency between source confidences
        source_confidences = [v.confidence for v in source_vectors.values()]
        confidence_consistency = 1.0 - np.std(source_confidences)
        coherence_scores.append(confidence_consistency)

        # Check feature space alignment
        if len(source_vectors) > 1:
            vectors = [v.features for v in source_vectors.values()]
            # Normalize to same length
            min_len = min(len(v) for v in vectors)
            normalized_vectors = [v[:min_len] for v in vectors]

            # Calculate pairwise similarities
            similarities = []
            for i in range(len(normalized_vectors)):
                for j in range(i + 1, len(normalized_vectors)):
                    v1 = normalized_vectors[i] / (np.linalg.norm(normalized_vectors[i]) + 1e-8)
                    v2 = normalized_vectors[j] / (np.linalg.norm(normalized_vectors[j]) + 1e-8)
                    similarity = np.dot(v1, v2)
                    similarities.append(max(0, similarity))

            if similarities:
                feature_coherence = np.mean(similarities)
                coherence_scores.append(feature_coherence)

        # Check result diversity (good fusion should produce varied but coherent results)
        if len(results) > 1:
            result_types = set(result.get('type', 'unknown') for result in results.values())
            diversity_score = len(result_types) / len(results)
            coherence_scores.append(diversity_score)

        return np.mean(coherence_scores) if coherence_scores else 0.5

    def get_fusion_analytics(self) -> Dict[str, Any]:
        """Get analytics about fusion performance"""
        if not self.fusion_history:
            return {"total_fusions": 0}

        coherence_scores = [f['coherence_score'] for f in self.fusion_history]
        generation_times = [f['generation_time_ms'] for f in self.fusion_history]

        source_modality_counts = {}
        target_modality_counts = {}

        for fusion in self.fusion_history:
            for modality in fusion['source_modalities']:
                source_modality_counts[modality] = source_modality_counts.get(modality, 0) + 1
            for modality in fusion['target_modalities']:
                target_modality_counts[modality] = target_modality_counts.get(modality, 0) + 1

        return {
            'total_fusions': len(self.fusion_history),
            'avg_coherence_score': np.mean(coherence_scores),
            'avg_generation_time_ms': np.mean(generation_times),
            'coherence_trend': coherence_scores[-10:],  # Last 10 scores
            'popular_source_modalities': source_modality_counts,
            'popular_target_modalities': target_modality_counts,
            'fusion_styles_used': [f['fusion_style'] for f in self.fusion_history[-20:]]
        }