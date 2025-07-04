# Developer Guide

This comprehensive guide explains how to build AI-powered applications using the claude-pocketflow-template.

## Overview

The claude-pocketflow-template provides a production-ready foundation for building AI applications with:

- **PocketFlow**: Node-based flow orchestration framework
- **Modern Python Tooling**: UV, Ruff, Pyright, pytest
- **AI-Assisted Development**: Optimized for Cursor AI and Claude Code
- **Comprehensive Testing**: 44+ tests with 88%+ coverage potential

## Getting Started

### Prerequisites

Before you begin, ensure you have:

- Python 3.10, 3.11, or 3.12 installed
- An Anthropic API key for Claude integration
- Basic familiarity with Python async/await

### Quick Setup

#### Running the Setup Script

**On Linux/Mac:**

```bash
# The script should already be executable, but if not:
chmod +x setup.sh

# Run the automated setup
./setup.sh
```

**On Windows (Git Bash/WSL):**

```bash
# In Git Bash or WSL
./setup.sh

# Or if you get permission errors:
bash setup.sh
```

**Alternative using Make:**

```bash
# If make is installed
make setup
```

**What the setup script does:**

1. Checks Python version (3.10+ required)
2. Installs UV package manager if needed
3. Creates virtual environment
4. Installs all dependencies
5. Sets up pre-commit hooks
6. Creates project structure
7. Runs initial code quality checks

**After setup, activate the virtual environment:**

```bash
# Linux/Mac
source .venv/bin/activate

# Windows Command Prompt
.venv\Scripts\activate.bat

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Git Bash on Windows
source .venv/Scripts/activate
```

## Project Structure

After running the setup script, you'll have the following structure automatically created:

### Core Components

```
src/claude_pocketflow_template/
├── __init__.py          # Package exports
├── __about__.py         # Version info
├── config.py            # Configuration management
└── daemon.py            # Flow orchestration daemon
```

**Note:** The setup script (`./setup.sh`) automatically creates this structure - you don't need to create these files manually. If any files are missing, simply run the setup script again.

### Configuration Management

The template uses Pydantic for robust configuration:

```python
from claude_pocketflow_template.config import Config

# Load from environment variables
config = Config()

# Or provide explicit values
config = Config(
    anthropic_api_key="sk-...",
    debug=True,
    log_level="DEBUG"
)
```

### Flow Daemon

The FlowDaemon manages your application's flows:

```python
from claude_pocketflow_template.daemon import FlowDaemon
from claude_pocketflow_template.config import Config

async def main():
    config = Config()
    daemon = FlowDaemon(config)

    # Add your flows
    daemon.add_flow("main_flow", my_flow)

    # Start the daemon
    await daemon.start()
```

## Creating Flows with PocketFlow

### Basic Flow Structure

```python
from pocketflow import Flow

# Define your flow
flow = Flow(
    name="example_flow",
    description="An example flow showing key concepts"
)

# Add nodes to your flow
flow.add_node("start", StartNode())
flow.add_node("process", ProcessNode())
flow.add_node("complete", CompleteNode())

# Define transitions
flow.add_edge("start", "process", condition="success")
flow.add_edge("process", "complete", condition="done")
flow.add_edge("process", "start", condition="retry")
```

### Node Implementation

Nodes in PocketFlow typically follow this pattern:

```python
from typing import Dict, Any
from pocketflow import Node

class ProcessNode(Node):
    """A node that processes data."""

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the node's logic."""
        try:
            # Your processing logic here
            result = await self.process_data(context["input"])

            return {
                "status": "success",
                "output": result,
                "next": "done"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "next": "retry"
            }

    async def process_data(self, data: Any) -> Any:
        """Process the input data."""
        # Implementation here
        return data
```

### (Example) Integrating with Claude

```python
from anthropic import AsyncAnthropic
from claude_pocketflow_template.config import Config

class ClaudeNode(Node):
    """A node that interacts with Claude."""

    def __init__(self, config: Config):
        self.client = AsyncAnthropic(api_key=config.anthropic_api_key)

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a response using Claude."""
        try:
            response = await self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": context["prompt"]
                }]
            )

            return {
                "status": "success",
                "response": response.content[0].text,
                "next": "continue"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "next": "error_handler"
            }
```

## Testing Your Application

### Writing Tests

The template includes comprehensive testing examples:

```python
import pytest
from claude_pocketflow_template.daemon import FlowDaemon
from claude_pocketflow_template.config import Config

@pytest.fixture
def test_config():
    """Create a test configuration."""
    return Config(
        anthropic_api_key="test_key",
        debug=True,
        log_level="DEBUG"
    )

@pytest.fixture
def flow_daemon(test_config):
    """Create a test daemon."""
    return FlowDaemon(test_config)

async def test_flow_execution(flow_daemon, mock_flow):
    """Test basic flow execution."""
    flow_daemon.add_flow("test_flow", mock_flow)

    # Your test logic here
    assert "test_flow" in flow_daemon.flows
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific tests
uv run pytest tests/test_flows.py -v

# Run tests matching a pattern
uv run pytest -k "config" -v
```

### Test Coverage

The template aims for high test coverage:

- Unit tests for individual components
- Integration tests for flow execution
- Edge case and error handling tests
- Performance and concurrency tests

