import pandas as pd

#Load Raw Data
orders = pd.read_csv("data/raw/orders.csv", keep_default_na=False)
customers = pd.read_csv("data/raw/customers.csv", keep_default_na=False)
tickets = pd.read_csv("data/raw/tickets.csv", keep_default_na=False)

print("\n=============RAW DATA AUDIT==============")

#Orders Audit
print("\nOrders")
print("Rows:", len(orders))
print("Exact duplicate rows:", orders.duplicated().sum())
print("Pending Status:",(orders["status"].str.lower() =="pending").sum())
print("Distinct order_id:",orders["order_id"].nunique())

#Order Amount Audit
amount = pd. to_numeric(orders["order_amount"], errors="coerce")
print("Non-numeric order amounts:",amount.isna().sum())

#Delivery Audit
delivery = pd. to_numeric(orders["delivery_minutes"], errors="coerce")
print("Negative delivery Minutes:",(delivery < 0).sum())
print("Blank Delivery Minutes:",orders["delivery_minutes"].eq("").sum())

#Customers Audit
print("\nCustomers")
print("\nBlank Ages:",customers["age"].eq("").sum())

age = pd. to_numeric(customers["age"], errors="coerce")
print("Ages outside 10-100:", ((age < 10) | (age > 100)).sum())

print("Distinct raw city spellings:",customers["city"].nunique())
print("Distinct raw gender spellings:",customers["gender"].nunique())
print("Blank genders:",customers["gender"].eq("").sum())

#Tickets audit
print("\nTickets")
print("Rows:", len(tickets))
print("Columns:",tickets.columns.tolist())

print("\n=========AUDIT COMPLETED===========")