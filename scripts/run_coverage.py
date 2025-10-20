"""Lightweight coverage runner using Python's stdlib trace module.

This is a fallback for environments where pytest-cov or coverage.py are not
available. It instruments the budget_generator package only and prints an
approximate line coverage summary.
"""

from __future__ import annotations

import argparse
import os
import sys
import trace
from pathlib import Path
from typing import Iterable

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PROJECT_ROOT / "src" / "budget_generator"
MIN_COVERAGE = 0.80


def iter_source_files() -> Iterable[Path]:
    for path in SOURCE_ROOT.rglob("*.py"):
        yield path


def is_countable(line: str) -> bool:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return False
    if stripped.startswith("\"\"\"") or stripped.startswith("'''"):
        return False
    if stripped.startswith("__all__"):
        return False
    if "pragma: no cover" in stripped:
        return False
    if stripped in {"(", ")", "[", "]", "{", "}"}:
        return False
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--min",
        type=float,
        default=MIN_COVERAGE,
        help="Minimum required coverage percentage (0-1). Default: 0.80",
    )
    args = parser.parse_args(argv)

    tracer = trace.Trace(
        count=True,
        trace=False,
        ignoremods=set(sys.builtin_module_names),
        ignoredirs=[str(PROJECT_ROOT / ".venv"), str(PROJECT_ROOT / "tests")],
    )

    # Run pytest under tracing.
    success = tracer.runfunc(pytest.main, ["-p", "no:cov"])
    if success != 0:
        print("pytest reported failures; aborting coverage calculation.", file=sys.stderr)
        return success

    results = tracer.results()

    counts_map: dict[Path, dict[int, int]] = {}
    for key, count in results.counts.items():
        if not isinstance(key, tuple) or len(key) != 2:
            continue
        filename, lineno = key
        if not isinstance(filename, (str, os.PathLike)):
            continue
        path = Path(filename).resolve()
        counts_for_file = counts_map.setdefault(path, {})
        counts_for_file[lineno] = counts_for_file.get(lineno, 0) + int(count)

    total_lines = 0
    executed_lines = 0
    missing: dict[Path, list[int]] = {}

    for source_file in iter_source_files():
        counts = counts_map.get(source_file.resolve())
        lines = source_file.read_text().splitlines()
        interesting_lines = {
            idx + 1 for idx, line in enumerate(lines) if is_countable(line)
        }

        total_lines += len(interesting_lines)
        if counts:
            executed_here = {
                lineno for lineno in counts.keys() if lineno in interesting_lines
            }
        else:
            executed_here = set()

        executed_lines += len(executed_here)
        missing_lines = sorted(interesting_lines - executed_here)
        if missing_lines:
            missing[source_file] = missing_lines

    coverage = (executed_lines / total_lines) if total_lines else 1.0
    percent = coverage * 100

    print(f"Total lines: {total_lines}")
    print(f"Executed lines: {executed_lines}")
    print(f"Approximate coverage: {percent:.2f}%")
    if missing:
        print("\nMissing lines:")
        for path, line_numbers in sorted(missing.items()):
            preview = ", ".join(str(n) for n in line_numbers[:10])
            suffix = "..." if len(line_numbers) > 10 else ""
            rel_path = path.relative_to(PROJECT_ROOT)
            print(f"  {rel_path}: {preview}{suffix}")

    if coverage < args.min:
        print(
            f"Coverage below target ({percent:.2f}% < {args.min * 100:.2f}%).",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
