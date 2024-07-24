import asyncio
import json
import os
from pathlib import Path
from typing import Any, Callable, Dict

import aiofiles
import git
import pathspec
import yaml

from .masker import mask_sensitive_info


def load_gitignore(project_path: str) -> pathspec.PathSpec:
    gitignore_path = os.path.join(project_path, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as gitignore_file:
            gitignore = gitignore_file.read().splitlines()
        return pathspec.PathSpec.from_lines("gitwildmatch", gitignore)
    return pathspec.PathSpec.from_lines("gitwildmatch", [])


def is_ignored(
    file_path: str, gitignore_spec: pathspec.PathSpec, ignore_patterns: list
) -> bool:
    """Check if a file should be ignored based on .gitignore and custom patterns."""
    relative_path = os.path.relpath(file_path)
    return gitignore_spec.match_file(relative_path) or any(
        pathspec.Pattern.from_pattern(pattern).match(relative_path)
        for pattern in ignore_patterns
    )


def get_git_tracked_files(project_path: str) -> set:
    """Get a set of files tracked by Git."""
    repo = git.Repo(project_path)
    return set(repo.git.ls_files().splitlines())


async def process_file(
    file_path: str, project_path: str, config: Dict[str, Any], out_file
) -> None:
    """Process a single file: read, mask sensitive info, and write to output."""
    relative_path = os.path.relpath(file_path, project_path)

    # If file_extensions is empty, process all files. Otherwise, check the extension.
    if config["file_extensions"] and not any(
        relative_path.endswith(ext) for ext in config["file_extensions"]
    ):
        return

    async with aiofiles.open(file_path, "r", errors="ignore") as f:
        code = await f.read()
        masked_code = mask_sensitive_info(code, config["mask_patterns"])
        await out_file.write(f"File: {relative_path}\n")
        await out_file.write(masked_code)
        await out_file.write("\n\n")


async def scrape_project(
    project_path: str,
    output_file: str,
    config: Dict[str, Any],
    output_format: str,
    progress_callback: Callable[[float], None],
) -> None:
    """Scrape the entire project, process files, and write to output."""
    gitignore_spec = load_gitignore(project_path)
    git_tracked_files = (
        get_git_tracked_files(project_path) if config["use_git"] else None
    )

    async with aiofiles.open(output_file, "w") as out_file:
        files_to_process = []
        for root, _, files in os.walk(project_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, project_path)

                if is_ignored(file_path, gitignore_spec, config["ignore_patterns"]):
                    continue

                if git_tracked_files and relative_path not in git_tracked_files:
                    continue

                files_to_process.append(file_path)

        total_files = len(files_to_process)

        for i, file_path in enumerate(files_to_process):
            await process_file(file_path, project_path, config, out_file)
            progress_callback((i + 1) / total_files * 100)

    if output_format in ["json", "yaml"]:
        convert_output(output_file, output_format)


def convert_output(output_file: str, output_format: str) -> None:
    """Convert the output file to JSON or YAML format."""
    with open(output_file, "r") as f:
        content = f.read()

    files = content.split("\nFile: ")
    files_dict = {file.split("\n", 1)[0]: file.split("\n", 1)[1] for file in files[1:]}

    if output_format == "json":
        with open(output_file, "w") as f:
            json.dump(files_dict, f, indent=2)
    elif output_format == "yaml":
        with open(output_file, "w") as f:
            yaml.dump(files_dict, f)
