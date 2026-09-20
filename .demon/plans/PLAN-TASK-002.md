# Implementation Plan: TASK-002 - Portfolio Enhancements, Real GitHub Integration & GitHub Pages CI/CD

- **Spec Reference**: `specs/SPEC-TASK-002.md`
- **Created**: 2026-09-20 23:15:41 UTC
- **Status**: IN_PROGRESS

---

## 1. Plan Overview
Step-by-step implementation of advanced enhancements:
1. Real GitHub integration (Avatar & genuine repositories).
2. Schema.org JSON-LD Person schema & search files (`robots.txt`, `sitemap.xml`).
3. Printable CV stylesheet (`@media print`) and Resume download trigger.
4. Interactive Project Detail Modal.
5. GitHub Pages deployment configuration (`.github/workflows/deploy-pages.yml` & `bin/deploy`).
6. Automated verification gauntlet.

---

## 2. Atomic Work Items

### Step 1: SEO, Robots & Sitemap
- **Target Files**: `portfolio/robots.txt`, `portfolio/sitemap.xml`
- **Action**: Create
- **Details**: Crawl instructions, canonical domain, sitemap locator.

### Step 2: GitHub Pages CI/CD Workflow
- **Target Files**: `.github/workflows/deploy-pages.yml`, `bin/deploy`
- **Action**: Create
- **Details**: Standard GitHub Actions pages artifact upload and deployment runner.

### Step 3: Real GitHub Avatar, Projects & JSON-LD
- **Target File**: `portfolio/index.html`
- **Action**: Modify
- **Details**:
  - Insert JSON-LD `<script type="application/ld+json">`.
  - Add GitHub avatar image in hero section.
  - Update project cards with real GitHub repos (`banking_application`, `protwum`, `Android1`, `demonOS`).
  - Add project modal container markup.
  - Add Resume download/print button in nav and hero.

### Step 4: Styling for Modal, Avatar & Print CV
- **Target File**: `portfolio/styles.css`
- **Action**: Modify
- **Details**: Add `.hero-avatar` styling, `.modal` overlay and card styling, and `@media print` rules.

### Step 5: Modal Interactivity & Keyboard Access
- **Target File**: `portfolio/app.js`
- **Action**: Modify
- **Details**: Project details dataset, modal open/close on project click, focus trapping, escape key listener.

### Step 6: Verification Gauntlet
- **Target File**: `tests/test_portfolio_v2.py`
- **Action**: Create
- **Details**: Validate JSON-LD valid JSON structure, robots/sitemap existence, modal markup presence, and CI/CD workflow syntax.
- **Verification Command**: `./bin/demon verify`
