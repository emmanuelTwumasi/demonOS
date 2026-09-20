# Quality & Security Review: [TASK_ID] - [TASK_TITLE]

- **Reviewed At**: [TIMESTAMP]
- **Reviewer**: Autonomous Senior Reviewer Agent
- **Verdict**: PASS | REVISE | BLOCK

---

## 1. Diff & Architecture Audit
- **Files Modified**:
  - `path/to/file`
- **Architecture Compliance**: Does the code adhere to the approved Spec? [YES/NO]
- **Complexity Assessment**: Any unnecessary over-engineering or dead code?

---

## 2. Security & Hygiene Checklist
- [ ] No hardcoded secrets, tokens, or credentials.
- [ ] Input validation and boundary sanitization present.
- [ ] Error handling does not leak stack traces or internal secrets to user interfaces.
- [ ] Resource cleanup handled (files closed, connections freed).

---

## 3. Gauntlet Status
- **Test Suite**: PASS / FAIL (Coverage: [X]%)
- **Lint / Style**: PASS / FAIL
- **Build / Runtime**: PASS / FAIL

---

## 4. Final Recommendation
- Summary of review and readiness to merge / commit.
