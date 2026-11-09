import pandas as pd

# Load cleaned customer data
df = pd.read_csv("data/processed/customers_clean.csv")

print("CUSTOMER DATA ANALYSIS")
print("----------------------")

print("Total Customers:", len(df))

print("\nCustomers by City:")
print(df["city"].value_counts())

print("\nGender Distribution:")
print(df["gender"].value_counts())

print("\nAverage Customer Age:")
print(df["age"].mean())

# Standardize gender values
df["gender"] = df["gender"].str.upper().str.strip()

df["gender"] = df["gender"].replace({"M": "MALE", "F": "FEMALE"})

print("\nStandardized Gender Distribution:")
print(df["gender"].value_counts())
print("\nTop 10 Customer Cities:")
print(df["city"].value_counts().head(10))
# Standardize city names
df["city"] = df["city"].str.title().str.strip()

print("\nCorrected City Distribution:")
print(df["city"].value_counts())

print("\nCustomer Age Statistics:")
print(df["age"].describe())

print("\nAge Groups:")
df["age_group"] = pd.cut(df["age"], bins=[0, 18, 30, 45, 60, 100], labels=["Below 18", "18-30", "31-45", "46-60", "Above 60"])
print(df["age_group"].value_counts())
                                                