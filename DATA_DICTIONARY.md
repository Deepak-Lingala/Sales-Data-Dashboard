# Data Dictionary - Sales Data Dashboard

This document describes all fields in the dataset. The **raw dataset** (`sales_data.csv`) contains 16 fields. The **cleaned dataset** (`sales_data_cleaned.csv`) adds 9 derived columns for a total of 25 fields.

---

## Raw Fields (sales_data.csv)

| # | Field | Type | Description | Example |
|---|-------|------|-------------|---------|
| 1 | `Order_ID` | String | Unique order identifier | `ORD-2024-00042` |
| 2 | `Order_Date` | Date | Date the order was placed (YYYY-MM-DD) | `2024-03-15` |
| 3 | `Ship_Date` | Date | Date the order was shipped | `2024-03-18` |
| 4 | `Ship_Mode` | String | Shipping method | `Standard Class`, `Second Class`, `First Class`, `Same Day` |
| 5 | `Customer_Name` | String | Full name of the customer | `John Smith` |
| 6 | `Segment` | String | Customer segment | `Consumer` (50%), `Corporate` (30%), `Home Office` (20%) |
| 7 | `City` | String | US city (40 cities) | `New York`, `Los Angeles`, `Chicago` |
| 8 | `State` | String | US state | `California`, `Texas`, `New York` |
| 9 | `Region` | String | US region | `East`, `West`, `Central`, `South` |
| 10 | `Category` | String | Product category | `Technology`, `Furniture`, `Office Supplies` |
| 11 | `Sub_Category` | String | Product sub-category (12 types) | `Phones`, `Laptops`, `Chairs`, `Paper` |
| 12 | `Product_Name` | String | Specific product name | `MacBook Air M3`, `Ergonomic Mesh Chair` |
| 13 | `Sales` | Float | Revenue in USD (after discount) | `1,199.00` |
| 14 | `Quantity` | Integer | Number of units ordered (1-14) | `3` |
| 15 | `Discount` | Float | Discount percentage (0.0-0.40) | `0.15` |
| 16 | `Profit` | Float | Profit in USD (can be negative) | `245.80` |

---

## Derived Fields (sales_data_cleaned.csv)

These fields are added during the data cleaning step:

| # | Field | Type | Description | Example |
|---|-------|------|-------------|---------|
| 17 | `Year` | Integer | Year extracted from Order_Date | `2024` |
| 18 | `Month` | Integer | Month number (1-12) | `3` |
| 19 | `Quarter` | Integer | Quarter number (1-4) | `1` |
| 20 | `Year_Quarter` | String | Combined year-quarter label | `2024-Q1` |
| 21 | `Month_Name` | String | Full month name | `March` |
| 22 | `Day_of_Week` | String | Day of the week | `Friday` |
| 23 | `Ship_Duration_Days` | Integer | Days between order and shipment | `3` |
| 24 | `Profit_Margin` | Float | Profit as % of sales | `20.50` |
| 25 | `Revenue_Per_Unit` | Float | Sales divided by quantity | `399.67` |

---

## Value Distributions

### Regions (10 cities each)
| Region | Cities |
|--------|--------|
| **East** | New York, Boston, Philadelphia, Washington, Miami, Atlanta, Charlotte, Baltimore, Richmond, Jacksonville |
| **West** | Los Angeles, San Francisco, Seattle, Denver, Phoenix, Portland, Las Vegas, San Diego, Salt Lake City, Sacramento |
| **Central** | Chicago, Houston, Dallas, Minneapolis, St. Louis, Kansas City, Milwaukee, Indianapolis, Columbus, Detroit |
| **South** | Nashville, New Orleans, Memphis, Louisville, Birmingham, San Antonio, Austin, Raleigh, Tampa, Orlando |

### Product Categories & Sub-Categories
| Category | Sub-Categories |
|----------|---------------|
| **Technology** | Phones, Laptops, Accessories, Monitors |
| **Furniture** | Chairs, Tables, Bookcases, Furnishings |
| **Office Supplies** | Paper, Binders, Art Supplies, Storage |

### Ship Modes
| Mode | Approx. Distribution |
|------|---------------------|
| Standard Class | 55% |
| Second Class | 20% |
| First Class | 15% |
| Same Day | 10% |
