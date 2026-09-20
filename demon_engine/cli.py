import argparse
import sys
from pathlib import Path
from demon_engine.config import load_config, save_config, get_demon_dir, DEFAULT_CONFIG
from demon_engine.board import (
    load_board, save_board, add_task, move_task, get_task, render_ascii_board, STAGES
)
from demon_engine.spec import create_spec_from_template, read_spec, get_spec_path
from demon_engine.plan import create_plan_from_template, read_plan, get_plan_path
from demon_engine.gauntlet import run_gauntlet, format_gauntlet_report
from demon_engine.inbox import (
    create_inbox_item, resolve_inbox_item, render_inbox, load_inbox
)

def cmd_init(args):
    root_dir = Path.cwd()
    demon_dir = root_dir / ".demon"
    
    subdirs = ["specs", "plans", "reviews", "inbox", "templates", "runs"]
    for s in subdirs:
        (demon_dir / s).mkdir(parents=True, exist_ok=True)
        
    config = load_config(root_dir)
    save_config(config, root_dir)
    board = load_board(root_dir)
    save_board(board, root_dir)
    
    print(f"✨ Initialized demonOS workspace in {demon_dir}")
    print("📁 Folders created: specs/, plans/, reviews/, inbox/, templates/, runs/")
    print("🚀 You can now create tasks with: demon task new \"<title>\"")

def cmd_task_new(args):
    root_dir = Path.cwd()
    task = add_task(
        title=args.title,
        description=args.desc or "",
        priority=args.priority or "MEDIUM",
        start_dir=root_dir
    )
    task_id = task["id"]
    spec_path = create_spec_from_template(task_id, args.title, args.desc or "", root_dir)
    create_plan_from_template(task_id, args.title, root_dir)
    
    # Create Gate 1 notification in inbox
    inbox_item = create_inbox_item(
        task_id=task_id,
        category="APPROVAL_GATE",
        summary=f"Gate 1: Review & Approve Spec for {task_id} ({args.title})",
        details=f"Spec generated at {spec_path}. Check requirements, scope boundaries, and acceptance criteria.",
        options=["Approve Spec (Proceed to Plan & Code)", "Request Revisions"],
        severity="HIGH",
        start_dir=root_dir
    )
    
    print(f"✅ Created {task_id}: {args.title}")
    print(f"📄 Generated Spec : {spec_path.relative_to(root_dir)}")
    print(f"🔔 Notification   : {inbox_item['id']} created in human inbox")
    print(f"\nNext: Review spec and run `demon resolve {inbox_item['id']} --choice 'Approve'` to start coding!")

def cmd_task_list(args):
    root_dir = Path.cwd()
    print(render_ascii_board(root_dir))

def cmd_task_move(args):
    root_dir = Path.cwd()
    try:
        updated = move_task(args.id, args.stage, root_dir)
        if not updated:
            print(f"❌ Task {args.id} not found.")
            sys.exit(1)
        print(f"🔄 Moved {updated['id']} to stage: {updated['stage']}")
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def cmd_task_show(args):
    root_dir = Path.cwd()
    task = get_task(args.id, root_dir)
    if not task:
        print(f"❌ Task {args.id} not found.")
        sys.exit(1)
        
    print("=" * 60)
    print(f"  {task['id']}: {task['title']}")
    print("=" * 60)
    print(f"Stage       : {task.get('stage')}")
    print(f"Priority    : {task.get('priority')}")
    print(f"Created At  : {task.get('created_at')}")
    print(f"Description : {task.get('description') or 'N/A'}")
    print(f"Spec File   : {task.get('spec_file')}")
    print(f"Plan File   : {task.get('plan_file')}")
    print(f"Review File : {task.get('review_file')}")
    
    spec = read_spec(task['id'], root_dir)
    if spec:
        print("\n--- SPEC EXCERPT ---")
        for line in spec.splitlines()[:20]:
            print("  " + line)
        print("  ...")

