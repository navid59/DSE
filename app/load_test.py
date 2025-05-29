import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import happybase
import time
import random

# Connect to HBase via Thrift
connection = happybase.Connection('localhost', port=9090)
connection.open()

# Table and column family settings
table_name = 'test_table'
column_family = 'cf1'

# Recreate the table if it exists
if table_name.encode() in connection.tables():
    print(f"Table '{table_name}' already exists. Deleting it...")
    connection.disable_table(table_name)
    connection.delete_table(table_name)
    print(f"Table '{table_name}' deleted.")

# Create the new table
connection.create_table(table_name, {column_family: dict()})
print(f"Table '{table_name}' created with column family '{column_family}'.")

# Connect to the table
table = connection.table(table_name)

# Perform test writes and reads
for i in range(1, 101):
    key = f'row{i}'
    value = f'value{i}-{random.randint(1, 100)}'

    # Measure put time
    start_put = time.time()
    table.put(key, {f'{column_family}:value': value})
    put_latency = (time.time() - start_put) * 1000  # ms

    # Measure get time
    start_get = time.time()
    row = table.row(key)
    get_latency = (time.time() - start_get) * 1000  # ms

    print(f"[{i}] Put: {put_latency:.2f} ms | Get: {get_latency:.2f} ms | Value: {row.get(f'{column_family}:value'.encode())}")

connection.close()
