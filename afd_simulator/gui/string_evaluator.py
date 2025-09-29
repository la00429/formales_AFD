"""
String Evaluator GUI component.

This module provides a graphical interface for evaluating strings
against AFD definitions with step-by-step visualization.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List, Tuple

from ..core.afd import AFD
from .i18n import *


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
        self.input_frame = ttk.LabelFrame(self.parent, text=STRING_EVALUATION, padding=10)
        self.input_label = ttk.Label(self.input_frame, text=ENTER_STRING_TO_EVALUATE)
        self.string_entry = ttk.Entry(self.input_frame, width=40)
        self.evaluate_btn = ttk.Button(self.input_frame, text=EVALUATE, command=self.evaluate_string)
        self.clear_btn = ttk.Button(self.input_frame, text=CLEAR, command=self.clear_evaluation)
        
        # Results section
        self.results_frame = ttk.LabelFrame(self.parent, text=EVALUATION_RESULTS, padding=10)
        self.result_label = ttk.Label(self.results_frame, text=NO_STRING_EVALUATED)
        self.result_label.config(font=("Arial", 12, "bold"))
        
        # Step-by-step visualization
        self.steps_frame = ttk.LabelFrame(self.parent, text=STEP_BY_STEP_PROCESS, padding=10)
        self.steps_tree = ttk.Treeview(
            self.steps_frame, 
            columns=(STEP, FROM, SYMBOL, TO, DESCRIPTION), 
            show="headings", 
            height=10
        )
        
        # Configure tree columns
        self.steps_tree.heading(STEP, text=STEP)
        self.steps_tree.heading(FROM, text=FROM)
        self.steps_tree.heading(SYMBOL, text=SYMBOL)
        self.steps_tree.heading(TO, text=TO)
        self.steps_tree.heading(DESCRIPTION, text=DESCRIPTION)
        
        self.steps_tree.column(STEP, width=50)
        self.steps_tree.column(FROM, width=80)
        self.steps_tree.column(SYMBOL, width=60)
        self.steps_tree.column(TO, width=80)
        self.steps_tree.column(DESCRIPTION, width=300)
        
        # Batch evaluation section
        self.batch_frame = ttk.LabelFrame(self.parent, text=BATCH_STRING_EVALUATION, padding=10)
        self.batch_label = ttk.Label(self.batch_frame, text=ENTER_MULTIPLE_STRINGS)
        self.batch_text = tk.Text(self.batch_frame, height=6, width=50)
        self.batch_evaluate_btn = ttk.Button(self.batch_frame, text=EVALUATE_ALL, command=self.evaluate_batch)
        self.batch_clear_btn = ttk.Button(self.batch_frame, text=CLEAR, command=self.clear_batch)
        
        # Batch results
        self.batch_results_frame = ttk.LabelFrame(self.parent, text=BATCH_RESULTS, padding=10)
        self.batch_results_tree = ttk.Treeview(
            self.batch_results_frame,
            columns=(STRING, RESULT, STEPS),
            show="headings",
            height=8
        )
        
        self.batch_results_tree.heading(STRING, text=STRING)
        self.batch_results_tree.heading(RESULT, text=RESULT)
        self.batch_results_tree.heading(STEPS, text=STEPS)
        
        self.batch_results_tree.column(STRING, width=150)
        self.batch_results_tree.column(RESULT, width=100)
        self.batch_results_tree.column(STEPS, width=80)
    
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
            messagebox.showwarning(WARNING, "No hay AFD cargado. Crea o carga uno primero.")
            return
        
        if not afd.is_valid():
            messagebox.showwarning(WARNING, "El AFD actual no es válido. Completa su definición.")
            return
        
        input_string = self.string_entry.get().strip()
        if not input_string:
            messagebox.showwarning(WARNING, "Ingresa una cadena para evaluar.")
            return
        
        try:
            is_accepted, transitions_path = afd.evaluate_string(input_string)
            
            # Update result label
            result_text = f"La cadena '{input_string}' fue {ACCEPTED if is_accepted else REJECTED}"
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
                description = f"Desde ({from_state}) con símbolo '{symbol}' transita a ({to_state})"
                self.steps_tree.insert("", "end", values=(i, from_state, symbol, to_state, description))
            
            # Show final state
            if transitions_path:
                final_state = transitions_path[-1][2]
                final_description = f"Estado final: {final_state} - {ACCEPTING if is_accepted else NON_ACCEPTING}"
                self.steps_tree.insert("", "end", values=("", "", "", final_state, final_description))
            
            self.main_app.update_status(f"Cadena '{input_string}' evaluada: {ACCEPTED if is_accepted else REJECTED}")
            
        except ValueError as e:
            messagebox.showerror(ERROR, f"La evaluación falló: {e}")
            self.result_label.config(text="La evaluación falló", foreground="red")
    
    def clear_evaluation(self):
        """Clear the current evaluation."""
        self.string_entry.delete(0, tk.END)
        self.result_label.config(text=NO_STRING_EVALUATED, foreground="black")
        
        for item in self.steps_tree.get_children():
            self.steps_tree.delete(item)
    
    def evaluate_batch(self):
        """Evaluate multiple strings from the batch input."""
        afd = self.main_app.get_current_afd()
        if not afd:
            messagebox.showwarning(WARNING, "No hay AFD cargado. Crea o carga uno primero.")
            return
        
        if not afd.is_valid():
            messagebox.showwarning(WARNING, "El AFD actual no es válido. Completa su definición.")
            return
        
        batch_text = self.batch_text.get("1.0", tk.END).strip()
        if not batch_text:
            messagebox.showwarning(WARNING, "Ingresa cadenas para evaluar.")
            return
        
        strings = [s.strip() for s in batch_text.split('\n') if s.strip()]
        if not strings:
            messagebox.showwarning(WARNING, "No se encontraron cadenas válidas.")
            return
        
        # Clear previous batch results
        for item in self.batch_results_tree.get_children():
            self.batch_results_tree.delete(item)
        
        # Evaluate each string
        for string in strings:
            try:
                is_accepted, transitions_path = afd.evaluate_string(string)
                result = ACCEPTED if is_accepted else REJECTED
                steps = len(transitions_path)
                
                self.batch_results_tree.insert("", "end", values=(string, result, steps))
                
            except ValueError as e:
                self.batch_results_tree.insert("", "end", values=(string, f"ERROR: {e}", 0))
        
        self.main_app.update_status(f"Evaluación por lotes completada: {len(strings)} cadenas procesadas")
    
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
