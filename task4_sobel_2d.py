
import numpy as np
from numba import cuda

@cuda.jit
def sobel_x_kernel(d_in, d_out, rows, cols):
    col, row = cuda.grid(2)

    if row < rows and col < cols:
        if row > 0 and row < rows - 1 and col > 0 and col < cols - 1:
            value = (
                -1.0 * d_in[row - 1, col - 1]
                + 1.0 * d_in[row - 1, col + 1]
                - 2.0 * d_in[row, col - 1]
                + 2.0 * d_in[row, col + 1]
                - 1.0 * d_in[row + 1, col - 1]
                + 1.0 * d_in[row + 1, col + 1]
            )
            d_out[row, col] = value
        else:
            d_out[row, col] = 0.0


def run_sobel(h_img):
    rows, cols = h_img.shape

    d_in = cuda.to_device(h_img)
    d_out = cuda.device_array((rows, cols), dtype=np.float32)

    threads_2d = (16, 16)
    blocks_2d = (
        (cols + 15) // 16,
        (rows + 15) // 16
    )

    sobel_x_kernel[blocks_2d, threads_2d](d_in, d_out, rows, cols)

    return d_out.copy_to_host()


if __name__ == "__main__":
    h_img = np.ones((2048, 2048), dtype=np.float32)

    result = run_sobel(h_img)

    assert np.allclose(result, 0.0)

    print("TASK 4 PASSED")
    print("Image shape:", h_img.shape)
    print("Threads per block:", (16, 16))
    print("Output shape:", result.shape)
    print("Maximum absolute value:", np.max(np.abs(result)))
    print("First 5x5 output:")
    print(result[:5, :5])
