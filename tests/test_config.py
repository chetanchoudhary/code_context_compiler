import pytest
from code_context_compiler.config import load_config
from pathlib import Path

def test_load_config_default():
    config = load_config()
    assert "ignore_patterns" in config
    assert "file_extensions" in config
    assert "mask_patterns" in config
    assert "use_git" in config
    assert config["file_extensions"] == []  # Should be empty by default

def test_load_config_custom(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text("""
    ignore_patterns:
      - '*.log'
    file_extensions:
      - '.py'
      - '.js'
    use_git: true
    """)

    config = load_config(config_file)
    assert config["ignore_patterns"] == ['*.log']
    assert config["file_extensions"] == ['.py', '.js']
    assert config["use_git"] is True

def test_load_config_merge(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text("""
    ignore_patterns:
      - '*.tmp'
    new_option: 'test'
    """)

    config = load_config(config_file)
    assert '*.tmp' in config["ignore_patterns"]
    assert config["new_option"] == 'test'
    assert "file_extensions" in config  # Should still have default options
