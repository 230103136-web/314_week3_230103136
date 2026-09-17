import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.atomic.AtomicLong;

public class SynchronizationTrap {

    static final long TOTAL_POINTS = 50_000_000L;
    static final int NUM_THREADS = 4;

    static AtomicLong totalHits = new AtomicLong(0);

    public static void main(String[] args) throws InterruptedException {

        // Part 2A: 4 threads with AtomicLong
        long startParallel = System.nanoTime();

        Thread[] threads = new Thread[NUM_THREADS];
        long pointsPerThread = TOTAL_POINTS / NUM_THREADS;

        for (int i = 0; i < NUM_THREADS; i++) {

            threads[i] = new Thread(() -> {

                for (long j = 0; j < pointsPerThread; j++) {

                    double x = ThreadLocalRandom.current().nextDouble();
                    double y = ThreadLocalRandom.current().nextDouble();

                    if (x * x + y * y <= 1.0) {
                        totalHits.incrementAndGet();
                    }
                }
            });

            threads[i].start();
        }

        for (Thread thread : threads) {
            thread.join();
        }

        long endParallel = System.nanoTime();

        double parallelPi =
                4.0 * totalHits.get() / TOTAL_POINTS;

        double parallelTime =
                (endParallel - startParallel) / 1_000_000.0;


        // Part 2B: Single-threaded version
        long singleHits = 0;

        long startSingle = System.nanoTime();

        for (long i = 0; i < TOTAL_POINTS; i++) {

            double x = ThreadLocalRandom.current().nextDouble();
            double y = ThreadLocalRandom.current().nextDouble();

            if (x * x + y * y <= 1.0) {
                singleHits++;
            }
        }

        long endSingle = System.nanoTime();

        double singlePi =
                4.0 * singleHits / TOTAL_POINTS;

        double singleTime =
                (endSingle - startSingle) / 1_000_000.0;


        System.out.println("=== AtomicLong (4 Threads) ===");
        System.out.println("Estimated Pi: " + parallelPi);
        System.out.println("Runtime: " + parallelTime + " ms");

        System.out.println();

        System.out.println("=== Single Thread ===");
        System.out.println("Estimated Pi: " + singlePi);
        System.out.println("Runtime: " + singleTime + " ms");
    }
}
