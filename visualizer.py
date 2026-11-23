"""
Visualizer Module
=================
This module creates visualizations for expense data analysis.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
from datetime import datetime


# Set style for better-looking plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


def ensure_output_directory():
    """Create output directory if it doesn't exist."""
    output_dir = os.path.join(os.path.dirname(__file__), 'charts')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def format_currency(x, pos):
    """Format axis labels as currency."""
    return f'${x:,.0f}'


def plot_category_pie_chart(category_data, save_path=None, figsize=(10, 8)):
    """
    Create a pie chart showing spending by category.

    Parameters:
    -----------
    category_data : dict
        Category-wise spending data from analyzer
    save_path : str, optional
        Path to save the chart (PNG format)
    figsize : tuple
        Figure size (width, height)

    Returns:
    --------
    matplotlib.figure.Figure : The pie chart figure
    """
    if not category_data:
        print("No category data provided for pie chart")
        return None

    categories = list(category_data.keys())
    totals = [category_data[cat]['total'] for cat in categories]
    percentages = [category_data[cat]['percentage'] for cat in categories]

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Create color palette
    colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))

    # Create pie chart with percentage labels
    wedges, texts, autotexts = ax.pie(
        totals,
        labels=categories,
        autopct=lambda pct: f'{pct:.1f}%\n(${totals[int(pct/100*len(totals))]:,.0f})',
        colors=colors,
        startangle=90,
        explode=[0.02] * len(categories),
        shadow=True,
        textprops={'fontsize': 9}
    )

    # Style the percentage text
    for autotext in autotexts:
        autotext.set_fontsize(8)
        autotext.set_fontweight('bold')

    # Add title
    ax.set_title('Spending by Category', fontsize=14, fontweight='bold', pad=20)

    # Add legend with totals
    legend_labels = [f'{cat}: ${totals[i]:,.2f} ({percentages[i]:.1f}%)'
                     for i, cat in enumerate(categories)]
    ax.legend(wedges, legend_labels, title="Categories", loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1), fontsize=8)

    plt.tight_layout()

    # Save if path provided
    if save_path:
        output_dir = ensure_output_directory()
        filepath = os.path.join(output_dir, save_path) if not os.path.dirname(save_path) else save_path
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"✓ Pie chart saved to: {filepath}")

    return fig


def plot_monthly_bar_chart(monthly_data, save_path=None, figsize=(12, 6)):
    """
    Create a bar chart showing monthly spending trends.

    Parameters:
    -----------
    monthly_data : dict
        Monthly spending data from analyzer
    save_path : str, optional
        Path to save the chart (PNG format)
    figsize : tuple
        Figure size (width, height)

    Returns:
    --------
    matplotlib.figure.Figure : The bar chart figure
    """
    if not monthly_data:
        print("No monthly data provided for bar chart")
        return None

    # Sort months chronologically
    sorted_months = sorted(monthly_data.keys())
    totals = [monthly_data[month]['total'] for month in sorted_months]
    counts = [monthly_data[month]['count'] for month in sorted_months]

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)

    # Create color gradient based on values
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(totals)))

    # Plot total spending
    bars = ax1.bar(range(len(sorted_months)), totals, color=colors, edgecolor='navy', linewidth=0.5)

    # Add value labels on bars
    for bar, total in zip(bars, totals):
        height = bar.get_height()
        ax1.annotate(f'${total:,.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8, fontweight='bold')

    ax1.set_ylabel('Total Spending ($)', fontsize=11)
    ax1.set_title('Monthly Spending Trends', fontsize=14, fontweight='bold', pad=10)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))

    # Plot transaction count
    ax2.bar(range(len(sorted_months)), counts, color=plt.cm.Greens(np.linspace(0.4, 0.9, len(counts))),
            edgecolor='darkgreen', linewidth=0.5)

    # Add value labels on bars
    for i, count in enumerate(counts):
        ax2.annotate(str(count),
                    xy=(i, count),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

    ax2.set_ylabel('Transaction Count', fontsize=11)
    ax2.set_xlabel('Month', fontsize=11)
    ax2.set_xticks(range(len(sorted_months)))
    ax2.set_xticklabels(sorted_months, rotation=45, ha='right')

    plt.tight_layout()

    # Save if path provided
    if save_path:
        output_dir = ensure_output_directory()
        filepath = os.path.join(output_dir, save_path) if not os.path.dirname(save_path) else save_path
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"✓ Monthly bar chart saved to: {filepath}")

    return fig


