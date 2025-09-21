"""
AFD Simulator - Interactive Deterministic Finite Automaton Simulator

This is the main application file that provides an interactive console interface
for defining, evaluating, and managing Deterministic Finite Automata (DFA).
"""

import os
import sys
from typing import List, Optional
from afd import AFD


class AFDSimulator:
    """
    Interactive AFD Simulator with console interface.
    
    Provides methods for creating, managing, and interacting with AFD instances
    through a user-friendly command-line interface.
    """
    
    def __init__(self):
        """Initialize the AFD Simulator."""
        self.current_afd: Optional[AFD] = None
        self.running = True
    
    def display_header(self) -> None:
        """Display the application header."""
        print("=" * 60)
        print("           AFD SIMULATOR")
        print("    Deterministic Finite Automaton Simulator")
        print("=" * 60)
        print()
    
    def display_menu(self) -> None:
        """Display the main menu options."""
        print("MAIN MENU:")
        print("1. Create new AFD")
        print("2. Load AFD from file")
        print("3. Display current AFD")
        print("4. Evaluate string")
        print("5. Generate accepted strings")
        print("6. Save AFD to file")
        print("7. Validate AFD")
        print("8. Help")
        print("9. Exit")
        print()
    
    def get_user_input(self, prompt: str) -> str:
        """
        Get input from user with error handling.
        
        Args:
            prompt: The prompt to display to the user
            
        Returns:
            User input string
        """
        try:
            return input(prompt).strip()
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
    
    def create_new_afd(self) -> None:
        """Create a new AFD by gathering input from the user."""
        print("\n" + "=" * 40)
        print("CREATING NEW AFD")
        print("=" * 40)
        
        self.current_afd = AFD()
        
        # Get states
        print("\n1. Define States (Q)")
        print("Enter state names separated by spaces (e.g., q0 q1 q2):")
        states_input = self.get_user_input("States: ")
        if not states_input:
            print("No states entered. Returning to main menu.")
            return
        
        states = states_input.split()
        for state in states:
            self.current_afd.add_state(state)
        
        print(f"Added states: {sorted(self.current_afd.states)}")
        
        # Get alphabet
        print("\n2. Define Alphabet (Σ)")
        print("Enter symbols separated by spaces (e.g., 0 1 a b):")
        alphabet_input = self.get_user_input("Alphabet: ")
        if not alphabet_input:
            print("No alphabet symbols entered. Returning to main menu.")
            return
        
        symbols = alphabet_input.split()
        for symbol in symbols:
            self.current_afd.add_symbol(symbol)
        
        print(f"Added alphabet: {sorted(self.current_afd.alphabet)}")
        
        # Get initial state
        print("\n3. Define Initial State (q₀)")
        print(f"Available states: {sorted(self.current_afd.states)}")
        initial_state = self.get_user_input("Initial state: ")
        
        try:
            self.current_afd.set_initial_state(initial_state)
            print(f"Initial state set to: {initial_state}")
        except ValueError as e:
            print(f"Error: {e}")
            return
        
        # Get accepting states
        print("\n4. Define Accepting States (F)")
        print(f"Available states: {sorted(self.current_afd.states)}")
        print("Enter accepting states separated by spaces:")
        accepting_input = self.get_user_input("Accepting states: ")
        
        if accepting_input:
            accepting_states = accepting_input.split()
            for state in accepting_states:
                try:
                    self.current_afd.add_accepting_state(state)
                except ValueError as e:
                    print(f"Error: {e}")
                    continue
            print(f"Accepting states: {sorted(self.current_afd.accepting_states)}")
        
        # Get transitions
        print("\n5. Define Transitions (δ)")
        print("Enter transitions in format: from_state symbol to_state")
        print("Type 'done' when finished")
        print(f"Available states: {sorted(self.current_afd.states)}")
        print(f"Available symbols: {sorted(self.current_afd.alphabet)}")
        
        while True:
            transition_input = self.get_user_input("Transition: ")
            if transition_input.lower() == 'done':
                break
            
            parts = transition_input.split()
            if len(parts) != 3:
                print("Invalid format. Use: from_state symbol to_state")
                continue
            
            from_state, symbol, to_state = parts
            try:
                self.current_afd.add_transition(from_state, symbol, to_state)
                print(f"Added transition: δ({from_state}, {symbol}) = {to_state}")
            except ValueError as e:
                print(f"Error: {e}")
        
        print("\nAFD creation completed!")
        
        # Validate the AFD
        if self.current_afd.is_valid():
            print("✓ AFD is valid and ready to use.")
        else:
            print("⚠ Warning: AFD is not complete. Some transitions may be missing.")
    
    def load_afd_from_file(self) -> None:
        """Load an AFD from a JSON file."""
        print("\n" + "=" * 40)
        print("LOADING AFD FROM FILE")
        print("=" * 40)
        
        filename = self.get_user_input("Enter filename: ")
        
        try:
            self.current_afd = AFD.load_from_file(filename)
            print(f"✓ AFD loaded successfully from '{filename}'")
            print(f"States: {sorted(self.current_afd.states)}")
            print(f"Alphabet: {sorted(self.current_afd.alphabet)}")
            print(f"Initial state: {self.current_afd.initial_state}")
            print(f"Accepting states: {sorted(self.current_afd.accepting_states)}")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"Error loading file: {e}")
    
    def display_current_afd(self) -> None:
        """Display the current AFD definition."""
        print("\n" + "=" * 40)
        print("CURRENT AFD DEFINITION")
        print("=" * 40)
        
        if self.current_afd is None:
            print("No AFD is currently loaded.")
            print("Please create a new AFD or load one from a file.")
            return
        
        print(self.current_afd)
    
    def evaluate_string(self) -> None:
        """Evaluate a string using the current AFD."""
        print("\n" + "=" * 40)
        print("EVALUATING STRING")
        print("=" * 40)
        
        if self.current_afd is None:
            print("No AFD is currently loaded.")
            print("Please create a new AFD or load one from a file.")
            return
        
        if not self.current_afd.is_valid():
            print("Current AFD is not valid. Please complete the definition.")
            return
        
        input_string = self.get_user_input("Enter string to evaluate: ")
        
        if not input_string:
            print("No string entered.")
            return
        
        try:
            is_accepted, transitions_path = self.current_afd.evaluate_string(input_string)
            
            print(f"\nEvaluating string: '{input_string}'")
            print("-" * 30)
            
            for i, (from_state, symbol, to_state) in enumerate(transitions_path, 1):
                print(f"{i}. From state ({from_state}) with symbol '{symbol}' "
                      f"transitions to state ({to_state}).")
            
            print("-" * 30)
            if is_accepted:
                print(f"✓ Result: The string '{input_string}' is ACCEPTED.")
            else:
                print(f"✗ Result: The string '{input_string}' is REJECTED.")
                
        except ValueError as e:
            print(f"Error: {e}")
    
    def generate_accepted_strings(self) -> None:
        """Generate the first 10 shortest accepted strings."""
        print("\n" + "=" * 40)
        print("GENERATING ACCEPTED STRINGS")
        print("=" * 40)
        
        if self.current_afd is None:
            print("No AFD is currently loaded.")
            print("Please create a new AFD or load one from a file.")
            return
        
        if not self.current_afd.is_valid():
            print("Current AFD is not valid. Please complete the definition.")
            return
        
        try:
            accepted_strings = self.current_afd.generate_accepted_strings()
            
            if accepted_strings:
                print("First 10 shortest accepted strings:")
                print("-" * 30)
                for i, string in enumerate(accepted_strings, 1):
                    print(f"{i:2d}. '{string}'")
            else:
                print("No accepted strings found.")
                print("This AFD may not accept any strings, or the language may be infinite.")
                
        except Exception as e:
            print(f"Error generating strings: {e}")
    
    def save_afd_to_file(self) -> None:
        """Save the current AFD to a JSON file."""
        print("\n" + "=" * 40)
        print("SAVING AFD TO FILE")
        print("=" * 40)
        
        if self.current_afd is None:
            print("No AFD is currently loaded.")
            print("Please create a new AFD or load one from a file.")
            return
        
        filename = self.get_user_input("Enter filename (with .json extension): ")
        
        if not filename:
            print("No filename entered.")
            return
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        try:
            self.current_afd.save_to_file(filename)
            print(f"✓ AFD saved successfully to '{filename}'")
        except Exception as e:
            print(f"Error saving file: {e}")
    
    def validate_afd(self) -> None:
        """Validate the current AFD."""
        print("\n" + "=" * 40)
        print("VALIDATING AFD")
        print("=" * 40)
        
        if self.current_afd is None:
            print("No AFD is currently loaded.")
            return
        
        is_valid = self.current_afd.is_valid()
        
        if is_valid:
            print("✓ AFD is valid and complete!")
        else:
            print("✗ AFD is not valid. Issues found:")
            
            # Check specific issues
            if not self.current_afd.states:
                print("  - No states defined")
            if not self.current_afd.alphabet:
                print("  - No alphabet defined")
            if self.current_afd.initial_state is None:
                print("  - No initial state defined")
            elif self.current_afd.initial_state not in self.current_afd.states:
                print("  - Initial state is not in the set of states")
            if not self.current_afd.accepting_states.issubset(self.current_afd.states):
                print("  - Some accepting states are not in the set of states")
            
            # Check for missing transitions
            missing_transitions = []
            for state in self.current_afd.states:
                for symbol in self.current_afd.alphabet:
                    if (state, symbol) not in self.current_afd.transitions:
                        missing_transitions.append(f"δ({state}, {symbol})")
            
            if missing_transitions:
                print(f"  - Missing transitions: {', '.join(missing_transitions[:5])}")
                if len(missing_transitions) > 5:
                    print(f"    ... and {len(missing_transitions) - 5} more")
    
    def display_help(self) -> None:
        """Display help information."""
        print("\n" + "=" * 40)
        print("HELP - AFD SIMULATOR")
        print("=" * 40)
        
        print("""
This simulator allows you to work with Deterministic Finite Automata (DFA).

DFA Components:
- States (Q): Finite set of state identifiers
- Alphabet (Σ): Set of input symbols
- Initial State (q₀): Starting state
- Accepting States (F): States that accept the input
- Transition Function (δ): Rules for state changes

Key Features:
1. Create and define complete DFA
2. Evaluate strings with step-by-step visualization
3. Generate accepted strings automatically
4. Save and load DFA definitions
5. Comprehensive validation

Tips:
- Use descriptive state names (e.g., q0, q1, q2)
- Define all transitions for complete functionality
- Test with various strings to verify behavior
- Save your work frequently
        """)
    
    def run(self) -> None:
        """Run the main application loop."""
        self.display_header()
        
        while self.running:
            try:
                self.display_menu()
                choice = self.get_user_input("Select an option (1-9): ")
                
                if choice == '1':
                    self.create_new_afd()
                elif choice == '2':
                    self.load_afd_from_file()
                elif choice == '3':
                    self.display_current_afd()
                elif choice == '4':
                    self.evaluate_string()
                elif choice == '5':
                    self.generate_accepted_strings()
                elif choice == '6':
                    self.save_afd_to_file()
                elif choice == '7':
                    self.validate_afd()
                elif choice == '8':
                    self.display_help()
                elif choice == '9':
                    if self.get_yes_no_input("Are you sure you want to exit?"):
                        print("Thank you for using AFD Simulator!")
                        self.running = False
                else:
                    print("Invalid option. Please select 1-9.")
                
                if self.running:
                    input("\nPress Enter to continue...")
                    print("\n" + "=" * 60)
                
            except KeyboardInterrupt:
                print("\n\nOperation interrupted by user.")
                if self.get_yes_no_input("Do you want to exit?"):
                    self.running = False
            except Exception as e:
                print(f"\nUnexpected error: {e}")
                input("Press Enter to continue...")


def main():
    """Main entry point of the application."""
    try:
        simulator = AFDSimulator()
        simulator.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
