# EvalForge pipeline (validation and packaging)

Status: the **validation and packaging** half is built and tested. The **model step that writes new
candidate features** is not built yet. It needs an API key and a live test before it can be relied on.

## What it does

`pipeline.py` takes candidate features and, for each one:

1. Checks it is distinct from accepted tasks (identifier overlap below 60%).
2. Confirms the feature tests **fail** on the base commit (nop check).
3. Confirms the patch **applies** and that the feature tests **pass** with it (oracle check).
4. Confirms the patch **breaks no existing test** (the 2,434-test regression baseline).
5. Writes accepted candidates as Harbor task folders.

## Testing done

- Replayed the five hand-written tasks: **5 of 5 accepted**.
- Four deliberately bad candidates, each rejected for the expected reason:
  - feature tests already passing on base
  - patch that breaks 8 existing tests
  - patch that does not apply
  - near-duplicate of an accepted task

## Bugs found and fixed while testing

- Test IDs were parsed by splitting on `" - "`. 482 of the 2,434 regression IDs contain that
  separator and were cut short, which made the combined run abort. IDs are now matched against the
  exact IDs from `pytest --collect-only`.

## Usage

    python pipeline.py --repo <clone of pallets/click> --python <venv python> \
        --candidates <dir of candidate dirs> --out <tasks dir> --report report.json

Each candidate directory needs `candidate.json`, `instruction.md`, `solution.patch` and `tests/`.
