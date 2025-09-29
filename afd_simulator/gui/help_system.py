"""
Sistema de ayuda contextual para la GUI del simulador AFD.

Este módulo proporciona tooltips, guías contextuales y un sistema
de ayuda integrado para mejorar la experiencia del usuario.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Optional, Callable
import webbrowser


class HelpTooltip:
    """Tooltip contextual que aparece al pasar el mouse sobre elementos.

    Evita superposición manteniendo un único tooltip activo a la vez y
    reposicionándolo cerca del cursor, sin bloquear la interacción.
    """
    # Referencia global al tooltip activo para evitar superposiciones
    active_tooltip = None
    
    def __init__(self, widget, text: str, delay: int = 500):
        """
        Inicializar tooltip.
        
        Args:
            widget: Widget al que se le aplicará el tooltip
            text: Texto del tooltip
            delay: Delay en milisegundos antes de mostrar el tooltip
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.after_id = None
        self.mouse_x = None
        self.mouse_y = None
        
        # Bind events
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Motion>", self.on_motion)
        self.widget.bind("<ButtonPress>", self.on_leave)
        self.widget.bind("<FocusIn>", self.on_leave)
        self.widget.bind("<Destroy>", lambda e: self.hide_tooltip())
    
    def on_enter(self, event):
        """Mostrar tooltip después del delay."""
        self.mouse_x = event.x_root
        self.mouse_y = event.y_root
        self.schedule_tooltip()
    
    def on_leave(self, event):
        """Ocultar tooltip."""
        self.unschedule_tooltip()
        self.hide_tooltip()
    
    def on_motion(self, event):
        """Reprogramar tooltip si el mouse se mueve."""
        self.mouse_x = event.x_root
        self.mouse_y = event.y_root
        if self.tooltip_window:
            # Reposicionar suavemente el tooltip existente
            self.position_tooltip_window()
        else:
            # Evitar reprogramación excesiva
            if not self.after_id:
                self.schedule_tooltip()
    
    def schedule_tooltip(self):
        """Programar la aparición del tooltip."""
        self.after_id = self.widget.after(self.delay, self.show_tooltip)
    
    def unschedule_tooltip(self):
        """Cancelar la programación del tooltip."""
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
    
    def show_tooltip(self):
        """Mostrar el tooltip."""
        if not self.widget.winfo_exists():
            return
        
        # Cerrar cualquier tooltip activo previo para evitar superposición
        if HelpTooltip.active_tooltip and HelpTooltip.active_tooltip is not self:
            HelpTooltip.active_tooltip.hide_tooltip()
        HelpTooltip.active_tooltip = self
        
        if not self.tooltip_window:
            # Crear ventana del tooltip
            self.tooltip_window = tk.Toplevel(self.widget)
            self.tooltip_window.wm_overrideredirect(True)
            self.tooltip_window.attributes("-topmost", True)
            
            # Crear frame con borde
            frame = ttk.Frame(self.tooltip_window, style="Tooltip.TFrame")
            frame.pack()
            
            # Crear label con el texto
            label = ttk.Label(
                frame, 
                text=self.text, 
                style="Tooltip.TLabel",
                wraplength=300,
                justify="left"
            )
            label.pack(padx=8, pady=4)
        else:
            # Ya existe, solo reposicionar
            pass
        
        self.position_tooltip_window()
    
    def position_tooltip_window(self):
        """Posicionar el tooltip cerca del cursor y dentro de la pantalla."""
        if not self.tooltip_window:
            return
        # Posición base
        x = (self.mouse_x or self.widget.winfo_rootx()) + 16
        y = (self.mouse_y or self.widget.winfo_rooty()) + 24
        
        # Obtener tamaño requerido del tooltip
        self.tooltip_window.update_idletasks()
        tw = self.tooltip_window.winfo_reqwidth()
        th = self.tooltip_window.winfo_reqheight()
        sw = self.widget.winfo_screenwidth()
        sh = self.widget.winfo_screenheight()
        
        # Ajustar para que no se salga de la pantalla
        if x + tw + 8 > sw:
            x = max(0, sw - tw - 8)
        if y + th + 8 > sh:
            y = max(0, sh - th - 8)
        
        self.tooltip_window.wm_geometry(f"+{int(x)}+{int(y)}")
    
    def hide_tooltip(self):
        """Ocultar el tooltip."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
        if HelpTooltip.active_tooltip is self:
            HelpTooltip.active_tooltip = None


class HelpSystem:
    """Sistema central de ayuda para la aplicación."""
    
    def __init__(self, root):
        """
        Inicializar sistema de ayuda.
        
        Args:
            root: Ventana principal de la aplicación
        """
        self.root = root
        self.tooltips: Dict[tk.Widget, HelpTooltip] = {}
        self.help_window = None
        
        # Configurar estilos para tooltips
        self.setup_styles()
        
        # Definir textos de ayuda
        self.help_texts = self._define_help_texts()
    
    def setup_styles(self):
        """Configurar estilos para tooltips."""
        style = ttk.Style()
        
        # Estilo para tooltip
        style.configure("Tooltip.TFrame", 
                       background="#ffffcc", 
                       relief="solid", 
                       borderwidth=1)
        style.configure("Tooltip.TLabel", 
                       background="#ffffcc", 
                       foreground="black",
                       font=("Arial", 9))
    
    def _define_help_texts(self) -> Dict[str, str]:
        """Definir todos los textos de ayuda."""
        return {
            # Main Interface
            "notebook_tabs": "Pestañas de la aplicación: Editor AFD, Evaluador de Cadenas, Visualizador AFD",
            "status_bar": "Barra de estado que muestra información sobre la operación actual",
            
            # AFD Editor
            "states_entry": "Ingresa los nombres de los estados separados por espacios. Ejemplo: q0 q1 q2",
            "add_states_btn": "Agrega los estados ingresados a la lista de estados del AFD",
            "states_listbox": "Lista de estados del AFD. Selecciona un estado para agregarlo como estado de aceptación",
            "remove_state_btn": "Elimina el estado seleccionado de la lista",
            
            "alphabet_entry": "Ingresa los símbolos del alfabeto separados por espacios. Ejemplo: a b c 0 1",
            "add_alphabet_btn": "Agrega los símbolos ingresados al alfabeto del AFD",
            "alphabet_listbox": "Lista de símbolos del alfabeto",
            "remove_alphabet_btn": "Elimina el símbolo seleccionado del alfabeto",
            
            "initial_combo": "Selecciona el estado inicial del AFD. Debe ser uno de los estados definidos",
            "accepting_listbox": "Lista de estados de aceptación. Los estados aquí listados son estados finales",
            "add_accepting_btn": "Agrega el estado seleccionado como estado de aceptación",
            "remove_accepting_btn": "Elimina el estado de aceptación seleccionado",
            
            "transitions_tree": "Tabla de transiciones del AFD. Muestra todas las transiciones definidas",
            "from_combo": "Selecciona el estado origen de la transición",
            "symbol_combo": "Selecciona el símbolo que activa la transición",
            "to_combo": "Selecciona el estado destino de la transición",
            "add_transition_btn": "Agrega la transición definida a la tabla",
            "remove_transition_btn": "Elimina la transición seleccionada de la tabla",
            
            "validate_btn": "Valida que el AFD esté completo y sea válido",
            "clear_btn": "Limpia todos los datos del formulario",
            "generate_btn": "Genera automáticamente todas las transiciones posibles",
            
            # String Evaluator
            "string_entry": "Ingresa la cadena que quieres evaluar con el AFD actual",
            "evaluate_btn": "Evalúa la cadena ingresada paso a paso",
            "clear_string_btn": "Limpia el campo de entrada de cadena",
            "step_btn": "Ejecuta el siguiente paso de la evaluación",
            "reset_btn": "Reinicia la evaluación desde el principio",
            
            # AFD Visualizer
            "refresh_btn": "Actualiza la visualización del AFD",
            "zoom_in_btn": "Aumenta el zoom de la visualización",
            "zoom_out_btn": "Disminuye el zoom de la visualización",
            "reset_zoom_btn": "Restaura el zoom original",
            "show_labels_check": "Muestra u oculta las etiquetas de los estados",
            "show_initial_check": "Resalta el estado inicial con un borde rojo",
            "compact_mode_check": "Modo compacto para AFDs con muchos estados"
        }
    
    def add_tooltip(self, widget: tk.Widget, help_key: str):
        """
        Agregar tooltip a un widget.
        
        Args:
            widget: Widget al que agregar el tooltip
            help_key: Clave del texto de ayuda
        """
        try:
            if help_key in self.help_texts and widget and hasattr(widget, 'winfo_exists'):
                tooltip = HelpTooltip(widget, self.help_texts[help_key])
                self.tooltips[widget] = tooltip
        except Exception:
            # Fallar silenciosamente si no se puede agregar el tooltip
            pass
    
    def show_help_window(self):
        """Mostrar ventana de ayuda principal."""
        if self.help_window and self.help_window.winfo_exists():
            self.help_window.lift()
            return
        
        self.help_window = tk.Toplevel(self.root)
        self.help_window.title("Ayuda - Simulador AFD")
        self.help_window.geometry("800x600")
        self.help_window.resizable(True, True)
        
        # Crear notebook para diferentes secciones de ayuda
        notebook = ttk.Notebook(self.help_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Pestaña de introducción
        intro_frame = ttk.Frame(notebook)
        notebook.add(intro_frame, text="Introducción")
        self._create_intro_tab(intro_frame)
        
        # Pestaña de editor AFD
        editor_frame = ttk.Frame(notebook)
        notebook.add(editor_frame, text="Editor AFD")
        self._create_editor_help_tab(editor_frame)
        
        # Pestaña de evaluador de cadenas
        evaluator_frame = ttk.Frame(notebook)
        notebook.add(evaluator_frame, text="Evaluador de Cadenas")
        self._create_evaluator_help_tab(evaluator_frame)
        
        # Pestaña de visualizador
        visualizer_frame = ttk.Frame(notebook)
        notebook.add(visualizer_frame, text="Visualizador AFD")
        self._create_visualizer_help_tab(visualizer_frame)
        
        # Pestaña de ejemplos
        examples_frame = ttk.Frame(notebook)
        notebook.add(examples_frame, text="Ejemplos")
        self._create_examples_help_tab(examples_frame)
    
    def _create_intro_tab(self, parent):
        """Crear pestaña de introducción."""
        text_widget = tk.Text(parent, wrap="word", padx=10, pady=10)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        intro_text = """
