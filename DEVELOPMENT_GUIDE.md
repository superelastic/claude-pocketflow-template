# Development Guide

This document provides comprehensive guidelines for developing with the Claude PocketFlow Template.

## Getting Started

### Prerequisites

- Python 3.10+
- UV package manager
- Git

### Installation

```bash
git clone <your-repo>
cd claude-pocketflow-template
uv sync
```

### Development Setup

```bash
# Install pre-commit hooks
uv run pre-commit install

# Run tests
uv run pytest

# Format code
uv run ruff format .

# Type check
uv run pyright
```

## Project Structure

```
claude-pocketflow-template/
├── src/
│   ├── claude_pocketflow_template/    # Main package
│   ├── flows/                         # Flow implementations
│   ├── nodes/                         # Node implementations
│   └── utils/                         # Utility functions
├── tests/                             # Test suite
├── docs/                             # Documentation
├── planning/                         # Project planning files
└── agents/                           # Agent configurations
```

## Development Workflow

1. **Planning**: Define requirements in `docs/design.md`
2. **Implementation**: Create nodes and flows in `src/`
3. **Testing**: Write comprehensive tests in `tests/`
4. **Documentation**: Update relevant documentation

## PocketFlow Framework

### Nodes

Nodes are the building blocks of flows. Each node implements:

- `prep()`: Preparation and validation
- `exec()`: Main execution logic
- `post()`: Cleanup and finalization

### Flows

Flows orchestrate node execution with action-based transitions.

## Testing

We use pytest with asyncio support. Tests cover:

- Unit tests for individual nodes
- Integration tests for complete flows
- Configuration and setup validation

## Code Quality

- **Formatting**: Ruff (88 character line limit)
- **Type checking**: Pyright
- **Linting**: Ruff with comprehensive rule set
- **Pre-commit**: Automated formatting and linting

## Contributing

1. Follow the established patterns
2. Write tests for new functionality
3. Update documentation
4. Ensure all checks pass before committing
