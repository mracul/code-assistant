# python_backend/utils/path_validator.py
import os

class PathValidator:
    def __init__(self, path: str, base_directory: str = "."):
        self.raw_path = path
        self.base_directory = os.path.abspath(base_directory)
        self.absolute_path = ""
        self.error = ""

    def validate(self) -> bool:
        """
        Validates the path for existence, permissions, and ensures it's within the project directory.
        Returns True if valid, False otherwise.
        """
        # 1. Normalize to an absolute path
        # This handles both absolute and relative paths provided by the user.
        self.absolute_path = os.path.abspath(os.path.join(self.base_directory, self.raw_path))

        # 2. Security Check: Ensure the path is within the base project directory
        if not self.absolute_path.startswith(self.base_directory):
            self.error = "Path is outside the allowed project directory."
            return False

        # 3. Check for existence
        if not os.path.exists(self.absolute_path):
            self.error = "Path does not exist."
            return False

        # 4. Check for read permissions
        if not os.access(self.absolute_path, os.R_OK):
            self.error = "Path is not readable."
            return False
        
        return True
