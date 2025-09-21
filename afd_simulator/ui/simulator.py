"""
Main AFD Simulator class with modular architecture.

This module contains the main simulator class that orchestrates
all the components of the AFD Simulator application.
"""

import os
import sys
from typing import Optional
from ..core.afd import AFD
from ..utils.validators import validate_afd_definition
from ..utils.formatters import (
    format_transition_path, 
    format_afd_summary, 
    format_accepted_strings,
    format_error_message,
    format_success_message
)
from .input_handler import InputHandler
from .menu_system import MenuSystem


class AFDSimulator:
    """
    Main AFD Simulator application with modular architecture.
    
    This class orchestrates all components of the simulator including
    the menu system, input handling, and AFD operations.
    """
    
    # Constants for error messages
    NO_AFD_LOADED_MSG = "No AFD is currently loaded."
    CREATE_OR_LOAD_MSG = "Please create a new AFD or load one from a file."
    
    def __init__(self):
        """Initialize the AFD Simulator."""
        self.current_afd: Optional[AFD] = None
        self.running = True
        self.input_handler = InputHandler()
        self.menu_system = MenuSystem()
        
        # Register menu handlers
        self._register_menu_handlers()
    
    def _register_menu_handlers(self) -> None:
        """Register all menu handlers."""
        self.menu_system.register_handler('1', self.create_new_afd)
        self.menu_system.register_handler('2', self.load_afd_from_file)
        self.menu_system.register_handler('3', self.display_current_afd)
        self.menu_system.register_handler('4', self.evaluate_string)
        self.menu_system.register_handler('5', self.generate_accepted_strings)
        self.menu_system.register_handler('6', self.save_afd_to_file)
        self.menu_system.register_handler('7', self.validate_afd)
        self.menu_system.register_handler('8', self.display_help)
    
    def run(self) -> None:
        """Run the main application loop."""
        self.menu_system.display_header()
        
        while self.running:
            try:
                self.menu_system.display_menu()
                choice = self.menu_system.get_user_choice()
                
                self.running = self.menu_system.handle_menu_choice(choice)
                
                if self.running:
                    self.menu_system.wait_for_continue()
                
            except KeyboardInterrupt:
                print("\n\nOperation interrupted by user.")
                if self.menu_system.confirm_exit():
                    self.running = False
            except Exception as e:
                self.menu_system.display_error(f"Unexpected error: {e}")
                self.menu_system.wait_for_continue()
    
    def create_new_afd(self) -> None:
        """Create a new AFD by gathering input from the user."""
        self.menu_system.display_section_header("CREATING NEW AFD")
        
        self.current_afd = AFD()
        
        # Get states
        print("\n1. Define States (Q)")
        print("Enter state names separated by spaces (e.g., q0 q1 q2):")
        states = self.input_handler.get_state_names("States: ")
        if not states:
            self.menu_system.display_warning("No states entered. Returning to main menu.")
            return
        
        for state in states:
            self.current_afd.add_state(state)
        
        print(f"Added states: {sorted(self.current_afd.states)}")
        
        # Get alphabet
        print("\n2. Define Alphabet (Σ)")
        print("Enter symbols separated by spaces (e.g., 0 1 a b):")
        symbols = self.input_handler.get_alphabet_symbols("Alphabet: ")
        if not symbols:
            self.menu_system.display_warning("No alphabet symbols entered. Returning to main menu.")
            return
        
        for symbol in symbols:
            self.current_afd.add_symbol(symbol)
        
        print(f"Added alphabet: {sorted(self.current_afd.alphabet)}")
        
        # Get initial state
        print("\n3. Define Initial State (q₀)")
        print(f"Available states: {sorted(self.current_afd.states)}")
        initial_state = self.input_handler.get_initial_state(
            "Initial state: ", self.current_afd.states
        )
        
        if initial_state:
            try:
                self.current_afd.set_initial_state(initial_state)
                print(f"Initial state set to: {initial_state}")
            except ValueError as e:
                self.menu_system.display_error(str(e))
                return
        
        # Get accepting states
        print("\n4. Define Accepting States (F)")
        print(f"Available states: {sorted(self.current_afd.states)}")
        print("Enter accepting states separated by spaces:")
        accepting_states = self.input_handler.get_accepting_states(
            "Accepting states: ", self.current_afd.states
        )
        
        for state in accepting_states:
            try:
                self.current_afd.add_accepting_state(state)
            except ValueError as e:
                self.menu_system.display_error(str(e))
                continue
        
        if accepting_states:
            print(f"Accepting states: {sorted(self.current_afd.accepting_states)}")
        
        # Get transitions
        print("\n5. Define Transitions (δ)")
        print("Enter transitions in format: from_state symbol to_state")
        print("Type 'done' when finished")
        print(f"Available states: {sorted(self.current_afd.states)}")
        print(f"Available symbols: {sorted(self.current_afd.alphabet)}")
        
        while True:
            transition = self.input_handler.get_transition(
                "Transition: ", self.current_afd.states, self.current_afd.alphabet
            )
            if transition is None:
                break
            
            from_state, symbol, to_state = transition
            try:
                self.current_afd.add_transition(from_state, symbol, to_state)
                print(f"Added transition: δ({from_state}, {symbol}) = {to_state}")
            except ValueError as e:
                self.menu_system.display_error(str(e))
        
        print("\nAFD creation completed!")
        
        # Validate the AFD
        if self.current_afd.is_valid():
            self.menu_system.display_success("AFD is valid and ready to use.")
        else:
            self.menu_system.display_warning("AFD is not complete. Some transitions may be missing.")
    
    def load_afd_from_file(self) -> None:
        """Load an AFD from a JSON file."""
        self.menu_system.display_section_header("LOADING AFD FROM FILE")
        
        filename = self.input_handler.get_filename("Enter filename: ")
        
        if not filename:
            self.menu_system.display_error("No filename entered.")
            return
        
        try:
            self.current_afd = AFD.load_from_file(filename)
            self.menu_system.display_success(f"AFD loaded successfully from '{filename}'")
            print(format_afd_summary(self.current_afd))
        except FileNotFoundError:
            self.menu_system.display_error(f"File '{filename}' not found.")
        except Exception as e:
            self.menu_system.display_error(f"Error loading file: {e}")
    
    def display_current_afd(self) -> None:
        """Display the current AFD definition."""
        self.menu_system.display_section_header("CURRENT AFD DEFINITION")
        
        if self.current_afd is None:
            self.menu_system.display_info(self.NO_AFD_LOADED_MSG)
            print(self.CREATE_OR_LOAD_MSG)
            return
        
        print(self.current_afd)
    
    def evaluate_string(self) -> None:
        """Evaluate a string using the current AFD."""
        self.menu_system.display_section_header("EVALUATING STRING")
        
        if self.current_afd is None:
            self.menu_system.display_info(self.NO_AFD_LOADED_MSG)
            print(self.CREATE_OR_LOAD_MSG)
            return
        
        if not self.current_afd.is_valid():
            self.menu_system.display_warning("Current AFD is not valid. Please complete the definition.")
            return
        
        input_string = self.input_handler.get_string_for_evaluation(
            "Enter string to evaluate: ", self.current_afd.alphabet
        )
        
        if not input_string:
            self.menu_system.display_info("No string entered.")
            return
        
        try:
            is_accepted, transitions_path = self.current_afd.evaluate_string(input_string)
            
            print(format_transition_path(transitions_path, input_string, is_accepted))
                
        except ValueError as e:
            self.menu_system.display_error(str(e))
    
    def generate_accepted_strings(self) -> None:
        """Generate the first 10 shortest accepted strings."""
        self.menu_system.display_section_header("GENERATING ACCEPTED STRINGS")
        
        if self.current_afd is None:
            self.menu_system.display_info(self.NO_AFD_LOADED_MSG)
            print(self.CREATE_OR_LOAD_MSG)
            return
        
        if not self.current_afd.is_valid():
            self.menu_system.display_warning("Current AFD is not valid. Please complete the definition.")
            return
        
        try:
            accepted_strings = self.current_afd.generate_accepted_strings()
            print(format_accepted_strings(accepted_strings))
                
        except Exception as e:
            self.menu_system.display_error(f"Error generating strings: {e}")
    
    def save_afd_to_file(self) -> None:
        """Save the current AFD to a JSON file."""
        self.menu_system.display_section_header("SAVING AFD TO FILE")
        
        if self.current_afd is None:
            self.menu_system.display_info(self.NO_AFD_LOADED_MSG)
            print(self.CREATE_OR_LOAD_MSG)
            return
        
        filename = self.input_handler.get_filename("Enter filename: ")
        
        if not filename:
            self.menu_system.display_error("No filename entered.")
            return
        
        try:
            self.current_afd.save_to_file(filename)
            self.menu_system.display_success(f"AFD saved successfully to '{filename}'")
        except Exception as e:
            self.menu_system.display_error(f"Error saving file: {e}")
    
    def validate_afd(self) -> None:
        """Validate the current AFD."""
        self.menu_system.display_section_header("VALIDATING AFD")
        
        if self.current_afd is None:
            self.menu_system.display_info("No AFD is currently loaded.")
            return
        
        is_valid, errors = validate_afd_definition(self.current_afd)
        
        if is_valid:
            self.menu_system.display_success("AFD is valid and complete!")
        else:
            self.menu_system.display_error("AFD is not valid. Issues found:")
            for error in errors:
                print(f"  - {error}")
    
    def display_help(self) -> None:
        """Display help information."""
        self.menu_system.display_help()


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
