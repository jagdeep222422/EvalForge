# click-string-length

Track 1 task. Base: pallets/click tag 8.5.1 (`cf19179e8e2fd54c601378cec9e0d21bb12b6fb1`).

Feature: add `StringLength(min_length, max_length)` parameter type.

- `tests/fail_to_pass.json`: 9 new feature tests (fail before, pass after)
- `tests/pass_to_pass.json`: 2434 existing tests that pass at the base commit
- `solution/solution.patch`: reference implementation
