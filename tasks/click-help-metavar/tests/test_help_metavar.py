import click
from click.testing import CliRunner


def make_cli(**option_kwargs):
    @click.command()
    @click.option("--name", **option_kwargs)
    def cli(name):
        """Greet someone."""

    return cli


def test_default_help_shows_metavar():
    result = CliRunner().invoke(make_cli(), ["--help"])
    assert "--name TEXT" in result.output


def test_show_metavar_false_hides_placeholder():
    result = CliRunner().invoke(make_cli(show_metavar=False), ["--help"])
    line = next(l for l in result.output.splitlines() if "--name" in l)
    assert "TEXT" not in line
    assert "--name" in line


def test_show_metavar_false_keeps_description():
    result = CliRunner().invoke(make_cli(show_metavar=False, help="Who to greet."), ["--help"])
    assert "Who to greet." in result.output


def test_show_metavar_default_is_true():
    opt = click.Option(["--name"])
    assert opt.show_metavar is True


def test_show_metavar_is_stored_on_option():
    opt = click.Option(["--name"], show_metavar=False)
    assert opt.show_metavar is False


def test_get_help_spec_without_metavar():
    ctx = click.Context(make_cli())
    opt = click.Option(["-n", "--name"], show_metavar=False)
    assert opt.get_help_spec(ctx) == "-n, --name"


def test_get_help_spec_with_metavar_is_unchanged():
    ctx = click.Context(make_cli())
    opt = click.Option(["-n", "--name"])
    assert opt.get_help_spec(ctx) == "-n, --name TEXT"


def test_flag_help_is_unaffected_by_show_metavar():
    ctx = click.Context(make_cli())
    opt = click.Option(["--verbose"], is_flag=True, show_metavar=False)
    assert opt.get_help_spec(ctx) == "--verbose"
