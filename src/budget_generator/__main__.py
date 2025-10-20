"""Command line entry point for the budget workbook generator."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import click

from . import __version__
from .utils import json_loader


LOGGER_NAME = "budget_generator"


def configure_logging(verbose: bool) -> None:
    """Initialise logging with a friendly default format."""

    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s %(name)s - %(message)s",
    )


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging output.")
def cli(verbose: bool) -> None:
    """Excel Budget Generator - create workbooks from JSON specs."""

    configure_logging(verbose)


@cli.command()
@click.argument("json_file", type=click.Path(path_type=Path))
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    default=Path("budget_workbook.xlsx"),
    show_default=True,
    help="Path where the generated workbook should be saved.",
)
@click.option(
    "--validate-only",
    is_flag=True,
    help="Validate the JSON specification without writing a workbook.",
)
def generate(json_file: Path, output: Path, validate_only: bool) -> None:
    """Generate an Excel budget workbook from *JSON_FILE*."""

    logger = logging.getLogger(LOGGER_NAME)

    if not json_file.exists():
        raise click.ClickException(f"Specification not found: {json_file}")

    try:
        spec = json_loader.load_json_spec(json_file)
        json_loader.validate_json_structure(spec)
    except json_loader.SpecReadError as exc:
        raise click.ClickException(str(exc))
    except json_loader.SpecParseError as exc:
        raise click.ClickException(str(exc))
    except json_loader.SpecValidationError as exc:
        raise click.ClickException(f"Specification validation failed: {exc}")

    if validate_only:
        message = "Specification validated successfully. No workbook written."
        logger.info(message)
        click.echo(message)
        return

    # Notebook generation is implemented in the dedicated generator module.  We
    # import lazily so that validation-only runs do not incur the dependency.
    from .generator import BudgetGenerator  # local import to avoid cycle

    generator = BudgetGenerator(spec)

    try:
        generator.create_workbook()
        generator.create_sheets(spec)
        generator.build_sheet_contents()
        generator.save_workbook(output)
    except Exception as exc:  # pragma: no cover - exercised via integration
        raise click.ClickException(f"Workbook generation failed: {exc}") from exc

    logger.info("Workbook successfully written to %s", output)
    click.echo(f"Workbook successfully written to {output}")


def main(argv: Optional[list[str]] = None) -> None:
    """Entry point for console scripts (mirrors `python -m`)."""

    cli.main(args=argv, prog_name="budget-generator", standalone_mode=False)


if __name__ == "__main__":  # pragma: no cover
    main()
