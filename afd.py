"""
Deterministic Finite Automaton (DFA) Implementation

This module contains the AFD class that represents a deterministic finite automaton
with all five required components: states (Q), alphabet (Σ), initial state (q₀),
accepting states (F), and transition function (δ).
"""

import json
from typing import Set, Dict, List, Tuple, Optional


class AFD:
    """
    Represents a Deterministic Finite Automaton (DFA).
    
    A DFA is defined by the 5-tuple (Q, Σ, δ, q₀, F) where:
    - Q: Finite set of states
    - Σ: Alphabet (set of input symbols)
    - δ: Transition function Q × Σ → Q
    - q₀: Initial state
    - F: Set of accepting states
    """
    
    def __init__(self):
        """Initialize an empty AFD."""
        self.states: Set[str] = set()
        self.alphabet: Set[str] = set()
        self.initial_state: Optional[str] = None
        self.accepting_states: Set[str] = set()
        self.transitions: Dict[Tuple[str, str], str] = {}
    
    def add_state(self, state: str) -> None:
        """
        Add a state to the AFD.
        
        Args:
            state: The state identifier to add
        """
        self.states.add(state)
    
    def add_symbol(self, symbol: str) -> None:
        """
        Add a symbol to the alphabet.
        
        Args:
            symbol: The symbol to add to the alphabet
        """
        self.alphabet.add(symbol)
    
    def set_initial_state(self, state: str) -> None:
        """
        Set the initial state of the AFD.
        
        Args:
            state: The initial state identifier
            
        Raises:
            ValueError: If the state is not in the set of states
        """
        if state not in self.states:
            raise ValueError(f"State '{state}' is not in the set of states")
        self.initial_state = state
    
    def add_accepting_state(self, state: str) -> None:
        """
        Add a state to the set of accepting states.
        
        Args:
            state: The accepting state identifier
            
        Raises:
            ValueError: If the state is not in the set of states
        """
        if state not in self.states:
            raise ValueError(f"State '{state}' is not in the set of states")
        self.accepting_states.add(state)
    
    def add_transition(self, from_state: str, symbol: str, to_state: str) -> None:
        """
        Add a transition to the transition function.
        
        Args:
            from_state: Source state of the transition
            symbol: Input symbol that triggers the transition
            to_state: Destination state of the transition
            
        Raises:
            ValueError: If any of the states or symbol are not defined
        """
        if from_state not in self.states:
            raise ValueError(f"Source state '{from_state}' is not in the set of states")
        if to_state not in self.states:
            raise ValueError(f"Destination state '{to_state}' is not in the set of states")
        if symbol not in self.alphabet:
            raise ValueError(f"Symbol '{symbol}' is not in the alphabet")
        
        self.transitions[(from_state, symbol)] = to_state
    
    def is_valid(self) -> bool:
        """
        Check if the AFD is properly defined.
        
        Returns:
            True if the AFD is valid, False otherwise
        """
        # Check if all required components are defined
        if not self.states:
            return False
        if not self.alphabet:
            return False
        if self.initial_state is None:
            return False
        if self.initial_state not in self.states:
            return False
        if not self.accepting_states.issubset(self.states):
            return False
        
        # Check if all transitions are defined for all state-symbol pairs
        for state in self.states:
            for symbol in self.alphabet:
                if (state, symbol) not in self.transitions:
                    return False
        
        return True
    
    def evaluate_string(self, input_string: str) -> Tuple[bool, List[Tuple[str, str, str]]]:
        """
        Evaluate if a string is accepted by the AFD.
        
        Args:
            input_string: The string to evaluate
            
        Returns:
            A tuple containing:
            - Boolean indicating if the string is accepted
            - List of transitions showing the path taken
            
        Raises:
            ValueError: If the AFD is not valid or contains invalid symbols
        """
        if not self.is_valid():
            raise ValueError("AFD is not properly defined")
        
        # Check if all symbols in the string are in the alphabet
        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError(f"Symbol '{symbol}' is not in the alphabet")
        
        # Simulate the AFD
        current_state = self.initial_state
        transitions_path = []
        
        for symbol in input_string:
            next_state = self.transitions.get((current_state, symbol))
            if next_state is None:
                raise ValueError(f"No transition defined for state '{current_state}' with symbol '{symbol}'")
            
            transitions_path.append((current_state, symbol, next_state))
            current_state = next_state
        
        # Check if final state is accepting
        is_accepted = current_state in self.accepting_states
        
        return is_accepted, transitions_path
    
    def generate_accepted_strings(self, max_count: int = 10) -> List[str]:
        """
        Generate the first n shortest strings accepted by the AFD.
        
        Args:
            max_count: Maximum number of strings to generate
            
        Returns:
            List of accepted strings in order of length
            
        Raises:
            ValueError: If the AFD is not valid
        """
        if not self.is_valid():
            raise ValueError("AFD is not properly defined")
        
        accepted_strings = []
        alphabet_list = list(self.alphabet)
        
        # Use BFS to find shortest paths to accepting states
        queue = [("", self.initial_state)]
        visited = set()
        
        while queue and len(accepted_strings) < max_count:
            current_string, current_state = queue.pop(0)
            
            # Skip if we've already visited this state with this string length
            state_length_key = (current_state, len(current_string))
            if state_length_key in visited:
                continue
            visited.add(state_length_key)
            
            # If current state is accepting, add string to results
            if current_state in self.accepting_states and current_string:
                accepted_strings.append(current_string)
            
            # Add transitions for each symbol
            for symbol in alphabet_list:
                next_state = self.transitions.get((current_state, symbol))
                if next_state is not None:
                    next_string = current_string + symbol
                    queue.append((next_string, next_state))
        
        return accepted_strings[:max_count]
    
    def save_to_file(self, filename: str) -> None:
        """
        Save the AFD definition to a JSON file.
        
        Args:
            filename: Name of the file to save to
        """
        afd_data = {
            "states": list(self.states),
            "alphabet": list(self.alphabet),
            "initial_state": self.initial_state,
            "accepting_states": list(self.accepting_states),
            "transitions": {f"{from_state},{symbol}": to_state 
                          for (from_state, symbol), to_state in self.transitions.items()}
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(afd_data, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'AFD':
        """
        Load an AFD definition from a JSON file.
        
        Args:
            filename: Name of the file to load from
            
        Returns:
            AFD instance loaded from the file
        """
        with open(filename, 'r', encoding='utf-8') as f:
            afd_data = json.load(f)
        
        afd = cls()
        
        # Load states
        for state in afd_data["states"]:
            afd.add_state(state)
        
        # Load alphabet
        for symbol in afd_data["alphabet"]:
            afd.add_symbol(symbol)
        
        # Load initial state
        afd.set_initial_state(afd_data["initial_state"])
        
        # Load accepting states
        for state in afd_data["accepting_states"]:
            afd.add_accepting_state(state)
        
        # Load transitions
        for transition_key, to_state in afd_data["transitions"].items():
            from_state, symbol = transition_key.split(',')
            afd.add_transition(from_state, symbol, to_state)
        
        return afd
    
    def __str__(self) -> str:
        """Return a string representation of the AFD."""
        return f"""AFD Definition:
States (Q): {sorted(self.states)}
Alphabet (Σ): {sorted(self.alphabet)}
Initial State (q₀): {self.initial_state}
Accepting States (F): {sorted(self.accepting_states)}
Transitions (δ):
{chr(10).join(f"  δ({from_state}, {symbol}) = {to_state}" 
              for (from_state, symbol), to_state in sorted(self.transitions.items()))}
Valid: {self.is_valid()}"""
