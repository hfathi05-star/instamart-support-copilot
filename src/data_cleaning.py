
import pandas as pd
import sqlite3
from pathlib import Path

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

RAW_DIR = Path("data/raw")
CLEAN_DIR = Path("data/clean")
DB_PATH = Path("data/instamart.db")

CLEAN_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 1. CLEAN CUSTOMERS
# --------------------------------------------------

def clean_customers():

    print("\nCUSTOMER DATA CLEANING")

    customers = pd.read_csv(
        RAW_DIR / "customers.csv",
        keep_default_na=False
    )

    # Convert age to numeric
    customers["age"] = pd.to_numeric(
        customers["age"], errors="coerce"
    )

    # Invalid ages become missing
    customers.loc[
        ~customers["age"].between(10, 100),
        "age"
    ] = pd.NA

    # Clean city
    customers["city"] = (
        customers["city"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    # Standardise gender
    customers["gender"] = (
        customers["gender"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    gender_mapping = {
        "m": "male",
        "male": "male",
        "f": "female",
        "female": "female"
    }

    customers["gender"] = customers["gender"].map(
        gender_mapping
    ).fillna("unknown")

    # Fill missing ages with city median
    customers["age"] = customers.groupby("city")[
        "age"
    ].transform(lambda x: x.fillna(x.median()))

    # Convert signup date
    customers["signup_date"] = pd.to_datetime(
        customers["signup_date"],
        errors="coerce"
    )

    # Save cleaned customers
    customers.to_csv(
        CLEAN_DIR / "customers.csv",
        index=False
    )

    print("Customers saved successfully")
    print("City counts:")
    print(customers["city"].value_counts())

    print("\nGender counts:")
    print(customers["gender"].value_counts())

    print("\nMissing ages:", customers["age"].isna().sum())

    return customers


# --------------------------------------------------
# 2. CLEAN PRODUCTS
# --------------------------------------------------

def clean_products():

    print("\nPRODUCT DATA CLEANING")

    products = pd.read_csv(
        RAW_DIR / "products.csv",
        keep_default_na=False
    )

    # Clean text columns
    for column in products.select_dtypes(
        include="object"
    ).columns:
        products[column] = (
            products[column]
            .astype(str)
            .str.strip()
        )

    # Convert price to numeric
    products["price_inr"] = pd.to_numeric(
        products["price_inr"],
        errors="coerce"
    )

    # Clean category
    products["category"] = (
        products["category"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    products.to_csv(
        CLEAN_DIR / "products.csv",
        index=False
    )

    print("Products saved successfully")
    print("Product count:", len(products))

    return products


# --------------------------------------------------
# 3. CLEAN ORDERS
# --------------------------------------------------

def clean_orders(products):

    print("\nORDERS DATA CLEANING")

    orders = pd.read_csv(
        RAW_DIR / "orders.csv",
        keep_default_na=False
    )

    # Convert order timestamp
    orders["order_ts"] = pd.to_datetime(
        orders["order_ts"],
        errors="coerce"
    )

    # Remove exact duplicate rows
    orders = orders.drop_duplicates()

    # Keep latest record for every order_id
    orders = orders.sort_values("order_ts")

    orders = orders.drop_duplicates(
        subset=["order_id"],
        keep="last"
    )

    # Convert order amount to numeric
    orders["order_amount"] = pd.to_numeric(
        orders["order_amount"],
        errors="coerce"
    )

    # Convert quantity and discount
    orders["quantity"] = pd.to_numeric(
        orders["quantity"],
        errors="coerce"
    )

    orders["discount_pct"] = pd.to_numeric(
        orders["discount_pct"],
        errors="coerce"
    )

    # Join product price and category
    product_info = products[
        ["product_id", "price_inr", "category"]
    ].copy()

    orders = orders.merge(
        product_info,
        on="product_id",
        how="left"
    )

    # Fill missing order amount using product price
    missing_amount = orders["order_amount"].isna()

    orders.loc[
        missing_amount,
        "order_amount"
    ] = (
        orders.loc[missing_amount, "price_inr"]
        * orders.loc[missing_amount, "quantity"]
        * (
            1 -
            orders.loc[missing_amount, "discount_pct"] / 100
        )
    ).round(2)

    # Convert delivery minutes to numeric
    orders["delivery_minutes"] = pd.to_numeric(
        orders["delivery_minutes"],
        errors="coerce"
    )

    # Negative delivery times become missing
    orders.loc[
        orders["delivery_minutes"] < 0,
        "delivery_minutes"
    ] = pd.NA

    # Fill missing delivery times only for completed orders
    completed_mask = orders["status"].str.lower() == "completed"

    orders.loc[
        ~completed_mask,
        "delivery_minutes"
    ] = pd.NA

    orders.loc[
        completed_mask,
        "delivery_minutes"
    ] = orders.loc[
        completed_mask,
        "delivery_minutes"
    ].fillna(
        orders.loc[
            completed_mask
        ].groupby("category")[
            "delivery_minutes"
        ].transform("median")
    )

    # Remove helper columns
    orders = orders.drop(
        columns=["price_inr", "category"]
    )

    # Save cleaned orders
    orders.to_csv(
        CLEAN_DIR / "orders.csv",
        index=False
    )

    print("Orders saved successfully")
    print("Total orders:", len(orders))
    print("Completed orders:", (orders["status"] == "completed").sum())
    print("Cancelled orders:", (orders["status"] == "cancelled").sum())

    return orders


# --------------------------------------------------
# 4. SAVE CLEAN TABLES TO SQLITE
# --------------------------------------------------

def save_to_database(customers, products, orders):

    print("\nSAVING DATA TO SQLITE")

    with sqlite3.connect(DB_PATH) as connection:

        customers.to_sql(
            "customers",
            connection,
            if_exists="replace",
            index=False
        )

        products.to_sql(
            "products",
            connection,
            if_exists="replace",
            index=False
        )

        orders.to_sql(
            "orders",
            connection,
            if_exists="replace",
            index=False
        )

    print("SQLite database saved successfully")
    print("Database:", DB_PATH)


# --------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------

if __name__ == "__main__":

    customers = clean_customers()

    products = clean_products()

    orders = clean_orders(products)

    save_to_database(
        customers,
        products,
        orders
    )

    print("\nALL DATASETS CLEANED SUCCESSFULLY!")
