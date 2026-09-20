# demonOS 🚀

**demonOS** is an autonomous AI agent operating system and task execution framework modeled directly after **Danny Postma's talk: *"How I Built My Own AgentOS on Claude's Agent SDK"***.

It eliminates the tedious back-and-forth micro-management common in AI coding assistants, transforming Antigravity into a self-driving engineering partner that takes tasks from concept to verified delivery with minimal human oversight.

---

## 💡 The Core Philosophy

Most AI coding workflows suffer from:
- **Babysitting**: Prompting step-by-step ("now add this file... now fix that error...").
- **Premature coding**: Agents writing code based on misaligned assumptions.
- **Unverified hallucinations**: Agents claiming "done!" while tests are failing or code doesn't build.

**demonOS solves this using the 2-Gate Closed-Loop Model:**

```
[User Request]
      │
      ▼
1. SPEC DRAFTING ───> 🛑 GATE 1: Spec Approval (You spend 10s checking scope)
                              │ (Approved)
                              ▼
                      2. ATOMIC PLANNING
                              │
                              ▼
                      3. AUTONOMOUS IMPLEMENTATION
                              │
                              ▼
                      4. VERIFICATION GAUNTLET (Self-Healing Loop)
                         [Lint + Tests + Typecheck + Build]
                              │ (Passing)
                              ▼
                      5. SENIOR CODE & SECURITY REVIEW
                              │
                              ▼
                      🛑 GATE 2: Delivery & Merge (You review the diff & commit)
```

**Between Gate 1 and Gate 2, the agent operates 100% autonomously.**

---

## 📦 What's Inside

- **`bin/demon`**: Zero-dependency Python CLI for managing tasks, the Kanban board, the verification gauntlet, and the inbox.
- **`.demon/`**: Machine-readable persistent workspace state:
  - `board.json`: Real-time Kanban board state.
  - `config.json`: Project-specific gauntlet test/lint/build commands.
  - `specs/`: Feature specifications with explicit Definitions of Done (DoD).
  - `plans/`: Atomic execution plans.
  - `reviews/`: Automated quality and security audit reports.
  - `inbox/`: Escalations and approvals requiring human sign-off.
  - `runs/`: Execution and test logs from the Verification Gauntlet.
- **`AGENTS.md` & `GEMINI.md`**: Pre-configured behavioral rules that instruct Antigravity on how to behave autonomously.
- **`.agents/skills/demon-flow/`**: Built-in Antigravity skill that guides multi-step execution and self-healing.

---

## ⚡ Quick Start

### 1. Check the Board and Inbox
```bash
./bin/demon task list
./bin/demon inbox
```

### 2. Create a New Feature Task
```bash
./bin/demon task new "Implement User Authentication" --desc "Add JWT login and register endpoints" --priority HIGH
```
This automatically:
- Creates `TASK-001` in stage `SPEC_DRAFTING`.
- Generates `.demon/specs/SPEC-TASK-001.md`.
- Generates `.demon/plans/PLAN-TASK-001.md`.
- Raises an item in `.demon/inbox/` for Gate 1 (Spec Approval).

### 3. Approve the Spec (Gate 1)
```bash
./bin/demon resolve INBOX-001 --choice "Approved"
```
Or simply tell Antigravity in chat: *"Spec approved, proceed with implementation."*

### 4. Run the Verification Gauntlet
```bash
./bin/demon verify
```
Runs linting, unit testing, and building as defined in `.demon/config.json`. Logs full stdout/stderr to `.demon/runs/`.

---

## 🛠️ Configuring Project Checks

Edit `.demon/config.json` to configure the commands for your specific tech stack:

```json
{
  "name": "demonOS",
  "gauntlet": {
    "test_command": "python3 -m unittest discover -s tests -p '*_test.py'",
    "lint_command": "python3 -m py_compile $(git ls-files '*.py' 2>/dev/null)",
    "typecheck_command": "",
    "build_command": ""
  },
  "max_auto_repair_attempts": 3
}
```

For a Node / TypeScript project, you would set:
```json
"gauntlet": {
  "test_command": "npm test",
  "lint_command": "npm run lint",
  "typecheck_command": "npx tsc --noEmit",
  "build_command": "npm run build"
}
```

---

## 🎯 The Minimal Human Assistance Workflow

When chatting with Antigravity, you only need to say:

> **"demon: build [feature description]"**

Antigravity will:
1. Initialize the task and write the detailed Spec.
2. Pause at **Gate 1** and present you with the 2-sentence summary and Spec link.
3. You reply: *"Approved"* or give 1 bullet point of adjustment.
4. Antigravity writes the plan, implements the code, runs the test gauntlet, fixes any errors, writes the code review, and presents the completed feature at **Gate 2**.
