# CUDA Lab 02: Advanced Geometries & Stencils

**Student ID:** 230103136  
**Allocated GPU Node:** Tesla T4  
**CUDA Compute Capability:** 7.5  
**Official Verification Token:** 489F8F38EEF7208C9D0C

## Task 1: Warp Divergence Microbenchmark

I tested three CUDA kernels to compare their execution times. Each kernel performed 1000 iterations per element. I used 10 trials to calculate the average execution time.

| Kernel | Average Time (ms) |
|---|---:|
| Uniform Path | 24.25 |
| Full Divergence | 93.51 |
| Warp-Aligned Branching | 46.87 |

The uniform kernel was the fastest because all threads followed the same instructions. The divergent kernel was the slowest because neighboring threads executed different branches. The warp-aligned kernel was faster than the divergent one because threads in the same warp followed the same path.

## Task 2: 1D Boundary Stencil

I implemented a 3-point smoothing filter using CUDA. For the first and last elements, I used boundary clamping to avoid accessing invalid memory.

- Array size: 10007
- Threads per block: 256
- Maximum difference: 5.9604645e-08
- Result: PASSED

The GPU output matched the CPU reference within the required tolerance.

## Task 3: Grid-Stride Scaling

I used a grid-stride loop to multiply all array elements by 4.25.

- Array size: 16777216
- Threads per block: 256
- Blocks per grid: 64
- Total GPU threads: 16384
- Scaling factor: 4.25
- Result: PASSED

The grid-stride loop allowed a smaller number of GPU threads to process a much larger array. All elements were scaled correctly.

## Task 4: 2D Sobel Horizontal Filter

I implemented a Sobel-X filter using a 2D CUDA grid.

- Image size: 2048 x 2048
- Threads per block: (16, 16)
- Maximum absolute output value: 0.0
- Result: PASSED

I tested the filter on a constant image. The output was zero because there were no horizontal changes in pixel values. Border pixels were also set to zero.

## Automated Verification

All required verification tests passed.

- Task 2: PASS
- Task 3: PASS
- Task 4: PASS

**Official Submission Token:** 489F8F38EEF7208C9D0C

## Conclusion

In this lab, I learned how warp divergence affects GPU performance, how to handle array boundaries safely, how grid-stride loops process large arrays, and how to use 2D CUDA kernels for image filtering.
