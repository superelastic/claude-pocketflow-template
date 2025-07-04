# API Reference

Complete API documentation for the claude-pocketflow-template components.

## Core Components

### Config Class

Configuration management with environment variable support.

```python
from claude_pocketflow_template.config import Config

# Create with defaults from environment
config = Config()

# Or with explicit values
config = Config(
    anthropic_api_key="sk-...",
    debug=True,
    log_level="DEBUG",
    flow_timeout=600,
    max_retries=5,
    data_dir=Path("/custom/data"),
    logs_dir=Path("/custom/logs")
)
```

**Properties:**

- `anthropic_api_key` (str): API key for Anthropic Claude
- `debug` (bool): Enable debug mode (default: False)
- `log_level` (str): Logging level (default: "INFO")
- `flow_timeout` (int): Timeout for flow execution in seconds (default: 300)
- `max_retries` (int): Maximum retry attempts (default: 3)
- `data_dir` (Path): Directory for data storage (default: "data")
- `logs_dir` (Path): Directory for logs (default: "logs")

**Environment Variables:**

- `ANTHROPIC_API_KEY`: Set API key
- `DEBUG`: Enable debug mode ("true"/"false")
- `LOG_LEVEL`: Set log level
- `FLOW_TIMEOUT`: Flow timeout in seconds
- `MAX_RETRIES`: Max retry attempts
- `DATA_DIR`: Data directory path
- `LOGS_DIR`: Logs directory path

### FlowDaemon Class

Manages the lifecycle of multiple flows.

```python
from claude_pocketflow_template.daemon import FlowDaemon

daemon = FlowDaemon(config)

# Add flows
daemon.add_flow("main_flow", flow_instance)
daemon.add_flow("secondary_flow", another_flow)

# Start daemon
await daemon.start()

# Stop daemon
await daemon.stop()
```

**Methods:**

#### `__init__(config: Config)`

Initialize the daemon with configuration.

#### `add_flow(name: str, flow: Flow) -> None`

Add a flow to the daemon.

- `name`: Unique identifier for the flow
- `flow`: PocketFlow Flow instance

#### `remove_flow(name: str) -> Optional[Flow]`

Remove and return a flow from the daemon.

- Returns: The removed flow or None if not found

#### `async start() -> None`

Start the daemon and initialize all flows.

#### `async stop() -> None`

Stop the daemon and clean up resources.

## PocketFlow Integration

### Creating Nodes

Basic node structure for PocketFlow:

```python
from pocketflow import Node
from typing import Dict, Any

class CustomNode(Node):
    """Custom node implementation."""

    def __init__(self, config: Config):
        self.config = config
        self.logger = logger.bind(node=self.__class__.__name__)

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute node logic."""
        try:
            # Validate inputs
            self._validate_inputs(context)

            # Process data
            result = await self._process(context)

            # Return success
            return {
                "status": "success",
                "output": result,
                "next": "continue"
            }
        except ValidationError as e:
            return {
                "status": "validation_error",
                "error": str(e),
                "next": "error_handler"
            }
        except Exception as e:
            self.logger.error(f"Node failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "next": "retry"
            }
```

### Flow Definition

Create flows with nodes and transitions:

```python
from pocketflow import Flow

# Create flow
flow = Flow(
    name="example_flow",
    description="Example flow with error handling"
)

# Add nodes
flow.add_node("start", StartNode(config))
flow.add_node("process", ProcessNode(config))
flow.add_node("error_handler", ErrorHandlerNode(config))
flow.add_node("complete", CompleteNode(config))

# Define transitions
flow.add_edge("start", "process", condition="success")
flow.add_edge("process", "complete", condition="success")
flow.add_edge("process", "error_handler", condition="error")
flow.add_edge("error_handler", "process", condition="retry")
flow.add_edge("error_handler", "complete", condition="skip")
```

### Context Management

The context dictionary passed between nodes:

```python
context = {
    # Input data
    "input": {...},

    # Node results
    "node_name": {
        "status": "success",
        "output": {...},
        "timestamp": "2024-01-01T12:00:00Z"
    },

    # Flow metadata
    "_flow_id": "unique-flow-id",
    "_start_time": datetime.now(),
    "_retries": {"node_name": 0}
}
```

## Testing Utilities

### Fixtures

