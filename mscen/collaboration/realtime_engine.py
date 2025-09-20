"""
Real-time collaboration engine with WebSocket support
Enables live multi-user creation sessions with conflict resolution
"""

from __future__ import annotations

import asyncio
import json
import time
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum

from ..core.logger import JsonlLogger


class OperationType(Enum):
    """Types of collaborative operations"""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    MOVE = "move"
    STYLE_CHANGE = "style_change"
    PARAMETER_CHANGE = "parameter_change"
    MEDIA_UPLOAD = "media_upload"
    COMMENT = "comment"
    CURSOR_MOVE = "cursor_move"
    SELECTION = "selection"


@dataclass
class CollaborativeOperation:
    """Represents a single collaborative operation"""
    id: str
    session_id: str
    user_id: str
    user_name: str
    operation_type: OperationType
    target_id: str
    data: Dict[str, Any]
    timestamp: float
    applied: bool = False
    conflicts: List[str] = None

    def __post_init__(self):
        if self.conflicts is None:
            self.conflicts = []


@dataclass
class CollaborationSession:
    """Real-time collaboration session"""
    id: str
    name: str
    owner_id: str
    participants: Dict[str, Dict[str, Any]]
    created_at: datetime
    last_activity: datetime
    settings: Dict[str, Any]
    shared_state: Dict[str, Any]
    operation_log: List[CollaborativeOperation]
    active: bool = True

    def __post_init__(self):
        if not self.participants:
            self.participants = {}
        if not self.shared_state:
            self.shared_state = {}
        if not self.operation_log:
            self.operation_log = []


class ConflictResolver:
    """Handles conflicts in real-time collaborative editing"""

    def __init__(self, logger: JsonlLogger):
        self.logger = logger

    def resolve_conflicts(self, operations: List[CollaborativeOperation]) -> List[CollaborativeOperation]:
        """Resolve conflicts between concurrent operations using operational transformation"""
        resolved_operations = []

        # Sort operations by timestamp
        sorted_ops = sorted(operations, key=lambda op: op.timestamp)

        for i, op in enumerate(sorted_ops):
            # Check for conflicts with previously resolved operations
            conflicts = self._detect_conflicts(op, resolved_operations)

            if conflicts:
                # Apply operational transformation
                transformed_op = self._transform_operation(op, conflicts)
                if transformed_op:
                    resolved_operations.append(transformed_op)
                    self.logger.log({
                        "event": "collaboration.conflict_resolved",
                        "operation_id": op.id,
                        "conflicts": [c.id for c in conflicts],
                        "transformation_applied": True
                    })
            else:
                resolved_operations.append(op)

        return resolved_operations

    def _detect_conflicts(self, operation: CollaborativeOperation,
                         resolved_ops: List[CollaborativeOperation]) -> List[CollaborativeOperation]:
        """Detect conflicts between operations"""
        conflicts = []

        for resolved_op in resolved_ops:
            if self._operations_conflict(operation, resolved_op):
                conflicts.append(resolved_op)

        return conflicts

    def _operations_conflict(self, op1: CollaborativeOperation, op2: CollaborativeOperation) -> bool:
        """Check if two operations conflict with each other"""
        # Same target conflicts
        if op1.target_id == op2.target_id:
            # Concurrent modifications to the same object
            if abs(op1.timestamp - op2.timestamp) < 1.0:  # Within 1 second
                return True

        # Dependency conflicts
        if op1.operation_type == OperationType.DELETE and op2.target_id == op1.target_id:
            return True

        return False

    def _transform_operation(self, operation: CollaborativeOperation,
                           conflicts: List[CollaborativeOperation]) -> Optional[CollaborativeOperation]:
        """Transform operation to resolve conflicts using operational transformation"""
        transformed_op = CollaborativeOperation(
            id=str(uuid.uuid4()),
            session_id=operation.session_id,
            user_id=operation.user_id,
            user_name=operation.user_name,
            operation_type=operation.operation_type,
            target_id=operation.target_id,
            data=operation.data.copy(),
            timestamp=time.time(),
            conflicts=[c.id for c in conflicts]
        )

        # Apply transformation based on conflict type
        for conflict in conflicts:
            if conflict.operation_type == OperationType.DELETE:
                # Can't modify deleted object
                return None

            elif conflict.operation_type == OperationType.UPDATE:
                # Merge updates intelligently
                if operation.operation_type == OperationType.UPDATE:
                    transformed_op.data = self._merge_updates(operation.data, conflict.data)

            elif conflict.operation_type == OperationType.MOVE:
                # Adjust positions for moves
                if "position" in operation.data and "position" in conflict.data:
                    transformed_op.data["position"] = self._adjust_position(
                        operation.data["position"],
                        conflict.data["position"]
                    )

        return transformed_op

    def _merge_updates(self, update1: Dict[str, Any], update2: Dict[str, Any]) -> Dict[str, Any]:
        """Intelligently merge two update operations"""
        merged = update1.copy()

        for key, value in update2.items():
            if key not in merged:
                merged[key] = value
            else:
                # For numeric values, take the average
                if isinstance(value, (int, float)) and isinstance(merged[key], (int, float)):
                    merged[key] = (merged[key] + value) / 2
                # For strings, prefer the longer one
                elif isinstance(value, str) and isinstance(merged[key], str):
                    merged[key] = value if len(value) > len(merged[key]) else merged[key]
                # For others, prefer the newer value
                else:
                    merged[key] = value

        return merged

    def _adjust_position(self, pos1: Dict[str, float], pos2: Dict[str, float]) -> Dict[str, float]:
        """Adjust position to avoid overlap"""
        adjusted = pos1.copy()

        # Simple strategy: offset slightly if positions are close
        if abs(pos1.get("x", 0) - pos2.get("x", 0)) < 10:
            adjusted["x"] = pos1.get("x", 0) + 15

        if abs(pos1.get("y", 0) - pos2.get("y", 0)) < 10:
            adjusted["y"] = pos1.get("y", 0) + 15

        return adjusted


