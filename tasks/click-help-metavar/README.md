# click-help-metavar

Track 1 task. Base: pallets/click tag 8.5.1 (`cf19179e8e2fd54c601378cec9e0d21bb12b6fb1`).

Feature: `Option(..., show_metavar=False)` hides the value placeholder (such as `TEXT`) in the help spec.

- `tests/fail_to_pass.json`: 6 new feature tests (fail before, pass after)
- `tests/pass_to_pass.json`: 2436 tests that pass at the base commit
- `solution/solution.patch`: reference implementation
