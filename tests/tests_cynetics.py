"""
Basic tests for Cynetics
"""
import pytest
import asyncio
from pathlib import Path
import tempfile
import shutil
from unittest.mock import Mock, AsyncMock
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import from cynetics module
try:
    from cynetics import (
        CyneticsConfig, Cynetics, Specification, TechnicalPlan, Task,
        SpecifyPhase, PlanPhase, TasksPhase, ImplementPhase,
        MCPServerConfig, AIProviderConfig
    )
except ImportError:
    # If running as module, try relative import
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "cynetics",
        Path(__file__).parent.parent / "cynetics.py"
    )
    cynetics = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cynetics)
    
    CyneticsConfig = cynetics.CyneticsConfig
    Cynetics = cynetics.Cynetics
    Specification = cynetics.Specification
    TechnicalPlan = cynetics.TechnicalPlan
    Task = cynetics.Task
    SpecifyPhase = cynetics.SpecifyPhase
    PlanPhase = cynetics.PlanPhase
    TasksPhase = cynetics.TasksPhase
    ImplementPhase = cynetics.ImplementPhase
    MCPServerConfig = cynetics.MCPServerConfig
    AIProviderConfig = cynetics.AIProviderConfig
