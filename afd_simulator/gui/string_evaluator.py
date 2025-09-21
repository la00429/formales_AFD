"""
String Evaluator GUI component.

This module provides a graphical interface for evaluating strings
against AFD definitions with step-by-step visualization.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List, Tuple

from ..core.afd import AFD


class StringEvaluator:
    """
    GUI component for evaluating strings against AFD definitions.
    """
    
    def __init__(self, parent, main_app):
        """
        Initialize the String Evaluator.
        
        Args:
            parent: Parent widget
            main_app: Reference to main application
        """
        self.parent = parent
        self.main_app = main_app
        
        self.create_widgets()
        self.setup_layout()
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Input section
        self.input_frame = ttk.LabelFrame(self.parent, text="String Evaluation", padding=10)
        self.input_label = ttk.Label(self.input_frame, text="Enter string to evaluate:")
        self.string_entry = ttk.Entry(self.input_frame, width=40)
        self.evaluate_btn = ttk.Button(self.input_frame, text="Evaluate", command=self.evaluate_string)
        self.clear_btn = ttk.Button(self.input_frame, text="Clear", command=self.clear_evaluation)
        
        # Results section
        self.results_frame = ttk.LabelFrame(self.parent, text="Evaluation Results", padding=10)
        self.result_label = ttk.Label(self.results_frame, text="No string evaluated yet")
        self.result_label.config(font=("Arial", 12, "bold"))
        
        # Step-by-step visualization
        self.steps_frame = ttk.LabelFrame(self.parent, text="Step-by-Step Process", padding=10)
        self.steps_tree = ttk.Treeview(
            self.steps_frame, 
            columns=("Step", "From", "Symbol", "To", "Description"), 
            show="headings", 
            height=10
        )
        
        # Configure tree columns
        self.steps_tree.heading("Step", text="Step")
        self.steps_tree.heading("From", text="From State")
        self.steps_tree.heading("Symbol", text="Symbol")
        self.steps_tree.heading("To", text="To State")
        self.steps_tree.heading("Description", text="Description")
        
        self.steps_tree.column("Step", width=50)
        self.steps_tree.column("From", width=80)
        self.steps_tree.column("Symbol", width=60)
        self.steps_tree.column("To", width=80)
        self.steps_tree.column("Description", width=300)
        
        # Batch evaluation section
        self.batch_frame = ttk.LabelFrame(self.parent, text="Batch String Evaluation", padding=10)
        self.batch_label = ttk.Label(self.batch_frame, text="Enter multiple strings (one per line):")
        self.batch_text = tk.Text(self.batch_frame, height=6, width=50)
        self.batch_evaluate_btn = ttk.Button(self.batch_frame, text="Evaluate All", command=self.evaluate_batch)
        self.batch_clear_btn = ttk.Button(self.batch_frame, text="Clear", command=self.clear_batch)
        
        # Batch results
        self.batch_results_frame = ttk.LabelFrame(self.parent, text="Batch Results", padding=10)
        self.batch_results_tree = ttk.Treeview(
            self.batch_results_frame,
            columns=("String", "Result", "Steps"),
            show="headings",
            height=8
        )
        
        self.batch_results_tree.heading("String", text="String")
        self.batch_results_tree.heading("Result", text="Result")
        self.batch_results_tree.heading("Steps", text="Steps")
        
        self.batch_results_tree.column("String", width=150)
        self.batch_results_tree.column("Result", width=100)
        self.batch_results_tree.column("Steps", width=80)
    
    def setup_layout(self):
        """Setup the layout of widgets."""
        # Input section
        self.input_frame.pack(fill="x", padx=10, pady=5)
        self.input_label.pack(anchor="w")
        input_row = ttk.Frame(self.input_frame)
        input_row.pack(fill="x", pady=5)
        self.string_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.evaluate_btn.pack(side="left", padx=5)
        self.clear_btn.pack(side="left", padx=5)
        
        # Results section
        self.results_frame.pack(fill="x", padx=10, pady=5)
        self.result_label.pack(pady=5)
        
        # Steps section
        self.steps_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.steps_tree.pack(fill="both", expand=True)
        
        # Batch evaluation section
        self.batch_frame.pack(fill="x", padx=10, pady=5)
        self.batch_label.pack(anchor="w")
        self.batch_text.pack(fill="x", pady=5)
        batch_buttons = ttk.Frame(self.batch_frame)
        batch_buttons.pack(fill="x")
        self.batch_evaluate_btn.pack(side="left", padx=(0, 5))
        self.batch_clear_btn.pack(side="left")
        
        # Batch results section
        self.batch_results_frame.pack(fill="x", padx=10, pady=5)
        self.batch_results_tree.pack(fill="x")
        
        # Bind Enter key to evaluation
        self.string_entry.bind("<Return>", lambda e: self.evaluate_string())
    
    def evaluate_string(self):
        """Evaluate the entered string against the current AFD."""
        afd = self.main_app.get_current_afd()
        if not afd:
            messagebox.showwarning("Warning", "No AFD loaded. Please create or load an AFD first.")
            return
        
        if not afd.is_valid():
            messagebox.showwarning("Warning", "Current AFD is not valid. Please complete the AFD definition.")
            return
        
        input_string = self.string_entry.get().strip()
        if not input_string:
            messagebox.showwarning("Warning", "Please enter a string to evaluate.")
            return
        
        try:
            is_accepted, transitions_path = afd.evaluate_string(input_string)
            
            # Update result label
            result_text = f"String '{input_string}' is {'ACCEPTED' if is_accepted else 'REJECTED'}"
            self.result_label.config(text=result_text)
            
            # Update result label color
            if is_accepted:
                self.result_label.config(foreground="green")
            else:
                self.result_label.config(foreground="red")
            
            # Clear and populate steps
            for item in self.steps_tree.get_children():
                self.steps_tree.delete(item)
            
            for i, (from_state, symbol, to_state) in enumerate(transitions_path, 1):
                description = f"From state ({from_state}) with symbol '{symbol}' transitions to state ({to_state})"
                self.steps_tree.insert("", "end", values=(i, from_state, symbol, to_state, description))
            
            # Show final state
            if transitions_path:
                final_state = transitions_path[-1][2]
                final_description = f"Final state: {final_state} - {'Accepting' if is_accepted else 'Non-accepting'}"
                self.steps_tree.insert("", "end", values=("", "", "", final_state, final_description))
            
            self.main_app.update_status(f"String '{input_string}' evaluated: {'ACCEPTED' if is_accepted else 'REJECTED'}")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Evaluation failed: {e}")
            self.result_label.config(text="Evaluation failed", foreground="red")
    
    def clear_evaluation(self):
        """Clear the current evaluation."""
        self.string_entry.delete(0, tk.END)
        self.result_label.config(text="No string evaluated yet", foreground="black")
        
        for item in self.steps_tree.get_children():
            self.steps_tree.delete(item)
    
    def evaluate_batch(self):
        """Evaluate multiple strings from the batch input."""
        afd = self.main_app.get_current_afd()
        if not afd:
            messagebox.showwarning("Warning", "No AFD loaded. Please create or load an AFD first.")
            return
        
        if not afd.is_valid():
            messagebox.showwarning("Warning", "Current AFD is not valid. Please complete the AFD definition.")
            return
        
        batch_text = self.batch_text.get("1.0", tk.END).strip()
        if not batch_text:
            messagebox.showwarning("Warning", "Please enter strings to evaluate.")
            return
        
        strings = [s.strip() for s in batch_text.split('\n') if s.strip()]
        if not strings:
            messagebox.showwarning("Warning", "No valid strings found.")
            return
        
        # Clear previous batch results
        for item in self.batch_results_tree.get_children():
            self.batch_results_tree.delete(item)
        
        # Evaluate each string
        for string in strings:
            try:
                is_accepted, transitions_path = afd.evaluate_string(string)
                result = "ACCEPTED" if is_accepted else "REJECTED"
                steps = len(transitions_path)
                
                self.batch_results_tree.insert("", "end", values=(string, result, steps))
                
            except ValueError as e:
                self.batch_results_tree.insert("", "end", values=(string, f"ERROR: {e}", 0))
        
        self.main_app.update_status(f"Batch evaluation completed: {len(strings)} strings processed")
    
    def clear_batch(self):
        """Clear the batch input and results."""
        self.batch_text.delete("1.0", tk.END)
        
        for item in self.batch_results_tree.get_children():
            self.batch_results_tree.delete(item)
    
    def update_afd_info(self):
        """Update the interface when AFD changes."""
        afd = self.main_app.get_current_afd()
        if afd:
            # Update any AFD-specific information if needed
            pass
        else:
            self.clear_evaluation()
            self.clear_batch()
