import uuid
from typing import Dict, Any

class SessionMemory:
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {"history": []}
        return session_id

    def add_interaction(self, session_id: str, user_input: str, agent_output: str):
        if session_id in self.sessions:
            self.sessions[session_id]["history"].append({
                "user": user_input,
                "agent": agent_output
            })

    def get_history(self, session_id: str):
        return self.sessions.get(session_id, {}).get("history", [])

    def clear_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

session_memory = SessionMemory()
