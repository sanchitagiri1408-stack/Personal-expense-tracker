"""
Report Generator Module
=======================
This module generates comprehensive expense reports.
"""

import os
from datetime import datetime
from analyzer import run_full_analysis
from visualizer import (
    plot_category_pie_chart,
    plot_monthly_bar_chart,
    plot_trend_line,
    plot_payment_breakdown,
    create_dashboard,
    close_all_figures
)


def ensure_output_directory():
    """Create output directory if it doesn't exist."""
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def generate_summary_report(analysis_results):
    """
    Generate a text summary of expense analysis.

    Parameters:
    -----------
    analysis_results : dict
        Complete analysis results

    Returns:
    --------
    str : Formatted summary report
    """
    if not analysis_results:
        return "No analysis results provided"

    stats = analysis_results.get('statistics', {})
    by_category = analysis_results.get('by_category', {})
    by_month = analysis_results.get('monthly_trends', {})
    by_payment = analysis_results.get('payment_methods', {})

    report = []
    report.append("=" * 60)
    report.append("PERSONAL EXPENSE TRACKER - SUMMARY REPORT")
    report.append("=" * 60)
    report.append(f"\nReport Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("-" * 60)

    # Overall Statistics (right-aligned values, $ glued to number)
    report.append("\n📊 OVERALL STATISTICS")
    report.append("-" * 40)
    report.append(f"Total Spending:      ${stats.get('total_spending', 0):>12,.2f}")
    report.append(f"Total Transactions:  {stats.get('total_transactions', 0):>13}")
    report.append(f"Average per Txn:     ${stats.get('average_per_transaction', 0):>12,.2f}")
    report.append(f"Median Transaction:  ${stats.get('median_transaction', 0):>12,.2f}")
    report.append(f"Minimum Transaction: ${stats.get('minimum_transaction', 0):>12,.2f}")
    report.append(f"Maximum Transaction: ${stats.get('maximum_transaction', 0):>12,.2f}")
    report.append(f"Daily Average:       ${stats.get('daily_average', 0):>12,.2f}")
    report.append(f"Monthly Average:     ${stats.get('monthly_average', 0):>12,.2f}")

    # Date Range
    date_range = stats.get('date_range', {})
    report.append(f"\n📅 PERIOD COVERED")
    report.append("-" * 40)
    report.append(f"Start Date:  {date_range.get('start', 'N/A')}")
    report.append(f"End Date:    {date_range.get('end', 'N/A')}")
    report.append(f"Total Days:  {date_range.get('days', 'N/A')}")

    # Spending by Category
    report.append("\n💰 SPENDING BY CATEGORY")
    report.append("-" * 40)
    if by_category:
        # Sort by total spending
        sorted_cats = sorted(by_category.items(), key=lambda x: x[1]['total'], reverse=True)
        for category, data in sorted_cats:
            bar_length = int(data['percentage'] / 2)
            bar = "█" * bar_length + "░" * (50 - bar_length)
            report.append(f"{category:20} ${data['total']:>10,.2f} [{data['percentage']:>5.1f}%] {bar}")

    # Monthly Trends
    report.append("\n📈 MONTHLY SPENDING TRENDS")
    report.append("-" * 40)
    if by_month:
        sorted_months = sorted(by_month.keys())
        for month in sorted_months:
            data = by_month[month]
            report.append(f"{month}: ${data['total']:>10,.2f} ({data['count']:>3} transactions)")

    # Payment Methods
    report.append("\n💳 PAYMENT METHODS")
    report.append("-" * 40)
    if by_payment:
        sorted_methods = sorted(by_payment.items(), key=lambda x: x[1]['total'], reverse=True)
        for method, data in sorted_methods:
            bar_length = int(data['percentage'] / 2)
            bar = "█" * bar_length + "░" * (50 - bar_length)
            report.append(f"{method:20} ${data['total']:>10,.2f} [{data['percentage']:>5.1f}%] {bar}")

    report.append("\n" + "=" * 60)
    report.append("END OF REPORT")
    report.append("=" * 60)

    return "\n".join(report)


def generate_detailed_report(expenses, output_path=None):
    """
    Generate a comprehensive detailed report.

    Parameters:
    -----------
    expenses : list
        List of expense dictionaries
    output_path : str, optional
        Path to save the report

    Returns:
    --------
    str : Detailed report content
    """
    if not expenses:
        return "No expense data provided"

    # Run analysis
    analysis = run_full_analysis(expenses)

    # Generate summary
    report = generate_summary_report(analysis)

    # Add detailed transaction list
    report += f"""

📋 DETAILED TRANSACTION LIST
{"=" * 60}

All Expenses (sorted by date):
{"-" * 60}

"""

    # Group by month
    from collections import defaultdict
    by_date = defaultdict(list)
    for expense in expenses:
        month = expense['date'][:7]  # YYYY-MM
        by_date[month].append(expense)

    # Sort months
    sorted_months = sorted(by_date.keys())

    for month in sorted_months:
        monthly_total = sum(e['amount'] for e in by_date[month])
        report += f"\n{month} - Total: ${monthly_total:,.2f}\n{'-' * 50}\n"

        for expense in sorted(by_date[month], key=lambda x: x['date']):
            report += f"  {expense['date']:10} | {expense['category']:18} | ${expense['amount']:>8.2f} | {expense['description'][:30]}\n"

    # Add top expenses
    top_expenses = analysis.get('top_expenses', [])[:10]
    if top_expenses:
        report += f"""

🔝 TOP 10 LARGEST EXPENSES
{"=" * 60}

"""
        for i, expense in enumerate(top_expenses, 1):
            report += f"{i:2}. ${expense['amount']:>10,.2f} - {expense['category']:18} - {expense['description'][:30]}\n"

    report += f"""

{"=" * 60}
Report generated by Personal Expense Tracker
Data Visualization Project
{"=" * 60}
"""

    # Save to file if path provided
    if output_path:
        output_dir = ensure_output_directory()
        filepath = os.path.join(output_dir, output_path) if not os.path.dirname(output_path) else output_path
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✓ Detailed report saved to: {filepath}")

    return report


def export_to_csv(expenses, output_path='expense_export.csv'):
    """
    Export cleaned expense data to CSV.

    Parameters:
    -----------
    expenses : list
        List of expense dictionaries
    output_path : str
        Output file path

    Returns:
    --------
    str : Path to exported file
    """
    if not expenses:
        print("No expense data to export")
        return None

    output_dir = ensure_output_directory()
    filepath = os.path.join(output_dir, output_path) if not os.path.dirname(output_path) else output_path

    import csv

    fieldnames = ['date', 'category', 'subcategory', 'amount', 'description', 'payment_method']

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)

    print(f"✓ Expenses exported to: {filepath}")
    return filepath


