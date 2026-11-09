import pandas as pd

orders = pd.read_csv("data/processed/orders_clean.csv")
customers = pd.read_csv("data/processed/customers_clean.csv")
products = pd.read_csv("data/processed/products_clean.csv")

# Completed orders only
orders = orders[orders["status"] == "completed"]

# Join customers
df = orders.merge(customers, on="customer_id")

# Revenue by city
city_revenue = df.groupby("city")["order_amount"].sum()

print("REVENUE BY CITY")
print(city_revenue)

print("\nTOTAL REVENUE:")
print(city_revenue.sum())