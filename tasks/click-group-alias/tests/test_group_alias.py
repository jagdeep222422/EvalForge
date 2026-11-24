import click
from click.testing import CliRunner


def make_cli(**kwargs):
    @click.group(**kwargs)
    def cli():
        pass

    @cli.command()
    def build():
        click.echo("building")

    @cli.command()
    def test():
        click.echo("testing")

    return cli


def test_alias_runs_target_command():
    cli = make_cli(aliases={"b": "build"})
    result = CliRunner().invoke(cli, ["b"])
    assert result.exit_code == 0
    assert result.output == "building\n"


def test_alias_resolves_via_get_command():
    cli = make_cli(aliases={"t": "test"})
    ctx = click.Context(cli)
    assert cli.get_command(ctx, "t") is cli.commands["test"]


def test_real_command_takes_precedence_over_alias():
    cli = make_cli(aliases={"build": "test"})
    result = CliRunner().invoke(cli, ["build"])
    assert result.output == "building\n"


def test_alias_to_missing_command_is_unknown():
    cli = make_cli(aliases={"x": "deploy"})
    ctx = click.Context(cli)
    assert cli.get_command(ctx, "x") is None
    result = CliRunner().invoke(cli, ["x"])
    assert result.exit_code == 2


def test_unknown_name_still_fails_with_exit_2():
    cli = make_cli(aliases={"b": "build"})
    result = CliRunner().invoke(cli, ["nope"])
    assert result.exit_code == 2
    assert "No such command" in result.output


def test_aliases_are_hidden_from_command_listing():
    cli = make_cli(aliases={"b": "build"})
    ctx = click.Context(cli)
    assert cli.list_commands(ctx) == ["build", "test"]


def test_aliases_are_stored_as_a_dict():
    cli = make_cli(aliases={"b": "build"})
    assert cli.aliases == {"b": "build"}


def test_group_without_aliases_still_runs_commands():
    cli = make_cli()
    result = CliRunner().invoke(cli, ["build"])
    assert result.exit_code == 0
    assert result.output == "building\n"


def test_unknown_command_without_aliases_fails_with_exit_2():
    cli = make_cli()
    result = CliRunner().invoke(cli, ["nope"])
    assert result.exit_code == 2
    assert "No such command" in result.output
