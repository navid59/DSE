import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import happybase
import time
import random

def main():
    try:
        print("Starting connection to HBase Thrift server on localhost:9090 ...")
        connection = happybase.Connection('localhost', port=9090)
        connection.open()
        print("Connection opened successfully.")

        table_name = 'test_table'
        column_family = 'cf1'

        print("Checking if table exists...")
        if table_name.encode() in connection.tables():
            print(f"Table '{table_name}' exists. Deleting...")
            connection.disable_table(table_name)
            connection.delete_table(table_name)
            print(f"Table '{table_name}' deleted.")

        print(f"Creating table '{table_name}' with column family '{column_family}'...")
        connection.create_table(table_name, {column_family: dict()})
        print("Table created successfully.")

        table = connection.table(table_name)

        print("Starting test writes and reads...")
        for i in range(1, 101):
            key = f'row{i}'
            value = f'value{i}-{random.randint(1, 100)}'

            start_put = time.time()
            table.put(key, {f'{column_family}:value': value})
            put_latency = (time.time() - start_put) * 1000  # ms

            start_get = time.time()
            row = table.row(key)
            get_latency = (time.time() - start_get) * 1000  # ms

            stored_value = row.get(f'{column_family}:value'.encode())
            print(f"[{i}] Put: {put_latency:.2f} ms | Get: {get_latency:.2f} ms | Value: {stored_value}")

        print("Test completed, closing connection.")
        connection.close()

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
