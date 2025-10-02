#!/usr/bin/env python3
"""
Cynetics - Autonomous Agentic Coding System
Main Orchestrator Module
"""

import asyncio
import json
import os
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
from pathlib import Path
from abc import ABC, abstractmethod
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cynetics")

# ============================================================================
# Data Models
# ============================================================================

@dataclass
class MCPServerConfig:
    """Configuration for an MCP server"""
    name: str
    command: str
    args: List[str] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)
    enabled: bool = True

@dataclass
class AIProviderConfig:
    """Configuration for AI provider"""
    provider: str
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4096

@dataclass
class CyneticsConfig:
    """Main configuration"""
    project_root: Path
    mcp_servers: List[MCPServerConfig]
    ai_providers: List[AIProviderConfig]
    default_provider: str
    workspace_dir: Path
    artifacts_dir: Path
    
    @classmethod
    def load(cls, config_path: Path) -> "CyneticsConfig":
        """Load from JSON file"""
        with open(config_path) as f:
            data = json.load(f)
        
        return cls(
            project_root=Path(data["project_root"]),
            mcp_servers=[MCPServerConfig(**srv) for srv in data.get("mcp_servers", [])],
            ai_providers=[AIProviderConfig(**prov) for prov in data.get("ai_providers", [])],
            default_provider=data.get("default_provider", "anthropic"),
            workspace_dir=Path(data.get("workspace_dir", "./workspace")),
            artifacts_dir=Path(data.get("artifacts_dir", "./artifacts"))
        )
    
    @classmethod
    def create_default(cls, project_root: Path) -> "CyneticsConfig":
        """Create default configuration"""
        return cls(
            project_root=project_root,
            mcp_servers=[
                MCPServerConfig(
                    name="filesystem",
                    command="npx",
                    args=["-y", "@modelcontextprotocol/server-filesystem", str(project_root)]
                ),
                MCPServerConfig(
                    name="git",
                    command="npx",
                    args=["-y", "@modelcontextprotocol/server-git"]
                ),
                MCPServerConfig(
                    name="shell",
                    command="npx",
                    args=["-y", "@modelcontextprotocol/server-shell"]
                ),
                MCPServerConfig(
                    name="memory",
                    command="npx",
                    args=["-y", "@modelcontextprotocol/server-memory"]
                ),
            ],
            ai_providers=[
                AIProviderConfig(
                    provider="anthropic",
                    model="claude-sonnet-4-5-20250929",
                    api_key=os.getenv("ANTHROPIC_API_KEY")
                )
            ],
            default_provider="anthropic",
            workspace_dir=project_root / "workspace",
            artifacts_dir=project_root / "artifacts"
        )

@dataclass
class Specification:
    """User-centric specification"""
    problem_statement: str
    target_users: List[str]
    user_journeys: List[Dict[str, Any]]
    success_criteria: List[str]
    constraints: List[str]
    raw_description: str
    version: int = 1

@dataclass
class TechnicalPlan:
    """Technical architecture plan"""
    architecture: str
    tech_stack: Dict[str, str]
    components: List[Dict[str, Any]]
    data_models: List[Dict[str, Any]]
    api_design: Dict[str, Any]
    infrastructure: Dict[str, Any]
    dependencies: List[str]
    alternatives: List[Dict[str, Any]]

@dataclass
class Task:
    """Atomic work unit"""
    id: str
    title: str
    description: str
    acceptance_criteria: List[str]
    dependencies: List[str]
    estimated_complexity: str
    files_to_modify: List[str]
    test_plan: str
    status: str = "pending"

# ============================================================================
# AI Provider Abstraction
# ============================================================================

class AIProvider(ABC):
    """Abstract AI provider"""
    
    @abstractmethod
    async def generate(self, messages: List[Dict[str, str]], **kwargs) -> str:
        pass

class AnthropicProvider(AIProvider):
    """Anthropic Claude provider"""
    
    def __init__(self, config: AIProviderConfig):
        self.config = config
        try:
            from anthropic import AsyncAnthropic
            self.client = AsyncAnthropic(api_key=config.api_key)
        except ImportError:
            raise ImportError("Install: pip install anthropic")
    
    async def generate(self, messages: List[Dict[str, str]], **kwargs) -> str:
        response = await self.client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            messages=messages,
            **kwargs
        )
        return response.content[0].text

