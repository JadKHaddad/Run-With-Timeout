use std::{
    collections::HashMap,
    error::Error,
    sync::mpsc::{self, RecvTimeoutError},
    thread,
    time::Duration,
};

#[derive(Debug)]
struct TimeoutError;

fn run_with_timeout<F, T>(f: F, timeout: Duration) -> Result<T, TimeoutError>
where
    F: FnOnce() -> T + Send + Sync + 'static,
    T: Send + Sync + 'static,
{
    let (tx, rx) = mpsc::channel();
    let _ = thread::spawn(move || {
        let result = f();
        match tx.send(result) {
            Ok(()) => {} // everything good
            Err(_) => {} // we have been released, don't panic
        }
    });

    match rx.recv_timeout(timeout) {
        Ok(result) => Ok(result),
        Err(RecvTimeoutError::Timeout) => Err(TimeoutError),
        Err(RecvTimeoutError::Disconnected) => unreachable!(),
    }
}

#[allow(dead_code)]
#[derive(Debug)]
struct Foo {
    bar: String,
    bar_vec: Vec<String>,
    bar_map: HashMap<String, String>,
}

fn return_foo() -> Foo {
    thread::sleep(Duration::from_secs(2));
    Foo {
        bar: "bar".to_string(),
        bar_vec: vec!["bar".to_string()],
        bar_map: [("bar".to_string(), "bar".to_string())]
            .iter()
            .cloned()
            .collect(),
    }
}

fn err() -> Result<String, Box<dyn Error + Send + Sync>> {
    thread::sleep(Duration::from_secs(2));
    let result = std::fs::read_to_string("not_there.txt")?;
    Ok(result)
}

fn scc() -> Result<String, Box<dyn Error + Send + Sync>> {
    thread::sleep(Duration::from_secs(2));
    let result = std::fs::read_to_string("there.txt")?;
    Ok(result)
}

fn looping() -> ! {
    loop {
        thread::sleep(Duration::from_secs(1));
        println!("looping");
    }
}

fn main() {
    // This will time out
    let result = run_with_timeout(
        || {
            thread::sleep(Duration::from_secs(2));
            42
        },
        Duration::from_secs(1),
    );
    println!("Result: {:?}", result);

    // This will not time out
    let result = run_with_timeout(
        || {
            thread::sleep(Duration::from_secs(2));
            42
        },
        Duration::from_secs(3),
    );
    println!("Result: {:?}", result);

    // This will time out (Custom type)
    let result = run_with_timeout(|| return_foo(), Duration::from_secs(1));
    println!("Result: {:?}", result);

    // This will not time out (Custom type)
    let result = run_with_timeout(|| return_foo(), Duration::from_secs(3));
    println!("Result: {:?}", result);

    // This will fail with dynamic Error
    let result = run_with_timeout(|| err(), Duration::from_secs(3));
    println!("Result: {:?}", result);

    // This will succeed (dynamic Error)
    let result = run_with_timeout(|| scc(), Duration::from_secs(3));
    println!("Result: {:?}", result);

    // This will loop forever
    let result = run_with_timeout(|| looping(), Duration::from_secs(3));
    // Notice that `looping` will time out, but will keep on looping, so `run_with_timeout` will not terminate the thread
    // Connection delays, etc. will cause a timeout, but the thread will keep on running until it is FINISHED!
    // Getting `TimeoutError` means that the program has ignored the thread, the thread is not FINISHED!
    // Use with caution!
    // Use Tokio instead!
    println!("Result: {:?}", result);
    thread::sleep(Duration::from_secs(10));
}
