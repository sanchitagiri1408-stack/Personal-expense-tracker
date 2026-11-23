"""
Data Generator Module
=====================
This module generates synthetic expense data for the Personal Expense Tracker.
It creates realistic sample data that mimics actual spending patterns.
"""

import random
from datetime import datetime, timedelta
import csv


def generate_synthetic_data(num_records=365, start_date=None):
    """
    Generate synthetic expense data.

    Parameters:
    -----------
    num_records : int
        Number of expense records to generate (default: 365 for one year)
    start_date : str, optional
        Start date in YYYY-MM-DD format. Defaults to 1 year ago.

    Returns:
    --------
    list : List of dictionaries containing expense records
    """

    # Define expense categories with subcategories
    categories = {
        'Food & Dining': ['Groceries', 'Restaurant', 'Coffee', 'Fast Food', 'Food Delivery'],
        'Transportation': ['Gas/Fuel', 'Public Transit', 'Uber/Lyft', 'Parking', 'Car Maintenance'],
        'Shopping': ['Clothing', 'Electronics', 'Home Goods', 'Gifts', 'Online Shopping'],
        'Bills & Utilities': ['Electricity', 'Water', 'Internet', 'Phone Bill', 'Rent'],
        'Entertainment': ['Movies', 'Concerts', 'Streaming Services', 'Gaming', 'Hobbies'],
        'Healthcare': ['Doctor Visit', 'Pharmacy', 'Health Insurance', 'Dental', 'Vision'],
        'Education': ['Books', 'Courses', 'Tuition', 'Software', 'Supplies'],
        'Other': ['Miscellaneous', 'Tips', 'Subscriptions', 'Donations', 'Travel']
    }

    # Payment methods with weighted probabilities
    payment_methods = {
        'Credit Card': 0.40,
        'Debit Card': 0.30,
        'Cash': 0.15,
        'Mobile Payment': 0.10,
        'Bank Transfer': 0.05
    }

    # Amount ranges by category (min, max)
    amount_ranges = {
        'Food & Dining': (5, 150),
        'Transportation': (5, 100),
        'Shopping': (10, 300),
        'Bills & Utilities': (50, 500),
        'Entertainment': (5, 100),
        'Healthcare': (10, 200),
        'Education': (20, 300),
        'Other': (5, 100)
    }

    # Set start date (default: 1 year ago)
    if start_date:
        start = datetime.strptime(start_date, '%Y-%m-%d')
    else:
        start = datetime.now() - timedelta(days=365)

    # Generate random dates within the date range
    end = datetime.now()
    date_range = (end - start).days

    # Generate expense records
    expenses = []

    for _ in range(num_records):
        # Random date
        days_offset = random.randint(0, date_range)
        date = start + timedelta(days=days_offset)

        # Random category
        category = random.choice(list(categories.keys()))

        # Random subcategory
        subcategory = random.choice(categories[category])

        # Random amount based on category
        min_amt, max_amt = amount_ranges[category]

        # Use different distributions for different categories
        if category in ['Bills & Utilities']:
            # Bills tend to be fixed amounts
            amount = round(random.uniform(min_amt, max_amt), 2)
        elif category in ['Food & Dining', 'Entertainment']:
            # More frequent small amounts
            amount = round(random.expovariate(1/30) + min_amt, 2)
            amount = min(amount, max_amt)
        else:
            # General distribution
            amount = round(random.uniform(min_amt, max_amt), 2)

        # Random description
        descriptions = get_descriptions(category, subcategory)
        description = random.choice(descriptions)

        # Random payment method
        payment = random.choices(
            list(payment_methods.keys()),
            weights=list(payment_methods.values())
        )[0]

        # Create expense record
        expense = {
            'date': date.strftime('%Y-%m-%d'),
            'category': category,
            'subcategory': subcategory,
            'amount': amount,
            'description': description,
            'payment_method': payment
        }

        expenses.append(expense)

    # Sort by date
    expenses.sort(key=lambda x: x['date'])

    return expenses