class OpenAIProvider(AIProvider):
    """OpenAI provider"""
    
    def __init__(self, config: AIProviderConfig):
        self.config = config
        try:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(
                api_key=config.api_key,
                base_url=config.base_url
            )
        except ImportError:
            raise ImportError("Install: pip install openai")
    
    async def generate(self, messages: List[Dict[str, str]], **kwargs) -> str:
        response = await self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content

# ============================================================================
# Phase Implementations
# ============================================================================

class SpecifyPhase:
    """Generate specifications"""
    
    def __init__(self, ai_provider: AIProvider):
        self.ai = ai_provider
    
    async def generate_spec(self, description: str) -> Specification:
        """Generate specification from description"""
        
        prompt = f"""You are a product specification expert. Generate a detailed specification.

Description: {description}

Output JSON with keys: problem_statement, target_users (array), user_journeys (array of objects with journey and steps), success_criteria (array), constraints (array)"""

        response = await self.ai.generate([{"role": "user", "content": prompt}])
        
        # Extract JSON from response
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            spec_data = json.loads(json_match.group())
        else:
            spec_data = json.loads(response)
        
        return Specification(
            problem_statement=spec_data["problem_statement"],
            target_users=spec_data["target_users"],
            user_journeys=spec_data["user_journeys"],
            success_criteria=spec_data["success_criteria"],
            constraints=spec_data.get("constraints", []),
            raw_description=description
        )

class PlanPhase:
    """Create technical plans"""
    
    def __init__(self, ai_provider: AIProvider):
        self.ai = ai_provider
    
    async def generate_plan(
        self, 
        spec: Specification, 
        tech_preferences: Optional[Dict[str, Any]] = None
    ) -> TechnicalPlan:
        """Generate technical plan"""
        
        prompt = f"""You are a software architect. Create a technical plan.

Specification: {json.dumps(asdict(spec), indent=2)}
Tech Preferences: {json.dumps(tech_preferences or {}, indent=2)}

Output JSON with keys: architecture, tech_stack (dict), components (array), data_models (array), api_design (dict), infrastructure (dict), dependencies (array), alternatives (array)"""

        response = await self.ai.generate([{"role": "user", "content": prompt}])
        
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            plan_data = json.loads(json_match.group())
        else:
            plan_data = json.loads(response)
        
        return TechnicalPlan(**plan_data)

class TasksPhase:
    """Break down into tasks"""
    
    def __init__(self, ai_provider: AIProvider):
        self.ai = ai_provider
    
    async def generate_tasks(
        self, 
        spec: Specification, 
        plan: TechnicalPlan
    ) -> List[Task]:
        """Generate tasks"""
        
        prompt = f"""You are a project manager. Break work into atomic tasks.

Specification: {json.dumps(asdict(spec), indent=2)}
Plan: {json.dumps(asdict(plan), indent=2)}

Output JSON array of tasks with keys: id, title, description, acceptance_criteria (array), dependencies (array), estimated_complexity, files_to_modify (array), test_plan, status"""

        response = await self.ai.generate([{"role": "user", "content": prompt}])
        
        import re
        json_match = re.search(r'\[.*\]', response, re.DOTALL)
        if json_match:
            tasks_data = json.loads(json_match.group())
        else:
            tasks_data = json.loads(response)
        
        return [Task(**task) for task in tasks_data]

