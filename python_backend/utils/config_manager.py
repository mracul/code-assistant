# python_backend/utils/config_manager.py
import json
import os

class ConfigManager:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        """Loads the configuration from the JSON file."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return self._default_config()
        return self._default_config()

    def save_config(self):
        """Saves the current configuration to the JSON file."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get(self, key, default=None):
        """Gets a value from the configuration."""
        return self.config.get(key, default)

    def set(self, key, value):
        """Sets a value in the configuration and saves it."""
        self.config[key] = value
        self.save_config()

    def _default_config(self):
        """Returns the default configuration."""
        return {
            "recent_files": [],
            "preferred_agents": {},
            "user_preferences": {}
        }

    def add_recent_file(self, file_path):
        """Adds a file to the list of recent files."""
        recent_files = self.get("recent_files", [])
        if file_path in recent_files:
            recent_files.remove(file_path)
        recent_files.insert(0, file_path)
        self.set("recent_files", recent_files[:10]) # Keep only the 10 most recent
