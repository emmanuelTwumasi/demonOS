import unittest
import shutil
import tempfile
from pathlib import Path
from demon_engine.config import load_config, save_config, get_demon_dir
from demon_engine.board import (
    load_board, save_board, add_task, move_task, get_task, STAGES
)
from demon_engine.spec import create_spec_from_template, read_spec
from demon_engine.plan import create_plan_from_template, read_plan
from demon_engine.inbox import (
    create_inbox_item, resolve_inbox_item, load_inbox
)
from demon_engine.gauntlet import run_gauntlet

class TestDemonEngine(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.demon_dir = self.test_dir / ".demon"
        self.demon_dir.mkdir(parents=True)
        (self.demon_dir / "templates").mkdir(parents=True)
        # copy real templates to temp
        real_templates = Path(__file__).resolve().parent.parent / ".demon" / "templates"
        if real_templates.exists():
            for item in real_templates.iterdir():
                if item.is_file():
                    shutil.copy(item, self.demon_dir / "templates" / item.name)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_config_loader(self):
        cfg = load_config(self.test_dir)
        self.assertEqual(cfg["name"], "demonOS")
        self.assertIn("gauntlet", cfg)

    def test_task_lifecycle(self):
        task = add_task("Build Auth Module", "Support JWT authentication", "HIGH", self.test_dir)
        self.assertEqual(task["id"], "TASK-001")
        self.assertEqual(task["stage"], "SPEC_DRAFTING")
        self.assertEqual(task["priority"], "HIGH")
        
        # Verify get_task
        fetched = get_task("TASK-001", self.test_dir)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["title"], "Build Auth Module")
        
        # Verify move_task
        moved = move_task("TASK-001", "IN_PROGRESS", self.test_dir)
        self.assertEqual(moved["stage"], "IN_PROGRESS")
        
        # Verify invalid stage rejection
        with self.assertRaises(ValueError):
            move_task("TASK-001", "NON_EXISTENT_STAGE", self.test_dir)

    def test_spec_and_plan_generation(self):
        spec_path = create_spec_from_template("TASK-001", "Build Auth Module", "Support JWT auth", self.test_dir)
        self.assertTrue(spec_path.exists())
        content = read_spec("TASK-001", self.test_dir)
        self.assertIn("Feature Spec: TASK-001 - Build Auth Module", content)
        self.assertIn("Definition of Done (DoD)", content)
        
        plan_path = create_plan_from_template("TASK-001", "Build Auth Module", self.test_dir)
        self.assertTrue(plan_path.exists())
        plan_content = read_plan("TASK-001", self.test_dir)
        self.assertIn("Implementation Plan: TASK-001 - Build Auth Module", plan_content)

    def test_inbox_and_resolution(self):
        item = create_inbox_item(
            task_id="TASK-001",
            category="APPROVAL_GATE",
            summary="Spec Approval Needed",
            details="Check spec",
            severity="HIGH",
            start_dir=self.test_dir
        )
        self.assertEqual(item["id"], "INBOX-001")
        self.assertEqual(item["status"], "OPEN")
        
        resolved = resolve_inbox_item("INBOX-001", "Approved", self.test_dir)
        self.assertEqual(resolved["status"], "RESOLVED")
        self.assertEqual(resolved["resolution"], "Approved")

    def test_gauntlet_execution(self):
        report = run_gauntlet(self.test_dir, custom_test_cmd="echo 'Test passed'")
        self.assertTrue(report["overall_passed"])

if __name__ == "__main__":
    unittest.main()
