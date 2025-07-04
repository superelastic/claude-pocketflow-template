"""Example flow implementations."""

from src.flows.base import BaseFlow, FlowNode
from src.nodes.examples import (
    ConditionalNode,
    DataTransformNode,
    GreetingNode,
    RandomNumberNode,
)

# Simple greeting flow
greeting_flow_definition = {
    "start": FlowNode(
        node_class=GreetingNode, transitions={"success": "end", "error": "end"}
    )
}

greeting_flow = BaseFlow(greeting_flow_definition, name="GreetingFlow")


# Random number with conditional branching
random_conditional_flow_definition = {
    "start": FlowNode(
        node_class=RandomNumberNode,
        transitions={"success": "check_threshold", "error": "end"},
    ),
    "check_threshold": FlowNode(
        node_class=ConditionalNode,
        transitions={
            "above_threshold": "high_value_handler",
            "below_threshold": "low_value_handler",
            "at_threshold": "end",
        },
    ),
    "high_value_handler": FlowNode(
        node_class=DataTransformNode, transitions={"success": "end", "error": "end"}
    ),
    "low_value_handler": FlowNode(
        node_class=DataTransformNode, transitions={"success": "end", "error": "end"}
    ),
}

random_conditional_flow = BaseFlow(
    random_conditional_flow_definition, name="RandomConditionalFlow"
)


# Data processing pipeline
data_pipeline_flow_definition = {
    "start": FlowNode(
        node_class=DataTransformNode,
        transitions={"success": "second_transform", "error": "error_handler"},
    ),
    "second_transform": FlowNode(
        node_class=DataTransformNode,
        transitions={"success": "final_transform", "error": "error_handler"},
    ),
    "final_transform": FlowNode(
        node_class=DataTransformNode,
        transitions={"success": "end", "error": "error_handler"},
    ),
    "error_handler": FlowNode(
        node_class=GreetingNode,  # Reusing as a simple logger
        transitions={"success": "end", "error": "end"},
    ),
}

data_pipeline_flow = BaseFlow(data_pipeline_flow_definition, name="DataPipelineFlow")
