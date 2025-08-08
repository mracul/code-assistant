# orchestrator.py
from utils import swe_tools
from orchestrator.agent_state import AgentState

class Orchestrator:
    def __init__(self, repo_path="."):
        # Initialize all the critical tools
        self.ast_parser = swe_tools.ASTParserTool()
        self.code_retriever = swe_tools.CodeRetrieverTool()
        self.token_estimator = swe_tools.TokenEstimateTool()
        self.prompt_builder = swe_tools.PromptContextBuilderTool()
        self.diff_formatter = swe_tools.DiffFormatterTool()
        self.dependency_grapher = swe_tools.DependencyGraphTool()
        self.flow_analyzer = swe_tools.RuntimeFlowAnalyzerTool()
        self.design_refactorer = swe_tools.DesignRefactorTool()
        self.repo_path = repo_path

    def run_analysis_workflow(self, file_path: str, function_name: str):
        """
        Example workflow demonstrating how to use the tools to analyze code.
        """
        state = AgentState(
            file_path=file_path,
            function_name=function_name,
            logs=[]
        )

        # 1. Read and parse the file
        state.logs.append(f"Analyzing file: {file_path}")
        with open(file_path, 'r') as f:
            content = f.read()
        
        state.ast_tree = self.ast_parser.parse(content)
        state.logs.append("Successfully parsed file into AST.")

        # 2. Analyze dependencies
        # In a real scenario, you'd get all project files
        all_files = [file_path] 
        state.dependency_graph = self.dependency_grapher.build_graph(all_files)
        state.logs.append("Successfully built dependency graph.")

        # 3. Analyze runtime flow from an entry point
        state.runtime_flow = self.flow_analyzer.analyze_flow(all_files, function_name)
        state.logs.append(f"Successfully analyzed runtime flow for '{function_name}'.")

        # 4. Retrieve semantically similar code
        state.similar_code = self.code_retriever.search(query=f"code related to {function_name}")
        state.logs.append("Retrieved semantically similar code chunks.")

        # 5. Propose a refactoring (using the placeholder tool)
        state.proposed_refactoring = self.design_refactorer.refactor_with_pattern(
            code=content,
            pattern_name="Singleton",
            instructions="Ensure only one instance of a key class is created."
        )
        state.logs.append("Proposed a design pattern-based refactoring.")

        # 6. Create a diff of the proposed change
        state.refactoring_diff = self.diff_formatter.create_diff(content, state.proposed_refactoring)
        state.logs.append("Formatted the proposed refactoring as a diff.")

        # 7. Estimate token count for a final prompt
        final_prompt_context = {
            "diff": state.refactoring_diff,
            "flow": state.runtime_flow,
            "dependencies": state.dependency_graph
        }
        final_prompt = self.prompt_builder.build_prompt(
            "Review the following change: {diff}\nFlow: {flow}\nDependencies: {dependencies}",
            final_prompt_context
        )
        state.token_estimate = self.token_estimator.count(final_prompt)
        state.logs.append(f"Estimated final prompt token count: {state.token_estimate}")

        return state

# Example usage:
if __name__ == '__main__':
    # This assumes you run it from the `python_backend` directory
    # and have a file named `main.py` to analyze.
    orchestrator = Orchestrator()
    final_state = orchestrator.run_analysis_workflow('main.py', 'user_input')
    
    print("--- Orchestration Complete ---")
    for log in final_state.logs:
        print(log)
    
    print("\n--- Final State ---")
    # Print a subset of the state for clarity
    print(f"Token Estimate: {final_state.token_estimate}")
    print(f"Refactoring Diff:\n{final_state.refactoring_diff}")
