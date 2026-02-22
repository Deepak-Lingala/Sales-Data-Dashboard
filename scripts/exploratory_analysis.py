"""
Sales Data Dashboard - Exploratory Data Analysis
Generates key insight charts and prints summary statistics.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# -- Style Setup ------------------------------------------------------------
plt.style.use("seaborn-v0_8-darkgrid")
sns.set_palette("husl")

COLORS = {
    "primary": "#6366f1",
    "secondary": "#8b5cf6",
    "accent": "#06b6d4",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "bg_dark": "#1e1b4b",
    "regions": ["#6366f1", "#06b6d4", "#10b981", "#f59e0b"],
    "categories": ["#6366f1", "#06b6d4", "#10b981"],
}

FIG_SIZE = (12, 6)
DPI = 150


def setup_dirs():
    """Create output directory."""
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def load_data():
    """Load cleaned dataset."""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    df = pd.read_csv(os.path.join(data_dir, "sales_data_cleaned.csv"))
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df


def print_summary(df: pd.DataFrame):
    """Print key summary statistics."""
    print("=" * 60)
    print("SALES DATA - KEY METRICS SUMMARY")
    print("=" * 60)

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order_ID"].nunique()
    avg_order = df.groupby("Order_ID")["Sales"].sum().mean()

    print(f"\n   Total Revenue:     ${total_sales:>12,.2f}")
    print(f"   Total Profit:      ${total_profit:>12,.2f}")
    print(f"   Total Orders:      {total_orders:>12,}")
    print(f"   Avg Order Value:   ${avg_order:>12,.2f}")
    print(f"   Profit Margin:     {total_profit/total_sales*100:>11.1f}%")

    print(f"\n{'-' * 60}")
    print("   Revenue by Region:")
    for _, row in df.groupby("Region")["Sales"].sum().sort_values(ascending=False).reset_index().iterrows():
        pct = row["Sales"] / total_sales * 100
        print(f"   {row['Region']:<10} ${row['Sales']:>12,.2f}  ({pct:.1f}%)")

    print(f"\n{'-' * 60}")
    print("   Revenue by Category:")
    for _, row in df.groupby("Category")["Sales"].sum().sort_values(ascending=False).reset_index().iterrows():
        pct = row["Sales"] / total_sales * 100
        print(f"   {row['Category']:<18} ${row['Sales']:>12,.2f}  ({pct:.1f}%)")

    print(f"\n{'-' * 60}")
    print("   Revenue by Year:")
    for _, row in df.groupby("Year")["Sales"].sum().sort_index().reset_index().iterrows():
        pct = row["Sales"] / total_sales * 100
        print(f"   {int(row['Year'])}    ${row['Sales']:>12,.2f}  ({pct:.1f}%)")


def plot_monthly_sales_trend(df: pd.DataFrame, output_dir: str):
    """Monthly sales trend line chart."""
    monthly = df.groupby(df["Order_Date"].dt.to_period("M")).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum")
    ).reset_index()
    monthly["Order_Date"] = monthly["Order_Date"].dt.to_timestamp()

    fig, ax = plt.subplots(figsize=FIG_SIZE, dpi=DPI)
    ax.plot(monthly["Order_Date"], monthly["Sales"], color=COLORS["primary"],
            linewidth=2.5, label="Revenue", marker="o", markersize=4)
    ax.plot(monthly["Order_Date"], monthly["Profit"], color=COLORS["success"],
            linewidth=2.5, label="Profit", marker="s", markersize=4)
    ax.fill_between(monthly["Order_Date"], monthly["Sales"], alpha=0.1, color=COLORS["primary"])
    ax.fill_between(monthly["Order_Date"], monthly["Profit"], alpha=0.1, color=COLORS["success"])

    ax.set_title("Monthly Sales & Profit Trend (2023-2025)", fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Amount ($)", fontsize=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.legend(fontsize=11, loc="upper left")
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "monthly_sales_trend.png"), bbox_inches="tight")
    plt.close()
    print("   [OK] monthly_sales_trend.png")


def plot_revenue_by_region(df: pd.DataFrame, output_dir: str):
    """Revenue by region bar chart."""
    region_data = df.groupby("Region").agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum")
    ).sort_values("Sales", ascending=True).reset_index()

    fig, ax = plt.subplots(figsize=(10, 6), dpi=DPI)
    bars = ax.barh(region_data["Region"], region_data["Sales"],
                   color=COLORS["regions"], edgecolor="white", height=0.6)

    for bar, val in zip(bars, region_data["Sales"]):
        ax.text(val + region_data["Sales"].max() * 0.01, bar.get_y() + bar.get_height() / 2,
                f"${val:,.0f}", va="center", fontsize=11, fontweight="bold")

    ax.set_title("Total Revenue by Region", fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Revenue ($)", fontsize=12)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "revenue_by_region.png"), bbox_inches="tight")
    plt.close()
    print("   [OK] revenue_by_region.png")


def plot_category_breakdown(df: pd.DataFrame, output_dir: str):
    """Category & sub-category breakdown."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=DPI)

    # Pie chart - Categories
    cat_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    wedges, texts, autotexts = ax1.pie(
        cat_sales, labels=cat_sales.index, autopct="%1.1f%%",
        colors=COLORS["categories"], startangle=90,
        textprops={"fontsize": 11}, pctdistance=0.75
    )
    for t in autotexts:
        t.set_fontweight("bold")
    ax1.set_title("Revenue by Category", fontsize=14, fontweight="bold", pad=15)

    # Bar chart - Top Sub-Categories
    sub_sales = df.groupby("Sub_Category")["Sales"].sum().sort_values(ascending=True).tail(10)
    ax2.barh(sub_sales.index, sub_sales.values, color=COLORS["primary"],
             edgecolor="white", height=0.6)
    for i, val in enumerate(sub_sales.values):
        ax2.text(val + sub_sales.max() * 0.01, i, f"${val:,.0f}", va="center", fontsize=9)
    ax2.set_title("Top 10 Sub-Categories by Revenue", fontsize=14, fontweight="bold", pad=15)
    ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "category_breakdown.png"), bbox_inches="tight")
    plt.close()
    print("   [OK] category_breakdown.png")


