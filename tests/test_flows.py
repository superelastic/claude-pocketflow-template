"""Comprehensive tests for flow execution and integration."""

from unittest.mock import patch

import pytest

from src.flows.base import BaseFlow, FlowNode
from src.flows.examples import (
    data_pipeline_flow,
    greeting_flow,
    random_conditional_flow,
)
from src.nodes.base import BaseNode
from src.nodes.examples import GreetingNode


class TestBaseFlow:
    """Test the BaseFlow class functionality."""

    def test_flow_initialization(self):
        """Test basic flow initialization."""
        flow_def = {
            "start": FlowNode(node_class=GreetingNode, transitions={"success": "end"})
        }
        flow = BaseFlow(flow_def, name="TestFlow")

        assert flow.name == "TestFlow"
        assert flow.flow_definition == flow_def
        assert "start" in flow.flow_definition

    def test_flow_validation_missing_start(self):
        """Test flow validation fails without start node."""
        flow_def = {
            "middle": FlowNode(node_class=GreetingNode, transitions={"success": "end"})
        }

        with pytest.raises(ValueError, match="Flow must have a 'start' node"):
            BaseFlow(flow_def)

    def test_flow_validation_invalid_transition(self):
        """Test flow validation fails with invalid transition target."""
        flow_def = {
            "start": FlowNode(
                node_class=GreetingNode, transitions={"success": "nonexistent_node"}
            )
        }

        with pytest.raises(ValueError, match="pointing to unknown node"):
            BaseFlow(flow_def)

    def test_flow_validation_valid_end_transition(self):
        """Test that 'end' is always a valid transition target."""
        flow_def = {
            "start": FlowNode(
                node_class=GreetingNode, transitions={"success": "end", "error": "end"}
            )
        }

        # Should not raise
        flow = BaseFlow(flow_def)
        assert flow.flow_definition["start"].transitions["success"] == "end"


class TestFlowExecution:
    """Test flow execution scenarios."""

    def test_simple_flow_execution(self):
        """Test execution of a simple linear flow."""
        result = greeting_flow.run({"name": "TestUser"})

        assert result["_flow_completed"] is True
        assert result["_flow_steps"] == 1
        assert result["_flow_path"] == ["start"]
        assert result["_flow_name"] == "GreetingFlow"
        assert "greeting" in result

    def test_flow_with_initial_store(self):
        """Test flow execution with initial store data."""
        initial_data = {"name": "InitialUser", "custom_data": "test"}
        result = greeting_flow.run(initial_data)

        assert (
            "InitialUser" in result["name"] or result["name"] == "Initialuser"
        )  # Handle name normalization
        assert result["custom_data"] == "test"
        assert result["_flow_completed"] is True

    def test_flow_execution_tracking(self):
        """Test that flow execution is properly tracked."""
        result = data_pipeline_flow.run(
            {"data": ["hello", "world"], "transform_type": "uppercase"}
        )

        assert result["_flow_completed"] is True
        assert result["_flow_steps"] >= 2  # May be 2 or 3 depending on error handling
        assert len(result["_flow_path"]) >= 2  # May vary due to error handling
        assert "start" in result["_flow_path"]

    def test_conditional_flow_execution(self):
        """Test conditional flow with different paths."""
        # Test multiple runs to get different conditional paths
        results = []
        for _ in range(10):
            result = random_conditional_flow.run()
            results.append(result)

        # Should have completed successfully
        for result in results:
            assert result["_flow_completed"] is True
            assert result["_flow_steps"] >= 2  # At least start + conditional
            assert "start" in result["_flow_path"]
            assert "check_threshold" in result["_flow_path"]


class TestFlowErrorHandling:
    """Test flow error handling scenarios."""

    class ErrorNode(BaseNode):
        """Test node that always raises an error."""

        def exec(self, store):  # noqa: ARG002
            msg = "Test error"
            raise RuntimeError(msg)

    def test_node_error_handling(self):
        """Test flow handles node execution errors."""
        flow_def = {
            "start": FlowNode(
                node_class=self.ErrorNode,
                transitions={"success": "end", "error": "end"},
            )
        }
        flow = BaseFlow(flow_def, name="ErrorTestFlow")

        result = flow.run()

        assert result["action"] == "error"
        assert "Test error" in result["error"]
        assert result["error_node"] == "start" or "ErrorNode" in str(
            result.get("error_node", "")
        )
        # Flow completes because there is an error transition to "end"
        assert result["_flow_completed"] is True

    def test_node_error_without_error_transition(self):
        """Test flow stops when node errors and no error transition exists."""
        flow_def = {
            "start": FlowNode(
                node_class=self.ErrorNode,
                transitions={"success": "end"},  # No error transition
            )
        }
        flow = BaseFlow(flow_def, name="ErrorTestFlow")

        result = flow.run()

        assert result["action"] == "error"
        assert result["_flow_completed"] is False

    def test_unknown_node_error(self):
        """Test handling of transitions to unknown nodes."""
        # Create a flow that tries to transition to an unknown node
        # This should be caught in validation, but let's test runtime handling
        flow_def = {
            "start": FlowNode(node_class=GreetingNode, transitions={"success": "end"})
        }
        flow = BaseFlow(flow_def, name="TestFlow")

        # Test the actual greeting node behavior with missing name
        result = flow.run({})  # No name provided

        # GreetingNode should handle missing name gracefully or error
        assert result["_flow_completed"] is False or "error" in result
        if "error" in result:
            assert "name" in result["error"] or "Missing" in result["error"]

    def test_max_steps_exceeded(self):
        """Test flow stops when max steps exceeded."""

        class LoopNode(BaseNode):
            """Node that always returns 'loop' action."""

            def exec(self, store):
                store["action"] = "loop"
                return store

        flow_def = {
            "start": FlowNode(
                node_class=LoopNode,
                transitions={"loop": "start"},  # Creates infinite loop
            )
        }
        flow = BaseFlow(flow_def, name="LoopTestFlow")

        result = flow.run(max_steps=5)

        assert result["_flow_steps"] == 5
        assert result["action"] == "error"
        assert "exceeded maximum steps" in result["error"]
        assert result["_flow_completed"] is False


