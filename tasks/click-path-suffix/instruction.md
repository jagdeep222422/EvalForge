# Add allowed_suffixes to click's Path type

`click.Path` checks that a path exists, is a file or directory, and is readable or writable. It cannot restrict the file extension. Add an optional `allowed_suffixes` argument so that a command can accept only certain file types.

## Requirements

1. `Path.__init__` gets a new keyword argument `allowed_suffixes: Sequence[str] | None = None`, added as the **last** parameter so existing calls keep working. Store it as `self.allowed_suffixes`, converted to a tuple, or `None`.
2. When `allowed_suffixes` is `None` (the default), behaviour is unchanged.
3. When it is set, `convert` must check the path string **before** any file system lookup. If the path (as given, before any resolution) does not end with one of the suffixes, fail with a `click.BadParameter` whose message contains `must end with one of:` followed by the suffixes joined with `, `.
4. The check is case-sensitive. `.csv` does not match `DATA.CSV`.
5. The check applies even when the file does not exist and `exists=False`.
6. The dash value `-` (when `allow_dash=True`) is exempt from the suffix check.
7. Used as a command option, a wrong suffix produces exit code 2 with the error shown.
8. Document the new parameter in the `Path` docstring.

No existing behaviour may change.
