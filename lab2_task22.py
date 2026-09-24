import threading
import time
import math

N = 1_000_000
STEP = 1.0 / N

def serial_pi():
    total = 0.0

    for i in range(N):
        x = (i + 0.5) * STEP
        total += 4.0 / (1.0 + x * x)

    return total * STEP


def critical_pi(num_threads=4):
    shared_sum = [0.0]
    lock = threading.Lock()
    threads = []

    chunk_size = N // num_threads

    def worker(start, end):
        for i in range(start, end):
            x = (i + 0.5) * STEP
            term = 4.0 / (1.0 + x * x)

            # Critical section
            with lock:
                shared_sum[0] += term

    for t in range(num_threads):
        start = t * chunk_size
        end = N if t == num_threads - 1 else start + chunk_size

        thread = threading.Thread(
            target=worker,
            args=(start, end)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return shared_sum[0] * STEP


print("Task 2.2 - Critical Section Overhead")
print("------------------------------------")

# Serial baseline
start = time.perf_counter()
pi_serial = serial_pi()
serial_time = time.perf_counter() - start

# Critical section with 4 threads
start = time.perf_counter()
pi_critical = critical_pi(4)
critical_time = time.perf_counter() - start

overhead = ((critical_time - serial_time) / serial_time) * 100

print(f"Serial Pi:          {pi_serial:.12f}")
print(f"Serial Time:        {serial_time:.4f} s")
print()
print(f"Critical Pi:        {pi_critical:.12f}")
print(f"Critical Time:      {critical_time:.4f} s")
print()
print(f"Lock Overhead:      {overhead:.2f}%")
print(f"Slowdown:           {critical_time / serial_time:.2f}x")
