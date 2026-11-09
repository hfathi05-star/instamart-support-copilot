
import pandas as pd

# Load cleaned orders
orders = pd.read_csv("data/clean/orders.csv")

# Completed orders only
completed = orders[orders["status"] == "completed"]

print("ORDERS ANALYSIS")
print("----------------")

print("Total orders:", len(orders))
print("Completed orders:", len(completed))

print("\nCompleted Order Amount Statistics:")
print(completed["order_amount"].describe())

print("\nAverage Order Amount:")
print(round(completed["order_amount"].mean(), 2))

print("\nMedian Order Amount:")
print(round(completed["order_amount"].median(), 2))
