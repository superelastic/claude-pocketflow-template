"""Tests to verify project setup is correct."""

import sys
from pathlib import Path

import pytest


def test_imports():
    """Test that all core modules can be imported."""
    # These imports should not raise any errors
    import src.flows.base  # noqa: PLC0415
    import src.flows.examples  # noqa: PLC0415
    import src.nodes.base  # noqa: PLC0415
    import src.nodes.examples  # noqa: PLC0415, F401

    assert True  # If we get here, imports worked


def test_python_version():
    """Test that Python version meets requirements."""
    assert sys.version_info >= (3, 10), "Python 3.10+ is required"


@pytest.mark.skip(reason="Too brittle for solo development")
def test_project_structure():
    """Test that expected directories exist."""
    project_root = Path(__file__).parent.parent

    expected_dirs = [
        "src",
        "src/nodes",
        "src/flows",
        "src/utils",
        "tests",
        "docs",
        "planning",
        "agents",
        ".mdc",
    ]

    for dir_path in expected_dirs:
        full_path = project_root / dir_path
        assert full_path.exists(), f"Directory {dir_path} should exist"
        assert full_path.is_dir(), f"{dir_path} should be a directory"


@pytest.mark.skip(reason="Too brittle for solo development")
def test_required_files():
    """Test that required files exist."""
    project_root = Path(__file__).parent.parent

    required_files = [
        "README.md",
        "DEVELOPMENT_GUIDE.md",
        "CLAUDE.md",
        "pyproject.toml",
        "setup.sh",
        ".env.example",
        ".gitignore",
        ".mdc/pocketflow-rules.md",
        "docs/design.md",
        "docs/flow-design.md",
    ]

    for file_path in required_files:
        full_path = project_root / file_path
        assert full_path.exists(), f"File {file_path} should exist"
        assert full_path.is_file(), f"{file_path} should be a file"
