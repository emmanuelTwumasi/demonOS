import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
from demon_engine.config import get_demon_dir

STAGES = [
    "BACKLOG",
    "SPEC_DRAFTING",
    "PENDING_SPEC_APPROVAL",
    "IN_PROGRESS",
    "IN_REVIEW",
    "PENDING_REVIEW_APPROVAL",
    "DONE"
]

STAGE_EMOJIS = {
    "BACKLOG": "📋",
    "SPEC_DRAFTING": "📐",
    "PENDING_SPEC_APPROVAL": "⏳",
    "IN_PROGRESS": "⚡",
    "IN_REVIEW": "🔍",
    "PENDING_REVIEW_APPROVAL": "🚦",
    "DONE": "✅"
}

def get_board_file(start_dir: Optional[Path] = None) -> Path:
    return get_demon_dir(start_dir) / "board.json"

def load_board(start_dir: Optional[Path] = None) -> Dict[str, Any]:
    board_file = get_board_file(start_dir)
    if not board_file.exists():
        return {
            "project": "demonOS",
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "stages": STAGES,
            "tasks": []
        }
    try:
        with open(board_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "project": "demonOS",
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "stages": STAGES,
            "tasks": []
        }

def save_board(board: Dict[str, Any], start_dir: Optional[Path] = None) -> None:
    board_file = get_board_file(start_dir)
    board_file.parent.mkdir(parents=True, exist_ok=True)
    board["updated_at"] = datetime.now(timezone.utc).isoformat()
    with open(board_file, "w", encoding="utf-8") as f:
        json.dump(board, f, indent=2)

def generate_task_id(board: Dict[str, Any]) -> str:
    existing_nums = []
    for task in board.get("tasks", []):
        tid = task.get("id", "")
        if tid.startswith("TASK-"):
            try:
                num = int(tid.split("-")[1])
                existing_nums.append(num)
            except ValueError:
                pass
    next_num = max(existing_nums, default=0) + 1
    return f"TASK-{next_num:03d}"

def add_task(title: str, description: str = "", priority: str = "MEDIUM", start_dir: Optional[Path] = None) -> Dict[str, Any]:
    board = load_board(start_dir)
    task_id = generate_task_id(board)
    now = datetime.now(timezone.utc).isoformat()
    
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "priority": priority.upper(),
        "stage": "SPEC_DRAFTING",
        "created_at": now,
        "updated_at": now,
        "spec_file": f".demon/specs/SPEC-{task_id}.md",
        "plan_file": f".demon/plans/PLAN-{task_id}.md",
        "review_file": f".demon/reviews/REVIEW-{task_id}.md"
    }
    board.setdefault("tasks", []).append(task)
    save_board(board, start_dir)
    return task

def get_task(task_id: str, start_dir: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    board = load_board(start_dir)
    for task in board.get("tasks", []):
        if task.get("id", "").upper() == task_id.upper():
            return task
    return None

def move_task(task_id: str, target_stage: str, start_dir: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    board = load_board(start_dir)
    target_stage = target_stage.upper()
    if target_stage not in STAGES:
        raise ValueError(f"Invalid stage '{target_stage}'. Allowed stages: {', '.join(STAGES)}")
    
    found_task = None
    for task in board.get("tasks", []):
        if task.get("id", "").upper() == task_id.upper():
            task["stage"] = target_stage
            task["updated_at"] = datetime.now(timezone.utc).isoformat()
            found_task = task
            break
            
    if found_task:
        save_board(board, start_dir)
    return found_task

def render_ascii_board(start_dir: Optional[Path] = None) -> str:
    board = load_board(start_dir)
    tasks = board.get("tasks", [])
    
    lines = []
    lines.append("=" * 78)
    lines.append(f"  demonOS TASK BOARD | {board.get('project', 'demonOS')} ({len(tasks)} tasks total)")
    lines.append("=" * 78)
    
    by_stage: Dict[str, List[Dict[str, Any]]] = {s: [] for s in STAGES}
    for t in tasks:
        stage = t.get("stage", "BACKLOG")
        if stage in by_stage:
            by_stage[stage].append(t)
        else:
            by_stage.setdefault("BACKLOG", []).append(t)
            
    for stage in STAGES:
        stage_tasks = by_stage[stage]
        emoji = STAGE_EMOJIS.get(stage, "•")
        lines.append(f"\n{emoji} [{stage}] ({len(stage_tasks)})")
        lines.append("-" * 78)
        if not stage_tasks:
            lines.append("  (No tasks)")
        else:
            for t in stage_tasks:
                prio = t.get("priority", "MEDIUM")
                prio_badge = f"[{prio}]"
                lines.append(f"  • {t['id']} {prio_badge:<8} {t['title']}")
                if t.get("description"):
                    lines.append(f"    └─ {t['description'][:65]}")
    lines.append("\n" + "=" * 78)
    return "\n".join(lines)
