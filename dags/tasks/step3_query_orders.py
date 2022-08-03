import psycopg2

# SQL statement for order and its details
order_and_details = """
    SELECT
        o.order_id,
        product_name,
        od.unit_price,
        quantity,
        discount,
        customer_id,
        employee_id,
        order_date
    FROM orders as o
    INNER JOIN order_details as od
    USING(order_id)
    INNER JOIN products
    USING(product_id)
    ORDER BY order_id
"""

# Connect to Postgres
try:
    conn = psycopg2.connect(
        database="northwind_data_analysis",
        user="admin",
        password="admin",
        host="final_db",
        port=5432
    )
except:
    print("Connection to Postgres has failed \nPlease check the access credentials")
    exit()

# Open cursor to perform database operations
cur = conn.cursor()

# Querying Data
cur.execute(f"{order_and_details}")

# Show query
[print(row) for row in cur.fetchall()]

# Export query as a CSV file
with open("../local_data/order_and_details.csv", "w") as file:
    cur.copy_expert(
        f"COPY ({order_and_details}) TO STDOUT WITH CSV HEADER", file)

# Close communication with database
cur.close()
conn.close()
