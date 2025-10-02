import pytest
from pathlib import Path

def test_files_exist():
    """Test that main files exist"""
    assert Path("cynetics.py").exists()
    assert Path("requirements.txt").exists()
    assert Path("README.md").exists()
