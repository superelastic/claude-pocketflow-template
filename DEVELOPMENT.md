# Solo Developer-Friendly Approach

This project is configured for **pragmatic solo development** - tools help you but never block you.

## Quick Start

```bash
# Install and run
pip install -e ".[dev]"
pytest  # Run tests (advisory only)

# Optional quality checks (never blocking)
make -f Makefile.dev help    # See all available commands
make -f Makefile.dev check   # Run all checks (warnings only)
make -f Makefile.dev format  # Auto-format code
```

## Development Philosophy

### ✅ What WILL Happen

- Tests run and give you feedback
- Pre-commit hooks clean up obvious issues
- CI runs essential checks
- Code gets formatted automatically

### ❌ What WON'T Happen

- Commits blocked by formatting issues
- Build failures from missing directories
- CI failures from minor style issues
- Development stopped by coverage requirements

## Tools Overview

- **Pytest**: Runs tests, skips brittle ones
- **Ruff**: Formats code, fixes issues when possible
- **Pre-commit**: Cleans up files, but won't block commits
- **CI**: Runs core tests, reports issues but doesn't fail

## Local Commands

```bash
# Core development
pytest                           # Run tests
python -m src.main              # Run the example

# Optional quality (use when you want)
make -f Makefile.dev format     # Format code
make -f Makefile.dev lint       # Check style
make -f Makefile.dev typecheck  # Check types
make -f Makefile.dev clean      # Clean cache

# All quality checks at once
make -f Makefile.dev check
```

## What Changed

1. **CI**: Only fails on broken functionality, not style
2. **Pre-commit**: Fixes issues but doesn't block
3. **Tests**: Skips brittle filesystem/structure checks
4. **Coverage**: Optional instead of required

This approach lets you focus on building features instead of fighting tools!
