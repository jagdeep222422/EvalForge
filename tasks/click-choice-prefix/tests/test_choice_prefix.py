import pytest

import click
from click.testing import CliRunner
from click.types import Choice


def test_unique_prefix_resolves_to_choice():
    assert Choice(["apple", "banana"], allow_prefix=True).convert("ba", None, None) == "banana"


def test_exact_match_wins_over_prefix():
    assert Choice(["go", "gopher"], allow_prefix=True).convert("go", None, None) == "go"


def test_ambiguous_prefix_fails():
    with pytest.raises(click.BadParameter) as exc:
        Choice(["apple", "apricot"], allow_prefix=True).convert("ap", None, None)
    assert "ambiguous" in str(exc.value)


def test_prefix_disabled_by_default_fails():
    with pytest.raises(click.BadParameter):
        Choice(["apple", "banana"]).convert("ba", None, None)


def test_empty_value_never_matches_by_prefix():
    with pytest.raises(click.BadParameter):
        Choice(["apple"], allow_prefix=True).convert("", None, None)


def test_prefix_respects_case_sensitivity():
    with pytest.raises(click.BadParameter):
        Choice(["Apple"], allow_prefix=True).convert("app", None, None)
    assert Choice(["Apple"], case_sensitive=False, allow_prefix=True).convert("APP", None, None) == "Apple"


def test_prefix_returns_original_enum_choice():
    import enum

    class Color(enum.Enum):
        RED = 1
        GREEN = 2

    assert Choice(list(Color), allow_prefix=True).convert("GR", None, None) is Color.GREEN


def test_cli_accepts_unique_prefix():
    @click.command()
    @click.option("--fruit", type=Choice(["apple", "banana"], allow_prefix=True))
    def cli(fruit):
        click.echo(fruit)

    result = CliRunner().invoke(cli, ["--fruit", "ban"])
    assert result.exit_code == 0
    assert result.output == "banana\n"


def test_cli_rejects_ambiguous_prefix_with_exit_2():
    @click.command()
    @click.option("--fruit", type=Choice(["apple", "apricot"], allow_prefix=True))
    def cli(fruit):
        click.echo(fruit)

    result = CliRunner().invoke(cli, ["--fruit", "ap"])
    assert result.exit_code == 2
    assert "ambiguous" in result.output
