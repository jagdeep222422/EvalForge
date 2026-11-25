# Innodata AI Hackathon: submission answers (Track 1)

## Team
- **Team name:** EvalForge
- **Team leader:** Jagdeep Kumar Mahto (solo)
- **Track:** Track 1, Coding Task Factory

## Problem statement
Testing AI on software work needs many realistic, verified coding tasks. Writing them by hand is slow, error-prone, and hard to repeat. A task with a wrong answer can mislead the whole evaluation.

## Brief about the idea
EvalForge turns a real open-source codebase into verified coding tasks. Each task has a clear requirement, a reference fix, and tests. A task is kept only if its feature tests fail before the fix, pass after it, and break no existing test. Each task is packaged in Harbor's standard format, so anyone can run it.

## Opportunity

**How is it different from existing ideas?**
Most coding benchmarks are built once by hand and then fixed. EvalForge generates tasks from a real repository, checks each one automatically, and can keep producing new ones. Every task is also checked against the existing test suite, so a task cannot quietly break the base code.

**How does it solve the problem?**
A pipeline proposes a feature, checks it against the base code, and keeps only tasks that pass. Five tasks are already built and verified this way. Each one scores 0.0 with no fix and 1.0 with the reference fix in the official Harbor checks.

**USP (unique selling point)**
- **Verified, not just written:** every task passes the nop and oracle checks.
- **Regression-safe:** a task that breaks any of click's 2,434 existing tests is rejected.
- **Hard to cheat:** grading runs in a separate container, so the expected answers are not visible to the AI being tested. This reduces test-data leakage.
- **Free to run:** Docker, Harbor, Python and click are all free.

## Feature list (what the solution offers today)
1. Automated validation of candidate features: distinctness, fail-before, pass-after and no-regression checks.
2. Automated packaging of accepted candidates as Harbor task folders.
3. Five verified tasks on pallets/click 8.5.1.
4. A grader that writes a reward from feature and regression results.
5. Mutation testing: 10 deliberately broken solutions, all caught by a test.

## Process flow
1. Pick a real repository and a fixed base commit.
2. Propose a feature that does not exist in that version.
3. Write the instructions, a reference fix and tests.
4. Validation pipeline: distinct? → fails before? → passes after? → breaks nothing? Reject any candidate that fails a check.
5. Package the accepted task as a Harbor folder.
6. Run the official checks: nop (expect 0.0) and oracle (expect 1.0).

## Architecture
- **Source:** pallets/click 8.5.1 at a fixed commit.
- **Pipeline (Python):** validates candidates against the base commit and packages accepted ones.
- **Task package (Harbor):** instructions, reference patch, feature and regression lists, grader.
- **Agent container (Docker):** clones click at the base commit and applies the agent's changes.
- **Verifier container (Docker):** runs the tests separately, on the agent's repository state.
- **Output:** a reward file per run, plus logs.

## Technologies
- Python 3.12
- Harbor 0.25.0 (task format and evaluation runner)
- pytest (feature and regression tests)
- Docker and Docker Compose (isolated containers)
- Git and GitHub
- Bash scripts for the oracle and verifier
- pallets/click 8.5.1 (the base project)
- Claude (Anthropic) as a development assistant. The pipeline does not call a model yet.

## Estimated implementation cost
Low. Everything runs on a laptop with free open-source tools. The only possible cost is model API credits, which are not used by the current pipeline.

## What is not built yet (stated honestly)
- A model that writes new features on its own. The five tasks were written by hand, with AI help.
- Track 2 (visual tasks). This submission covers Track 1 only.
- A live dashboard. Results are shown as files and in the deck.

## Requirements checklist
- [x] Runnable source code: https://github.com/jagdeep222422/EvalForge
- [x] Sample task packages: `tasks/`
- [x] Validation test logs: `docs/HARBOR_RESULTS.md`, `docs/MUTATION_RESULTS.md`
- [x] Technical documentation: `docs/TECHNICAL_WRITEUP.md`
- [ ] Live prototype demonstration: record using `docs/DEMO_SCRIPT.md`
