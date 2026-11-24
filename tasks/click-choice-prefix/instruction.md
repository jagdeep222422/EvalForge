# Add unique-prefix matching to click's Choice type

`click.Choice` only accepts a value that exactly matches one of its choices (optionally ignoring case). Add an opt-in option that lets users type a short unique prefix instead.

## Requirements

1. `Choice.__init__` gets a new keyword argument: `allow_prefix: bool = False`. Store it as `self.allow_prefix`.
2. When `allow_prefix` is `False` (the default), behaviour is unchanged.
3. When `allow_prefix` is `True`, converting a value works like this:
   - If the value exactly matches a normalized choice (respecting `case_sensitive` and `normalize_choice`), return that choice. An exact match always wins.
   - Otherwise, if the value is non-empty and is a prefix of exactly one normalized choice, return that original choice. Enum choices return the enum member.
   - If the value is a prefix of more than one choice, fail with a `click.BadParameter` whose message contains `is ambiguous`.
   - If the value is empty, or matches no choice by prefix, fail with the existing invalid-choice error.
4. Prefix matching respects `case_sensitive` in the same way exact matching does.
5. Used as a command option, an ambiguous or invalid value produces exit code 2 with the error shown.
6. Document the new parameter in the `Choice` docstring.

No existing behaviour may change.
