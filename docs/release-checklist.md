# Release Checklist (v1.0.0)

Use this checklist before tagging and publishing the release.

## Verification
- [ ] `uv run pytest --cov=budget_generator --cov-report=term` (confirm ≥80 % coverage)
- [ ] If pytest-cov unavailable: `uv run python scripts/run_coverage.py` and record percentage
- [ ] `uv run budget-generator generate examples/tutorial_spec.json -o build/tutorial.xlsx -v`
- [ ] Open generated workbook in Microsoft 365 and LibreOffice (latest -1) to verify:
  - Settings dropdowns and validations
  - Dropdown Data hidden sheet values
  - Planning formulas (`D13`, unallocated row) and Year 2 scaffold
  - Tracking table formatting, validations, and formulas
  - Dashboard selectors, KPI tiles, doughnut charts
- [ ] Compare `build/tutorial.xlsx` against `tests/fixtures/golden_tutorial.xlsx` using `pytest -k output`

## Documentation
- [ ] README reflects installation, CLI usage, testing, coverage commands, and customization tips
- [ ] `docs/tutorial-mapping.md` updated for any spec changes
- [ ] Changelog / release notes drafted
- [ ] PRD checkboxes updated through Phase 4

## Packaging
- [ ] `uv build`
- [ ] Smoke test built wheel: `uv run pip install dist/*.whl`
- [ ] `budget-generator --version` matches target release

## Tag & Publish
- [ ] Commit all changes
- [ ] `git tag v1.0.0`
- [ ] `git push origin main --tags`
- [ ] Create GitHub release with notes and attach artifacts
- [ ] (Optional) `uv publish` to PyPI/TestPyPI

## Post-Release
- [ ] Generate sample workbook(s) for distribution
- [ ] Update project board / issues with release status
- [ ] Draft follow-up tasks or known issues
