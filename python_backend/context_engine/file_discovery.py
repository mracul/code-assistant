import os
import pathspec

SUPPORTED_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.json', '.md', '.html', '.css',
    '.yml', '.yaml', '.sh', '.bash', '.java', '.c', '.cpp', '.h', '.hpp',
    '.go', '.rs', '.php', '.rb', '.sql', '.txt'
}

def discover_files(start_path: str):
    """
    Recursively discovers files in a directory, respecting a top-level .gitignore file.
    Yields paths for supported files that are not ignored.
    """
    gitignore_path = os.path.join(start_path, '.gitignore')
    spec = None
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            spec = pathspec.PathSpec.from_lines('gitwildmatch', f.readlines())

    for root, dirs, files in os.walk(start_path, topdown=True):
        # Prune ignored directories
        if spec:
            rel_root = os.path.relpath(root, start_path)
            # Add trailing slash for directory matching
            # Use '.' for the root directory itself
            rel_root_for_match = rel_root if rel_root != '.' else ''

            original_dirs = list(dirs) # copy before modifying
            dirs[:] = [d for d in original_dirs if not spec.match_file(os.path.join(rel_root_for_match, d) + '/')]

        for file in files:
            # Avoid processing files in the .git directory
            if '.git' in root.split(os.sep):
                continue

            file_path = os.path.join(root, file)

            # Get relative path for matching
            relative_path = os.path.relpath(file_path, start_path)

            if spec and spec.match_file(relative_path):
                continue

            _, ext = os.path.splitext(file)
            if ext.lower() in SUPPORTED_EXTENSIONS:
                yield file_path
