"""Tests for example nodes."""

from src.nodes.examples import (
    ConditionalNode,
    DataTransformNode,
    GreetingNode,
    RandomNumberNode,
)


class TestGreetingNode:
    """Test the GreetingNode implementation."""

    def test_greeting_success(self):
        """Test successful greeting generation."""
        node = GreetingNode()
        store = {"name": "alice", "time_of_day": "morning"}

        result = node.run(store)

        assert result["action"] == "success"
        assert result["greeting"] == "Good morning, Alice! ☀️"
        assert result["greeting_metadata"]["personalized"] is True
        assert result["greeting_metadata"]["time_aware"] is True

    def test_greeting_default_time(self):
        """Test greeting with default time of day."""
        node = GreetingNode()
        store = {"name": "bob"}

        result = node.run(store)

        assert result["action"] == "success"
        assert result["greeting"] == "Hello, Bob! 👋"
        assert result["greeting_metadata"]["time_aware"] is False

    def test_greeting_missing_name(self):
        """Test error when name is missing."""
        node = GreetingNode()
        store = {}

        result = node.run(store)

        assert result["action"] == "error"
        assert "Missing required fields: name" in result["error"]

    def test_greeting_name_normalization(self):
        """Test that names are properly normalized."""
        node = GreetingNode()
        store = {"name": "  jOhN dOe  "}

        result = node.run(store)

        assert result["action"] == "success"
        assert "John Doe" in result["greeting"]


class TestRandomNumberNode:
    """Test the RandomNumberNode implementation."""

    def test_random_number_default_range(self):
        """Test random number with default range."""
        node = RandomNumberNode()
        store = {}

        result = node.run(store)

        assert result["action"] == "success"
        assert "random_number" in result
        assert 1 <= result["random_number"] <= 100

    def test_random_number_custom_range(self):
        """Test random number with custom range."""
        node = RandomNumberNode()
        store = {"min_value": 10, "max_value": 20}

        result = node.run(store)

        assert result["action"] == "success"
        assert 10 <= result["random_number"] <= 20

    def test_random_number_invalid_range(self):
        """Test error with invalid range."""
        node = RandomNumberNode()
        store = {"min_value": 50, "max_value": 10}

        result = node.run(store)

        assert result["action"] == "error"
        assert "must be less than" in result["error"]


class TestDataTransformNode:
    """Test the DataTransformNode implementation."""

    def test_transform_uppercase(self):
        """Test uppercase transformation."""
        node = DataTransformNode()
        store = {"input_data": ["hello", "world"], "transform_type": "uppercase"}

        result = node.run(store)

        assert result["action"] == "success"
        assert result["transformed_data"] == ["HELLO", "WORLD"]
        assert result["transform_stats"]["input_count"] == 2
        assert result["transform_stats"]["output_count"] == 2

    def test_transform_reverse(self):
        """Test reverse transformation."""
        node = DataTransformNode()
        store = {"input_data": [1, 2, 3, 4, 5], "transform_type": "reverse"}

        result = node.run(store)

        assert result["action"] == "success"
        assert result["transformed_data"] == [5, 4, 3, 2, 1]

    def test_transform_sort(self):
        """Test sort transformation."""
        node = DataTransformNode()
        store = {"input_data": [3, 1, 4, 1, 5], "transform_type": "sort"}

        result = node.run(store)

        assert result["action"] == "success"
        assert result["transformed_data"] == [1, 1, 3, 4, 5]

    def test_transform_missing_data(self):
        """Test error when input data is missing."""
        node = DataTransformNode()
        store = {}

        result = node.run(store)

        assert result["action"] == "error"
        assert "Missing required fields" in result["error"]

    def test_transform_invalid_type(self):
        """Test error when input is not a list."""
        node = DataTransformNode()
        store = {"input_data": "not a list"}

        result = node.run(store)

        assert result["action"] == "error"
        assert "must be list" in result["error"]


class TestConditionalNode:
    """Test the ConditionalNode implementation."""

    def test_conditional_above_threshold(self):
        """Test value above threshold."""
        node = ConditionalNode()
        store = {"value": 75, "threshold": 50}

        result = node.run(store)

        assert result["action"] == "above_threshold"
        assert "above threshold" in result["message"]

    def test_conditional_below_threshold(self):
        """Test value below threshold."""
        node = ConditionalNode()
        store = {"value": 25, "threshold": 50}

        result = node.run(store)

        assert result["action"] == "below_threshold"
        assert "below threshold" in result["message"]

    def test_conditional_at_threshold(self):
        """Test value equal to threshold."""
        node = ConditionalNode()
        store = {"value": 50, "threshold": 50}

        result = node.run(store)

        assert result["action"] == "at_threshold"
        assert "equals threshold" in result["message"]
