import sys
import os

# Receive the date as the first command line argument
date = sys.argv[1]

# Create directory if not exists
os.makedirs(f"../local_data/csv/{date}/", exist_ok=True)

# Copy csv to local file system
os.system(
    f"cp ../data/order_details.csv ../local_data/csv/{date}/order_details.csv")
