# Add a length-limited string parameter type to click

click's built-in `STRING` type accepts any text. Add a new parameter type so that command-line values can be restricted by length.

## Requirements

1. Add a class `StringLength` in `click.types`. It is a subclass of `StringParamType`.
2. Its constructor is `StringLength(min_length=None, max_length=None)`.
   - Both bounds are optional and inclusive. `None` means no limit on that side.
   - If both are given and `min_length` is greater than `max_length`, raise `ValueError`.
3. Converting a value:
   - Convert the value exactly as `STRING` does, including bytes input.
   - If the result is shorter than `min_length`, fail with a `click.BadParameter` whose message contains `at least N characters`, where N is `min_length`.
   - If the result is longer than `max_length`, fail with a `click.BadParameter` whose message contains `at most N characters`, where N is `max_length`.
   - Otherwise return the converted string.
4. Export `StringLength` from the top-level `click` package, so `click.StringLength` works.
5. When used as an option type, a failing value must produce exit code 2 and show the error message, like other click type errors.

No existing behaviour may change.
