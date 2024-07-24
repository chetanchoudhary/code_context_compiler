import pytest
from typer.testing import CliRunner
from code_context_compiler.cli import app
from pathlib import Path

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
    assert 'password = "******"' in content

def test_cli_with_config(tmp_path):
    project_path = tmp_path / "project"
    project_path.mkdir()
    file_path = project_path / "test_file.py"
    file_path.write_text('api_key = "secret"')

    config_file = tmp_path / "config.yaml"
    config_file.write_text("""
mask_patterns:
  - 'api_key\\s*=\\s*["''].*?["'']'
""")

    output_file = tmp_path / "output.txt"
    
    result = runner.invoke(app, [str(project_path), str(output_file), "--config-file", str(config_file)])
    assert result.exit_code == 0

    content = output_file.read_text()
    assert 'api_key = "******"' in content

# def test_cli_output_format(tmp_path):
#     project_path = tmp_path / "project"
#     project_path.mkdir()
#     file_path = project_path / "test_file.py"
#     file_path.write_text('password = "secret"')

#     output_file = tmp_path / "output.json"
    
#     result = runner.invoke(app, [str(project_path), str(output_file), "--output-format", "json"])
#     assert result.exit_code == 0

#     content = output_file.read_text()
#     assert '"test_file.py"' in content
#     assert '"password = \\"***MASKED***\\""' in content
