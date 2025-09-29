"""
Main GUI window for AFD Simulator.

This module contains the main Tkinter window that orchestrates
all GUI components of the AFD Simulator.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional
import os

from ..core.afd import AFD
from ..examples import AFDFactory, ExampleLoader
from ..utils.validators import validate_afd_definition
from .afd_editor import AFDEditor
from .string_evaluator import StringEvaluator
from .afd_visualizer import AFDVisualizer
from .help_system import HelpSystem
from .styles import StyleManager
from .tutorial_system import TutorialSystem
from .demo_improvements import show_improvements_demo
from .i18n import *


class AFDSimulatorGUI:
    """
    Main GUI application for AFD Simulator using Tkinter.
    """
    
    def __init__(self):
        """Initialize the GUI application."""
        self.root = tk.Tk()
        self.current_afd: Optional[AFD] = None
        
        # Initialize style manager and help system
        self.style_manager = StyleManager(self.root)
        self.help_system = HelpSystem(self.root)
        self.tutorial_system = TutorialSystem(self.root, self)
        
        self.setup_window()
        self.create_menu()
        self.create_main_interface()
        self.create_status_bar()
        self.setup_help_tooltips()
    
    def setup_window(self):
        """Setup the main window properties."""
        self.root.title("Simulador AFD - Autómata Finito Determinista")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configure grid weights for responsive design
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def create_menu(self):
        """Create the main menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=MENU_FILE, menu=file_menu)
        file_menu.add_command(label=NEW_AFD, command=self.new_afd)
        file_menu.add_command(label=LOAD_AFD, command=self.load_afd)
        file_menu.add_command(label=SAVE_AFD, command=self.save_afd)
        file_menu.add_separator()
        file_menu.add_command(label=EXIT, command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=MENU_EDIT, menu=edit_menu)
        edit_menu.add_command(label=CLEAR_AFD, command=self.clear_afd)
        edit_menu.add_command(label=VALIDATE_AFD_MENU, command=self.validate_afd)
        
        # Examples menu
        examples_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=MENU_EXAMPLES, menu=examples_menu)
        
        # Add factory examples
        factory_examples = AFDFactory.get_available_examples()
        for name, description, _ in factory_examples:
            examples_menu.add_command(
                label=description,
                command=lambda n=name: self.load_factory_example(n)
            )
        
        examples_menu.add_separator()
        
        # Add file examples
        loader = ExampleLoader("examples")
        file_examples = loader.get_available_examples()
        for example_name in file_examples:
            examples_menu.add_command(
                label=f"Cargar {example_name}",
                command=lambda n=example_name: self.load_file_example(n)
            )
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=MENU_TOOLS, menu=tools_menu)
        tools_menu.add_command(label=STRING_EVALUATOR, command=self.open_string_evaluator)
        tools_menu.add_command(label=AFD_VISUALIZER, command=self.open_visualizer)
        tools_menu.add_command(label=GENERATE_ACCEPTED_STRINGS, command=self.generate_strings)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=MENU_HELP, menu=help_menu)
        help_menu.add_command(label=TUTORIAL, command=self.start_tutorial)
        help_menu.add_command(label=HELP, command=self.show_help)
        help_menu.add_command(label=WHATS_NEW, command=self.show_improvements)
        help_menu.add_command(label=ABOUT, command=self.show_about)
        help_menu.add_command(label=DOCUMENTATION, command=self.show_documentation)
        help_menu.add_separator()
        help_menu.add_command(label=KEYBOARD_SHORTCUTS, command=self.show_shortcuts)
    
    def create_main_interface(self):
        """Create the main interface components."""
        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # AFD Editor tab
        self.editor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.editor_frame, text="Editor AFD")
        self.afd_editor = AFDEditor(self.editor_frame, self)
        
        # String Evaluator tab
        self.evaluator_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.evaluator_frame, text="Evaluador de Cadenas")
        self.string_evaluator = StringEvaluator(self.evaluator_frame, self)
        
        # AFD Visualizer tab
        self.visualizer_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.visualizer_frame, text="Visualizador AFD")
        self.afd_visualizer = AFDVisualizer(self.visualizer_frame, self)
        
        # Configure notebook
        self.notebook.grid_rowconfigure(0, weight=1)
        self.notebook.grid_columnconfigure(0, weight=1)
    
    def create_status_bar(self):
        """Create the status bar."""
        self.status_bar = ttk.Label(
            self.root, 
            text="Listo - No hay AFD cargado", 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.grid(row=2, column=0, sticky="ew")
    
    def setup_help_tooltips(self):
        """Setup help tooltips for main interface."""
        # Agregar tooltips ligeros solo a contenedores principales (evitar spam)
        try:
            self.help_system.add_tooltip(self.notebook, "notebook_tabs")
            self.help_system.add_tooltip(self.status_bar, "status_bar")
        except Exception:
            pass
    
    def update_status(self, message: str):
        """Update the status bar message."""
        self.status_bar.config(text=message)
    
    def new_afd(self):
        """Create a new AFD."""
        self.current_afd = AFD()
        self.afd_editor.set_afd(self.current_afd)
        self.update_status("New AFD created")
        messagebox.showinfo("New AFD", "New AFD created. Start by adding states and alphabet.")
    
    def load_afd(self):
        """Load an AFD from file."""
        filename = filedialog.askopenfilename(
            title="Load AFD",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.current_afd = AFD.load_from_file(filename)
                self.afd_editor.set_afd(self.current_afd)
                self.update_status(f"AFD loaded from {os.path.basename(filename)}")
                messagebox.showinfo("Success", f"AFD loaded successfully from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load AFD: {e}")
    
    def save_afd(self):
        """Save the current AFD to file."""
        if not self.current_afd:
            messagebox.showwarning("Warning", "No AFD to save")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save AFD",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.current_afd.save_to_file(filename)
                self.update_status(f"AFD saved to {os.path.basename(filename)}")
                messagebox.showinfo("Success", f"AFD saved successfully to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save AFD: {e}")
    
    def clear_afd(self):
        """Clear the current AFD."""
        if self.current_afd:
            if messagebox.askyesno("Clear AFD", "Are you sure you want to clear the current AFD?"):
                self.current_afd = None
                self.afd_editor.set_afd(None)
                self.update_status("AFD cleared")
    
    def validate_afd(self):
        """Validate the current AFD."""
        if not self.current_afd:
            messagebox.showwarning("Warning", "No AFD to validate")
            return
        
        is_valid, errors = validate_afd_definition(self.current_afd)
        
        if is_valid:
            messagebox.showinfo("Validation", "AFD is valid and complete!")
        else:
            error_text = "AFD validation failed:\n\n" + "\n".join(f"• {error}" for error in errors)
            messagebox.showerror("Validation Error", error_text)
    
    def load_factory_example(self, example_name: str):
        """Load a factory example AFD."""
        try:
            self.current_afd = AFDFactory.create_example_by_name(example_name)
            self.afd_editor.set_afd(self.current_afd)
            self.update_status(f"Factory example '{example_name}' loaded")
            messagebox.showinfo("Success", f"Factory example '{example_name}' loaded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load factory example: {e}")
    
    def load_file_example(self, example_name: str):
        """Load a file example AFD."""
        try:
            loader = ExampleLoader("examples")
            self.current_afd = loader.load_example(example_name)
            self.afd_editor.set_afd(self.current_afd)
            self.update_status(f"File example '{example_name}' loaded")
            messagebox.showinfo("Success", f"File example '{example_name}' loaded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file example: {e}")
    
    def open_string_evaluator(self):
        """Open the string evaluator tab."""
        self.notebook.select(1)  # Switch to evaluator tab
    
    def open_visualizer(self):
        """Open the AFD visualizer tab."""
        self.notebook.select(2)  # Switch to visualizer tab
    
    def generate_strings(self):
        """Generate accepted strings for the current AFD."""
        if not self.current_afd:
            messagebox.showwarning("Warning", "No AFD loaded")
            return
        
        if not self.current_afd.is_valid():
            messagebox.showwarning("Warning", "Current AFD is not valid")
            return
        
        try:
            accepted_strings = self.current_afd.generate_accepted_strings(20)
            
            if accepted_strings:
                string_list = "\n".join(f"{i+1:2d}. '{s}'" for i, s in enumerate(accepted_strings))
                messagebox.showinfo(
                    "Accepted Strings", 
                    f"First 20 accepted strings:\n\n{string_list}"
                )
            else:
                messagebox.showinfo("Accepted Strings", "No accepted strings found.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate strings: {e}")
    
    def start_tutorial(self):
        """Start the interactive tutorial."""
        self.tutorial_system.start_tutorial()
    
    def show_help(self):
        """Show main help window."""
        self.help_system.show_help_window()
    
    def show_improvements(self):
        """Show improvements demo."""
        show_improvements_demo(self.root)
    
    def show_shortcuts(self):
        """Show keyboard shortcuts dialog."""
        shortcuts_text = """
ATAJOS DE TECLADO - Simulador AFD

GENERALES:
• Ctrl+N: Nuevo AFD
• Ctrl+O: Abrir AFD
• Ctrl+S: Guardar AFD
• Ctrl+W: Cerrar AFD
• F1: Ayuda
• F5: Actualizar visualización
• Ctrl+Q: Salir

EDITOR AFD:
• Tab: Siguiente campo
• Shift+Tab: Campo anterior
• Enter: Agregar elemento (en campos de entrada)
• Delete: Eliminar elemento seleccionado
• Ctrl+A: Seleccionar todo (en listas)

EVALUADOR DE CADENAS:
• Enter: Evaluar cadena
• Espacio: Siguiente paso
• R: Reiniciar evaluación
• Ctrl+Enter: Evaluar paso a paso

VISUALIZADOR AFD:
• Ctrl++: Zoom in
• Ctrl+-: Zoom out
• Ctrl+0: Reset zoom
• F5: Actualizar visualización

NAVEGACIÓN:
• Ctrl+Tab: Siguiente pestaña
• Ctrl+Shift+Tab: Pestaña anterior
• Ctrl+1: Editor AFD
• Ctrl+2: Evaluador de Cadenas
• Ctrl+3: Visualizador AFD
        """
        messagebox.showinfo("Atajos de Teclado", shortcuts_text.strip())
    
    def show_about(self):
        """Show about dialog."""
        about_text = """
AFD Simulator v2.0

Una herramienta completa para simular Autómatas Finitos Deterministas (AFD).

Características:
• Creación y edición visual de AFDs
• Evaluación de cadenas con visualización paso a paso
• Generación automática de cadenas
• Visualización y validación de AFDs
• Guardar y cargar definiciones de AFD
• Ejemplos integrados y patrones
• Sistema de ayuda contextual
• Validación en tiempo real
• Interfaz moderna y atractiva

Desarrollado con Python y Tkinter.
Versión 2.0 - Mejoras en la interfaz y experiencia de usuario
        """
        messagebox.showinfo("Acerca de AFD Simulator", about_text.strip())
    
    def show_documentation(self):
        """Show documentation."""
        doc_text = """
AFD Simulator Documentation

1. Creating an AFD:
   - Use the AFD Editor tab to define states, alphabet, and transitions
   - Set initial state and accepting states
   - Validate your AFD using Edit > Validate AFD

2. Evaluating Strings:
   - Switch to the String Evaluator tab
   - Enter a string to evaluate
   - View step-by-step transitions

3. Visualizing AFD:
   - Use the AFD Visualizer tab for graphical representation
   - See states, transitions, and accepting states

4. Examples:
   - Load pre-built examples from Examples menu
   - Factory examples: Common patterns
   - File examples: Saved AFD definitions

5. File Operations:
   - Save your AFD: File > Save AFD
   - Load existing AFD: File > Load AFD
   - Create new AFD: File > New AFD
        """
        messagebox.showinfo("Documentation", doc_text.strip())
    
    def get_current_afd(self) -> Optional[AFD]:
        """Get the current AFD instance."""
        return self.current_afd
    
    def set_current_afd(self, afd: AFD):
        """Set the current AFD instance."""
        self.current_afd = afd
        self.afd_editor.set_afd(afd)
        self.update_status("AFD updated")
    
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()
