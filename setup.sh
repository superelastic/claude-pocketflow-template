#!/bin/bash

# Claude PocketFlow Template Setup Script
# This script sets up the development environment for the Claude PocketFlow template

set -e  # Exit on any error

echo "🚀 Setting up Claude PocketFlow Template..."

# Check if Python 3.10+ is available
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.10+ required, found $python_version"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

echo "✅ Python $python_version found"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
else
    echo "✅ uv package manager found"
fi

# Create virtual environment and install dependencies
echo "📦 Creating virtual environment and installing dependencies..."
uv venv
source .venv/bin/activate

# Install project dependencies
echo "📦 Installing project dependencies..."
uv pip install -e ".[dev]"

# Install PocketFlow separately as it may have compatibility issues with uv
echo "📦 Installing PocketFlow..."
pip install pocketflow

# Set up pre-commit hooks
echo "🔧 Setting up pre-commit hooks..."
uv run pre-commit install

# Create necessary directories
echo "📁 Creating project structure..."
mkdir -p src/claude_pocketflow_template
mkdir -p tests
mkdir -p docs
mkdir -p .mdc

# Create basic package structure if it doesn't exist
if [ ! -f "src/claude_pocketflow_template/__init__.py" ]; then
    echo "📝 Creating basic package structure..."

    # Create __init__.py
    cat > src/claude_pocketflow_template/__init__.py << 'EOF'
"""Claude PocketFlow Template - A template for building AI flows with PocketFlow and Claude."""

__version__ = "0.1.0"

from .config import Config
from .daemon import FlowDaemon

__all__ = ["Config", "FlowDaemon", "__version__"]
EOF

    # Create __about__.py
    cat > src/claude_pocketflow_template/__about__.py << 'EOF'
# SPDX-FileCopyrightText: 2024-present Your Name <your.email@example.com>
# SPDX-License-Identifier: MIT
__version__ = "0.1.0"
EOF

    # Create basic config.py
    cat > src/claude_pocketflow_template/config.py << 'EOF'
"""Configuration management for Claude PocketFlow Template."""

import os
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, Field


class Config(BaseSettings):
    """Application configuration."""

    # API Configuration
    anthropic_api_key: str = Field(..., env="ANTHROPIC_API_KEY")

    # Application Settings
    debug: bool = Field(False, env="DEBUG")
    log_level: str = Field("INFO", env="LOG_LEVEL")

    # Flow Configuration
    flow_timeout: int = Field(300, env="FLOW_TIMEOUT")
    max_retries: int = Field(3, env="MAX_RETRIES")

    # File Paths
    data_dir: Path = Field(Path("data"), env="DATA_DIR")
    logs_dir: Path = Field(Path("logs"), env="LOGS_DIR")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def __post_init__(self):
        """Create necessary directories."""
        self.data_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
EOF

    # Create basic daemon.py
    cat > src/claude_pocketflow_template/daemon.py << 'EOF'
"""Main daemon for Claude PocketFlow Template."""

import asyncio
from typing import Any, Dict, Optional

from loguru import logger
from pocketflow import Flow

from .config import Config


class FlowDaemon:
    """Main daemon for managing AI flows."""

    def __init__(self, config: Config):
        """Initialize the flow daemon."""
        self.config = config
        self.flows: Dict[str, Flow] = {}
        self._running = False

    async def start(self) -> None:
        """Start the flow daemon."""
        logger.info("Starting Flow Daemon...")
        self._running = True

        # Initialize flows here
        await self._initialize_flows()

        # Main daemon loop
        while self._running:
            try:
                await asyncio.sleep(1)
            except KeyboardInterrupt:
                logger.info("Received shutdown signal")
                break

        await self.stop()

    async def stop(self) -> None:
        """Stop the flow daemon."""
        logger.info("Stopping Flow Daemon...")
        self._running = False

        # Clean up flows
        for flow_name, flow in self.flows.items():
            logger.info(f"Stopping flow: {flow_name}")
            # Add flow cleanup logic here

    async def _initialize_flows(self) -> None:
        """Initialize all flows."""
        logger.info("Initializing flows...")
        # Add your flow initialization logic here

    def add_flow(self, name: str, flow: Flow) -> None:
        """Add a flow to the daemon."""
        self.flows[name] = flow
        logger.info(f"Added flow: {name}")

    def remove_flow(self, name: str) -> Optional[Flow]:
        """Remove a flow from the daemon."""
        if name in self.flows:
            flow = self.flows.pop(name)
            logger.info(f"Removed flow: {name}")
            return flow
        return None
EOF

fi

# Create .env.example if it doesn't exist
if [ ! -f ".env.example" ]; then
    cat > .env.example << 'EOF'
# API Keys
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Application Settings
DEBUG=false
LOG_LEVEL=INFO

# Flow Configuration
FLOW_TIMEOUT=300
MAX_RETRIES=3

# Directories
DATA_DIR=data
LOGS_DIR=logs
EOF
fi

# Run initial code quality checks
echo "🔍 Running initial code quality checks..."
uv run ruff format .
uv run ruff check . --fix || true
uv run pyright || true

echo ""
echo "✅ Setup complete! Your Claude PocketFlow Template is ready."
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env and configure your API keys"
echo "2. Activate the virtual environment: source .venv/bin/activate"
echo "3. Start building your flows in src/claude_pocketflow_template/"
echo "4. Run tests: uv run pytest"
echo "5. Format code: uv run ruff format ."
echo "6. Check types: uv run pyright"
echo ""
echo "Happy coding! 🎉"