def plot_top_products(df: pd.DataFrame, output_dir: str):
    """Top 10 products by total sales."""
    top = df.groupby("Product_Name").agg(
        Sales=("Sales", "sum"), Quantity=("Quantity", "sum"), Profit=("Profit", "sum")
    ).sort_values("Sales", ascending=True).tail(10)

    fig, ax = plt.subplots(figsize=(12, 7), dpi=DPI)
    colors = [COLORS["success"] if p > 0 else COLORS["danger"] for p in top["Profit"]]
    bars = ax.barh(top.index, top["Sales"], color=colors, edgecolor="white", height=0.6)

    for bar, val in zip(bars, top["Sales"]):
        ax.text(val + top["Sales"].max() * 0.01, bar.get_y() + bar.get_height() / 2,
                f"${val:,.0f}", va="center", fontsize=10, fontweight="bold")

    ax.set_title("Top 10 Products by Revenue\n(Green = Profitable, Red = Loss)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Total Revenue ($)", fontsize=12)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "top_products.png"), bbox_inches="tight")
    plt.close()
    print("   [OK] top_products.png")


def plot_segment_analysis(df: pd.DataFrame, output_dir: str):
    """Customer segment analysis."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=DPI)

    seg_data = df.groupby("Segment").agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique")
    ).reset_index()

    # Donut chart
    colors_seg = [COLORS["primary"], COLORS["accent"], COLORS["warning"]]
    wedges, texts, autotexts = ax1.pie(
        seg_data["Sales"], labels=seg_data["Segment"], autopct="%1.1f%%",
        colors=colors_seg, startangle=90, pctdistance=0.8,
        wedgeprops={"width": 0.5}, textprops={"fontsize": 12}
    )
    for t in autotexts:
        t.set_fontweight("bold")
    ax1.set_title("Revenue by Customer Segment", fontsize=14, fontweight="bold", pad=15)

    # Profit margin by segment
    seg_data["Margin"] = seg_data["Profit"] / seg_data["Sales"] * 100
    bars = ax2.bar(seg_data["Segment"], seg_data["Margin"], color=colors_seg,
                   edgecolor="white", width=0.5)
    for bar, val in zip(bars, seg_data["Margin"]):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                 f"{val:.1f}%", ha="center", fontsize=12, fontweight="bold")
    ax2.set_title("Profit Margin by Segment", fontsize=14, fontweight="bold", pad=15)
    ax2.set_ylabel("Profit Margin (%)", fontsize=12)

    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "segment_analysis.png"), bbox_inches="tight")
    plt.close()
    print("   [OK] segment_analysis.png")


def plot_quarterly_heatmap(df: pd.DataFrame, output_dir: str):
    """Quarterly revenue heatmap by region."""
    pivot = df.pivot_table(values="Sales", index="Region", columns="Year_Quarter",
                           aggfunc="sum").fillna(0)
    # Sort columns chronologically
    pivot = pivot[sorted(pivot.columns)]

    fig, ax = plt.subplots(figsize=(16, 5), dpi=DPI)
    sns.heatmap(pivot, annot=True, fmt=",.0f", cmap="YlOrRd",
                linewidths=1, linecolor="white", ax=ax,
                annot_kws={"fontsize": 8})
    ax.set_title("Revenue Heatmap: Region x Quarter", fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Quarter", fontsize=12)
    ax.set_ylabel("Region", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "quarterly_heatmap.png"), bbox_inches="tight")
    plt.close()
    print("   [OK] quarterly_heatmap.png")


def main():
    output_dir = setup_dirs()
    df = load_data()

    print(f"\n   Loaded {len(df):,} records")
    print_summary(df)

    print(f"\n{'=' * 60}")
    print("GENERATING CHARTS...")
    print(f"{'=' * 60}")

    plot_monthly_sales_trend(df, output_dir)
    plot_revenue_by_region(df, output_dir)
    plot_category_breakdown(df, output_dir)
    plot_top_products(df, output_dir)
    plot_segment_analysis(df, output_dir)
    plot_quarterly_heatmap(df, output_dir)

    print(f"\nAll charts saved to {output_dir}/")
    print("   Ready for portfolio & Power BI reference!")


if __name__ == "__main__":
    main()
