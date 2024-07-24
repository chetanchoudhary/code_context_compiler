import asyncio
import fnmatch
import json
import logging
import os
from pathlib import Path
from typing import Any, Callable, Dict

import aiofiles
import git
import pathspec
import yaml

from code_context_compiler.masker import mask_sensitive_info

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def load_gitignore(project_path: str) -> pathspec.PathSpec:
    gitignore_path = os.path.join(project_path, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as gitignore_file:
            gitignore = gitignore_file.read().splitlines()
        return pathspec.PathSpec.from_lines("gitwildmatch", gitignore)
    return pathspec.PathSpec.from_lines("gitwildmatch", [])


def is_ignored(
    file_path: str,
    project_path: str,
    gitignore_spec: pathspec.PathSpec,
    ignore_patterns: list,
) -> bool:
    """Check if a file should be ignored based on .gitignore and custom patterns."""
    relative_path = os.path.relpath(file_path, project_path)

    # Check gitignore patterns
    if gitignore_spec.match_file(relative_path):
        logger.debug(f"File {relative_path} ignored due to .gitignore")
        return True

    # Check custom ignore patterns
    for pattern in ignore_patterns:
        if pattern.endswith("/"):
            # It's a directory pattern
            if relative_path.startswith(pattern) or relative_path.startswith(
                pattern[:-1]
            ):
                logger.debug(
                    f"File {relative_path} ignored due to directory pattern: {pattern}"
                )
                return True
        elif fnmatch.fnmatch(relative_path, pattern):
            logger.debug(
                f"File {relative_path} ignored due to custom pattern: {pattern}"
            )
            return True

    logger.debug(f"File {relative_path} is not ignored")
    return False


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
        # Add the LLM prompt at the beginning of the file
        llm_prompt = """
This document contains the compiled code of an entire project. The content is organized as follows:

1. Each file's content is preceded by a line starting with "File: " followed by the file path.
2. The actual content of each file follows immediately after the "File: " line.
3. There's an empty line between each file's content for better readability.
4. Some sensitive information may have been masked and replaced with "******".

When analyzing or referring to this code:
- Pay attention to the file paths to understand the project structure.
- Treat each "File: " section as a separate file in the project.
- Be aware that masked information is sensitive and should not be speculated upon.
- Consider the relationships and dependencies between different files.

Please process this information accordingly and use it to understand the overall structure and content of the project.

The project files and their contents begin below:

"""
        await out_file.write(llm_prompt)

        files_to_process = []
        for root, dirs, files in os.walk(project_path):
            # Remove ignored directories
            dirs[:] = [
                d
                for d in dirs
                if not is_ignored(
                    os.path.join(root, d),
                    project_path,
                    gitignore_spec,
                    config["ignore_patterns"],
                )
            ]

            for file in files:
                file_path = os.path.join(root, file)
                if not is_ignored(
                    file_path, project_path, gitignore_spec, config["ignore_patterns"]
                ):
                    if (
                        not git_tracked_files
                        or os.path.relpath(file_path, project_path) in git_tracked_files
                    ):
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

    # Split the content into the prompt and the files
    prompt, files_content = content.split(
        "The project files and their contents begin below:", 1
    )

    files = files_content.strip().split("\nFile: ")
    files_dict = {
        file.split("\n", 1)[0]: file.split("\n", 1)[1] for file in files if file
    }

    output_dict = {"prompt": prompt.strip(), "files": files_dict}

    if output_format == "json":
        with open(output_file, "w") as f:
            json.dump(output_dict, f, indent=2)
    elif output_format == "yaml":
        with open(output_file, "w") as f:
            yaml.dump(output_dict, f)
