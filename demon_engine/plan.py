from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from demon_engine.config import get_demon_dir

def get_plan_path(task_id: str, start_dir: Optional[Path] = None) -> Path:
    return get_demon_dir(start_dir) / "plans" / f"PLAN-{task_id.upper()}.md"

def create_plan_from_template(task_id: str, title: str, start_dir: Optional[Path] = None) -> Path:
    demon_dir = get_demon_dir(start_dir)
    template_path = demon_dir / "templates" / "plan_template.md"
    target_path = get_plan_path(task_id, start_dir)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    content = ""
    if template_path.exists():
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = "# Implementation Plan: [TASK_ID] - [TASK_TITLE]\n"
        
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    content = content.replace("[TASK_ID]", task_id)
    content = content.replace("[TASK_TITLE]", title)
    content = content.replace("[TIMESTAMP]", now)
    
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    return target_path

def read_plan(task_id: str, start_dir: Optional[Path] = None) -> Optional[str]:
    target_path = get_plan_path(task_id, start_dir)
    if not target_path.exists():
        return None
    with open(target_path, "r", encoding="utf-8") as f:
        return f.read()
