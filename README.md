# AFD Simulator - Deterministic Finite Automaton Simulator

A comprehensive Python application for simulating Deterministic Finite Automata (DFA). This simulator allows users to define, save, load, and evaluate DFAs, as well as generate strings that belong to the language recognized by the automaton.

## Features

- **AFD Definition**: Define all five components of a DFA (states, alphabet, initial state, accepting states, transition function)
- **String Evaluation**: Evaluate strings with step-by-step visualization of state transitions
- **String Generation**: Generate the first 10 shortest strings accepted by the automaton
- **Data Persistence**: Save and load DFA configurations in JSON format
- **Interactive Interface**: User-friendly console interface
- **Error Handling**: Robust error handling for invalid inputs

## Requirements

- Python 3.7 or higher
- No external dependencies (uses only Python standard library)

## Usage

Run the main application:
```bash
python afd_simulator.py
```

## File Structure

- `afd_simulator.py` - Main application file
- `afd.py` - DFA class implementation
- `README.md` - This file
- `requirements.txt` - Project dependencies

## Author

Developed as an educational tool for automata theory and formal languages.
