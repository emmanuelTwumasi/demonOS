# Feature Spec: TASK-002 - Portfolio Enhancements, Real GitHub Integration & GitHub Pages CI/CD

- **Created**: 2026-09-20 23:15:33 UTC
- **Status**: APPROVED (Autonomous Execution Mandate Granted)
- **Owner**: Emmanuel Twumasi / Antigravity

---

## 1. Executive Summary
Elevate Emmanuel Twumasi's portfolio website to elite 2026 developer standards by integrating his verified GitHub avatar (`avatars.githubusercontent.com/u/58420781`) and real repositories (`banking_application`, `protwum`, `Android1`, `demonOS`), implementing Schema.org `Person` JSON-LD structured data for search and AI Answer Engine Optimization (AEO), generating `robots.txt` and `sitemap.xml`, adding printable CV/Resume styling (`@media print`), introducing an interactive project detail modal, and configuring an automated GitHub Pages GitHub Actions deployment pipeline (`.github/workflows/deploy-pages.yml`).

---

## 2. User Stories & Core Requirements

### User Stories
- **US-1**: As a recruiter or hiring manager, I want to see Emmanuel's authentic GitHub avatar and real public repositories directly linked on the portfolio.
- **US-2**: As an AI answer engine (Perplexity, ChatGPT, Gemini) or Google Search, I want structured JSON-LD `Person` metadata to index Emmanuel as a specialized full-stack & autonomous systems software engineer.
- **US-3**: As a technical recruiter, I want to print or save the portfolio as a clean PDF resume using standard browser print (`Cmd+P`).
- **US-4**: As Emmanuel, I want automated CI/CD so every push to `master` automatically publishes to GitHub Pages via GitHub Actions with zero manual build steps.

### Functional Requirements
1. **Real GitHub Integration**:
   - Hero Section: Display Emmanuel's GitHub avatar badge (`https://avatars.githubusercontent.com/u/58420781?v=4`) alongside profile card.
   - Showcase Projects: Connect actual repositories:
     - `emmanuelTwumasi/banking_application` (Secure Banking System)
     - `emmanuelTwumasi/protwum` (Developer Utilities)
     - `emmanuelTwumasi/demonOS` (Autonomous Agent Framework)
     - `emmanuelTwumasi/Android1` (Mobile Engineering)
2. **SEO, AEO & Structured Data**:
   - Add Schema.org `Person` & `ProfilePage` in `<script type="application/ld+json">`.
   - Create `portfolio/robots.txt` allowing search crawlers and pointing to `sitemap.xml`.
   - Create `portfolio/sitemap.xml` with canonical URLs.
3. **Printable CV Stylesheet**:
   - Add `@media print` rules in `portfolio/styles.css` that hide navigation, theme buttons, and decorative elements to render a crisp, clean, black-and-white 1-to-2 page PDF resume when printing.
4. **Interactive Project Modal**:
   - Add an interactive modal view for project cards to inspect Architecture, Technical Challenges, and Technologies used.
5. **GitHub Pages CI/CD Workflow**:
   - Create `.github/workflows/deploy-pages.yml` with permissions `pages: write` and `id-token: write`.
   - Create `bin/deploy` helper script to guide remote connection and pushing.

---

## 3. Technical Architecture & Files Affected
- **Files Modified/Created**:
  - `portfolio/index.html` (Avatar, real projects, JSON-LD schema, modal container)
  - `portfolio/styles.css` (Modal styles, print stylesheet, avatar badge styling)
  - `portfolio/app.js` (Project modal open/close handling, keyboard accessibility)
  - `portfolio/robots.txt` (SEO indexation instructions)
  - `portfolio/sitemap.xml` (Search engine sitemap)
  - `.github/workflows/deploy-pages.yml` (GitHub Pages Actions CI/CD)
  - `bin/deploy` (Executable deployment runner script)
  - `tests/test_portfolio_v2.py` (Test coverage for SEO schema, sitemap, robots, and modal)

---

## 4. Definition of Done (DoD) & Verification Gauntlet
All of the following MUST be true before this feature can be marked `DONE`:
- [ ] Real GitHub avatar and repositories connected accurately.
- [ ] Schema.org JSON-LD `Person` block validates with valid JSON.
- [ ] `robots.txt` and `sitemap.xml` exist and are accessible.
- [ ] `@media print` rules hide interactive buttons and optimize typography.
- [ ] Project modal opens on click, traps focus, and closes on Escape / backdrop click.
- [ ] Automated verification gauntlet passes (`./bin/demon verify`).
- [ ] Senior code review documented in `.demon/reviews/REVIEW-TASK-002.md`.
