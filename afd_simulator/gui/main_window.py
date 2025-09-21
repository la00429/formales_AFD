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


class AFDSimulatorGUI:
    """
    Main GUI application for AFD Simulator using Tkinter.
    """
    
    def __init__(self):
        """Initialize the GUI application."""
        self.root = tk.Tk()
        self.current_afd: Optional[AFD] = None
        self.setup_window()
        self.create_menu()
        self.create_main_interface()
        self.create_status_bar()
    
    def setup_window(self):
        """Setup the main window properties."""
        self.root.title("AFD Simulator - Deterministic Finite Automaton Simulator")
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
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New AFD", command=self.new_afd)
        file_menu.add_command(label="Load AFD...", command=self.load_afd)
        file_menu.add_command(label="Save AFD...", command=self.save_afd)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear AFD", command=self.clear_afd)
        edit_menu.add_command(label="Validate AFD", command=self.validate_afd)
        
        # Examples menu
        examples_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Examples", menu=examples_menu)
        
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
                label=f"Load {example_name}",
                command=lambda n=example_name: self.load_file_example(n)
            )
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="String Evaluator", command=self.open_string_evaluator)
        tools_menu.add_command(label="AFD Visualizer", command=self.open_visualizer)
        tools_menu.add_command(label="Generate Accepted Strings", command=self.generate_strings)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
    
    def create_main_interface(self):
        """Create the main interface components."""
        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # AFD Editor tab
        self.editor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.editor_frame, text="AFD Editor")
        self.afd_editor = AFDEditor(self.editor_frame, self)
        
        # String Evaluator tab
        self.evaluator_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.evaluator_frame, text="String Evaluator")
        self.string_evaluator = StringEvaluator(self.evaluator_frame, self)
        
        # AFD Visualizer tab
        self.visualizer_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.visualizer_frame, text="AFD Visualizer")
        self.afd_visualizer = AFDVisualizer(self.visualizer_frame, self)
        
        # Configure notebook
        self.notebook.grid_rowconfigure(0, weight=1)
        self.notebook.grid_columnconfigure(0, weight=1)
    
    def create_status_bar(self):
        """Create the status bar."""
        self.status_bar = ttk.Label(
            self.root, 
            text="Ready - No AFD loaded", 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.grid(row=2, column=0, sticky="ew")
    
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
    
    def show_about(self):
        """Show about dialog."""
        about_text = """
AFD Simulator v1.0

A comprehensive tool for simulating Deterministic Finite Automata (DFA).

Features:
• Visual AFD creation and editing
• String evaluation with step-by-step visualization
• Automatic string generation
• AFD visualization and validation
• Save and load AFD definitions
• Built-in examples and patterns

Developed with Python and Tkinter.
        """
        messagebox.showinfo("About AFD Simulator", about_text.strip())
    
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
