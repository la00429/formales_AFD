"""
Sistema de tutorial paso a paso para la GUI del simulador AFD.

Este módulo proporciona un tutorial interactivo que guía a los usuarios
nuevos a través de las funcionalidades principales de la aplicación.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Optional, Callable
from enum import Enum


class TutorialStep:
    """Paso individual del tutorial."""
    
    def __init__(self, title: str, description: str, target_widget: str = None, 
                 action: str = None, highlight: bool = True):
        """
        Inicializar paso del tutorial.
        
        Args:
            title: Título del paso
            description: Descripción detallada del paso
            target_widget: Widget objetivo (opcional)
            action: Acción a realizar (opcional)
            highlight: Si debe resaltar el widget objetivo
        """
        self.title = title
        self.description = description
        self.target_widget = target_widget
        self.action = action
        self.highlight = highlight


class TutorialSystem:
    """Sistema de tutorial interactivo."""
    
    def __init__(self, parent, main_app):
        """
        Inicializar sistema de tutorial.
        
        Args:
            parent: Widget padre
            main_app: Aplicación principal
        """
        self.parent = parent
        self.main_app = main_app
        self.tutorial_window = None
        self.current_step = 0
        self.tutorial_steps: List[TutorialStep] = []
        self.highlight_overlay = None
        
        self.setup_tutorial_steps()
    
    def setup_tutorial_steps(self):
        """Configurar los pasos del tutorial."""
        self.tutorial_steps = [
            # Introducción
            TutorialStep(
                "¡Bienvenido al Simulador AFD!",
                "Este tutorial te guiará a través de las funcionalidades principales de la aplicación. "
                "Aprenderás a crear, editar y probar autómatas finitos deterministas.",
                highlight=False
            ),
            
            # Editor AFD - Estados
            TutorialStep(
                "Paso 1: Definir Estados",
                "Los estados son los nodos de tu autómata. En el campo 'States', ingresa los nombres "
                "de los estados separados por espacios. Por ejemplo: q0 q1 q2",
                target_widget="states_entry",
                action="focus"
            ),
            
            TutorialStep(
                "Agregar Estados",
                "Después de ingresar los nombres de los estados, haz clic en 'Add States' para "
                "agregarlos a la lista. Verás los estados aparecer en la lista de abajo.",
                target_widget="add_states_btn",
                action="click"
            ),
            
            # Editor AFD - Alfabeto
            TutorialStep(
                "Paso 2: Definir Alfabeto",
                "El alfabeto son los símbolos que tu autómata puede procesar. En el campo 'Alphabet', "
                "ingresa los símbolos separados por espacios. Por ejemplo: a b c o 0 1",
                target_widget="alphabet_entry",
                action="focus"
            ),
            
            TutorialStep(
                "Agregar Símbolos",
                "Haz clic en 'Add Symbols' para agregar los símbolos al alfabeto del autómata.",
                target_widget="add_alphabet_btn",
                action="click"
            ),
            
            # Editor AFD - Estado Inicial
            TutorialStep(
                "Paso 3: Seleccionar Estado Inicial",
                "El estado inicial es donde comienza la ejecución del autómata. Selecciona uno de "
                "los estados que definiste anteriormente en el menú desplegable.",
                target_widget="initial_combo",
                action="focus"
            ),
            
            # Editor AFD - Estados de Aceptación
            TutorialStep(
                "Paso 4: Definir Estados de Aceptación",
                "Los estados de aceptación son los estados finales donde el autómata acepta una cadena. "
                "Selecciona un estado de la lista y haz clic en 'Add Selected'.",
                target_widget="accepting_listbox",
                action="focus"
            ),
            
            TutorialStep(
                "Agregar Estado de Aceptación",
                "Haz clic en 'Add Selected' para agregar el estado seleccionado como estado de aceptación.",
                target_widget="add_accepting_btn",
                action="click"
            ),
            
            # Editor AFD - Transiciones
            TutorialStep(
                "Paso 5: Definir Transiciones",
                "Las transiciones definen cómo el autómata cambia de estado. Selecciona el estado "
                "origen, el símbolo y el estado destino, luego haz clic en 'Add Transition'.",
                target_widget="transitions_tree",
                action="focus"
            ),
            
            TutorialStep(
                "Agregar Transición",
                "Haz clic en 'Add Transition' para agregar la transición definida a la tabla.",
                target_widget="add_transition_btn",
                action="click"
            ),
            
            # Validación
            TutorialStep(
                "Paso 6: Validar AFD",
                "Una vez que hayas definido todos los componentes, haz clic en 'Validate AFD' para "
                "verificar que tu autómata esté completo y sea válido.",
                target_widget="validate_btn",
                action="click"
            ),
            
            # Evaluador de Cadenas
            TutorialStep(
                "Paso 7: Probar Cadenas",
                "Ahora puedes probar tu autómata. Ve a la pestaña 'String Evaluator' para evaluar "
                "cadenas y ver cómo funciona tu autómata paso a paso.",
                target_widget="evaluator_tab",
                action="switch_tab"
            ),
            
            # Visualizador
            TutorialStep(
                "Paso 8: Visualizar AFD",
                "Ve a la pestaña 'AFD Visualizer' para ver una representación gráfica de tu autómata "
                "con estados, transiciones y símbolos.",
                target_widget="visualizer_tab",
                action="switch_tab"
            ),
            
            # Finalización
            TutorialStep(
                "¡Tutorial Completado!",
                "Has completado el tutorial básico. Ahora puedes explorar todas las funcionalidades "
                "de la aplicación. Usa el menú Help para obtener más información.",
                highlight=False
            )
        ]
    
    def start_tutorial(self):
        """Iniciar el tutorial."""
        if self.tutorial_window and self.tutorial_window.winfo_exists():
            self.tutorial_window.lift()
            return
        
        self.current_step = 0
        self.create_tutorial_window()
        self.show_current_step()
    
    def create_tutorial_window(self):
        """Crear ventana del tutorial."""
        self.tutorial_window = tk.Toplevel(self.parent)
        self.tutorial_window.title("Tutorial - Simulador AFD")
        self.tutorial_window.geometry("600x500")
        self.tutorial_window.resizable(False, False)
        
        # Hacer la ventana no modal para no bloquear la interacción
        # Mantenerla al frente sin capturar los eventos de toda la app
        try:
            self.tutorial_window.transient(self.parent)
            self.tutorial_window.attributes('-topmost', True)
        except tk.TclError:
            pass
        
        # Frame principal
        main_frame = ttk.Frame(self.tutorial_window, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Constante para fuente
        FONT_FAMILY = "Segoe UI"
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="Tutorial Interactivo",
            font=(FONT_FAMILY, 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Frame de contenido
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)
        
        # Título del paso
        self.step_title_label = ttk.Label(
            content_frame,
            font=(FONT_FAMILY, 12, "bold"),
            wraplength=550
        )
        self.step_title_label.pack(anchor="w", pady=(0, 10))
        
        # Descripción del paso
        self.step_description_label = ttk.Label(
            content_frame,
            font=(FONT_FAMILY, 10),
            wraplength=550,
            justify="left"
        )
        self.step_description_label.pack(anchor="w", pady=(0, 20))
        
        # Frame de botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(20, 0))
        
        # Botón anterior
        self.prev_button = ttk.Button(
            button_frame,
            text="← Anterior",
            command=self.previous_step,
            state="disabled"
        )
        self.prev_button.pack(side="left")
        
        # Botón siguiente
        self.next_button = ttk.Button(
            button_frame,
            text="Siguiente →",
            command=self.next_step
        )
        self.next_button.pack(side="right")
        
        # Botón cerrar
        self.close_button = ttk.Button(
            button_frame,
            text="Cerrar Tutorial",
            command=self.close_tutorial
        )
        self.close_button.pack(side="right", padx=(0, 10))
        
        # Barra de progreso
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.pack(fill="x", pady=(10, 0))
        
        self.progress_label = ttk.Label(
            self.progress_frame,
            text="Paso 1 de 14",
            font=(FONT_FAMILY, 9)
        )
        self.progress_label.pack(side="left")
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode="determinate",
            length=300
        )
        self.progress_bar.pack(side="right")
        
        # Centrar la ventana
        self.tutorial_window.update_idletasks()
        x = (self.tutorial_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.tutorial_window.winfo_screenheight() // 2) - (500 // 2)
        self.tutorial_window.geometry(f"600x500+{x}+{y}")
    
    def show_current_step(self):
        """Mostrar el paso actual del tutorial."""
        if self.current_step >= len(self.tutorial_steps):
            return
        
        step = self.tutorial_steps[self.current_step]
        
        # Actualizar contenido
        self.step_title_label.config(text=step.title)
        self.step_description_label.config(text=step.description)
        
        # Actualizar botones
        self.prev_button.config(state="normal" if self.current_step > 0 else "disabled")
        
        if self.current_step == len(self.tutorial_steps) - 1:
            self.next_button.config(text="Finalizar", command=self.finish_tutorial)
        else:
            self.next_button.config(text="Siguiente →", command=self.next_step)
        
        # Actualizar progreso
        progress = (self.current_step + 1) / len(self.tutorial_steps) * 100
        self.progress_bar.config(value=progress)
        self.progress_label.config(text=f"Paso {self.current_step + 1} de {len(self.tutorial_steps)}")
        
        # Resaltar widget objetivo si existe
        if step.target_widget and step.highlight:
            self.highlight_target_widget(step.target_widget)
        
        # Realizar acción si existe
        if step.action:
            self.perform_action(step.action, step.target_widget)
    
    def highlight_target_widget(self, widget_name: str):
        """Resaltar widget objetivo."""
        # Limpiar resaltado anterior
        self.clear_highlight()
        
        # Buscar widget en la aplicación
        widget = self.find_widget_by_name(widget_name)
        if widget:
            self.create_highlight_overlay(widget)
    
    def find_widget_by_name(self, widget_name: str) -> Optional[tk.Widget]:
        """Buscar widget por nombre."""
        try:
            # Mapeo de nombres a widgets con verificación de existencia
            widget_map = {
                "states_entry": getattr(self.main_app.afd_editor, 'states_entry', None),
                "add_states_btn": getattr(self.main_app.afd_editor, 'add_states_btn', None),
                "states_listbox": getattr(self.main_app.afd_editor, 'states_listbox', None),
                "alphabet_entry": getattr(self.main_app.afd_editor, 'alphabet_entry', None),
                "add_alphabet_btn": getattr(self.main_app.afd_editor, 'add_alphabet_btn', None),
                "alphabet_listbox": getattr(self.main_app.afd_editor, 'alphabet_listbox', None),
                "initial_combo": getattr(self.main_app.afd_editor, 'initial_combo', None),
                "accepting_listbox": getattr(self.main_app.afd_editor, 'accepting_listbox', None),
                "add_accepting_btn": getattr(self.main_app.afd_editor, 'add_accepting_btn', None),
                "transitions_tree": getattr(self.main_app.afd_editor, 'transitions_tree', None),
                "add_transition_btn": getattr(self.main_app.afd_editor, 'add_transition_btn', None),
                "validate_btn": getattr(self.main_app.afd_editor, 'validate_btn', None),
            }
            
            widget = widget_map.get(widget_name)
            if widget and hasattr(widget, 'winfo_exists') and widget.winfo_exists():
                return widget
            return None
        except Exception:
            return None
    
    def create_highlight_overlay(self, widget: tk.Widget):
        """Crear overlay de resaltado."""
        try:
            # Obtener posición del widget
            x = widget.winfo_rootx()
            y = widget.winfo_rooty()
            width = widget.winfo_width()
            height = widget.winfo_height()
            
            # Crear overlay
            self.highlight_overlay = tk.Toplevel(self.parent)
            self.highlight_overlay.wm_overrideredirect(True)
            self.highlight_overlay.wm_attributes("-topmost", True)
            self.highlight_overlay.wm_attributes("-alpha", 0.3)
            self.highlight_overlay.configure(bg="yellow")
            self.highlight_overlay.geometry(f"{width}x{height}+{x}+{y}")
        except tk.TclError:
            # Ignorar errores de widget
            pass
    
    def clear_highlight(self):
        """Limpiar resaltado."""
        if self.highlight_overlay:
            self.highlight_overlay.destroy()
            self.highlight_overlay = None
    
    def perform_action(self, action: str, widget_name: str):
        """Realizar acción del tutorial."""
        if action == "focus":
            widget = self.find_widget_by_name(widget_name)
            if widget:
                widget.focus_set()
        elif action == "click":
            widget = self.find_widget_by_name(widget_name)
            if widget and hasattr(widget, 'invoke'):
                widget.invoke()
        elif action == "switch_tab":
            if widget_name == "evaluator_tab":
                self.main_app.open_string_evaluator()
            elif widget_name == "visualizer_tab":
                self.main_app.open_visualizer()
    
    def next_step(self):
        """Ir al siguiente paso."""
        if self.current_step < len(self.tutorial_steps) - 1:
            self.current_step += 1
            self.show_current_step()
    
    def previous_step(self):
        """Ir al paso anterior."""
        if self.current_step > 0:
            self.current_step -= 1
            self.show_current_step()
    
    def finish_tutorial(self):
        """Finalizar tutorial."""
        self.close_tutorial()
        messagebox.showinfo(
            "Tutorial Completado",
            "¡Felicidades! Has completado el tutorial. Ahora puedes explorar "
            "todas las funcionalidades de la aplicación. Usa el menú Help "
            "para obtener más información."
        )
    
    def close_tutorial(self):
        """Cerrar tutorial."""
        self.clear_highlight()
        if self.tutorial_window:
            self.tutorial_window.destroy()
            self.tutorial_window = None
    
    def skip_tutorial(self):
        """Saltar tutorial."""
        self.close_tutorial()
    
    def restart_tutorial(self):
        """Reiniciar tutorial desde el principio."""
        self.current_step = 0
        self.show_current_step()
