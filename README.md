# AFD Simulator - Deterministic Finite Automaton Simulator

A comprehensive Python application for simulating Deterministic Finite Automata (DFA). This simulator provides both console and graphical interfaces for defining, visualizing, and analyzing DFAs with advanced features for educational and research purposes.

## Features

### Core Functionality
- **Complete AFD Definition**: Define all five components of a DFA (states Q, alphabet Σ, initial state q₀, accepting states F, transition function δ)
- **Interactive String Evaluation**: Evaluate strings with detailed step-by-step visualization of state transitions
- **Automatic String Generation**: Generate the first 10 shortest strings accepted by the automaton using BFS algorithm
- **Data Persistence**: Save and load DFA configurations in JSON format
- **Robust Validation**: Comprehensive validation with detailed error reporting

### User Interfaces
- **Graphical User Interface (GUI)**: Modern Tkinter-based interface with visual AFD editing and visualization
- **Console Interface**: Command-line interface for quick operations and scripting
- **Visual AFD Editor**: Drag-and-drop style editing with real-time validation
- **Interactive Visualizer**: Graphical representation of AFDs with states, transitions, and flow

### Advanced Features
- **Factory Pattern**: Pre-built common AFD patterns (ending with 1, even length, contains substring, etc.)
- **Batch Processing**: Evaluate multiple strings simultaneously
- **Export/Import**: JSON-based file format for sharing AFD definitions
- **Educational Examples**: Built-in examples demonstrating various automata concepts

## Requirements

- Python 3.7 or higher
- No external dependencies (uses only Python standard library)

## Quick Start

### Using the Main Launcher (Recommended)

1. **Launch different interfaces:**
```bash
python main.py                # Console interface (default)
python main.py --gui          # GUI interface
python main.py --demo         # Demo mode
python main.py --console      # Console interface (explicit)
```

2. **GUI Features:**
   - Visual AFD editor with drag-and-drop interface
   - Real-time AFD visualization with states and transitions
   - Step-by-step string evaluation
   - Batch string processing
   - Built-in examples and factory patterns

### Programming Interface

```python
from afd_simulator import AFD, AFDFactory

# Create an AFD using factory
afd = AFDFactory.create_binary_ending_with_one()

# Evaluate a string
is_accepted, path = afd.evaluate_string("101")

# Generate accepted strings
accepted = afd.generate_accepted_strings(10)
```

### Module Interface

```bash
# Run as Python module
python -m afd_simulator                # Console interface (default)
python -m afd_simulator --gui          # GUI interface
python -m afd_simulator --demo         # Demo mode
python -m afd_simulator --console      # Console interface (explicit)
```

## File Structure

### Modular Architecture

```
project_AFD/
├── afd_simulator/              # Main package
│   ├── __init__.py            # Package initialization
│   ├── __main__.py            # Module entry point
│   ├── core/                  # Core AFD implementation
│   │   ├── __init__.py
│   │   └── afd.py            # AFD class implementation
│   ├── ui/                    # Console interface components
│   │   ├── __init__.py
│   │   ├── simulator.py      # Console simulator class
│   │   ├── input_handler.py  # Input validation and handling
│   │   └── menu_system.py    # Menu display and navigation
│   ├── gui/                   # Graphical user interface
│   │   ├── __init__.py
│   │   ├── main_window.py    # Main GUI window
│   │   ├── afd_editor.py     # Visual AFD editor
│   │   ├── string_evaluator.py # String evaluation interface
│   │   └── afd_visualizer.py # AFD visualization component
│   ├── utils/                 # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py     # Input and AFD validation
│   │   └── formatters.py     # Output formatting utilities
│   ├── examples/              # Example AFDs and factory
│   │   ├── __init__.py
│   │   ├── factory.py        # AFD factory for common patterns
│   │   └── loader.py         # Example loading utilities
│   ├── data/                  # Data files and resources
│   │   ├── __init__.py
│   │   ├── binary_afd.json   # Example: strings ending with '1'
│   │   ├── even_length.json  # Example: strings of even length
│   │   ├── ends_with_01.json # Example: strings ending with '01'
│   │   └── exactly_two_as.json # Example: exactly two 'a's
│   └── entry_points/          # Application entry points
│       ├── __init__.py
│       ├── console_app.py    # Console application entry
│       ├── gui_app.py        # GUI application entry
│       └── demo_app.py       # Demo application entry
├── main.py                   # Universal application launcher
├── README.md                 # This documentation
└── requirements.txt          # Project dependencies
```

## Usage Examples

### GUI Interface

The graphical interface provides three main tabs:

1. **AFD Editor**: Create and edit AFD definitions visually
   - Add states and alphabet symbols
   - Set initial and accepting states
   - Define transitions with dropdown menus
   - Real-time validation and summary

2. **String Evaluator**: Test strings against your AFD
   - Single string evaluation with step-by-step process
   - Batch evaluation of multiple strings
   - Visual feedback for accepted/rejected strings

3. **AFD Visualizer**: See your AFD graphically
   - States represented as circles
   - Accepting states as double circles
   - Initial state highlighted in red
   - Transitions as arrows with symbols
   - Zoom and pan capabilities

### Console Interface

1. **Creating an AFD**:
   - Choose option 1 from the main menu
   - Define states: `q0 q1 q2`
   - Define alphabet: `0 1`
   - Set initial state: `q0`
   - Set accepting states: `q2`
   - Add transitions:
     - `q0 0 q1`
     - `q0 1 q0`
     - `q1 0 q1`
     - `q1 1 q2`
     - `q2 0 q2`
     - `q2 1 q0`

### Evaluating Strings
The simulator will show step-by-step transitions:
```
Evaluating string: '101'
1. From state (q0) with symbol '1' transitions to state (q0).
2. From state (q0) with symbol '0' transitions to state (q1).
3. From state (q1) with symbol '1' transitions to state (q2).
Result: The string '101' is ACCEPTED.
```

### Generated Accepted Strings
The simulator can automatically generate accepted strings:
```
1. '01'
2. '001'
3. '011'
4. '0001'
5. '0101'
6. '0111'
7. '00001'
8. '00101'
9. '00111'
10. '01001'
```

## Technical Implementation

### Modular Architecture Benefits

- **Separation of Concerns**: Core logic, UI, utilities, and examples are separated
- **Maintainability**: Easy to modify individual components without affecting others
- **Extensibility**: Simple to add new features or AFD patterns
- **Testability**: Each module can be tested independently
- **Reusability**: Components can be imported and used in other projects

### Core Components

- **State Management**: Uses Python sets for efficient state operations
- **Transition Function**: Implemented as dictionary for O(1) lookup
- **String Generation**: BFS algorithm ensures shortest strings first
- **Validation**: Comprehensive checking of all DFA requirements
- **Persistence**: JSON format for human-readable storage
- **Input Handling**: Robust validation with user-friendly error messages
- **Factory Pattern**: Easy creation of common AFD patterns

### GUI Implementation

- **Tkinter Framework**: Cross-platform GUI using Python's standard library
- **Modular Design**: Separate components for editing, evaluation, and visualization
- **Visual Editor**: Intuitive form-based AFD creation with real-time validation
- **Interactive Visualization**: Canvas-based drawing with zoom, pan, and layout algorithms
- **Responsive Layout**: Adaptive interface that works on different screen sizes

## Educational Value

This simulator is designed as an educational tool for:
- Understanding DFA concepts and formal language theory
- Visualizing state transitions and computation paths
- Exploring different language patterns and their corresponding automata
- Practicing automata design and analysis

## Author

Developed as an educational tool for automata theory and formal languages.
