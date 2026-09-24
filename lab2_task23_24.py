import time
from numba import njit, prange, set_num_threads, get_num_threads

N = 10_000_000
TRIALS = 5

@njit(parallel=True)
def calc_pi_reduction(num_steps):
    step = 1.0 / num_steps
    total_sum = 0.0

    for i in prange(num_steps):
        x = (i + 0.5) * step
        total_sum += 4.0 / (1.0 + x * x)

    return total_sum * step


# JIT warm-up
calc_pi_reduction(1000)

requested_threads = [1, 2, 4, 8, 16]
results = {}

print("Task 2.3 & 2.4 - Strong Scaling Benchmark")
print("==============================================================")

for p in requested_threads:

    try:
        set_num_threads(p)

        times = []

        for trial in range(TRIALS):
            start = time.perf_counter()
            pi_value = calc_pi_reduction(N)
            end = time.perf_counter()

            times.append(end - start)

        avg_time = sum(times) / TRIALS
        results[p] = (avg_time, pi_value)

    except ValueError:
        results[p] = None


t1 = results[1][0]

print("Threads | Average Time | Speedup | Efficiency | Pi")
print("==============================================================")

for p in requested_threads:

    if results[p] is None:
        print(f"{p:7d} | NOT SUPPORTED BY CURRENT RUNTIME/HARDWARE")
        continue

    avg_time, pi_value = results[p]

    speedup = t1 / avg_time
    efficiency = speedup / p

    print(
        f"{p:7d} | "
        f"{avg_time:12.6f} | "
        f"{speedup:7.2f}x | "
        f"{efficiency:9.2%} | "
        f"{pi_value:.12f}"
    )
