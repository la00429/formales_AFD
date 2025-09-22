#!/usr/bin/env python3
"""
AFD Simulator - Main Launcher

This script provides a simple way to launch the AFD Simulator
in different modes without using the module interface.
"""

import sys
import argparse


def main():
    """Main launcher for AFD Simulator."""
    parser = argparse.ArgumentParser(
        description="AFD Simulator - Deterministic Finite Automaton Simulator",
        epilog="For more options, use: python -m afd_simulator"
    )
    parser.add_argument("--gui", action="store_true", help="Launch GUI interface")
    parser.add_argument("--demo", action="store_true", help="Run demonstration mode")
    parser.add_argument("--console", action="store_true", help="Launch console interface (default)")
    
    args = parser.parse_args()
    
    try:
        if args.gui:
            from afd_simulator.entry_points.gui_app import run_gui_app
            run_gui_app()
        elif args.demo:
            from afd_simulator.entry_points.demo_app import run_demo_app
            run_demo_app()
        else:
            # Default to console interface
            from afd_simulator.entry_points.console_app import run_console_app
            run_console_app()
    except ImportError as e:
        print(f"Error: {e}")
        print("Make sure the afd_simulator package is properly installed.")
        sys.exit(1)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
