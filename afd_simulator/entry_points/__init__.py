"""
Entry points module for AFD Simulator.

This module contains the main entry point functions
for different interfaces of the AFD Simulator.
"""

from .console_app import run_console_app
from .gui_app import run_gui_app
from .demo_app import run_demo_app

__all__ = ["run_console_app", "run_gui_app", "run_demo_app"]