def plot_trend_line(monthly_data, save_path=None, figsize=(12, 6)):
    """
    Create a line chart showing spending trends over time.

    Parameters:
    -----------
    monthly_data : dict
        Monthly spending data from analyzer
    save_path : str, optional
        Path to save the chart (PNG format)
    figsize : tuple
        Figure size (width, height)

    Returns:
    --------
    matplotlib.figure.Figure : The line chart figure
    """
    if not monthly_data:
        print("No monthly data provided for trend line")
        return None

    # Sort months chronologically
    sorted_months = sorted(monthly_data.keys())
    totals = [monthly_data[month]['total'] for month in sorted_months]

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Plot line chart
    ax.plot(range(len(sorted_months)), totals, marker='o', linewidth=2,
            color='steelblue', markersize=8, markerfacecolor='white',
            markeredgewidth=2, markeredgecolor='steelblue')

    # Add moving average
    if len(totals) >= 3:
        moving_avg = np.convolve(totals, np.ones(3)/3, mode='valid')
        ax.plot(range(2, len(totals)), moving_avg, linestyle='--', linewidth=2,
                color='orange', label='3-Month Moving Avg')
        ax.legend()

    # Add value labels
    for i, (month, total) in enumerate(zip(sorted_months, totals)):
        ax.annotate(f'${total:,.0f}',
                   xy=(i, total),
                   xytext=(0, 10),
                   textcoords="offset points",
                   ha='center', va='bottom', fontsize=8, fontweight='bold')

    ax.set_xticks(range(len(sorted_months)))
    ax.set_xticklabels(sorted_months, rotation=45, ha='right')
    ax.set_xlabel('Month', fontsize=11)
    ax.set_ylabel('Total Spending ($)', fontsize=11)
    ax.set_title('Spending Trend Over Time', fontsize=14, fontweight='bold', pad=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    # Save if path provided
    if save_path:
        output_dir = ensure_output_directory()
        filepath = os.path.join(output_dir, save_path) if not os.path.dirname(save_path) else save_path
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"✓ Trend line chart saved to: {filepath}")

    return fig


def plot_payment_breakdown(payment_data, save_path=None, figsize=(10, 6)):
    """
    Create a horizontal bar chart showing spending by payment method.

    Parameters:
    -----------
    payment_data : dict
        Payment method data from analyzer
    save_path : str, optional
        Path to save the chart (PNG format)
    figsize : tuple
        Figure size (width, height)

    Returns:
    --------
    matplotlib.figure.Figure : The horizontal bar chart figure
    """
    if not payment_data:
        print("No payment data provided for breakdown chart")
        return None

    methods = list(payment_data.keys())
    totals = [payment_data[method]['total'] for method in methods]
    percentages = [payment_data[method]['percentage'] for method in methods]
    counts = [payment_data[method]['count'] for method in methods]

    # Sort by total spending
    sorted_indices = np.argsort(totals)[::-1]
    methods = [methods[i] for i in sorted_indices]
    totals = [totals[i] for i in sorted_indices]
    percentages = [percentages[i] for i in sorted_indices]
    counts = [counts[i] for i in sorted_indices]

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Create horizontal bar chart
    y_pos = np.arange(len(methods))
    colors = plt.cm.Pastel1(np.linspace(0, 1, len(methods)))

    bars = ax.barh(y_pos, totals, color=colors, edgecolor='gray', linewidth=0.5)

    # Add value labels
    for i, (bar, total, pct, count) in enumerate(zip(bars, totals, percentages, counts)):
        ax.annotate(f'${total:,.0f} ({pct:.1f}%) - {count} transactions',
                   xy=(bar.get_width(), bar.get_y() + bar.get_height()/2),
                   xytext=(5, 0),
                   textcoords="offset points",
                   ha='left', va='center', fontsize=9)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(methods)
    ax.set_xlabel('Total Spending ($)', fontsize=11)
    ax.set_ylabel('Payment Method', fontsize=11)
    ax.set_title('Spending by Payment Method', fontsize=14, fontweight='bold', pad=10)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    ax.invert_yaxis()  # Highest at top

    plt.tight_layout()

    # Save if path provided
    if save_path:
        output_dir = ensure_output_directory()
        filepath = os.path.join(output_dir, save_path) if not os.path.dirname(save_path) else save_path
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"✓ Payment breakdown chart saved to: {filepath}")

    return fig


