# click-group-alias

Track 1 task. Base: pallets/click tag 8.5.1 (`cf19179e8e2fd54c601378cec9e0d21bb12b6fb1`).

Feature: `Group(aliases={"b": "build"})` lets a short name run a subcommand. Aliases stay out of the help listing.

- `tests/fail_to_pass.json`: 7 new feature tests (fail before, pass after)
- `tests/pass_to_pass.json`: 2436 tests that pass at the base commit
- `solution/solution.patch`: reference implementation
