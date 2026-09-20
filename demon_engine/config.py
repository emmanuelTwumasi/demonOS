import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

DEFAULT_CONFIG = {
    "name": "demonOS",
    "version": "1.0.0",
    "description": "Autonomous Agent Workflow System",
    "gauntlet": {
        "test_command": "python3 -m unittest discover -s tests -p '*_test.py'",
        "lint_command": "python3 -m py_compile $(git ls-files '*.py' 2>/dev/null)",
        "typecheck_command": "",
        "build_command": ""
    },
    "max_auto_repair_attempts": 3,
    "auto_advance_stages": False,
    "human_approval_gates": [
        "PENDING_SPEC_APPROVAL",
        "PENDING_REVIEW_APPROVAL"
    ]
}

def find_demon_root(start_dir: Optional[Path] = None) -> Path:
    """Find the directory containing the .demon folder by walking upwards."""
    current = start_dir or Path.cwd()
    while current != current.parent:
        if (current / ".demon").is_dir():
            return current
        current = current.parent
    return Path.cwd()

def get_demon_dir(start_dir: Optional[Path] = None) -> Path:
    return find_demon_root(start_dir) / ".demon"

def load_config(start_dir: Optional[Path] = None) -> Dict[str, Any]:
    config_file = get_demon_dir(start_dir) / "config.json"
    if not config_file.exists():
        return DEFAULT_CONFIG.copy()
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            merged = DEFAULT_CONFIG.copy()
            merged.update(data)
            return merged
    except Exception:
        return DEFAULT_CONFIG.copy()

def save_config(config_data: Dict[str, Any], start_dir: Optional[Path] = None) -> None:
    demon_dir = get_demon_dir(start_dir)
    demon_dir.mkdir(parents=True, exist_ok=True)
    with open(demon_dir / "config.json", "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2)
