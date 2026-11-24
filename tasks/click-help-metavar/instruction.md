# Add show_metavar to click's Option

On the help page, click shows an option's value placeholder next to its name, for example `--name TEXT`. Sometimes the placeholder is noise, for instance when the option's value is self-explanatory. Add an option to hide it.

## Requirements

1. `Option.__init__` gets a new keyword argument `show_metavar: bool = True`, placed after `show_envvar`. Store it as `self.show_metavar`.
2. When `show_metavar` is `True` (the default), the help spec is unchanged, for example `-n, --name TEXT`.
3. When `show_metavar` is `False`, `Option.get_help_spec(ctx)` omits the placeholder for every spelling, for example `-n, --name`. The rest of the help record, including the description, is unchanged.
4. Flags never show a placeholder, so `show_metavar=False` changes nothing for a flag.
5. Document the parameter in the `Option` docstring.

No existing behaviour may change.
