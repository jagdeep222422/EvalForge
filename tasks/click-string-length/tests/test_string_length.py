import pytest

import click
from click.testing import CliRunner
from click.types import StringLength


def test_accepts_value_within_range():
    assert StringLength(min_length=2, max_length=5).convert("abc", None, None) == "abc"


def test_bounds_are_inclusive():
    t = StringLength(min_length=2, max_length=5)
    assert t.convert("ab", None, None) == "ab"
    assert t.convert("abcde", None, None) == "abcde"


def test_too_short_raises_bad_parameter():
    with pytest.raises(click.BadParameter) as exc:
        StringLength(min_length=3).convert("ab", None, None)
    assert "at least 3 characters" in str(exc.value)


def test_too_long_raises_bad_parameter():
    with pytest.raises(click.BadParameter) as exc:
        StringLength(max_length=4).convert("abcdef", None, None)
    assert "at most 4 characters" in str(exc.value)


def test_no_bounds_accepts_any_length():
    assert StringLength().convert("", None, None) == ""
    assert StringLength().convert("x" * 1000, None, None) == "x" * 1000


def test_min_greater_than_max_is_rejected():
    with pytest.raises(ValueError):
        StringLength(min_length=5, max_length=2)


def test_converts_bytes_like_string_type():
    assert StringLength(max_length=10).convert(b"hello", None, None) == "hello"


def test_cli_option_reports_length_error():
    @click.command()
    @click.option("--name", type=StringLength(max_length=4))
    def cli(name):
        click.echo(name)

    result = CliRunner().invoke(cli, ["--name", "abcdef"])
    assert result.exit_code == 2
    assert "at most 4 characters" in result.output


def test_cli_option_accepts_valid_value():
    @click.command()
    @click.option("--name", type=StringLength(min_length=2, max_length=4))
    def cli(name):
        click.echo(name)

    result = CliRunner().invoke(cli, ["--name", "abc"])
    assert result.exit_code == 0
    assert result.output == "abc\n"