class ImplementPhase:
    """Autonomous implementation"""
    
    def __init__(self, ai_provider: AIProvider, workspace: Path):
        self.ai = ai_provider
        self.workspace = workspace
    
    async def implement_task(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Implement a task"""
        
        prompt = f"""You are a software engineer. Implement this task.

Task: {task.title}
Description: {task.description}
Acceptance Criteria: {', '.join(task.acceptance_criteria)}
Files: {', '.join(task.files_to_modify)}

Context: {json.dumps(context, indent=2, default=str)}

Provide implementation as text explaining what code to write."""

        response = await self.ai.generate([{"role": "user", "content": prompt}])
        
        logger.info(f"Task {task.id}: {response[:200]}...")
        
        return {
            "task_id": task.id,
            "status": "completed",
            "implementation": response
        }

# ============================================================================
# Main Orchestrator
# ============================================================================

class Cynetics:
    """Main orchestrator"""
    
    def __init__(self, config: CyneticsConfig):
        self.config = config
        self.ai_providers: Dict[str, AIProvider] = {}
        
        # Initialize AI providers
        for provider_config in config.ai_providers:
            if provider_config.provider == "anthropic":
                self.ai_providers["anthropic"] = AnthropicProvider(provider_config)
            elif provider_config.provider == "openai":
                self.ai_providers["openai"] = OpenAIProvider(provider_config)
        
        # Initialize phases
        default_ai = self.ai_providers[config.default_provider]
        self.specify = SpecifyPhase(default_ai)
        self.plan = PlanPhase(default_ai)
        self.tasks = TasksPhase(default_ai)
        self.implement = ImplementPhase(default_ai, config.workspace_dir)
    
    async def start(self):
        """Initialize"""
        self.config.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.config.artifacts_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Cynetics started")
    
    async def stop(self):
        """Cleanup"""
        logger.info("Cynetics stopped")
    
    async def run(
        self, 
        description: str, 
        tech_preferences: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Run complete workflow"""
        
        logger.info("=" * 70)
        logger.info("CYNETICS - Autonomous Coding Workflow")
        logger.info("=" * 70)
        
        # Phase 1: Specify
        logger.info("\n📋 Phase 1: Generating specification...")
        spec = await self.specify.generate_spec(description)
        self._save_artifact("specification.json", asdict(spec))
        logger.info(f"✓ Specification: {spec.problem_statement}")
        
        # Phase 2: Plan
        logger.info("\n🏗️  Phase 2: Creating technical plan...")
        plan = await self.plan.generate_plan(spec, tech_preferences)
        self._save_artifact("plan.json", asdict(plan))
        logger.info(f"✓ Plan: {plan.architecture}")
        
        # Phase 3: Tasks
        logger.info("\n📝 Phase 3: Breaking down into tasks...")
        task_list = await self.tasks.generate_tasks(spec, plan)
        self._save_artifact("tasks.json", [asdict(t) for t in task_list])
        logger.info(f"✓ Generated {len(task_list)} tasks")
        
        # Phase 4: Implement
        logger.info("\n⚙️  Phase 4: Implementing...")
        context = {"spec": asdict(spec), "plan": asdict(plan)}
        
        for i, task in enumerate(task_list, 1):
            logger.info(f"  [{i}/{len(task_list)}] {task.title}")
            result = await self.implement.implement_task(task, context)
            task.status = result["status"]
        
        logger.info("\n✅ Workflow complete!")
        
        return {
            "spec": spec,
            "plan": plan,
            "tasks": task_list
        }
    
    def _save_artifact(self, filename: str, data: Any):
        """Save artifact"""
        path = self.config.artifacts_dir / filename
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

# ============================================================================
# CLI Entry Point
# ============================================================================

async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Cynetics - Autonomous Coder")
    parser.add_argument("--init", action="store_true", help="Initialize config")
    parser.add_argument("--config", type=Path, default="cynetics.json")
    parser.add_argument("--description", type=str, help="Project description")
    parser.add_argument("--stack", type=str, help="Tech preferences (JSON)")
    
    args = parser.parse_args()
    
    if args.init:
        config = CyneticsConfig.create_default(Path.cwd())
        config_data = {
            "project_root": str(config.project_root),
            "workspace_dir": str(config.workspace_dir),
            "artifacts_dir": str(config.artifacts_dir),
            "default_provider": config.default_provider,
            "mcp_servers": [asdict(s) for s in config.mcp_servers],
            "ai_providers": [asdict(p) for p in config.ai_providers]
        }
        with open("cynetics.json", 'w') as f:
            json.dump(config_data, f, indent=2)
        print("✓ Created cynetics.json")
        return
    
    if not args.description:
        parser.print_help()
        return
    
    # Load config
    config = CyneticsConfig.load(args.config)
    
    # Parse tech preferences
    tech_prefs = json.loads(args.stack) if args.stack else None
    
    # Run
    cynetics = Cynetics(config)
    await cynetics.start()
    
    try:
        await cynetics.run(args.description, tech_prefs)
    finally:
        await cynetics.stop()

if __name__ == "__main__":
    asyncio.run(main())
