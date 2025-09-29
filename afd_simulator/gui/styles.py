"""
Sistema de estilos mejorado para la GUI del simulador AFD.

Este módulo proporciona estilos modernos y atractivos para todos
los componentes de la interfaz gráfica.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any


class StyleManager:
    """Gestor de estilos para la aplicación."""
    
    def __init__(self, root: tk.Tk):
        """
        Inicializar el gestor de estilos.
        
        Args:
            root: Ventana principal de la aplicación
        """
        self.root = root
        self.style = ttk.Style()
        self.setup_theme()
        self.setup_colors()
        self.setup_fonts()
        self.configure_styles()
    
    def setup_theme(self):
        """Configurar el tema base."""
        # Usar tema moderno si está disponible
        available_themes = self.style.theme_names()
        if 'clam' in available_themes:
            self.style.theme_use('clam')
        elif 'alt' in available_themes:
            self.style.theme_use('alt')
        else:
            self.style.theme_use('default')
    
    def setup_colors(self):
        """Definir paleta de colores."""
        self.colors = {
            # Colores principales
            'primary': '#2E86AB',      # Azul principal
            'secondary': '#A23B72',    # Rosa/Magenta
            'accent': '#F18F01',       # Naranja
            'success': '#4CAF50',      # Verde
            'warning': '#FF9800',      # Naranja de advertencia
            'error': '#F44336',        # Rojo
            'info': '#2196F3',         # Azul información
            
            # Colores de fondo
            'bg_primary': '#FFFFFF',   # Blanco
            'bg_secondary': '#F5F5F5', # Gris muy claro
            'bg_tertiary': '#EEEEEE',  # Gris claro
            'bg_dark': '#424242',      # Gris oscuro
            
            # Colores de texto
            'text_primary': '#212121', # Negro suave
            'text_secondary': '#757575', # Gris medio
            'text_light': '#FFFFFF',   # Blanco
            'text_disabled': '#BDBDBD', # Gris claro
            
            # Colores de borde
            'border_light': '#E0E0E0', # Gris muy claro
            'border_medium': '#BDBDBD', # Gris medio
            'border_dark': '#757575',  # Gris oscuro
            
            # Colores específicos para AFD
            'state_normal': '#FFFFFF',     # Estado normal
            'state_accepting': '#E3F2FD',  # Estado de aceptación
            'state_initial': '#FFF3E0',    # Estado inicial
            'transition': '#2196F3',       # Transiciones
            'symbol': '#4CAF50',          # Símbolos
        }
    
    def setup_fonts(self):
        """Configurar fuentes."""
        # Constantes de fuentes
        FONT_FAMILY = 'Segoe UI'
        MONOSPACE_FAMILY = 'Consolas'
        
        self.fonts = {
            'title': (FONT_FAMILY, 16, 'bold'),
            'heading': (FONT_FAMILY, 12, 'bold'),
            'body': (FONT_FAMILY, 10),
            'small': (FONT_FAMILY, 9),
            'monospace': (MONOSPACE_FAMILY, 10),
            'button': (FONT_FAMILY, 10, 'bold'),
        }
    
    def configure_styles(self):
        """Configurar todos los estilos de la aplicación."""
        self.configure_frames()
        self.configure_labels()
        self.configure_buttons()
        self.configure_entries()
        self.configure_comboboxes()
        self.configure_listboxes()
        self.configure_trees()
        self.configure_text_widgets()
        self.configure_notebook()
        self.configure_tooltips()
        self.configure_special_widgets()
    
    def configure_frames(self):
        """Configurar estilos de frames."""
        # Frame principal
        self.style.configure('Main.TFrame',
                           background=self.colors['bg_primary'])
        
        # Frame de sección
        self.style.configure('Section.TFrame',
                           background=self.colors['bg_secondary'],
                           relief='solid',
                           borderwidth=1)
        
        # Frame de control
        self.style.configure('Control.TFrame',
                           background=self.colors['bg_tertiary'])
        
        # LabelFrame
        self.style.configure('Section.TLabelframe',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           font=self.fonts['heading'],
                           relief='solid',
                           borderwidth=1)
        
        self.style.configure('Section.TLabelframe.Label',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['primary'],
                           font=self.fonts['heading'])
    
    def configure_labels(self):
        """Configurar estilos de labels."""
        # Label principal
        self.style.configure('Title.TLabel',
                           background=self.colors['bg_primary'],
                           foreground=self.colors['text_primary'],
                           font=self.fonts['title'])
        
        # Label de encabezado
        self.style.configure('Heading.TLabel',
                           background=self.colors['bg_primary'],
                           foreground=self.colors['primary'],
                           font=self.fonts['heading'])
        
        # Label de cuerpo
        self.style.configure('Body.TLabel',
                           background=self.colors['bg_primary'],
                           foreground=self.colors['text_primary'],
                           font=self.fonts['body'])
        
        # Label de estado
        self.style.configure('Status.TLabel',
                           background=self.colors['bg_tertiary'],
                           foreground=self.colors['text_secondary'],
                           font=self.fonts['small'],
                           relief='sunken')
        
        # Label de información
        self.style.configure('Info.TLabel',
                           background=self.colors['info'],
                           foreground=self.colors['text_light'],
                           font=self.fonts['body'],
                           padding=5)
        
        # Label de éxito
        self.style.configure('Success.TLabel',
                           background=self.colors['success'],
                           foreground=self.colors['text_light'],
                           font=self.fonts['body'],
                           padding=5)
        
        # Label de advertencia
        self.style.configure('Warning.TLabel',
                           background=self.colors['warning'],
                           foreground=self.colors['text_light'],
                           font=self.fonts['body'],
                           padding=5)
        
        # Label de error
        self.style.configure('Error.TLabel',
                           background=self.colors['error'],
                           foreground=self.colors['text_light'],
                           font=self.fonts['body'],
                           padding=5)
    
    def configure_buttons(self):
        """Configurar estilos de botones."""
        # Botón primario
        self.style.configure('Primary.TButton',
                           background=self.colors['primary'],
                           foreground=self.colors['text_light'],
                           font=self.fonts['button'],
                           padding=(10, 5),
                           relief='raised',
                           borderwidth=2)
        
        self.style.map('Primary.TButton',
                      background=[('active', self.colors['secondary']),
                                ('pressed', self.colors['accent'])])
        
        # Botón secundario
        self.style.configure('Secondary.TButton',
                           background=self.colors['bg_tertiary'],
                           foreground=self.colors['text_primary'],
                           font=self.fonts['button'],
                           padding=(8, 4),
                           relief='raised',
                           borderwidth=1)
        
        # Constante para estilo de botón secundario
        SECONDARY_BUTTON_STYLE = 'Secondary.TButton'
        
        self.style.map(SECONDARY_BUTTON_STYLE,
                      background=[('active', self.colors['border_medium']),
                                ('pressed', self.colors['border_dark'])])
        
        # Botón de éxito
        self.style.configure('Success.TButton',
                           background=self.colors['success'],
                           foreground=self.colors['text_light'],
                           font=self.fonts['button'],
                           padding=(8, 4))
        
        # Botón de advertencia
        self.style.configure('Warning.TButton',
                           background=self.colors['warning'],
                           foreground=self.colors['text_light'],
                           font=self.fonts['button'],
                           padding=(8, 4))
        
        # Botón de error
        self.style.configure('Error.TButton',
                           background=self.colors['error'],
                           foreground=self.colors['text_light'],
                           font=self.fonts['button'],
                           padding=(8, 4))
        
        # Botón pequeño
        self.style.configure('Small.TButton',
                           background=self.colors['bg_tertiary'],
                           foreground=self.colors['text_primary'],
                           font=self.fonts['small'],
                           padding=(4, 2))
    
    def configure_entries(self):
        """Configurar estilos de campos de entrada."""
        self.style.configure('Modern.TEntry',
                           fieldbackground=self.colors['bg_primary'],
                           foreground=self.colors['text_primary'],
                           font=self.fonts['body'],
                           relief='solid',
                           borderwidth=1,
                           padding=5)
        
        # Constante para estilo de entrada
        MODERN_ENTRY_STYLE = 'Modern.TEntry'
        
        self.style.map(MODERN_ENTRY_STYLE,
                      focuscolor=[('!focus', self.colors['border_light']),
                                ('focus', self.colors['primary'])])
    
    def configure_comboboxes(self):
        """Configurar estilos de comboboxes."""
        self.style.configure('Modern.TCombobox',
                           fieldbackground=self.colors['bg_primary'],
                           foreground=self.colors['text_primary'],
                           font=self.fonts['body'],
                           relief='solid',
                           borderwidth=1,
                           padding=5)
        
        # Constante para estilo de combobox
        MODERN_COMBOBOX_STYLE = 'Modern.TCombobox'
        
        self.style.map(MODERN_COMBOBOX_STYLE,
                      focuscolor=[('!focus', self.colors['border_light']),
                                ('focus', self.colors['primary'])])
    
    def configure_listboxes(self):
        """Configurar estilos de listboxes."""
        # Configurar colores del listbox
        self.root.option_add('*Listbox*background', self.colors['bg_primary'])
        self.root.option_add('*Listbox*foreground', self.colors['text_primary'])
        self.root.option_add('*Listbox*selectBackground', self.colors['primary'])
        self.root.option_add('*Listbox*selectForeground', self.colors['text_light'])
        self.root.option_add('*Listbox*font', self.fonts['body'])
    
    def configure_trees(self):
        """Configurar estilos de TreeView."""
        self.style.configure('Modern.Treeview',
                           background=self.colors['bg_primary'],
                           foreground=self.colors['text_primary'],
                           font=self.fonts['body'],
                           relief='solid',
                           borderwidth=1)
        
        self.style.configure('Modern.Treeview.Heading',
                           background=self.colors['bg_tertiary'],
                           foreground=self.colors['text_primary'],
                           font=self.fonts['heading'],
                           relief='solid',
                           borderwidth=1)
        
        self.style.map('Modern.Treeview',
                      background=[('selected', self.colors['primary'])],
                      foreground=[('selected', self.colors['text_light'])])
    
    def configure_text_widgets(self):
        """Configurar estilos de widgets de texto."""
        # Configurar colores del Text widget
        self.root.option_add('*Text*background', self.colors['bg_primary'])
        self.root.option_add('*Text*foreground', self.colors['text_primary'])
        self.root.option_add('*Text*selectBackground', self.colors['primary'])
        self.root.option_add('*Text*selectForeground', self.colors['text_light'])
        self.root.option_add('*Text*font', self.fonts['monospace'])
    
    def configure_notebook(self):
        """Configurar estilos del notebook."""
        self.style.configure('Modern.TNotebook',
                           background=self.colors['bg_secondary'],
                           borderwidth=0)
        
        self.style.configure('Modern.TNotebook.Tab',
                           background=self.colors['bg_tertiary'],
                           foreground=self.colors['text_primary'],
                           font=self.fonts['body'],
                           padding=(12, 8))
        
        self.style.map('Modern.TNotebook.Tab',
                      background=[('selected', self.colors['bg_primary']),
                                ('active', self.colors['border_light'])])
    
    def configure_tooltips(self):
        """Configurar estilos de tooltips."""
        self.style.configure('Tooltip.TFrame',
                           background=self.colors['accent'],
                           relief='solid',
                           borderwidth=1)
        
        self.style.configure('Tooltip.TLabel',
                           background=self.colors['accent'],
                           foreground=self.colors['text_light'],
                           font=self.fonts['small'])
    
    def configure_special_widgets(self):
        """Configurar estilos de widgets especiales."""
        # Canvas para visualización
        self.root.option_add('*Canvas*background', self.colors['bg_primary'])
        
        # Scrollbar
        self.style.configure('Modern.Vertical.TScrollbar',
                           background=self.colors['bg_tertiary'],
                           troughcolor=self.colors['bg_secondary'],
                           borderwidth=0,
                           arrowcolor=self.colors['text_secondary'],
                           darkcolor=self.colors['bg_tertiary'],
                           lightcolor=self.colors['bg_tertiary'])
        
        self.style.configure('Modern.Horizontal.TScrollbar',
                           background=self.colors['bg_tertiary'],
                           troughcolor=self.colors['bg_secondary'],
                           borderwidth=0,
                           arrowcolor=self.colors['text_secondary'],
                           darkcolor=self.colors['bg_tertiary'],
                           lightcolor=self.colors['bg_tertiary'])
    
    def get_color(self, color_name: str) -> str:
        """
        Obtener un color por nombre.
        
        Args:
            color_name: Nombre del color
            
        Returns:
            Código hexadecimal del color
        """
        return self.colors.get(color_name, '#000000')
    
    def get_font(self, font_name: str) -> tuple:
        """
        Obtener una fuente por nombre.
        
        Args:
            font_name: Nombre de la fuente
            
        Returns:
            Tupla de configuración de fuente
        """
        return self.fonts.get(font_name, self.fonts['body'])
    
    def create_gradient_frame(self, parent, **kwargs):
        """
        Crear un frame con gradiente (simulado con colores).
        
        Args:
            parent: Widget padre
            **kwargs: Argumentos adicionales para el frame
            
        Returns:
            Frame con estilo de gradiente
        """
        frame = ttk.Frame(parent, style='Gradient.TFrame', **kwargs)
        # Nota: Tkinter no soporta gradientes nativos, esto es una aproximación
        return frame
    
    def apply_modern_theme(self):
        """Aplicar tema moderno completo."""
        # Configurar colores del sistema
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Aplicar estilos a widgets existentes
        for widget in self.root.winfo_children():
            self._apply_modern_style_recursive(widget)
    
    def _apply_modern_style_recursive(self, widget):
        """Aplicar estilos modernos recursivamente a un widget y sus hijos."""
        try:
            if isinstance(widget, ttk.Frame):
                widget.configure(style='Main.TFrame')
            elif isinstance(widget, ttk.Label):
                widget.configure(style='Body.TLabel')
            elif isinstance(widget, ttk.Button):
                widget.configure(style='Secondary.TButton')
            elif isinstance(widget, ttk.Entry):
                widget.configure(style='Modern.TEntry')
            elif isinstance(widget, ttk.Combobox):
                widget.configure(style='Modern.TCombobox')
            elif isinstance(widget, ttk.Treeview):
                widget.configure(style='Modern.TTreeview')
        except tk.TclError:
            # Ignorar errores de configuración de estilo
            pass
        
        # Aplicar recursivamente a los hijos
        try:
            for child in widget.winfo_children():
                self._apply_modern_style_recursive(child)
        except tk.TclError:
            pass
