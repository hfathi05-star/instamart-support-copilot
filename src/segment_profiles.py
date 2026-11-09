import pandas as pd

df = pd.read_csv("data/processed/customer_segments.csv")

profiles = df.groupby("segment").agg(
    customers=("customer_id", "count"),
    avg_recency=("recency", "mean"),
    avg_frequency=("frequency", "mean"),
    avg_monetary=("monetary", "mean")
).round(2)

print("CUSTOMER SEGMENT PROFILES")
print("=========================")
print(profiles)

profiles.to_csv("data/processed/segment_profiles.csv")

print("\nProfiles saved successfully!")
print("\nTotal customers in file:",len(df))