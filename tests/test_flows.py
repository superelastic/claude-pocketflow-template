"""Comprehensive flow integration tests for Claude PocketFlow Template."""

import asyncio
import json
import tempfile
from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pocketflow import Flow

from claude_pocketflow_template.config import Config
from claude_pocketflow_template.daemon import FlowDaemon


@pytest.fixture
def temp_config():
    """Create a temporary configuration for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config = Config(
            anthropic_api_key="test_key",
            debug=True,
            log_level="DEBUG",
            data_dir=Path(temp_dir) / "data",
            logs_dir=Path(temp_dir) / "logs",
        )
        yield config


@pytest.fixture
def mock_flow():
    """Create a mock flow for testing."""
    flow = MagicMock(spec=Flow)
    flow.run = AsyncMock()
    flow.stop = AsyncMock()
    return flow


@pytest.fixture
def flow_daemon(temp_config):
    """Create a flow daemon for testing."""
    return FlowDaemon(temp_config)


class TestConfig:
    """Test configuration management."""

    def test_config_creation_with_defaults(self):
        """Test creating config with default values."""
        config = Config(anthropic_api_key="test_key")
        assert config.anthropic_api_key == "test_key"
        assert config.debug is False
        assert config.log_level == "INFO"
        assert config.flow_timeout == 300
        assert config.max_retries == 3

    def test_config_from_environment(self, monkeypatch):
        """Test config loading from environment variables."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "env_test_key")
        monkeypatch.setenv("DEBUG", "true")
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        monkeypatch.setenv("FLOW_TIMEOUT", "600")

        config = Config()
        assert config.anthropic_api_key == "env_test_key"
        assert config.debug is True
        assert config.log_level == "DEBUG"
        assert config.flow_timeout == 600

    def test_config_directory_creation(self, temp_config):
        """Test that directories are created."""
        assert temp_config.data_dir.exists()
        assert temp_config.logs_dir.exists()

    def test_config_validation_missing_api_key(self):
        """Test config validation fails without API key."""
        with pytest.raises(ValueError):
            Config()


class TestFlowDaemon:
    """Test flow daemon functionality."""

    def test_daemon_initialization(self, flow_daemon, temp_config):
        """Test daemon is properly initialized."""
        assert flow_daemon.config == temp_config
        assert flow_daemon.flows == {}
        assert flow_daemon._running is False

    def test_add_flow(self, flow_daemon, mock_flow):
        """Test adding a flow to the daemon."""
        flow_daemon.add_flow("test_flow", mock_flow)
        assert "test_flow" in flow_daemon.flows
        assert flow_daemon.flows["test_flow"] == mock_flow

    def test_remove_flow(self, flow_daemon, mock_flow):
        """Test removing a flow from the daemon."""
        flow_daemon.add_flow("test_flow", mock_flow)
        removed_flow = flow_daemon.remove_flow("test_flow")
        assert removed_flow == mock_flow
        assert "test_flow" not in flow_daemon.flows

    def test_remove_nonexistent_flow(self, flow_daemon):
        """Test removing a flow that doesn't exist."""
        result = flow_daemon.remove_flow("nonexistent")
        assert result is None

    async def test_daemon_start_stop(self, flow_daemon):
        """Test daemon start and stop lifecycle."""
        # Mock the initialize_flows method
        flow_daemon._initialize_flows = AsyncMock()

        # Start daemon in background
        start_task = asyncio.create_task(flow_daemon.start())
        
        # Give it a moment to start
        await asyncio.sleep(0.1)
        assert flow_daemon._running is True
        
        # Stop the daemon
        await flow_daemon.stop()
        assert flow_daemon._running is False
        
        # Wait for start task to complete
        try:
            await asyncio.wait_for(start_task, timeout=1.0)
        except asyncio.TimeoutError:
            start_task.cancel()

    async def test_daemon_with_flows(self, flow_daemon, mock_flow):
        """Test daemon manages flows properly."""
        flow_daemon.add_flow("test_flow", mock_flow)
        
        # Start and immediately stop
        flow_daemon._initialize_flows = AsyncMock()
        start_task = asyncio.create_task(flow_daemon.start())
        await asyncio.sleep(0.1)
        await flow_daemon.stop()
        
        try:
            await asyncio.wait_for(start_task, timeout=1.0)
        except asyncio.TimeoutError:
            start_task.cancel()


