from concurrent.futures import ThreadPoolExecutor
import time

def worker_task(thread_id):
    # Small task executed by each thread
    return thread_id * thread_id

def measure_team_time(num_threads):
    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(worker_task, tid)
            for tid in range(num_threads)
        ]

        for f in futures:
            f.result()

    end = time.perf_counter()
    return end - start

if __name__ == "__main__":
    thread_counts = [1, 2, 4, 8, 16, 32, 64]

    print("Task 1.2 - Thread Oversubscription Sweep")
    print("-----------------------------------------")
    print("Threads | Execution Time (seconds)")
    print("-----------------------------------------")

    for p in thread_counts:
        elapsed = measure_team_time(p)
        print(f"{p:7d} | {elapsed:.6f}")