¡Bienvenido al Simulador de Autómatas Finitos Deterministas (AFD)!

Este programa te permite crear, editar, visualizar y probar autómatas finitos deterministas de manera interactiva.

¿Qué es un AFD?
Un Autómata Finito Determinista es un modelo computacional que consiste en:
• Un conjunto finito de estados
• Un alfabeto finito de símbolos
• Un estado inicial
• Un conjunto de estados de aceptación
• Una función de transición que define cómo cambiar de estado

¿Cómo usar este programa?

1. CREAR UN AFD:
   - Ve a la pestaña "Editor AFD"
   - Define los estados, alfabeto, estado inicial y estados de aceptación
   - Agrega las transiciones necesarias
   - Valida tu AFD

2. PROBAR CADENAS:
   - Ve a la pestaña "Evaluador de Cadenas"
   - Ingresa una cadena para probar
   - Ve el proceso de evaluación paso a paso

3. VISUALIZAR:
   - Ve a la pestaña "Visualizador AFD"
   - Ve una representación gráfica de tu AFD

4. EJEMPLOS:
   - Usa el menú "Examples" para cargar AFDs de ejemplo
   - Aprende de patrones comunes

CONSEJOS:
• Usa nombres descriptivos para los estados (ej: q0, q1, q2)
• Los símbolos pueden ser letras, números o caracteres especiales
• Asegúrate de que cada estado tenga una transición para cada símbolo del alfabeto
• El estado inicial debe estar definido
• Al menos un estado debe ser de aceptación