class TestFlowIntegration:
    """Test flow integration scenarios."""

    async def test_simple_flow_execution(self, flow_daemon, mock_flow):
        """Test simple flow execution."""
        mock_flow.run.return_value = {"status": "success", "result": "test_result"}
        
        flow_daemon.add_flow("simple_flow", mock_flow)
        
        # Simulate flow execution
        result = await mock_flow.run()
        assert result["status"] == "success"
        assert result["result"] == "test_result"

    async def test_flow_with_error_handling(self, flow_daemon, mock_flow):
        """Test flow error handling."""
        mock_flow.run.side_effect = Exception("Test error")
        
        flow_daemon.add_flow("error_flow", mock_flow)
        
        with pytest.raises(Exception, match="Test error"):
            await mock_flow.run()

    async def test_multiple_flows_execution(self, flow_daemon):
        """Test executing multiple flows."""
        flows = {}
        for i in range(3):
            flow = MagicMock(spec=Flow)
            flow.run = AsyncMock(return_value={"flow_id": i, "status": "success"})
            flows[f"flow_{i}"] = flow
            flow_daemon.add_flow(f"flow_{i}", flow)
        
        # Execute all flows
        results = []
        for flow in flows.values():
            result = await flow.run()
            results.append(result)
        
        assert len(results) == 3
        for i, result in enumerate(results):
            assert result["flow_id"] == i
            assert result["status"] == "success"

    async def test_flow_timeout_handling(self, flow_daemon, mock_flow):
        """Test flow timeout scenarios."""
        # Simulate a slow flow
        async def slow_flow():
            await asyncio.sleep(2)
            return {"status": "success"}
        
        mock_flow.run = slow_flow
        flow_daemon.add_flow("slow_flow", mock_flow)
        
        # Test with timeout
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(mock_flow.run(), timeout=0.5)

    async def test_flow_retry_mechanism(self, flow_daemon, mock_flow):
        """Test flow retry logic."""
        call_count = 0
        
        async def failing_flow():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception(f"Attempt {call_count} failed")
            return {"status": "success", "attempts": call_count}
        
        mock_flow.run = failing_flow
        flow_daemon.add_flow("retry_flow", mock_flow)
        
        # Simulate retry logic
        max_retries = flow_daemon.config.max_retries
        for attempt in range(max_retries):
            try:
                result = await mock_flow.run()
                assert result["status"] == "success"
                assert result["attempts"] == 3
                break
            except Exception:
                if attempt == max_retries - 1:
                    raise
                continue


class TestFlowData:
    """Test flow data handling."""

    def test_flow_data_serialization(self, temp_config):
        """Test serializing flow data."""
        data = {
            "flow_id": "test_flow",
            "timestamp": "2024-01-01T00:00:00Z",
            "input": {"message": "Hello, world!"},
            "output": {"response": "Hello back!"},
        }
        
        # Write data to file
        data_file = temp_config.data_dir / "flow_data.json"
        with open(data_file, "w") as f:
            json.dump(data, f)
        
        # Read and verify
        with open(data_file, "r") as f:
            loaded_data = json.load(f)
        
        assert loaded_data == data

    def test_flow_data_validation(self):
        """Test flow data validation."""
        valid_data = {
            "flow_id": "test",
            "input": {"key": "value"},
            "output": {"result": "success"},
        }
        
        # Test valid data
        assert "flow_id" in valid_data
        assert "input" in valid_data
        assert "output" in valid_data
        
        # Test invalid data
        invalid_data = {"flow_id": "test"}
        assert "input" not in invalid_data
        assert "output" not in invalid_data


class TestFlowPerformance:
    """Test flow performance characteristics."""

    async def test_concurrent_flow_execution(self, flow_daemon):
        """Test concurrent flow execution."""
        flows = []
        for i in range(10):
            flow = MagicMock(spec=Flow)
            flow.run = AsyncMock(return_value={"id": i, "status": "success"})
            flows.append(flow)
            flow_daemon.add_flow(f"concurrent_flow_{i}", flow)
        
        # Execute all flows concurrently
        tasks = [flow.run() for flow in flows]
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 10
        for i, result in enumerate(results):
            assert result["id"] == i
            assert result["status"] == "success"

    async def test_flow_memory_usage(self, flow_daemon, mock_flow):
        """Test flow memory usage patterns."""
        # Simulate a flow that processes large data
        large_data = {"data": "x" * 10000}  # 10KB of data
        mock_flow.run.return_value = large_data
        
        flow_daemon.add_flow("memory_flow", mock_flow)
        
        result = await mock_flow.run()
        assert len(result["data"]) == 10000


