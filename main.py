#!/usr/bin/env python3
"""
Main entry point for the AFD Simulator application.

This script provides the main entry point for running the AFD Simulator
with the modular architecture.
"""

import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from afd_simulator import AFDSimulator


def main():
    """Main entry point of the application."""
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
    main()
