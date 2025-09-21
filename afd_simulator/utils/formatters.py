"""
Formatting utilities for AFD Simulator.

This module contains functions for formatting output, displaying
transition paths, and creating user-friendly representations
of AFD data structures.
"""

from typing import List, Tuple
from ..core.afd import AFD


def format_transition_path(transitions_path: List[Tuple[str, str, str]], 
                          input_string: str, is_accepted: bool) -> str:
    """
    Format the transition path for display to the user.
    
    Args:
        transitions_path: List of transitions taken during evaluation
        input_string: The input string that was evaluated
        is_accepted: Whether the string was accepted
        
    Returns:
        Formatted string showing the evaluation process
    """
    result = []
    result.append(f"Evaluating string: '{input_string}'")
    result.append("-" * 30)
    
    for i, (from_state, symbol, to_state) in enumerate(transitions_path, 1):
        result.append(f"{i}. From state ({from_state}) with symbol '{symbol}' "
                     f"transitions to state ({to_state}).")
    
    result.append("-" * 30)
    
    status = "ACCEPTED" if is_accepted else "REJECTED"
    result.append(f"✓ Result: The string '{input_string}' is {status}.")
    
    return "\n".join(result)


def format_afd_summary(afd: AFD) -> str:
    """
    Format a concise summary of an AFD definition.
    
    Args:
        afd: The AFD to summarize
        
    Returns:
        Formatted string with AFD summary
    """
    summary = []
    summary.append("AFD Summary:")
    summary.append(f"  States: {sorted(afd.states)}")
    summary.append(f"  Alphabet: {sorted(afd.alphabet)}")
    summary.append(f"  Initial State: {afd.initial_state}")
    summary.append(f"  Accepting States: {sorted(afd.accepting_states)}")
    summary.append(f"  Total Transitions: {len(afd.transitions)}")
    summary.append(f"  Valid: {afd.is_valid()}")
    
    return "\n".join(summary)


def format_accepted_strings(accepted_strings: List[str], max_display: int = 10) -> str:
    """
    Format a list of accepted strings for display.
    
    Args:
        accepted_strings: List of accepted strings
        max_display: Maximum number of strings to display
        
    Returns:
        Formatted string showing accepted strings
    """
    if not accepted_strings:
        return "No accepted strings found."
    
    result = []
    result.append("Accepted strings:")
    result.append("-" * 20)
    
    display_strings = accepted_strings[:max_display]
    for i, string in enumerate(display_strings, 1):
        result.append(f"{i:2d}. '{string}'")
    
    if len(accepted_strings) > max_display:
        result.append(f"... and {len(accepted_strings) - max_display} more")
    
    return "\n".join(result)


def format_menu_header(title: str, width: int = 60) -> str:
    """
    Format a menu header with consistent styling.
    
    Args:
        title: The title to display
        width: Width of the header line
        
    Returns:
        Formatted header string
    """
    lines = []
    lines.append("=" * width)
    lines.append(f"{title:^{width}}")
    lines.append("=" * width)
    return "\n".join(lines)


def format_section_header(title: str, width: int = 40) -> str:
    """
    Format a section header for sub-menus.
    
    Args:
        title: The section title
        width: Width of the header line
        
    Returns:
        Formatted section header
    """
    lines = []
    lines.append("\n" + "=" * width)
    lines.append(title)
    lines.append("=" * width)
    return "\n".join(lines)


def format_error_message(error: str, context: str = "") -> str:
    """
    Format an error message with consistent styling.
    
    Args:
        error: The error message
        context: Optional context information
        
    Returns:
        Formatted error message
    """
    if context:
        return f"✗ Error in {context}: {error}"
    else:
        return f"✗ Error: {error}"


def format_success_message(message: str, context: str = "") -> str:
    """
    Format a success message with consistent styling.
    
    Args:
        message: The success message
        context: Optional context information
        
    Returns:
        Formatted success message
    """
    if context:
        return f"✓ Success in {context}: {message}"
    else:
        return f"✓ {message}"


def format_help_text() -> str:
    """
    Format the help text for the application.
    
    Returns:
        Formatted help text
    """
    help_lines = [
        "HELP - AFD SIMULATOR",
        "=" * 40,
        "",
        "This simulator allows you to work with Deterministic Finite Automata (DFA).",
        "",
        "DFA Components:",
        "- States (Q): Finite set of state identifiers",
        "- Alphabet (Σ): Set of input symbols",
        "- Initial State (q₀): Starting state",
        "- Accepting States (F): States that accept the input",
        "- Transition Function (δ): Rules for state changes",
        "",
        "Key Features:",
        "1. Create and define complete DFA",
        "2. Evaluate strings with step-by-step visualization",
        "3. Generate accepted strings automatically",
        "4. Save and load DFA definitions",
        "5. Comprehensive validation",
        "",
        "Tips:",
        "- Use descriptive state names (e.g., q0, q1, q2)",
        "- Define all transitions for complete functionality",
        "- Test with various strings to verify behavior",
        "- Save your work frequently"
    ]
    
    return "\n".join(help_lines)