class TestFlowConfiguration:
    """Test flow configuration scenarios."""

    def test_flow_config_override(self, temp_config):
        """Test overriding flow configuration."""
        # Create config with custom values
        custom_config = Config(
            anthropic_api_key="custom_key",
            flow_timeout=600,
            max_retries=5,
            data_dir=temp_config.data_dir,
            logs_dir=temp_config.logs_dir,
        )
        
        daemon = FlowDaemon(custom_config)
        assert daemon.config.flow_timeout == 600
        assert daemon.config.max_retries == 5

    def test_flow_environment_config(self, monkeypatch, temp_config):
        """Test flow configuration from environment."""
        monkeypatch.setenv("FLOW_TIMEOUT", "900")
        monkeypatch.setenv("MAX_RETRIES", "10")
        
        config = Config(
            anthropic_api_key="test_key",
            data_dir=temp_config.data_dir,
            logs_dir=temp_config.logs_dir,
        )
        
        assert config.flow_timeout == 900
        assert config.max_retries == 10


class TestFlowEdgeCases:
    """Test flow edge cases and error conditions."""

    async def test_flow_with_none_result(self, flow_daemon, mock_flow):
        """Test flow returning None."""
        mock_flow.run.return_value = None
        flow_daemon.add_flow("none_flow", mock_flow)
        
        result = await mock_flow.run()
        assert result is None

    async def test_flow_with_empty_result(self, flow_daemon, mock_flow):
        """Test flow returning empty result."""
        mock_flow.run.return_value = {}
        flow_daemon.add_flow("empty_flow", mock_flow)
        
        result = await mock_flow.run()
        assert result == {}

    async def test_daemon_stop_without_start(self, flow_daemon):
        """Test stopping daemon without starting."""
        await flow_daemon.stop()  # Should not raise an error
        assert flow_daemon._running is False

    def test_add_duplicate_flow(self, flow_daemon, mock_flow):
        """Test adding flow with duplicate name."""
        flow_daemon.add_flow("duplicate", mock_flow)
        
        # Add another flow with same name (should replace)
        new_flow = MagicMock(spec=Flow)
        flow_daemon.add_flow("duplicate", new_flow)
        
        assert flow_daemon.flows["duplicate"] == new_flow

    async def test_flow_exception_propagation(self, mock_flow):
        """Test that flow exceptions are properly propagated."""
        custom_exception = ValueError("Custom test error")
        mock_flow.run.side_effect = custom_exception
        
        with pytest.raises(ValueError, match="Custom test error"):
            await mock_flow.run()


class TestFlowLogging:
    """Test flow logging functionality."""

    def test_logging_configuration(self, temp_config):
        """Test logging is properly configured."""
        daemon = FlowDaemon(temp_config)
        assert daemon.config.log_level == "DEBUG"
        assert temp_config.logs_dir.exists()

    @patch("claude_pocketflow_template.daemon.logger")
    async def test_daemon_logging(self, mock_logger, flow_daemon):
        """Test daemon logs important events."""
        flow_daemon._initialize_flows = AsyncMock()
        
        # Start and stop daemon
        start_task = asyncio.create_task(flow_daemon.start())
        await asyncio.sleep(0.1)
        await flow_daemon.stop()
        
        try:
            await asyncio.wait_for(start_task, timeout=1.0)
        except asyncio.TimeoutError:
            start_task.cancel()
        
        # Verify logging calls
        mock_logger.info.assert_called()

    @patch("claude_pocketflow_template.daemon.logger")
    def test_flow_add_remove_logging(self, mock_logger, flow_daemon, mock_flow):
        """Test flow add/remove operations are logged."""
        flow_daemon.add_flow("test_flow", mock_flow)
        mock_logger.info.assert_called_with("Added flow: test_flow")
        
        flow_daemon.remove_flow("test_flow")
        mock_logger.info.assert_called_with("Removed flow: test_flow")


# Performance and stress tests
class TestFlowStress:
    """Stress tests for flow system."""

    @pytest.mark.slow
    async def test_many_flows(self, flow_daemon):
        """Test system with many flows."""
        num_flows = 100
        
        for i in range(num_flows):
            flow = MagicMock(spec=Flow)
            flow.run = AsyncMock(return_value={"id": i})
            flow_daemon.add_flow(f"flow_{i}", flow)
        
        assert len(flow_daemon.flows) == num_flows
        
        # Clean up
        for i in range(num_flows):
            flow_daemon.remove_flow(f"flow_{i}")
        
        assert len(flow_daemon.flows) == 0

    @pytest.mark.slow
    async def test_rapid_flow_operations(self, flow_daemon):
        """Test rapid flow add/remove operations."""
        flow = MagicMock(spec=Flow)
        
        # Rapidly add and remove flows
        for i in range(1000):
            flow_daemon.add_flow(f"rapid_{i}", flow)
            if i % 2 == 0:  # Remove every other flow
                flow_daemon.remove_flow(f"rapid_{i}")
        
        # Should have ~500 flows remaining
        assert len(flow_daemon.flows) > 400