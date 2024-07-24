import pytest
from typer.testing import CliRunner
from code_context_compiler.cli import app

runner = CliRunner()

def test_cli(tmp_path):
    project_path = tmp_path / "project"
    project_path.mkdir()
    file_path = project_path / "test_file.py"
    file_path.write_text('password = "secret"')

    output_file = tmp_path / "output.txt"
    
    result = runner.invoke(app, [str(project_path), str(output_file)])
    assert result.exit_code == 0

    content = output_file.read_text()
    assert 'password = "***MASKED***"' in content