¡Explora las diferentes pestañas para aprender más sobre cada funcionalidad!
        """
        
        text_widget.insert("1.0", intro_text.strip())
        text_widget.config(state="disabled")
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_editor_help_tab(self, parent):
        """Crear pestaña de ayuda del editor."""
        text_widget = tk.Text(parent, wrap="word", padx=10, pady=10)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        editor_text = """
EDITOR AFD - Guía Completa

ESTADOS (Q):
• Campo de entrada: Escribe los nombres de los estados separados por espacios
• Botón "Add States": Agrega los estados a la lista
• Lista de estados: Muestra todos los estados definidos
• Botón "Remove Selected": Elimina el estado seleccionado

ALFABETO (Σ):
• Campo de entrada: Escribe los símbolos del alfabeto separados por espacios
• Botón "Add Symbols": Agrega los símbolos al alfabeto
• Lista de símbolos: Muestra todos los símbolos del alfabeto
• Botón "Remove Selected": Elimina el símbolo seleccionado

ESTADO INICIAL (q₀):
• ComboBox: Selecciona cuál de los estados definidos será el inicial
• Solo puedes seleccionar estados que ya estén en la lista

ESTADOS DE ACEPTACIÓN (F):
• Lista de estados de aceptación: Muestra los estados finales
• Botón "Add Selected": Agrega el estado seleccionado como de aceptación
• Botón "Remove Selected": Elimina el estado de aceptación seleccionado