def cmd_verify(args):
    root_dir = Path.cwd()
    print("🛡️  Running demonOS Verification Gauntlet...")
    report = run_gauntlet(root_dir, custom_test_cmd=args.test_cmd)
    print(format_gauntlet_report(report))
    if not report.get("overall_passed"):
        sys.exit(1)

def cmd_inbox(args):
    root_dir = Path.cwd()
    print(render_inbox(root_dir))

def cmd_resolve(args):
    root_dir = Path.cwd()
    choice = args.choice or "Approved / Resolved"
    resolved = resolve_inbox_item(args.item_id, choice, root_dir)
    if not resolved:
        print(f"❌ Inbox item {args.item_id} not found.")
        sys.exit(1)
        
    print(f"✅ Resolved {resolved['id']} with: {choice}")
    
    # Check if this item is linked to an approval gate and auto-advance task stage
    task_id = resolved.get("task_id")
    if task_id:
        task = get_task(task_id, root_dir)
        if task:
            current_stage = task.get("stage")
            if current_stage == "SPEC_DRAFTING" or current_stage == "PENDING_SPEC_APPROVAL":
                if "approve" in choice.lower():
                    move_task(task_id, "IN_PROGRESS", root_dir)
                    print(f"🚀 Gate 1 Passed: {task_id} transitioned to IN_PROGRESS!")
            elif current_stage == "IN_REVIEW" or current_stage == "PENDING_REVIEW_APPROVAL":
                if "approve" in choice.lower():
                    move_task(task_id, "DONE", root_dir)
                    print(f"🏁 Gate 2 Passed: {task_id} transitioned to DONE!")

def main():
    parser = argparse.ArgumentParser(
        prog="demon",
        description="demonOS: Autonomous Closed-Loop Agent Workflow Engine"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # init
    p_init = subparsers.add_parser("init", help="Initialize demonOS in current workspace")
    p_init.set_defaults(func=cmd_init)
    
    # task
    p_task = subparsers.add_parser("task", help="Task and Kanban board operations")
    task_subs = p_task.add_subparsers(dest="task_command", help="Task subcommands")
    
    # task new
    p_task_new = task_subs.add_parser("new", help="Create a new task & generate spec")
    p_task_new.add_argument("title", help="Task title")
    p_task_new.add_argument("--desc", help="Detailed description", default="")
    p_task_new.add_argument("--priority", choices=["HIGH", "MEDIUM", "LOW"], default="MEDIUM")
    p_task_new.set_defaults(func=cmd_task_new)
    
    # task list
    p_task_list = task_subs.add_parser("list", help="Render Kanban board")
    p_task_list.set_defaults(func=cmd_task_list)
    
    # task move
    p_task_move = task_subs.add_parser("move", help="Move a task to another stage")
    p_task_move.add_argument("id", help="Task ID (e.g. TASK-001)")
    p_task_move.add_argument("stage", choices=STAGES, help="Target stage")
    p_task_move.set_defaults(func=cmd_task_move)
    
    # task show
    p_task_show = task_subs.add_parser("show", help="Show task details and spec")
    p_task_show.add_argument("id", help="Task ID (e.g. TASK-001)")
    p_task_show.set_defaults(func=cmd_task_show)
    
    # verify
    p_verify = subparsers.add_parser("verify", help="Execute the verification gauntlet")
    p_verify.add_argument("--test-cmd", help="Override test command")
    p_verify.set_defaults(func=cmd_verify)
    
    # inbox
    p_inbox = subparsers.add_parser("inbox", help="View human approval gates and alerts")
    p_inbox.set_defaults(func=cmd_inbox)
    
    # resolve
    p_resolve = subparsers.add_parser("resolve", help="Resolve an inbox item or approval gate")
    p_resolve.add_argument("item_id", help="Inbox Item ID (e.g. INBOX-001)")
    p_resolve.add_argument("--choice", help="Resolution decision or comment", default="Approved")
    p_resolve.set_defaults(func=cmd_resolve)
    
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
        
    if args.command == "task" and not getattr(args, "task_command", None):
        p_task.print_help()
        sys.exit(0)
        
    args.func(args)

if __name__ == "__main__":
    main()
