import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
from demon_engine.config import get_demon_dir

def get_inbox_file(start_dir: Optional[Path] = None) -> Path:
    return get_demon_dir(start_dir) / "inbox" / "inbox.json"

def load_inbox(start_dir: Optional[Path] = None) -> Dict[str, Any]:
    inbox_file = get_inbox_file(start_dir)
    if not inbox_file.exists():
        return {"items": []}
    try:
        with open(inbox_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"items": []}

def save_inbox(data: Dict[str, Any], start_dir: Optional[Path] = None) -> None:
    inbox_file = get_inbox_file(start_dir)
    inbox_file.parent.mkdir(parents=True, exist_ok=True)
    with open(inbox_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def create_inbox_item(
    task_id: str,
    category: str,
    summary: str,
    details: str = "",
    options: Optional[List[str]] = None,
    severity: str = "MEDIUM",
    start_dir: Optional[Path] = None
) -> Dict[str, Any]:
    inbox = load_inbox(start_dir)
    item_num = len(inbox.get("items", [])) + 1
    item_id = f"INBOX-{item_num:03d}"
    now = datetime.now(timezone.utc).isoformat()
    
    item = {
        "id": item_id,
        "task_id": task_id,
        "category": category.upper(),
        "severity": severity.upper(),
        "status": "OPEN",
        "summary": summary,
        "details": details,
        "options": options or ["Approve / Proceed", "Reject / Modify"],
        "created_at": now,
        "resolved_at": None,
        "resolution": None
    }
    inbox.setdefault("items", []).append(item)
    save_inbox(inbox, start_dir)
    
    # Also write a readable markdown note in .demon/inbox/
    demon_dir = get_demon_dir(start_dir)
    md_file = demon_dir / "inbox" / f"{item_id}.md"
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(f"# {item_id}: {summary}\n\n")
        f.write(f"- **Task**: {task_id}\n")
        f.write(f"- **Category**: {category.upper()}\n")
        f.write(f"- **Severity**: {severity.upper()}\n")
        f.write(f"- **Created**: {now}\n\n")
        f.write(f"## Details\n{details or 'No additional details.'}\n\n")
        f.write("## Options\n")
        for idx, opt in enumerate(item["options"], 1):
            f.write(f"{idx}. {opt}\n")
        f.write("\n## Action\n")
        f.write(f"Resolve in chat or run:\n`demon resolve {item_id} --choice \"<option>\"`\n")
        
    return item

def resolve_inbox_item(item_id: str, resolution: str, start_dir: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    inbox = load_inbox(start_dir)
    found_item = None
    for item in inbox.get("items", []):
        if item.get("id", "").upper() == item_id.upper():
            item["status"] = "RESOLVED"
            item["resolved_at"] = datetime.now(timezone.utc).isoformat()
            item["resolution"] = resolution
            found_item = item
            break
            
    if found_item:
        save_inbox(inbox, start_dir)
    return found_item

def render_inbox(start_dir: Optional[Path] = None) -> str:
    inbox = load_inbox(start_dir)
    items = inbox.get("items", [])
    open_items = [i for i in items if i.get("status") == "OPEN"]
    
    lines = []
    lines.append("=" * 70)
    lines.append(f"  demonOS HUMAN INBOX ({len(open_items)} pending / {len(items)} total)")
    lines.append("=" * 70)
    
    if not open_items:
        lines.append("\n  ✨ Inbox is clean! No human approvals or decisions pending.\n")
    else:
        for i in open_items:
            lines.append(f"\n🔔 [{i['id']}] [{i['category']}] ({i['severity']}) -> Task: {i['task_id']}")
            lines.append(f"   Summary: {i['summary']}")
            if i.get("details"):
                lines.append(f"   Details: {i['details'][:100]}")
            lines.append("   Options:")
            for idx, opt in enumerate(i.get("options", []), 1):
                lines.append(f"     [{idx}] {opt}")
    lines.append("\n" + "=" * 70)
    return "\n".join(lines)
