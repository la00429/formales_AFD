#!/usr/bin/env python3
"""
Main entry point for the AFD Simulator GUI application.

This script launches the graphical user interface version of the AFD Simulator
using Tkinter for a modern, visual experience.
"""

import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from afd_simulator.gui import AFDSimulatorGUI


def main():
    """Main entry point for the GUI application."""
    try:
        print("Starting AFD Simulator GUI...")
        app = AFDSimulatorGUI()
        app.run()
    except ImportError as e:
        print(f"Error: Tkinter is not available on this system: {e}")
        print("Please install Python with Tkinter support.")
        sys.exit(1)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
