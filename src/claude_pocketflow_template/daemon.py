"""Flow daemon for managing and executing flows."""

import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)


class FlowDaemon:
    """Daemon for managing and executing flows."""

    def __init__(self, config: Any):
        """Initialize the flow daemon.

        Args:
            config: Configuration object
        """
        self.config = config
        self.flows: dict[str, Any] = {}
        self._running = False
        self._task = None
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def add_flow(self, name: str, flow: Any) -> None:
        """Add a flow to the daemon.

        Args:
            name: Name identifier for the flow
            flow: Flow object to add
        """
        self.flows[name] = flow
        self.logger.info(f"Added flow: {name}")

    def remove_flow(self, name: str) -> Any | None:
        """Remove a flow from the daemon.

        Args:
            name: Name of the flow to remove

        Returns:
            The removed flow object, or None if not found
        """
        if name in self.flows:
            flow = self.flows.pop(name)
            self.logger.info(f"Removed flow: {name}")
            return flow
        return None

    def get_flow(self, name: str) -> Any | None:
        """Get a flow by name.

        Args:
            name: Name of the flow

        Returns:
            Flow object or None if not found
        """
        return self.flows.get(name)

    async def start(self) -> None:
        """Start the daemon."""
        if self._running:
            return

        self._running = True
        self.logger.info("Starting Flow Daemon...")

        # Initialize flows
        await self._initialize_flows()

        # Start the main daemon loop
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self) -> None:
        """Stop the daemon."""
        if not self._running:
            return

        self._running = False
        self.logger.info("Stopping Flow Daemon...")

        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None

    async def _run_loop(self) -> None:
        """Main daemon loop."""
        while self._running:
            try:
                # Process flows or handle requests
                await asyncio.sleep(1)  # Simple heartbeat
            except asyncio.CancelledError:
                break
            except Exception:
                self.logger.exception("Error in daemon loop")

    async def execute_flow(
        self, flow_name: str, input_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute a flow by name.

        Args:
            flow_name: Name of the flow to execute
            input_data: Input data for the flow

        Returns:
            Flow execution result

        Raises:
            ValueError: If flow not found
        """
        flow = self.get_flow(flow_name)
        if not flow:
            msg = f"Flow not found: {flow_name}"
            raise ValueError(msg)

        self.logger.info(f"Executing flow: {flow_name}")

        # Execute the flow (this would be implementation-specific)
        # For now, return a mock result
        return {
            "flow_name": flow_name,
            "input": input_data,
            "status": "completed",
            "result": "Mock execution result",
        }

    @property
    def is_running(self) -> bool:
        """Check if daemon is running."""
        return self._running

    def list_flows(self) -> list[str]:
        """List all registered flow names."""
        return list(self.flows.keys())

    async def _initialize_flows(self) -> None:
        """Initialize flows on daemon startup.

        This method can be overridden by subclasses to perform
        custom flow initialization logic.
        """
        self.logger.info("Initializing flows...")
        # Default implementation does nothing
        # Subclasses can override to load flows from config, database, etc.
        pass
