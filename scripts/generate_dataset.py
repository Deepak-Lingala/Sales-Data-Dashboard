"""
Sales Data Dashboard - Synthetic Dataset Generator
Generates ~10,000 realistic US sales records (2023-2025).
"""

import os
import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import timedelta

fake = Faker("en_US")
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# -- Configuration ---------------------------------------------------------
NUM_RECORDS = 10_000
DATE_START = pd.Timestamp("2023-01-01")
DATE_END = pd.Timestamp("2025-12-31")

REGIONS = {
    "East":    ["New York", "Boston", "Philadelphia", "Washington", "Miami",
                "Atlanta", "Charlotte", "Baltimore", "Richmond", "Jacksonville"],
    "West":    ["Los Angeles", "San Francisco", "Seattle", "Denver", "Phoenix",
                "Portland", "Las Vegas", "San Diego", "Salt Lake City", "Sacramento"],
    "Central": ["Chicago", "Houston", "Dallas", "Minneapolis", "St. Louis",
                "Kansas City", "Milwaukee", "Indianapolis", "Columbus", "Detroit"],
    "South":   ["Nashville", "New Orleans", "Memphis", "Louisville", "Birmingham",
                "San Antonio", "Austin", "Raleigh", "Tampa", "Orlando"],
}

STATES_FOR_CITY = {
    "New York": "New York", "Boston": "Massachusetts", "Philadelphia": "Pennsylvania",
    "Washington": "District of Columbia", "Miami": "Florida", "Atlanta": "Georgia",
    "Charlotte": "North Carolina", "Baltimore": "Maryland", "Richmond": "Virginia",
    "Jacksonville": "Florida", "Los Angeles": "California", "San Francisco": "California",
    "Seattle": "Washington", "Denver": "Colorado", "Phoenix": "Arizona",
    "Portland": "Oregon", "Las Vegas": "Nevada", "San Diego": "California",
    "Salt Lake City": "Utah", "Sacramento": "California", "Chicago": "Illinois",
    "Houston": "Texas", "Dallas": "Texas", "Minneapolis": "Minnesota",
    "St. Louis": "Missouri", "Kansas City": "Missouri", "Milwaukee": "Wisconsin",
    "Indianapolis": "Indiana", "Columbus": "Ohio", "Detroit": "Michigan",
    "Nashville": "Tennessee", "New Orleans": "Louisiana", "Memphis": "Tennessee",
    "Louisville": "Kentucky", "Birmingham": "Alabama", "San Antonio": "Texas",
    "Austin": "Texas", "Raleigh": "North Carolina", "Tampa": "Florida",
    "Orlando": "Florida",
}

SEGMENTS = ["Consumer", "Corporate", "Home Office"]
SEGMENT_WEIGHTS = [0.50, 0.30, 0.20]

PRODUCTS = {
    "Technology": {
        "Phones":       [("iPhone 15 Pro", 999), ("Samsung Galaxy S24", 849),
                         ("Google Pixel 8", 699), ("OnePlus 12", 599)],
        "Laptops":      [("MacBook Air M3", 1199), ("Dell XPS 15", 1399),
                         ("ThinkPad X1 Carbon", 1249), ("HP Spectre x360", 1099)],
        "Accessories":  [("AirPods Pro", 249), ("Logitech MX Master", 99),
                         ("USB-C Hub 10-in-1", 49), ("Webcam HD 1080p", 79)],
        "Monitors":     [("Dell UltraSharp 27\"", 449), ("LG 4K 32\"", 399),
                         ("Samsung Curved 34\"", 549), ("ASUS ProArt 27\"", 629)],
    },
    "Furniture": {
        "Chairs":       [("Ergonomic Mesh Chair", 349), ("Executive Leather Chair", 499),
                         ("Standing Desk Stool", 199), ("Task Chair Standard", 149)],
        "Tables":       [("Standing Desk Electric", 599), ("Conference Table 8ft", 899),
                         ("Corner Desk L-Shape", 399), ("Compact Writing Desk", 249)],
        "Bookcases":    [("5-Shelf Bookcase Oak", 179), ("Metal Storage Shelf", 129),
                         ("Glass Display Case", 299), ("Floating Wall Shelf Set", 89)],
        "Furnishings":  [("Desk Lamp LED", 59), ("Filing Cabinet 3-Drawer", 189),
                         ("Whiteboard 48x36", 129), ("Desk Organizer Set", 39)],
    },
    "Office Supplies": {
        "Paper":        [("Copy Paper 5000 Sheets", 45), ("Legal Pads 12-Pack", 24),
                         ("Sticky Notes Bulk Pack", 18), ("Cardstock 250 Sheets", 29)],
        "Binders":      [("3-Ring Binder Set", 22), ("Report Covers 25-Pack", 15),
                         ("Expanding File Folder", 12), ("Presentation Binder", 19)],
        "Art Supplies": [("Marker Set 24-Color", 28), ("Highlighter 12-Pack", 14),
                         ("Pen Set Professional", 35), ("Pencil Set Mechanical", 16)],
        "Storage":      [("Storage Boxes 12-Pack", 32), ("Drawer Organizer", 24),
                         ("Label Maker Pro", 49), ("Tape Dispenser Heavy", 18)],
    },
}

