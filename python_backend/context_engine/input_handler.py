import os

def validate_path(path: str):
    """
    Validates if the given path exists.
    Raises ValueError if the path is invalid.
    """
    if not os.path.exists(path):
        raise ValueError(f"Path does not exist: {path}")
