import matplotlib.pyplot as plt

threads = [1, 2, 4, 8]

measured_speedup = [1.00, 1.95, 3.25, 4.98]
ideal_speedup = [1, 2, 4, 8]

plt.figure(figsize=(8, 5))

plt.plot(
    threads,
    measured_speedup,
    marker="o",
    label="Measured Speedup"
)

plt.plot(
    threads,
    ideal_speedup,
    marker="o",
    linestyle="--",
    label="Linear Ideal Speedup"
)

plt.xlabel("Number of Threads (P)")
plt.ylabel("Speedup S(P)")
plt.title("Measured Speedup vs Linear Ideal Speedup")

plt.xticks(threads)
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("lab2_speedup_graph.png", dpi=300)

print("Graph saved as lab2_speedup_graph.png")

plt.show()
