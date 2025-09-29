#!/usr/bin/env python3
"""
Script de diagnóstico para identificar problemas en la GUI.
"""

import sys
import traceback

def diagnosticar_gui():
    """Diagnosticar problemas en la GUI."""
    print("=== DIAGNÓSTICO DE GUI AFD SIMULATOR ===\n")
    
    problemas = []
    
    # 1. Verificar importaciones
    print("1. Verificando importaciones...")
    try:
        from afd_simulator.gui.main_window import AFDSimulatorGUI
        print("   ✓ AFDSimulatorGUI importado correctamente")
    except Exception as e:
        problemas.append(f"Error importando AFDSimulatorGUI: {e}")
        print(f"   ❌ Error: {e}")
    
    try:
        from afd_simulator.gui.help_system import HelpSystem
        print("   ✓ HelpSystem importado correctamente")
    except Exception as e:
        problemas.append(f"Error importando HelpSystem: {e}")
        print(f"   ❌ Error: {e}")
    
    try:
        from afd_simulator.gui.styles import StyleManager
        print("   ✓ StyleManager importado correctamente")
    except Exception as e:
        problemas.append(f"Error importando StyleManager: {e}")
        print(f"   ❌ Error: {e}")
    
    try:
        from afd_simulator.gui.validation_feedback import ValidationFeedback
        print("   ✓ ValidationFeedback importado correctamente")
    except Exception as e:
        problemas.append(f"Error importando ValidationFeedback: {e}")
        print(f"   ❌ Error: {e}")
    
    try:
        from afd_simulator.gui.tutorial_system import TutorialSystem
        print("   ✓ TutorialSystem importado correctamente")
    except Exception as e:
        problemas.append(f"Error importando TutorialSystem: {e}")
        print(f"   ❌ Error: {e}")
    
    # 2. Verificar creación de widgets
    print("\n2. Verificando creación de widgets...")
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana de prueba
        
        app = AFDSimulatorGUI()
        print("   ✓ Aplicación creada correctamente")
        
        # Verificar componentes principales
        if hasattr(app, 'afd_editor'):
            print("   ✓ AFD Editor inicializado")
        else:
            problemas.append("AFD Editor no inicializado")
            
        if hasattr(app, 'help_system'):
            print("   ✓ Sistema de ayuda inicializado")
        else:
            problemas.append("Sistema de ayuda no inicializado")
            
        if hasattr(app, 'style_manager'):
            print("   ✓ Gestor de estilos inicializado")
        else:
            problemas.append("Gestor de estilos no inicializado")
        
        root.destroy()
        
    except Exception as e:
        problemas.append(f"Error creando aplicación: {e}")
        print(f"   ❌ Error: {e}")
        traceback.print_exc()
    
    # 3. Verificar funcionalidades específicas
    print("\n3. Verificando funcionalidades específicas...")
    
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        
        from afd_simulator.gui.help_system import HelpSystem
        help_system = HelpSystem(root)
        
        # Verificar tooltips
        if hasattr(help_system, 'help_texts') and help_system.help_texts:
            print("   ✓ Textos de ayuda cargados")
        else:
            problemas.append("Textos de ayuda no cargados")
        
        # Verificar ventana de ayuda
        try:
            help_system.show_help_window()
            if help_system.help_window:
                help_system.help_window.destroy()
            print("   ✓ Ventana de ayuda funcional")
        except Exception as e:
            problemas.append(f"Error en ventana de ayuda: {e}")
            print(f"   ❌ Error en ventana de ayuda: {e}")
        
        root.destroy()
        
    except Exception as e:
        problemas.append(f"Error verificando funcionalidades: {e}")
        print(f"   ❌ Error: {e}")
    
    # 4. Resumen
    print("\n=== RESUMEN DEL DIAGNÓSTICO ===")
    
    if not problemas:
        print("✅ No se encontraron problemas. La GUI debería funcionar correctamente.")
        print("\nPara ejecutar la aplicación:")
        print("  python main.py --gui")
        print("  o")
        print("  python test_gui.py")
    else:
        print(f"❌ Se encontraron {len(problemas)} problemas:")
        for i, problema in enumerate(problemas, 1):
            print(f"  {i}. {problema}")
        
        print("\nRecomendaciones:")
        print("1. Verificar que todos los archivos estén presentes")
        print("2. Verificar que no haya errores de sintaxis")
        print("3. Ejecutar con python test_gui.py para más detalles")
    
    return len(problemas) == 0

if __name__ == "__main__":
    success = diagnosticar_gui()
    sys.exit(0 if success else 1)