def plot_category_comparison(categories, totals, save_path=None, figsize=(12, 6)):
    """
    Create a comparison bar chart for categories.

    Parameters:
    -----------
    categories : list
        List of category names
    totals : list
        List of total amounts
    save_path : str, optional
        Path to save the chart (PNG format)
    figsize : tuple
        Figure size (width, height)

    Returns:
    --------
    matplotlib.figure.Figure : The comparison chart figure
    """
    if not categories or not totals:
        print("No data provided for comparison chart")
        return None

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Sort by total
    sorted_indices = np.argsort(totals)[::-1]
    categories = [categories[i] for i in sorted_indices]
    totals = [totals[i] for i in sorted_indices]

    # Create color gradient
    colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(categories)))

    bars = ax.bar(categories, totals, color=colors, edgecolor='black', linewidth=0.5)

    # Add value labels
    for bar, total in zip(bars, totals):
        height = bar.get_height()
        ax.annotate(f'${total:,.0f}',
                   xy=(bar.get_x() + bar.get_width() / 2, height),
                   xytext=(0, 3),
                   textcoords="offset points",
                   ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_xlabel('Category', fontsize=11)
    ax.set_ylabel('Total Spending ($)', fontsize=11)
    ax.set_title('Category-wise Spending Comparison', fontsize=14, fontweight='bold', pad=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()

    # Save if path provided
    if save_path:
        output_dir = ensure_output_directory()
        filepath = os.path.join(output_dir, save_path) if not os.path.dirname(save_path) else save_path
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"✓ Comparison chart saved to: {filepath}")

    return fig


def create_dashboard(analysis_results, save_path=None):
    """
    Create a comprehensive dashboard with multiple charts.

    Parameters:
    -----------
    analysis_results : dict
        Complete analysis results from analyzer
    save_path : str, optional
        Base path to save charts (PNG format)

    Returns:
    --------
    matplotlib.figure.Figure : The dashboard figure
    """
    if not analysis_results:
        print("No analysis results provided for dashboard")
        return None

    # Create figure with subplots (constrained_layout avoids tight_layout warnings)
    fig = plt.figure(figsize=(16, 12), constrained_layout=True)

    # Define grid
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.25)

    # 1. Pie chart - Spending by Category
    ax1 = fig.add_subplot(gs[0, 0])
    if 'by_category' in analysis_results:
        category_data = analysis_results['by_category']
        categories = list(category_data.keys())
        totals = [category_data[cat]['total'] for cat in categories]
        colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
        wedges, texts, autotexts = ax1.pie(totals, labels=None, colors=colors, autopct='%1.1f%%',
                                           startangle=90, textprops={'fontsize': 8})
        ax1.set_title('Spending by Category', fontsize=12, fontweight='bold')
        ax1.legend(wedges, categories, loc='upper right', fontsize=7)

    # 2. Bar chart - Monthly Trends
    ax2 = fig.add_subplot(gs[0, 1])
    if 'monthly_trends' in analysis_results:
        monthly_data = analysis_results['monthly_trends']
        sorted_months = sorted(monthly_data.keys())
        totals = [monthly_data[month]['total'] for month in sorted_months]
        ax2.bar(range(len(sorted_months)), totals, color='steelblue', edgecolor='navy')
        ax2.set_xticks(range(len(sorted_months)))
        ax2.set_xticklabels(sorted_months, rotation=45, ha='right', fontsize=7)
        ax2.set_ylabel('Total ($)', fontsize=10)
        ax2.set_title('Monthly Spending', fontsize=12, fontweight='bold')
        ax2.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))

    # 3. Line chart - Trend Over Time
    ax3 = fig.add_subplot(gs[1, 0])
    if 'monthly_trends' in analysis_results:
        monthly_data = analysis_results['monthly_trends']
        sorted_months = sorted(monthly_data.keys())
        totals = [monthly_data[month]['total'] for month in sorted_months]
        ax3.plot(range(len(sorted_months)), totals, marker='o', linewidth=2,
                color='steelblue', markersize=6)
        ax3.set_xticks(range(len(sorted_months)))
        ax3.set_xticklabels(sorted_months, rotation=45, ha='right', fontsize=7)
        ax3.set_ylabel('Total ($)', fontsize=10)
        ax3.set_title('Spending Trend', fontsize=12, fontweight='bold')
        ax3.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
        ax3.grid(True, alpha=0.3)

    # 4. Payment Methods
    ax4 = fig.add_subplot(gs[1, 1])
    if 'payment_methods' in analysis_results:
        payment_data = analysis_results['payment_methods']
        methods = list(payment_data.keys())
        totals = [payment_data[m]['total'] for m in methods]
        ax4.barh(methods, totals, color=plt.cm.Pastel1(np.linspace(0, 1, len(methods))))
        ax4.set_xlabel('Total ($)', fontsize=10)
        ax4.set_title('By Payment Method', fontsize=12, fontweight='bold')
        ax4.xaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
        ax4.invert_yaxis()

    # 5. Statistics Summary
    ax5 = fig.add_subplot(gs[2, :])
    ax5.axis('off')
    if 'statistics' in analysis_results:
        stats = analysis_results['statistics']
        summary_text = f"""
        EXPENSE SUMMARY STATISTICS
        ─────────────────────────────────────────────────────────
        Total Spending:      ${stats.get('total_spending', 0):>12,.2f}
        Total Transactions:  {stats.get('total_transactions', 0):>12}
        Average per Txn:     ${stats.get('average_per_transaction', 0):>12,.2f}
        Median Transaction:  ${stats.get('median_transaction', 0):>12,.2f}
        Min Transaction:     ${stats.get('minimum_transaction', 0):>12,.2f}
        Max Transaction:     ${stats.get('maximum_transaction', 0):>12,.2f}
        Daily Average:       ${stats.get('daily_average', 0):>12,.2f}
        Monthly Average:     ${stats.get('monthly_average', 0):>12,.2f}
        ─────────────────────────────────────────────────────────
        Period: {stats.get('date_range', {}).get('start', 'N/A')} to {stats.get('date_range', {}).get('end', 'N/A')}
        """
        ax5.text(0.5, 0.5, summary_text, transform=ax5.transAxes, fontsize=11,
                verticalalignment='center', horizontalalignment='center',
                fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.3))

    # Main title
    fig.suptitle('Personal Expense Tracker Dashboard', fontsize=16, fontweight='bold')

    # Save if path provided
    if save_path:
        output_dir = ensure_output_directory()
        filepath = os.path.join(output_dir, save_path) if not os.path.dirname(save_path) else save_path
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"✓ Dashboard saved to: {filepath}")

    return fig


def close_all_figures():
    """Close all matplotlib figures to free memory."""
    plt.close('all')


# Test function
if __name__ == "__main__":
    print("Visualizer Module Test")
    print("-" * 30)

    # Import analyzer for test data
    from analyzer import run_full_analysis
    from data_generator import generate_synthetic_data

    # Generate test data
    test_expenses = generate_synthetic_data(num_records=100)

    # Run analysis
    analysis = run_full_analysis(test_expenses)

    # Create test charts
    print("\nCreating test visualizations...")

    plot_category_pie_chart(analysis['by_category'], 'test_category_pie.png')
    plot_monthly_bar_chart(analysis['monthly_trends'], 'test_monthly_bar.png')
    plot_trend_line(analysis['monthly_trends'], 'test_trend_line.png')
    plot_payment_breakdown(analysis['payment_methods'], 'test_payment.png')
    create_dashboard(analysis, 'test_dashboard.png')

    print("\n✓ All test visualizations created!")
    print(f"Charts saved to: {ensure_output_directory()}")