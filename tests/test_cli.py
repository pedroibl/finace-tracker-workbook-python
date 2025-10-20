from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from budget_generator.__main__ import cli


def fixture_path(filename: str) -> Path:
    return Path(__file__).parent / "fixtures" / filename


def test_cli_help_displays_usage() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Excel Budget Generator" in result.output


def test_generate_validate_only_runs_validation() -> None:
    runner = CliRunner()
    spec_path = fixture_path("valid_spec.json")
    result = runner.invoke(cli, ["generate", str(spec_path), "--validate-only"])
    assert result.exit_code == 0
    assert "validated successfully" in result.output


def test_generate_missing_file_reports_error(tmp_path: Path) -> None:
    runner = CliRunner()
    missing = tmp_path / "missing.json"
    result = runner.invoke(cli, ["generate", str(missing), "--validate-only"])
    assert result.exit_code != 0
    assert "Specification not found" in result.output
