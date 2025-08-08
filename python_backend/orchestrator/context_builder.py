# python_backend/orchestrator/context_builder.py
import os
from orchestrator.agent_state import AgentState
from agents.code_search_agent import CodeSearchAgent
from context_engine.file_discovery import discover_files

class ContextBuilder:
    """
    Builds the initial context for a user request by discovering, searching,
    and loading relevant files into the agent's state.
    """
    def __init__(self, state: AgentState, project_root: str = "."):
        self.state = state
        self.project_root = os.path.abspath(project_root)
        # Ensure the codebase index is initialized for searching
        if not self.state.codebase_index.is_indexed():
            self.state.codebase_index.index_directory(self.project_root)

    async def run(self):
        """
        Executes the context-building process.
        """
        await self.state.send_log("Starting context build...")

        # 1. Discover all files in the project (respecting .gitignore)
        await self.state.send_log("Discovering project files...")
        all_files = discover_files(self.project_root)
        await self.state.send_log(f"Found {len(all_files)} files in the project.")

        # 2. Perform a semantic search based on the user's request
        if not self.state.user_request:
            await self.state.send_log("No user request provided, skipping semantic search.")
            return

        await self.state.send_log(f"Searching for files relevant to: '{self.state.user_request}'")
        search_agent = CodeSearchAgent(self.state)
        search_results = search_agent.run(self.state.user_request)

        # 3. Load the content of the top search results into the state
        if not search_results:
            await self.state.send_log("No relevant files found from search.")
            return
            
        # Load top 3 files, for example
        files_to_load = [result['file_path'] for result in search_results[:3]]
        
        await self.state.send_log(f"Loading top {len(files_to_load)} files into context...")
        for file_path in files_to_load:
            if file_path not in self.state.loaded_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.state.load_file(file_path, content)
                    # Notify the frontend that a file has been loaded
                    await self.state.send_message("file_context", self.state.loaded_files)
                except Exception as e:
                    await self.state.send_log(f"Error loading file {file_path}: {e}")
        
        await self.state.send_log("Context build complete.")