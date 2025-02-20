import asyncio
import logging
from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress

from code_context_compiler.config import load_config
from code_context_compiler.scraper import scrape_project

app = typer.Typer()
console = Console()


@app.command()
def main(
    project_path: Path = typer.Argument(..., help="Path to the project to scan"),
    output_file: Path = typer.Argument(..., help="Path to the output file"),
    config_file: Path = typer.Option(None, help="Path to the configuration file"),
    output_format: str = typer.Option(
        "text", help="Output format: text, json, or yaml"
    ),
    debug: bool = typer.Option(False, help="Enable debug logging"),
):
    """
    CLI tool to scan a code project and create a single file with the entire project code.
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if output_format in ["json", "yaml"]:
        raise NotImplementedError
    try:
        config = load_config(config_file)

        with Progress() as progress:
            task = progress.add_task("[green]Scanning project...", total=100)

            def update_progress(percentage):
                progress.update(task, completed=percentage)

            asyncio.run(
                scrape_project(
                    project_path, output_file, config, output_format, update_progress
                )
            )

        console.print(f"[green]Output written to {output_file}[/green]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
