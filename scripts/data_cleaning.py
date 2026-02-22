"""
Sales Data Dashboard - Data Cleaning Script
Loads the raw CSV, cleans and transforms data, exports cleaned version.
"""

import os
import pandas as pd
import numpy as np


def main():
    print("Cleaning sales data...")

    # -- Load --------------------------------------------------------------
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    raw_path = os.path.join(data_dir, "sales_data.csv")
    df = pd.read_csv(raw_path)
    print(f"   Loaded {len(df):,} records from {raw_path}")

    # -- Data Type Fixes ----------------------------------------------------
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Ship_Date"] = pd.to_datetime(df["Ship_Date"])

    # -- Derived Columns ----------------------------------------------------
    df["Year"] = df["Order_Date"].dt.year
    df["Month"] = df["Order_Date"].dt.month
    df["Quarter"] = df["Order_Date"].dt.quarter
    df["Year_Quarter"] = df["Year"].astype(str) + "-Q" + df["Quarter"].astype(str)
    df["Month_Name"] = df["Order_Date"].dt.strftime("%B")
    df["Day_of_Week"] = df["Order_Date"].dt.day_name()
    df["Ship_Duration_Days"] = (df["Ship_Date"] - df["Order_Date"]).dt.days
    df["Profit_Margin"] = np.where(df["Sales"] != 0, (df["Profit"] / df["Sales"] * 100).round(2), 0)
    df["Revenue_Per_Unit"] = (df["Sales"] / df["Quantity"]).round(2)

    # -- Handle Anomalies ---------------------------------------------------
    # Cap extreme negative profits (data quality check)
    profit_floor = df["Profit"].quantile(0.001)
    df.loc[df["Profit"] < profit_floor, "Profit"] = profit_floor

    # Ensure no negative ship durations
    df.loc[df["Ship_Duration_Days"] < 0, "Ship_Duration_Days"] = 0

    # -- Missing Value Check ------------------------------------------------
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(f"   WARNING: Missing values found:\n{missing[missing > 0]}")
        df = df.dropna()
        print(f"   Dropped rows with missing values. Remaining: {len(df):,}")
    else:
        print("   No missing values found")

    # -- Export -------------------------------------------------------------
    clean_path = os.path.join(data_dir, "sales_data_cleaned.csv")
    df.to_csv(clean_path, index=False)

    print(f"Cleaned data exported -> {clean_path}")
    print(f"   Shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
    print(f"   Columns added: Year, Month, Quarter, Year_Quarter, Month_Name,")
    print(f"                  Day_of_Week, Ship_Duration_Days, Profit_Margin, Revenue_Per_Unit")
    print(f"\n   Quick Summary:")
    print(f"   Sales range:  ${df['Sales'].min():,.2f} to ${df['Sales'].max():,.2f}")
    print(f"   Profit range: ${df['Profit'].min():,.2f} to ${df['Profit'].max():,.2f}")
    print(f"   Avg discount: {df['Discount'].mean():.1%}")
    print(f"   Ship duration avg: {df['Ship_Duration_Days'].mean():.1f} days")


if __name__ == "__main__":
    main()
