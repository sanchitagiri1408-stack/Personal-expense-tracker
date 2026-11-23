"""
Data Loader Module
==================
This module handles loading expense data from CSV files.
"""

import csv
import os
from datetime import datetime


def load_csv_data(filepath):
    """
    Load expense data from a CSV file.

    Parameters:
    -----------
    filepath : str
        Path to the CSV file

    Returns:
    --------
    list : List of dictionaries containing expense records

    Raises:
    -------
    FileNotFoundError: If the file doesn't exist
    ValueError: If the file format is invalid
    """
    # Check if file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    expenses = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Validate required columns exist in header
            required_columns = ['date', 'category', 'amount']
            if reader.fieldnames is None:
                raise ValueError("CSV file is empty")
            missing_columns = [col for col in required_columns if col not in reader.fieldnames]
            if missing_columns:
                raise ValueError(f"CSV missing required columns: {missing_columns}")

            for row_num, row in enumerate(reader, start=2):
                try:
                    # Validate required fields
                    if not row.get('date') or not row.get('category') or not row.get('amount'):
                        print(f"⚠ Warning: Skipping row {row_num} - missing required fields")
                        continue

                    # Parse and validate amount
                    try:
                        amount = float(row['amount'])
                        if amount < 0:
                            print(f"⚠ Warning: Skipping row {row_num} - negative amount")
                            continue
                    except ValueError:
                        print(f"⚠ Warning: Skipping row {row_num} - invalid amount")
                        continue

                    # Parse date
                    try:
                        datetime.strptime(row['date'], '%Y-%m-%d')
                    except ValueError:
                        # Try alternative formats
                        for fmt in ['%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']:
                            try:
                                datetime.strptime(row['date'], fmt)
                                break
                            except ValueError:
                                continue
                        else:
                            print(f"⚠ Warning: Skipping row {row_num} - invalid date format")
                            continue

                    # Create expense record
                    expense = {
                        'date': row['date'],
                        'category': row['category'].strip(),
                        'subcategory': row.get('subcategory', '').strip() or 'General',
                        'amount': amount,
                        'description': row.get('description', '').strip() or 'No description',
                        'payment_method': row.get('payment_method', '').strip() or 'Other'
                    }

                    expenses.append(expense)

                except Exception as e:
                    print(f"⚠ Warning: Error processing row {row_num}: {e}")
                    continue

    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")

    if not expenses:
        raise ValueError("No valid expense records found in file")

    return expenses


def display_sample_csv_format():
    """
    Display the expected CSV format for the user.
    """
    print("\n" + "="*60)
    print("CSV FILE FORMAT REQUIREMENTS")
    print("="*60)
    print("\nYour CSV file should have these columns:")
    print("  • date        - Date in YYYY-MM-DD format (required)")
    print("  • category    - Expense category (required)")
    print("  • subcategory - Specific expense type (optional)")
    print("  • amount      - Amount as a number (required)")
    print("  • description - What was purchased (optional)")
    print("  • payment_method - How you paid (optional)")
    print("\nExample CSV content:")
    print("-" * 60)
    print("date,category,subcategory,amount,description,payment_method")
    print("2024-01-15,Food & Dining,Restaurant,25.50,Lunch at cafe,Credit Card")
    print("2024-01-16,Transportation,Gas/Fuel,45.00,Gas station,Debit Card")
    print("2024-01-17,Shopping,Clothing,89.99,New shoes,Credit Card")
    print("-" * 60)
    print()


def get_data_info(expenses):
    """
    Get basic information about loaded data.

    Parameters:
    -----------
    expenses : list
        List of expense dictionaries

    Returns:
    --------
    dict : Information about the data
    """
    if not expenses:
        return None

    # Get date range
    dates = [datetime.strptime(e['date'], '%Y-%m-%d') for e in expenses]

    # Get unique categories
    categories = set(e['category'] for e in expenses)

    # Get unique payment methods
    payment_methods = set(e['payment_method'] for e in expenses)

    # Calculate total
    total = sum(e['amount'] for e in expenses)

    info = {
        'total_records': len(expenses),
        'date_range': {
            'start': min(dates).strftime('%Y-%m-%d'),
            'end': max(dates).strftime('%Y-%m-%d')
        },
        'total_amount': total,
        'categories': sorted(list(categories)),
        'payment_methods': sorted(list(payment_methods))
    }

    return info


# Test function
if __name__ == "__main__":
    print("Data Loader Module Test")
    print("-" * 30)
    display_sample_csv_format()
    print("\nThis module is ready to load CSV data!")