## Development Workflow

### 1. Code Quality Tools

```bash
# Format your code
make format

# Check for linting issues
make lint

# Run type checking
make type-check

# Run all checks at once
make dev
```

### 2. Pre-commit Hooks

Pre-commit hooks run automatically on git commit:

- Code formatting with Ruff
- YAML/JSON formatting with Prettier
- File cleanup (trailing whitespace, EOF)

### 3. Continuous Integration

The GitHub Actions workflow:

- Tests on Python 3.10, 3.11, and 3.12
- Runs all quality checks
- Generates coverage reports
- Performs security scanning

## Best Practices

### 1. Configuration Management

- Use environment variables for sensitive data
- Provide sensible defaults
- Validate configuration early
- Use type hints for all config fields

### 2. Flow Design

- Keep nodes focused and single-purpose
- Use clear, descriptive node names
- Handle errors gracefully
- Log important state transitions

### 3. Testing Strategy

- Write tests alongside your code
- Test both success and failure paths
- Mock external services
- Use fixtures for common test data

### 4. Code Organization

```python
# Good: Focused, reusable nodes
class FetchDataNode(Node):
    """Fetches data from API."""
    pass

class ProcessDataNode(Node):
    """Processes fetched data."""
    pass

# Avoid: Monolithic nodes
class DoEverythingNode(Node):
    """Fetches, processes, and saves data."""
    pass
```

### 5. Error Handling

```python
async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute with proper error handling."""
    try:
        # Validate inputs
        if not context.get("input"):
            raise ValueError("Missing required input")

        # Process data
        result = await self.process(context["input"])

        return {
            "status": "success",
            "output": result
        }
    except ValueError as e:
        self.logger.warning(f"Validation error: {e}")
        return {"status": "validation_error", "error": str(e)}
    except Exception as e:
        self.logger.error(f"Unexpected error: {e}")
        return {"status": "error", "error": str(e)}
```

## Advanced Topics

### Async/Await Best Practices

```python
# Good: Concurrent execution
async def process_multiple(self, items: List[Any]) -> List[Any]:
    """Process multiple items concurrently."""
    tasks = [self.process_item(item) for item in items]
    return await asyncio.gather(*tasks)

# Avoid: Sequential execution
async def process_multiple_slow(self, items: List[Any]) -> List[Any]:
    """Process items one by one."""
    results = []
    for item in items:
        result = await self.process_item(item)
        results.append(result)
    return results
```

### Performance Optimization

- Use connection pooling for external services
- Implement caching where appropriate
- Monitor memory usage in long-running flows
- Use async operations for I/O-bound tasks

### Logging Best Practices

```python
from loguru import logger

class DataNode(Node):
    """Node with proper logging."""

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute with detailed logging."""
        logger.info(f"Starting {self.__class__.__name__}")
        logger.debug(f"Context keys: {list(context.keys())}")

        try:
            result = await self.process(context)
            logger.info(f"Successfully processed {len(result)} items")
            return {"status": "success", "output": result}
        except Exception as e:
            logger.error(f"Processing failed: {e}", exc_info=True)
            return {"status": "error", "error": str(e)}
```

## Deployment Considerations

### Environment Setup

```bash
# Production environment variables
export ANTHROPIC_API_KEY="your-production-key"
export DEBUG=false
export LOG_LEVEL=INFO
export FLOW_TIMEOUT=300
export MAX_RETRIES=3
export DATA_DIR=/var/app/data
export LOGS_DIR=/var/app/logs
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install UV
RUN pip install uv

# Copy files
COPY pyproject.toml .
COPY src/ src/

# Install dependencies
RUN uv pip install -e .
RUN pip install pocketflow

# Run the application
CMD ["python", "-m", "claude_pocketflow_template"]
```

### Monitoring and Observability

- Use structured logging with Loguru
- Implement health check endpoints
- Track flow execution metrics
- Monitor resource usage

## Troubleshooting

### Common Issues

**Import Errors**

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall in development mode
uv pip install -e ".[dev]"
```

**Type Checking Failures**

```bash
# Install type stubs
uv pip install types-requests types-aiofiles

# Run with more verbose output
uv run pyright --verbose
```

**Test Failures**

```bash
# Run tests with more detail
uv run pytest -vvs

# Run specific test with debugging
uv run pytest tests/test_flows.py::TestFlowExecution -vvs
```

## Next Steps

1. **Explore the Test Suite**: Review `tests/` for comprehensive examples
2. **Build Your First Flow**: Start with a simple flow and iterate
3. **Integrate External Services**: Add API clients in the utils directory
4. **Customize Configuration**: Extend the Config class for your needs
5. **Deploy Your Application**: Use the CI/CD pipeline for deployment

## Additional Resources

- [PocketFlow Documentation](https://pocketflow.readthedocs.io/)
- [Anthropic API Reference](https://docs.anthropic.com/)
- [Python Async/Await Guide](https://docs.python.org/3/library/asyncio.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## Getting Help

- Review the comprehensive test suite for examples
- Check the [Architecture Guide](architecture.md) for design patterns
- Consult the [API Reference](api-reference.md) for detailed documentation
- Use AI assistants with the provided CLAUDE.md instructions
