
import pandas as pd
import sqlite3

print("INSTAMART DATA VALIDATION")
print("========================")

# Load cleaned datasets
customers = pd.read_csv("data/clean/customers.csv")
products = pd.read_csv("data/clean/products.csv")
orders = pd.read_csv("data/clean/orders.csv")

# Check customer data
assert len(customers) == 1200
assert customers["age"].isna().sum() == 0
assert customers["city"].nunique() == 6

# Check product data
assert len(products) == 40

# Check orders data
assert len(orders) == 12309
assert orders["order_id"].nunique() == 12309
assert orders["status"].value_counts().get("completed", 0) == 11110
assert orders["status"].value_counts().get("cancelled", 0) == 1199

# Check completed order amounts
completed = orders[orders["status"] == "completed"]

assert completed["order_amount"].isna().sum() == 0

# Check SQLite tables
conn = sqlite3.connect("data/instamart.db")

tables = pd.read_sql_query(
    "SELECT name FROM sqlite_master WHERE type='table'",
    conn
)

print("\nSQLite Tables:")
print(tables)

conn.close()

print("\nALL CHECKS PASSED!")