# -- Generator --------------------------------------------------------------

def generate_order_date():
    """Generate a random order date with seasonal sales patterns."""
    date = DATE_START + timedelta(days=random.randint(0, (DATE_END - DATE_START).days))
    # Boost Q4 (holiday season) probability
    if random.random() < 0.15 and date.month not in [10, 11, 12]:
        new_month = random.choice([10, 11, 12])
        # Clamp day to valid range for the new month
        import calendar
        max_day = calendar.monthrange(date.year, new_month)[1]
        day = min(date.day, max_day)
        date = date.replace(month=new_month, day=day)
    return date


def generate_record(order_id: int) -> dict:
    """Generate a single sales record."""
    # Region & location
    region = random.choice(list(REGIONS.keys()))
    city = random.choice(REGIONS[region])
    state = STATES_FOR_CITY[city]

    # Customer
    segment = np.random.choice(SEGMENTS, p=SEGMENT_WEIGHTS)
    customer_name = fake.name()

    # Product
    category = random.choice(list(PRODUCTS.keys()))
    sub_category = random.choice(list(PRODUCTS[category].keys()))
    product_name, base_price = random.choice(PRODUCTS[category][sub_category])

    # Dates
    order_date = generate_order_date()
    ship_days = np.random.choice([1, 2, 3, 4, 5, 6, 7], p=[0.05, 0.15, 0.25, 0.25, 0.15, 0.10, 0.05])
    ship_date = order_date + timedelta(days=int(ship_days))

    # Quantity & financials
    quantity = int(np.random.choice(range(1, 15), p=[
        0.25, 0.20, 0.15, 0.12, 0.08, 0.06, 0.04, 0.03, 0.02, 0.015, 0.015, 0.01, 0.005, 0.005
    ]))
    discount = round(np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40],
                                       p=[0.35, 0.15, 0.15, 0.10, 0.10, 0.07, 0.05, 0.03]), 2)

    # Price variation (+/- 15%)
    price_variation = base_price * np.random.uniform(0.85, 1.15)
    sales = round(price_variation * quantity * (1 - discount), 2)

    # Profit margin varies by category
    margin_ranges = {"Technology": (0.10, 0.35), "Furniture": (-0.05, 0.25), "Office Supplies": (0.15, 0.50)}
    margin = np.random.uniform(*margin_ranges[category])
    # Higher discounts squeeze margins
    margin -= discount * 0.5
    profit = round(sales * margin, 2)

    ship_mode = np.random.choice(
        ["Standard Class", "Second Class", "First Class", "Same Day"],
        p=[0.55, 0.20, 0.15, 0.10]
    )

    return {
        "Order_ID": f"ORD-{order_date.year}-{order_id:05d}",
        "Order_Date": order_date.strftime("%Y-%m-%d"),
        "Ship_Date": ship_date.strftime("%Y-%m-%d"),
        "Ship_Mode": ship_mode,
        "Customer_Name": customer_name,
        "Segment": segment,
        "City": city,
        "State": state,
        "Region": region,
        "Category": category,
        "Sub_Category": sub_category,
        "Product_Name": product_name,
        "Sales": sales,
        "Quantity": quantity,
        "Discount": discount,
        "Profit": profit,
    }


def main():
    print("Generating synthetic sales dataset...")
    records = [generate_record(i + 1) for i in range(NUM_RECORDS)]
    df = pd.DataFrame(records)

    # Sort by date
    df = df.sort_values("Order_Date").reset_index(drop=True)

    # Save
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "sales_data.csv")
    df.to_csv(output_path, index=False)

    print(f"Generated {len(df):,} records -> {output_path}")
    print(f"   Date range: {df['Order_Date'].min()} to {df['Order_Date'].max()}")
    print(f"   Total Sales: ${df['Sales'].sum():,.2f}")
    print(f"   Total Profit: ${df['Profit'].sum():,.2f}")
    print(f"   Regions: {df['Region'].nunique()} | Categories: {df['Category'].nunique()}")


if __name__ == "__main__":
    main()
