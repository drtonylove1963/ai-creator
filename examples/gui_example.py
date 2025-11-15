"""
Example of launching the AI Creator GUI programmatically.

This demonstrates how to launch the GUI from within your own Python scripts.
"""

from ai_creator.gui import launch_gui


def main():
    """Launch the GUI with custom settings."""
    print("Launching AI Creator GUI...")
    print("This will open a web interface in your browser.")
    print()
    print("Features available:")
    print("  • Single Agent Execution")
    print("  • Multi-Agent Orchestration")
    print("  • Agent Tools Explorer")
    print("  • Execution History Viewer")
    print()

    # Launch the GUI
    # Set share=True to create a public link (useful for demos)
    # Set server_port to change the port (default is 7860)
    launch_gui(
        share=False,      # Set to True for public link
        server_port=7860  # Change port if needed
    )


if __name__ == "__main__":
    main()
