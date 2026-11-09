
import pandas as pd

# Load data
customers = pd.read_csv("data/processed/customers_clean.csv")
orders = pd.read_csv("data/processed/orders_clean.csv")

# Snapshot date
snapshot = pd.Timestamp("2025-10-01")

# Convert order date
orders["order_ts"] = pd.to_datetime(orders["order_ts"])

# Filter completed orders before snapshot
completed = orders[
    (orders["status"].str.lower() == "completed") &
    (orders["order_ts"] < snapshot)
].copy()

# Find last purchase date
last_purchase = completed.groupby("customer_id")["order_ts"].max()

# Create lapse dataset
df = customers.copy()
df["last_purchase"] = df["customer_id"].map(last_purchase)

# Calculate recency
df["recency"] = (snapshot - df["last_purchase"]).dt.days

# Handle customers without purchases
df["recency"] = df["recency"].fillna(181)

# Define lapse label
df["lapsed"] = (df["recency"] > 90).astype(int)

# Save dataset
df.to_csv("data/processed/lapse_dataset.csv", index=False)

print("LAPSE DATASET CREATED!")
print("Total customers:", len(df))
print("\nLapse distribution:")
print(df["lapsed"].value_counts())
print("\nSaved to data/processed/lapse_dataset.csv")
