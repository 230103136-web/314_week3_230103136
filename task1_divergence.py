
import numpy as np
import time
from numba import cuda

@cuda.jit
def uniform_kernel(arr):
    idx = cuda.grid(1)
    if idx < arr.size:
        x = arr[idx]
        for i in range(1000):
            x = x * 1.0001 + 0.0001
        arr[idx] = x

@cuda.jit
def divergent_kernel(arr):
    idx = cuda.grid(1)
    if idx < arr.size:
        x = arr[idx]
        if idx % 2 == 0:
            for i in range(1000):
                x = x * 1.0001 + 0.0001
        else:
            for i in range(1000):
                x = (x - 0.0001) / 1.0001
        arr[idx] = x

@cuda.jit
def aligned_kernel(arr):
    idx = cuda.grid(1)
    if idx < arr.size:
        x = arr[idx]
        warp_id = idx // 32

        if warp_id % 2 == 0:
            for i in range(1000):
                x = x * 1.0001 + 0.0001
        else:
            for i in range(1000):
                x = (x - 0.0001) / 1.0001
        arr[idx] = x

def benchmark(kernel, data):
    d_arr = cuda.to_device(data)
    threads = 256
    blocks = (data.size + threads - 1) // threads

    kernel[blocks, threads](d_arr)
    cuda.synchronize()

    times = []

    for i in range(10):
        start = time.perf_counter()
        kernel[blocks, threads](d_arr)
        cuda.synchronize()
        end = time.perf_counter()
        times.append((end - start) * 1000)

    return np.mean(times)

if __name__ == "__main__":
    data = np.ones(1 << 20, dtype=np.float32)

    print("Task 1: Warp Divergence")
    print("Uniform:", benchmark(uniform_kernel, data), "ms")
    print("Divergent:", benchmark(divergent_kernel, data), "ms")
    print("Warp Aligned:", benchmark(aligned_kernel, data), "ms")
