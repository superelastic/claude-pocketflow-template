"""Pytest configuration and shared fixtures."""

import asyncio
import tempfile
from pathlib import Path

import pytest

from claude_pocketflow_template.config import Config


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def test_config(temp_dir):
    """Create a test configuration."""
    return Config(
        anthropic_api_key="test_anthropic_key",
        debug=True,
        log_level="DEBUG",
        data_dir=temp_dir / "data",
        logs_dir=temp_dir / "logs",
        flow_timeout=30,
        max_retries=2,
    )


@pytest.fixture
def sample_flow_data():
    """Sample flow data for testing."""
    return {
        "flow_id": "test_flow_001",
        "timestamp": "2024-01-01T12:00:00Z",
        "input": {
            "message": "Hello, world!",
            "user_id": "user123",
            "context": {"session_id": "session456"},
        },
        "output": {
            "response": "Hello! How can I help you today?",
            "confidence": 0.95,
            "tokens_used": 42,
        },
        "metadata": {
            "model": "claude-3-sonnet",
            "duration_ms": 1500,
            "retries": 0,
        },
    }


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
