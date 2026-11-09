
import pandas as pd

# Load cleaned tickets
tickets = pd.read_csv("data/processed/tickets_clean.csv")

print("TICKET CATEGORY ANALYSIS")
print("----------------------")

# Category distribution
print("\nCategory Counts:")
print(tickets["true_category"].value_counts())

# Category percentages
print("\nCategory Percentage:")
print(
    (tickets["true_category"].value_counts(normalize=True) * 100)
    .round(2)
)

# Missing category values
print("\nMissing Categories:")
print(tickets["true_category"].isnull().sum())

# Sample ticket text for each category
print("\nSample Tickets by Category:")
for category in tickets["true_category"].unique():
    print(f"\nCategory: {category}")
    print(
        tickets[tickets["true_category"] == category]["text"]
        .head(2)
        .to_string(index=False)
    )

print("\nCATEGORY ANALYSIS COMPLETED!")
