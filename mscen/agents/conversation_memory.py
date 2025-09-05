from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


class ConversationMemory:
    def __init__(self, memory_dir: Path) -> None:
        self.memory_dir = memory_dir
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.session_file = self.memory_dir / "current_session.json"
        self.history_file = self.memory_dir / "conversation_history.jsonl"
        self.current_session: List[Dict[str, Any]] = []
        self._load_session()
    
    def _load_session(self) -> None:
        if self.session_file.exists():
            try:
                with self.session_file.open("r", encoding="utf-8") as f:
                    self.current_session = json.load(f)
            except Exception:
                self.current_session = []
    
    def _save_session(self) -> None:
        with self.session_file.open("w", encoding="utf-8") as f:
            json.dump(self.current_session, f, ensure_ascii=False, indent=2)
    
    def add_turn(self, user_input: str, system_output: Dict[str, Any], feedback: Optional[Dict[str, Any]] = None) -> None:
        turn = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_input": user_input,
            "system_output": system_output,
            "feedback": feedback
        }
        self.current_session.append(turn)
        self._save_session()
        
        # Also append to history file
        with self.history_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(turn, ensure_ascii=False) + "\n")
    
    def get_recent_context(self, max_turns: int = 5) -> List[Dict[str, Any]]:
        return self.current_session[-max_turns:]
    
    def clear_session(self) -> None:
        self.current_session = []
        if self.session_file.exists():
            self.session_file.unlink()
    
    def get_user_preferences(self) -> Dict[str, Any]:
        # Analyze conversation history to extract preferences
        themes = []
        successful_outputs = []
        
        for turn in self.current_session:
            if turn.get("feedback", {}).get("rating", 0) >= 4:  # Good feedback
                themes.append(turn.get("user_input", ""))
                successful_outputs.append(turn.get("system_output", {}))
        
        return {
            "preferred_themes": themes[-10:],  # Last 10 successful themes
            "successful_patterns": successful_outputs[-10:]
        }
