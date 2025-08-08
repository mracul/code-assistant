# python_backend/orchestrator/agent_state.py
from orchestrator.conversation_history import ConversationHistory
from context_engine.codebase_index import CodebaseIndex
import json

class AgentState:
    """
    A structured class to manage the agent's state, context, and memory.
    """
    def __init__(self, connection_id: str, project_root: str):
        # Core Conversation with persistence
        history_path = f".conversation_history_{connection_id}.json"
        self.conversation_history = ConversationHistory(persist_path=history_path)
        
        # Centralized Code Index
        self.codebase_index = CodebaseIndex()

        # File Management
        self.loaded_files = {}  # path: content
        self.modified_buffers = {} # path: new_content
        
        # Connection & Workflow State
        self.websocket = None
        self.user_request = ""
        self.last_agent_output = None
        self.proposed_strategies = []
        self.selected_solution = None
        self.project_root = project_root

    async def connect(self, websocket):
        """Establishes the WebSocket connection for the client."""
        await websocket.accept()
        self.websocket = websocket

    def disconnect(self):
        """Clears the WebSocket connection."""
        self.websocket = None
        self.conversation_history.save() # Save history on disconnect

    def add_message(self, role: str, content: str, embed: bool = False):
        """Adds a message to the conversation history."""
        self.conversation_history.add_message(role, content, embed)

    def load_file(self, file_path: str, content: str):
        """Loads file content into the state."""
        self.loaded_files[file_path] = content

    def get_full_context_for_prompt(self) -> dict:
        """Assembles all relevant information for a comprehensive prompt."""
        return {
            "user_request": self.user_request,
            "conversation_history": self.conversation_history.get_history(),
            "loaded_files": self.loaded_files,
            "modified_buffers": self.modified_buffers,
            "last_agent_output": self.last_agent_output
        }

    async def send_message(self, type: str, data: dict):
        """Sends a structured message to the frontend."""
        if self.websocket:
            await self.websocket.send_text(json.dumps({"type": type, "data": data}))

    async def send_log(self, data: str):
        """Sends a log message to the frontend."""
        if self.websocket:
            await self.send_message("log", {"message": data})
    
    async def send_diff(self, file_path: str, diff_text: str):
        """Sends a diff to the frontend."""
        if self.websocket:
            await self.send_message("diff", {"file_path": file_path, "diff": diff_text})