# Claude PocketFlow Template - Usage Guide

## 🚀 Quick Start

This template provides a production-ready foundation for building AI-powered applications with PocketFlow and Claude.

### Using This Template

1. **Create Your Repository**
   - Click the "Use this template" button on GitHub
   - Name your new repository
   - Choose public or private visibility

2. **Clone and Setup**

   ```bash
   git clone <your-new-repository-url>
   cd <your-repository-name>

   # Make setup script executable (Linux/Mac)
   chmod +x setup.sh

   # Run setup
   ./setup.sh

   # Or on Windows/if permission issues:
   bash setup.sh
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your ANTHROPIC_API_KEY
   ```

## ✅ What's Included

### Core Features

- **🏗️ Project Structure**: Pre-configured Python package with src layout
- **🧪 Testing Suite**: 44+ tests with pytest, achieving 88%+ coverage
- **🔧 Modern Tooling**: UV, Ruff, Pyright, pre-commit hooks
- **🤖 AI Integration**: Claude API integration ready
- **📦 CI/CD Pipeline**: GitHub Actions for automated testing
- **📚 Documentation**: Comprehensive docs for humans and AI

### Development Tools

- **Makefile**: Common commands (`make test`, `make dev`, etc.)
- **Setup Script**: One-command project initialization
- **Pre-commit Hooks**: Automatic code quality checks
- **Type Checking**: Full type hints with Pyright

## 📝 Customization Checklist

After creating your repository from this template:

### Essential Updates

- [ ] Update `pyproject.toml`:
  - [ ] Change `name` from "claude-pocketflow-template"
  - [ ] Update `description`
  - [ ] Modify `authors` with your information
  - [ ] Update repository URLs
- [ ] Update `README.md`:
  - [ ] Replace template content with your project description
  - [ ] Update badges if using
  - [ ] Add your specific installation instructions
- [ ] Configure `.env`:
  - [ ] Add your `ANTHROPIC_API_KEY`
  - [ ] Set any project-specific environment variables

### Code Customization

- [ ] Rename the package:

  ```bash
  # Rename src/claude_pocketflow_template to your package name
  mv src/claude_pocketflow_template src/your_package_name

  # Update imports in tests
  find tests -type f -name "*.py" -exec sed -i 's/claude_pocketflow_template/your_package_name/g' {} +
  ```

- [ ] Create your first flow:
  - [ ] Add nodes in `src/your_package_name/nodes.py`
  - [ ] Define flow in `src/your_package_name/flows.py`
  - [ ] Update daemon initialization
- [ ] Add your dependencies:
  ```bash
  uv add your-required-package
  ```

### Documentation Updates

- [ ] Update `docs/design.md` with your product requirements
- [ ] Modify `CLAUDE.md` with project-specific AI instructions
- [ ] Update `.cursorrules` for your coding standards
- [ ] Customize `docs/developer-guide.md` for your workflows

## 🏃 Development Workflow

### 1. Initial Development

```bash
# Activate virtual environment
source .venv/bin/activate

# Start with the example structure
cd src/your_package_name/

# Create your first node
touch nodes/my_first_node.py
```

### 2. Test-Driven Development

```bash
# Write test first
touch tests/test_my_first_node.py

# Run tests continuously
make test

# Check coverage
make test-cov
```

### 3. Code Quality

```bash
# Before committing, run all checks
make dev

# Or individually:
make format      # Format code
make lint        # Check style
make type-check  # Verify types
```

## 🔧 Configuration Options

### Environment Variables

The template supports these configuration options:

- `ANTHROPIC_API_KEY`: Your Claude API key (required)
- `DEBUG`: Enable debug logging (true/false)
- `LOG_LEVEL`: Logging verbosity (DEBUG/INFO/WARNING/ERROR)
- `FLOW_TIMEOUT`: Maximum flow execution time in seconds
- `MAX_RETRIES`: Retry attempts for failed operations
- `DATA_DIR`: Directory for data storage
- `LOGS_DIR`: Directory for log files

### Adding New Configuration

1. Update `src/your_package_name/config.py`:

```python
class Config(BaseSettings):
    # Add your new config field
    my_new_setting: str = Field("default_value", env="MY_NEW_SETTING")
```

2. Update `.env.example` with the new variable
3. Document in `docs/api-reference.md`

## 🚀 Deployment Preparation

### Before deploying:

- [ ] Update `LICENSE` file with your chosen license
- [ ] Review and update security settings
- [ ] Configure production environment variables
- [ ] Set up monitoring and logging
- [ ] Create deployment documentation

### Docker Support (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install uv
COPY pyproject.toml .
COPY src/ src/
RUN uv pip install -e .
RUN pip install pocketflow
CMD ["python", "-m", "your_package_name"]
```

## 🤝 Contributing to Your Project

Set up contribution guidelines:

1. Create `CONTRIBUTING.md`
2. Define code review process
3. Set up issue templates
4. Configure PR templates

## 📚 Learning Resources

### PocketFlow Development

- Review example flows in `tests/test_flows.py`
- Study the FlowDaemon pattern in `src/claude_pocketflow_template/daemon.py`
- Check PocketFlow documentation for advanced patterns

### AI-Assisted Development

- Use Cursor AI with the included `.cursorrules`
- Leverage Claude Code with `CLAUDE.md` instructions
- Follow test-driven development for best results

## 🆘 Troubleshooting

### Common Issues

**Module Import Errors**

```bash
# Ensure you're in virtual environment
which python  # Should show .venv/bin/python

# Reinstall in development mode
uv pip install -e ".[dev]"
```

**Test Discovery Issues**

```bash
# Run from project root
python -m pytest tests/

# Or use make
make test
```

**Type Checking Errors**

```bash
# Install missing type stubs
uv pip install types-requests

# Ignore specific files if needed
# Add to pyproject.toml [tool.pyright] exclude
```

## 🎯 Next Steps

1. **Build Your First Flow**: Start with a simple flow to understand the pattern
2. **Add External Integrations**: Create utility classes for APIs you need
3. **Expand Test Coverage**: Aim for 90%+ coverage
4. **Set Up CI/CD**: Customize GitHub Actions for your deployment needs
5. **Create Documentation**: Document your specific flows and APIs

## 📞 Support

- **Template Issues**: Open an issue in the original template repository
- **PocketFlow Questions**: Check PocketFlow documentation
- **Claude API**: Refer to Anthropic's documentation
- **Your Project**: Update this section with your support channels

---

Remember to remove this TEMPLATE.md file once you've completed the setup, or convert it to your own setup guide!
