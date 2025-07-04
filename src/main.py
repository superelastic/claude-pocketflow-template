"""Main entry point for the PocketFlow example application."""
# ruff: noqa: T201, DTZ005, PLR2004

import logging
import sys
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.flows.examples import (
    data_pipeline_flow,
    greeting_flow,
    random_conditional_flow,
)


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def run_greeting_example():
    """Run the greeting flow example."""
    print("\n" + "=" * 50)
    print("🎯 Running Greeting Flow Example")
    print("=" * 50 + "\n")

    # Determine time of day
    hour = datetime.now().hour
    if hour < 12:
        time_of_day = "morning"
    elif hour < 17:
        time_of_day = "afternoon"
    else:
        time_of_day = "evening"

    # Run the flow
    result = greeting_flow.run({"name": "Developer", "time_of_day": time_of_day})

    if result.get("action") == "success":
        print(f"✅ {result['greeting']}")
        print(f"📊 Metadata: {result.get('greeting_metadata', {})}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")

    return result


def run_random_conditional_example():
    """Run the random number conditional flow example."""
    print("\n" + "=" * 50)
    print("🎲 Running Random Conditional Flow Example")
    print("=" * 50 + "\n")

    # Set up the flow with random number generation and conditional logic
    initial_store = {
        "min_value": 1,
        "max_value": 100,
        "threshold": 50,
        # For the transform nodes
        "input_data": ["apple", "banana", "cherry"],
        "transform_type": "uppercase",
    }

    result = random_conditional_flow.run(initial_store)

    print(f"🔢 Generated number: {result.get('random_number', 'N/A')}")
    print(f"📝 {result.get('message', '')}")

    if "transformed_data" in result:
        print(f"🔄 Transformed data: {result['transformed_data']}")

    print(f"\n📍 Flow path: {' -> '.join(result.get('_flow_path', []))}")

    return result


def run_data_pipeline_example():
    """Run the data processing pipeline example."""
    print("\n" + "=" * 50)
    print("🔄 Running Data Pipeline Flow Example")
    print("=" * 50 + "\n")

    # Set up a multi-stage data transformation
    initial_store = {
        "input_data": ["hello", "world", "from", "pocketflow"],
        "transform_type": "uppercase",
    }

    # First transform will uppercase
    result = data_pipeline_flow.run(initial_store)

    # For the second transform, we'll reverse
    if "_flow_path" in result and len(result["_flow_path"]) > 1:
        # This is a simple example - in real flows, nodes would handle this
        result["input_data"] = result.get("transformed_data", [])
        result["transform_type"] = "reverse"

    print("📊 Pipeline Results:")
    print(f"  - Original: {initial_store['input_data']}")
    print(f"  - Transformed: {result.get('transformed_data', 'N/A')}")
    print(f"  - Transform stats: {result.get('transform_stats', {})}")
    print(f"  - Flow completed: {result.get('_flow_completed', False)}")

    return result


def main():
    """Run all examples."""
    setup_logging()

    print("\n🚀 Welcome to PocketFlow Examples!")
    print("This demonstrates the basic concepts of nodes and flows.\n")

    # Run examples
    results = []

    results.append(run_greeting_example())
    results.append(run_random_conditional_example())
    results.append(run_data_pipeline_example())

    # Summary
    print("\n" + "=" * 50)
    print("📋 Summary")
    print("=" * 50)

    successful = sum(1 for r in results if r.get("_flow_completed", False))
    print(f"\n✅ Completed flows: {successful}/{len(results)}")

    print("\n🎉 Examples completed!")
    print("\n💡 Next steps:")
    print("  - Check out src/nodes/examples.py to see node implementations")
    print("  - Look at src/flows/examples.py to understand flow definitions")
    print("  - Read DEVELOPMENT_GUIDE.md for the complete methodology")
    print("  - Start building your own nodes and flows!")


if __name__ == "__main__":
    main()
