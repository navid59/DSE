# HBase Distributed System Testing

This project is designed to test and evaluate the performance of an HBase distributed setup using Docker and multi-threaded Python load testing scripts. It simulates real-world scenarios and captures key performance metrics such as latency, throughput, and fault tolerance.

## 📦 Components

- **Docker Compose** setup for:
  - Apache ZooKeeper
  - HBase Master
  - HBase RegionServers (configurable)
- **Python Load Test Script** using `happybase` and `threading`
- **CSV Result Output** for post-analysis
- **Real-time logging** to console during execution

---


## 📊 Output

- Real-time operation logs printed in terminal
- Results saved to `*.csv` in the **Report** folder.

---

## 🧪 Tested Scenarios

### ✅ Scenario 1: Baseline Load Test

- **Goal**: Measure normal performance under steady load.
- **Setup**: 1 HBase Master, 2 RegionServers, 5–10 threads.
- **Metrics**: Latency, throughput, error rate.
- **Why**: Establish baseline system behavior.

### 🔧 Scenario 2: Failure Simulation

- **Goal**: Test fault tolerance by stopping one RegionServer mid-test.
- **Setup**: Same as baseline.
- **How**: After 30 seconds of load
- **Metrics**: Error spike, latency, recovery time.
- **Why**: Validate system resilience.

### 📈 Scenario 3: Scaling Test

- **Goal**: See if adding RegionServers improves throughput.
- **Steps**:
  1. Run with 1 RS
  2. Then with 2 RS
  3. Then with 3 RS
- **Metrics**: Latency and throughput as RS count changes.
- **Why**: Measure horizontal scalability.

### 🔥 Scenario 4: Stress Test

- **Goal**: Push HBase to its limits.
- **Setup**: 2–3 RS, 20–50 threads.
- **Duration**: 5–10 minutes.
- **Metrics**: Max sustainable throughput, error rates, bottlenecks.

---

## 📌 Requirements

- Docker
- Python 3.7+
- Python dependencies: `happybase`

---

## 🧠 Notes

- This test made by geting help of **Open AI**
- By getting help of **Open AI** , I tried to undrestand the progress
