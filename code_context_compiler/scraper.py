import os
import fnmatch
import aiofiles
import asyncio
from .masker import mask_sensitive_info

def is_ignored(file_path, gitignore_patterns):
    """Check if a file should be ignored based on .gitignore patterns."""
    for pattern in gitignore_patterns:
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False

def get_gitignore_patterns(project_path):
    """Read .gitignore and return a list of patterns."""
    gitignore_path = os.path.join(project_path, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

async def process_file(file_path, project_path, gitignore_patterns, out_file):
    if not is_ignored(file_path, gitignore_patterns):
        async with aiofiles.open(file_path, 'r', errors='ignore') as f:
            code = await f.read()
            masked_code = mask_sensitive_info(code)
            relative_path = os.path.relpath(file_path, project_path)
            await out_file.write(f'File: {relative_path}\n')
            await out_file.write(masked_code)
            await out_file.write('\n\n')

async def scrape_project(project_path, output_file):
    gitignore_patterns = get_gitignore_patterns(project_path)

    prompt = f"""
    This text file contains the code from the project located at {project_path}.
    Each file's content is separated by a header indicating the file path.
    Below is an example format:

    File: path/to/first_file.py
    (Content of the first file)

    File: path/to/second_file.py
    (Content of the second file)

    The actual project files and their contents are provided below:
    """

    async with aiofiles.open(output_file, 'w') as out_file:
        await out_file.write(prompt + '\n\n')
        
        tasks = []
        for root, _, files in os.walk(project_path):
            for file in files:
                file_path = os.path.join(root, file)
                tasks.append(process_file(file_path, project_path, gitignore_patterns, out_file))
        
        await asyncio.gather(*tasks)