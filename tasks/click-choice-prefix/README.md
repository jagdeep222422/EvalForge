# click-choice-prefix

Track 1 task. Base: pallets/click tag 8.5.1 (`cf19179e8e2fd54c601378cec9e0d21bb12b6fb1`).

Feature: `Choice(..., allow_prefix=True)` accepts a unique prefix of one choice.

- `tests/fail_to_pass.json`: 8 new feature tests (fail before, pass after)
- `tests/pass_to_pass.json`: 2435 tests that pass at the base commit
- `solution/solution.patch`: reference implementation
