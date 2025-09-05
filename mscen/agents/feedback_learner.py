from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class FeedbackEntry:
    user_input: str
    system_output: Dict[str, Any]
    rating: int  # 1-5 scale
    comments: str
    timestamp: str


class FeedbackLearner:
    def __init__(self, feedback_dir: Path) -> None:
        self.feedback_dir = feedback_dir
        self.feedback_dir.mkdir(parents=True, exist_ok=True)
        self.feedback_file = self.feedback_dir / "feedback_data.jsonl"
        
    def record_feedback(self, entry: FeedbackEntry) -> None:
        data = {
            "user_input": entry.user_input,
            "system_output": entry.system_output,
            "rating": entry.rating,
            "comments": entry.comments,
            "timestamp": entry.timestamp
        }
        
        with self.feedback_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    
    def get_feedback_stats(self) -> Dict[str, Any]:
        if not self.feedback_file.exists():
            return {"total": 0, "avg_rating": 0, "rating_distribution": {}}
        
        ratings = []
        rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        with self.feedback_file.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    rating = data.get("rating", 0)
                    if 1 <= rating <= 5:
                        ratings.append(rating)
                        rating_counts[rating] += 1
                except:
                    continue
        
        return {
            "total": len(ratings),
            "avg_rating": np.mean(ratings) if ratings else 0,
            "rating_distribution": rating_counts
        }
    
    def get_successful_patterns(self, min_rating: int = 4) -> List[Dict[str, Any]]:
        patterns = []
        
        if not self.feedback_file.exists():
            return patterns
            
        with self.feedback_file.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    if data.get("rating", 0) >= min_rating:
                        patterns.append({
                            "input": data.get("user_input", ""),
                            "output": data.get("system_output", {}),
                            "rating": data.get("rating", 0)
                        })
                except:
                    continue
        
        return patterns[-20:]  # Return last 20 successful patterns
    
    def suggest_improvements(self, current_input: str) -> Dict[str, Any]:
        # Simple similarity-based recommendation
        successful = self.get_successful_patterns()
        
        if not successful:
            return {"suggestions": [], "confidence": 0}
        
        # Find similar inputs (basic keyword matching)
        input_words = set(current_input.lower().split())
        similarities = []
        
        for pattern in successful:
            pattern_words = set(pattern["input"].lower().split())
            similarity = len(input_words & pattern_words) / len(input_words | pattern_words) if input_words | pattern_words else 0
            similarities.append((similarity, pattern))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[0], reverse=True)
        top_similar = similarities[:3]
        
        suggestions = []
        for sim, pattern in top_similar:
            if sim > 0.2:  # Threshold for relevance
                suggestions.append({
                    "similar_input": pattern["input"],
                    "successful_output": pattern["output"],
                    "similarity": sim,
                    "rating": pattern["rating"]
                })
        
        return {
            "suggestions": suggestions,
            "confidence": max([s["similarity"] for s in suggestions]) if suggestions else 0
        }
