"""
Data Cleaner Module
===================
This module handles cleaning and preprocessing expense data.
"""

from datetime import datetime
import pandas as pd


def clean_expense_data(expenses):
    """
    Clean and validate expense data.

    Parameters:
    -----------
    expenses : list
        List of expense dictionaries

    Returns:
    --------
    tuple : (cleaned_data, cleaning_report)
    """
    if not expenses:
        return [], {"error": "No data to clean"}

    # Convert to DataFrame for easier processing
    df = pd.DataFrame(expenses)

    cleaning_report = {
        "original_count": len(df),
        "duplicates_removed": 0,
        "invalid_dates": 0,
        "negative_amounts": 0,
        "empty_categories": 0,
        "final_count": 0
    }

    # Track initial count
    initial_count = len(df)

    # 1. Remove duplicates
    if 'date' in df.columns and 'category' in df.columns and 'amount' in df.columns:
        df = df.drop_duplicates(subset=['date', 'category', 'amount'], keep='first')
        cleaning_report["duplicates_removed"] = initial_count - len(df)

    # 2. Remove rows with invalid dates
    invalid_dates = []
    for idx, row in df.iterrows():
        try:
            datetime.strptime(str(row['date']), '%Y-%m-%d')
        except:
            invalid_dates.append(idx)

    df = df.drop(index=invalid_dates)
    cleaning_report["invalid_dates"] = len(invalid_dates)

    # 3. Remove negative or zero amounts
    df = df[pd.to_numeric(df['amount'], errors='coerce') > 0]
    cleaning_report["negative_amounts"] = cleaning_report["original_count"] - cleaning_report["duplicates_removed"] - len(df) - cleaning_report["invalid_dates"]

    # 4. Fill empty categories with 'Other'
    df['category'] = df['category'].fillna('Other')
    df.loc[df['category'].str.strip() == '', 'category'] = 'Other'
    cleaning_report["empty_categories"] = len(df[df['category'] == 'Other'])

    # 5. Standardize category names (capitalize properly)
    df['category'] = df['category'].str.strip().str.title()

    # 6. Standardize payment methods
    df['payment_method'] = df['payment_method'].fillna('Other')
    df['payment_method'] = df['payment_method'].str.strip()

    # Sort by date
    df = df.sort_values('date')

    # Convert back to list of dictionaries
    cleaned_data = df.to_dict('records')

    cleaning_report["final_count"] = len(cleaned_data)

    return cleaned_data, cleaning_report


def handle_missing_values(expenses):
    """
    Handle missing values in expense data.

    Parameters:
    -----------
    expenses : list
        List of expense dictionaries

    Returns:
    --------
    list : Data with missing values handled
    """
    for expense in expenses:
        # Fill missing subcategory with 'General'
        if 'subcategory' not in expense or not expense['subcategory']:
            expense['subcategory'] = 'General'

        # Fill missing description with 'No description'
        if 'description' not in expense or not expense['description']:
            expense['description'] = 'No description'

        # Fill missing payment_method with 'Other'
        if 'payment_method' not in expense or not expense['payment_method']:
            expense['payment_method'] = 'Other'

        # Ensure amount is a number
        try:
            expense['amount'] = float(expense['amount'])
        except:
            expense['amount'] = 0.0

    return expenses


def standardize_categories(expenses):
    """
    Normalize category names for consistent analysis.

    Parameters:
    -----------
    expenses : list
        List of expense dictionaries

    Returns:
    --------
    list : Data with standardized categories
    """
    # Category mapping for standardization
    category_mapping = {
        'food': 'Food & Dining',
        'food & dining': 'Food & Dining',
        'food and dining': 'Food & Dining',
        'groceries': 'Food & Dining',
        'restaurants': 'Food & Dining',
        'transport': 'Transportation',
        'transportation': 'Transportation',
        'travel': 'Transportation',
        'commute': 'Transportation',
        'shopping': 'Shopping',
        'retail': 'Shopping',
        'clothes': 'Shopping',
        'bills': 'Bills & Utilities',
        'bills & utilities': 'Bills & Utilities',
        'bills and utilities': 'Bills & Utilities',
        'utilities': 'Bills & Utilities',
        'rent': 'Bills & Utilities',
        'entertainment': 'Entertainment',
        'fun': 'Entertainment',
        'healthcare': 'Healthcare',
        'health': 'Healthcare',
        'medical': 'Healthcare',
        'education': 'Education',
        'learning': 'Education',
        'other': 'Other',
        'misc': 'Other',
        'miscellaneous': 'Other'
    }

    for expense in expenses:
        category = expense.get('category', '').lower().strip()

        if category in category_mapping:
            expense['category'] = category_mapping[category]
        else:
            # Capitalize first letter of each word
            expense['category'] = expense['category'].title()

    return expenses


def validate_data(expenses):
    """
    Validate expense data before processing.

    Parameters:
    -----------
    expenses : list
        List of expense dictionaries

    Returns:
    --------
    tuple : (is_valid, validation_errors)
    """
    validation_errors = []

    if not expenses:
        validation_errors.append("No expense records provided")
        return False, validation_errors

    # Check required fields
    required_fields = ['date', 'category', 'amount']

    for idx, expense in enumerate(expenses):
        for field in required_fields:
            if field not in expense or not expense[field]:
                validation_errors.append(f"Row {idx + 1}: Missing required field '{field}'")

        # Validate amount is positive
        try:
            if float(expense.get('amount', 0)) <= 0:
                validation_errors.append(f"Row {idx + 1}: Amount must be positive")
        except ValueError:
            validation_errors.append(f"Row {idx + 1}: Invalid amount format")

    is_valid = len(validation_errors) == 0

    return is_valid, validation_errors


def print_cleaning_report(cleaning_report):
    """
    Print a formatted cleaning report.

    Parameters:
    -----------
    cleaning_report : dict
        Report from clean_expense_data
    """
    print("\n" + "=" * 50)
    print("DATA CLEANING REPORT")
    print("=" * 50)
    print(f"Original records:     {cleaning_report['original_count']}")
    print(f"Duplicates removed:   {cleaning_report['duplicates_removed']}")
    print(f"Invalid dates:        {cleaning_report['invalid_dates']}")
    print(f"Negative amounts:     {cleaning_report['negative_amounts']}")
    print(f"Empty categories:     {cleaning_report['empty_categories']}")
    print(f"Final valid records:  {cleaning_report['final_count']}")
    print("=" * 50)


# Test function
if __name__ == "__main__":
    print("Data Cleaner Module Test")
    print("-" * 30)

    # Test with sample data (includes payment_method for full coverage)
    sample_data = [
        {'date': '2024-01-15', 'category': 'food', 'amount': 25.50, 'description': 'Lunch', 'payment_method': 'Credit Card'},
        {'date': '2024-01-15', 'category': 'food', 'amount': 25.50, 'description': 'Lunch', 'payment_method': 'Credit Card'},  # duplicate
        {'date': '2024-01-16', 'category': 'Transportation', 'amount': 45.00, 'description': 'Gas', 'payment_method': 'Debit Card'},
        {'date': '2024-01-17', 'category': 'Shopping', 'amount': 89.99, 'description': '', 'payment_method': 'Cash'},  # empty description
    ]

    cleaned, report = clean_expense_data(sample_data)
    print_cleaning_report(report)
    print(f"\nCleaned {len(cleaned)} records")