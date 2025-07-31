#!/usr/bin/env python3
"""
Test Code for Independent Variable Generator
Tests the functionality of func.py and lib.py modules.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add current directory to path to import local modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import func
import lib


def test_generate_random_variables():
    """Test the random variable generation function."""
    print("Testing generate_random_variables()...")
    
    # Test default case (5 variables)
    variables = func.generate_random_variables()
    assert len(variables) == 5, f"Expected 5 variables, got {len(variables)}"
    assert all(isinstance(v, int) for v in variables), "All variables should be integers"
    assert all(1 <= v <= 1000 for v in variables), "All variables should be between 1 and 1000"
    
    # Test custom number
    variables = func.generate_random_variables(10)
    assert len(variables) == 10, f"Expected 10 variables, got {len(variables)}"
    
    # Test single variable
    variables = func.generate_random_variables(1)
    assert len(variables) == 1, f"Expected 1 variable, got {len(variables)}"
    
    print("✓ generate_random_variables() tests passed")


def test_save_to_csv():
    """Test CSV saving functionality."""
    print("Testing save_to_csv()...")
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        test_data = [1, 3, 5, 23, 56]
        csv_path = func.save_to_csv(test_data, temp_dir)
        
        # Check if file was created
        assert os.path.exists(csv_path), "CSV file was not created"
        
        # Check file contents
        with open(csv_path, 'r') as f:
            lines = f.read().strip().split('\n')
            assert lines[0] == 'x', f"Expected header 'x', got '{lines[0]}'"
            assert len(lines) == 6, f"Expected 6 lines (header + 5 data), got {len(lines)}"
            
            # Check data values
            for i, expected_value in enumerate(test_data):
                assert lines[i+1] == str(expected_value), f"Expected {expected_value}, got {lines[i+1]}"
    
    print("✓ save_to_csv() tests passed")


def test_read_csv_data():
    """Test CSV reading functionality."""
    print("Testing read_csv_data()...")
    
    # Create temporary CSV file
    with tempfile.TemporaryDirectory() as temp_dir:
        csv_path = os.path.join(temp_dir, 'test_data.csv')
        test_data = [1, 3, 5, 23, 56]
        
        # Create test CSV file
        with open(csv_path, 'w') as f:
            f.write('x\n')
            for value in test_data:
                f.write(f'{value}\n')
        
        # Test reading
        read_data = lib.read_csv_data(csv_path)
        assert read_data == test_data, f"Expected {test_data}, got {read_data}"
    
    # Test file not found
    try:
        lib.read_csv_data('nonexistent_file.csv')
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError:
        pass  # Expected
    
    print("✓ read_csv_data() tests passed")


def test_output_csv_content():
    """Test CSV content output functionality."""
    print("Testing output_csv_content()...")
    
    # Create temporary CSV file
    with tempfile.TemporaryDirectory() as temp_dir:
        csv_path = os.path.join(temp_dir, 'test_data.csv')
        test_data = [1, 3, 5]
        
        # Create test CSV file
        with open(csv_path, 'w') as f:
            f.write('x\n')
            for value in test_data:
                f.write(f'{value}\n')
        
        # Test output (should return True for success)
        result = lib.output_csv_content(csv_path)
        assert result == True, "output_csv_content should return True on success"
    
    # Test with non-existent file
    result = lib.output_csv_content('nonexistent_file.csv')
    assert result == False, "output_csv_content should return False on failure"
    
    print("✓ output_csv_content() tests passed")


def test_get_csv_statistics():
    """Test CSV statistics functionality."""
    print("Testing get_csv_statistics()...")
    
    # Create temporary CSV file
    with tempfile.TemporaryDirectory() as temp_dir:
        csv_path = os.path.join(temp_dir, 'test_data.csv')
        test_data = [10, 20, 30, 40, 50]
        
        # Create test CSV file
        with open(csv_path, 'w') as f:
            f.write('x\n')
            for value in test_data:
                f.write(f'{value}\n')
        
        # Test statistics
        stats = lib.get_csv_statistics(csv_path)
        assert "error" not in stats, f"Error in statistics: {stats.get('error')}"
        assert stats['count'] == 5, f"Expected count 5, got {stats['count']}"
        assert stats['min'] == 10, f"Expected min 10, got {stats['min']}"
        assert stats['max'] == 50, f"Expected max 50, got {stats['max']}"
        assert stats['average'] == 30.0, f"Expected average 30.0, got {stats['average']}"
        assert stats['sum'] == 150, f"Expected sum 150, got {stats['sum']}"
    
    print("✓ get_csv_statistics() tests passed")


def test_validate_csv_format():
    """Test CSV format validation functionality."""
    print("Testing validate_csv_format()...")
    
    # Create temporary CSV file with valid format
    with tempfile.TemporaryDirectory() as temp_dir:
        csv_path = os.path.join(temp_dir, 'valid_data.csv')
        
        # Create valid CSV file
        with open(csv_path, 'w') as f:
            f.write('x\n1\n2\n3\n')
        
        # Test validation
        result = lib.validate_csv_format(csv_path)
        assert result['valid'] == True, f"Valid CSV should pass validation: {result['messages']}"
        
        # Create invalid CSV file (wrong header)
        invalid_csv_path = os.path.join(temp_dir, 'invalid_data.csv')
        with open(invalid_csv_path, 'w') as f:
            f.write('y\n1\n2\n3\n')
        
        result = lib.validate_csv_format(invalid_csv_path)
        assert result['valid'] == False, "Invalid CSV should fail validation"
    
    print("✓ validate_csv_format() tests passed")


def test_integration():
    """Integration test: Generate data and read it back."""
    print("Testing integration (func.py + lib.py)...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate random variables and save to CSV
        variables = func.generate_random_variables(7)
        csv_path = func.save_to_csv(variables, temp_dir)
        
        # Read back the data
        read_data = lib.read_csv_data(csv_path)
        
        # Verify data matches
        assert read_data == variables, f"Generated: {variables}, Read: {read_data}"
        
        # Test statistics
        stats = lib.get_csv_statistics(csv_path)
        assert stats['count'] == 7, f"Expected count 7, got {stats['count']}"
        
        # Test validation
        validation = lib.validate_csv_format(csv_path)
        assert validation['valid'] == True, f"Generated CSV should be valid: {validation['messages']}"
    
    print("✓ Integration tests passed")


def run_all_tests():
    """Run all test functions."""
    print("=" * 50)
    print("Running Independent Variable Generator Tests")
    print("=" * 50)
    
    test_functions = [
        test_generate_random_variables,
        test_save_to_csv,
        test_read_csv_data,
        test_output_csv_content,
        test_get_csv_statistics,
        test_validate_csv_format,
        test_integration
    ]
    
    passed = 0
    failed = 0
    
    for test_func in test_functions:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__} failed: {str(e)}")
            failed += 1
    
    print("=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    if failed == 0:
        print("All tests passed! ✓")
        return True
    else:
        print(f"{failed} test(s) failed! ✗")
        return False


def demo_usage():
    """Demonstrate the usage of the modules."""
    print("\n" + "=" * 50)
    print("Demonstration of Independent Variable Generator")
    print("=" * 50)
    
    # Create temporary directory for demo
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Demo directory: {temp_dir}")
        
        # Generate some random variables
        print("\n1. Generating 5 random variables...")
        variables = func.generate_random_variables(5)
        print(f"Generated variables: {variables}")
        
        # Save to CSV
        print("\n2. Saving to CSV file...")
        csv_path = func.save_to_csv(variables, temp_dir)
        
        # Read and display CSV content
        print("\n3. Reading and displaying CSV content...")
        lib.output_csv_content(csv_path)
        
        # Show statistics
        print("\n4. Calculating statistics...")
        stats = lib.get_csv_statistics(csv_path)
        if "error" not in stats:
            print(f"Statistics: {stats}")
        
        # Validate format
        print("\n5. Validating CSV format...")
        validation = lib.validate_csv_format(csv_path)
        print(f"Validation result: {validation}")
        
        print("\n" + "=" * 50)
        print("Demo completed!")
        print("=" * 50)


if __name__ == "__main__":
    """Main execution point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test and demo the Independent Variable Generator')
    parser.add_argument('--demo', action='store_true', help='Run demonstration')
    parser.add_argument('--test', action='store_true', help='Run tests')
    
    args = parser.parse_args()
    
    if args.demo:
        demo_usage()
    elif args.test:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    else:
        # Run both by default
        success = run_all_tests()
        if success:
            demo_usage()
        sys.exit(0 if success else 1)
