# AFD Simulator - Deterministic Finite Automaton Simulator

A comprehensive Python application for simulating Deterministic Finite Automata (DFA). This simulator allows users to define, save, load, and evaluate DFAs, as well as generate strings that belong to the language recognized by the automaton.

## Features

- **Complete AFD Definition**: Define all five components of a DFA (states Q, alphabet Σ, initial state q₀, accepting states F, transition function δ)
- **Interactive String Evaluation**: Evaluate strings with detailed step-by-step visualization of state transitions
- **Automatic String Generation**: Generate the first 10 shortest strings accepted by the automaton using BFS algorithm
- **Data Persistence**: Save and load DFA configurations in JSON format
- **Robust Validation**: Comprehensive validation with detailed error reporting
- **User-Friendly Interface**: Intuitive console interface with help system
- **Example Automata**: Pre-loaded examples demonstrating common DFA patterns

## Requirements

- Python 3.7 or higher
- No external dependencies (uses only Python standard library)

## Quick Start

1. **Run the interactive simulator:**
```bash
python afd_simulator.py
```

2. **Test with examples:**
```bash
python test_examples.py
```

## File Structure

- `afd_simulator.py` - Main interactive application
- `afd.py` - Core DFA class implementation
- `test_examples.py` - Demonstration script with example automata
- `examples/` - Directory containing example AFD definitions
  - `binary_afd.json` - Accepts strings ending with '1'
  - `even_length.json` - Accepts strings of even length
  - `ends_with_01.json` - Accepts strings ending with '01'
- `README.md` - This documentation
- `requirements.txt` - Project dependencies

## Example Usage

### Creating an AFD
1. Choose option 1 from the main menu
2. Define states: `q0 q1 q2`
3. Define alphabet: `0 1`
4. Set initial state: `q0`
5. Set accepting states: `q2`
6. Add transitions:
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

- **State Management**: Uses Python sets for efficient state operations
- **Transition Function**: Implemented as dictionary for O(1) lookup
- **String Generation**: BFS algorithm ensures shortest strings first
- **Validation**: Comprehensive checking of all DFA requirements
- **Persistence**: JSON format for human-readable storage

## Educational Value

This simulator is designed as an educational tool for:
- Understanding DFA concepts and formal language theory
- Visualizing state transitions and computation paths
- Exploring different language patterns and their corresponding automata
- Practicing automata design and analysis

## Author

Developed as an educational tool for automata theory and formal languages.
