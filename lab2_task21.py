import threading
import math
import time

N = 1_000_000
STEP = 1.0 / N

def run_naive_race(num_threads):
    shared_sum = [0.0]
    threads = []
    chunk_size = N // num_threads

    def worker(start, end):
        for i in range(start, end):
            x = (i + 0.5) * STEP

            # Naive shared update - no lock
            shared_sum[0] += 4.0 / (1.0 + x * x)

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


print("Task 2.1 - Race Condition Quantification")
print("------------------------------------------------")
print("Threads | Calculated Pi | Absolute Error | Time")
print("------------------------------------------------")

for p in [1, 2, 4, 8]:
    start_time = time.perf_counter()

    pi_value = run_naive_race(p)

    end_time = time.perf_counter()

    error = abs(pi_value - math.pi)
    elapsed = end_time - start_time

    print(
        f"{p:7d} | {pi_value:.12f} | "
        f"{error:.2e} | {elapsed:.4f}s"
    )
