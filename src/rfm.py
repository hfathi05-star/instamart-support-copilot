
import pandas as pd

# Snapshot date
snapshot = pd.Timestamp("2025-10-01")

# Load cleaned data
orders = pd.read_csv("data/processed/orders_clean.csv")
customers = pd.read_csv("data/processed/customers_clean.csv")

# Convert order date
orders["order_ts"] = pd.to_datetime(orders["order_ts"])

# Keep completed orders before snapshot
completed = orders[
    (orders["status"].str.lower() == "completed") &
    (orders["order_ts"] < snapshot)
].copy()

# Calculate RFM
rfm = completed.groupby("customer_id").agg(
    last_order_ts=("order_ts", "max"),
    frequency=("order_id", "nunique"),
    monetary=("order_amount", "sum")
).reset_index()

rfm["recency"] = (
    snapshot - rfm["last_order_ts"]
).dt.days

# Save RFM table
rfm = rfm[
    ["customer_id", "recency", "frequency", "monetary"]
]

rfm.to_csv("data/processed/rfm.csv", index=False)

print("RFM TABLE CREATED!")
print("Customers:", len(rfm))
print(rfm.head())
print("\nRFM saved to data/processed/rfm.csv")

print("\nRFM STATISTICS:")
print(rfm[["recency", "frequency", "monetary"]].describe())
print("\nRecency Median:", rfm["recency"].median())