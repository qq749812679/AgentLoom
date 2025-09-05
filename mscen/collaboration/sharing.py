from __future__ import annotations

import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class SharedProject:
    project_id: str
    title: str
    description: str
    creator_id: str
    creator_name: str
    created_at: str
    is_public: bool
    tags: List[str]
    content: Dict[str, Any]  # Generated content paths and metadata
    stats: Dict[str, int]  # views, likes, downloads
    collaboration_settings: Dict[str, Any]


@dataclass
class CollaborationSession:
    session_id: str
    project_id: str
    participants: List[str]
    created_at: str
    last_activity: str
    shared_state: Dict[str, Any]
    is_active: bool


class SharingManager:
    def __init__(self, storage_dir: Path) -> None:
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.projects_dir = self.storage_dir / "shared_projects"
        self.sessions_dir = self.storage_dir / "collaboration_sessions"
        self.projects_dir.mkdir(exist_ok=True)
        self.sessions_dir.mkdir(exist_ok=True)
    
    def share_project(self, 
                     creator_id: str, 
                     creator_name: str,
                     title: str, 
                     content: Dict[str, Any],
                     description: str = "",
                     tags: List[str] = None,
                     is_public: bool = True) -> str:
        """Share a project and return share ID"""
        project_id = str(uuid.uuid4())[:8]
        
        shared_project = SharedProject(
            project_id=project_id,
            title=title,
            description=description,
            creator_id=creator_id,
            creator_name=creator_name,
            created_at=datetime.utcnow().isoformat(),
            is_public=is_public,
            tags=tags or [],
            content=content,
            stats={"views": 0, "likes": 0, "downloads": 0},
            collaboration_settings={
                "allow_comments": True,
                "allow_remixes": True,
                "allow_downloads": True
            }
        )
        
        # Save project
        project_file = self.projects_dir / f"{project_id}.json"
        with project_file.open("w", encoding="utf-8") as f:
            json.dump(asdict(shared_project), f, ensure_ascii=False, indent=2)
        
        return project_id
    
    def get_shared_project(self, project_id: str) -> Optional[SharedProject]:
        """Get shared project by ID"""
        project_file = self.projects_dir / f"{project_id}.json"
        if not project_file.exists():
            return None
        
        try:
            with project_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                return SharedProject(**data)
        except Exception:
            return None
    
    def browse_shared_projects(self, 
                              tags: List[str] = None,
                              creator_id: str = None,
                              search_query: str = "",
                              sort_by: str = "created_at",
                              limit: int = 20) -> List[SharedProject]:
        """Browse shared projects with filters"""
        projects = []
        
        for project_file in self.projects_dir.glob("*.json"):
            try:
                with project_file.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    project = SharedProject(**data)
                    
                    # Apply filters
                    if not project.is_public:
                        continue
                    
                    if creator_id and project.creator_id != creator_id:
                        continue
                    
                    if tags and not any(tag in project.tags for tag in tags):
                        continue
                    
                    if search_query:
                        search_fields = f"{project.title} {project.description} {' '.join(project.tags)}".lower()
                        if search_query.lower() not in search_fields:
                            continue
                    
                    projects.append(project)
            except Exception:
                continue
        
        # Sort projects
        if sort_by == "created_at":
            projects.sort(key=lambda p: p.created_at, reverse=True)
        elif sort_by == "popularity":
            projects.sort(key=lambda p: p.stats["views"] + p.stats["likes"], reverse=True)
        elif sort_by == "likes":
            projects.sort(key=lambda p: p.stats["likes"], reverse=True)
        
        return projects[:limit]
    
    def update_project_stats(self, project_id: str, action: str) -> bool:
        """Update project statistics"""
        project = self.get_shared_project(project_id)
        if not project:
            return False
        
        if action == "view":
            project.stats["views"] += 1
        elif action == "like":
            project.stats["likes"] += 1
        elif action == "download":
            project.stats["downloads"] += 1
        
        # Save updated project
        project_file = self.projects_dir / f"{project_id}.json"
        with project_file.open("w", encoding="utf-8") as f:
            json.dump(asdict(project), f, ensure_ascii=False, indent=2)
        
        return True
    
    def create_collaboration_session(self, project_id: str, creator_id: str) -> str:
        """Create a real-time collaboration session"""
        session_id = str(uuid.uuid4())[:8]
        
        session = CollaborationSession(
            session_id=session_id,
            project_id=project_id,
            participants=[creator_id],
            created_at=datetime.utcnow().isoformat(),
            last_activity=datetime.utcnow().isoformat(),
            shared_state={
                "current_theme": "",
                "current_parameters": {},
                "chat_messages": [],
                "pending_changes": {}
            },
            is_active=True
        )
        
        # Save session
        session_file = self.sessions_dir / f"{session_id}.json"
        with session_file.open("w", encoding="utf-8") as f:
            json.dump(asdict(session), f, ensure_ascii=False, indent=2)
        
        return session_id
    
    def join_collaboration_session(self, session_id: str, user_id: str) -> bool:
        """Join an existing collaboration session"""
        session_file = self.sessions_dir / f"{session_id}.json"
        if not session_file.exists():
            return False
        
        try:
            with session_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                session = CollaborationSession(**data)
            
            if not session.is_active:
                return False
            
            if user_id not in session.participants:
                session.participants.append(user_id)
                session.last_activity = datetime.utcnow().isoformat()
                
                # Save updated session
                with session_file.open("w", encoding="utf-8") as f:
                    json.dump(asdict(session), f, ensure_ascii=False, indent=2)
            
            return True
        except Exception:
            return False
    
    def update_collaboration_state(self, session_id: str, user_id: str, updates: Dict[str, Any]) -> bool:
        """Update shared collaboration state"""
        session_file = self.sessions_dir / f"{session_id}.json"
        if not session_file.exists():
            return False
        
        try:
            with session_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                session = CollaborationSession(**data)
            
            if user_id not in session.participants or not session.is_active:
                return False
            
            # Update shared state
            session.shared_state.update(updates)
            session.last_activity = datetime.utcnow().isoformat()
            
            # Add to chat if it's a chat message
            if "chat_message" in updates:
                chat_entry = {
                    "user_id": user_id,
                    "message": updates["chat_message"],
                    "timestamp": datetime.utcnow().isoformat()
                }
                session.shared_state["chat_messages"].append(chat_entry)
                
                # Keep only last 50 messages
                session.shared_state["chat_messages"] = session.shared_state["chat_messages"][-50:]
            
            # Save updated session
            with session_file.open("w", encoding="utf-8") as f:
                json.dump(asdict(session), f, ensure_ascii=False, indent=2)
            
            return True
        except Exception:
            return False
    
    def get_collaboration_session(self, session_id: str) -> Optional[CollaborationSession]:
        """Get collaboration session details"""
        session_file = self.sessions_dir / f"{session_id}.json"
        if not session_file.exists():
            return None
        
        try:
            with session_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                return CollaborationSession(**data)
        except Exception:
            return None
    
    def end_collaboration_session(self, session_id: str, user_id: str) -> bool:
        """End a collaboration session"""
        session = self.get_collaboration_session(session_id)
        if not session or user_id not in session.participants:
            return False
        
        session.is_active = False
        session.last_activity = datetime.utcnow().isoformat()
        
        # Save final state
        session_file = self.sessions_dir / f"{session_id}.json"
        with session_file.open("w", encoding="utf-8") as f:
            json.dump(asdict(session), f, ensure_ascii=False, indent=2)
        
        return True
    
    def cleanup_old_sessions(self, days_old: int = 7) -> int:
        """Clean up old inactive sessions"""
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        cleaned_count = 0
        
        for session_file in self.sessions_dir.glob("*.json"):
            try:
                with session_file.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    session = CollaborationSession(**data)
                
                last_activity = datetime.fromisoformat(session.last_activity.replace('Z', '+00:00'))
                if last_activity < cutoff_date and not session.is_active:
                    session_file.unlink()
                    cleaned_count += 1
            except Exception:
                continue
        
        return cleaned_count
    
    def export_project_for_sharing(self, content: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Export project in shareable format"""
        export_data = {
            "version": "1.0",
            "exported_at": datetime.utcnow().isoformat(),
            "metadata": metadata,
            "content": content,
            "generation_info": {
                "theme": metadata.get("theme", ""),
                "parameters": metadata.get("parameters", {}),
                "model_versions": metadata.get("model_versions", {}),
                "total_generation_time": metadata.get("generation_time", 0)
            },
            "compatibility": {
                "min_app_version": "1.0.0",
                "required_features": ["basic_generation"],
                "optional_features": ["device_control", "video_generation"]
            }
        }
        
        return export_data
    
    def import_shared_project(self, shared_data: Dict[str, Any], user_id: str) -> Optional[Dict[str, Any]]:
        """Import a shared project"""
        try:
            # Validate format
            if shared_data.get("version") != "1.0":
                return None
            
            # Extract content and metadata
            content = shared_data.get("content", {})
            metadata = shared_data.get("metadata", {})
            generation_info = shared_data.get("generation_info", {})
            
            # Create local project
            imported_project = {
                "imported_at": datetime.utcnow().isoformat(),
                "imported_by": user_id,
                "original_metadata": metadata,
                "content": content,
                "generation_info": generation_info,
                "import_source": "shared_project"
            }
            
            return imported_project
        except Exception:
            return None
    
    def get_trending_tags(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get trending tags from shared projects"""
        tag_counts = {}
        
        for project_file in self.projects_dir.glob("*.json"):
            try:
                with project_file.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    project = SharedProject(**data)
                    
                    if project.is_public:
                        for tag in project.tags:
                            if tag not in tag_counts:
                                tag_counts[tag] = {"count": 0, "recent_views": 0}
                            tag_counts[tag]["count"] += 1
                            tag_counts[tag]["recent_views"] += project.stats.get("views", 0)
            except Exception:
                continue
        
        # Sort by combination of frequency and recent activity
        trending_tags = []
        for tag, stats in tag_counts.items():
            score = stats["count"] * 2 + stats["recent_views"] * 0.1
            trending_tags.append({
                "tag": tag,
                "count": stats["count"],
                "score": score
            })
        
        trending_tags.sort(key=lambda x: x["score"], reverse=True)
        return trending_tags[:limit]
    
    def generate_share_link(self, project_id: str, access_type: str = "view") -> str:
        """Generate shareable link for project"""
        # In a real implementation, this would generate a secure link
        base_url = "https://your-app.com/share"
        return f"{base_url}/{project_id}?access={access_type}"
    
    def get_user_projects(self, user_id: str) -> List[SharedProject]:
        """Get all projects created by a user"""
        user_projects = []
        
        for project_file in self.projects_dir.glob("*.json"):
            try:
                with project_file.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    project = SharedProject(**data)
                    
                    if project.creator_id == user_id:
                        user_projects.append(project)
            except Exception:
                continue
        
        # Sort by creation date
        user_projects.sort(key=lambda p: p.created_at, reverse=True)
        return user_projects
