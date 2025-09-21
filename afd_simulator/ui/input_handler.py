"""
Input handling utilities for AFD Simulator.

This module contains classes and functions for handling user input
with proper validation and error handling.
"""

from typing import Optional, List, Set, Tuple
from ..utils.validators import (
    validate_state_name, 
    validate_symbol, 
    validate_transition_input,
    validate_string_input
)


class InputHandler:
    """
    Handles user input with validation and error recovery.
    """
    
    def __init__(self):
        """Initialize the input handler."""
        pass
    
    def get_user_input(self, prompt: str, default: str = "") -> str:
        """
        Get input from user with error handling.
        
        Args:
            prompt: The prompt to display to the user
            default: Default value if input is empty
            
        Returns:
            User input string
        """
        try:
            user_input = input(prompt).strip()
            return user_input if user_input else default
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return ""
        except EOFError:
            print("\nEnd of input reached.")
            return ""
    
    def get_yes_no_input(self, prompt: str) -> bool:
        """
        Get yes/no input from user.
        
        Args:
            prompt: The prompt to display to the user
            
        Returns:
            True if user responds yes, False otherwise
        """
        while True:
            response = self.get_user_input(prompt + " (y/n): ").lower()
            if response in ['y', 'yes', 's', 'si']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")
    
    def get_state_names(self, prompt: str) -> List[str]:
        """
        Get state names from user input with validation.
        
        Args:
            prompt: The prompt to display to the user
            
        Returns:
            List of validated state names
        """
        while True:
            states_input = self.get_user_input(prompt)
            if not states_input:
                return []
            
            states = states_input.split()
            valid_states = []
            errors = []
            
            for state in states:
                is_valid, error = validate_state_name(state)
                if is_valid:
                    valid_states.append(state)
                else:
                    errors.append(f"'{state}': {error}")
            
            if errors:
                print("Invalid state names:")
                for error in errors:
                    print(f"  {error}")
                print("Please try again.")
                continue
            
            return valid_states
    
    def get_alphabet_symbols(self, prompt: str) -> List[str]:
        """
        Get alphabet symbols from user input with validation.
        
        Args:
            prompt: The prompt to display to the user
            
        Returns:
            List of validated symbols
        """
        while True:
            symbols_input = self.get_user_input(prompt)
            if not symbols_input:
                return []
            
            symbols = symbols_input.split()
            valid_symbols = []
            errors = []
            
            for symbol in symbols:
                is_valid, error = validate_symbol(symbol)
                if is_valid:
                    valid_symbols.append(symbol)
                else:
                    errors.append(f"'{symbol}': {error}")
            
            if errors:
                print("Invalid symbols:")
                for error in errors:
                    print(f"  {error}")
                print("Please try again.")
                continue
            
            return valid_symbols
    
    def get_initial_state(self, prompt: str, valid_states: Set[str]) -> Optional[str]:
        """
        Get initial state from user with validation.
        
        Args:
            prompt: The prompt to display to the user
            valid_states: Set of valid state names
            
        Returns:
            Valid initial state name or None if cancelled
        """
        while True:
            initial_state = self.get_user_input(prompt)
            if not initial_state:
                return None
            
            if initial_state in valid_states:
                return initial_state
            else:
                print(f"State '{initial_state}' is not valid.")
                print(f"Valid states: {sorted(valid_states)}")
    
    def get_accepting_states(self, prompt: str, valid_states: Set[str]) -> List[str]:
        """
        Get accepting states from user with validation.
        
        Args:
            prompt: The prompt to display to the user
            valid_states: Set of valid state names
            
        Returns:
            List of valid accepting states
        """
        while True:
            accepting_input = self.get_user_input(prompt)
            if not accepting_input:
                return []
            
            accepting_states = accepting_input.split()
            valid_accepting = []
            errors = []
            
            for state in accepting_states:
                if state in valid_states:
                    valid_accepting.append(state)
                else:
                    errors.append(f"'{state}' is not a valid state")
            
            if errors:
                print("Invalid accepting states:")
                for error in errors:
                    print(f"  {error}")
                print(f"Valid states: {sorted(valid_states)}")
                continue
            
            return valid_accepting
    
    def get_transition(self, prompt: str, valid_states: Set[str], 
                      valid_symbols: Set[str]) -> Optional[Tuple[str, str, str]]:
        """
        Get a single transition from user with validation.
        
        Args:
            prompt: The prompt to display to the user
            valid_states: Set of valid state names
            valid_symbols: Set of valid symbols
            
        Returns:
            Tuple of (from_state, symbol, to_state) or None if cancelled
        """
        while True:
            transition_input = self.get_user_input(prompt)
            if not transition_input or transition_input.lower() == 'done':
                return None
            
            parts = transition_input.split()
            if len(parts) != 3:
                print("Invalid format. Use: from_state symbol to_state")
                continue
            
            from_state, symbol, to_state = parts
            is_valid, error = validate_transition_input(
                from_state, symbol, to_state, valid_states, valid_symbols
            )
            
            if is_valid:
                return (from_state, symbol, to_state)
            else:
                print(f"Invalid transition: {error}")
    
    def get_string_for_evaluation(self, prompt: str, alphabet: Set[str]) -> Optional[str]:
        """
        Get a string for evaluation with validation.
        
        Args:
            prompt: The prompt to display to the user
            alphabet: Valid alphabet symbols
            
        Returns:
            Valid string for evaluation or None if cancelled
        """
        while True:
            input_string = self.get_user_input(prompt)
            if not input_string:
                return None
            
            is_valid, error = validate_string_input(input_string, alphabet)
            if is_valid:
                return input_string
            else:
                print(f"Invalid string: {error}")
                print(f"Valid symbols: {sorted(alphabet)}")
    
    def get_filename(self, prompt: str, extension: str = ".json") -> str:
        """
        Get a filename from user with optional extension.
        
        Args:
            prompt: The prompt to display to the user
            extension: Default file extension to add if not provided
            
        Returns:
            Filename with proper extension
        """
        filename = self.get_user_input(prompt)
        if not filename:
            return ""
        
        if not filename.endswith(extension):
            filename += extension
        
        return filename
