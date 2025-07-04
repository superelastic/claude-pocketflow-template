"""Tests for the flow daemon."""

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from claude_pocketflow_template.daemon import FlowDaemon


class MockFlow:
    """Mock Flow class for testing."""

    def __init__(self, name: str = "test_flow"):
        self.name = name


class TestFlowDaemonBasics:
    """Test basic daemon functionality."""

    def test_daemon_initialization(self, test_config):
        """Test daemon is initialized correctly."""
        daemon = FlowDaemon(test_config)
        assert daemon.config == test_config
        assert daemon.flows == {}
        assert daemon._running is False

    def test_add_single_flow(self, test_config):
        """Test adding a single flow."""
        daemon = FlowDaemon(test_config)
        mock_flow = MockFlow("test_flow")

        daemon.add_flow("test_flow", mock_flow)

        assert "test_flow" in daemon.flows
        assert daemon.flows["test_flow"] == mock_flow
        assert len(daemon.flows) == 1

    def test_add_multiple_flows(self, test_config):
        """Test adding multiple flows."""
        daemon = FlowDaemon(test_config)
        flows = {}

        for i in range(5):
            flow_name = f"flow_{i}"
            mock_flow = MockFlow()
            flows[flow_name] = mock_flow
            daemon.add_flow(flow_name, mock_flow)

        assert len(daemon.flows) == 5
        for flow_name, flow in flows.items():
            assert daemon.flows[flow_name] == flow

    def test_remove_existing_flow(self, test_config):
        """Test removing an existing flow."""
        daemon = FlowDaemon(test_config)
        mock_flow = MockFlow()

        daemon.add_flow("test_flow", mock_flow)
        removed_flow = daemon.remove_flow("test_flow")

        assert removed_flow == mock_flow
        assert "test_flow" not in daemon.flows
        assert len(daemon.flows) == 0

    def test_remove_nonexistent_flow(self, test_config):
        """Test removing a flow that doesn't exist."""
        daemon = FlowDaemon(test_config)

        result = daemon.remove_flow("nonexistent_flow")

        assert result is None
        assert len(daemon.flows) == 0

    def test_replace_existing_flow(self, test_config):
        """Test replacing an existing flow with same name."""
        daemon = FlowDaemon(test_config)
        old_flow = MockFlow()
        new_flow = MockFlow()

        daemon.add_flow("test_flow", old_flow)
        daemon.add_flow("test_flow", new_flow)  # Replace

        assert daemon.flows["test_flow"] == new_flow
        assert daemon.flows["test_flow"] != old_flow
        assert len(daemon.flows) == 1


class TestFlowDaemonLifecycle:
    """Test daemon lifecycle management."""

    async def test_daemon_start_sets_running_flag(self, test_config):
        """Test that starting daemon sets running flag."""
        daemon = FlowDaemon(test_config)
        daemon._initialize_flows = AsyncMock()

        # Start daemon in background
        start_task = asyncio.create_task(daemon.start())

        # Give it time to start
        await asyncio.sleep(0.1)

        assert daemon._running is True

        # Clean up
        await daemon.stop()
        try:
            await asyncio.wait_for(start_task, timeout=1.0)
        except asyncio.TimeoutError:
            start_task.cancel()

    async def test_daemon_stop_clears_running_flag(self, test_config):
        """Test that stopping daemon clears running flag."""
        daemon = FlowDaemon(test_config)
        daemon._initialize_flows = AsyncMock()

        # Start and stop daemon
        start_task = asyncio.create_task(daemon.start())
        await asyncio.sleep(0.1)
        await daemon.stop()

        assert daemon._running is False

        try:
            await asyncio.wait_for(start_task, timeout=1.0)
        except asyncio.TimeoutError:
            start_task.cancel()

    async def test_daemon_initializes_flows_on_start(self, test_config):
        """Test that daemon initializes flows when starting."""
        daemon = FlowDaemon(test_config)
        daemon._initialize_flows = AsyncMock()

        start_task = asyncio.create_task(daemon.start())
        await asyncio.sleep(0.1)
        await daemon.stop()

        daemon._initialize_flows.assert_called_once()

        try:
            await asyncio.wait_for(start_task, timeout=1.0)
        except asyncio.TimeoutError:
            start_task.cancel()

    async def test_daemon_handles_keyboard_interrupt(self, test_config):
        """Test daemon handles KeyboardInterrupt gracefully."""
        daemon = FlowDaemon(test_config)
        daemon._initialize_flows = AsyncMock()

        # Mock sleep to raise KeyboardInterrupt
        with patch("asyncio.sleep", side_effect=KeyboardInterrupt):
            await daemon.start()

        assert daemon._running is False

    async def test_daemon_stop_without_start(self, test_config):
        """Test stopping daemon that was never started."""
        daemon = FlowDaemon(test_config)

        # Should not raise any errors
        await daemon.stop()
        assert daemon._running is False

    async def test_daemon_multiple_stops(self, test_config):
        """Test calling stop multiple times."""
        daemon = FlowDaemon(test_config)
        daemon._initialize_flows = AsyncMock()

        # Start daemon
        start_task = asyncio.create_task(daemon.start())
        await asyncio.sleep(0.1)

        # Stop multiple times
        await daemon.stop()
        await daemon.stop()
        await daemon.stop()

        assert daemon._running is False

        try:
            await asyncio.wait_for(start_task, timeout=1.0)
        except asyncio.TimeoutError:
            start_task.cancel()


