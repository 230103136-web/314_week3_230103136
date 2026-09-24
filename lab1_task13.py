from concurrent.futures import ThreadPoolExecutor
import math
import time

WORK = 10_000_000

def cpu_work(thread_id):
    total = 0.0

    for i in range(WORK):
        total += math.sqrt(i + 1)

    return total

def main():
    num_threads = 10

    print(f"Starting CPU workload with {num_threads} threads...")
    print(f"Each thread calculates {WORK:,} square roots.")

    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(cpu_work, tid)
            for tid in range(num_threads)
        ]

        for f in futures:
            f.result()

    end = time.perf_counter()

    print("All threads completed.")
    print(f"Execution Time: {end - start:.4f} seconds")

if __name__ == "__main__":
    main()
