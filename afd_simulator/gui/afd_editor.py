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


class AFDEditor:
    """
    GUI component for editing AFD definitions.
    """
    
    # Constants for button text
    REMOVE_SELECTED_TEXT = "Remove Selected"
    
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
        
        self.create_widgets()
        self.setup_layout()
    
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
        self.states_frame = ttk.LabelFrame(self.scrollable_frame, text="States (Q)", padding=10)
        self.states_entry = ttk.Entry(self.states_frame, width=40)
        self.add_states_btn = ttk.Button(self.states_frame, text="Add States", command=self.add_states)
        self.states_listbox = tk.Listbox(self.states_frame, height=6)
        self.remove_state_btn = ttk.Button(self.states_frame, text=self.REMOVE_SELECTED_TEXT, command=self.remove_state)
        
        # Alphabet section
        self.alphabet_frame = ttk.LabelFrame(self.scrollable_frame, text="Alphabet (Σ)", padding=10)
        self.alphabet_entry = ttk.Entry(self.alphabet_frame, width=40)
        self.add_alphabet_btn = ttk.Button(self.alphabet_frame, text="Add Symbols", command=self.add_alphabet)
        self.alphabet_listbox = tk.Listbox(self.alphabet_frame, height=4)
        self.remove_alphabet_btn = ttk.Button(self.alphabet_frame, text=self.REMOVE_SELECTED_TEXT, command=self.remove_alphabet)
        
        # Initial state section
        self.initial_frame = ttk.LabelFrame(self.scrollable_frame, text="Initial State (q₀)", padding=10)
        self.initial_var = tk.StringVar()
        self.initial_combo = ttk.Combobox(self.initial_frame, textvariable=self.initial_var, state="readonly")
        
        # Accepting states section
        self.accepting_frame = ttk.LabelFrame(self.scrollable_frame, text="Accepting States (F)", padding=10)
        self.accepting_listbox = tk.Listbox(self.accepting_frame, height=4)
        self.add_accepting_btn = ttk.Button(self.accepting_frame, text="Add Selected", command=self.add_accepting_state)
        self.remove_accepting_btn = ttk.Button(self.accepting_frame, text=self.REMOVE_SELECTED_TEXT, command=self.remove_accepting_state)
        
        # Transitions section
        self.transitions_frame = ttk.LabelFrame(self.scrollable_frame, text="Transitions (δ)", padding=10)
        self.transitions_tree = ttk.Treeview(self.transitions_frame, columns=("From", "Symbol", "To"), show="headings", height=8)
        self.transitions_tree.heading("From", text="From State")
        self.transitions_tree.heading("Symbol", text="Symbol")
        self.transitions_tree.heading("To", text="To State")
        
        # Transition input
        self.trans_input_frame = ttk.Frame(self.transitions_frame)
        self.from_var = tk.StringVar()
        self.symbol_var = tk.StringVar()
        self.to_var = tk.StringVar()
        
        self.from_combo = ttk.Combobox(self.trans_input_frame, textvariable=self.from_var, state="readonly", width=15)
        self.symbol_combo = ttk.Combobox(self.trans_input_frame, textvariable=self.symbol_var, state="readonly", width=10)
        self.to_combo = ttk.Combobox(self.trans_input_frame, textvariable=self.to_var, state="readonly", width=15)
        
        self.add_transition_btn = ttk.Button(self.trans_input_frame, text="Add Transition", command=self.add_transition)
        self.remove_transition_btn = ttk.Button(self.trans_input_frame, text=self.REMOVE_SELECTED_TEXT, command=self.remove_transition)
        
        # AFD Summary section
        self.summary_frame = ttk.LabelFrame(self.scrollable_frame, text="AFD Summary", padding=10)
        self.summary_text = tk.Text(self.summary_frame, height=8, width=60, state="disabled")
        
        # Action buttons
        self.actions_frame = ttk.Frame(self.scrollable_frame)
        self.validate_btn = ttk.Button(self.actions_frame, text="Validate AFD", command=self.validate_current_afd)
        self.clear_btn = ttk.Button(self.actions_frame, text="Clear All", command=self.clear_all)
        self.generate_btn = ttk.Button(self.actions_frame, text="Generate Complete AFD", command=self.generate_complete_afd)
    
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
        ttk.Label(self.trans_input_frame, text="with").pack(side="left", padx=5)
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
    
    def add_states(self):
        """Add states from the entry field."""
        states_text = self.states_entry.get().strip()
        if not states_text:
            messagebox.showwarning("Warning", "Please enter state names")
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
            messagebox.showwarning("Warning", "Please enter symbols")
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
        if selection:
            state = self.states_listbox.get(selection[0])
            if state not in [self.accepting_listbox.get(i) for i in range(self.accepting_listbox.size())]:
                self.accepting_listbox.insert(tk.END, state)
                self.update_afd()
    
    def remove_accepting_state(self):
        """Remove selected accepting state."""
        selection = self.accepting_listbox.curselection()
        if selection:
            self.accepting_listbox.delete(selection[0])
            self.update_afd()
    
    def add_transition(self):
        """Add a new transition."""
        from_state = self.from_var.get()
        symbol = self.symbol_var.get()
        to_state = self.to_var.get()
        
        if not all([from_state, symbol, to_state]):
            messagebox.showwarning("Warning", "Please select all transition components")
            return
        
        # Check if transition already exists
        for item in self.transitions_tree.get_children():
            if (self.transitions_tree.item(item, "values")[0] == from_state and 
                self.transitions_tree.item(item, "values")[1] == symbol):
                messagebox.showwarning("Warning", f"Transition δ({from_state}, {symbol}) already exists")
                return
        
        self.transitions_tree.insert("", "end", values=(from_state, symbol, to_state))
        self.update_afd()
    
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
        # Update initial state combo
        states = [self.states_listbox.get(i) for i in range(self.states_listbox.size())]
        self.initial_combo['values'] = states
        
        # Update transition comboboxes
        self.from_combo['values'] = states
        self.to_combo['values'] = states
        
        symbols = [self.alphabet_listbox.get(i) for i in range(self.alphabet_listbox.size())]
        self.symbol_combo['values'] = symbols
    
    def update_afd(self):
        """Update the current AFD with current form data."""
        if not self.current_afd:
            self.current_afd = AFD()
        
        # Clear current AFD
        self.current_afd.states.clear()
        self.current_afd.alphabet.clear()
        self.current_afd.accepting_states.clear()
        self.current_afd.transitions.clear()
        
        # Add states
        for i in range(self.states_listbox.size()):
            self.current_afd.add_state(self.states_listbox.get(i))
        
        # Add alphabet
        for i in range(self.alphabet_listbox.size()):
            self.current_afd.add_symbol(self.alphabet_listbox.get(i))
        
        # Set initial state
        if self.initial_var.get():
            try:
                self.current_afd.set_initial_state(self.initial_var.get())
            except ValueError:
                pass  # State not in list yet
        
        # Add accepting states
        for i in range(self.accepting_listbox.size()):
            try:
                self.current_afd.add_accepting_state(self.accepting_listbox.get(i))
            except ValueError:
                pass  # State not in list yet
        
        # Add transitions
        for item in self.transitions_tree.get_children():
            from_state, symbol, to_state = self.transitions_tree.item(item, "values")
            try:
                self.current_afd.add_transition(from_state, symbol, to_state)
            except ValueError:
                pass  # Invalid transition
        
        self.update_comboboxes()
        self.update_summary()
        self.main_app.update_status("AFD updated")
    
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
            messagebox.showwarning("Warning", "No AFD to validate")
            return
        
        is_valid = self.current_afd.is_valid()
        
        if is_valid:
            messagebox.showinfo("Validation", "AFD is valid and complete!")
        else:
            messagebox.showwarning("Validation", "AFD is not complete. Check for missing transitions.")
    
    def clear_all(self):
        """Clear all form data."""
        if messagebox.askyesno("Clear All", "Are you sure you want to clear all data?"):
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
            self.main_app.update_status("All data cleared")
    
    def generate_complete_afd(self):
        """Generate all possible transitions for the current states and alphabet."""
        if not self.current_afd or not self.current_afd.states or not self.current_afd.alphabet:
            messagebox.showwarning("Warning", "Please define states and alphabet first")
            return
        
        if messagebox.askyesno("Generate Complete AFD", 
                              "This will generate all possible transitions. Continue?"):
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
