"""
Lanzador sencillo para abrir la GUI del Simulador AFD.

Uso:
  python main.py

También puedes ejecutar:
  python -m afd_simulator           # GUI (por defecto)
  python -m afd_simulator --console # Consola
"""

from afd_simulator.entry_points.gui_app import run_gui_app


if __name__ == "__main__":
    run_gui_app()


