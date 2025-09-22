"""
Data module for AFD Simulator.

This module contains data files, examples, and resources
used by the AFD Simulator application.
"""

import os

# Get the directory containing this file
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Example AFD files
EXAMPLE_FILES = {
    "binary_afd": "binary_afd.json",
    "even_length": "even_length.json", 
    "ends_with_01": "ends_with_01.json",
    "exactly_two_as": "exactly_two_as.json"
}

def get_example_path(example_name: str) -> str:
    """
    Get the full path to an example AFD file.
    
    Args:
        example_name: Name of the example file
        
    Returns:
        Full path to the example file
    """
    if example_name in EXAMPLE_FILES:
        return os.path.join(DATA_DIR, EXAMPLE_FILES[example_name])
    else:
        raise ValueError(f"Unknown example: {example_name}")

def get_available_examples() -> list:
    """
    Get list of available example names.
    
    Returns:
        List of example names
    """
    return list(EXAMPLE_FILES.keys())

__all__ = ["DATA_DIR", "EXAMPLE_FILES", "get_example_path", "get_available_examples"]
