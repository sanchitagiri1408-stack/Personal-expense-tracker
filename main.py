"""
Personal Expense Tracker with Data Visualization
=================================================
Main entry point for the application.

This script orchestrates the entire expense tracking pipeline:
1. Generate or load expense data
2. Clean and validate the data
3. Analyze spending patterns
4. Visualize results
5. Generate reports

Usage:
    python main.py                    # Run full pipeline with synthetic data
    python main.py --file data.csv    # Run with your own CSV file
    python main.py --records 500      # Generate specific number of records
"""

import argparse
import os
import sys
from datetime import datetime

# Local module imports
from data_generator import generate_synthetic_data, save_to_csv
from data_loader import load_csv_data, display_sample_csv_format, get_data_info
from data_cleaner import clean_expense_data, standardize_categories, validate_data, print_cleaning_report
from analyzer import run_full_analysis
from visualizer import (
    plot_category_pie_chart,
    plot_monthly_bar_chart,
    plot_trend_line,
    plot_payment_breakdown,
    create_dashboard,
    close_all_figures
)
from report_generator import generate_full_report, generate_summary_report


def print_banner():
    """Print application banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        PERSONAL EXPENSE TRACKER WITH DATA VISUALIZATION      ║
║                                                              ║
║        A Complete Data Analysis Pipeline for Expenses        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_menu():
    """Print interactive menu options."""
    print("\n" + "=" * 60)
    print("MAIN MENU")
    print("=" * 60)
    print("1. Generate synthetic data and run full analysis")
    print("2. Load data from CSV file")
    print("3. View sample CSV format")
    print("4. Generate full report (data + charts + text)")
    print("5. Quick statistics only")
    print("6. Exit")
    print("=" * 60)


def get_user_choice():
    """Get and validate user menu choice."""
    while True:
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return int(choice)
            else:
                print("Please enter a number between 1 and 6.")
        except (ValueError, EOFError):
            print("Invalid input. Please enter a number.")


def generate_data_option():
    """Handle option 1: Generate synthetic data."""
    print("\n" + "-" * 60)
    print("GENERATING SYNTHETIC EXPENSE DATA")
    print("-" * 60)

    # Get number of records from user
    while True:
        try:
            num_records = input("Enter number of records to generate (default 365): ").strip()
            num_records = int(num_records) if num_records else 365
            if num_records < 10:
                print("Please enter at least 10 records.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    # Generate data
    print(f"\nGenerating {num_records} expense records...")
    expenses = generate_synthetic_data(num_records=num_records)

    # Save to CSV
    csv_path = 'sample_expenses.csv'
    save_to_csv(expenses, csv_path)

    return expenses


def load_data_option():
    """Handle option 2: Load data from CSV."""
    print("\n" + "-" * 60)
    print("LOADING DATA FROM CSV FILE")
    print("-" * 60)

    display_sample_csv_format()

    filepath = input("Enter CSV file path (or press Enter for 'sample_expenses.csv'): ").strip()
    if not filepath:
        filepath = 'sample_expenses.csv'

    try:
        expenses = load_csv_data(filepath)
        print(f"\n✓ Successfully loaded {len(expenses)} records from {filepath}")

        # Show data info
        info = get_data_info(expenses)
        if info:
            print(f"\nData Summary:")
            print(f"  Date range: {info['date_range']['start']} to {info['date_range']['end']}")
            print(f"  Total amount: ${info['total_amount']:,.2f}")
            print(f"  Categories: {', '.join(info['categories'])}")

        return expenses

    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        return None
    except ValueError as e:
        print(f"\n✗ Error: {e}")
        return None


def clean_and_analyze(expenses):
    """Clean data and run analysis."""
    if not expenses:
        print("No expense data provided!")
        return None

    print("\n" + "-" * 60)
    print("CLEANING DATA")
    print("-" * 60)

    # Clean the data
    cleaned_expenses, cleaning_report = clean_expense_data(expenses)
    print_cleaning_report(cleaning_report)

    # Standardize categories
    cleaned_expenses = standardize_categories(cleaned_expenses)

    # Validate data
    is_valid, errors = validate_data(cleaned_expenses)
    if not is_valid:
        print("\n⚠ Validation warnings:")
        for error in errors[:5]:  # Show first 5 errors
            print(f"  • {error}")

    print("\n" + "-" * 60)
    print("RUNNING ANALYSIS")
    print("-" * 60)

    # Run full analysis
    analysis = run_full_analysis(cleaned_expenses)

    # Display key findings
    print("\n📊 ANALYSIS RESULTS")
    print("-" * 40)

    stats = analysis['statistics']
    print(f"Total Spending:      ${stats['total_spending']:>15,.2f}")
    print(f"Total Transactions:  {stats['total_transactions']:>15}")
    print(f"Average per Txn:     ${stats['average_per_transaction']:>15,.2f}")
    print(f"Median Transaction:  ${stats['median_transaction']:>15,.2f}")
    print(f"Daily Average:       ${stats['daily_average']:>15,.2f}")

    print(f"\n📅 PERIOD COVERED")
    print("-" * 40)
    print(f"Start Date:  {stats['date_range']['start']}")
    print(f"End Date:    {stats['date_range']['end']}")
    print(f"Total Days:  {stats['date_range']['days']}")

    print(f"\n💰 TOP 5 CATEGORIES")
    print("-" * 40)
    sorted_cats = sorted(analysis['by_category'].items(),
                        key=lambda x: x[1]['total'], reverse=True)[:5]
    for i, (category, data) in enumerate(sorted_cats, 1):
        print(f"{i}. {category:20} ${data['total']:>10,.2f} ({data['percentage']:>5.1f}%)")

    print(f"\n💳 PAYMENT METHODS")
    print("-" * 40)
    sorted_payments = sorted(analysis['payment_methods'].items(),
                            key=lambda x: x[1]['total'], reverse=True)
    for method, data in sorted_payments:
        print(f"{method:20} ${data['total']:>10,.2f} ({data['percentage']:>5.1f}%)")

    return analysis


def visualize_data(analysis):
    """Create all visualizations."""
    if not analysis:
        print("No analysis data to visualize!")
        return

    print("\n" + "-" * 60)
    print("CREATING VISUALIZATIONS")
    print("-" * 60)

    # Create individual charts
    plot_category_pie_chart(analysis['by_category'], 'category_pie_chart.png')
    plot_monthly_bar_chart(analysis['monthly_trends'], 'monthly_bar_chart.png')
    plot_trend_line(analysis['monthly_trends'], 'trend_line_chart.png')
    plot_payment_breakdown(analysis['payment_methods'], 'payment_breakdown.png')

    # Create dashboard
    create_dashboard(analysis, 'expense_dashboard.png')

    # Close all figures
    close_all_figures()

    print("\n✓ All visualizations created successfully!")
    print("  Check the 'charts' folder for all PNG files.")


def generate_reports(expenses, analysis):
    """Generate text reports and CSV export."""
    if not expenses:
        print("No expense data to report on!")
        return

    print("\n" + "-" * 60)
    print("GENERATING REPORTS")
    print("-" * 60)

    # Generate full report
    files = generate_full_report(expenses, 'expense_report')

    if files:
        print("\n📁 Generated files:")
        for key, path in files.items():
            print(f"  ✓ {key}: {path}")


def run_full_pipeline(num_records=365):
    """Run the complete analysis pipeline."""
    print_banner()

    print(f"\nStarting full pipeline with {num_records} records...")

    # Step 1: Generate synthetic data
    print("\n[1/5] Generating synthetic data...")
    expenses = generate_synthetic_data(num_records=num_records)
    print(f"✓ Generated {len(expenses)} records")

    # Step 2: Clean data
    print("\n[2/5] Cleaning data...")
    cleaned_expenses, cleaning_report = clean_expense_data(expenses)
    print_cleaning_report(cleaning_report)
    cleaned_expenses = standardize_categories(cleaned_expenses)
    print(f"✓ Data cleaned and standardized")

    # Step 3: Analyze data
    print("\n[3/5] Analyzing data...")
    analysis = run_full_analysis(cleaned_expenses)
    print(f"✓ Analysis complete")

    # Step 4: Create visualizations
    print("\n[4/5] Creating visualizations...")
    plot_category_pie_chart(analysis['by_category'], 'category_pie_chart.png')
    plot_monthly_bar_chart(analysis['monthly_trends'], 'monthly_bar_chart.png')
    plot_trend_line(analysis['monthly_trends'], 'trend_line_chart.png')
    plot_payment_breakdown(analysis['payment_methods'], 'payment_breakdown.png')
    create_dashboard(analysis, 'expense_dashboard.png')
    close_all_figures()
    print(f"✓ Visualizations created")

    # Step 5: Generate reports
    print("\n[5/5] Generating reports...")
    files = generate_full_report(cleaned_expenses, 'expense_report')
    print(f"✓ Reports generated")

    # Summary
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE!")
    print("=" * 60)
    print(f"\nGenerated files:")
    if files:
        for key, path in files.items():
            print(f"  • {path}")

    print(f"\n📊 Quick Summary:")
    print(f"  Total Spending:     ${analysis['statistics']['total_spending']:,.2f}")
    print(f"  Total Transactions: {analysis['statistics']['total_transactions']}")
    print(f"  Average per Txn:    ${analysis['statistics']['average_per_transaction']:,.2f}")
    print(f"  Top Category:       {list(analysis['by_category'].keys())[0]}")

    return analysis


def interactive_mode():
    """Run interactive menu mode."""
    print_banner()

    expenses = None
    analysis = None

    while True:
        print_menu()
        choice = get_user_choice()

        if choice == 1:
            expenses = generate_data_option()
            if expenses:
                analysis = clean_and_analyze(expenses)

        elif choice == 2:
            expenses = load_data_option()
            if expenses:
                analysis = clean_and_analyze(expenses)

        elif choice == 3:
            display_sample_csv_format()

        elif choice == 4:
            if expenses is None:
                print("\n⚠ No data loaded. Please generate or load data first (options 1 or 2).")
            else:
                generate_reports(expenses, analysis)

        elif choice == 5:
            if analysis is None:
                print("\n⚠ No analysis available. Please generate or load data first (options 1 or 2).")
            else:
                print("\n" + generate_summary_report(analysis))

        elif choice == 6:
            print("\nThank you for using Personal Expense Tracker!")
            print("Goodbye! 👋")
            break


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Personal Expense Tracker with Data Visualization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Run full pipeline with 365 records
  python main.py --records 500            # Generate 500 records
  python main.py --file my_expenses.csv   # Load from CSV file
  python main.py --interactive            # Run interactive menu mode
        """
    )

    parser.add_argument('--file', '-f', type=str, help='Path to CSV file with expense data')
    parser.add_argument('--records', '-r', type=int, default=365, help='Number of synthetic records to generate (default: 365)')
    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive menu mode')
    parser.add_argument('--quick', '-q', action='store_true', help='Run quick analysis (no charts)')

    args = parser.parse_args()

    # Interactive mode
    if args.interactive:
        interactive_mode()
        return

    # Quick mode (statistics only)
    if args.quick:
        print_banner()
        print("\nRunning quick analysis (no charts)...")

        if args.file:
            expenses = load_csv_data(args.file)
        else:
            expenses = generate_synthetic_data(num_records=args.records)
            print(f"✓ Generated {len(expenses)} records")

        analysis = clean_and_analyze(expenses)
        return

    # File mode
    if args.file:
        print_banner()
        print(f"\nLoading data from: {args.file}")

        try:
            expenses = load_csv_data(args.file)
            analysis = clean_and_analyze(expenses)
            visualize_data(analysis)
            generate_reports(expenses, analysis)
        except Exception as e:
            print(f"\n✗ Error: {e}")
            sys.exit(1)
        return

    # Default: full pipeline with synthetic data
    run_full_pipeline(num_records=args.records)


if __name__ == "__main__":
    main()