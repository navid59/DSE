import threading
import time
import csv
import happybase
import random
from datetime import datetime

# Configuration
HBASE_HOST = 'localhost'
HBASE_PORT = 9090
TABLE_NAME = 'test_table'
COLUMN_FAMILY = 'cf1'
COLUMN_QUALIFIER = 'value'
NUM_THREADS = 5
DURATION_SECONDS = 60
CSV_FILE = './Report/multi_threaded_load_test_report.csv'

def connect():
    return happybase.Connection(HBASE_HOST, port=HBASE_PORT)

def setup_table():
    print("[SETUP] Connecting to HBase...")
    connection = connect()
    try:
        connection.open()
        tables = connection.tables()
        if TABLE_NAME.encode() in tables:
            print(f"[SETUP] Table '{TABLE_NAME}' exists. Deleting...")
            connection.disable_table(TABLE_NAME)
            connection.delete_table(TABLE_NAME)
            print(f"[SETUP] Table '{TABLE_NAME}' deleted.")

        print(f"[SETUP] Creating table '{TABLE_NAME}'...")
        connection.create_table(TABLE_NAME, {COLUMN_FAMILY: dict()})
        print(f"[SETUP] Table '{TABLE_NAME}' created.")
    except Exception as e:
        print(f"[ERROR] During table setup: {e}")
    finally:
        connection.close()

def worker(thread_id, results, stop_event):
    connection = connect()
    connection.open()
    table = connection.table(TABLE_NAME)
    count = 0

    while not stop_event.is_set():
        key = f'thread{thread_id}-row{count}'
        value = f'value-{random.randint(1, 1000)}'
        
        try:
            start_put = time.time()
            table.put(key, {f'{COLUMN_FAMILY}:{COLUMN_QUALIFIER}': value})
            put_latency = (time.time() - start_put) * 1000

            start_get = time.time()
            row = table.row(key)
            get_latency = (time.time() - start_get) * 1000
            retrieved_value = row.get(f'{COLUMN_FAMILY}:{COLUMN_QUALIFIER}'.encode())

            results.append({
                'thread_id': thread_id,
                'operation': 'put_get',
                'key': key,
                'value': retrieved_value.decode() if retrieved_value else None,
                'put_latency_ms': round(put_latency, 2),
                'get_latency_ms': round(get_latency, 2),
                'timestamp': datetime.utcnow().isoformat()
            })

            print(f"[THREAD {thread_id}] {key} | Put: {put_latency:.2f} ms | Get: {get_latency:.2f} ms")
            count += 1

        except Exception as e:
            print(f"[ERROR] Thread {thread_id}: {e}")
            break

    connection.close()

def write_csv(results):
    print(f"[CSV] Writing results to {CSV_FILE}...")
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print("[CSV] Done.")

def main():
    print("[MAIN] Setting up HBase table...")
    setup_table()

    print(f"[MAIN] Starting test with {NUM_THREADS} threads for {DURATION_SECONDS} seconds...")
    threads = []
    results = []
    stop_event = threading.Event()

    for i in range(NUM_THREADS):
        t = threading.Thread(target=worker, args=(i, results, stop_event))
        t.start()
        threads.append(t)

    time.sleep(DURATION_SECONDS)
    stop_event.set()

    for t in threads:
        t.join()

    if results:
        write_csv(results)
    else:
        print("[MAIN] No results collected.")

    print("[MAIN] Test completed.")

if __name__ == '__main__':
    main()
