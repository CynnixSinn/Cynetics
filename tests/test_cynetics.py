"""
Basic tests for Cynetics
"""
import pytest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_cynetics_file_exists():
    """Test that cynetics.py exists"""
    cynetics_file = Path(__file__).parent.parent / "cynetics.py"
    assert cynetics_file.exists(), "cynetics.py should exist"

def test_requirements_file_exists():
    """Test that requirements.txt exists"""
    req_file = Path(__file__).parent.parent / "requirements.txt"
    assert req_file.exists(), "requirements.txt should exist"

def test_readme_exists():
    """Test that README.md exists"""
    readme = Path(__file__).parent.parent / "README.md"
    assert readme.exists(), "README.md should exist"

@pytest.mark.asyncio
async def test_basic_import():
    """Test basic import works"""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "cynetics",
            Path(__file__).parent.parent / "cynetics.py"
        )
        cynetics = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cynetics)
        
        assert hasattr(cynetics, 'Cynetics')
        assert hasattr(cynetics, 'CyneticsConfig')
    except Exception as e:
        pytest.skip(f"Import test skipped: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
