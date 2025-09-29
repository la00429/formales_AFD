"""
Demostración de las mejoras implementadas en la GUI del simulador AFD.

Este módulo muestra las nuevas funcionalidades y mejoras visuales
implementadas en la interfaz gráfica.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict


class ImprovementsDemo:
    """Demostración de las mejoras de la GUI."""
    
    def __init__(self, parent):
        """
        Inicializar demostración.
        
        Args:
            parent: Widget padre
        """
        self.parent = parent
        self.create_demo_window()
    
    def create_demo_window(self):
        """Crear ventana de demostración."""
        self.demo_window = tk.Toplevel(self.parent)
        self.demo_window.title("Demostración de Mejoras - Simulador AFD v2.0")
        self.demo_window.geometry("800x600")
        self.demo_window.resizable(True, True)
        
        # Hacer la ventana modal
        self.demo_window.transient(self.parent)
        self.demo_window.grab_set()
        
        # Frame principal con scroll
        main_frame = ttk.Frame(self.demo_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(
            main_frame,
            text="🚀 Mejoras Implementadas en AFD Simulator v2.0",
            font=("Segoe UI", 18, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Crear notebook para diferentes secciones
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True)
        
        # Pestaña de mejoras visuales
        visual_frame = ttk.Frame(notebook)
        notebook.add(visual_frame, text="🎨 Mejoras Visuales")
        self.create_visual_improvements_tab(visual_frame)
        
        # Pestaña de sistema de ayuda
        help_frame = ttk.Frame(notebook)
        notebook.add(help_frame, text="❓ Sistema de Ayuda")
        self.create_help_system_tab(help_frame)
        
        # Pestaña de validación
        validation_frame = ttk.Frame(notebook)
        notebook.add(validation_frame, text="✅ Validación Mejorada")
        self.create_validation_tab(validation_frame)
        
        # Pestaña de tutorial
        tutorial_frame = ttk.Frame(notebook)
        notebook.add(tutorial_frame, text="📚 Tutorial Interactivo")
        self.create_tutorial_tab(tutorial_frame)
        
        # Botón cerrar
        close_button = ttk.Button(
            main_frame,
            text="Cerrar Demostración",
            command=self.demo_window.destroy
        )
        close_button.pack(pady=(20, 0))
    
    def create_visual_improvements_tab(self, parent):
        """Crear pestaña de mejoras visuales."""
        # Frame con scroll
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido
        content = """
🎨 MEJORAS VISUALES IMPLEMENTADAS

1. SISTEMA DE ESTILOS MODERNO:
   ✅ Paleta de colores profesional y consistente
   ✅ Fuentes modernas (Segoe UI)
   ✅ Estilos personalizados para todos los widgets
   ✅ Colores temáticos para diferentes estados

2. INTERFAZ MEJORADA:
   ✅ Diseño más limpio y organizado
   ✅ Mejor espaciado y padding
   ✅ Colores de estado para validación
   ✅ Botones con estilos diferenciados

3. ELEMENTOS VISUALES:
   ✅ Tooltips informativos en todos los elementos
   ✅ Resaltado visual para estados de validación
   ✅ Colores específicos para AFD (estados, transiciones, símbolos)
   ✅ Mejor contraste y legibilidad

4. RESPONSIVIDAD:
   ✅ Interfaz adaptable a diferentes tamaños
   ✅ Scrollbars automáticos cuando es necesario
   ✅ Layout flexible y organizado

