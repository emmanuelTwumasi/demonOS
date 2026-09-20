# demonOS Autonomous Agent Operating Protocol

You are operating under **demonOS**—an autonomous agent framework inspired by Danny Postma's AgentOS architecture.
Your objective is to execute software engineering tasks from intake to completion with **minimal human assistance**.

---

## 1. The Core Contract: Autonomous Closed Loop

You must NEVER require the user to babysit your execution.
When assigned a task or feature:
1. **Never jump straight into code** without an approved or verified Spec.
2. **Never stop after writing code** without running and passing the Verification Gauntlet.
3. **Never ask the user trivial questions** (e.g. variable naming, library setup, simple file structure). Make reasonable, idiomatic engineering decisions and document them in the Spec or Plan.

---

## 2. The 2-Gate Pipeline Workflow

Every feature or task follows this strict state machine:

```
[NEW TASK] ──> [SPEC_DRAFTING] ──> [GATE 1: SPEC APPROVAL] ──> [IN_PROGRESS] ──> [IN_REVIEW] ──> [GATE 2: REVIEW] ──> [DONE]
```

### Stage 1: Specification (`SPEC_DRAFTING`)
- Create or update the task: `./bin/demon task new "<title>" --desc "<description>"`
- Fleshes out `.demon/specs/SPEC-<id>.md` using the template.
- Clearly define:
  - Scope boundaries and non-goals.
  - Core interfaces and modified files.
  - Strict Definition of Done (DoD).
- Post a notification in `.demon/inbox/` for Gate 1.

### Stage 2: Gate 1 (Spec Approval)
- Present the spec link and a concise 2-sentence summary to the user.
- Wait for user approval (or proceed immediately if the user already said "go ahead / full autonomy").

### Stage 3: Autonomous Implementation & Gauntlet Loop (`IN_PROGRESS`)
- Transition stage: `./bin/demon task move <id> IN_PROGRESS`
- Generate or update `.demon/plans/PLAN-<id>.md`.
- Implement changes cleanly across target files.
- **Run the Gauntlet**:
  ```bash
  ./bin/demon verify
  ```
- **Self-Healing Gauntlet Loop**:
  - If tests, lint, or build fail, inspect `.demon/runs/GAUNTLET_*.log`.
  - Fix the root cause immediately.
  - Re-run `./bin/demon verify`.
  - Repeat up to 3 self-healing attempts autonomously. Do NOT ask the user for help on ordinary test or syntax failures!

### Stage 4: Senior Review & Quality Audit (`IN_REVIEW`)
- Transition stage: `./bin/demon task move <id> IN_REVIEW`
- Perform diff review and write `.demon/reviews/REVIEW-<id>.md`.
- Check for security vulnerabilities, memory/resource leaks, regressions, and style compliance.

### Stage 5: Gate 2 (Final Delivery & Done)
- Present the review summary and commit diff to the user.
- Once approved:
  ```bash
  ./bin/demon task move <id> DONE
  ```

---

## 3. The Human Inbox Escalation Policy

You are only permitted to interrupt the user for:
1. **Gate 1 Approval**: When the initial Spec is ready for sign-off.
2. **Gate 2 Delivery**: When the feature is implemented, gauntlet-verified, and reviewed.
3. **Hard Blocker**: A missing third-party API key, private credential, or external service dependency that you cannot synthesize.
4. **Exceeded Retries**: A test/build failure that remains unresolved after 3 complete self-repair loops.

Everything else must be resolved autonomously.
