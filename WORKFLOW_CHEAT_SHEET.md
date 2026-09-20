# demonOS Cheat Sheet: Minimal Assistance Workflow

Keep this open whenever you want Antigravity to do heavy lifting while you stay high-leverage.

---

## 🏎️ The 3 Golden Commands for Emmanuel

### 1. The Delegation Prompt (Start a Feature)
> *"demon: build [what you want built, e.g. 'a secure JWT authentication service with refresh tokens and SQLite persistence']"*

Antigravity will create the task, draft the Spec in `.demon/specs/`, define acceptance criteria, and notify you at **Gate 1**.

---

### 2. The Approval Prompt (Gate 1 Sign-Off)
> *"Approved. Run the flow autonomously."*

Antigravity will now:
- Break down the task into atomic steps.
- Write the code across all necessary files.
- Write unit tests for all new logic.
- Run `./bin/demon verify` (the Gauntlet).
- Automatically fix any test/lint errors without bugging you.
- Perform a self-review of security and performance in `.demon/reviews/`.

---

### 3. The Delivery Prompt (Gate 2 Sign-Off)
Antigravity will present:
- Summary of verified tests.
- Diff summary and review findings.
- Link to the commit/PR.

You reply:
> *"Looks good, ship it."*

---

## 🚨 When Antigravity Will Interrupt You (The Inbox)
Antigravity will only ask you a question if:
1. It needs an external API key or token that cannot be simulated (e.g. `STRIPE_SECRET_KEY`).
2. An unresolvable business decision needs a human call (e.g. *"Delete existing table or migrate data?"*).
3. The Verification Gauntlet failed after 3 consecutive auto-repair attempts.

---

## 💻 Handy CLI Shortcuts
| Command | What it does |
|---|---|
| `./bin/demon task list` | View the live Kanban board in your terminal |
| `./bin/demon inbox` | View pending approvals or blocker items |
| `./bin/demon verify` | Run tests, lint, and build checks immediately |
| `./bin/demon task show <TASK-ID>` | View details and spec excerpt for a task |
| `./bin/demon resolve <INBOX-ID>` | Mark an inbox item as resolved |
