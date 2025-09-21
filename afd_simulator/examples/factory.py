"""
AFD Factory for creating common AFD patterns.

This module provides factory functions to create common types of
Deterministic Finite Automata for educational and demonstration purposes.
"""

from typing import List
from ..core.afd import AFD


class AFDFactory:
    """
    Factory class for creating common AFD patterns.
    """
    
    @staticmethod
    def create_binary_ending_with_one() -> AFD:
        """
        Create an AFD that accepts binary strings ending with '1'.
        
        Returns:
            AFD instance that accepts strings ending with '1'
        """
        afd = AFD()
        
        # Add states
        afd.add_state("q0")
        afd.add_state("q1")
        
        # Add alphabet
        afd.add_symbol("0")
        afd.add_symbol("1")
        
        # Set initial state
        afd.set_initial_state("q0")
        
        # Set accepting states
        afd.add_accepting_state("q1")
        
        # Add transitions
        afd.add_transition("q0", "0", "q0")
        afd.add_transition("q0", "1", "q1")
        afd.add_transition("q1", "0", "q1")
        afd.add_transition("q1", "1", "q1")
        
        return afd
    
    @staticmethod
    def create_even_length_strings() -> AFD:
        """
        Create an AFD that accepts strings of even length.
        
        Returns:
            AFD instance that accepts even-length strings
        """
        afd = AFD()
        
        # Add states
        afd.add_state("q0")  # Even length
        afd.add_state("q1")  # Odd length
        
        # Add alphabet
        afd.add_symbol("a")
        afd.add_symbol("b")
        
        # Set initial state
        afd.set_initial_state("q0")
        
        # Set accepting states
        afd.add_accepting_state("q0")
        
        # Add transitions
        afd.add_transition("q0", "a", "q1")
        afd.add_transition("q0", "b", "q1")
        afd.add_transition("q1", "a", "q0")
        afd.add_transition("q1", "b", "q0")
        
        return afd
    
    @staticmethod
    def create_strings_ending_with_01() -> AFD:
        """
        Create an AFD that accepts binary strings ending with '01'.
        
        Returns:
            AFD instance that accepts strings ending with '01'
        """
        afd = AFD()
        
        # Add states
        afd.add_state("q0")  # No pattern yet
        afd.add_state("q1")  # Last symbol was '0'
        afd.add_state("q2")  # Last symbols were '01'
        
        # Add alphabet
        afd.add_symbol("0")
        afd.add_symbol("1")
        
        # Set initial state
        afd.set_initial_state("q0")
        
        # Set accepting states
        afd.add_accepting_state("q2")
        
        # Add transitions
        afd.add_transition("q0", "0", "q1")
        afd.add_transition("q0", "1", "q0")
        afd.add_transition("q1", "0", "q1")
        afd.add_transition("q1", "1", "q2")
        afd.add_transition("q2", "0", "q1")
        afd.add_transition("q2", "1", "q0")
        
        return afd
    
    @staticmethod
    def create_exactly_two_as() -> AFD:
        """
        Create an AFD that accepts strings with exactly two 'a's.
        
        Returns:
            AFD instance that accepts strings with exactly two 'a's
        """
        afd = AFD()
        
        # Add states
        afd.add_state("q0")  # No 'a's yet
        afd.add_state("q1")  # One 'a'
        afd.add_state("q2")  # Two 'a's
        afd.add_state("q3")  # More than two 'a's
        
        # Add alphabet
        afd.add_symbol("a")
        afd.add_symbol("b")
        
        # Set initial state
        afd.set_initial_state("q0")
        
        # Set accepting states
        afd.add_accepting_state("q2")
        
        # Add transitions
        afd.add_transition("q0", "a", "q1")
        afd.add_transition("q0", "b", "q0")
        afd.add_transition("q1", "a", "q2")
        afd.add_transition("q1", "b", "q1")
        afd.add_transition("q2", "a", "q3")
        afd.add_transition("q2", "b", "q2")
        afd.add_transition("q3", "a", "q3")
        afd.add_transition("q3", "b", "q3")
        
        return afd
    
    @staticmethod
    def create_strings_with_substring_ab() -> AFD:
        """
        Create an AFD that accepts strings containing the substring 'ab'.
        
        Returns:
            AFD instance that accepts strings containing 'ab'
        """
        afd = AFD()
        
        # Add states
        afd.add_state("q0")  # No pattern yet
        afd.add_state("q1")  # Last symbol was 'a'
        afd.add_state("q2")  # Found 'ab'
        
        # Add alphabet
        afd.add_symbol("a")
        afd.add_symbol("b")
        
        # Set initial state
        afd.set_initial_state("q0")
        
        # Set accepting states
        afd.add_accepting_state("q2")
        
        # Add transitions
        afd.add_transition("q0", "a", "q1")
        afd.add_transition("q0", "b", "q0")
        afd.add_transition("q1", "a", "q1")
        afd.add_transition("q1", "b", "q2")
        afd.add_transition("q2", "a", "q2")
        afd.add_transition("q2", "b", "q2")
        
        return afd
    
    @staticmethod
    def get_available_examples() -> List[tuple]:
        """
        Get a list of available example AFDs.
        
        Returns:
            List of tuples containing (name, description, factory_method)
        """
        return [
            ("binary_ending_one", "Binary strings ending with '1'", AFDFactory.create_binary_ending_with_one),
            ("even_length", "Strings of even length", AFDFactory.create_even_length_strings),
            ("ending_01", "Binary strings ending with '01'", AFDFactory.create_strings_ending_with_01),
            ("exactly_two_as", "Strings with exactly two 'a's", AFDFactory.create_exactly_two_as),
            ("contains_ab", "Strings containing substring 'ab'", AFDFactory.create_strings_with_substring_ab)
        ]
    
    @staticmethod
    def create_example_by_name(name: str) -> AFD:
        """
        Create an example AFD by name.
        
        Args:
            name: The name of the example to create
            
        Returns:
            AFD instance of the requested example
            
        Raises:
            ValueError: If the example name is not found
        """
        examples = AFDFactory.get_available_examples()
        
        for example_name, _, factory_method in examples:
            if example_name == name:
                return factory_method()
        
        available_names = [name for name, _, _ in examples]
        raise ValueError(f"Example '{name}' not found. Available examples: {available_names}")
