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
            '1': ('Crear nuevo AFD', self._placeholder_handler),
            '2': ('Cargar AFD desde archivo', self._placeholder_handler),
            '3': ('Mostrar AFD actual', self._placeholder_handler),
            '4': ('Evaluar cadena', self._placeholder_handler),
            '5': ('Generar cadenas aceptadas', self._placeholder_handler),
            '6': ('Guardar AFD en archivo', self._placeholder_handler),
            '7': ('Validar AFD', self._placeholder_handler),
            '8': ('Ayuda', self._placeholder_handler),
            '9': ('Salir', self._placeholder_handler)
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
        print(format_menu_header("SIMULADOR AFD", 60))
        print("    Simulador de Autómatas Finitos Deterministas")
        print("=" * 60)
        print()
    
    def display_menu(self) -> None:
        """Display the main menu options."""
        print("MENÚ PRINCIPAL:")
        for menu_id, (description, _) in self.menu_items.items():
            print(f"{menu_id}. {description}")
        print()
    
    def get_user_choice(self) -> str:
        """
        Get user's menu choice.
        
        Returns:
            The user's menu selection
        """
        return self.input_handler.get_user_input("Selecciona una opción (1-9): ")
    
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
        self.display_section_header("AYUDA")
        print(format_help_text())
    
    def confirm_exit(self) -> bool:
        """
        Confirm if user wants to exit.
        
        Returns:
            True if user confirms exit, False otherwise
        """
        return self.input_handler.get_yes_no_input("¿Estás seguro de que quieres salir?")
    
    def wait_for_continue(self) -> None:
        """Wait for user to press Enter to continue."""
        input("\nPresiona Enter para continuar...")
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
        print(f"⚠ Advertencia: {warning_message}")
    
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
                print("¡Gracias por usar el Simulador AFD!")
                return False
            return True
        else:
            self.display_error("Opción inválida. Por favor selecciona 1-9.")
            return True
    
    def _placeholder_handler(self) -> None:
        """Placeholder handler for unregistered menu items."""
        self.display_error("Esta funcionalidad aún no está implementada.")
