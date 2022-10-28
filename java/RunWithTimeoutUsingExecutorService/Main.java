import java.util.concurrent.*;
import java.util.function.Function;

public class Main {
    public static String fail() {
        System.out.println("failing");
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return "done!";
    }

    public static String scc() {
        System.out.println("succeeding");
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return "done!";
    }

    public static String err() {
        System.out.println("error");
        throw new RuntimeException("error");
    }

    public static String looping() {
        int counter = 0;
        while (counter < 1000000000) {
            System.out.println("looping");
            try {
                Thread.sleep(1000);
                counter++;
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        return "done!";
    }

    public static <R> R runWithTimeout(int timeout, Function<Void, R> func) throws TimeoutException, InterruptedException, ExecutionException {
        ExecutorService executor = Executors.newSingleThreadScheduledExecutor();
        Callable<R> task = new Callable<R>() {
            public R call() throws InterruptedException {
                return func.apply(null);
            }
        };
        Future<R> future = executor.submit(task);
        try {
            R result = future.get(timeout, TimeUnit.SECONDS);
            return result;
        } finally {
            executor.shutdown();
        }
    }

    public static void main(String[] args) {
        try {
            String result = runWithTimeout(2, (Void) -> fail());
            System.out.println(result);
        } catch (TimeoutException e) {
            System.out.println("Timeout");
        } catch (InterruptedException e) {

        } catch (ExecutionException e) {

        }

        try {
            String result = runWithTimeout(2, (Void) -> scc());
            System.out.println(result);
        } catch (TimeoutException e) {
            System.out.println("Timeout");
        } catch (InterruptedException e) {

        } catch (ExecutionException e) {

        }

        try {
            String result = runWithTimeout(2, (Void) -> err());
            System.out.println(result);
        } catch (TimeoutException e) {
            System.out.println("Timeout");
        } catch (InterruptedException e) {

        } catch (ExecutionException e) {
            System.out.println("Execution Exception");
        }

        // Notice that `looping` will time out, but will keep on looping, so `run_with_timeout` will not terminate the thread
        // Connection delays, etc. will cause a timeout, but the thread will keep on running until it is FINISHED!
        // Getting `TimeoutException` means that the program has ignored the thread, the thread is not FINISHED!
        // Use with caution!
        try {
            String result = runWithTimeout(2, (Void) -> looping());
            System.out.println(result);
        } catch (TimeoutException e) {
            System.out.println("Timeout");
        } catch (InterruptedException e) {

        } catch (ExecutionException e) {

        }
        try {
            Thread.sleep(1000000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}