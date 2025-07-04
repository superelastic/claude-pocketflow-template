"""Base node implementations for PocketFlow."""

import logging
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger(__name__)


class BaseNode(ABC):
    """Base class for all PocketFlow nodes.

    Implements the three-phase lifecycle:
    1. prep() - Preparation and validation
    2. exec() - Main execution logic
    3. post() - Cleanup and finalization
    """

    def __init__(self, name: str | None = None):
        """Initialize the node with an optional name."""
        self.name = name or self.__class__.__name__
        self.logger = logging.getLogger(f"{__name__}.{self.name}")

    def prep(self, store: dict[str, Any]) -> dict[str, Any]:
        """Preparation phase - validate inputs and setup.

        Override this method to:
        - Validate required inputs
        - Set up resources
        - Initialize state

        Args:
            store: The shared state dictionary

        Returns:
            Updated store dictionary
        """
        self.logger.debug(f"Preparing {self.name}")
        return store

    @abstractmethod
    def exec(self, store: dict[str, Any]) -> dict[str, Any]:
        """Execution phase - main logic implementation.

        This method must be implemented by all nodes.

        Args:
            store: The shared state dictionary

        Returns:
            Updated store dictionary with results
        """
        pass

    def post(self, store: dict[str, Any]) -> dict[str, Any]:
        """Post-processing phase - cleanup and finalization.

        Override this method to:
        - Clean up resources
        - Format outputs
        - Set transition actions

        Args:
            store: The shared state dictionary

        Returns:
            Final store state
        """
        self.logger.debug(f"Post-processing {self.name}")
        return store

    def run(self, store: dict[str, Any]) -> dict[str, Any]:
        """Execute the complete node lifecycle.

        Runs all three phases in order: prep → exec → post

        Args:
            store: The shared state dictionary

        Returns:
            Final store state after all phases
        """
        try:
            self.logger.info(f"Running {self.name}")
            store = self.prep(store)

            # Skip execution if prep phase set an error
            if store.get("action") != "error":
                store = self.exec(store)

            store = self.post(store)

            self.logger.info(
                f"Completed {self.name} with action: {store.get('action', 'none')}"
            )
            return store

        except Exception as e:
            self.logger.error(f"Error in {self.name}: {e!s}")
            store["action"] = "error"
            store["error"] = str(e)
            store["error_node"] = self.name
            return store


class ValidationMixin:
    """Mixin for common validation patterns."""

    def validate_required_fields(
        self, store: dict[str, Any], required_fields: list[str]
    ) -> tuple[bool, str | None]:
        """Validate that required fields exist in store.

        Args:
            store: The shared state dictionary
            required_fields: List of required field names

        Returns:
            Tuple of (is_valid, error_message)
        """
        missing_fields = [field for field in required_fields if field not in store]

        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"

        return True, None

    def validate_field_types(
        self, store: dict[str, Any], field_types: dict[str, type]
    ) -> tuple[bool, str | None]:
        """Validate that fields have correct types.

        Args:
            store: The shared state dictionary
            field_types: Dict mapping field names to expected types

        Returns:
            Tuple of (is_valid, error_message)
        """
        for field, expected_type in field_types.items():
            if field in store and not isinstance(store[field], expected_type):
                actual_type = type(store[field]).__name__
                expected_type_name = expected_type.__name__
                return (
                    False,
                    f"Field '{field}' must be {expected_type_name}, got {actual_type}",
                )

        return True, None
