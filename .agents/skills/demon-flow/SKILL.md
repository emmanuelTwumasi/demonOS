---
name: demon-flow
description: >-
  Autonomous closed-loop task execution pipeline for demonOS. Follows Danny Postma's
  AgentOS pattern (Spec -> Approval Gate -> Plan -> Gauntlet Loop -> Review -> PR)
  enabling end-to-end task completion with minimal human intervention.
---

# demon-flow: Autonomous Agent Task Runbook

Use this skill whenever you are tasked with implementing features, fixing bugs, or refactoring in a repository utilizing **demonOS**.

---

## The Autonomous Execution Cycle

```
  1. Intake & Spec
       │
       ▼
  2. Gate 1: Spec Approval (Only checkpoint before code)
       │
       ▼
  3. Plan Breakdown & Task Tree
       │
       ▼
  4. Autonomous Execution (Atomic edits)
       │
       ▼
  5. Verification Gauntlet Loop (Auto-repair tests/lint/build)
       │
       ▼
  6. Senior Code Review (Diff & security audit)
       │
       ▼
  7. Gate 2: Delivery & PR
```

---

## Operational Commands

### 1. Initialize Task
```bash
./bin/demon task new "<Task Title>" --desc "<Short description>" --priority HIGH
```
- Populates `.demon/specs/SPEC-<id>.md`
- Creates `.demon/plans/PLAN-<id>.md`
- Creates an alert in `.demon/inbox/`

### 2. Check Board & Open Approvals
```bash
./bin/demon task list
./bin/demon inbox
```

### 3. Move Task Along Pipeline
```bash
./bin/demon task move <id> IN_PROGRESS
./bin/demon task move <id> IN_REVIEW
./bin/demon task move <id> DONE
```

### 4. Run the Verification Gauntlet
```bash
./bin/demon verify
```
- Runs all configured checks in `.demon/config.json` (`test_command`, `lint_command`, `typecheck_command`, `build_command`).
- Outputs log to `.demon/runs/GAUNTLET_<timestamp>.log`.
- **Must pass 100%** before moving to `IN_REVIEW`.

### 5. Resolve Human Inbox Notification
```bash
./bin/demon resolve <item_id> --choice "Approved"
```

---

## Subagent Specialization Guidelines

When handling large or complex features:
1. **Architect Role (Parent Agent)**: Writes the Spec, plans the task breakdown, and coordinates stages.
2. **Researcher Subagent (`invoke_subagent` type: 'research')**: Explores complex external libraries, documentation, or large codebase files when necessary.
3. **Builder Role**: Executes atomic code changes according to the plan.
4. **Verifier / Gauntlet**: Runs `./bin/demon verify` and handles self-repair iterations.
5. **Reviewer Role**: Audits git diff against the approved spec and writes `.demon/reviews/REVIEW-<id>.md`.
