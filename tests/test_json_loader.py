from __future__ import annotations

from pathlib import Path

import pytest

from budget_generator.utils.json_loader import (
    SpecParseError,
    SpecReadError,
    SpecValidationError,
    ValidationResult,
    load_json_spec,
    validate_json_structure,
)


def fixture_path(filename: str) -> Path:
    return Path(__file__).parent / "fixtures" / filename


def test_load_json_spec_success() -> None:
    spec_path = fixture_path("valid_spec.json")
    spec = load_json_spec(spec_path)
    assert spec["meta"]["name"] == "Budget Excel Generator Specification"


def test_load_json_spec_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "does-not-exist.json"
    with pytest.raises(SpecReadError):
        load_json_spec(missing)


def test_load_json_spec_invalid_json(tmp_path: Path) -> None:
    bad = tmp_path / "invalid.json"
    bad.write_text("{broken}", encoding="utf-8")
    with pytest.raises(SpecParseError):
        load_json_spec(bad)


def test_validate_json_structure_success() -> None:
    spec = load_json_spec(fixture_path("valid_spec.json"))
    result = validate_json_structure(spec)
    assert isinstance(result, ValidationResult)


def test_validate_json_structure_reports_all_issues() -> None:
    spec = load_json_spec(fixture_path("invalid_spec.json"))
    with pytest.raises(SpecValidationError) as exc:
        validate_json_structure(spec)
    message = str(exc.value)
    assert "Missing required sheets" in message
    assert "must be an object" in message
