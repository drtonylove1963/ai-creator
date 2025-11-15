#!/usr/bin/env python3
"""
Launch script for AI Creator GUI.

This script launches the web-based GUI interface for AI Creator.
"""

import argparse
from ai_creator.gui import launch_gui


def main():
    """Main entry point for GUI launcher."""
    parser = argparse.ArgumentParser(
        description="Launch AI Creator GUI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Launch on default port (7860)
  python launch_gui.py

  # Launch on custom port
  python launch_gui.py --port 8080

  # Create public shareable link
  python launch_gui.py --share

  # Launch with custom settings
  python launch_gui.py --port 8080 --share
        """
    )

    parser.add_argument(
        "--port",
        type=int,
        default=7860,
        help="Port to run the server on (default: 7860)"
    )

    parser.add_argument(
        "--share",
        action="store_true",
        help="Create a public shareable link (default: False)"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode (default: False)"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("🤖 AI Creator - Agent System GUI")
    print("=" * 60)
    print(f"Server starting on port {args.port}...")
    if args.share:
        print("⚠️  Share mode enabled - creating public link")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    print()

    try:
        launch_gui(share=args.share, server_port=args.port)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
