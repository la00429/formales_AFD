#!/usr/bin/env python3
"""
Script de prueba específico para las funcionalidades del editor AFD.
"""

import tkinter as tk
from tkinter import messagebox
import sys

def test_editor_functions():
    """Probar las funcionalidades específicas del editor."""
    print("=== PRUEBA DE FUNCIONALIDADES DEL EDITOR AFD ===\n")
    
    try:
        # Crear ventana de prueba
        root = tk.Tk()
        root.title("Prueba Editor AFD")
        root.geometry("800x600")
        
        # Importar y crear editor
        from afd_simulator.gui.main_window import AFDSimulatorGUI
        app = AFDSimulatorGUI()
        
        # Obtener referencia al editor
        editor = app.afd_editor
        
        print("1. Probando agregar estados...")
        # Simular agregar estados
        editor.states_entry.insert(0, "q0 q1 q2")
        editor.add_states()
        
        states_count = editor.states_listbox.size()
        print(f"   Estados agregados: {states_count}")
        
        if states_count > 0:
            print("   ✓ Agregar estados funciona")
        else:
            print("   ❌ Agregar estados falló")
            return False
        
        print("\n2. Probando agregar alfabeto...")
        # Simular agregar alfabeto
        editor.alphabet_entry.insert(0, "a b")
        editor.add_alphabet()
        
        alphabet_count = editor.alphabet_listbox.size()
        print(f"   Símbolos agregados: {alphabet_count}")
        
        if alphabet_count > 0:
            print("   ✓ Agregar alfabeto funciona")
        else:
            print("   ❌ Agregar alfabeto falló")
            return False
        
        print("\n3. Probando seleccionar estado inicial...")
        # Seleccionar estado inicial
        states = [editor.states_listbox.get(i) for i in range(editor.states_listbox.size())]
        if states:
            editor.initial_var.set(states[0])
            print(f"   Estado inicial seleccionado: {states[0]}")
            print("   ✓ Seleccionar estado inicial funciona")
        else:
            print("   ❌ No hay estados para seleccionar")
            return False
        
        print("\n4. Probando agregar estado de aceptación...")
        # Seleccionar un estado y agregarlo como aceptación
        editor.states_listbox.selection_set(0)
        editor.add_accepting_state()
        
        accepting_count = editor.accepting_listbox.size()
        print(f"   Estados de aceptación: {accepting_count}")
        
        if accepting_count > 0:
            print("   ✓ Agregar estado de aceptación funciona")
        else:
            print("   ❌ Agregar estado de aceptación falló")
            return False
        
        print("\n5. Probando agregar transición...")
        # Configurar transición
        states = [editor.states_listbox.get(i) for i in range(editor.states_listbox.size())]
        symbols = [editor.alphabet_listbox.get(i) for i in range(editor.alphabet_listbox.size())]
        
        if states and symbols:
            editor.from_var.set(states[0])
            editor.symbol_var.set(symbols[0])
            editor.to_var.set(states[1] if len(states) > 1 else states[0])
            
            # Agregar transición
            editor.add_transition()
            
            transitions_count = len(editor.transitions_tree.get_children())
            print(f"   Transiciones agregadas: {transitions_count}")
            
            if transitions_count > 0:
                print("   ✓ Agregar transición funciona")
            else:
                print("   ❌ Agregar transición falló")
                return False
        else:
            print("   ❌ No hay estados o símbolos para crear transición")
            return False
        
        print("\n6. Probando validación del AFD...")
        # Validar AFD
        editor.validate_current_afd()
        print("   ✓ Validación ejecutada")
        
        print("\n7. Probando resumen del AFD...")
        # Verificar resumen
        summary = editor.summary_text.get(1.0, tk.END).strip()
        if summary:
            print("   ✓ Resumen del AFD generado")
            print(f"   Resumen: {summary[:100]}...")
        else:
            print("   ❌ Resumen del AFD vacío")
            return False
        
        print("\n=== RESULTADO ===")
        print("✅ Todas las funcionalidades básicas del editor funcionan correctamente")
        
        # Mostrar ventana por unos segundos para verificar visualmente
        print("\nMostrando ventana por 5 segundos para verificación visual...")
        root.after(5000, root.destroy)
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_editor_functions()
    if success:
        print("\n🎉 ¡Prueba exitosa! Las funcionalidades del editor están funcionando.")
    else:
        print("\n💥 Prueba falló. Hay problemas con las funcionalidades del editor.")
        sys.exit(1)
