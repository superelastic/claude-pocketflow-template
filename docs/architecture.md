# System Architecture

## Overview

The claude-pocketflow-template implements a modern, production-ready architecture for building AI-powered applications with PocketFlow and Claude. The system emphasizes modularity, testability, and developer experience.

## Core Architecture

### Technology Stack

- **Runtime**: Python 3.10+ with async/await support
- **Framework**: PocketFlow for flow orchestration
- **AI Integration**: Anthropic Claude API
- **Configuration**: Pydantic for type-safe config management
- **Testing**: Pytest with 88%+ coverage
- **Tooling**: UV, Ruff, Pyright, Pre-commit

### Project Structure

```
claude-pocketflow-template/
├── src/
│   └── claude_pocketflow_template/
│       ├── __init__.py          # Package exports
│       ├── __about__.py         # Version management
│       ├── config.py            # Pydantic configuration
│       └── daemon.py            # Flow orchestration daemon
├── tests/                       # Comprehensive test suite
│   ├── conftest.py             # Shared fixtures
│   ├── test_config.py          # Config tests
│   ├── test_daemon.py          # Daemon tests
│   └── test_flows.py           # Integration tests
└── Infrastructure/
    ├── pyproject.toml          # Project metadata
    ├── Makefile                # Developer commands
    └── .github/workflows/      # CI/CD pipelines
```

## Design Principles

### 1. Configuration-Driven

All application behavior is controlled through configuration:

```python
config = Config(
    anthropic_api_key="...",
    flow_timeout=300,
    max_retries=3
)
```

### 2. Async-First

Built on Python's asyncio for efficient I/O operations:

```python
async def main():
    daemon = FlowDaemon(config)
    await daemon.start()
```

### 3. Type Safety

Full type hints with Pyright validation:

```python
def add_flow(self, name: str, flow: Flow) -> None:
    """Type-safe flow management."""
```

### 4. Test-Driven

Comprehensive test coverage from the start:

- Unit tests for components
- Integration tests for flows
- Performance tests for scalability
- Edge case coverage

## Component Architecture

### Configuration Layer

```
┌─────────────────────────────────────┐
│         Config (Pydantic)           │
├─────────────────────────────────────┤
│  - Environment variables            │
│  - Type validation                  │
│  - Default values                   │
│  - Directory management             │
└─────────────────────────────────────┘
```

The Config class provides:

- Environment variable loading
- Type-safe configuration
- Automatic directory creation
- Validation at startup

### Flow Daemon

```
┌─────────────────────────────────────┐
│           FlowDaemon                │
├─────────────────────────────────────┤
│  - Flow lifecycle management        │
│  - Concurrent flow execution        │
│  - Error handling & recovery        │
│  - Graceful shutdown                │
└─────────────────────────────────────┘
```

The daemon manages:

- Multiple flow instances
- Flow initialization
- Lifecycle events
- Resource cleanup

### PocketFlow Integration

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Node A    │────▶│   Node B    │────▶│   Node C    │
└─────────────┘     └─────────────┘     └─────────────┘
       │                    │                    │
       └────────────────────┴────────────────────┘
                     Context Store
```

Flows consist of:

- **Nodes**: Individual processing units
- **Edges**: Conditional transitions
- **Context**: Shared state dictionary

### Node Architecture

```python
class ProcessNode(Node):
    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Input validation
        # Processing logic
        # Output formatting
        return {"status": "success", "next": "continue"}
```

## Data Flow Patterns

### Request Processing

```
Request → Validation → Processing → Response
           ↓             ↓           ↓
         Error       Retry       Success
```

### Error Handling

```
Try Operation → Success → Continue
      ↓
    Failure → Retry (with backoff)
      ↓
  Max Retries → Error Handler → Notification
```

### State Management

Context flows through nodes carrying:

- Input data
- Processing results
- Error information
- Metadata (timestamps, retries)

## Integration Patterns

### Claude Integration

```python
class ClaudeNode(Node):
    def __init__(self, config: Config):
        self.client = AsyncAnthropic(
            api_key=config.anthropic_api_key
        )

    async def run(self, context):
        response = await self.client.messages.create(...)
        return {"response": response.content}
```

### External Services

- Use async HTTP clients (httpx)
- Implement connection pooling
- Add retry logic
- Handle timeouts gracefully

## Testing Architecture

### Test Pyramid

```
        ┌───────────┐
       │ E2E Tests  │     (Few)
      ┌─────────────┐
     │ Integration  │     (Some)
    ┌───────────────┐
   │  Unit Tests    │     (Many)
   └───────────────┘
```

### Test Organization

- **Unit Tests**: Individual components
- **Integration Tests**: Flow execution
- **Performance Tests**: Concurrency, memory
- **Edge Cases**: Error conditions

### Test Infrastructure

```python
@pytest.fixture
def test_config():
    """Isolated test configuration."""
    return Config(anthropic_api_key="test")

@pytest.fixture
async def flow_daemon(test_config):
    """Test daemon with cleanup."""
    daemon = FlowDaemon(test_config)
    yield daemon
    await daemon.stop()
```

## Performance Considerations

### Async Optimization

- Concurrent node execution where possible
- Non-blocking I/O operations
- Connection pooling for external services
- Efficient context passing

### Memory Management

- Stream large data instead of loading
- Clear unused context keys
- Implement pagination for large results
- Monitor memory usage in long-running flows

### Scalability Patterns

- Horizontal scaling through multiple daemons
- Flow partitioning by type/priority
- Distributed state management (future)
- Queue-based flow triggering (future)

## Security Architecture

### Configuration Security

- API keys from environment only
- No secrets in code or logs
- Secure defaults
- Input validation

### Runtime Security

- Type checking at boundaries
- Sanitize user inputs
- Audit logging
- Error message sanitization

## Monitoring & Observability

### Logging Strategy

```python
logger.info("Flow started", flow_id=flow_id)
logger.error("Node failed", error=str(e), node=node_name)
```

### Metrics Collection

- Flow execution time
- Node success/failure rates
- API call latency
- Resource utilization

### Health Checks

- Daemon status endpoint
- Flow health monitoring
- External service connectivity
- Resource availability

## Development Workflow

### Local Development

```bash
# Setup environment
./setup.sh

# Run tests
make test

# Check code quality
make dev

# Start application
python -m claude_pocketflow_template
```

### CI/CD Pipeline

1. Pre-commit hooks (local)
2. GitHub Actions (PR validation)
3. Multi-version testing (3.10, 3.11, 3.12)
4. Security scanning
5. Coverage reporting

### Deployment Options

- Direct Python execution
- Docker containers
- Kubernetes pods
- Serverless functions (with modifications)

## Future Architecture Considerations

### Planned Enhancements

- WebSocket support for real-time flows
- Flow visualization dashboard
- Distributed flow execution
- Plugin system for custom nodes

### Extensibility Points

- Custom node types
- Flow middleware
- Context transformers
- Result exporters

## Best Practices

### Code Organization

- One node per file for complex nodes
- Group related utilities
- Consistent naming patterns
- Clear module boundaries

### Error Handling

- Fail fast with clear errors
- Provide actionable error messages
- Log errors with context
- Implement circuit breakers

### Performance

- Profile before optimizing
- Use async for I/O operations
- Cache expensive computations
- Monitor resource usage

This architecture provides a solid foundation for building scalable, maintainable AI applications while remaining flexible enough to adapt to changing requirements.
