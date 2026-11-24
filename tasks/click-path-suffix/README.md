# click-path-suffix

Track 1 task. Base: pallets/click tag 8.5.1 (`cf19179e8e2fd54c601378cec9e0d21bb12b6fb1`).

Feature: `Path(..., allowed_suffixes=[...])` restricts the file extension.

- `tests/fail_to_pass.json`: 9 new feature tests (fail before, pass after)
- `tests/pass_to_pass.json`: 2436 tests that pass at the base commit
- `solution/solution.patch`: reference implementation
