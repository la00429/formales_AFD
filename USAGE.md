# AFD Simulator - Guía de Uso Rápido

## 🚀 Inicio Rápido

### Opción 1: Launcher Principal (Recomendado)
```bash
# Interfaz de consola (por defecto)
python main.py

# Interfaz gráfica
python main.py --gui

# Modo demostración
python main.py --demo

# Ayuda
python main.py --help
```

### Opción 2: Como Módulo Python
```bash
# Interfaz de consola
python -m afd_simulator

# Interfaz gráfica
python -m afd_simulator --gui

# Modo demostración
python -m afd_simulator --demo
```

### Opción 3: Importación en Python
```python
from afd_simulator import AFD, AFDFactory

# Crear AFD usando factory
afd = AFDFactory.create_binary_ending_with_one()

# Evaluar cadena
is_accepted, path = afd.evaluate_string("101")
print(f"Cadena aceptada: {is_accepted}")

# Generar cadenas aceptadas
accepted = afd.generate_accepted_strings(10)
print(f"Primeras cadenas: {accepted}")
```

## 🎯 Características Principales

- **Interfaz Gráfica**: Editor visual de AFD con visualización en tiempo real
- **Interfaz de Consola**: Menú interactivo completo
- **Factory Patterns**: Creación rápida de AFD comunes
- **Validación Robusta**: Verificación completa de definiciones
- **Persistencia**: Guardar/cargar AFD en formato JSON
- **Ejemplos Incluidos**: 4 patrones de AFD predefinidos

## 📁 Ejemplos Incluidos

1. **Binary AFD**: Acepta cadenas que terminan con '1'
2. **Even Length**: Acepta cadenas de longitud par
3. **Ends with 01**: Acepta cadenas que terminan con '01'
4. **Exactly Two A's**: Acepta cadenas con exactamente dos 'a's

## 🛠️ Requisitos

- Python 3.7+
- Solo librerías estándar de Python (incluye Tkinter para GUI)
