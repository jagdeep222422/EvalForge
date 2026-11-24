import pytest

import click
from click.testing import CliRunner
from click.types import Path


def test_allowed_suffix_is_accepted(tmp_path):
    f = tmp_path / "data.csv"
    f.write_text("a")
    assert Path(allowed_suffixes=[".csv", ".json"]).convert(str(f), None, None) == str(f)


def test_other_suffix_is_rejected(tmp_path):
    with pytest.raises(click.BadParameter) as exc:
        Path(allowed_suffixes=[".csv"]).convert(str(tmp_path / "notes.txt"), None, None)
    assert "must end with one of: .csv" in str(exc.value)


def test_suffix_checked_even_when_file_missing(tmp_path):
    with pytest.raises(click.BadParameter):
        Path(allowed_suffixes=[".csv"]).convert(str(tmp_path / "missing.txt"), None, None)


def test_missing_file_with_allowed_suffix_is_accepted(tmp_path):
    name = str(tmp_path / "later.csv")
    assert Path(allowed_suffixes=[".csv"]).convert(name, None, None) == name


def test_matching_is_case_sensitive(tmp_path):
    with pytest.raises(click.BadParameter):
        Path(allowed_suffixes=[".csv"]).convert(str(tmp_path / "DATA.CSV"), None, None)


def test_no_suffixes_means_no_restriction(tmp_path):
    name = str(tmp_path / "anything.xyz")
    assert Path().convert(name, None, None) == name


def test_dash_is_exempt_from_suffix_check():
    assert Path(allowed_suffixes=[".csv"], allow_dash=True).convert("-", None, None) == "-"


def test_suffix_check_runs_before_existence_check(tmp_path):
    with pytest.raises(click.BadParameter) as exc:
        Path(exists=True, allowed_suffixes=[".csv"]).convert(str(tmp_path / "gone.txt"), None, None)
    assert "must end with one of" in str(exc.value)


def test_cli_rejects_wrong_suffix_with_exit_2(tmp_path):
    @click.command()
    @click.option("--input", type=Path(allowed_suffixes=[".csv"]))
    def cli(input):
        click.echo(input)

    result = CliRunner().invoke(cli, ["--input", str(tmp_path / "bad.txt")])
    assert result.exit_code == 2
    assert "must end with one of" in result.output


def test_cli_accepts_allowed_suffix(tmp_path):
    @click.command()
    @click.option("--input", type=Path(allowed_suffixes=[".csv"]))
    def cli(input):
        click.echo(input)

    result = CliRunner().invoke(cli, ["--input", str(tmp_path / "ok.csv")])
    assert result.exit_code == 0


def test_every_listed_suffix_is_accepted(tmp_path):
    t = Path(allowed_suffixes=[".csv", ".json", ".yaml"])
    for ext in (".csv", ".json", ".yaml"):
        name = str(tmp_path / f"data{ext}")
        assert t.convert(name, None, None) == name
