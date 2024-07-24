import pytest
import asyncio
from code_context_compiler.scraper import scrape_project

@pytest.mark.asyncio
async def test_scrape_project(tmp_path):
    project_path = tmp_path / "project"
    project_path.mkdir()
    file_path = project_path / "test_file.py"
    file_path.write_text('password = "secret"')

    output_file = tmp_path / "output.txt"
    
    await scrape_project(str(project_path), str(output_file))
    
    content = output_file.read_text()
    assert 'password = "***MASKED***"' in content
