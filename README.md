# claude-pocketflow-template

A **solo developer-friendly** template for building AI-powered applications with PocketFlow and Claude. Features pragmatic tooling that helps without hindering your development flow.

> 🎯 **Philosophy**: Tools should help you build features, not fight you over formatting. This template uses a "minimal CI" approach - quality tools when you want them, never blocking your progress.

## 🚀 Use This Template

Click the "Use this template" button above to create a new repository based on this template.

**📖 New to this approach?** See **[DEVELOPMENT.md](DEVELOPMENT.md)** for the complete solo developer workflow.

## ✨ Features

- **🚀 Solo Dev Optimized**: Tools help instead of block - no CI fatigue!
- **🧪 Smart Testing**: Core functionality tests, skips brittle checks
- **🔧 Pragmatic Tooling**: Ruff, Pyright, pytest - all advisory, never blocking
- **🤖 AI Development Ready**: Optimized for Cursor AI and Claude Code
- **⚡ Fast Iteration**: Pre-commit hooks auto-fix but won't fail commits
- **📚 Clear Documentation**: Both technical docs and pragmatic workflow guides

## Quick Start

### Prerequisites

- Python 3.10+
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

See **[DEVELOPMENT.md](DEVELOPMENT.md)** for the complete solo developer workflow.

### Quick Commands

```bash
# Core development (nothing blocks you)
pytest                           # Run core tests
git commit -m "Working feature"  # Auto-formatting, never fails

# Optional quality tools (use when you want)
make -f Makefile.dev help        # See all available commands
make -f Makefile.dev format      # Format code
make -f Makefile.dev check       # All quality checks (warnings only)
```

### Testing Philosophy

This template uses **pragmatic testing** - core functionality is thoroughly tested, but brittle checks (like exact directory structure) are skipped to avoid CI fatigue.

```bash
# Run core tests (skips brittle ones automatically)
pytest

# Run all tests including skipped ones
pytest --run-skipped

# Coverage is optional, not required
pytest --cov=claude_pocketflow_template --cov-report=html
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

1. Write code - tools help, never block
2. `git commit` - pre-commit auto-fixes style but won't fail
3. `git push` - CI runs essential checks, reports warnings only
4. Use quality tools when you want: `make -f Makefile.dev check`

See **[DEVELOPMENT.md](DEVELOPMENT.md)** for the complete workflow.

## 🧪 Testing Strategy

**Pragmatic testing** - focuses on functionality over perfection:

- **Core Tests**: Config, flows, nodes - the stuff that matters
- **Integration Tests**: Real workflows and error handling
- **Skipped Tests**: Brittle filesystem/structure checks
- **Optional Coverage**: Available but not required

Tests run fast and focus on catching real bugs, not enforcing arbitrary standards.

## 🚢 Deployment

### GitHub Actions CI/CD

**Solo developer-friendly CI** that helps without hindering:

- Runs essential tests on Python 3.10
- Reports style/type issues as warnings (doesn't fail builds)
- Skips brittle checks that cause CI fatigue
- Focuses on functional correctness over perfect compliance

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

**Streamlined process for solo or collaborative development:**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write code - tools help, don't worry about perfect style
4. `git commit` - pre-commit auto-fixes issues but won't block
5. Push to branch - CI reports issues but doesn't fail builds
6. Open a Pull Request

### Development Guidelines

- **Focus on functionality** - tools handle style automatically
- **Test important features** - but don't obsess over coverage
- **Use quality tools when helpful** - `make -f Makefile.dev check`
- **Iterate fast** - commit early, refine later

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
