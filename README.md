# claude-pocketflow-template

A production-ready template for building AI-powered applications with PocketFlow and Claude. Features comprehensive testing, modern Python tooling, and AI-assisted development support.

## 🚀 Use This Template

Click the "Use this template" button above to create a new repository based on this template.

## ✨ Features

- **🧪 Comprehensive Testing**: 44+ tests with pytest, achieving 88%+ coverage
- **🔧 Modern Python Tooling**: UV package manager, Ruff formatter, Pyright type checker
- **🤖 AI Development Ready**: Optimized for Cursor AI and Claude Code
- **📦 Production Ready**: Pre-commit hooks, GitHub Actions CI/CD, structured logging
- **🏗️ Clean Architecture**: Modular design with config management and flow orchestration
- **📚 Extensive Documentation**: For both human developers and AI assistants

## Quick Start

### Prerequisites

- Python 3.10+ (3.10, 3.11, or 3.12 supported)
- UV package manager (installs automatically with setup script)
- Anthropic API key for Claude integration

### One-Command Setup

```bash
# Clone your repository (after using template)
git clone <your-new-repository-url>
cd your-project-name

# Make setup script executable (if needed)
chmod +x setup.sh

# Run the automated setup
./setup.sh

# Or on Windows/if you get permission errors:
bash setup.sh
```

The setup script will:

- ✅ Check Python version compatibility
- ✅ Install UV package manager if needed
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Set up pre-commit hooks
- ✅ Create project structure
- ✅ Run initial code quality checks

### Manual Setup (Alternative)

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e ".[dev]"
pip install pocketflow

# Set up environment
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY

# Install pre-commit hooks
uv run pre-commit install
```

## 🛠️ Development

### Using the Makefile

```bash
make help        # Show all available commands
make test        # Run tests
make test-cov    # Run tests with coverage report
make format      # Format code with ruff
make lint        # Check code style
make type-check  # Run type checking
make dev         # Run all checks (format, lint, type-check, test)
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=claude_pocketflow_template --cov-report=html

# Run specific test file
uv run pytest tests/test_flows.py

# Run tests matching pattern
uv run pytest -k "test_config"
```

### Code Quality Tools

```bash
# Format code
uv run ruff format .

# Fix linting issues
uv run ruff check . --fix

# Type checking
uv run pyright

# Run pre-commit on all files
uv run pre-commit run --all-files
```

## 📁 Project Structure

```
claude-pocketflow-template/
├── src/
│   └── claude_pocketflow_template/
│       ├── __init__.py          # Package initialization
│       ├── __about__.py         # Version information
│       ├── config.py            # Configuration management
│       └── daemon.py            # Flow daemon orchestration
├── tests/                       # Comprehensive test suite
│   ├── conftest.py             # Pytest configuration
│   ├── test_config.py          # Configuration tests
│   ├── test_daemon.py          # Daemon tests
│   └── test_flows.py           # Flow integration tests
├── docs/                        # Documentation
│   ├── developer-guide.md      # Development guide
│   ├── architecture.md         # System architecture
│   ├── api-reference.md        # API documentation
│   ├── design.md               # Product design
│   └── flow-design.md          # Flow patterns
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD
├── .mdc/                        # Cursor-specific rules
├── CLAUDE.md                    # AI assistant instructions
├── pyproject.toml              # Project configuration
├── Makefile                    # Development commands
├── setup.sh                    # Automated setup script
└── .pre-commit-config.yaml     # Pre-commit hooks
```

## 📚 Documentation

### For Developers

- **[Developer Guide](docs/developer-guide.md)** - Complete guide to building with this template
- **[Architecture](docs/architecture.md)** - System design, patterns, and best practices
- **[API Reference](docs/api-reference.md)** - Detailed API documentation
- **[Flow Design](docs/flow-design.md)** - PocketFlow patterns and examples

### For AI Assistants

- **[CLAUDE.md](CLAUDE.md)** - Instructions for Claude Code and AI assistants
- **[.cursorrules](.cursorrules)** - Cursor AI IDE integration rules
- **[.mdc/](.mdc/)** - Framework-specific patterns and guidelines

## 🤖 AI-Assisted Development

This template is optimized for AI-powered development:

### Cursor AI Integration

- Custom rules in `.cursorrules` for project-specific assistance
- Framework patterns in `.mdc/` directory
- Automatic code formatting and linting

### Claude Code Support

- Comprehensive `CLAUDE.md` with project guidelines
- Test-driven development patterns
- Clear documentation structure

### Development Workflow

1. Use Cursor AI for code generation with project rules
2. Run `make dev` to ensure code quality
3. Use Claude Code for complex refactoring
4. Commit with conventional commit messages

## 🧪 Testing Strategy

The template includes a comprehensive test suite:

- **Unit Tests**: Config management, daemon lifecycle
- **Integration Tests**: Flow execution, error handling
- **Performance Tests**: Concurrent operations, memory usage
- **Edge Cases**: Error conditions, boundary testing

Run tests with coverage:

```bash
make test-cov
# Opens HTML coverage report in browser
```

## 🚢 Deployment

### GitHub Actions CI/CD

The template includes a complete CI/CD pipeline that:

- Runs on Python 3.10, 3.11, and 3.12
- Executes all tests with coverage reporting
- Performs security scanning with pip-audit
- Enforces code quality with pre-commit hooks

### Environment Variables

Configure your deployment environment:

```bash
ANTHROPIC_API_KEY=your_api_key_here
DEBUG=false
LOG_LEVEL=INFO
FLOW_TIMEOUT=300
MAX_RETRIES=3
DATA_DIR=/path/to/data
LOGS_DIR=/path/to/logs
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Run `make dev` to ensure code quality
4. Commit your changes (following conventional commits)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Development Guidelines

- Write tests for new features
- Update documentation as needed
- Follow the code style (enforced by Ruff)
- Ensure type hints are complete (checked by Pyright)

## 📈 Roadmap

- [ ] Add more flow examples
- [ ] Implement flow visualization
- [ ] Add performance monitoring
- [ ] Create flow testing utilities
- [ ] Add deployment templates (Docker, K8s)

## 🆘 Troubleshooting

### Common Issues

**UV Installation Fails**

```bash
# Try installing with pip instead
pip install uv
```

**Import Errors**

```bash
# Ensure you're in the virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

**Type Checking Errors**

```bash
# Update type stubs
uv pip install types-requests types-pyyaml
```

### Getting Help

- Check the [Developer Guide](docs/developer-guide.md)
- Review the test files for usage examples
- Open an issue for bugs or feature requests

## 📄 License

This template is provided as-is for use in your projects. Add your preferred license here.
