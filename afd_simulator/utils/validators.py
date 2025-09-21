"""
Validation utilities for AFD Simulator.

This module contains functions for validating AFD definitions,
user inputs, and other data structures used in the simulator.
"""

from typing import List, Tuple, Optional, Set
from ..core.afd import AFD


def validate_afd_definition(afd: AFD) -> Tuple[bool, List[str]]:
    """
    Validate an AFD definition and return detailed error messages.
    
    Args:
        afd: The AFD instance to validate
        
    Returns:
        A tuple containing:
        - Boolean indicating if the AFD is valid
        - List of error messages (empty if valid)
    """
    errors = []
    
    # Check if states are defined
    if not afd.states:
        errors.append("No states defined")
    
    # Check if alphabet is defined
    if not afd.alphabet:
        errors.append("No alphabet defined")
    
    # Check if initial state is defined
    if afd.initial_state is None:
        errors.append("No initial state defined")
    elif afd.initial_state not in afd.states:
        errors.append(f"Initial state '{afd.initial_state}' is not in the set of states")
    
    # Check if accepting states are valid
    if not afd.accepting_states.issubset(afd.states):
        invalid_states = afd.accepting_states - afd.states
        errors.append(f"Some accepting states are not in the set of states: {invalid_states}")
    
    # Check for missing transitions
    missing_transitions = []
    for state in afd.states:
        for symbol in afd.alphabet:
            if (state, symbol) not in afd.transitions:
                missing_transitions.append(f"δ({state}, {symbol})")
    
    if missing_transitions:
        error_msg = f"Missing transitions: {', '.join(missing_transitions[:5])}"
        if len(missing_transitions) > 5:
            error_msg += f" ... and {len(missing_transitions) - 5} more"
        errors.append(error_msg)
    
    return len(errors) == 0, errors


def validate_string_input(input_string: str, alphabet: Set[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate that a string contains only symbols from the given alphabet.
    
    Args:
        input_string: The string to validate
        alphabet: The valid alphabet symbols
        
    Returns:
        A tuple containing:
        - Boolean indicating if the string is valid
        - Error message if invalid, None if valid
    """
    if not input_string:
        return True, None
    
    invalid_symbols = []
    for symbol in input_string:
        if symbol not in alphabet:
            invalid_symbols.append(symbol)
    
    if invalid_symbols:
        return False, f"String contains invalid symbols: {set(invalid_symbols)}"
    
    return True, None


def validate_state_name(state_name: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a state name for proper formatting.
    
    Args:
        state_name: The state name to validate
        
    Returns:
        A tuple containing:
        - Boolean indicating if the state name is valid
        - Error message if invalid, None if valid
    """
    if not state_name or not state_name.strip():
        return False, "State name cannot be empty"
    
    if len(state_name.strip()) != len(state_name):
        return False, "State name cannot have leading or trailing whitespace"
    
    # Check for invalid characters (basic validation)
    invalid_chars = [' ', ',', ';', ':', '"', "'"]
    for char in invalid_chars:
        if char in state_name:
            return False, f"State name cannot contain '{char}'"
    
    return True, None


def validate_symbol(symbol: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a symbol for the alphabet.
    
    Args:
        symbol: The symbol to validate
        
    Returns:
        A tuple containing:
        - Boolean indicating if the symbol is valid
        - Error message if invalid, None if valid
    """
    if not symbol or not symbol.strip():
        return False, "Symbol cannot be empty"
    
    if len(symbol.strip()) != len(symbol):
        return False, "Symbol cannot have leading or trailing whitespace"
    
    if len(symbol) != 1:
        return False, "Symbol must be a single character"
    
    # Check for invalid characters
    invalid_chars = [' ', ',', ';', ':', '"', "'"]
    for char in invalid_chars:
        if char in symbol:
            return False, f"Symbol cannot contain '{char}'"
    
    return True, None


def validate_transition_input(from_state: str, symbol: str, to_state: str, 
                            valid_states: Set[str], valid_symbols: Set[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate transition input parameters.
    
    Args:
        from_state: Source state of the transition
        symbol: Input symbol
        to_state: Destination state
        valid_states: Set of valid state names
        valid_symbols: Set of valid symbols
        
    Returns:
        A tuple containing:
        - Boolean indicating if the transition is valid
        - Error message if invalid, None if valid
    """
    # Validate from_state
    if from_state not in valid_states:
        return False, f"Source state '{from_state}' is not valid"
    
    # Validate symbol
    if symbol not in valid_symbols:
        return False, f"Symbol '{symbol}' is not in the alphabet"
    
    # Validate to_state
    if to_state not in valid_states:
        return False, f"Destination state '{to_state}' is not valid"
    
    return True, None
