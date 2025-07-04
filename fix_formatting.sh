#!/bin/bash
# This script fixes all formatting issues that pre-commit would fix

echo "Fixing formatting issues..."

# Add all files to git staging (pre-commit only runs on staged files)
git add -A

# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run pre-commit on all files and auto-fix issues
pre-commit run --all-files || true

# The above command will fail but fix issues. Run again to verify
pre-commit run --all-files

echo "Formatting fixes complete!"
