"""
Main module for AFD Simulator package.

This allows running the package with: python -m afd_simulator
"""

import sys
import argparse
from .entry_points import run_console_app, run_gui_app, run_demo_app


def main():
    """Main entry point when running as module."""
    parser = argparse.ArgumentParser(description="AFD Simulator - Deterministic Finite Automaton Simulator")
    parser.add_argument("--gui", action="store_true", help="Run GUI interface")
    parser.add_argument("--demo", action="store_true", help="Run demo mode")
    parser.add_argument("--console", action="store_true", help="Run console interface (default)")
    
    args = parser.parse_args()
    
    if args.gui:
        run_gui_app()
    elif args.demo:
        run_demo_app()
    else:
        # Default to console interface
        run_console_app()


if __name__ == "__main__":
    main()
