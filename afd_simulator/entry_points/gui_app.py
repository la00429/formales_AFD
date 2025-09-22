"""
GUI application entry point for AFD Simulator.

This module provides the main entry point for the graphical
AFD Simulator application using Tkinter.
"""

import sys

try:
    from ..gui.main_window import AFDSimulatorGUI
except ImportError:
    print("Error: Tkinter is not available on this system.")
    print("Please install Python with Tkinter support.")
    sys.exit(1)


def run_gui_app():
    """Run the GUI AFD Simulator application."""
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
    run_gui_app()
