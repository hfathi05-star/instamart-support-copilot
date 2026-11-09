
import pandas as pd

# Load cleaned tickets data
tickets = pd.read_csv("data/processed/tickets_clean.csv")

print("TICKET ANALYSIS")
print("------------------------")

# Total tickets
print("\nTotal Tickets:", len(tickets))

# Display column names
print("\nTicket Columns:")
print(tickets.columns.tolist())

# Ticket category distribution
print("\nTicket Categories:")
print(tickets["true_category"].value_counts())

# Sample tickets
print("\nSample Tickets:")
print(tickets[["ticket_id", "text", "true_category"]].head(5))

# Missing values
print("\nMissing Values:")
print(tickets.isnull().sum())

print("\nTICKET ANALYSIS COMPLETED!")
