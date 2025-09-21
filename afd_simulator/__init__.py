"""
AFD Simulator - Deterministic Finite Automaton Simulator Package

A comprehensive Python package for simulating Deterministic Finite Automata (DFA).
This package provides tools for defining, evaluating, and managing DFAs with
an interactive user interface.

Modules:
- core: Core AFD implementation and algorithms
- ui: User interface components
- utils: Utility functions and helpers
- examples: Example AFD definitions and demonstrations
"""

__version__ = "1.0.0"
__author__ = "AFD Simulator Team"

# Import main classes for easy access
from .core.afd import AFD
from .ui.simulator import AFDSimulator

# Import GUI classes (optional - may not be available on all systems)
try:
    from .gui.main_window import AFDSimulatorGUI
    __all__ = ["AFD", "AFDSimulator", "AFDSimulatorGUI"]
except ImportError:
    __all__ = ["AFD", "AFDSimulator"]
