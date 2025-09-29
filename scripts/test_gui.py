#!/usr/bin/env python3
"""
Script de prueba para la GUI del AFD Simulator.
"""

import sys
import traceback

def test_gui():
    """Probar la GUI paso a paso."""
    try:
        print("1. Importando módulos...")
        from afd_simulator.gui.main_window import AFDSimulatorGUI
        print("   ✓ Importación exitosa")
        
        print("2. Creando instancia de la aplicación...")
        app = AFDSimulatorGUI()
        print("   ✓ Aplicación creada")
        
        print("3. Iniciando bucle principal...")
        print("   (La ventana debería aparecer ahora)")
        app.run()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTraceback completo:")
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("=== PRUEBA DE GUI AFD SIMULATOR ===")
    success = test_gui()
    if success:
        print("✓ Prueba completada exitosamente")
    else:
        print("❌ Prueba falló")
        sys.exit(1)
