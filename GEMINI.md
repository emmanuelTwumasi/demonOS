# demonOS Agent Guidelines for Gemini / Antigravity

This repository is governed by the **demonOS Autonomous Protocol** specified in [`AGENTS.md`](file:///Users/EmmanuelTwumasi/Documents/demonOS/AGENTS.md).

### Autonomous Directives:
1. **Task Flow**: When asked to build or fix anything, check `.demon/board.json` or run `./bin/demon task list`.
2. **Spec & Plan First**: Draft a spec in `.demon/specs/SPEC-<id>.md` and define the Definition of Done.
3. **Continuous Gauntlet**: Always execute `./bin/demon verify` after code changes. Never report a task as completed if the Gauntlet fails.
4. **Self-Healing Loop**: If a test or lint fails, debug and fix it automatically without bothering the user.
5. **Zero-Friction Commits**: Commit changes with structured semantic commit messages once the Gauntlet passes and the review is complete.
