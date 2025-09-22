"""
Console application entry point for AFD Simulator.

This module provides the main entry point for the console-based
AFD Simulator application.
"""

import sys
from ..ui.simulator import AFDSimulator


def run_console_app():
    """Run the console AFD Simulator application."""
    try:
        simulator = AFDSimulator()
        simulator.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_console_app()
