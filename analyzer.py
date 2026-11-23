"""
Analyzer Module
===============
This module performs various analysis on expense data.
"""

from datetime import datetime
import pandas as pd
import numpy as np
from collections import defaultdict


def analyze_by_category(expenses):
    """
    Analyze spending by category.

    Parameters:
    -----------
    expenses : list
        List of expense dictionaries

    Returns:
    --------
    dict : Category-wise spending breakdown
    """
    if not expenses:
        return {}

    df = pd.DataFrame(expenses)

    # Group by category and sum amounts
    category_totals = df.groupby('category')['amount'].sum().sort_values(ascending=False)

    # Calculate percentages
    total = category_totals.sum()
    category_percentages = (category_totals / total * 100).round(2)

    # Build result dictionary
    result = {}
    for category in category_totals.index:
        result[category] = {
            'total': round(category_totals[category], 2),
            'percentage': round(category_percentages[category], 2)
        }

    return result


def analyze_by_subcategory(expenses):
    """
    Analyze spending by subcategory within each main category.

    Parameters:
    -----------
    expenses : list
        List of expense dictionaries

    Returns:
    --------
    dict : Nested category-subcategory breakdown
    """
    if not expenses:
        return {}

    df = pd.DataFrame(expenses)

    # Group by category and subcategory
    subcategory_totals = df.groupby(['category', 'subcategory'])['amount'].sum()

    # Build result dictionary
    result = {}
    for (category, subcategory), amount in subcategory_totals.items():
        if category not in result:
            result[category] = {}

        result[category][subcategory] = round(amount, 2)

    return result


def analyze_monthly_trends(expenses):
    """
    Analyze spending patterns by month.

    Parameters:
    -----------
    expenses : list
        List of expense dictionaries

    Returns:
    --------
    dict : Monthly spending breakdown
    """
    if not expenses:
        return {}

    df = pd.DataFrame(expenses)
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M')

    # Monthly totals
    monthly_totals = df.groupby('month')['amount'].sum()

    # Transaction count per month
    monthly_counts = df.groupby('month').size()

    # Average transaction per month
    monthly_avg = df.groupby('month')['amount'].mean()

    result = {}
    for month in monthly_totals.index:
        month_str = str(month)
        result[month_str] = {
            'total': round(monthly_totals[month], 2),
            'count': int(monthly_counts[month]),
            'average': round(monthly_avg[month], 2)
        }

    return result


def analyze_yearly_summary(expenses):
    """
    Get yearly spending summary.

    Parameters:
    -----------
    expenses : list
        List of expense dictionaries

    Returns:
    --------
    dict : Year-level summary statistics
    """
    if not expenses:
        return {}

    df = pd.DataFrame(expenses)
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year

    yearly_totals = df.groupby('year')['amount'].agg(['sum', 'count', 'mean', 'min', 'max'])

    result = {}
    for year in yearly_totals.index:
        result[int(year)] = {
            'total': round(yearly_totals.loc[year, 'sum'], 2),
            'count': int(yearly_totals.loc[year, 'count']),
            'average': round(yearly_totals.loc[year, 'mean'], 2),
            'min': round(yearly_totals.loc[year, 'min'], 2),
            'max': round(yearly_totals.loc[year, 'max'], 2)
        }

    return result


def analyze_payment_methods(expenses):
    """
    Analyze spending by payment method.

    Parameters:
    -----------
    expenses : list
        List of expense dictionaries

    Returns:
    --------
    dict : Payment method breakdown
    """
    if not expenses:
        return {}

    df = pd.DataFrame(expenses)

    # Group by payment method
    payment_totals = df.groupby('payment_method')['amount'].sum().sort_values(ascending=False)

    # Calculate percentages
    total = payment_totals.sum()
    payment_percentages = (payment_totals / total * 100).round(2)

    # Transaction count
    payment_counts = df.groupby('payment_method').size()

    result = {}
    for method in payment_totals.index:
        result[method] = {
            'total': round(payment_totals[method], 2),
            'percentage': round(payment_percentages[method], 2),
            'count': int(payment_counts[method])
        }

    return result