class TestFlowDaemonWithFlows:
    """Test daemon behavior with flows."""

    async def test_daemon_with_single_flow(self, test_config):
        """Test daemon managing a single flow."""
        daemon = FlowDaemon(test_config)
        mock_flow = MockFlow()
        daemon._initialize_flows = AsyncMock()

        daemon.add_flow("test_flow", mock_flow)

        start_task = asyncio.create_task(daemon.start())
        await asyncio.sleep(0.1)
        await daemon.stop()

        assert "test_flow" in daemon.flows

        try:
            await asyncio.wait_for(start_task, timeout=1.0)
        except asyncio.TimeoutError:
            start_task.cancel()

    async def test_daemon_with_multiple_flows(self, test_config):
        """Test daemon managing multiple flows."""
        daemon = FlowDaemon(test_config)
        daemon._initialize_flows = AsyncMock()

        flows = {}
        for i in range(3):
            flow_name = f"flow_{i}"
            mock_flow = MockFlow()
            flows[flow_name] = mock_flow
            daemon.add_flow(flow_name, mock_flow)

        start_task = asyncio.create_task(daemon.start())
        await asyncio.sleep(0.1)
        await daemon.stop()

        assert len(daemon.flows) == 3
        for flow_name in flows:
            assert flow_name in daemon.flows

        try:
            await asyncio.wait_for(start_task, timeout=1.0)
        except asyncio.TimeoutError:
            start_task.cancel()

    async def test_daemon_flow_cleanup_on_stop(self, test_config):
        """Test that flows are handled during daemon stop."""
        daemon = FlowDaemon(test_config)
        daemon._initialize_flows = AsyncMock()

        # Add flows
        for i in range(3):
            mock_flow = MockFlow()
            daemon.add_flow(f"flow_{i}", mock_flow)

        start_task = asyncio.create_task(daemon.start())
        await asyncio.sleep(0.1)
        await daemon.stop()

        # Flows should still be in the daemon (cleanup is logged but flows remain)
        assert len(daemon.flows) == 3

        try:
            await asyncio.wait_for(start_task, timeout=1.0)
        except asyncio.TimeoutError:
            start_task.cancel()


class TestFlowDaemonLogging:
    """Test daemon logging behavior."""

    @patch("claude_pocketflow_template.daemon.logger")
    def test_add_flow_logging(self, mock_logger, test_config):
        """Test that adding flows is logged."""
        daemon = FlowDaemon(test_config)
        mock_flow = MockFlow()

        daemon.add_flow("test_flow", mock_flow)

        mock_logger.info.assert_called_with("Added flow: test_flow")

    @patch("claude_pocketflow_template.daemon.logger")
    def test_remove_flow_logging(self, mock_logger, test_config):
        """Test that removing flows is logged."""
        daemon = FlowDaemon(test_config)
        mock_flow = MockFlow()

        daemon.add_flow("test_flow", mock_flow)
        daemon.remove_flow("test_flow")

        # Should have two calls: one for add, one for remove
        calls = mock_logger.info.call_args_list
        assert any("Added flow: test_flow" in str(call) for call in calls)
        assert any("Removed flow: test_flow" in str(call) for call in calls)

    @patch("claude_pocketflow_template.daemon.logger")
    async def test_daemon_start_logging(self, mock_logger, test_config):
        """Test that daemon start is logged."""
        daemon = FlowDaemon(test_config)
        daemon._initialize_flows = AsyncMock()

        start_task = asyncio.create_task(daemon.start())
        await asyncio.sleep(0.1)
        await daemon.stop()

        mock_logger.info.assert_any_call("Starting Flow Daemon...")

        try:
            await asyncio.wait_for(start_task, timeout=1.0)
        except asyncio.TimeoutError:
            start_task.cancel()

    @patch("claude_pocketflow_template.daemon.logger")
    async def test_daemon_stop_logging(self, mock_logger, test_config):
        """Test that daemon stop is logged."""
        daemon = FlowDaemon(test_config)
        daemon._initialize_flows = AsyncMock()

        start_task = asyncio.create_task(daemon.start())
        await asyncio.sleep(0.1)
        await daemon.stop()

        mock_logger.info.assert_any_call("Stopping Flow Daemon...")

        try:
            await asyncio.wait_for(start_task, timeout=1.0)
        except asyncio.TimeoutError:
            start_task.cancel()

    @patch("claude_pocketflow_template.daemon.logger")
    async def test_flow_initialization_logging(self, mock_logger, test_config):
        """Test that flow initialization is logged."""
        daemon = FlowDaemon(test_config)
        daemon._initialize_flows = AsyncMock()

        start_task = asyncio.create_task(daemon.start())
        await asyncio.sleep(0.1)
        await daemon.stop()

        mock_logger.info.assert_any_call("Initializing flows...")

        try:
            await asyncio.wait_for(start_task, timeout=1.0)
        except asyncio.TimeoutError:
            start_task.cancel()


