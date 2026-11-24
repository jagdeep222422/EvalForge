# Add command aliases to click's Group

A `click.Group` can register subcommands, but it cannot offer a short alternative name for one. Add an `aliases` option so that a group can map alternative names to existing subcommands.

## Requirements

1. `Group.__init__` gets a new keyword argument `aliases: Mapping[str, str] | None = None`. It maps an alias to the name of a registered subcommand. Store it as `self.aliases` (a `dict`, empty when not given).
2. `Group.get_command(ctx, name)` returns the subcommand registered under `name`, as before.
3. If `name` is not a registered subcommand but is a key in `self.aliases`, return the subcommand named by that alias's value.
4. A registered command name always takes precedence over an alias with the same name.
5. If an alias points to a command that is not registered, `get_command` returns `None`, the same as an unknown name.
6. Aliases are not shown in `list_commands`, so they do not appear in the help output.
7. Invoking an alias from the command line runs the target command. An unknown name still gives exit code 2 with "No such command".

No existing behaviour may change. Document the parameter in the `Group` docstring.
