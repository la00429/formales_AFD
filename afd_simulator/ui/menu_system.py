"""
Menu system for AFD Simulator.

This module contains the menu display and navigation components
for the interactive console interface.
"""

from typing import Dict, Callable, Optional
from .input_handler import InputHandler
from ..utils.formatters import format_menu_header, format_section_header


class MenuSystem:
    """
    Handles menu display and navigation for the AFD Simulator.
    """
    
    def __init__(self):
        """Initialize the menu system."""
        self.input_handler = InputHandler()
        self.menu_items = {
            '1': ('Create new AFD', self._placeholder_handler),
            '2': ('Load AFD from file', self._placeholder_handler),
            '3': ('Display current AFD', self._placeholder_handler),
            '4': ('Evaluate string', self._placeholder_handler),
            '5': ('Generate accepted strings', self._placeholder_handler),
            '6': ('Save AFD to file', self._placeholder_handler),
            '7': ('Validate AFD', self._placeholder_handler),
            '8': ('Help', self._placeholder_handler),
            '9': ('Exit', self._placeholder_handler)
        }
        self.handlers: Dict[str, Callable] = {}
    
    def register_handler(self, menu_id: str, handler: Callable) -> None:
        """
        Register a handler function for a menu item.
        
        Args:
            menu_id: The menu item ID (e.g., '1', '2', etc.)
            handler: Function to call when menu item is selected
        """
        self.handlers[menu_id] = handler
    
    def display_header(self) -> None:
        """Display the application header."""
        print(format_menu_header("AFD SIMULATOR", 60))
        print("    Deterministic Finite Automaton Simulator")
        print("=" * 60)
        print()
    
    def display_menu(self) -> None:
        """Display the main menu options."""
        print("MAIN MENU:")
        for menu_id, (description, _) in self.menu_items.items():
            print(f"{menu_id}. {description}")
        print()
    
    def get_user_choice(self) -> str:
        """
        Get user's menu choice.
        
        Returns:
            The user's menu selection
        """
        return self.input_handler.get_user_input("Select an option (1-9): ")
    
    def display_section_header(self, title: str) -> None:
        """
        Display a section header.
        
        Args:
            title: The section title
        """
        print(format_section_header(title))
    
    def display_help(self) -> None:
        """Display help information."""
        from ..utils.formatters import format_help_text
        self.display_section_header("HELP")
        print(format_help_text())
    
    def confirm_exit(self) -> bool:
        """
        Confirm if user wants to exit.
        
        Returns:
            True if user confirms exit, False otherwise
        """
        return self.input_handler.get_yes_no_input("Are you sure you want to exit?")
    
    def wait_for_continue(self) -> None:
        """Wait for user to press Enter to continue."""
        input("\nPress Enter to continue...")
        print("\n" + "=" * 60)
    
    def display_error(self, error_message: str) -> None:
        """
        Display an error message.
        
        Args:
            error_message: The error message to display
        """
        print(f"✗ Error: {error_message}")
    
    def display_success(self, success_message: str) -> None:
        """
        Display a success message.
        
        Args:
            success_message: The success message to display
        """
        print(f"✓ {success_message}")
    
    def display_warning(self, warning_message: str) -> None:
        """
        Display a warning message.
        
        Args:
            warning_message: The warning message to display
        """
        print(f"⚠ Warning: {warning_message}")
    
    def display_info(self, info_message: str) -> None:
        """
        Display an info message.
        
        Args:
            info_message: The info message to display
        """
        print(f"ℹ {info_message}")
    
    def handle_menu_choice(self, choice: str) -> bool:
        """
        Handle a menu choice selection.
        
        Args:
            choice: The menu choice selected by user
            
        Returns:
            True if the application should continue, False if it should exit
        """
        if choice in self.handlers:
            try:
                result = self.handlers[choice]()
                return result if isinstance(result, bool) else True
            except Exception as e:
                self.display_error(f"Unexpected error: {e}")
                return True
        elif choice == '9':
            if self.confirm_exit():
                print("Thank you for using AFD Simulator!")
                return False
            return True
        else:
            self.display_error("Invalid option. Please select 1-9.")
            return True
    
    def _placeholder_handler(self) -> None:
        """Placeholder handler for unregistered menu items."""
        self.display_error("This functionality is not yet implemented.")
