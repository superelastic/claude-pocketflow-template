"""Example node implementations."""

import random
from typing import Any

from src.nodes.base import BaseNode, ValidationMixin


class GreetingNode(BaseNode, ValidationMixin):
    """Example node that creates personalized greetings."""

    def prep(self, store: dict[str, Any]) -> dict[str, Any]:
        """Validate that name is provided."""
        # Use validation mixin for common patterns
        is_valid, error = self.validate_required_fields(store, ["name"])
        if not is_valid:
            store["action"] = "error"
            store["error"] = error
            return store

        # Normalize the name
        store["name"] = store["name"].strip().title()
        return store

    def exec(self, store: dict[str, Any]) -> dict[str, Any]:
        """Generate the greeting based on time of day."""
        if store.get("action") == "error":
            return store

        name = store["name"]
        time_of_day = store.get("time_of_day", "day")

        greetings = {
            "morning": f"Good morning, {name}! ☀️",
            "afternoon": f"Good afternoon, {name}! 🌤️",
            "evening": f"Good evening, {name}! 🌙",
            "day": f"Hello, {name}! 👋",
        }

        store["greeting"] = greetings.get(time_of_day, greetings["day"])
        store["action"] = "success"
        return store

    def post(self, store: dict[str, Any]) -> dict[str, Any]:
        """Add metadata about the greeting."""
        if store.get("action") == "success":
            store["greeting_metadata"] = {
                "length": len(store["greeting"]),
                "personalized": True,
                "time_aware": store.get("time_of_day") is not None,
            }
        return store


class RandomNumberNode(BaseNode):
    """Example node that generates random numbers."""

    def prep(self, store: dict[str, Any]) -> dict[str, Any]:
        """Set default range if not provided."""
        if "min_value" not in store:
            store["min_value"] = 1
        if "max_value" not in store:
            store["max_value"] = 100

        # Validate range
        if store["min_value"] >= store["max_value"]:
            store["action"] = "error"
            store["error"] = "min_value must be less than max_value"

        return store

    def exec(self, store: dict[str, Any]) -> dict[str, Any]:
        """Generate a random number within the specified range."""
        if store.get("action") == "error":
            return store

        min_val = store["min_value"]
        max_val = store["max_value"]

        store["random_number"] = random.randint(min_val, max_val)  # noqa: S311
        store["action"] = "success"

        return store


class DataTransformNode(BaseNode, ValidationMixin):
    """Example node that transforms data structures."""

    def prep(self, store: dict[str, Any]) -> dict[str, Any]:
        """Validate input data exists."""
        is_valid, error = self.validate_required_fields(store, ["input_data"])
        if not is_valid:
            store["action"] = "error"
            store["error"] = error
            return store

        # Validate it's a list
        is_valid, error = self.validate_field_types(store, {"input_data": list})
        if not is_valid:
            store["action"] = "error"
            store["error"] = error

        return store

    def exec(self, store: dict[str, Any]) -> dict[str, Any]:
        """Transform the input data."""
        if store.get("action") == "error":
            return store

        input_data = store["input_data"]
        transform_type = store.get("transform_type", "uppercase")

        if transform_type == "uppercase":
            transformed = [str(item).upper() for item in input_data]
        elif transform_type == "reverse":
            transformed = list(reversed(input_data))
        elif transform_type == "sort":
            transformed = sorted(input_data)
        else:
            store["action"] = "error"
            store["error"] = f"Unknown transform type: {transform_type}"
            return store

        store["transformed_data"] = transformed
        store["action"] = "success"

        return store

    def post(self, store: dict[str, Any]) -> dict[str, Any]:
        """Add transformation statistics."""
        if store.get("action") == "success":
            store["transform_stats"] = {
                "input_count": len(store["input_data"]),
                "output_count": len(store["transformed_data"]),
                "transform_type": store.get("transform_type", "uppercase"),
            }
        return store


class ConditionalNode(BaseNode):
    """Example node that demonstrates conditional branching."""

    def exec(self, store: dict[str, Any]) -> dict[str, Any]:
        """Evaluate condition and set appropriate action."""
        value = store.get("value", 0)
        threshold = store.get("threshold", 50)

        if value > threshold:
            store["action"] = "above_threshold"
            store["message"] = f"Value {value} is above threshold {threshold}"
        elif value < threshold:
            store["action"] = "below_threshold"
            store["message"] = f"Value {value} is below threshold {threshold}"
        else:
            store["action"] = "at_threshold"
            store["message"] = f"Value {value} equals threshold {threshold}"

        return store
