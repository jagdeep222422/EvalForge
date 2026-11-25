# EvalForge: prototype brief

**What it is:** A system that creates realistic coding tasks from a real codebase, and checks that each task is correct, so AI coding tools can be tested fairly.

**Why it matters:** Testing AI on coding work needs many tasks that are realistic, clearly written, and verified. Writing them by hand is slow and error-prone.

**How it works:**
1. Take a real open-source project: pallets/click, version 8.5.1.
2. Define a new feature that does not exist in that version.
3. Write the instructions, a reference solution and tests.
4. Check it: the tests must fail without the change and pass with it, and no existing tests may break.
5. Package it as a Harbor task that anyone can run.

**What is built:**
- 5 verified tasks, each adding a different click feature.
- Every task passes the official Harbor checks: 0.0 with no change, 1.0 with the solution.
- Mutation tests: deliberately broken solutions are all caught.
- A validation pipeline that accepts good candidates and rejects bad ones (5 of 5 good accepted, 4 of 4 bad rejected).

**What is not built yet:**
- A model that proposes new features on its own. The five tasks were written by hand, with AI help.

**Why it should be selected:**
- Works end to end and is verified, not just described.
- Clear, honest evidence: results, test counts and known limits are all written down.
- Free to run: Docker, Harbor, Python and click are all free.

**Links:**
- Repository: https://github.com/jagdeep222422/EvalForge
- Results: docs/HARBOR_RESULTS.md
- Full write-up: docs/TECHNICAL_WRITEUP.md
