"""
Test script to demonstrate AFD Simulator functionality with example automata.

This script loads example AFD definitions and demonstrates key features
including string evaluation and string generation.
"""

from afd import AFD
import os


def test_afd_examples():
    """Test the AFD simulator with example automata."""
    print("=" * 60)
    print("AFD SIMULATOR - EXAMPLE DEMONSTRATIONS")
    print("=" * 60)
    
    # Test Binary AFD (accepts strings that end with '1')
    print("\n1. BINARY AFD - Accepts strings ending with '1'")
    print("-" * 50)
    
    try:
        binary_afd = AFD.load_from_file("examples/binary_afd.json")
        print(f"Loaded AFD: {binary_afd}")
        
        # Test string evaluation
        test_strings = ["0", "1", "01", "10", "101", "110", "000", "111"]
        print(f"\nTesting string evaluation:")
        for string in test_strings:
            try:
                is_accepted, path = binary_afd.evaluate_string(string)
                status = "ACCEPTED" if is_accepted else "REJECTED"
                print(f"  '{string}' -> {status}")
            except Exception as e:
                print(f"  '{string}' -> ERROR: {e}")
        
        # Generate accepted strings
        print(f"\nGenerating first 10 accepted strings:")
        accepted = binary_afd.generate_accepted_strings()
        for i, string in enumerate(accepted, 1):
            print(f"  {i:2d}. '{string}'")
            
    except Exception as e:
        print(f"Error loading binary AFD: {e}")
    
    # Test Even Length AFD
    print("\n\n2. EVEN LENGTH AFD - Accepts strings of even length")
    print("-" * 50)
    
    try:
        even_afd = AFD.load_from_file("examples/even_length.json")
        print(f"Loaded AFD: {even_afd}")
        
        # Test string evaluation
        test_strings = ["", "a", "aa", "ab", "aaa", "aab", "baa", "bb"]
        print(f"\nTesting string evaluation:")
        for string in test_strings:
            try:
                is_accepted, path = even_afd.evaluate_string(string)
                status = "ACCEPTED" if is_accepted else "REJECTED"
                print(f"  '{string}' -> {status}")
            except Exception as e:
                print(f"  '{string}' -> ERROR: {e}")
        
        # Generate accepted strings
        print(f"\nGenerating first 10 accepted strings:")
        accepted = even_afd.generate_accepted_strings()
        for i, string in enumerate(accepted, 1):
            print(f"  {i:2d}. '{string}'")
            
    except Exception as e:
        print(f"Error loading even length AFD: {e}")
    
    # Test Ends with 01 AFD
    print("\n\n3. ENDS WITH '01' AFD - Accepts strings ending with '01'")
    print("-" * 50)
    
    try:
        ends01_afd = AFD.load_from_file("examples/ends_with_01.json")
        print(f"Loaded AFD: {ends01_afd}")
        
        # Test string evaluation with detailed path
        test_string = "101"
        print(f"\nDetailed evaluation of '{test_string}':")
        try:
            is_accepted, path = ends01_afd.evaluate_string(test_string)
            for i, (from_state, symbol, to_state) in enumerate(path, 1):
                print(f"  {i}. From state ({from_state}) with symbol '{symbol}' "
                      f"transitions to state ({to_state}).")
            status = "ACCEPTED" if is_accepted else "REJECTED"
            print(f"  Result: '{test_string}' is {status}.")
        except Exception as e:
            print(f"  Error: {e}")
        
        # Generate accepted strings
        print(f"\nGenerating first 10 accepted strings:")
        accepted = ends01_afd.generate_accepted_strings()
        for i, string in enumerate(accepted, 1):
            print(f"  {i:2d}. '{string}'")
            
    except Exception as e:
        print(f"Error loading ends with 01 AFD: {e}")
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETED")
    print("=" * 60)
    print("\nTo run the interactive simulator, execute:")
    print("python afd_simulator.py")


def create_sample_afd():
    """Create a sample AFD programmatically."""
    print("\n\n4. PROGRAMMATIC AFD CREATION")
    print("-" * 50)
    
    # Create AFD that accepts strings with exactly two 'a's
    afd = AFD()
    
    # Add states
    afd.add_state("q0")  # No 'a's yet
    afd.add_state("q1")  # One 'a'
    afd.add_state("q2")  # Two 'a's
    afd.add_state("q3")  # More than two 'a's
    
    # Add alphabet
    afd.add_symbol("a")
    afd.add_symbol("b")
    
    # Set initial state
    afd.set_initial_state("q0")
    
    # Set accepting states
    afd.add_accepting_state("q2")
    
    # Add transitions
    afd.add_transition("q0", "a", "q1")
    afd.add_transition("q0", "b", "q0")
    afd.add_transition("q1", "a", "q2")
    afd.add_transition("q1", "b", "q1")
    afd.add_transition("q2", "a", "q3")
    afd.add_transition("q2", "b", "q2")
    afd.add_transition("q3", "a", "q3")
    afd.add_transition("q3", "b", "q3")
    
    print("Created AFD that accepts strings with exactly two 'a's:")
    print(afd)
    
    # Test some strings
    test_strings = ["", "a", "aa", "aaa", "ab", "aab", "baa", "baba", "aaab"]
    print(f"\nTesting string evaluation:")
    for string in test_strings:
        try:
            is_accepted, path = afd.evaluate_string(string)
            status = "ACCEPTED" if is_accepted else "REJECTED"
            print(f"  '{string}' -> {status}")
        except Exception as e:
            print(f"  '{string}' -> ERROR: {e}")
    
    # Save to file
    try:
        afd.save_to_file("examples/exactly_two_as.json")
        print(f"\n✓ AFD saved to 'examples/exactly_two_as.json'")
    except Exception as e:
        print(f"✗ Error saving AFD: {e}")


if __name__ == "__main__":
    # Create examples directory if it doesn't exist
    os.makedirs("examples", exist_ok=True)
    
    test_afd_examples()
    create_sample_afd()