def generate_full_report(expenses, base_filename='expense_report'):
    """
    Generate complete report with all charts and text reports.

    Parameters:
    -----------
    expenses : list
        List of expense dictionaries
    base_filename : str
        Base name for output files

    Returns:
    --------
    dict : Paths to all generated files
    """
    if not expenses:
        print("No expense data provided")
        return None

    print("\n" + "=" * 60)
    print("GENERATING COMPREHENSIVE EXPENSE REPORT")
    print("=" * 60)

    output_dir = ensure_output_directory()
    generated_files = {}

    # Run analysis
    analysis = run_full_analysis(expenses)

    # Generate and save summary report
    summary = generate_summary_report(analysis)
    summary_path = os.path.join(output_dir, f'{base_filename}_summary.txt')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    generated_files['summary_report'] = summary_path
    print(f"✓ Summary report saved to: {summary_path}")

    # Generate and save detailed report
    detailed = generate_detailed_report(expenses)
    detailed_path = os.path.join(output_dir, f'{base_filename}_detailed.txt')
    with open(detailed_path, 'w', encoding='utf-8') as f:
        f.write(detailed)
    generated_files['detailed_report'] = detailed_path
    print(f"✓ Detailed report saved to: {detailed_path}")

    # Export data to CSV
    csv_path = export_to_csv(expenses, f'{base_filename}_data.csv')
    generated_files['csv_export'] = csv_path

    # Generate charts
    print("\n📊 Generating Charts...")

    pie_path = os.path.join(output_dir, f'{base_filename}_category_pie.png')
    plot_category_pie_chart(analysis['by_category'], pie_path)
    generated_files['category_pie_chart'] = pie_path

    bar_path = os.path.join(output_dir, f'{base_filename}_monthly_bar.png')
    plot_monthly_bar_chart(analysis['monthly_trends'], bar_path)
    generated_files['monthly_bar_chart'] = bar_path

    trend_path = os.path.join(output_dir, f'{base_filename}_trend_line.png')
    plot_trend_line(analysis['monthly_trends'], trend_path)
    generated_files['trend_line_chart'] = trend_path

    payment_path = os.path.join(output_dir, f'{base_filename}_payment_breakdown.png')
    plot_payment_breakdown(analysis['payment_methods'], payment_path)
    generated_files['payment_breakdown_chart'] = payment_path

    dashboard_path = os.path.join(output_dir, f'{base_filename}_dashboard.png')
    create_dashboard(analysis, dashboard_path)
    generated_files['dashboard'] = dashboard_path

    # Close all figures to free memory
    close_all_figures()

    print("\n" + "=" * 60)
    print("ALL REPORTS GENERATED SUCCESSFULLY!")
    print("=" * 60)

    return generated_files


# Test function
if __name__ == "__main__":
    print("Report Generator Module Test")
    print("-" * 30)

    # Import data generator for testing
    from data_generator import generate_synthetic_data

    # Generate test data
    test_expenses = generate_synthetic_data(num_records=50)

    # Generate full report
    files = generate_full_report(test_expenses, 'test_expense_report')

    print("\n📁 Generated files:")
    for key, path in files.items():
        print(f"  - {key}: {path}")