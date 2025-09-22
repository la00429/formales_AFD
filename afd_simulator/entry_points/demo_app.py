"""
Demo application entry point for AFD Simulator.

This module provides demonstration functionality for the AFD Simulator
showing various features and examples.
"""

import sys
from ..core import AFD
from ..examples import AFDFactory, ExampleLoader
from ..utils.formatters import format_transition_path, format_accepted_strings
from ..data import get_available_examples


def demonstrate_afd_factory():
    """Demonstrate AFD factory examples."""
    print("=" * 60)
    print("AFD FACTORY DEMONSTRATIONS")
    print("=" * 60)
    
    examples = AFDFactory.get_available_examples()
    
    for name, description, _ in examples:
        print(f"\n{name}: {description}")
        print("-" * 50)
        
        try:
            afd = AFDFactory.create_example_by_name(name)
            print(f"States: {sorted(afd.states)}")
            print(f"Alphabet: {sorted(afd.alphabet)}")
            print(f"Initial: {afd.initial_state}")
            print(f"Accepting: {sorted(afd.accepting_states)}")
            print(f"Valid: {afd.is_valid()}")
            
            # Test with some strings
            test_strings = ["", "a", "ab", "aa", "ba", "aba", "aab", "baa"]
            print("\nTesting strings:")
            for test_string in test_strings[:4]:  # Test first 4 strings
                try:
                    is_accepted, _ = afd.evaluate_string(test_string)
                    status = "ACCEPTED" if is_accepted else "REJECTED"
                    print(f"  '{test_string}' -> {status}")
                except Exception as e:
                    print(f"  '{test_string}' -> ERROR: {e}")
            
        except Exception as e:
            print(f"Error creating {name}: {e}")


def demonstrate_example_loader():
    """Demonstrate example loader functionality."""
    print("\n\n" + "=" * 60)
    print("EXAMPLE LOADER DEMONSTRATIONS")
    print("=" * 60)
    
    loader = ExampleLoader("afd_simulator/data")
    
    available_examples = loader.get_available_examples()
    print(f"Available examples: {available_examples}")
    
    for example_name in available_examples:
        print(f"\nLoading example: {example_name}")
        print("-" * 30)
        
        try:
            # Get info without loading
            info = loader.get_example_info(example_name)
            print(f"Info: {info}")
            
            # Load and test
            afd = loader.load_example(example_name)
            
            # Generate some accepted strings
            accepted = afd.generate_accepted_strings(5)
            print(f"First 5 accepted strings: {accepted}")
            
        except Exception as e:
            print(f"Error loading {example_name}: {e}")


def demonstrate_modular_usage():
    """Demonstrate modular usage of the AFD components."""
    print("\n\n" + "=" * 60)
    print("MODULAR COMPONENT DEMONSTRATIONS")
    print("=" * 60)
    
    # Create AFD using factory
    print("\n1. Creating AFD using factory:")
    afd = AFDFactory.create_binary_ending_with_one()
    print(f"Created: {afd}")
    
    # Test string evaluation
    print("\n2. String evaluation:")
    test_strings = ["0", "1", "01", "10", "101", "110", "000", "111"]
    for string in test_strings:
        try:
            is_accepted, _ = afd.evaluate_string(string)
            status = "ACCEPTED" if is_accepted else "REJECTED"
            print(f"  '{string}' -> {status}")
        except Exception as e:
            print(f"  '{string}' -> ERROR: {e}")
    
    # Generate accepted strings
    print("\n3. Generating accepted strings:")
    accepted = afd.generate_accepted_strings()
    print(format_accepted_strings(accepted))
    
    # Save to file
    print("\n4. Saving to file:")
    try:
        afd.save_to_file("demo_output.json")
        print("✓ Saved to demo_output.json")
    except Exception as e:
        print(f"✗ Error saving: {e}")
    
    # Load from file
    print("\n5. Loading from file:")
    try:
        loaded_afd = AFD.load_from_file("demo_output.json")
        print(f"✓ Loaded AFD with {len(loaded_afd.states)} states")
        print(f"  Valid: {loaded_afd.is_valid()}")
    except Exception as e:
        print(f"✗ Error loading: {e}")


def run_demo_app():
    """Run the demo AFD Simulator application."""
    print("AFD SIMULATOR - MODULAR ARCHITECTURE DEMONSTRATION")
    
    try:
        demonstrate_afd_factory()
        demonstrate_example_loader()
        demonstrate_modular_usage()
        
        print("\n" + "=" * 60)
        print("DEMONSTRATION COMPLETED")
        print("=" * 60)
        print("\nTo run the interactive simulator, execute:")
        print("python -m afd_simulator.entry_points.console_app")
        print("\nTo run the GUI simulator, execute:")
        print("python -m afd_simulator.entry_points.gui_app")
        
    except Exception as e:
        print(f"Demonstration error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_demo_app()
