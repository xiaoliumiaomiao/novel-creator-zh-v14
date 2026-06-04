# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Identity

中文网文工业化创作工具集 (Chinese Web Novel Industrial Creation Toolset). A Python CLI toolset integrated with Claude Code multi-agent orchestration and an Obsidian vault knowledge hub, targeting 番茄/七猫 platform style for both male (男频) and female (女频) genres.

## Build, Test, Lint

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
python -m pytest

# Run a single test file
python -m pytest tests/test_linting.py

# Lint
ruff check .

# Build package
python -m build

# CLI smoke test
python -m novel_creator.cli --help
```

## Architecture

```
novelctl (CLI) → novel_creator/ (Python package)
                 ├── orchestration.py  # Multi-agent dispatch and Director logic
                 ├── cli.py            # Typer/Rich CLI entry
                 ├── vault.py          # Obsidian vault operations, init, templates
                 ├── corpus.py         # Reference import, pattern extraction, IMA
                 ├── scoring.py        # Chapter scoring (commercial, continuity, deai, risk)
                 ├── dashboard.py      # Markdown + HTML dashboard generation
                 ├── linting.py        # Hard rules checker (YAML, links, word count, style blacklist)
                 ├── deai.py           # Anti-AI voice: expression-only, detail-light, dramatic-boost
                 ├── risk.py           # Legal/political/platform risk review
                 ├── git_sync.py       # Git branch protection, auto commit+push
                 └── config.py         # Shared config

.claude/
├── agents/   # Per-agent definitions (male/female/shared agents with duties, I/O, checklists)
├── skills/   # Slash-command skill definitions with multi-agent call sequences
└── commands/ # Degraded fallback entry points if skills aren't supported

vault/        # Obsidian vault = novel project knowledge hub (not committed except Samples)
├── 00_Dashboard/Agent_Traces/  # Per-chapter detailed agent trace
├── 01_Projects/                # Per-book master docs
├── 02_Characters/              # Character cards
├── 03_Worldbuilding/           # World rules, power systems, factions
├── 04_Plot/                    # Main plot, volume outlines, chapter outlines
├── 05_Chapters/                # Chapter drafts with YAML frontmatter properties
├── 06_Foreshadowing/           # Foreshadowing ledger (new/recovered/pending)
├── 07_Timeline/                # Story timeline
├── References/                 # IMA imports — NEVER committed to git
├── Templates/                  # File templates
└── Samples/                    # Mini male/female sample novels
```

## Mandatory Rules (Non-Negotiable)

### Multi-Agent Requirement
- **Every chapter MUST go through multiple agents.** A single agent must never draft a complete chapter from outline to final.
- Minimum chain per chapter: Director → Chapter Planner → Character Agent → Drafter → Commercial Reviewer → Continuity Auditor → Anti-AI Voice Editor → Polisher → Obsidian Librarian → Director Final Decision.
- Every chapter run must generate a detailed Agent Trace in `vault/00_Dashboard/Agent_Traces/`.

### Hard Writing Rules (enforced by `novelctl lint` and `novelctl publish-check`)
- Effective word count: 2500–4000 per chapter (Chinese chars + digits only, excluding whitespace/punctuation).
- English character ratio ≤ 1%.
- No completely empty lines in chapter body.
- Single paragraph max 180 effective Chinese chars.
- Chapter title format: `第N章 标题`, filename: `第N章 标题.md`.
- Chinese quotation marks `""` only; speaker on separate line.
- Chinese punctuation only (no ASCII punctuation in body text).
- First 3 chapters: no filler, fast conflict entry, show genre hook, no exposition dumps.
- Style blacklist enforced: banned patterns like `A——不是B`, overly explanatory tone, mechanical summaries, template "golden sentences", empty emotional word stacking.

### Chapter State Machine
```
planned → drafted → reviewed → deai → polished → approved
rejected → revision-planned → revised → reviewed
```
Chapters must not enter `approved` without user confirmation.

### Risk Review (mandatory in lint, publish-check, Commercial Reviewer, Director)
- Legal, political, 涉黄, gambling, drugs, violence/terror, inciting crime, infringement, defamation, privacy, extreme gore, cyber violence instigation.
- Auto-mitigate once on trigger; if still risky after re-check, block approval.

### Anti-AI Voice
- Three modes: `expression-only`, `detail-light`, `dramatic-boost`.
- Always output three drafts: `original`, `natural`, `web-serial`.
- Must preserve commercial pacing; must not add major plot facts (`dramatic-boost` must annotate any new micro-content).

### Director Decision Priority
```
Commercial rhythm > Legal/political risk > Setting consistency > Character motivation > Anti-AI voice > Stylistic polish
```

### Quality Gate
- Chapter score threshold: **85/100**.
- Auto-fix max **2 rounds**; if still failing, stop and report.

### Reference Library (vault/References/)
- **NEVER commit** reference originals to Git.
- Only learn structural patterns (openings, conflict density, hook types, emotional curves, pacing).
- Never copy reusable source text into prompts, templates, or generated materials.

### Git
- Always use feature branches; **never push directly to main/master**.
- Commit only after phase acceptance; use Chinese commit messages.
- If no `origin` remote, stop push and prompt user to configure GitHub remote.

## Scoring System

Chapters are scored on: commercial rhythm, continuity, character motivation, anti-AI voice, risk status, word count and formatting. All scores feed into `vault/00_Dashboard/` and `reports/` (HTML).

## CLI Entry Points

```
novelctl init-vault        # Create vault dirs, templates, dashboard, samples
novelctl import-ima        # Scan References/, deduplicate, generate structure cards
novelctl index             # Build SQLite index in data/index/
novelctl extract-patterns  # Extract story structure patterns from corpus
novelctl score-chapter     # Score a chapter file
novelctl deai              # Apply anti-AI voice processing (3-mode)
novelctl lint              # Full hard-rules check
novelctl dashboard         # Generate Markdown + HTML dashboard
novelctl publish-check     # Pre-publish gate (all checks)
novelctl git-sync          # Safe branch-push with pre-flight tests
```