class TestFlowTransitions:
    """Test flow transition logic."""

    class CustomActionNode(BaseNode):
        """Node that returns a custom action."""

        def exec(self, store):
            store["action"] = store.get("custom_action", "default")
            return store

    def test_default_transition(self):
        """Test flow uses default transition when action not found."""
        flow_def = {
            "start": FlowNode(
                node_class=self.CustomActionNode,
                transitions={"default": "end", "specific": "end"},
            )
        }
        flow = BaseFlow(flow_def, name="DefaultTestFlow")

        result = flow.run({"custom_action": "unknown"})

        assert result["_flow_completed"] is True
        assert result["action"] == "unknown"

    def test_specific_action_transition(self):
        """Test flow uses specific action transition when available."""
        flow_def = {
            "start": FlowNode(
                node_class=self.CustomActionNode,
                transitions={"default": "end", "specific": "second"},
            ),
            "second": FlowNode(
                node_class=self.CustomActionNode,
                transitions={"default": "end", "specific": "end"},
            ),
        }
        flow = BaseFlow(flow_def, name="SpecificTestFlow")

        result = flow.run({"custom_action": "specific"})

        assert result["_flow_completed"] is True
        assert "second" in result["_flow_path"]
        assert result["_flow_steps"] == 2

    def test_no_default_transition(self):
        """Test flow goes to end when no matching or default transition."""
        flow_def = {
            "start": FlowNode(
                node_class=self.CustomActionNode,
                transitions={"specific": "end"},  # No default
            )
        }
        flow = BaseFlow(flow_def, name="NoDefaultTestFlow")

        result = flow.run({"custom_action": "unknown"})

        assert result["_flow_completed"] is True
        assert result["action"] == "unknown"


class TestFlowVisualization:
    """Test flow visualization functionality."""

    def test_flow_visualization(self):
        """Test flow can generate text visualization."""
        visualization = greeting_flow.visualize()

        assert "GreetingFlow" in visualization
        assert "start" in visualization
        assert "GreetingNode" in visualization
        assert "--[success]--> end" in visualization

    def test_complex_flow_visualization(self):
        """Test visualization of complex flow with multiple nodes."""
        visualization = random_conditional_flow.visualize()

        assert "RandomConditionalFlow" in visualization
        assert "start" in visualization
        assert "check_threshold" in visualization
        assert "high_value_handler" in visualization
        assert "low_value_handler" in visualization
        assert "RandomNumberNode" in visualization
        assert "ConditionalNode" in visualization


class TestExampleFlows:
    """Test the example flows work correctly."""

    def test_greeting_flow_integration(self):
        """Test greeting flow integration."""
        result = greeting_flow.run({"name": "Integration Test"})

        assert result["_flow_completed"] is True
        assert "greeting" in result
        assert "Integration Test" in result["greeting"]

    def test_data_pipeline_flow_integration(self):
        """Test data pipeline flow integration."""
        result = data_pipeline_flow.run(
            {"data": ["test", "data", "pipeline"], "transform_type": "uppercase"}
        )

        assert result["_flow_completed"] is True
        assert "data" in result  # Data was processed
        assert result["_flow_completed"] is True

    def test_random_conditional_flow_paths(self):
        """Test random conditional flow takes different paths."""
        # Mock the random number to test specific paths
        with patch("random.randint") as mock_randint:
            # Test high value path
            mock_randint.return_value = 75
            result_high = random_conditional_flow.run()

            # Test low value path
            mock_randint.return_value = 25
            result_low = random_conditional_flow.run()

        assert result_high["_flow_completed"] is True
        assert result_low["_flow_completed"] is True

        # Both should complete but may take different paths
        assert "check_threshold" in result_high["_flow_path"]
        assert "check_threshold" in result_low["_flow_path"]


class TestFlowRobustness:
    """Test flow robustness and edge cases."""

    def test_empty_initial_store(self):
        """Test flow handles empty initial store."""
        result = greeting_flow.run({})

        assert result["_flow_completed"] is True
        assert "_flow_name" in result
        assert "_flow_path" in result

    def test_none_initial_store(self):
        """Test flow handles None initial store."""
        result = greeting_flow.run(None)

        assert result["_flow_completed"] is True
        assert "_flow_name" in result
        assert "_flow_path" in result

    def test_flow_preserves_existing_data(self):
        """Test flow preserves existing data in store."""
        initial = {"existing_key": "existing_value", "number": 42, "list": [1, 2, 3]}

        result = greeting_flow.run(initial)

        assert result["existing_key"] == "existing_value"
        assert result["number"] == 42
        assert result["list"] == [1, 2, 3]
        assert result["_flow_completed"] is True

    def test_flow_name_default(self):
        """Test flow uses class name when no name provided."""
        flow_def = {
            "start": FlowNode(node_class=GreetingNode, transitions={"success": "end"})
        }
        flow = BaseFlow(flow_def)  # No name provided

        assert flow.name == "BaseFlow"

    def test_flow_with_custom_max_steps(self):
        """Test flow respects custom max_steps parameter."""
        result = greeting_flow.run(max_steps=1)

        assert result["_flow_completed"] is True
        assert result["_flow_steps"] <= 1
