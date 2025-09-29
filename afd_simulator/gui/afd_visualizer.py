"""
AFD Visualizer GUI component.

This module provides a graphical visualization of AFD definitions
with states, transitions, and accepting states.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
from typing import Optional, Dict, Set, Tuple

from ..core.afd import AFD
from .i18n import *


class AFDVisualizer:
    """
    GUI component for visualizing AFD definitions.
    """
    
    def __init__(self, parent, main_app):
        """
        Initialize the AFD Visualizer.
        
        Args:
            parent: Parent widget
            main_app: Reference to main application
        """
        self.parent = parent
        self.main_app = main_app
        self.canvas_size = 600
        
        self.create_widgets()
        self.setup_layout()
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Control panel
        self.control_frame = ttk.Frame(self.parent)
        self.refresh_btn = ttk.Button(self.control_frame, text=REFRESH_VISUALIZATION, command=self.refresh_visualization)
        self.zoom_in_btn = ttk.Button(self.control_frame, text=ZOOM_IN, command=self.zoom_in)
        self.zoom_out_btn = ttk.Button(self.control_frame, text=ZOOM_OUT, command=self.zoom_out)
        self.reset_zoom_btn = ttk.Button(self.control_frame, text=RESET_ZOOM, command=self.reset_zoom)
        
        # Canvas for visualization
        self.canvas_frame = ttk.Frame(self.parent)
        self.canvas = tk.Canvas(self.canvas_frame, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.scrollbar_v = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_h = ttk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.scrollbar_v.set, xscrollcommand=self.scrollbar_h.set)
        
        # Info panel
        self.info_frame = ttk.LabelFrame(self.parent, text=AFD_INFORMATION, padding=10)
        self.info_text = tk.Text(self.info_frame, height=8, width=50, state="disabled")
        
        # Visualization settings
        self.settings_frame = ttk.LabelFrame(self.parent, text=VISUALIZATION_SETTINGS, padding=10)
        self.show_labels_var = tk.BooleanVar(value=True)
        self.show_initial_var = tk.BooleanVar(value=True)
        self.compact_mode_var = tk.BooleanVar(value=False)
        
        self.show_labels_check = ttk.Checkbutton(self.settings_frame, text=SHOW_STATE_LABELS, variable=self.show_labels_var)
        self.show_initial_check = ttk.Checkbutton(self.settings_frame, text=HIGHLIGHT_INITIAL_STATE, variable=self.show_initial_var)
        self.compact_mode_check = ttk.Checkbutton(self.settings_frame, text=COMPACT_MODE, variable=self.compact_mode_var)
        
        # Bind events
        self.show_labels_var.trace('w', lambda *args: self.refresh_visualization())
        self.show_initial_var.trace('w', lambda *args: self.refresh_visualization())
        self.compact_mode_var.trace('w', lambda *args: self.refresh_visualization())
        
        self.zoom_factor = 1.0
        self.state_positions: Dict[str, Tuple[int, int]] = {}
    
    def setup_layout(self):
        """Setup the layout of widgets."""
        # Control panel
        self.control_frame.pack(fill="x", padx=10, pady=5)
        self.refresh_btn.pack(side="left", padx=(0, 5))
        self.zoom_in_btn.pack(side="left", padx=5)
        self.zoom_out_btn.pack(side="left", padx=5)
        self.reset_zoom_btn.pack(side="left", padx=5)
        
        # Canvas with scrollbars
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_v.grid(row=0, column=1, sticky="ns")
        self.scrollbar_h.grid(row=1, column=0, sticky="ew")
        
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        
        # Info panel
        self.info_frame.pack(fill="x", padx=10, pady=5)
        self.info_text.pack(fill="x")
        
        # Settings panel
        self.settings_frame.pack(fill="x", padx=10, pady=5)
        self.show_labels_check.pack(side="left", padx=(0, 10))
        self.show_initial_check.pack(side="left", padx=(0, 10))
        self.compact_mode_check.pack(side="left")
    
    def refresh_visualization(self):
        """Refresh the AFD visualization."""
        afd = self.main_app.get_current_afd()
        if not afd:
            self.clear_canvas()
            self.update_info("No AFD loaded")
            return
        
        self.clear_canvas()
        self.calculate_state_positions(afd)
        self.draw_afd(afd)
        self.update_info(afd)
    
    def calculate_state_positions(self, afd: AFD):
        """Calculate positions for states in the visualization."""
        states = list(afd.states)
        if not states:
            return
        
        # Center the visualization
        center_x = self.canvas_size // 2
        center_y = self.canvas_size // 2
        
        if len(states) == 1:
            self.state_positions[states[0]] = (center_x, center_y)
        elif len(states) == 2:
            radius = 100
            self.state_positions[states[0]] = (center_x - radius, center_y)
            self.state_positions[states[1]] = (center_x + radius, center_y)
        else:
            # Arrange states in a circle
            radius = min(150, self.canvas_size // 4)
            for i, state in enumerate(states):
                angle = 2 * math.pi * i / len(states) - math.pi / 2  # Start from top
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                self.state_positions[state] = (int(x), int(y))
    
    def draw_afd(self, afd: AFD):
        """Draw the AFD on the canvas."""
        # Draw transitions first (so they appear behind states)
        self.draw_transitions(afd)
        
        # Draw states
        self.draw_states(afd)
        
        # Update scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def draw_states(self, afd: AFD):
        """Draw AFD states."""
        state_radius = 30
        
        for state in afd.states:
            if state in self.state_positions:
                x, y = self.state_positions[state]
                
                # Draw state circle
                if state in afd.accepting_states:
                    # Double circle for accepting states
                    self.canvas.create_oval(
                        x - state_radius, y - state_radius,
                        x + state_radius, y + state_radius,
                        outline="blue", width=3, fill="lightblue"
                    )
                    self.canvas.create_oval(
                        x - state_radius + 8, y - state_radius + 8,
                        x + state_radius - 8, y + state_radius - 8,
                        outline="blue", width=2, fill="white"
                    )
                else:
                    # Single circle for non-accepting states
                    self.canvas.create_oval(
                        x - state_radius, y - state_radius,
                        x + state_radius, y + state_radius,
                        outline="black", width=2, fill="white"
                    )
                
                # Highlight initial state
                if state == afd.initial_state and self.show_initial_var.get():
                    self.canvas.create_oval(
                        x - state_radius - 5, y - state_radius - 5,
                        x + state_radius + 5, y + state_radius + 5,
                        outline="red", width=3, fill=""
                    )
                
                # Draw state label
                if self.show_labels_var.get():
                    self.canvas.create_text(x, y, text=state, font=("Arial", 12, "bold"))
    
    def draw_transitions(self, afd: AFD):
        """Draw AFD transitions."""
        for (from_state, symbol), to_state in afd.transitions.items():
            if from_state in self.state_positions and to_state in self.state_positions:
                from_x, from_y = self.state_positions[from_state]
                to_x, to_y = self.state_positions[to_state]
                
                # Calculate arrow position
                if from_state == to_state:
                    # Self-loop
                    self.draw_self_loop(from_x, from_y, symbol)
                else:
                    # Regular transition
                    self.draw_arrow(from_x, from_y, to_x, to_y, symbol)
    
    def draw_self_loop(self, x: int, y: int, symbol: str):
        """Draw a self-loop transition."""
        radius = 40
        # Draw arc for self-loop
        self.canvas.create_arc(
            x - radius, y - radius,
            x + radius, y + radius,
            start=0, extent=270,
            outline="black", width=2
        )
        
        # Draw arrowhead
        arrow_x = x + radius * math.cos(math.radians(45))
        arrow_y = y - radius * math.sin(math.radians(45))
        self.draw_arrowhead(arrow_x, arrow_y, 45)
        
        # Draw symbol label
        label_x = x + radius * math.cos(math.radians(135))
        label_y = y - radius * math.sin(math.radians(135))
        self.canvas.create_text(label_x, label_y, text=symbol, font=("Arial", 10))
    
    def draw_arrow(self, from_x: int, from_y: int, to_x: int, to_y: int, symbol: str):
        """Draw an arrow from one state to another."""
        # Calculate positions on the circle edges
        dx = to_x - from_x
        dy = to_y - from_y
        length = math.sqrt(dx*dx + dy*dy)
        
        if length > 0:
            # Normalize direction vector
            dx /= length
            dy /= length
            
            # Calculate arrow positions (30 pixels from circle edges)
            arrow_from_x = from_x + dx * 30
            arrow_from_y = from_y + dy * 30
            arrow_to_x = to_x - dx * 30
            arrow_to_y = to_y - dy * 30
            
            # Draw arrow line
            self.canvas.create_line(
                arrow_from_x, arrow_from_y, arrow_to_x, arrow_to_y,
                arrow=tk.LAST, arrowshape=(10, 12, 3), width=2
            )
            
            # Draw symbol label at midpoint
            mid_x = (arrow_from_x + arrow_to_x) / 2
            mid_y = (arrow_from_y + arrow_to_y) / 2
            
            # Offset label perpendicular to arrow
            offset = 15
            perp_x = -dy * offset
            perp_y = dx * offset
            
            label_x = mid_x + perp_x
            label_y = mid_y + perp_y
            
            self.canvas.create_text(label_x, label_y, text=symbol, font=("Arial", 10))
    
    def draw_arrowhead(self, x: int, y: int, angle: float):
        """Draw an arrowhead at the specified position and angle."""
        size = 8
        angle_rad = math.radians(angle)
        
        # Calculate arrowhead points
        x1 = x - size * math.cos(angle_rad - math.pi/6)
        y1 = y + size * math.sin(angle_rad - math.pi/6)
        x2 = x - size * math.cos(angle_rad + math.pi/6)
        y2 = y + size * math.sin(angle_rad + math.pi/6)
        
        self.canvas.create_polygon(x, y, x1, y1, x2, y2, fill="black")
    
    def clear_canvas(self):
        """Clear the canvas."""
        self.canvas.delete("all")
    
    def update_info(self, afd_or_message):
        """Update the information panel."""
        self.info_text.config(state="normal")
        self.info_text.delete(1.0, tk.END)
        
        if isinstance(afd_or_message, str):
            self.info_text.insert(1.0, afd_or_message)
        else:
            afd = afd_or_message
            info = f"""Información del AFD:
