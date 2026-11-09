import sqlite3
from pathlib import Path

conn = sqlite3.connect("data/instamart.db")

sql = Path("src/sql/queries.sql").read_text()

queries = sql.split(";")

for i, query in enumerate(queries, start=1):
    if query.strip():
        print(f"\nQUERY {i}")
        result = conn.execute(query)
        for row in result.fetchmany(10):
            print(row)

conn.close()