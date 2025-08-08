# python_backend/orchestrator/context_builder.py
import os
from orchestrator.agent_state import AgentState
from agents.code_search_agent import CodeSearchAgent
from context_engine.file_discovery import discover_files

class ContextBuilder:
    """
    Builds context by discovering, indexing, and searching files.
    """
    def __init__(self, state: AgentState):
        self.state = state
        self.project_root = state.project_root

    async def run_initial_scan(self):
        """
        Performs the initial, one-time scan and indexing of the entire project.
        This is typically run once when the server starts or a new project is loaded.
        """
        await self.state.send_log("Performing initial codebase scan...")
        
        # 1. Discover all files and convert the generator to a list
        all_files = list(discover_files(self.project_root))
        await self.state.send_log(f"Found {len(all_files)} total files.")
        
        # 2. Index the entire directory for future searches
        await self.state.send_log("Creating codebase index for semantic search...")
        self.state.codebase_index.index_directory(self.project_root)
        await self.state.send_log("Codebase indexing complete.")

    async def run(self):
        """
        Builds context specifically for the current user_request. This runs
        after the initial scan and before the main agentic workflow.
        """
        await self.state.send_log("Building context for the current prompt...")

        if not self.state.user_request:
            await self.state.send_log("No user request provided, skipping file search.")
            return

        if not self.state.codebase_index.is_indexed():
            await self.state.send_log("Warning: Codebase index is not ready. Context may be incomplete.")
            return

        # Perform a semantic search to find the most relevant files
        await self.state.send_log(f"Searching for files relevant to: '{self.state.user_request}'")
        search_agent = CodeSearchAgent(self.state)
        search_results = search_agent.run(self.state.user_request)

        if not search_results:
            await self.state.send_log("No relevant files found from search.")
            return
            
        # Load the top 3 most relevant files into the agent's state
        files_to_load = [result['file_path'] for result in search_results[:3]]
        
        await self.state.send_log(f"Loading top {len(files_to_load)} files into context...")
        for file_path in files_to_load:
            if file_path not in self.state.loaded_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.state.load_file(file_path, content)
                    await self.state.send_message("file_context", self.state.loaded_files)
                except Exception as e:
                    await self.state.send_log(f"Error loading file {file_path}: {e}")
        
        await self.state.send_log("Prompt-specific context build complete.")
