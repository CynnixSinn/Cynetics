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
sys.path.insert(0, str(Path(__file__).parent.parent))

from cynetics import (
    CyneticsConfig, Cynetics, Specification, TechnicalPlan, Task,
    SpecifyPhase, PlanPhase, TasksPhase, ImplementPhase,
    MCPServerConfig, AIProviderConfig
)

@pytest.fixture
def temp_dir():
    """Create temporary directory"""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)

@pytest.fixture
def mock_ai_provider():
    """Mock AI provider"""
    provider = Mock()
    provider.generate = AsyncMock()
    return provider

@pytest.fixture
def sample_config(temp_dir):
    """Sample configuration"""
    return CyneticsConfig(
        project_root=temp_dir,
        mcp_servers=[],
        ai_providers=[
            AIProviderConfig(
                provider="mock",
                model="test-model",
                api_key="test-key"
            )
        ],
        default_provider="mock",
        workspace_dir=temp_dir / "workspace",
        artifacts_dir=temp_dir / "artifacts"
    )

class TestConfiguration:
    """Test configuration management"""
    
    def test_create_default_config(self, temp_dir):
        """Test creating default configuration"""
        config = CyneticsConfig.create_default(temp_dir)
        
        assert config.project_root == temp_dir
        assert len(config.mcp_servers) > 0
        assert len(config.ai_providers) > 0
        assert config.default_provider == "anthropic"
    
    def test_config_serialization(self, temp_dir, sample_config):
        """Test saving and loading configuration"""
        config_file = temp_dir / "test_config.json"
        
        # Save
        config_data = {
            "project_root": str(sample_config.project_root),
            "workspace_dir": str(sample_config.workspace_dir),
            "artifacts_dir": str(sample_config.artifacts_dir),
            "default_provider": sample_config.default_provider,
            "mcp_servers": [],
            "ai_providers": [
                {
                    "provider": "mock",
                    "model": "test",
                    "api_key": "key",
                    "temperature": 0.7,
                    "max_tokens": 4096
                }
            ]
        }
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        # Load
        loaded = CyneticsConfig.load(config_file)
        assert loaded.default_provider == "mock"

class TestSpecifyPhase:
    """Test specification generation"""
    
    @pytest.mark.asyncio
    async def test_generate_spec(self, mock_ai_provider):
        """Test spec generation"""
        mock_ai_provider.generate.return_value = json.dumps({
            "problem_statement": "Test problem",
            "target_users": ["developers"],
            "user_journeys": [{"journey": "test", "steps": ["step1"]}],
            "success_criteria": ["works"],
            "constraints": []
        })
        
        phase = SpecifyPhase(mock_ai_provider)
        spec = await phase.generate_spec("Test description")
        
        assert isinstance(spec, Specification)
        assert spec.problem_statement == "Test problem"
        assert "developers" in spec.target_users

class TestPlanPhase:
    """Test technical planning"""
    
    @pytest.mark.asyncio
    async def test_generate_plan(self, mock_ai_provider):
        """Test plan generation"""
        mock_ai_provider.generate.return_value = json.dumps({
            "architecture": "Layered",
            "tech_stack": {"language": "Python"},
            "components": [],
            "data_models": [],
            "api_design": {},
            "infrastructure": {},
            "dependencies": [],
            "alternatives": []
        })
        
        spec = Specification(
            problem_statement="Test",
            target_users=["users"],
            user_journeys=[],
            success_criteria=[],
            constraints=[],
            raw_description="Test"
        )
        
        phase = PlanPhase(mock_ai_provider)
        plan = await phase.generate_plan(spec)
        
        assert isinstance(plan, TechnicalPlan)
        assert plan.architecture == "Layered"

class TestTasksPhase:
    """Test task decomposition"""
    
    @pytest.mark.asyncio
    async def test_generate_tasks(self, mock_ai_provider):
        """Test task generation"""
        mock_ai_provider.generate.return_value = json.dumps([
            {
                "id": "task-1",
                "title": "Setup",
                "description": "Init project",
                "acceptance_criteria": ["works"],
                "dependencies": [],
                "estimated_complexity": "simple",
                "files_to_modify": ["main.py"],
                "test_plan": "pytest",
                "status": "pending"
            }
        ])
        
        spec = Specification(
            problem_statement="Test",
            target_users=["users"],
            user_journeys=[],
            success_criteria=[],
            constraints=[],
            raw_description="Test"
        )
        
        plan = TechnicalPlan(
            architecture="Test",
            tech_stack={},
            components=[],
            data_models=[],
            api_design={},
            infrastructure={},
            dependencies=[],
            alternatives=[]
        )
        
        phase = TasksPhase(mock_ai_provider)
        tasks = await phase.generate_tasks(spec, plan)
        
        assert len(tasks) == 1
        assert tasks[0].id == "task-1"

class TestImplementPhase:
    """Test implementation"""
    
    @pytest.mark.asyncio
    async def test_implement_task(self, mock_ai_provider, temp_dir):
        """Test task implementation"""
        mock_ai_provider.generate.return_value = "Implementation complete"
        
        task = Task(
            id="task-1",
            title="Test",
            description="Test task",
            acceptance_criteria=["works"],
            dependencies=[],
            estimated_complexity="simple",
            files_to_modify=[],
            test_plan="test"
        )
        
        phase = ImplementPhase(mock_ai_provider, temp_dir)
        result = await phase.implement_task(task, {})
        
        assert result["task_id"] == "task-1"
        assert result["status"] == "completed"

class TestCyneticsIntegration:
    """Integration tests"""
    
    @pytest.mark.asyncio
    async def test_full_workflow(self, mock_ai_provider, sample_config):
        """Test complete workflow"""
        # Mock responses
        responses = [
            json.dumps({
                "problem_statement": "Test",
                "target_users": ["users"],
                "user_journeys": [],
                "success_criteria": [],
                "constraints": []
            }),
            json.dumps({
                "architecture": "Test",
                "tech_stack": {},
                "components": [],
                "data_models": [],
                "api_design": {},
                "infrastructure": {},
                "dependencies": [],
                "alternatives": []
            }),
            json.dumps([
                {
                    "id": "task-1",
                    "title": "Test",
                    "description": "Test",
                    "acceptance_criteria": [],
                    "dependencies": [],
                    "estimated_complexity": "simple",
                    "files_to_modify": [],
                    "test_plan": "",
                    "status": "pending"
                }
            ])
        ]
        
        mock_ai_provider.generate.side_effect = responses
        
        # Create cynetics instance
        cynetics = Cynetics(sample_config)
        cynetics.ai_providers["mock"] = mock_ai_provider
        cynetics.specify = SpecifyPhase(mock_ai_provider)
        cynetics.plan = PlanPhase(mock_ai_provider)
        cynetics.tasks = TasksPhase(mock_ai_provider)
        
        await cynetics.start()
        
        # Run (skip actual implementation)
        spec = await cynetics.specify.generate_spec("Test")
        assert spec.problem_statement == "Test"
        
        plan = await cynetics.plan.generate_plan(spec)
        assert plan.architecture == "Test"
        
        tasks = await cynetics.tasks.generate_tasks(spec, plan)
        assert len(tasks) == 1

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
