import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
from demon_engine.config import load_config, get_demon_dir

def run_command_step(command: str, root_dir: Path) -> Dict[str, Any]:
    if not command.strip():
        return {
            "command": command,
            "status": "SKIPPED",
            "exit_code": 0,
            "stdout": "",
            "stderr": ""
        }
        
    try:
        proc = subprocess.run(
            command,
            shell=True,
            cwd=str(root_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300
        )
        status = "PASSED" if proc.returncode == 0 else "FAILED"
        return {
            "command": command,
            "status": status,
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            "command": command,
            "status": "TIMEOUT",
            "exit_code": -1,
            "stdout": "",
            "stderr": "Execution timed out after 300 seconds."
        }
    except Exception as e:
        return {
            "command": command,
            "status": "ERROR",
            "exit_code": -1,
            "stdout": "",
            "stderr": str(e)
        }

def run_gauntlet(start_dir: Optional[Path] = None, custom_test_cmd: Optional[str] = None) -> Dict[str, Any]:
    root_dir = start_dir or Path.cwd()
    demon_dir = get_demon_dir(root_dir)
    config = load_config(root_dir)
    gauntlet_cfg = config.get("gauntlet", {})
    
    test_cmd = custom_test_cmd or gauntlet_cfg.get("test_command", "")
    lint_cmd = gauntlet_cfg.get("lint_command", "")
    typecheck_cmd = gauntlet_cfg.get("typecheck_command", "")
    build_cmd = gauntlet_cfg.get("build_command", "")
    
    steps = [
        ("LINT", lint_cmd),
        ("TYPECHECK", typecheck_cmd),
        ("TESTS", test_cmd),
        ("BUILD", build_cmd)
    ]
    
    results: List[Dict[str, Any]] = []
    overall_passed = True
    
    for step_name, cmd in steps:
        if not cmd or not cmd.strip():
            continue
        res = run_command_step(cmd, root_dir)
        res["step"] = step_name
        results.append(res)
        if res["status"] != "PASSED" and res["status"] != "SKIPPED":
            overall_passed = False
            # Stop immediately on failure so agent can fix it
            break
            
    now = datetime.now(timezone.utc)
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")
    runs_dir = demon_dir / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    log_file = runs_dir / f"GAUNTLET_{timestamp_str}.log"
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"demonOS Gauntlet Run: {now.isoformat()}\n")
        f.write(f"Overall Result: {'PASSED' if overall_passed else 'FAILED'}\n")
        f.write("=" * 70 + "\n\n")
        for r in results:
            f.write(f"[{r['step']}] Command: {r['command']}\n")
            f.write(f"Status: {r['status']} (Exit Code: {r['exit_code']})\n")
            if r['stdout']:
                f.write("STDOUT:\n" + r['stdout'] + "\n")
            if r['stderr']:
                f.write("STDERR:\n" + r['stderr'] + "\n")
            f.write("-" * 70 + "\n")
            
    return {
        "timestamp": now.isoformat(),
        "overall_passed": overall_passed,
        "results": results,
        "log_file": str(log_file)
    }

def format_gauntlet_report(report: Dict[str, Any]) -> str:
    lines = []
    lines.append("=" * 60)
    lines.append("  demonOS VERIFICATION GAUNTLET")
    lines.append("=" * 60)
    for r in report.get("results", []):
        icon = "✅" if r["status"] == "PASSED" else "❌"
        lines.append(f" {icon} {r['step']:<12}: {r['status']}")
        if r["status"] != "PASSED":
            lines.append(f"    Command: {r['command']}")
            if r["stderr"]:
                lines.append(f"    Error: {r['stderr'].strip()[:200]}")
            elif r["stdout"]:
                lines.append(f"    Output: {r['stdout'].strip()[:200]}")
    lines.append("-" * 60)
    overall = "🎉 GAUNTLET PASSED" if report.get("overall_passed") else "🛑 GAUNTLET FAILED - REPAIR NEEDED"
    lines.append(f"  {overall}")
    lines.append(f"  Log: {report.get('log_file')}")
    lines.append("=" * 60)
    return "\n".join(lines)
