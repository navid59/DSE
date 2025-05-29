import happybase
import time
import random
import csv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='happybase')

# HBase config
HOST = 'localhost'
PORT = 9090
TABLE_NAME = 'test_table'
COLUMN_FAMILY = 'cf1'

# Test config
NUM_THREADS = 5
DURATION_SECONDS = 60  # 1 minute test duration

# Output path
REPORT_FOLDER = 'Report'
os.makedirs(REPORT_FOLDER, exist_ok=True)
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')
CSV_FILE = os.path.join(REPORT_FOLDER, f'baseline_results_{TIMESTAMP}.csv')

def worker(thread_id, stop_time):
    results = []
    op_count = 0
    last_print = time.time()

    # Use independent connection per thread
    connection = happybase.Connection(HOST, port=PORT)
    connection.open()
    table = connection.table(TABLE_NAME)

    while time.time() < stop_time:
        operation = random.choice(['put', 'get'])
        row_key = f'row{random.randint(1, 1000)}'.encode()
        column = f'{COLUMN_FAMILY}:value'.encode()
        value = f'value-{random.randint(1, 100000)}'.encode()

        start_time = time.time()
        try:
            if operation == 'put':
                table.put(row_key, {column: value})
            else:
                _ = table.row(row_key)
            success = True
        except Exception as e:
            success = False
        end_time = time.time()

        latency_ms = (end_time - start_time) * 1000
        results.append({
            'timestamp': datetime.now().isoformat(),
            'thread_id': thread_id,
            'operation': operation,
            'latency_ms': latency_ms,
            'success': success
        })

        op_count += 1
        if time.time() - last_print >= 10:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Thread {thread_id}: performed {op_count} operations so far")
            last_print = time.time()

    connection.close()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Thread {thread_id} finished. Total operations: {op_count}")
    return results

def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting baseline load test with {NUM_THREADS} threads...")
    stop_time = time.time() + DURATION_SECONDS
    all_results = []

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = [executor.submit(worker, i, stop_time) for i in range(NUM_THREADS)]
        for future in as_completed(futures):
            all_results.extend(future.result())

    # Write results to CSV
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp', 'thread_id', 'operation', 'latency_ms', 'success'])
        writer.writeheader()
        writer.writerows(all_results)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Load test completed. Results saved to: {CSV_FILE}")

if __name__ == '__main__':
    main()
