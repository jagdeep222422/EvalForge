# EvalForge: technical write-up (Innodata AI Hackathon, Track 1)

Author: Jagdeep Kumar Mahto (solo)
Repository: https://github.com/jagdeep222422/EvalForge

## 1. Problem

Track 1 asks for a system that turns a real codebase into realistic software-development tasks. Each task
needs a requirement, a working reference solution, and tests that separate correct from incorrect work.
Each task must be packaged in Harbor's standard format and pass two checks:

- **nop** (no change by the agent): reward 0.0, because the feature tests fail before the change.
- **oracle** (reference solution applied): reward 1.0, because all feature and regression tests pass.

## 2. Base repository and assumptions

- Base: `pallets/click`, tag `8.5.1`, commit `cf19179e8e2fd54c601378cec9e0d21bb12b6fb1`.
- Chosen because it is pure Python with a fast test suite (2,434 regression tests run in about 5 seconds), so
  per-task Docker builds stay light.
- Assumption: a feature counts only if it does not already exist upstream. I checked each candidate against
  the 8.5.1 source before writing it.

## 3. Architecture

```
tasks/<name>/            one Harbor task per feature
  instruction.md         requirement text shown to the tested AI
  task.toml              metadata, base commit, verifier mode, artifacts
  environment/Dockerfile clones click at the base commit
  solution/solve.sh      oracle: applies solution.patch in /app
  solution/solution.patch reference implementation
  tests/                 feature tests, regression list, grader, verifier Dockerfile
tools/pipeline/          validation and packaging of candidate features
docs/                    plan, mutation results, Harbor results
```

**Grading.** `tests/grade.py` runs the feature tests and the regression list and writes a reward:
any regression failure gives 0.0; all feature tests passing gives 1.0; otherwise the share of feature
tests that pass.

**Verifier isolation.** The verifier runs in a separate container, so the expected answers are not in the
AI's sandbox. Harbor's `artifacts` setting copies `/app` (the agent's modified repository, excluding `.git`)
into the verifier at the same path. The verifier installs click in editable mode, so grading sees the
agent's code.

**Pipeline (validation and packaging).** `tools/pipeline/pipeline.py` takes candidate features and:
1. rejects candidates too similar to accepted tasks (identifier overlap of 60% or more);
2. confirms the feature tests fail on the base commit;
3. confirms the patch applies and the feature tests pass with it;
4. confirms the patch breaks no regression test (checked against the 2,434-test baseline);
5. writes accepted candidates as Harbor task folders.

## 4. The five tasks

| Task | Feature | Feature tests | Regression tests |
|---|---|---|---|
| click-string-length | `StringLength(min_length, max_length)` parameter type | 9 | 2,434 |
| click-choice-prefix | `Choice(..., allow_prefix=True)` unique-prefix matching | 8 | 2,435 |
| click-path-suffix | `Path(..., allowed_suffixes=[...])` extension check | 10 | 2,435 |
| click-group-alias | `Group(aliases={...})` alternative command names | 7 | 2,436 |
| click-help-metavar | `Option(..., show_metavar=False)` hides the value placeholder in help | 6 | 2,436 |

**Variation.** The five tasks cover five different parts of click: parameter types (two tasks),
path validation, command groups, and help output. Each changes behaviour rather than wording, and none
overlaps another (the pipeline's distinctness check enforces this).

## 5. Verification evidence

- **Official Harbor 0.25.0 runs** (Ubuntu 24.04, Docker): nop 0.0 and oracle 1.0 for all five tasks.
  Results are in `docs/HARBOR_RESULTS.md`.
- **Mutation testing.** I broke each reference change in 10 deliberate ways (off-by-one bounds, skipped
  checks, wrong lookup, and similar). All 10 were caught by at least one feature test. Two weak spots were
  fixed: a missing test for a second suffix, and a mutant that changed nothing. See `docs/MUTATION_RESULTS.md`.
- **Pipeline self-test.** Replaying the five accepted tasks gives 5 of 5 accepted. Four deliberately bad
  candidates were each rejected for the expected reason: already-passing tests, a patch that breaks 8
  existing tests, a patch that does not apply, and a near-duplicate.

## 6. Bugs found and fixed during validation

These are the errors that mattered, since each one could have produced a wrong result:

- **Silent task rejection.** Harbor ignored tasks with unknown `task.toml` fields and reported "no tasks".
  `harbor lint` showed the real reason.
- **Missing oracle script.** Harbor runs `solution/solve.sh`, not a bare patch.
- **Wrong grading source.** A separate verifier does not get the agent's changes by default, so the oracle
  scored 0. Fixed with the `artifacts` setting.
- **Missing system tools.** The pager tests need `less`, which the base Ubuntu image lacks.
- **Truncated test IDs.** 482 regression IDs were cut short by a naive parser, which made the validator
  reject good tasks. Fixed by matching against exact collected IDs.

## 7. Tools and models used (declaration)

- **Claude (Anthropic)** was used as a coding assistant throughout: reading the click source, drafting the
  features, tests and reference patches, writing the validator and grader, and debugging Harbor runs. The
  model in this session was Claude Haiku 5.5. The human author reviewed each step and ran the Harbor checks
  on their own machine.
- **Harbor 0.25.0** (task format, `harbor run`, `harbor lint`).
- **pallets/click 8.5.1** (base repository, BSD-3-Clause), pytest, Docker, Git, Python 3.12/3.13.

No model is used to generate tasks at run time yet (see section 8).

## 8. Limitations and next steps

- **The model-based generator is not built.** The five tasks were written by hand, with AI assistance. The
  pipeline validates and packages candidates, but it does not yet write new features with a model. This
  needs an API key and a live test.
- **Scale.** The spec's minimum is five distinct tasks, which is met. Scale testing has not been done.
- **Mutation script** (`tools/mutation_check.py`) still contains paths from the author's sandbox and
  needs cleanup before others can run it.
- **Demo.** The walkthrough video has not been recorded yet.
