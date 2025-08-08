# python_backend/orchestrator/prompt_parser.py
import re

class PromptParser:
    def __init__(self, raw_prompt: str):
        self.raw_prompt = raw_prompt.strip()
        self.command = ""
        self.args = []
        self.files = []
        self.instruction = ""

    def parse(self):
        """
        Parses the raw prompt to extract a command, arguments, file tags, and a core instruction.
        """
        # 1. Check for a command prefix
        if self.raw_prompt.startswith('/'):
            parts = self.raw_prompt.split()
            self.command = parts[0][1:].lower()
            self.args = parts[1:]
            # The rest of the logic might not apply for commands, but we can still extract files
            self._extract_files(self.raw_prompt)
            self.instruction = ' '.join(self.args) # The instruction is the arguments
        else:
            # Treat as a natural language prompt
            self.command = "prompt"
            self._extract_files(self.raw_prompt)
            # Remove file tags to get the clean instruction
            file_pattern = r'@([\w\./\\-]+)'
            self.instruction = re.sub(file_pattern, '', self.raw_prompt).strip()

        return {
            "command": self.command,
            "args": self.args,
            "files": self.files,
            "instruction": self.instruction
        }

    def _extract_files(self, text: str):
        """Extracts @filename tags from any text."""
        file_pattern = r'@([\w\./\\-]+)'
        self.files = re.findall(file_pattern, text)

