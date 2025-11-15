"""
Basic usage example for AI Creator.

This script demonstrates the basic functionality of the AI Creator toolkit.
"""

from ai_creator import Creator


def main():
    """Main example function."""
    print("AI Creator - Basic Usage Example")
    print("=" * 50)

    # Initialize the creator
    creator = Creator()

    # Example 1: Text generation
    print("\n1. Text Generation:")
    prompt = "Create a short poem about artificial intelligence"
    result = creator.generate(prompt)
    print(f"Prompt: {prompt}")
    print(f"Result: {result}")

    # Example 2: Image creation
    print("\n2. Image Creation:")
    description = "A futuristic cityscape at sunset"
    image_path = creator.create_image(description)
    print(f"Description: {description}")
    print(f"Image: {image_path}")

    # Example 3: Content analysis
    print("\n3. Content Analysis:")
    content = "Artificial intelligence is transforming the world."
    analysis = creator.analyze(content)
    print(f"Content: {content}")
    print(f"Analysis: {analysis}")

    print("\n" + "=" * 50)
    print("Example completed!")


if __name__ == "__main__":
    main()
