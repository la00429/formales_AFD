"""
AFD Editor GUI component.

This module provides a graphical interface for creating and editing
AFD definitions with visual feedback and validation.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List, Set

from ..core.afd import AFD
from ..utils.validators import validate_state_name, validate_symbol, validate_transition_input
from .help_system import HelpSystem
from .styles import StyleManager
from .validation_feedback import ValidationFeedback, AFDValidator
from .i18n import *


class AFDEditor:
    """
    GUI component for editing AFD definitions.
    """
    
    # Constants for button text
    REMOVE_SELECTED_TEXT = REMOVE_SELECTED
    
    def __init__(self, parent, main_app):
        """
        Initialize the AFD Editor.
        
        Args:
            parent: Parent widget
            main_app: Reference to main application
        """
        self.parent = parent
        self.main_app = main_app
        self.current_afd: Optional[AFD] = None
        
        # Initialize style manager and help system
        self.style_manager = StyleManager(parent)
        self.help_system = HelpSystem(parent)
        self.validation_feedback = ValidationFeedback(parent, self.style_manager)
        self.afd_validator = AFDValidator(self.validation_feedback)
        
        self.create_widgets()
        self.setup_layout()
        self.setup_help_tooltips()
        self.setup_validation()
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Create main frame with scrollbar
        self.main_frame = ttk.Frame(self.parent)
        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # States section
        self.states_frame = ttk.LabelFrame(self.scrollable_frame, text=STATES_Q, padding=10)
        self.states_entry = ttk.Entry(self.states_frame, width=40)
        self.add_states_btn = ttk.Button(self.states_frame, text=ADD_STATES, command=self.add_states)
        self.states_listbox = tk.Listbox(self.states_frame, height=6)
        self.remove_state_btn = ttk.Button(self.states_frame, text=REMOVE_SELECTED, command=self.remove_state)
        
        # Alphabet section
        self.alphabet_frame = ttk.LabelFrame(self.scrollable_frame, text=ALPHABET_SIGMA, padding=10)
        self.alphabet_entry = ttk.Entry(self.alphabet_frame, width=40)
        self.add_alphabet_btn = ttk.Button(self.alphabet_frame, text=ADD_SYMBOLS, command=self.add_alphabet)
        self.alphabet_listbox = tk.Listbox(self.alphabet_frame, height=4)
        self.remove_alphabet_btn = ttk.Button(self.alphabet_frame, text=REMOVE_SELECTED, command=self.remove_alphabet)
        
        # Initial state section
        self.initial_frame = ttk.LabelFrame(self.scrollable_frame, text=INITIAL_STATE_Q0, padding=10)
        self.initial_var = tk.StringVar()
        self.initial_combo = ttk.Combobox(self.initial_frame, textvariable=self.initial_var, state="readonly")
        
        # Accepting states section
        self.accepting_frame = ttk.LabelFrame(self.scrollable_frame, text=ACCEPTING_STATES_F, padding=10)
        self.accepting_listbox = tk.Listbox(self.accepting_frame, height=4)
        self.add_accepting_btn = ttk.Button(self.accepting_frame, text=ADD_SELECTED, command=self.add_accepting_state)
        self.remove_accepting_btn = ttk.Button(self.accepting_frame, text=REMOVE_SELECTED, command=self.remove_accepting_state)
        
        # Transitions section
        self.transitions_frame = ttk.LabelFrame(self.scrollable_frame, text=TRANSITIONS_DELTA, padding=10)
        self.transitions_tree = ttk.Treeview(self.transitions_frame, columns=(FROM, SYMBOL, TO), show="headings", height=8)
        self.transitions_tree.heading(FROM, text=FROM)
        self.transitions_tree.heading(SYMBOL, text=SYMBOL)
        self.transitions_tree.heading(TO, text=TO)
        
        # Transition input
        self.trans_input_frame = ttk.Frame(self.transitions_frame)
        self.from_var = tk.StringVar()
        self.symbol_var = tk.StringVar()
        self.to_var = tk.StringVar()
        
        self.from_combo = ttk.Combobox(self.trans_input_frame, textvariable=self.from_var, state="readonly", width=15)
        self.symbol_combo = ttk.Combobox(self.trans_input_frame, textvariable=self.symbol_var, state="readonly", width=10)
        self.to_combo = ttk.Combobox(self.trans_input_frame, textvariable=self.to_var, state="readonly", width=15)
        
        self.add_transition_btn = ttk.Button(self.trans_input_frame, text=ADD_TRANSITION, command=self.add_transition)
        self.remove_transition_btn = ttk.Button(self.trans_input_frame, text=REMOVE_SELECTED, command=self.remove_transition)
        
        # AFD Summary section
        self.summary_frame = ttk.LabelFrame(self.scrollable_frame, text=AFD_SUMMARY, padding=10)
        self.summary_text = tk.Text(self.summary_frame, height=8, width=60, state="disabled")
        
        # Action buttons
        self.actions_frame = ttk.Frame(self.scrollable_frame)
        self.validate_btn = ttk.Button(self.actions_frame, text=VALIDATE_AFD, command=self.validate_current_afd)
        self.clear_btn = ttk.Button(self.actions_frame, text=CLEAR_ALL, command=self.clear_all)
        self.generate_btn = ttk.Button(self.actions_frame, text=GENERATE_COMPLETE_AFD, command=self.generate_complete_afd)
    
    def setup_layout(self):
        """Setup the layout of widgets."""
        # Main frame
        self.main_frame.pack(fill="both", expand=True)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # States section
        self.states_frame.pack(fill="x", padx=10, pady=5)
        self.states_entry.pack(side="left", padx=(0, 5))
        self.add_states_btn.pack(side="left", padx=5)
        self.states_listbox.pack(fill="x", pady=5)
        self.remove_state_btn.pack(pady=5)
        
        # Alphabet section
        self.alphabet_frame.pack(fill="x", padx=10, pady=5)
        self.alphabet_entry.pack(side="left", padx=(0, 5))
        self.add_alphabet_btn.pack(side="left", padx=5)
        self.alphabet_listbox.pack(fill="x", pady=5)
        self.remove_alphabet_btn.pack(pady=5)
        
        # Initial state section
        self.initial_frame.pack(fill="x", padx=10, pady=5)
        self.initial_combo.pack(fill="x")
        
        # Accepting states section
        self.accepting_frame.pack(fill="x", padx=10, pady=5)
        self.accepting_listbox.pack(fill="x", pady=5)
        self.add_accepting_btn.pack(side="left", padx=(0, 5))
        self.remove_accepting_btn.pack(side="left")
        
        # Transitions section
        self.transitions_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.transitions_tree.pack(fill="both", expand=True, pady=5)
        
        self.trans_input_frame.pack(fill="x", pady=5)
        self.from_combo.pack(side="left", padx=(0, 5))
        ttk.Label(self.trans_input_frame, text="con").pack(side="left", padx=5)
        self.symbol_combo.pack(side="left", padx=5)
        ttk.Label(self.trans_input_frame, text="→").pack(side="left", padx=5)
        self.to_combo.pack(side="left", padx=(0, 5))
        self.add_transition_btn.pack(side="left", padx=5)
        self.remove_transition_btn.pack(side="left", padx=(5, 0))
        
        # Summary section
        self.summary_frame.pack(fill="x", padx=10, pady=5)
        self.summary_text.pack(fill="x")
        
        # Actions section
        self.actions_frame.pack(fill="x", padx=10, pady=5)
        self.validate_btn.pack(side="left", padx=(0, 5))
        self.clear_btn.pack(side="left", padx=5)
        self.generate_btn.pack(side="left", padx=5)
        
        # Bind events
        self.states_listbox.bind("<<ListboxSelect>>", self.on_states_selection)
        self.alphabet_listbox.bind("<<ListboxSelect>>", self.on_alphabet_selection)
    
    def setup_help_tooltips(self):
        """Setup help tooltips for all widgets."""
        # States section
        self.help_system.add_tooltip(self.states_entry, "states_entry")
        self.help_system.add_tooltip(self.add_states_btn, "add_states_btn")
        self.help_system.add_tooltip(self.states_listbox, "states_listbox")
        self.help_system.add_tooltip(self.remove_state_btn, "remove_state_btn")
        
        # Alphabet section
        self.help_system.add_tooltip(self.alphabet_entry, "alphabet_entry")
        self.help_system.add_tooltip(self.add_alphabet_btn, "add_alphabet_btn")
        self.help_system.add_tooltip(self.alphabet_listbox, "alphabet_listbox")
        self.help_system.add_tooltip(self.remove_alphabet_btn, "remove_alphabet_btn")
        
        # Initial state section
        self.help_system.add_tooltip(self.initial_combo, "initial_combo")
        
        # Accepting states section
        self.help_system.add_tooltip(self.accepting_listbox, "accepting_listbox")
        self.help_system.add_tooltip(self.add_accepting_btn, "add_accepting_btn")
        self.help_system.add_tooltip(self.remove_accepting_btn, "remove_accepting_btn")
        
        # Transitions section
        # Reducir tooltips en la sección de transiciones para evitar sobreposición
        self.help_system.add_tooltip(self.transitions_tree, "transitions_tree")
        # Solo tooltips en combos cuando reciben foco (bind dinámico)
        for combo, key in [
            (self.from_combo, "from_combo"),
            (self.symbol_combo, "symbol_combo"),
            (self.to_combo, "to_combo"),
        ]:
            combo.bind("<FocusIn>", lambda e, c=combo, k=key: self.help_system.add_tooltip(c, k))
        
        self.help_system.add_tooltip(self.add_transition_btn, "add_transition_btn")
        self.help_system.add_tooltip(self.remove_transition_btn, "remove_transition_btn")
        
        # Action buttons
        self.help_system.add_tooltip(self.validate_btn, "validate_btn")
        self.help_system.add_tooltip(self.clear_btn, "clear_btn")
        self.help_system.add_tooltip(self.generate_btn, "generate_btn")
    
    def setup_validation(self):
        """Setup validation for form fields."""
        # Register fields for validation
        self.validation_feedback.register_field('states', self.states_listbox)
        self.validation_feedback.register_field('alphabet', self.alphabet_listbox)
        self.validation_feedback.register_field('initial_state', self.initial_combo)
        self.validation_feedback.register_field('accepting_states', self.accepting_listbox)
        self.validation_feedback.register_field('transitions', self.transitions_tree)
    
    def add_states(self):
        """Add states from the entry field."""
        states_text = self.states_entry.get().strip()
        if not states_text:
            messagebox.showwarning(WARNING, ENTER_STATE_NAMES)
            return
        
        states = [s.strip() for s in states_text.split()]
        valid_states = []
        errors = []
        
        for state in states:
            is_valid, error = validate_state_name(state)
            if is_valid:
                if state not in [self.states_listbox.get(i) for i in range(self.states_listbox.size())]:
                    valid_states.append(state)
            else:
                errors.append(f"'{state}': {error}")
        
        if errors:
            error_text = "Invalid state names:\n" + "\n".join(errors)
            messagebox.showerror("Error", error_text)
            return
        
        for state in valid_states:
            self.states_listbox.insert(tk.END, state)
        
        self.states_entry.delete(0, tk.END)
        self.update_afd()
    
    def remove_state(self):
        """Remove selected state."""
        selection = self.states_listbox.curselection()
        if selection:
            self.states_listbox.delete(selection[0])
            self.update_afd()
    
    def add_alphabet(self):
        """Add alphabet symbols from the entry field."""
        symbols_text = self.alphabet_entry.get().strip()
        if not symbols_text:
            messagebox.showwarning(WARNING, ENTER_SYMBOLS)
            return
        
        symbols = [s.strip() for s in symbols_text.split()]
        valid_symbols = []
        errors = []
        
        for symbol in symbols:
            is_valid, error = validate_symbol(symbol)
            if is_valid:
                if symbol not in [self.alphabet_listbox.get(i) for i in range(self.alphabet_listbox.size())]:
                    valid_symbols.append(symbol)
            else:
                errors.append(f"'{symbol}': {error}")
        
        if errors:
            error_text = "Invalid symbols:\n" + "\n".join(errors)
            messagebox.showerror("Error", error_text)
            return
        
        for symbol in valid_symbols:
            self.alphabet_listbox.insert(tk.END, symbol)
        
        self.alphabet_entry.delete(0, tk.END)
        self.update_afd()
    
    def remove_alphabet(self):
        """Remove selected alphabet symbol."""
        selection = self.alphabet_listbox.curselection()
        if selection:
            self.alphabet_listbox.delete(selection[0])
            self.update_afd()
    
    def add_accepting_state(self):
        """Add selected state as accepting state."""
        selection = self.states_listbox.curselection()
        if not selection:
            messagebox.showwarning(WARNING, SELECT_STATE_FROM_LIST)
            return
            
        state = self.states_listbox.get(selection[0])
        if not state:
            messagebox.showwarning(WARNING, NO_STATE_SELECTED)
            return
            
        # Check if already in accepting states
        existing_states = [self.accepting_listbox.get(i) for i in range(self.accepting_listbox.size())]
        if state not in existing_states:
            self.accepting_listbox.insert(tk.END, state)
            self.update_afd()
            messagebox.showinfo(SUCCESS, f"Estado '{state}' agregado como de aceptación")
        else:
            messagebox.showwarning(WARNING, f"El estado '{state}' ya es de aceptación")
    
    def remove_accepting_state(self):
        """Remove selected accepting state."""
        selection = self.accepting_listbox.curselection()
        if selection:
            self.accepting_listbox.delete(selection[0])
            self.update_afd()
    
    def add_transition(self):
        """Add a new transition."""
        from_state = self.from_var.get().strip()
        symbol = self.symbol_var.get().strip()
        to_state = self.to_var.get().strip()
        
        if not from_state:
            messagebox.showwarning(WARNING, SELECT_FROM_STATE)
            return
        if not symbol:
            messagebox.showwarning(WARNING, SELECT_SYMBOL)
            return
        if not to_state:
            messagebox.showwarning(WARNING, SELECT_TO_STATE)
            return
        
        # Check if transition already exists
        for item in self.transitions_tree.get_children():
            values = self.transitions_tree.item(item, "values")
            if len(values) >= 2 and values[0] == from_state and values[1] == symbol:
                messagebox.showwarning(WARNING, f"La transición δ({from_state}, {symbol}) ya existe")
                return
        
        # Add the transition
        self.transitions_tree.insert("", "end", values=(from_state, symbol, to_state))
        self.update_afd()
        
        # Clear the input fields
        self.from_var.set("")
        self.symbol_var.set("")
        self.to_var.set("")
        
        messagebox.showinfo(SUCCESS, f"Transición δ({from_state}, {symbol}) → {to_state} agregada")
    
    def remove_transition(self):
        """Remove selected transition."""
        selection = self.transitions_tree.selection()
        if selection:
            self.transitions_tree.delete(selection[0])
            self.update_afd()
    
    def on_states_selection(self, event):
        """Handle states listbox selection."""
        self.update_comboboxes()
    
    def on_alphabet_selection(self, event):
        """Handle alphabet listbox selection."""
        self.update_comboboxes()
    
    def update_comboboxes(self):
        """Update comboboxes with current states and symbols."""
        try:
            # Update initial state combo
            states = [self.states_listbox.get(i) for i in range(self.states_listbox.size())]
            self.initial_combo['values'] = states
            
            # Update transition comboboxes
            self.from_combo['values'] = states
            self.to_combo['values'] = states
            
            symbols = [self.alphabet_listbox.get(i) for i in range(self.alphabet_listbox.size())]
            self.symbol_combo['values'] = symbols
            
            # Force update of comboboxes
            self.initial_combo.update()
            self.from_combo.update()
            self.to_combo.update()
            self.symbol_combo.update()
            
        except Exception as e:
            print(f"Error updating comboboxes: {e}")
            # Continue without failing
    
    def update_afd(self):
        """Update the current AFD with current form data."""
        try:
            if not self.current_afd:
                self.current_afd = AFD()
            
            # Clear current AFD
            self.current_afd.states.clear()
            self.current_afd.alphabet.clear()
            self.current_afd.accepting_states.clear()
            self.current_afd.transitions.clear()
            
            # Add states
            for i in range(self.states_listbox.size()):
                state = self.states_listbox.get(i)
                if state:
                    self.current_afd.add_state(state)
            
            # Add alphabet
            for i in range(self.alphabet_listbox.size()):
                symbol = self.alphabet_listbox.get(i)
                if symbol:
                    self.current_afd.add_symbol(symbol)
            
            # Set initial state
            initial_state = self.initial_var.get().strip()
            if initial_state and initial_state in self.current_afd.states:
                try:
                    self.current_afd.set_initial_state(initial_state)
                except ValueError as e:
                    print(f"Error setting initial state: {e}")
            
            # Add accepting states
            for i in range(self.accepting_listbox.size()):
                state = self.accepting_listbox.get(i)
                if state and state in self.current_afd.states:
                    try:
                        self.current_afd.add_accepting_state(state)
                    except ValueError as e:
                        print(f"Error adding accepting state: {e}")
            
            # Add transitions
            for item in self.transitions_tree.get_children():
                values = self.transitions_tree.item(item, "values")
                if len(values) >= 3:
                    from_state, symbol, to_state = values[0], values[1], values[2]
                    if (from_state in self.current_afd.states and 
                        symbol in self.current_afd.alphabet and 
                        to_state in self.current_afd.states):
                        try:
                            self.current_afd.add_transition(from_state, symbol, to_state)
                        except ValueError as e:
                            print(f"Error adding transition: {e}")
            
            self.update_comboboxes()
            self.update_summary()
            self.main_app.update_status(AFD_UPDATED)
            
        except Exception as e:
            print(f"Error updating AFD: {e}")
            self.main_app.update_status(ERROR_UPDATING_AFD)
    
    def update_summary(self):
        """Update the AFD summary display."""
        self.summary_text.config(state="normal")
        self.summary_text.delete(1.0, tk.END)
        
        if self.current_afd:
            summary = str(self.current_afd)
            self.summary_text.insert(1.0, summary)
        
        self.summary_text.config(state="disabled")
    
    def validate_current_afd(self):
        """Validate the current AFD."""
        if not self.current_afd:
            self.help_system.show_contextual_help("no_afd_loaded")
            return
        
        # Validate all fields first
        self.validation_feedback.validate_all_fields()
        
        # Validate complete AFD
        is_valid, errors = self.afd_validator.validate_complete_afd(self.current_afd)
        
        if is_valid:
            self.help_system.show_contextual_help("afd_complete")
            self.validation_feedback.clear_all_messages()
        else:
            # Show detailed validation errors
            error_text = "Errores de validación del AFD:\n\n" + "\n".join(f"• {error}" for error in errors)
            messagebox.showerror(ERROR, error_text)
            self.help_system.show_contextual_help("missing_transitions")
    
    def clear_all(self):
        """Clear all form data."""
        if messagebox.askyesno(CLEAR_ALL, ARE_YOU_SURE_CLEAR_ALL):
            self.states_listbox.delete(0, tk.END)
            self.alphabet_listbox.delete(0, tk.END)
            self.accepting_listbox.delete(0, tk.END)
            self.initial_var.set("")
            self.from_var.set("")
            self.symbol_var.set("")
            self.to_var.set("")
            
            for item in self.transitions_tree.get_children():
                self.transitions_tree.delete(item)
            
            self.current_afd = None
            self.update_summary()
            self.main_app.update_status(ALL_DATA_CLEARED)
    
    def generate_complete_afd(self):
        """Generate all possible transitions for the current states and alphabet."""
        if not self.current_afd or not self.current_afd.states or not self.current_afd.alphabet:
            messagebox.showwarning(WARNING, DEFINE_STATES_AND_ALPHABET_FIRST)
            return
        
        if messagebox.askyesno(GENERATE_COMPLETE_AFD, 
                              THIS_WILL_GENERATE_ALL_TRANSITIONS):
            # Clear existing transitions
            for item in self.transitions_tree.get_children():
                self.transitions_tree.delete(item)
            
            # Generate all transitions
            for state in self.current_afd.states:
                for symbol in self.current_afd.alphabet:
                    self.transitions_tree.insert("", "end", values=(state, symbol, state))
            
            self.update_afd()
            messagebox.showinfo("Success", "Complete AFD generated. Edit transitions as needed.")
    
    def set_afd(self, afd: Optional[AFD]):
        """Set the AFD to edit."""
        self.current_afd = afd
        
        if afd:
            # Clear current form
            self.clear_form()
            
            # Populate states
            for state in sorted(afd.states):
                self.states_listbox.insert(tk.END, state)
            
            # Populate alphabet
            for symbol in sorted(afd.alphabet):
                self.alphabet_listbox.insert(tk.END, symbol)
            
            # Set initial state
            if afd.initial_state:
                self.initial_var.set(afd.initial_state)
            
            # Populate accepting states
            for state in sorted(afd.accepting_states):
                self.accepting_listbox.insert(tk.END, state)
            
            # Populate transitions
            for (from_state, symbol), to_state in sorted(afd.transitions.items()):
                self.transitions_tree.insert("", "end", values=(from_state, symbol, to_state))
            
            self.update_comboboxes()
            self.update_summary()
        else:
            self.clear_form()
    
    def clear_form(self):
        """Clear the form without confirmation."""
        self.states_listbox.delete(0, tk.END)
        self.alphabet_listbox.delete(0, tk.END)
        self.accepting_listbox.delete(0, tk.END)
        self.initial_var.set("")
        self.from_var.set("")
        self.symbol_var.set("")
        self.to_var.set("")
        
        for item in self.transitions_tree.get_children():
            self.transitions_tree.delete(item)
        
        self.update_summary()