COLORES IMPLEMENTADOS:
• Azul principal (#2E86AB) - Elementos principales
• Rosa/Magenta (#A23B72) - Elementos secundarios
• Naranja (#F18F01) - Acentos y tooltips
• Verde (#4CAF50) - Estados de éxito
• Rojo (#F44336) - Estados de error
• Azul información (#2196F3) - Información
        """
        
        text_widget = tk.Text(scrollable_frame, wrap="word", padx=20, pady=20)
        text_widget.insert("1.0", content.strip())
        text_widget.config(state="disabled", font=("Consolas", 10))
        text_widget.pack(fill="both", expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_help_system_tab(self, parent):
        """Crear pestaña de sistema de ayuda."""
        # Frame con scroll
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido
        content = """
❓ SISTEMA DE AYUDA IMPLEMENTADO

1. TOOLTIPS CONTEXTUALES:
   ✅ Ayuda instantánea al pasar el mouse
   ✅ Explicaciones detalladas para cada elemento
   ✅ Guías paso a paso integradas
   ✅ Información contextual relevante

2. VENTANA DE AYUDA PRINCIPAL:
   ✅ Pestañas organizadas por funcionalidad
   ✅ Guías completas para cada sección
   ✅ Ejemplos prácticos y consejos
   ✅ Navegación fácil y intuitiva

3. AYUDA CONTEXTUAL:
   ✅ Mensajes de ayuda específicos por situación
   ✅ Sugerencias automáticas en caso de error
   ✅ Guías de resolución de problemas
   ✅ Tips y trucos integrados

4. DOCUMENTACIÓN INTEGRADA:
   ✅ Introducción completa al AFD
   ✅ Guía del Editor AFD
   ✅ Guía del Evaluador de Cadenas
   ✅ Guía del Visualizador AFD
   ✅ Ejemplos y patrones comunes

FUNCIONALIDADES DE AYUDA:
• Tooltips en todos los widgets
• Ventana de ayuda con pestañas
• Ayuda contextual por situación
• Atajos de teclado documentados
• Ejemplos interactivos
• Guías paso a paso
        """
        
        text_widget = tk.Text(scrollable_frame, wrap="word", padx=20, pady=20)
        text_widget.insert("1.0", content.strip())
        text_widget.config(state="disabled", font=("Consolas", 10))
        text_widget.pack(fill="both", expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_validation_tab(self, parent):
        """Crear pestaña de validación."""
        # Frame con scroll
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido
        content = """
✅ SISTEMA DE VALIDACIÓN MEJORADO

1. VALIDACIÓN EN TIEMPO REAL:
   ✅ Feedback inmediato al escribir
   ✅ Validación automática de campos
   ✅ Indicadores visuales de estado
   ✅ Mensajes de error específicos

2. INDICADORES VISUALES:
   ✅ Campos con borde verde para válidos
   ✅ Campos con borde rojo para errores
   ✅ Campos con borde naranja para advertencias
   ✅ Mensajes de feedback contextuales

3. VALIDACIÓN INTELIGENTE:
   ✅ Validación de nombres de estados
   ✅ Validación de símbolos del alfabeto
   ✅ Validación de transiciones
   ✅ Validación completa del AFD

4. MENSAJES DE ERROR MEJORADOS:
   ✅ Descripciones claras y específicas
   ✅ Sugerencias de corrección
   ✅ Ayuda contextual para resolver errores
   ✅ Resumen de validación completo

TIPOS DE VALIDACIÓN:
• Estados: Nombres únicos, no vacíos, formato válido
• Alfabeto: Símbolos únicos, caracteres individuales
• Estado inicial: Debe existir en la lista de estados
• Estados de aceptación: Al menos uno, deben existir
• Transiciones: Sin duplicados, estados válidos
• AFD completo: Todas las transiciones necesarias

NIVELES DE VALIDACIÓN:
• ✅ ÉXITO: Campo válido y completo
• ⚠️ ADVERTENCIA: Campo con problemas menores
• ❌ ERROR: Campo con errores que impiden funcionamiento
• ℹ️ INFORMACIÓN: Sugerencias y tips
        """
        
        text_widget = tk.Text(scrollable_frame, wrap="word", padx=20, pady=20)
        text_widget.insert("1.0", content.strip())
        text_widget.config(state="disabled", font=("Consolas", 10))
        text_widget.pack(fill="both", expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_tutorial_tab(self, parent):
        """Crear pestaña de tutorial."""
        # Frame con scroll
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido
        content = """
📚 TUTORIAL INTERACTIVO IMPLEMENTADO

1. TUTORIAL PASO A PASO:
   ✅ Guía interactiva completa
   ✅ 14 pasos detallados
   ✅ Navegación fácil (anterior/siguiente)
   ✅ Barra de progreso visual

2. RESALTADO VISUAL:
   ✅ Resaltado de elementos importantes
   ✅ Overlay visual para widgets objetivo
   ✅ Enfoque automático en campos relevantes
   ✅ Acciones automáticas guiadas

3. CONTENIDO EDUCATIVO:
   ✅ Explicaciones claras y detalladas
   ✅ Ejemplos prácticos
   ✅ Consejos y mejores prácticas
   ✅ Guía completa del flujo de trabajo

4. FUNCIONALIDADES AVANZADAS:
   ✅ Tutorial modal (no interfiere con la app)
   ✅ Posibilidad de saltar pasos
   ✅ Reinicio del tutorial
   ✅ Finalización con confirmación

PASOS DEL TUTORIAL:
1. Introducción y bienvenida
2. Definir estados del AFD
3. Agregar estados a la lista
4. Definir alfabeto
5. Agregar símbolos al alfabeto
6. Seleccionar estado inicial
7. Definir estados de aceptación
8. Agregar estados de aceptación
9. Definir transiciones
10. Agregar transiciones
11. Validar AFD completo
12. Probar cadenas (cambiar pestaña)
13. Visualizar AFD (cambiar pestaña)
14. Finalización y consejos

CARACTERÍSTICAS:
• Interfaz intuitiva y fácil de usar
• Progreso visual claro
• Navegación flexible
• Contenido educativo completo
• Integración perfecta con la aplicación
        """
        
        text_widget = tk.Text(scrollable_frame, wrap="word", padx=20, pady=20)
        text_widget.insert("1.0", content.strip())
        text_widget.config(state="disabled", font=("Consolas", 10))
        text_widget.pack(fill="both", expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


def show_improvements_demo(parent):
    """Mostrar demostración de mejoras."""
    demo = ImprovementsDemo(parent)
    return demo.demo_window