class RealtimeCollaborationEngine:
    """Main engine for real-time collaboration"""

    def __init__(self, base_dir: Path, logger: JsonlLogger):
        self.base_dir = base_dir
        self.logger = logger
        self.conflict_resolver = ConflictResolver(logger)

        # In-memory session storage (in production, use Redis or similar)
        self.sessions: Dict[str, CollaborationSession] = {}
        self.user_sessions: Dict[str, str] = {}  # user_id -> session_id
        self.operation_queue: Dict[str, List[CollaborativeOperation]] = {}

        # WebSocket connections (would be actual WebSocket connections in production)
        self.connections: Dict[str, List[Callable]] = {}

        # Auto-save and cleanup
        self._start_background_tasks()

    def create_session(self, name: str, owner_id: str, owner_name: str,
                      settings: Optional[Dict[str, Any]] = None) -> str:
        """Create a new collaboration session"""
        session_id = str(uuid.uuid4())[:8]

        if settings is None:
            settings = {
                "max_participants": 10,
                "auto_save_interval": 30,
                "conflict_resolution": "auto",
                "permissions": {
                    "all": ["view", "comment"],
                    "collaborators": ["view", "edit", "comment"],
                    "owner": ["view", "edit", "comment", "admin"]
                }
            }

        session = CollaborationSession(
            id=session_id,
            name=name,
            owner_id=owner_id,
            participants={
                owner_id: {
                    "name": owner_name,
                    "role": "owner",
                    "joined_at": datetime.now().isoformat(),
                    "cursor_position": {"x": 0, "y": 0},
                    "selection": None,
                    "active": True
                }
            },
            created_at=datetime.now(),
            last_activity=datetime.now(),
            settings=settings,
            shared_state={
                "current_theme": "",
                "generation_params": {},
                "media_assets": [],
                "comments": []
            }
        )

        self.sessions[session_id] = session
        self.user_sessions[owner_id] = session_id
        self.operation_queue[session_id] = []

        self.logger.log({
            "event": "collaboration.session_created",
            "session_id": session_id,
            "owner_id": owner_id,
            "name": name
        })

        return session_id

    def join_session(self, session_id: str, user_id: str, user_name: str) -> bool:
        """Join an existing collaboration session"""
        if session_id not in self.sessions:
            return False

        session = self.sessions[session_id]

        # Check if session is full
        max_participants = session.settings.get("max_participants", 10)
        if len(session.participants) >= max_participants:
            return False

        # Add participant
        session.participants[user_id] = {
            "name": user_name,
            "role": "collaborator",
            "joined_at": datetime.now().isoformat(),
            "cursor_position": {"x": 0, "y": 0},
            "selection": None,
            "active": True
        }

        self.user_sessions[user_id] = session_id
        session.last_activity = datetime.now()

        # Broadcast join event
        self._broadcast_to_session(session_id, {
            "type": "user_joined",
            "user_id": user_id,
            "user_name": user_name,
            "timestamp": time.time()
        })

        self.logger.log({
            "event": "collaboration.user_joined",
            "session_id": session_id,
            "user_id": user_id,
            "user_name": user_name
        })

        return True

    def leave_session(self, user_id: str) -> bool:
        """Leave the current session"""
        if user_id not in self.user_sessions:
            return False

        session_id = self.user_sessions[user_id]
        session = self.sessions.get(session_id)

        if not session:
            return False

        # Remove participant
        if user_id in session.participants:
            session.participants[user_id]["active"] = False
            session.last_activity = datetime.now()

            # Broadcast leave event
            self._broadcast_to_session(session_id, {
                "type": "user_left",
                "user_id": user_id,
                "timestamp": time.time()
            })

        del self.user_sessions[user_id]

        self.logger.log({
            "event": "collaboration.user_left",
            "session_id": session_id,
            "user_id": user_id
        })

        return True

    def submit_operation(self, user_id: str, operation_type: OperationType,
                        target_id: str, data: Dict[str, Any]) -> Optional[str]:
        """Submit a collaborative operation"""
        if user_id not in self.user_sessions:
            return None

        session_id = self.user_sessions[user_id]
        session = self.sessions.get(session_id)

        if not session or user_id not in session.participants:
            return None

        # Create operation
        operation = CollaborativeOperation(
            id=str(uuid.uuid4()),
            session_id=session_id,
            user_id=user_id,
            user_name=session.participants[user_id]["name"],
            operation_type=operation_type,
            target_id=target_id,
            data=data,
            timestamp=time.time()
        )

        # Add to operation queue
        if session_id not in self.operation_queue:
            self.operation_queue[session_id] = []

        self.operation_queue[session_id].append(operation)

        # Process operation immediately
        self._process_operations(session_id)

        self.logger.log({
            "event": "collaboration.operation_submitted",
            "session_id": session_id,
            "operation_id": operation.id,
            "user_id": user_id,
            "operation_type": operation_type.value
        })

        return operation.id

    def _process_operations(self, session_id: str):
        """Process pending operations for a session"""
        if session_id not in self.operation_queue:
            return

        operations = self.operation_queue[session_id]
        if not operations:
            return

        # Resolve conflicts
        resolved_ops = self.conflict_resolver.resolve_conflicts(operations)

        session = self.sessions[session_id]

        # Apply resolved operations
        for op in resolved_ops:
            self._apply_operation(session, op)
            op.applied = True

        # Add to session log
        session.operation_log.extend(resolved_ops)
        session.last_activity = datetime.now()

        # Broadcast operations to all participants
        for op in resolved_ops:
            self._broadcast_to_session(session_id, {
                "type": "operation_applied",
                "operation": asdict(op),
                "timestamp": time.time()
            })

        # Clear processed operations
        self.operation_queue[session_id] = [op for op in operations if not op.applied]

    def _apply_operation(self, session: CollaborationSession, operation: CollaborativeOperation):
        """Apply an operation to the session state"""
        if operation.operation_type == OperationType.PARAMETER_CHANGE:
            session.shared_state["generation_params"].update(operation.data)

        elif operation.operation_type == OperationType.UPDATE:
            if operation.target_id == "theme":
                session.shared_state["current_theme"] = operation.data.get("value", "")

        elif operation.operation_type == OperationType.MEDIA_UPLOAD:
            session.shared_state["media_assets"].append({
                "id": operation.target_id,
                "type": operation.data.get("type"),
                "url": operation.data.get("url"),
                "uploaded_by": operation.user_id,
                "timestamp": operation.timestamp
            })

        elif operation.operation_type == OperationType.COMMENT:
            session.shared_state["comments"].append({
                "id": operation.id,
                "target_id": operation.target_id,
                "user_id": operation.user_id,
                "user_name": operation.user_name,
                "text": operation.data.get("text", ""),
                "timestamp": operation.timestamp
            })

        elif operation.operation_type == OperationType.CURSOR_MOVE:
            if operation.user_id in session.participants:
                session.participants[operation.user_id]["cursor_position"] = operation.data

        elif operation.operation_type == OperationType.SELECTION:
            if operation.user_id in session.participants:
                session.participants[operation.user_id]["selection"] = operation.data

    def get_session_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get the current state of a session"""
        session = self.sessions.get(session_id)
        if not session:
            return None

        return {
            "session_info": {
                "id": session.id,
                "name": session.name,
                "owner_id": session.owner_id,
                "created_at": session.created_at.isoformat(),
                "last_activity": session.last_activity.isoformat(),
                "active": session.active
            },
            "participants": session.participants,
            "shared_state": session.shared_state,
            "recent_operations": [
                asdict(op) for op in session.operation_log[-10:]  # Last 10 operations
            ]
        }

    def update_cursor_position(self, user_id: str, x: float, y: float):
        """Update user's cursor position"""
        self.submit_operation(
            user_id,
            OperationType.CURSOR_MOVE,
            "cursor",
            {"x": x, "y": y}
        )

    def add_comment(self, user_id: str, target_id: str, text: str) -> Optional[str]:
        """Add a comment to a target element"""
        return self.submit_operation(
            user_id,
            OperationType.COMMENT,
            target_id,
            {"text": text}
        )

    def _broadcast_to_session(self, session_id: str, message: Dict[str, Any]):
        """Broadcast a message to all session participants"""
        if session_id in self.connections:
            for callback in self.connections[session_id]:
                try:
                    callback(message)
                except Exception as e:
                    self.logger.log({
                        "event": "collaboration.broadcast_error",
                        "session_id": session_id,
                        "error": str(e)
                    })

    def register_connection(self, session_id: str, callback: Callable):
        """Register a connection callback for session updates"""
        if session_id not in self.connections:
            self.connections[session_id] = []
        self.connections[session_id].append(callback)

    def unregister_connection(self, session_id: str, callback: Callable):
        """Unregister a connection callback"""
        if session_id in self.connections:
            try:
                self.connections[session_id].remove(callback)
            except ValueError:
                pass

    def _start_background_tasks(self):
        """Start background tasks for auto-save and cleanup"""
        # In a real implementation, this would start async tasks
        pass

    def cleanup_inactive_sessions(self, max_age_hours: int = 24):
        """Clean up inactive sessions"""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)

        inactive_sessions = [
            session_id for session_id, session in self.sessions.items()
            if session.last_activity < cutoff_time
        ]

        for session_id in inactive_sessions:
            self._cleanup_session(session_id)

    def _cleanup_session(self, session_id: str):
        """Clean up a specific session"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.active = False

            # Remove user mappings
            users_to_remove = [
                user_id for user_id, sid in self.user_sessions.items()
                if sid == session_id
            ]

            for user_id in users_to_remove:
                del self.user_sessions[user_id]

            # Clean up operation queue
            if session_id in self.operation_queue:
                del self.operation_queue[session_id]

            # Clean up connections
            if session_id in self.connections:
                del self.connections[session_id]

            self.logger.log({
                "event": "collaboration.session_cleaned_up",
                "session_id": session_id
            })

    def export_session_data(self, session_id: str, output_path: Path) -> bool:
        """Export session data for backup or analysis"""
        session = self.sessions.get(session_id)
        if not session:
            return False

        session_data = {
            "session_info": {
                "id": session.id,
                "name": session.name,
                "owner_id": session.owner_id,
                "created_at": session.created_at.isoformat(),
                "last_activity": session.last_activity.isoformat(),
                "settings": session.settings
            },
            "participants": session.participants,
            "shared_state": session.shared_state,
            "operation_log": [asdict(op) for op in session.operation_log],
            "exported_at": datetime.now().isoformat()
        }

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False, default=str)
            return True
        except Exception as e:
            self.logger.log({
                "event": "collaboration.export_failed",
                "session_id": session_id,
                "error": str(e)
            })
            return False