def get_descriptions(category, subcategory):
    """
    Get sample descriptions for each category.
    """
    descriptions = {
        'Food & Dining': {
            'Groceries': ['Weekly groceries at Walmart', 'Whole Foods Market', 'Trader Joes', 'Costco run'],
            'Restaurant': ['Dinner at Italian place', 'Lunch with coworkers', 'Birthday dinner', 'Date night'],
            'Coffee': ['Starbucks morning coffee', 'Local cafe', 'Starbucks', 'Dunkin Donuts'],
            'Fast Food': ['McDonalds', 'Subway', 'Chipotle', 'Chick-fil-A'],
            'Food Delivery': ['DoorDash order', 'Uber Eats', 'Grubhub', 'Postmates']
        },
        'Transportation': {
            'Gas/Fuel': ['Shell gas station', 'BP gas', 'Chevron', 'ExxonMobil'],
            'Public Transit': ['Monthly bus pass', 'Subway fare', 'Train ticket', 'Metro card'],
            'Uber/Lyft': ['Uber ride', 'Lyft to airport', 'Uber Eats trip', 'Lyft ride home'],
            'Parking': ['Downtown parking', 'Airport parking', 'Event parking', 'Monthly parking'],
            'Car Maintenance': ['Oil change', 'Car wash', 'Tire rotation', 'Battery replacement']
        },
        'Shopping': {
            'Clothing': ['New shoes', 'Winter jacket', 'Amazon clothing', 'Target clothes'],
            'Electronics': ['New headphones', 'Phone charger', 'Laptop accessories', 'Tablet'],
            'Home Goods': ['Bed sheets', 'Kitchen items', 'Home decor', 'IKEA trip'],
            'Gifts': ['Birthday gift', 'Holiday presents', 'Wedding gift', 'Baby shower gift'],
            'Online Shopping': ['Amazon order', 'Etsy purchase', 'eBay item', 'Online deal']
        },
        'Bills & Utilities': {
            'Electricity': ['Electric bill', 'Power company', 'Monthly electric'],
            'Water': ['Water bill', 'Monthly water', 'Utility payment'],
            'Internet': ['Internet service', 'WiFi bill', 'Monthly internet'],
            'Phone Bill': ['Cell phone bill', 'Monthly phone', 'Verizon bill', 'AT&T bill'],
            'Rent': ['Monthly rent', 'Rent payment', 'Housing']
        },
        'Entertainment': {
            'Movies': ['Movie tickets', 'Cinema', 'Netflix', 'AMC Theaters'],
            'Concerts': ['Concert tickets', 'Music festival', 'Live show', 'Event'],
            'Streaming Services': ['Netflix subscription', 'Spotify', 'Disney+', 'HBO Max'],
            'Gaming': ['Video game purchase', 'PlayStation store', 'Xbox game', 'Steam'],
            'Hobbies': ['Art supplies', 'Photography gear', 'Sporting goods', 'Craft supplies']
        },
        'Healthcare': {
            'Doctor Visit': ['Annual checkup', 'Doctor appointment', 'Specialist visit', 'Urgent care'],
            'Pharmacy': ['Prescription', 'CVS pharmacy', 'Walgreens', 'Medicine'],
            'Health Insurance': ['Monthly premium', 'Health insurance', 'Copay'],
            'Dental': ['Dental cleaning', 'Dentist visit', 'Dental work', 'Orthodontist'],
            'Vision': ['Eye exam', 'Glasses', 'Contact lenses', 'Vision insurance']
        },
        'Education': {
            'Books': ['Textbook', 'Amazon books', 'Course materials', 'Novels'],
            'Courses': ['Online course', 'Udemy', 'Coursera', 'Workshop'],
            'Tuition': ['College tuition', 'School payment', 'Tuition installment'],
            'Software': ['Microsoft 365', 'Adobe subscription', 'Software license', 'App purchase'],
            'Supplies': ['School supplies', 'Notebooks', 'Pens and pencils', 'Office supplies']
        },
        'Other': {
            'Miscellaneous': ['Misc purchase', 'Random expense', 'Uncategorized', 'Other'],
            'Tips': ['Restaurant tip', 'Delivery tip', 'Service tip', 'Gratuity'],
            'Subscriptions': ['Gym membership', 'Amazon Prime', 'Cloud storage', 'Newsletter'],
            'Donations': ['Charity donation', 'Nonprofit', 'Church offering', 'Crowdfunding'],
            'Travel': ['Hotel', 'Flight', 'Vacation expense', 'Travel expense']
        }
    }

    if category in descriptions and subcategory in descriptions[category]:
        return descriptions[category][subcategory]

    return ['General expense', 'Monthly expense', 'Regular payment']


def save_to_csv(expenses, filepath='expenses.csv'):
    """
    Save expense data to a CSV file.

    Parameters:
    -----------
    expenses : list
        List of expense dictionaries
    filepath : str
        Output CSV file path
    """
    fieldnames = ['date', 'category', 'subcategory', 'amount', 'description', 'payment_method']

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)

    print(f"✓ Generated {len(expenses)} expense records")
    print(f"✓ Saved to: {filepath}")


# Run if executed directly
if __name__ == "__main__":
    # Generate sample data
    print("Generating synthetic expense data...")
    data = generate_synthetic_data(num_records=100)
    save_to_csv(data, 'sample_expenses.csv')
    print("\nSample data generated successfully!")