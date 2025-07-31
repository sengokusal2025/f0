#!/usr/bin/env python3
"""
Independent Variable Generator
Generates random independent variables and saves them to data.csv file.
"""

import argparse
import random
import os
import csv
import sys


def generate_random_variables(num_variables=5):
    """
    Generate specified number of random variables.
    
    Args:
        num_variables (int): Number of random variables to generate (default: 5)
    
    Returns:
        list: List of generated random integers
    """
    # Generate random integers between 1 and 1000
    variables = [random.randint(1, 1000) for _ in range(num_variables)]
    return variables


def save_to_csv(variables, output_path):
    """
    Save variables to CSV file with specified format.
    
    Args:
        variables (list): List of variables to save
        output_path (str): Path where to save the CSV file
    """
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    # Create full file path
    csv_file_path = os.path.join(output_path, 'data.csv')
    
    # Write to CSV file with header 'x'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['x'])  # Header
        for variable in variables:
            writer.writerow([variable])
    
    print(f"Generated {len(variables)} variables and saved to: {csv_file_path}")
    return csv_file_path


def main():
    """
    Main function to handle command line arguments and execute the program.
    """
    parser = argparse.ArgumentParser(
        description='Generate random independent variables and save to data.csv'
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output folder or file path'
    )
    
    parser.add_argument(
        '-n', '--num',
        type=int,
        default=5,
        help='Number of random variables to generate (default: 5)'
    )
    
    args = parser.parse_args()
    
    # Validate number of variables
    if args.num <= 0:
        print("Error: Number of variables must be positive")
        sys.exit(1)
    
    # Generate random variables
    print(f"Generating {args.num} random variables...")
    variables = generate_random_variables(args.num)
    
    # Save to CSV file
    csv_path = save_to_csv(variables, args.output)
    
    # Display generated variables
    print(f"Generated variables: {variables}")
    print("Process completed successfully!")


if __name__ == "__main__":
    main()