class TestFlowDaemonEdgeCases:
    """Test edge cases and error conditions."""

    def test_add_flow_with_none_flow(self, test_config):
        """Test adding None as a flow."""
        daemon = FlowDaemon(test_config)

        daemon.add_flow("none_flow", None)

        assert "none_flow" in daemon.flows
        assert daemon.flows["none_flow"] is None

    def test_add_flow_with_empty_name(self, test_config):
        """Test adding flow with empty name."""
        daemon = FlowDaemon(test_config)
        mock_flow = MockFlow()

        daemon.add_flow("", mock_flow)

        assert "" in daemon.flows
        assert daemon.flows[""] == mock_flow

    def test_add_flow_with_special_characters(self, test_config):
        """Test adding flow with special characters in name."""
        daemon = FlowDaemon(test_config)
        mock_flow = MockFlow()
        special_name = "flow-with_special.chars@123"

        daemon.add_flow(special_name, mock_flow)

        assert special_name in daemon.flows
        assert daemon.flows[special_name] == mock_flow

    def test_remove_flow_from_empty_daemon(self, test_config):
        """Test removing flow when daemon has no flows."""
        daemon = FlowDaemon(test_config)

        result = daemon.remove_flow("any_flow")

        assert result is None
        assert len(daemon.flows) == 0

    async def test_daemon_with_failing_initialization(self, test_config):
        """Test daemon when flow initialization fails."""
        daemon = FlowDaemon(test_config)
        daemon._initialize_flows = AsyncMock(side_effect=Exception("Init failed"))

        # Should not raise exception, daemon should handle it gracefully
        with pytest.raises(Exception, match="Init failed"):
            start_task = asyncio.create_task(daemon.start())
            await asyncio.sleep(0.1)
            await start_task

    def test_daemon_config_mutation(self, test_config):
        """Test that daemon doesn't break if config is mutated."""
        daemon = FlowDaemon(test_config)
        original_timeout = test_config.flow_timeout

        # Mutate config
        test_config.flow_timeout = 999

        # Daemon should still have reference to the config
        assert daemon.config.flow_timeout == 999
        assert daemon.config.flow_timeout != original_timeout


class TestFlowDaemonConcurrency:
    """Test daemon behavior under concurrent operations."""

    async def test_concurrent_flow_additions(self, test_config):
        """Test adding flows concurrently."""
        daemon = FlowDaemon(test_config)

        async def add_flow(i):
            mock_flow = MockFlow()
            daemon.add_flow(f"concurrent_flow_{i}", mock_flow)

        # Add flows concurrently
        tasks = [add_flow(i) for i in range(10)]
        await asyncio.gather(*tasks)

        assert len(daemon.flows) == 10
        for i in range(10):
            assert f"concurrent_flow_{i}" in daemon.flows

    async def test_concurrent_flow_removals(self, test_config):
        """Test removing flows concurrently."""
        daemon = FlowDaemon(test_config)

        # Add flows first
        for i in range(10):
            mock_flow = MockFlow()
            daemon.add_flow(f"concurrent_flow_{i}", mock_flow)

        async def remove_flow(i):
            daemon.remove_flow(f"concurrent_flow_{i}")

        # Remove flows concurrently
        tasks = [remove_flow(i) for i in range(10)]
        await asyncio.gather(*tasks)

        assert len(daemon.flows) == 0

    async def test_concurrent_mixed_operations(self, test_config):
        """Test mixed concurrent operations."""
        daemon = FlowDaemon(test_config)

        async def add_flow(i):
            mock_flow = MockFlow()
            daemon.add_flow(f"add_flow_{i}", mock_flow)

        async def remove_flow(i):
            daemon.remove_flow(f"remove_flow_{i}")

        # Pre-populate some flows to remove
        for i in range(5):
            mock_flow = MockFlow()
            daemon.add_flow(f"remove_flow_{i}", mock_flow)

        # Mix of add and remove operations
        add_tasks = [add_flow(i) for i in range(5)]
        remove_tasks = [remove_flow(i) for i in range(5)]

        await asyncio.gather(*add_tasks, *remove_tasks)

        # Should have 5 flows (added 5, removed 5)
        assert len(daemon.flows) == 5
        for i in range(5):
            assert f"add_flow_{i}" in daemon.flows
            assert f"remove_flow_{i}" not in daemon.flows
