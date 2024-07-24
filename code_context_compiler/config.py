from pathlib import Path
from typing import Any, Dict

import yaml

DEFAULT_CONFIG = {
    "ignore_patterns": [
        ".git",  # Ignore the entire .git directory
        ".git/**/*",  # Ignore all contents of .git directory (for thoroughness)
        "*.log",
        "*.tmp",
        "poetry.lock",
        "package-lock.json",
        "yarn.lock",
        "Pipfile.lock",
        "pnpm-lock.yaml",
        "composer.lock",
        "Gemfile.lock",
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".DS_Store",
        "node_modules",
        "venv",
        ".env",
    ],
    "file_extensions": [],  # Empty list means all file extensions are included
    "mask_patterns": [
        r'password\s*=\s*["\'].*?["\']',
        r'api[_-]?key\s*=\s*["\'].*?["\']',
        r'secret\s*=\s*["\'].*?["\']',
        r'token\s*=\s*["\'].*?["\']',
        r'client[_-]?id\s*=\s*["\'].*?["\']',
        r'client[_-]?secret\s*=\s*["\'].*?["\']',
        r'access[_-]?token\s*=\s*["\'].*?["\']',
        r'refresh[_-]?token\s*=\s*["\'].*?["\']',
        r'private[_-]?key\s*=\s*["\'].*?["\']',
        r'public[_-]?key\s*=\s*["\'].*?["\']',
        r'aws[_-]?access[_-]?key[_-]?id\s*=\s*["\'].*?["\']',
        r'aws[_-]?secret[_-]?access[_-]?key\s*=\s*["\'].*?["\']',
        r'ssh[_-]?key\s*=\s*["\'].*?["\']',
        r'database[_-]?url\s*=\s*["\'].*?["\']',
        r'username\s*=\s*["\'].*?["\']',
    ],
    "use_git": False,
}


def load_config(config_path: Path = None) -> Dict[str, Any]:
    """
    Load configuration from a YAML file or return default config if no file is provided.
    """
    if config_path and config_path.exists():
        with open(config_path, "r") as config_file:
            user_config = yaml.safe_load(config_file)
        return {**DEFAULT_CONFIG, **user_config}
    return DEFAULT_CONFIG
