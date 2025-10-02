# Contributing to Cynetics

Thank you for your interest in contributing to Cynetics! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/cynetics.git
   cd cynetics
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   make install
   ```

## Development Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Run tests:
   ```bash
   make test
   ```

4. Run linting:
   ```bash
   make lint
   ```

5. Format code:
   ```bash
   make format
   ```

6. Commit your changes:
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

8. Create a Pull Request

## Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting
- Use type hints where possible
- Write docstrings for all functions and classes
- Keep functions small and focused

### Example

```python
async def process_task(task: Task, context: Dict[str, Any]) -> TaskResult:
    """
    Process a single task with given context.
    
    Args:
        task: The task to process
        context: Execution context with spec and plan
        
    Returns:
        TaskResult with status and output
        
    Raises:
        TaskExecutionError: If task processing fails
    """
    # Implementation
    pass
```

## Testing

- Write tests for all new features
- Maintain test coverage above 80%
- Use pytest for testing
- Use async tests for async code

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_cynetics.py

# Run with coverage
pytest --cov=. --cov-report=html

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

## Documentation

- Update README.md if adding features
- Add docstrings to all public functions
- Update docs/ for significant changes
- Include examples in docstrings

## Pull Request Guidelines

### PR Title Format

```
[Type] Brief description

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- test: Test additions/changes
- refactor: Code refactoring
- chore: Maintenance tasks
```

### PR Description Template

```markdown
## Description
Brief description of changes

## Changes Made
- Change 1
- Change 2

## Testing
How the changes were tested

## Checklist
- [ ] Tests pass
- [ ] Code is formatted
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## Adding New Features

### 1. AI Providers

To add a new AI provider:

```python
class NewProvider(AIProvider):
    """New AI provider implementation"""
    
    def __init__(self, config: AIProviderConfig):
        self.config = config
        # Initialize provider client
    
    async def generate(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate completion from messages"""
        # Implementation
        pass
```

Add to `cynetics.py` in the Cynetics class:

```python
elif provider_config.provider == "newprovider":
    self.ai_providers["newprovider"] = NewProvider(provider_config)
```

### 2. MCP Servers

To add a custom MCP server:

1. Create the server following MCP protocol
2. Add configuration to `cynetics.json`:
   ```json
   {
     "name": "custom-server",
     "command": "node",
     "args": ["path/to/server.js"],
     "enabled": true
   }
   ```

### 3. Phases

To extend a phase:

```python
class CustomPhase:
    """Custom workflow phase"""
    
    def __init__(self, ai_provider: AIProvider):
        self.ai = ai_provider
    
    async def execute(self, input_data: Any) -> Any:
        """Execute phase logic"""
        # Implementation
        pass
```

## Commit Message Guidelines

Use conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Examples

```
feat(specify): add support for multi-language specs

Added ability to generate specifications in multiple languages
using the --language flag.

Closes #123
```

```
fix(implement): handle timeout errors correctly

Tasks would fail silently on timeout. Now properly catch and
retry with exponential backoff.

Fixes #456
```

## Release Process

Maintainers only:

1. Update version in `setup.py`
2. Update CHANGELOG.md
3. Create git tag:
   ```bash
   git tag -a v1.0.0 -m "Release 1.0.0"
   git push origin v1.0.0
   ```
4. GitHub Actions will build and publish

## Getting Help

- GitHub Discussions: For questions and discussions
- GitHub Issues: For bugs and feature requests
- Discord: For real-time chat

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