TRANSICIONES (δ):
• Tabla de transiciones: Muestra todas las transiciones definidas
• Estado origen: Selecciona el estado desde donde parte la transición
• Símbolo: Selecciona el símbolo que activa la transición
• Estado destino: Selecciona el estado hacia donde va la transición
• Botón "Add Transition": Agrega la transición a la tabla
• Botón "Remove Selected": Elimina la transición seleccionada

BOTONES DE ACCIÓN:
• "Validate AFD": Verifica que el AFD esté completo y sea válido
• "Clear All": Limpia todos los datos del formulario
• "Generate Complete AFD": Genera automáticamente todas las transiciones posibles

REGLAS IMPORTANTES:
• Cada estado debe tener exactamente una transición para cada símbolo del alfabeto
• No pueden existir transiciones duplicadas (mismo estado origen y símbolo)
• El estado inicial debe estar definido
• Debe haber al menos un estado de aceptación
• Los nombres de estados y símbolos no pueden estar vacíos

CONSEJOS:
• Usa nombres descriptivos: q0, q1, q2 o start, middle, end
• Los símbolos pueden ser cualquier carácter: a, b, 0, 1, etc.
• Revisa la sección "AFD Summary" para ver un resumen de tu autómata
• Usa "Generate Complete AFD" para crear un AFD básico y luego edita las transiciones
        """
        
        text_widget.insert("1.0", editor_text.strip())
        text_widget.config(state="disabled")
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_evaluator_help_tab(self, parent):
        """Crear pestaña de ayuda del evaluador."""
        text_widget = tk.Text(parent, wrap="word", padx=10, pady=10)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        evaluator_text = """
EVALUADOR DE CADENAS - Guía Completa

FUNCIONALIDAD:
El evaluador de cadenas te permite probar si una cadena es aceptada por tu AFD.

CÓMO USAR:

1. PREPARAR EL AFD:
   • Asegúrate de que tienes un AFD válido cargado
   • El AFD debe estar completo (todas las transiciones definidas)

2. INGRESAR CADENA:
   • En el campo "String to Evaluate" escribe la cadena a probar
   • La cadena puede contener cualquier símbolo del alfabeto del AFD
   • Ejemplo: si tu alfabeto es {a, b}, puedes probar "ab", "aab", "bbaa", etc.

