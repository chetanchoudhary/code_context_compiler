import pytest
import asyncio
import json
from code_context_compiler.scraper import scrape_project, is_ignored, get_git_tracked_files, load_gitignore
from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
async def test_scrape_project(tmp_path):
    project_path = tmp_path / "project"
    project_path.mkdir()
    file_path = project_path / "test_file.py"
    file_path.write_text('password = "secret"')

    output_file = tmp_path / "output.txt"
    
    config = {
        "ignore_patterns": [],
        "file_extensions": [],
        "mask_patterns": [r'password\s*=\s*["\'].*?["\']'],
        "use_git": False
    }
    
    await scrape_project(str(project_path), str(output_file), config, "text", lambda x: None)
    
    content = output_file.read_text()
    assert 'password = "******"' in content

@pytest.mark.asyncio
async def test_scrape_project_with_gitignore(tmp_path):
    project_path = tmp_path / "project"
    project_path.mkdir()
    
    # Create a .gitignore file
    gitignore_path = project_path / ".gitignore"
    gitignore_path.write_text("*.log\n")
    
    # Create files
    (project_path / "test_file.py").write_text('password = "secret"')
    (project_path / "test_file.log").write_text('sensitive_log = "should_be_ignored"')

    output_file = tmp_path / "output.txt"
    
    config = {
        "ignore_patterns": [],
        "file_extensions": [],
        "mask_patterns": [r'password\s*=\s*["\'].*?["\']'],
        "use_git": False
    }
    
    await scrape_project(str(project_path), str(output_file), config, "text", lambda x: None)
    
    content = output_file.read_text()
    assert 'password = "******"' in content
    assert 'sensitive_log = "should_be_ignored"' not in content

# @pytest.mark.asyncio
# async def test_scrape_project_output_format(tmp_path):
#     project_path = tmp_path / "project"
#     project_path.mkdir()
#     file_path = project_path / "test_file.py"
#     file_path.write_text('password = "secret"')

#     output_file = tmp_path / "output.json"
    
#     config = {
#         "ignore_patterns": [],
#         "file_extensions": [],
#         "mask_patterns": [r'password\s*=\s*["\'].*?["\']'],
#         "use_git": False
#     }
    
#     await scrape_project(str(project_path), str(output_file), config, "json", lambda x: None)
    
#     with open(output_file, 'r') as f:
#         content = json.load(f)
    
#     assert "test_file.py" in content
#     assert 'password = "******"' in content["test_file.py"]

def test_is_ignored(tmp_path):
    project_path = tmp_path / "project"
    project_path.mkdir()
    
    # Create a .gitignore file
    gitignore_path = project_path / ".gitignore"
    gitignore_path.write_text("*.log\n")
    
    gitignore_spec = load_gitignore(str(project_path))
    
    assert is_ignored(str(project_path / "test.log"), gitignore_spec, []) == True
    assert is_ignored(str(project_path / "test.py"), gitignore_spec, []) == False

@patch('git.Repo')
def test_get_git_tracked_files(mock_repo):
    mock_git = MagicMock()
    mock_git.ls_files.return_value = "file1.py\nfile2.py"
    mock_repo.return_value.git = mock_git

    tracked_files = get_git_tracked_files("/fake/path")
    assert tracked_files == {"file1.py", "file2.py"}
