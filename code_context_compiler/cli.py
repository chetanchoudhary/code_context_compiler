import typer
import asyncio
from .scraper import scrape_project

app = typer.Typer()

@app.command()
def main(project_path: str, output_file: str):
    """CLI tool to scan a code project and create a single text file with the entire project code."""
    typer.echo(f"Scanning project at {project_path}...")
    asyncio.run(scrape_project(project_path, output_file))
    typer.echo(f"Output written to {output_file}")

if __name__ == "__main__":
    app()