3. EVALUAR:
   • Haz clic en "Evaluate String" para evaluar la cadena completa
   • O usa "Step" para evaluar paso a paso
   • Usa "Reset" para reiniciar la evaluación

4. INTERPRETAR RESULTADOS:
   • "ACCEPTED": La cadena es aceptada por el AFD
   • "REJECTED": La cadena es rechazada por el AFD
   • "INVALID SYMBOL": La cadena contiene símbolos no válidos

EVALUACIÓN PASO A PASO:
• Estado actual: Muestra el estado en el que se encuentra el AFD
• Símbolo leído: Muestra el símbolo que se está procesando
• Próxima transición: Muestra hacia dónde va el AFD
• Historial: Muestra todos los pasos realizados

CONSEJOS:
• Usa cadenas cortas al principio para entender el comportamiento
• Prueba cadenas que sabes que deberían ser aceptadas
• Prueba cadenas que sabes que deberían ser rechazadas
• Observa el patrón de transiciones para entender el lenguaje

EJEMPLOS DE CADENAS:
• Para un AFD que acepta cadenas con número par de 'a':
  - Aceptadas: "", "aa", "aaaa", "baab"
  - Rechazadas: "a", "aaa", "aab"
• Para un AFD que acepta cadenas que terminan en "01":
  - Aceptadas: "01", "001", "101", "0001"
  - Rechazadas: "0", "1", "10", "00"
        """
        
        text_widget.insert("1.0", evaluator_text.strip())
        text_widget.config(state="disabled")
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_visualizer_help_tab(self, parent):
        """Crear pestaña de ayuda del visualizador."""
        text_widget = tk.Text(parent, wrap="word", padx=10, pady=10)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        visualizer_text = """
VISUALIZADOR AFD - Guía Completa

FUNCIONALIDAD:
El visualizador te permite ver una representación gráfica de tu AFD.

ELEMENTOS VISUALES:

ESTADOS:
• Círculo negro: Estado regular
• Círculo azul doble: Estado de aceptación
• Borde rojo: Estado inicial (si está habilitado)

TRANSICIONES:
• Flechas: Muestran las transiciones entre estados
• Etiquetas: Símbolos que activan cada transición
• Bucles: Transiciones que van del estado a sí mismo

CONTROLES:

BOTONES DE CONTROL:
• "Refresh Visualization": Actualiza la visualización
• "Zoom In": Aumenta el tamaño de la visualización
• "Zoom Out": Disminuye el tamaño de la visualización
• "Reset Zoom": Restaura el tamaño original

CONFIGURACIONES:
• "Show State Labels": Muestra u oculta las etiquetas de los estados
• "Highlight Initial State": Resalta el estado inicial con borde rojo
• "Compact Mode": Modo compacto para AFDs con muchos estados

INFORMACIÓN DEL AFD:
La panel de información muestra:
• Número y nombres de estados
• Número y símbolos del alfabeto
• Estado inicial
• Estados de aceptación
• Número de transiciones
• Si el AFD es válido

LEYENDA:
• Círculo negro: Estado regular
• Círculo azul doble: Estado de aceptación
• Borde rojo: Estado inicial
• Flechas: Transiciones con símbolos

CONSEJOS:
• Usa el zoom para ver detalles en AFDs grandes
• El modo compacto es útil para AFDs con muchos estados
• La visualización se actualiza automáticamente cuando cambias el AFD
• Puedes hacer scroll en la visualización si es más grande que la ventana

NAVEGACIÓN:
• Usa las barras de scroll para navegar por AFDs grandes
• El zoom te permite ver detalles específicos
• El botón de actualizar es útil si la visualización no se actualiza automáticamente
        """
        
        text_widget.insert("1.0", visualizer_text.strip())
        text_widget.config(state="disabled")
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_examples_help_tab(self, parent):
        """Crear pestaña de ayuda de ejemplos."""
        text_widget = tk.Text(parent, wrap="word", padx=10, pady=10)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        examples_text = """
