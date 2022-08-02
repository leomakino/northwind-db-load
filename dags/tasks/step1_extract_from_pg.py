import psycopg2
import os
import sys

# Receive the date as the first command line argument
date = sys.argv[1]

# Connect to Postgres
try:
    conn = psycopg2.connect(
        database="northwind",
        user="northwind_user",
        password="thewindisblowing",
        host="0.0.0.0",
        port=5434
    )
except:
    print("Connection to Postgres has failed \nPlease check the access credentials")
    exit()

# Open cursor to perform database operations
cur = conn.cursor()

# Query the database's table names
cur.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")

# List of the table names
tables = [table[0] for table in cur.fetchall()]

# Export all tables locally
for table in tables:
    os.makedirs(f"../../local_data/postgres/{table}/{date}/", exist_ok=True)
    with open(f"../../local_data/postgres/{table}/{date}/{table}.csv", "w") as file:
        cur.copy_expert(
            f"""COPY {table} TO STDOUT WITH CSV HEADER""", file)

# Close communication with database
cur.close()
conn.close()