```python
@pytest.fixture
def test_config():
    """Test configuration."""
    return Config(
        anthropic_api_key="test_key",
        debug=True,
        log_level="DEBUG"
    )

@pytest.fixture
def mock_flow():
    """Mock flow for testing."""
    flow = MagicMock(spec=Flow)
    flow.run = AsyncMock()
    return flow

@pytest.fixture
async def daemon_with_flow(test_config, mock_flow):
    """Daemon with a test flow."""
    daemon = FlowDaemon(test_config)
    daemon.add_flow("test_flow", mock_flow)
    yield daemon
    await daemon.stop()
```

### Test Patterns

```python
# Test node execution
async def test_node_success():
    node = CustomNode(config)
    context = {"input": "test_data"}

    result = await node.run(context)

    assert result["status"] == "success"
    assert "output" in result

# Test error handling
async def test_node_error():
    node = CustomNode(config)
    context = {}  # Missing required input

    result = await node.run(context)

    assert result["status"] == "validation_error"
    assert "error" in result

# Test flow execution
async def test_flow_execution(daemon_with_flow):
    await daemon_with_flow.start()

    # Flow should be initialized
    assert "test_flow" in daemon_with_flow.flows
```

## Logging

The template uses Loguru for structured logging:

```python
from loguru import logger

# Configure logging
logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="1 week",
    level=config.log_level
)

# Use in nodes
logger.info("Processing started", node="CustomNode", input_size=len(data))
logger.error("Processing failed", error=str(e), node="CustomNode")
```

## Error Handling

### Standard Error Response

```python
{
    "status": "error",
    "error": "Descriptive error message",
    "error_type": "ValidationError",
    "node": "ProcessNode",
    "timestamp": "2024-01-01T12:00:00Z",
    "next": "error_handler"
}
```

### Retry Logic

```python
class RetryableNode(Node):
    """Node with retry capability."""

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        retries = context.get("_retries", {}).get(self.name, 0)

        if retries >= self.config.max_retries:
            return {
                "status": "max_retries_exceeded",
                "error": f"Failed after {retries} attempts",
                "next": "error_handler"
            }

        try:
            result = await self._attempt_operation()
            return {"status": "success", "output": result}
        except Exception as e:
            context["_retries"][self.name] = retries + 1
            return {
                "status": "retry",
                "error": str(e),
                "attempt": retries + 1,
                "next": "retry"
            }
```

## Performance Optimization

### Async Best Practices

```python
# Concurrent operations
async def process_batch(items: List[Any]) -> List[Any]:
    """Process items concurrently."""
    async def process_item(item):
        # Process individual item
        return await some_async_operation(item)

    # Process all items concurrently
    tasks = [process_item(item) for item in items]
    return await asyncio.gather(*tasks)

# Connection pooling
class APINode(Node):
    """Node with connection pooling."""

    def __init__(self, config: Config):
        self.config = config
        self.client = httpx.AsyncClient(
            limits=httpx.Limits(max_connections=10),
            timeout=httpx.Timeout(30.0)
        )

    async def cleanup(self):
        """Clean up resources."""
        await self.client.aclose()
```

### Memory Management

```python
# Stream large data
async def process_large_file(file_path: Path):
    """Process large file in chunks."""
    async with aiofiles.open(file_path, 'r') as f:
        async for chunk in f:
            # Process chunk
            yield process_chunk(chunk)

# Clear large objects
def clear_context(context: Dict[str, Any]) -> Dict[str, Any]:
    """Remove large objects from context."""
    keys_to_clear = ["large_data", "temp_results"]
    for key in keys_to_clear:
        context.pop(key, None)
    return context
```

## Type Definitions

Common type definitions used throughout the template:

```python
from typing import TypedDict, Literal, Optional

class NodeResult(TypedDict):
    """Standard node result structure."""
    status: Literal["success", "error", "retry", "skip"]
    output: Optional[Any]
    error: Optional[str]
    next: Optional[str]

class FlowContext(TypedDict, total=False):
    """Flow execution context."""
    input: Any
    _flow_id: str
    _start_time: datetime
    _retries: Dict[str, int]
    _metadata: Dict[str, Any]
```

## Environment Setup

### Development Environment

```bash
# Install with all development dependencies
uv pip install -e ".[dev]"

# Run development server with hot reload
uv run python -m claude_pocketflow_template --debug --reload
```

### Production Environment

```bash
# Install production dependencies only
uv pip install -e .

# Run with production settings
python -m claude_pocketflow_template
```

## Version Information

Access version information:

```python
from claude_pocketflow_template import __version__

print(f"Version: {__version__}")
```
