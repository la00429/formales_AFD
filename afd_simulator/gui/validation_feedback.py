"""
Sistema de validación visual mejorado para la GUI del simulador AFD.

Este módulo proporciona feedback visual en tiempo real para la validación
de AFDs y entrada del usuario.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Optional, Callable, Any
from enum import Enum


class ValidationLevel(Enum):
    """Niveles de validación."""
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    INFO = "info"


class ValidationMessage:
    """Mensaje de validación con nivel y texto."""
    
    def __init__(self, text: str, level: ValidationLevel, field: str = None):
        """
        Inicializar mensaje de validación.
        
        Args:
            text: Texto del mensaje
            level: Nivel de validación
            field: Campo relacionado (opcional)
        """
        self.text = text
        self.level = level
        self.field = field


class ValidationFeedback:
    """Sistema de feedback visual para validación."""
    
    def __init__(self, parent, style_manager):
        """
        Inicializar sistema de feedback.
        
        Args:
            parent: Widget padre
            style_manager: Gestor de estilos
        """
        self.parent = parent
        self.style_manager = style_manager
        self.validation_messages: List[ValidationMessage] = []
        self.field_validators: Dict[str, Callable] = {}
        self.field_widgets: Dict[str, tk.Widget] = {}
        self.feedback_widgets: Dict[str, tk.Widget] = {}
        
        self.setup_validation_styles()
    
    def setup_validation_styles(self):
        """Configurar estilos para validación."""
        style = ttk.Style()
        
        # Estilos para mensajes de validación
        style.configure('ValidationSuccess.TLabel',
                       background=self.style_manager.get_color('success'),
                       foreground=self.style_manager.get_color('text_light'),
                       font=self.style_manager.get_font('small'),
                       padding=5)
        
        style.configure('ValidationWarning.TLabel',
                       background=self.style_manager.get_color('warning'),
                       foreground=self.style_manager.get_color('text_light'),
                       font=self.style_manager.get_font('small'),
                       padding=5)
        
        style.configure('ValidationError.TLabel',
                       background=self.style_manager.get_color('error'),
                       foreground=self.style_manager.get_color('text_light'),
                       font=self.style_manager.get_font('small'),
                       padding=5)
        
        style.configure('ValidationInfo.TLabel',
                       background=self.style_manager.get_color('info'),
                       foreground=self.style_manager.get_color('text_light'),
                       font=self.style_manager.get_font('small'),
                       padding=5)
        
        # Estilos para campos con validación
        style.configure('FieldSuccess.TEntry',
                       fieldbackground=self.style_manager.get_color('state_accepting'),
                       foreground=self.style_manager.get_color('text_primary'),
                       font=self.style_manager.get_font('body'),
                       relief='solid',
                       borderwidth=2)
        
        style.configure('FieldWarning.TEntry',
                       fieldbackground=self.style_manager.get_color('state_initial'),
                       foreground=self.style_manager.get_color('text_primary'),
                       font=self.style_manager.get_font('body'),
                       relief='solid',
                       borderwidth=2)
        
        style.configure('FieldError.TEntry',
                       fieldbackground='#FFEBEE',
                       foreground=self.style_manager.get_color('error'),
                       font=self.style_manager.get_font('body'),
                       relief='solid',
                       borderwidth=2)
    
    def register_field(self, field_name: str, widget: tk.Widget, validator: Callable = None):
        """
        Registrar un campo para validación.
        
        Args:
            field_name: Nombre del campo
            widget: Widget del campo
            validator: Función validadora (opcional)
        """
        self.field_widgets[field_name] = widget
        if validator:
            self.field_validators[field_name] = validator
        
        # Bind eventos de validación
        if isinstance(widget, (ttk.Entry, ttk.Combobox)):
            widget.bind('<KeyRelease>', lambda e: self.validate_field(field_name))
            widget.bind('<FocusOut>', lambda e: self.validate_field(field_name))
        elif isinstance(widget, tk.Listbox):
            widget.bind('<<ListboxSelect>>', lambda e: self.validate_field(field_name))
    
    def validate_field(self, field_name: str) -> bool:
        """
        Validar un campo específico.
        
        Args:
            field_name: Nombre del campo a validar
            
        Returns:
            True si el campo es válido, False en caso contrario
        """
        try:
            if field_name not in self.field_widgets:
                return True
            
            widget = self.field_widgets[field_name]
            if not widget or not hasattr(widget, 'winfo_exists') or not widget.winfo_exists():
                return True
                
            value = self.get_widget_value(widget)
            
            # Limpiar mensajes anteriores del campo
            self.clear_field_messages(field_name)
            
            # Validar usando el validador registrado
            if field_name in self.field_validators:
                validator = self.field_validators[field_name]
                try:
                    is_valid, message = validator(value)
                    if not is_valid:
                        self.add_field_message(field_name, message, ValidationLevel.ERROR)
                        self.set_field_style(field_name, 'error')
                        return False
                    else:
                        self.set_field_style(field_name, 'success')
                except Exception as e:
                    # Solo mostrar error si es crítico
                    if "critical" in str(e).lower():
                        self.add_field_message(field_name, f"Error de validación: {str(e)}", ValidationLevel.ERROR)
                        self.set_field_style(field_name, 'error')
                        return False
            
            return True
        except Exception:
            # Fallar silenciosamente para no interrumpir la interfaz
            return True
    
    def get_widget_value(self, widget: tk.Widget) -> Any:
        """
        Obtener valor de un widget.
        
        Args:
            widget: Widget del cual obtener el valor
            
        Returns:
            Valor del widget
        """
        if isinstance(widget, ttk.Entry):
            return widget.get()
        elif isinstance(widget, ttk.Combobox):
            return widget.get()
        elif isinstance(widget, tk.Listbox):
            return [widget.get(i) for i in range(widget.size())]
        elif isinstance(widget, ttk.Treeview):
            return [widget.item(item, 'values') for item in widget.get_children()]
        else:
            return None
    
    def add_field_message(self, field_name: str, message: str, level: ValidationLevel):
        """
        Agregar mensaje de validación para un campo.
        
        Args:
            field_name: Nombre del campo
            message: Mensaje de validación
            level: Nivel de validación
        """
        validation_msg = ValidationMessage(message, level, field_name)
        self.validation_messages.append(validation_msg)
        
        # Crear widget de mensaje si no existe
        if field_name not in self.feedback_widgets:
            self.create_field_feedback_widget(field_name)
        
        # Actualizar mensaje
        self.update_field_feedback(field_name)
    
    def create_field_feedback_widget(self, field_name: str):
        """Crear widget de feedback para un campo."""
        if field_name in self.feedback_widgets:
            return
        
        # Crear frame para el mensaje
        _ = ttk.Frame(self.parent)  # feedback_frame no se usa directamente
        feedback_label = ttk.Label(_, text="")
        
        self.feedback_widgets[field_name] = (_, feedback_label)
    
    def update_field_feedback(self, field_name: str):
        """Actualizar el feedback visual de un campo."""
        if field_name not in self.feedback_widgets:
            return
        
        feedback_frame, feedback_label = self.feedback_widgets[field_name]
        
        # Obtener mensajes del campo
        field_messages = [msg for msg in self.validation_messages if msg.field == field_name]
        
        if field_messages:
            # Mostrar el mensaje más importante
            message = field_messages[-1]  # Último mensaje
            level = message.level
            
            # Configurar estilo según el nivel
            if level == ValidationLevel.SUCCESS:
                style_name = 'ValidationSuccess.TLabel'
            elif level == ValidationLevel.WARNING:
                style_name = 'ValidationWarning.TLabel'
            elif level == ValidationLevel.ERROR:
                style_name = 'ValidationError.TLabel'
            else:
                style_name = 'ValidationInfo.TLabel'
            
            feedback_label.configure(text=message.text, style=style_name)
            feedback_label.pack(padx=5, pady=2)
        else:
            # Ocultar mensaje
            feedback_label.pack_forget()
    
    def set_field_style(self, field_name: str, style_type: str):
        """
        Establecer estilo visual de un campo.
        
        Args:
            field_name: Nombre del campo
            style_type: Tipo de estilo ('success', 'warning', 'error')
        """
        if field_name not in self.field_widgets:
            return
        
        widget = self.field_widgets[field_name]
        
        if isinstance(widget, (ttk.Entry, ttk.Combobox)):
            if style_type == 'success':
                widget.configure(style='FieldSuccess.TEntry')
            elif style_type == 'warning':
                widget.configure(style='FieldWarning.TEntry')
            elif style_type == 'error':
                widget.configure(style='FieldError.TEntry')
            else:
                widget.configure(style='Modern.TEntry')
    
    def clear_field_messages(self, field_name: str):
        """Limpiar mensajes de un campo específico."""
        self.validation_messages = [msg for msg in self.validation_messages if msg.field != field_name]
        self.update_field_feedback(field_name)
    
    def clear_all_messages(self):
        """Limpiar todos los mensajes de validación."""
        self.validation_messages.clear()
        for field_name in self.feedback_widgets:
            self.update_field_feedback(field_name)
    
    def validate_all_fields(self) -> bool:
        """
        Validar todos los campos registrados.
        
        Returns:
            True si todos los campos son válidos, False en caso contrario
        """
        all_valid = True
        
        for field_name in self.field_widgets:
            if not self.validate_field(field_name):
                all_valid = False
        
        return all_valid
    
    def get_validation_summary(self) -> str:
        """
        Obtener resumen de validación.
        
        Returns:
            Resumen de todos los mensajes de validación
        """
        if not self.validation_messages:
            return "Todos los campos son válidos"
        
        summary_parts = []
        error_count = 0
        warning_count = 0
        info_count = 0
        
        for msg in self.validation_messages:
            if msg.level == ValidationLevel.ERROR:
                error_count += 1
                summary_parts.append(f"❌ {msg.text}")
            elif msg.level == ValidationLevel.WARNING:
                warning_count += 1
                summary_parts.append(f"⚠️ {msg.text}")
            elif msg.level == ValidationLevel.INFO:
                info_count += 1
                summary_parts.append(f"ℹ️ {msg.text}")
            else:
                summary_parts.append(f"✅ {msg.text}")
        
        header = f"Resumen de validación: {error_count} errores, {warning_count} advertencias, {info_count} informaciones"
        return header + "\n\n" + "\n".join(summary_parts)
    
    def show_validation_dialog(self):
        """Mostrar diálogo con resumen de validación."""
        summary = self.get_validation_summary()
        
        # Determinar tipo de diálogo según el nivel más alto
        has_errors = any(msg.level == ValidationLevel.ERROR for msg in self.validation_messages)
        has_warnings = any(msg.level == ValidationLevel.WARNING for msg in self.validation_messages)
        
        if has_errors:
            messagebox.showerror("Errores de Validación", summary)
        elif has_warnings:
            messagebox.showwarning("Advertencias de Validación", summary)
        else:
            messagebox.showinfo("Validación Exitosa", summary)


class AFDValidator:
    """Validador específico para AFDs."""
    
    def __init__(self, feedback_system: ValidationFeedback):
        """
        Inicializar validador AFD.
        
        Args:
            feedback_system: Sistema de feedback
        """
        self.feedback = feedback_system
        self.setup_afd_validators()
    
    def setup_afd_validators(self):
        """Configurar validadores específicos para AFD."""
        # Validador para nombres de estados
        self.feedback.register_field('states', None, self.validate_states)
        
        # Validador para alfabeto
        self.feedback.register_field('alphabet', None, self.validate_alphabet)
        
        # Validador para estado inicial
        self.feedback.register_field('initial_state', None, self.validate_initial_state)
        
        # Validador para estados de aceptación
        self.feedback.register_field('accepting_states', None, self.validate_accepting_states)
        
        # Validador para transiciones
        self.feedback.register_field('transitions', None, self.validate_transitions)
    
    def validate_states(self, states: List[str]) -> tuple[bool, str]:
        """
        Validar lista de estados.
        
        Args:
            states: Lista de estados
            
        Returns:
            Tupla (es_válido, mensaje)
        """
        if not states:
            return False, "Debe definir al menos un estado"
        
        if len(states) != len(set(states)):
            return False, "Los nombres de estados deben ser únicos"
        
        for state in states:
            if not state or not state.strip():
                return False, "Los nombres de estados no pueden estar vacíos"
            
            if not state.replace('_', '').replace('-', '').isalnum():
                return False, f"Nombre de estado inválido: '{state}'. Use solo letras, números, _ y -"
        
        return True, f"Estados válidos: {len(states)} estados definidos"
    
    def validate_alphabet(self, symbols: List[str]) -> tuple[bool, str]:
        """
        Validar alfabeto.
        
        Args:
            symbols: Lista de símbolos
            
        Returns:
            Tupla (es_válido, mensaje)
        """
        if not symbols:
            return False, "Debe definir al menos un símbolo en el alfabeto"
        
        if len(symbols) != len(set(symbols)):
            return False, "Los símbolos del alfabeto deben ser únicos"
        
        for symbol in symbols:
            if not symbol or not symbol.strip():
                return False, "Los símbolos no pueden estar vacíos"
            
            if len(symbol) > 1:
                return False, f"Símbolo inválido: '{symbol}'. Use solo caracteres individuales"
        
        return True, f"Alfabeto válido: {len(symbols)} símbolos definidos"
    
    def validate_initial_state(self, initial_state: str) -> tuple[bool, str]:
        """
        Validar estado inicial.
        
        Args:
            initial_state: Estado inicial
            
        Returns:
            Tupla (es_válido, mensaje)
        """
        if not initial_state or not initial_state.strip():
            return False, "Debe seleccionar un estado inicial"
        
        return True, f"Estado inicial válido: {initial_state}"
    
    def validate_accepting_states(self, accepting_states: List[str]) -> tuple[bool, str]:
        """
        Validar estados de aceptación.
        
        Args:
            accepting_states: Lista de estados de aceptación
            
        Returns:
            Tupla (es_válido, mensaje)
        """
        if not accepting_states:
            return False, "Debe definir al menos un estado de aceptación"
        
        return True, f"Estados de aceptación válidos: {len(accepting_states)} estados"
    
    def validate_transitions(self, transitions: List[tuple]) -> tuple[bool, str]:
        """
        Validar transiciones.
        
        Args:
            transitions: Lista de transiciones (from_state, symbol, to_state)
            
        Returns:
            Tupla (es_válido, mensaje)
        """
        if not transitions:
            return False, "Debe definir al menos una transición"
        
        # Verificar transiciones duplicadas
        transition_keys = set()
        for from_state, symbol, to_state in transitions:
            key = (from_state, symbol)
            if key in transition_keys:
                return False, f"Transición duplicada: δ({from_state}, {symbol})"
            transition_keys.add(key)
        
        return True, f"Transiciones válidas: {len(transitions)} transiciones definidas"
    
    def validate_complete_afd(self, afd) -> tuple[bool, List[str]]:
        """
        Validar AFD completo.
        
        Args:
            afd: Instancia de AFD
            
        Returns:
            Tupla (es_válido, lista_de_errores)
        """
        errors = []
        
        # Validar estados
        if not afd.states:
            errors.append("No hay estados definidos")
        
        # Validar alfabeto
        if not afd.alphabet:
            errors.append("No hay alfabeto definido")
        
        # Validar estado inicial
        if not afd.initial_state:
            errors.append("No hay estado inicial definido")
        elif afd.initial_state not in afd.states:
            errors.append("El estado inicial no está en la lista de estados")
        
        # Validar estados de aceptación
        if not afd.accepting_states:
            errors.append("No hay estados de aceptación definidos")
        else:
            for state in afd.accepting_states:
                if state not in afd.states:
                    errors.append(f"Estado de aceptación '{state}' no está en la lista de estados")
        
        # Validar transiciones completas
        if afd.states and afd.alphabet:
            required_transitions = len(afd.states) * len(afd.alphabet)
            actual_transitions = len(afd.transitions)
            
            if actual_transitions < required_transitions:
                missing = required_transitions - actual_transitions
                errors.append(f"Faltan {missing} transiciones. Cada estado debe tener una transición para cada símbolo del alfabeto")
        
        return len(errors) == 0, errors
