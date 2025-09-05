from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict

import numpy as np


@dataclass
class UserPreference:
    category: str  # theme, style, color, music_genre, etc.
    value: str
    confidence: float  # 0.0 - 1.0
    last_updated: str
    frequency: int = 1


@dataclass
class UserProfile:
    user_id: str
    created_at: str
    preferences: List[UserPreference]
    usage_stats: Dict[str, Any]
    quality_threshold: float = 0.8
    preferred_speed: str = "balanced"  # fast, balanced, quality
    notification_settings: Dict[str, bool] = None
    
    def __post_init__(self):
        if self.notification_settings is None:
            self.notification_settings = {
                "completion_notifications": True,
                "recommendation_updates": True,
                "system_updates": False
            }


class PersonalizationEngine:
    def __init__(self, profiles_dir: Path) -> None:
        self.profiles_dir = profiles_dir
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self.profiles: Dict[str, UserProfile] = {}
        self._load_existing_profiles()
    
    def _load_existing_profiles(self) -> None:
        """Load existing user profiles from disk"""
        for profile_file in self.profiles_dir.glob("*.json"):
            try:
                with profile_file.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    preferences = [UserPreference(**p) for p in data.get("preferences", [])]
                    profile = UserProfile(
                        user_id=data["user_id"],
                        created_at=data["created_at"],
                        preferences=preferences,
                        usage_stats=data.get("usage_stats", {}),
                        quality_threshold=data.get("quality_threshold", 0.8),
                        preferred_speed=data.get("preferred_speed", "balanced"),
                        notification_settings=data.get("notification_settings", {})
                    )
                    self.profiles[profile.user_id] = profile
            except Exception as e:
                print(f"Failed to load profile {profile_file}: {e}")
    
    def get_or_create_profile(self, user_id: str) -> UserProfile:
        """Get existing profile or create new one"""
        if user_id not in self.profiles:
            self.profiles[user_id] = UserProfile(
                user_id=user_id,
                created_at=datetime.utcnow().isoformat(),
                preferences=[],
                usage_stats={
                    "total_generations": 0,
                    "favorite_themes": [],
                    "avg_session_duration": 0,
                    "preferred_time_slots": [],
                    "device_preferences": {}
                }
            )
            self._save_profile(user_id)
        return self.profiles[user_id]
    
    def update_preference(self, user_id: str, category: str, value: str, confidence: float = 1.0) -> None:
        """Update user preference with learning"""
        profile = self.get_or_create_profile(user_id)
        
        # Find existing preference
        existing_pref = None
        for pref in profile.preferences:
            if pref.category == category and pref.value == value:
                existing_pref = pref
                break
        
        if existing_pref:
            # Update existing preference
            existing_pref.frequency += 1
            existing_pref.confidence = min(1.0, existing_pref.confidence + 0.1)
            existing_pref.last_updated = datetime.utcnow().isoformat()
        else:
            # Add new preference
            new_pref = UserPreference(
                category=category,
                value=value,
                confidence=confidence,
                last_updated=datetime.utcnow().isoformat()
            )
            profile.preferences.append(new_pref)
        
        # Decay old preferences
        self._decay_old_preferences(profile)
        self._save_profile(user_id)
    
    def _decay_old_preferences(self, profile: UserProfile) -> None:
        """Decay confidence of old preferences"""
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        
        for pref in profile.preferences:
            last_updated = datetime.fromisoformat(pref.last_updated.replace('Z', '+00:00'))
            if last_updated < cutoff_date:
                pref.confidence *= 0.9  # Gradual decay
        
        # Remove very low confidence preferences
        profile.preferences = [p for p in profile.preferences if p.confidence > 0.1]
    
    def get_recommendations(self, user_id: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate personalized recommendations"""
        profile = self.get_or_create_profile(user_id)
        context = context or {}
        
        # Analyze preferences by category
        category_preferences = defaultdict(list)
        for pref in profile.preferences:
            category_preferences[pref.category].append(pref)
        
        recommendations = {
            "themes": self._recommend_themes(category_preferences, context),
            "styles": self._recommend_styles(category_preferences, context),
            "parameters": self._recommend_parameters(profile, context),
            "workflows": self._recommend_workflows(profile, context),
            "optimization_settings": self._recommend_optimization(profile)
        }
        
        return recommendations
    
    def _recommend_themes(self, categories: Dict[str, List[UserPreference]], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend themes based on user history"""
        theme_prefs = categories.get("theme", [])
        if not theme_prefs:
            return [
                {"theme": "现代简约", "confidence": 0.5, "reason": "通用推荐"},
                {"theme": "温馨家居", "confidence": 0.5, "reason": "通用推荐"}
            ]
        
        # Sort by confidence * frequency
        sorted_themes = sorted(theme_prefs, 
                             key=lambda p: p.confidence * p.frequency, 
                             reverse=True)
        
        recommendations = []
        for pref in sorted_themes[:5]:
            recommendations.append({
                "theme": pref.value,
                "confidence": pref.confidence,
                "reason": f"您经常使用此主题 ({pref.frequency}次)"
            })
        
        # Add contextual recommendations
        current_hour = datetime.now().hour
        if 18 <= current_hour <= 22:
            recommendations.insert(0, {
                "theme": "温馨晚间", 
                "confidence": 0.8, 
                "reason": "适合当前时间"
            })
        
        return recommendations
    
    def _recommend_styles(self, categories: Dict[str, List[UserPreference]], context: Dict[str, Any]) -> List[str]:
        """Recommend visual styles"""
        style_prefs = categories.get("style", [])
        if not style_prefs:
            return ["现代", "简约", "温馨"]
        
        return [p.value for p in sorted(style_prefs, 
                                       key=lambda p: p.confidence * p.frequency, 
                                       reverse=True)[:3]]
    
    def _recommend_parameters(self, profile: UserProfile, context: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend generation parameters"""
        params = {
            "quality_priority": profile.quality_threshold,
            "speed_setting": profile.preferred_speed,
        }
        
        # Adjust based on usage patterns
        usage = profile.usage_stats
        if usage.get("total_generations", 0) > 50:
            # Experienced user, enable advanced features
            params["advanced_mode"] = True
            params["custom_parameters"] = True
        
        return params
    
    def _recommend_workflows(self, profile: UserProfile, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend optimal workflows"""
        workflows = []
        
        # Based on usage patterns
        usage = profile.usage_stats
        favorite_themes = usage.get("favorite_themes", [])
        
        if "派对" in str(favorite_themes):
            workflows.append({
                "name": "派对专用流程",
                "steps": ["音乐", "灯光", "视频"],
                "description": "基于您的使用习惯定制"
            })
        
        if profile.preferred_speed == "fast":
            workflows.append({
                "name": "快速生成",
                "steps": ["简化图片", "短音乐", "基础灯光"],
                "description": "追求速度的优化流程"
            })
        
        return workflows
    
    def _recommend_optimization(self, profile: UserProfile) -> Dict[str, Any]:
        """Recommend optimization settings"""
        settings = {
            "cache_enabled": True,
            "batch_processing": profile.preferred_speed != "quality",
            "quality_checks": profile.quality_threshold > 0.8
        }
        
        # Device-specific optimizations
        device_prefs = profile.usage_stats.get("device_preferences", {})
        if "mobile" in device_prefs:
            settings["mobile_optimized"] = True
            settings["reduced_resolution"] = True
        
        return settings
    
    def learn_from_interaction(self, user_id: str, interaction: Dict[str, Any]) -> None:
        """Learn from user interaction"""
        profile = self.get_or_create_profile(user_id)
        
        # Extract preferences from interaction
        if "theme" in interaction:
            self.update_preference(user_id, "theme", interaction["theme"])
        
        if "rating" in interaction and interaction["rating"] >= 4:
            # High rating - reinforce preferences
            for key, value in interaction.items():
                if key in ["style", "mood", "genre"]:
                    self.update_preference(user_id, key, str(value), confidence=0.8)
        
        # Update usage stats
        profile.usage_stats["total_generations"] = profile.usage_stats.get("total_generations", 0) + 1
        
        # Track session duration
        if "session_duration" in interaction:
            current_avg = profile.usage_stats.get("avg_session_duration", 0)
            total = profile.usage_stats["total_generations"]
            new_avg = (current_avg * (total - 1) + interaction["session_duration"]) / total
            profile.usage_stats["avg_session_duration"] = new_avg
        
        # Track time preferences
        current_hour = datetime.now().hour
        time_slots = profile.usage_stats.get("preferred_time_slots", [])
        time_slots.append(current_hour)
        profile.usage_stats["preferred_time_slots"] = time_slots[-50:]  # Keep last 50
        
        self._save_profile(user_id)
    
    def get_adaptive_ui_config(self, user_id: str) -> Dict[str, Any]:
        """Get adaptive UI configuration"""
        profile = self.get_or_create_profile(user_id)
        
        config = {
            "show_advanced_options": profile.usage_stats.get("total_generations", 0) > 10,
            "default_quality": profile.quality_threshold,
            "quick_access_themes": self._get_top_themes(profile, limit=5),
            "suggested_workflows": self._recommend_workflows(profile, {}),
            "notification_settings": profile.notification_settings
        }
        
        return config
    
    def _get_top_themes(self, profile: UserProfile, limit: int = 5) -> List[str]:
        """Get top themes for quick access"""
        theme_prefs = [p for p in profile.preferences if p.category == "theme"]
        if not theme_prefs:
            return ["睡眠", "派对", "禅修", "浪漫", "圣诞节"]
        
        sorted_themes = sorted(theme_prefs, 
                             key=lambda p: p.confidence * p.frequency, 
                             reverse=True)
        return [p.value for p in sorted_themes[:limit]]
    
    def _save_profile(self, user_id: str) -> None:
        """Save user profile to disk"""
        if user_id in self.profiles:
            profile = self.profiles[user_id]
            profile_data = {
                "user_id": profile.user_id,
                "created_at": profile.created_at,
                "preferences": [asdict(p) for p in profile.preferences],
                "usage_stats": profile.usage_stats,
                "quality_threshold": profile.quality_threshold,
                "preferred_speed": profile.preferred_speed,
                "notification_settings": profile.notification_settings
            }
            
            profile_file = self.profiles_dir / f"{user_id}.json"
            with profile_file.open("w", encoding="utf-8") as f:
                json.dump(profile_data, f, ensure_ascii=False, indent=2)
    
    def export_insights(self, user_id: str) -> Dict[str, Any]:
        """Export user insights for analytics"""
        profile = self.get_or_create_profile(user_id)
        
        insights = {
            "user_segment": self._classify_user_segment(profile),
            "engagement_score": self._calculate_engagement_score(profile),
            "preference_diversity": self._calculate_preference_diversity(profile),
            "loyalty_indicators": self._get_loyalty_indicators(profile),
            "growth_opportunities": self._identify_growth_opportunities(profile)
        }
        
        return insights
    
    def _classify_user_segment(self, profile: UserProfile) -> str:
        """Classify user into segments"""
        total_gens = profile.usage_stats.get("total_generations", 0)
        avg_session = profile.usage_stats.get("avg_session_duration", 0)
        
        if total_gens >= 100 and avg_session >= 300:
            return "power_user"
        elif total_gens >= 20:
            return "regular_user"
        elif total_gens >= 5:
            return "casual_user"
        else:
            return "new_user"
    
    def _calculate_engagement_score(self, profile: UserProfile) -> float:
        """Calculate user engagement score"""
        factors = {
            "frequency": min(1.0, profile.usage_stats.get("total_generations", 0) / 50),
            "session_length": min(1.0, profile.usage_stats.get("avg_session_duration", 0) / 600),
            "preference_strength": np.mean([p.confidence for p in profile.preferences]) if profile.preferences else 0,
            "feature_adoption": len(set(p.category for p in profile.preferences)) / 10
        }
        
        return sum(factors.values()) / len(factors)
    
    def _calculate_preference_diversity(self, profile: UserProfile) -> float:
        """Calculate diversity of user preferences"""
        if not profile.preferences:
            return 0.0
        
        categories = set(p.category for p in profile.preferences)
        values_per_category = {}
        
        for pref in profile.preferences:
            if pref.category not in values_per_category:
                values_per_category[pref.category] = set()
            values_per_category[pref.category].add(pref.value)
        
        avg_values_per_category = np.mean([len(values) for values in values_per_category.values()])
        return min(1.0, avg_values_per_category / 5)  # Normalize
    
    def _get_loyalty_indicators(self, profile: UserProfile) -> Dict[str, Any]:
        """Get loyalty indicators"""
        total_gens = profile.usage_stats.get("total_generations", 0)
        created_days_ago = (datetime.utcnow() - datetime.fromisoformat(profile.created_at.replace('Z', '+00:00'))).days
        
        return {
            "retention_days": created_days_ago,
            "usage_frequency": total_gens / max(1, created_days_ago),
            "feature_exploration": len(set(p.category for p in profile.preferences)),
            "quality_satisfaction": profile.quality_threshold
        }
    
    def _identify_growth_opportunities(self, profile: UserProfile) -> List[str]:
        """Identify opportunities to increase engagement"""
        opportunities = []
        
        total_gens = profile.usage_stats.get("total_generations", 0)
        used_categories = set(p.category for p in profile.preferences)
        
        if total_gens < 10:
            opportunities.append("新手引导：推荐热门主题和模板")
        
        if "video" not in used_categories:
            opportunities.append("功能推广：尝试视频生成功能")
        
        if "device_control" not in used_categories:
            opportunities.append("设备集成：连接智能灯具获得完整体验")
        
        if profile.quality_threshold < 0.7:
            opportunities.append("质量提升：推荐高级生成选项")
        
        if len(used_categories) < 3:
            opportunities.append("功能探索：体验更多创作类型")
        
        return opportunities