def calculate_overall_statistics(expenses):
    """
    Calculate overall statistics for the expense data.

    Parameters:
    -----------
    expenses : list
        List of expense dictionaries

    Returns:
    --------
    dict : Overall statistics
    """
    if not expenses:
        return {}

    df = pd.DataFrame(expenses)
    df['date'] = pd.to_datetime(df['date'])

    amounts = df['amount'].astype(float)

    total = amounts.sum()
    count = len(amounts)
    average = amounts.mean()
    median = amounts.median()
    minimum = amounts.min()
    maximum = amounts.max()
    std_dev = amounts.std()

    # Date range
    date_min = df['date'].min()
    date_max = df['date'].max()

    # Daily average
    days = (date_max - date_min).days + 1
    daily_average = total / days if days > 0 else 0

    # Monthly average (approximate)
    monthly_average = total / 12 if count >= 12 else (total / (days / 30))

    return {
        'total_spending': round(total, 2),
        'total_transactions': count,
        'average_per_transaction': round(average, 2),
        'median_transaction': round(median, 2),
        'minimum_transaction': round(minimum, 2),
        'maximum_transaction': round(maximum, 2),
        'standard_deviation': round(std_dev, 2),
        'date_range': {
            'start': date_min.strftime('%Y-%m-%d'),
            'end': date_max.strftime('%Y-%m-%d'),
            'days': days
        },
        'daily_average': round(daily_average, 2),
        'monthly_average': round(monthly_average, 2)
    }


def find_top_expenses(expenses, n=10):
    """
    Find the top N largest expenses.

    Parameters:
    -----------
    expenses : list
        List of expense dictionaries
    n : int
        Number of top expenses to return (default: 10)

    Returns:
    --------
    list : Top N expenses sorted by amount descending
    """
    if not expenses:
        return []

    df = pd.DataFrame(expenses)
    df = df.nlargest(n, 'amount')

    return df.to_dict('records')


def analyze_daily_patterns(expenses):
    """
    Analyze spending patterns by day of week.

    Parameters:
    -----------
    expenses : list
        List of expense dictionaries

    Returns:
    --------
    dict : Day-of-week spending breakdown
    """
    if not expenses:
        return {}

    df = pd.DataFrame(expenses)
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.day_name()

    day_totals = df.groupby('day_of_week')['amount'].sum()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    result = {}
    for day in day_order:
        if day in day_totals.index:
            result[day] = {
                'total': round(day_totals[day], 2),
                'percentage': round(day_totals[day] / day_totals.sum() * 100, 2)
            }
        else:
            result[day] = {'total': 0, 'percentage': 0}

    return result


def run_full_analysis(expenses):
    """
    Run complete analysis on expense data.

    Parameters:
    -----------
    expenses : list
        List of expense dictionaries

    Returns:
    --------
    dict : Complete analysis results
    """
    if not expenses or len(expenses) == 0:
        return {"error": "No expense data provided"}

    analysis = {
        'statistics': calculate_overall_statistics(expenses),
        'by_category': analyze_by_category(expenses),
        'by_subcategory': analyze_by_subcategory(expenses),
        'monthly_trends': analyze_monthly_trends(expenses),
        'yearly_summary': analyze_yearly_summary(expenses),
        'payment_methods': analyze_payment_methods(expenses),
        'daily_patterns': analyze_daily_patterns(expenses),
        'top_expenses': find_top_expenses(expenses, n=10)
    }

    return analysis


# Test function
if __name__ == "__main__":
    print("Analyzer Module Test")
    print("-" * 30)

    # Import data generator for testing
    from data_generator import generate_synthetic_data

    # Generate sample data
    sample_expenses = generate_synthetic_data(num_records=50)

    # Run analysis
    analysis = run_full_analysis(sample_expenses)

    print(f"Total spending: ${analysis['statistics']['total_spending']:,.2f}")
    print(f"Total transactions: {analysis['statistics']['total_transactions']}")
    print(f"Average per transaction: ${analysis['statistics']['average_per_transaction']:,.2f}")
    print(f"\nCategories: {list(analysis['by_category'].keys())[:3]}...")
    print(f"\nMonthly trends: {len(analysis['monthly_trends'])} months of data")