Estados: {len(afd.states)} ({', '.join(sorted(afd.states))})
Alfabeto: {len(afd.alphabet)} ({', '.join(sorted(afd.alphabet))})
Estado inicial: {afd.initial_state or NOT_SET}
Estados de aceptación: {len(afd.accepting_states)} ({', '.join(sorted(afd.accepting_states))})
Transiciones: {len(afd.transitions)}
Válido: {VALID if afd.is_valid() else INVALID}

Leyenda:
• {LEGEND_BLACK_CIRCLE}
• {LEGEND_BLUE_DOUBLE_CIRCLE}
• {LEGEND_RED_OUTLINE}
• {LEGEND_ARROWS}"""
            
            self.info_text.insert(1.0, info)
        
        self.info_text.config(state="disabled")
    
    def zoom_in(self):
        """Zoom in the visualization."""
        self.zoom_factor *= 1.2
        self.canvas.scale("all", 0, 0, 1.2, 1.2)
    
    def zoom_out(self):
        """Zoom out the visualization."""
        self.zoom_factor *= 0.8
        self.canvas.scale("all", 0, 0, 0.8, 0.8)
    
    def reset_zoom(self):
        """Reset zoom to original size."""
        self.canvas.scale("all", 0, 0, 1.0/self.zoom_factor, 1.0/self.zoom_factor)
        self.zoom_factor = 1.0
