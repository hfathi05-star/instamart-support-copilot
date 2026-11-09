import pandas as pd
import sqlite3
import os
#-----------------------------
#PART A - DATA LOADING
#-----------------------------

RAW_DIR = "data/raw"

print("Checking raw data files..")

for file in os.listdir(RAW_DIR):
    print(file)

#-----------------------------
#LOAD CUSTOMERS
#-----------------------------

customers = pd.read_csv("data/raw/customers.csv")

print("\nCustomers Data Loaded Successfully!")
print(customers.head())
print("Total Customers:", len(customers))

#-----------------------------
#LOAD ORDERS
#-----------------------------
orders = pd.read_csv("data/raw/orders.csv")

print("\nOrders Data Loaded Successfully!")
print(orders.head())
print("Total Orders:", len(orders))

#-----------------------------
#LOAD PRODUCTS
#-----------------------------

products = pd.read_csv("data/raw/products.csv")

print("\nProducts Data Loaded Successfully!")
print(products.head())
print("Total Products:", len(products))

#-----------------------------
#LOAD TICKETS
#-----------------------------

tickets = pd.read_csv("data/raw/tickets.csv")

print("\nTickets Data Loaded Successfully!")
print(tickets.head())
print("Total Tickets:", len(tickets))

#-----------------------------
#LOAD AGENT SCENARIOS
#-----------------------------

agent_scenarios = pd.read_csv("data/raw/agent_scenarios.csv")

print("\nAgent Scenarios Data Loaded Successfully!")
print(agent_scenarios.head())
print("Total Agent Scenarios:", len(agent_scenarios))

#-----------------------------
#LOAD POLICY EVALUATION
#-----------------------------

policy_eval = pd.read_csv("data/raw/policy_eval.csv")

print("\nPolicy Evaluation Loaded Successfully!")
print(policy_eval.head())
print("Total Policy Evaluation Rows:", len(policy_eval))

#-----------------------------
#COMPLETED
#-----------------------------

print("\nALL RAW DATA FILES LOADED SUCCESSFULLY!")

#-----------------------------
#SQLITE DATABASE INTEGRATION
#-----------------------------

import sqlite3
import os

os.makedirs("data/processed", exist_ok=True)

DB_PATH = "data/processed/instamart.db"

conn = sqlite3.connect(DB_PATH)

customers.to_sql("customers", conn, if_exists="replace", index=False)
orders.to_sql("orders", conn, if_exists="replace", index=False)
products.to_sql("products", conn, if_exists="replace", index=False)
tickets.to_sql("tickets", conn, if_exists="replace", index=False)
agent_scenarios.to_sql("agent_scenarios", conn, if_exists="replace", index=False)
policy_eval.to_sql("policy_eval", conn, if_exists="replace", index=False)

conn.close()

print("\nAll datasets successfully saved to SQLite!")
print("Database:", DB_PATH)




