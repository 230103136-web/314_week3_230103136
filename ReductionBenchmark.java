import java.util.concurrent.ThreadLocalRandom;

public class ReductionBenchmark {

    static final long TOTAL_POINTS = 100_000_000L;

    public static long runBenchmark(int numThreads) throws InterruptedException {

        Thread[] threads = new Thread[numThreads];
        long[] localHits = new long[numThreads];

        long pointsPerThread = TOTAL_POINTS / numThreads;
        long remainder = TOTAL_POINTS % numThreads;

        long startTime = System.nanoTime();

        for (int i = 0; i < numThreads; i++) {

            final int threadId = i;

            final long iterations =
                    pointsPerThread + (i < remainder ? 1 : 0);

            threads[i] = new Thread(() -> {

                long hits = 0;

                ThreadLocalRandom random =
                        ThreadLocalRandom.current();

                for (long j = 0; j < iterations; j++) {

                    double x = random.nextDouble();
                    double y = random.nextDouble();

                    if (x * x + y * y <= 1.0) {
                        hits++;
                    }
                }

                localHits[threadId] = hits;
            });

            threads[i].start();
        }

        for (Thread thread : threads) {
            thread.join();
        }

        long totalHits = 0;

        for (long hits : localHits) {
            totalHits += hits;
        }

        long endTime = System.nanoTime();

        double pi =
                4.0 * totalHits / TOTAL_POINTS;

        System.out.printf(
                "Threads: %d | Pi: %.6f%n",
                numThreads,
                pi
        );

        return endTime - startTime;
    }


    public static void main(String[] args)
            throws InterruptedException {

        int[] threadCounts = {1, 2, 4, 8, 16, 32};

        double[] runtimes =
                new double[threadCounts.length];

        System.out.println(
                "=== OpenMP-Style Reduction Benchmark ==="
        );

        for (int i = 0; i < threadCounts.length; i++) {

            long runtime =
                    runBenchmark(threadCounts[i]);

            runtimes[i] =
                    runtime / 1_000_000.0;
        }

        double baseline = runtimes[0];

        System.out.println();
        System.out.println(
                "Threads | Runtime(ms) | Speedup | Efficiency"
        );

        for (int i = 0; i < threadCounts.length; i++) {

            double speedup =
                    baseline / runtimes[i];

            double efficiency =
                    (speedup / threadCounts[i]) * 100.0;

            System.out.printf(
                    "%7d | %11.2f | %6.2fx | %9.2f%%%n",
                    threadCounts[i],
                    runtimes[i],
                    speedup,
                    efficiency
            );
        }
    }
}
