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
    }
}