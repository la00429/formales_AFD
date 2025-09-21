"""
Example loader for AFD Simulator.

This module provides functionality to load example AFD definitions
from files and manage example collections.
"""

import os
from typing import List, Optional
from ..core.afd import AFD


class ExampleLoader:
    """
    Handles loading and management of example AFD definitions.
    """
    
    def __init__(self, examples_directory: str = "examples"):
        """
        Initialize the example loader.
        
        Args:
            examples_directory: Directory containing example files
        """
        self.examples_directory = examples_directory
    
    def get_available_examples(self) -> List[str]:
        """
        Get a list of available example files.
        
        Returns:
            List of example filenames (without extension)
        """
        if not os.path.exists(self.examples_directory):
            return []
        
        examples = []
        for filename in os.listdir(self.examples_directory):
            if filename.endswith('.json'):
                examples.append(filename[:-5])  # Remove .json extension
        
        return sorted(examples)
    
    def load_example(self, example_name: str) -> AFD:
        """
        Load an example AFD from file.
        
        Args:
            example_name: Name of the example to load
            
        Returns:
            AFD instance loaded from the example file
            
        Raises:
            FileNotFoundError: If the example file is not found
            Exception: If there's an error loading the file
        """
        filename = os.path.join(self.examples_directory, f"{example_name}.json")
        
        if not os.path.exists(filename):
            available = self.get_available_examples()
            raise FileNotFoundError(f"Example '{example_name}' not found. Available examples: {available}")
        
        return AFD.load_from_file(filename)
    
    def save_example(self, afd: AFD, example_name: str) -> None:
        """
        Save an AFD as an example.
        
        Args:
            afd: The AFD to save
            example_name: Name for the example file
        """
        if not os.path.exists(self.examples_directory):
            os.makedirs(self.examples_directory)
        
        filename = os.path.join(self.examples_directory, f"{example_name}.json")
        afd.save_to_file(filename)
    
    def get_example_info(self, example_name: str) -> dict:
        """
        Get information about an example AFD without loading it.
        
        Args:
            example_name: Name of the example
            
        Returns:
            Dictionary with example information
            
        Raises:
            FileNotFoundError: If the example file is not found
        """
        filename = os.path.join(self.examples_directory, f"{example_name}.json")
        
        if not os.path.exists(filename):
            available = self.get_available_examples()
            raise FileNotFoundError(f"Example '{example_name}' not found. Available examples: {available}")
        
        # Load and return summary information
        afd = AFD.load_from_file(filename)
        
        return {
            "name": example_name,
            "states": len(afd.states),
            "alphabet_size": len(afd.alphabet),
            "transitions": len(afd.transitions),
            "accepting_states": len(afd.accepting_states),
            "valid": afd.is_valid()
        }