EJEMPLOS - Guía Completa

FACTORY EXAMPLES (Ejemplos de Fábrica):
Estos son ejemplos predefinidos que puedes cargar directamente.

EJEMPLOS DISPONIBLES:

1. BINARY_AFD:
   • Acepta cadenas binarias (solo 0s y 1s)
   • Estados: q0, q1
   • Alfabeto: {0, 1}
   • Estado inicial: q0
   • Estados de aceptación: {q1}

2. ENDS_WITH_01:
   • Acepta cadenas que terminan en "01"
   • Estados: q0, q1, q2
   • Alfabeto: {0, 1}
   • Estado inicial: q0
   • Estados de aceptación: {q2}

3. EVEN_LENGTH:
   • Acepta cadenas de longitud par
   • Estados: q0, q1
   • Alfabeto: {a, b}
   • Estado inicial: q0
   • Estados de aceptación: {q0}

4. EXACTLY_TWO_AS:
   • Acepta cadenas con exactamente dos 'a's
   • Estados: q0, q1, q2, q3
   • Alfabeto: {a, b}
   • Estado inicial: q0
   • Estados de aceptación: {q2}

FILE EXAMPLES (Ejemplos de Archivo):
Estos son ejemplos guardados en archivos JSON que puedes cargar.

CÓMO CARGAR EJEMPLOS:
1. Ve al menú "Examples"
2. Selecciona el ejemplo que quieres cargar
3. El AFD se cargará automáticamente en el editor

CÓMO USAR LOS EJEMPLOS:
1. Carga un ejemplo
2. Ve a la pestaña "Editor AFD" para ver su estructura
3. Ve a "Evaluador de Cadenas" para probar cadenas
4. Ve a "Visualizador AFD" para ver la representación gráfica

EXPERIMENTA CON LOS EJEMPLOS:
• Prueba diferentes cadenas en el evaluador
• Modifica el AFD en el editor
• Observa cómo cambia la visualización
• Crea tus propios AFDs basados en los ejemplos

CONSEJOS:
• Los ejemplos son una excelente forma de aprender
• Estudia la estructura de cada ejemplo
• Prueba modificar los ejemplos para entender mejor cómo funcionan
• Usa los ejemplos como base para crear tus propios AFDs

CREAR TUS PROPIOS EJEMPLOS:
1. Crea un AFD en el editor
2. Guárdalo usando "File > Save AFD"
3. El archivo se guardará como JSON
4. Puedes cargarlo después usando "File > Load AFD"
        """
        
        text_widget.insert("1.0", examples_text.strip())
        text_widget.config(state="disabled")
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_contextual_help(self, context: str):
        """
        Mostrar ayuda contextual específica.
        
        Args:
            context: Contexto de la ayuda a mostrar
        """
        help_messages = {
            "no_afd_loaded": "No hay AFD cargado. Ve a 'File > New AFD' o carga un ejemplo.",
            "invalid_afd": "El AFD actual no es válido. Revisa que todas las transiciones estén definidas.",
            "empty_string": "La cadena está vacía. Ingresa una cadena para evaluar.",
            "invalid_symbol": "La cadena contiene símbolos no válidos para este AFD.",
            "afd_complete": "¡AFD válido y completo! Puedes proceder a evaluar cadenas.",
            "missing_transitions": "Faltan transiciones. Cada estado debe tener una transición para cada símbolo del alfabeto."
        }
        
        if context in help_messages:
            messagebox.showinfo("Ayuda Contextual", help_messages[context])
    
    def cleanup(self):
        """Limpiar recursos del sistema de ayuda."""
        for tooltip in self.tooltips.values():
            if tooltip.tooltip_window:
                tooltip.hide_tooltip()
        
        if self.help_window and self.help_window.winfo_exists():
            self.help_window.destroy()
