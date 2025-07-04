"""Base flow implementation for PocketFlow."""

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class FlowNode:
    """Configuration for a node in a flow."""

    node_class: type
    transitions: dict[str, str] = field(default_factory=dict)


class BaseFlow:
    """Base class for PocketFlow flows.

    Manages node execution and transitions based on actions.
    """

    def __init__(self, flow_definition: dict[str, FlowNode], name: str | None = None):
        """Initialize the flow with its definition.

        Args:
            flow_definition: Dictionary mapping node IDs to FlowNode configs
            name: Optional name for the flow
        """
        self.flow_definition = flow_definition
        self.name = name or self.__class__.__name__
        self.logger = logging.getLogger(f"{__name__}.{self.name}")
        self._validate_flow()

    def _validate_flow(self) -> None:
        """Validate the flow definition."""
        if "start" not in self.flow_definition:
            msg = "Flow must have a 'start' node"
            raise ValueError(msg)

        # Check that all transitions point to valid nodes
        all_node_ids = set(self.flow_definition.keys())
        all_node_ids.add("end")  # 'end' is always valid

        for node_id, node_config in self.flow_definition.items():
            for action, target_id in node_config.transitions.items():
                if target_id not in all_node_ids:
                    msg = (
                        f"Node '{node_id}' has transition '{action}' "
                        f"pointing to unknown node '{target_id}'"
                    )
                    raise ValueError(msg)

    def run(
        self, initial_store: dict[str, Any] | None = None, max_steps: int = 100
    ) -> dict[str, Any]:
        """Execute the flow starting from the 'start' node.

        Args:
            initial_store: Initial state dictionary
            max_steps: Maximum steps to prevent infinite loops

        Returns:
            Final store state after flow completion
        """
        store = initial_store or {}
        store["_flow_name"] = self.name
        store["_flow_path"] = []

        current_node_id = "start"
        steps = 0

        self.logger.info(f"Starting flow: {self.name}")

        while current_node_id != "end" and steps < max_steps:
            steps += 1

            # Record the path
            store["_flow_path"].append(current_node_id)

            # Get the node configuration
            if current_node_id not in self.flow_definition:
                self.logger.error(f"Unknown node: {current_node_id}")
                store["action"] = "error"
                store["error"] = f"Unknown node: {current_node_id}"
                break

            node_config = self.flow_definition[current_node_id]

            # Create and run the node
            try:
                node = node_config.node_class()
                self.logger.info(f"Executing node: {current_node_id}")
                store = node.run(store)
            except Exception as e:
                self.logger.error(f"Error in node {current_node_id}: {e!s}")
                store["action"] = "error"
                store["error"] = str(e)
                store["error_node"] = current_node_id
                break

            # Determine the next node based on action
            action = store.get("action", "default")

            if action == "error" and "error" not in node_config.transitions:
                # If there's an error but no error transition, stop
                self.logger.error(f"Error in node {current_node_id}, stopping flow")
                break

            next_node_id = node_config.transitions.get(
                action, node_config.transitions.get("default", "end")
            )

            self.logger.info(
                f"Transition: {current_node_id} --[{action}]--> {next_node_id}"
            )

            current_node_id = next_node_id

        if steps >= max_steps:
            self.logger.error(f"Flow exceeded maximum steps ({max_steps})")
            store["action"] = "error"
            store["error"] = f"Flow exceeded maximum steps ({max_steps})"

        store["_flow_steps"] = steps
        store["_flow_completed"] = current_node_id == "end"

        self.logger.info(
            f"Flow completed: {self.name} "
            f"(steps: {steps}, completed: {store['_flow_completed']})"
        )

        return store

    def visualize(self) -> str:
        """Generate a simple text visualization of the flow.

        Returns:
            String representation of the flow structure
        """
        lines = [f"Flow: {self.name}", "=" * (len(self.name) + 6), ""]

        for node_id, node_config in self.flow_definition.items():
            lines.append(f"{node_id} ({node_config.node_class.__name__}):")

            for action, target in node_config.transitions.items():
                lines.append(f"  --[{action}]--> {target}")

            lines.append("")

        return "\n".join(lines)
