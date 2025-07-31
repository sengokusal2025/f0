#!/usr/bin/env python3
"""
Data CSV Library
Library functions for reading and outputting data.csv files.
"""

import csv
import os
import sys


def read_csv_data(file_path):
    """
    Read data from CSV file.
    
    Args:
        file_path (str): Path to the CSV file
    
    Returns:
        list: List of values read from the CSV file
        
    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        Exception: If there's an error reading the file
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    
    data = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            
            # Skip header row
            header = next(reader, None)
            if header is None:
                raise Exception("CSV file is empty")
            
            # Read data rows
            for row in reader:
                if row:  # Skip empty rows
                    try:
                        # Convert to integer if possible
                        value = int(row[0])
                        data.append(value)
                    except (ValueError, IndexError):
                        # If conversion fails, keep as string
                        data.append(row[0] if row else "")
        
        return data
        
    except Exception as e:
        raise Exception(f"Error reading CSV file: {str(e)}")


def output_csv_content(file_path):
    """
    Output the contents of CSV file to stdout.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read the data
        data = read_csv_data(file_path)
        
        # Output header
        print("CSV Content:")
        print("=" * 20)
        print("x")  # Header
        print("-" * 20)
        
        # Output data values
        for value in data:
            print(value)
        
        print("=" * 20)
        print(f"Total records: {len(data)}")
        
        return True
        
    except FileNotFoundError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return False


def get_csv_statistics(file_path):
    """
    Get basic statistics of the CSV data.
    
    Args:
        file_path (str): Path to the CSV file
    
    Returns:
        dict: Dictionary containing statistics (min, max, average, count)
    """
    try:
        data = read_csv_data(file_path)
        
        # Filter only numeric values
        numeric_data = [x for x in data if isinstance(x, (int, float))]
        
        if not numeric_data:
            return {"error": "No numeric data found"}
        
        stats = {
            "count": len(numeric_data),
            "min": min(numeric_data),
            "max": max(numeric_data),
            "average": sum(numeric_data) / len(numeric_data),
            "sum": sum(numeric_data)
        }
        
        return stats
        
    except Exception as e:
        return {"error": str(e)}


def validate_csv_format(file_path):
    """
    Validate if the CSV file follows the expected format.
    
    Args:
        file_path (str): Path to the CSV file
    
    Returns:
        dict: Validation result with status and messages
    """
    result = {
        "valid": True,
        "messages": []
    }
    
    try:
        if not os.path.exists(file_path):
            result["valid"] = False
            result["messages"].append("File does not exist")
            return result
        
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            
            # Check header
            header = next(reader, None)
            if header is None:
                result["valid"] = False
                result["messages"].append("File is empty")
                return result
            
            if len(header) != 1 or header[0].lower() != 'x':
                result["valid"] = False
                result["messages"].append("Invalid header format. Expected 'x'")
            
            # Check data rows
            row_count = 0
            for row_num, row in enumerate(reader, start=2):
                if row:  # Skip empty rows
                    row_count += 1
                    if len(row) != 1:
                        result["valid"] = False
                        result["messages"].append(f"Row {row_num}: Expected 1 column, found {len(row)}")
                    
                    try:
                        int(row[0])
                    except (ValueError, IndexError):
                        result["messages"].append(f"Row {row_num}: Non-numeric value '{row[0] if row else ''}'")
            
            if row_count == 0:
                result["valid"] = False
                result["messages"].append("No data rows found")
            else:
                result["messages"].append(f"Found {row_count} data rows")
                
    except Exception as e:
        result["valid"] = False
        result["messages"].append(f"Error reading file: {str(e)}")
    
    return result


# Convenience function for command line usage
def main():
    """
    Main function for command line usage of the library.
    """
    if len(sys.argv) < 2:
        print("Usage: python lib.py <csv_file_path>")
        print("This will output the contents of the specified CSV file.")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    print(f"Processing file: {csv_file}")
    print()
    
    # Output file contents
    if output_csv_content(csv_file):
        print()
        
        # Show statistics
        stats = get_csv_statistics(csv_file)
        if "error" not in stats:
            print("Statistics:")
            print(f"  Count: {stats['count']}")
            print(f"  Min: {stats['min']}")
            print(f"  Max: {stats['max']}")
            print(f"  Average: {stats['average']:.2f}")
            print(f"  Sum: {stats['sum']}")
        
        print()
        
        # Validate format
        validation = validate_csv_format(csv_file)
        print("Validation Result:")
        print(f"  Valid: {validation['valid']}")
        for message in validation['messages']:
            print(f"  - {message}")


if __name__ == "__main__":
    main()
