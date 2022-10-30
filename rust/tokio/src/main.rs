use std::collections::HashMap;
use std::error::Error;
use tokio::time::timeout;
use tokio::time::{sleep, Duration};

async fn num() -> i32 {
    sleep(Duration::from_secs(2)).await;
    42
}

#[allow(dead_code)]
#[derive(Debug)]
struct Foo {
    bar: String,
    bar_vec: Vec<String>,
    bar_map: HashMap<String, String>,
}

async fn return_foo() -> Foo {
    sleep(Duration::from_secs(2)).await;
    Foo {
        bar: "bar".to_string(),
        bar_vec: vec!["bar".to_string()],
        bar_map: [("bar".to_string(), "bar".to_string())]
            .iter()
            .cloned()
            .collect(),
    }
}

async fn err() -> Result<String, Box<dyn Error>> {
    sleep(Duration::from_secs(2)).await;
    let result = std::fs::read_to_string("not_there.txt")?;
    Ok(result)
}

async fn scc() -> Result<String, Box<dyn Error>> {
    sleep(Duration::from_secs(2)).await;
    let result = std::fs::read_to_string("there.txt")?;
    Ok(result)
}

async fn looping() -> ! {
    loop {
        sleep(Duration::from_secs(1)).await;
        println!("looping");
    }
}

#[tokio::main]
async fn main() {
    // This will time out
    let result = timeout(Duration::from_secs(1), num()).await;
    println!("Result: {:?}", result);

    // This will not time out
    let result = timeout(Duration::from_secs(3), num()).await;
    println!("Result: {:?}", result);

    // This will time out (Custom type)
    let result = timeout(Duration::from_secs(1), return_foo()).await;
    println!("Result: {:?}", result);

    // This will not time out (Custom type)
    let result = timeout(Duration::from_secs(3), return_foo()).await;
    println!("Result: {:?}", result);

    // This will fail with dynamic Error
    let result = timeout(Duration::from_secs(3), err()).await;
    println!("Result: {:?}", result);

    // This will succeed (dynamic Error)
    let result = timeout(Duration::from_secs(3), scc()).await;
    println!("Result: {:?}", result);

    // This will loop forever
    // Tokio will terminate the task if it times out
    let result = timeout(Duration::from_secs(3), looping()).await;
    println!("Result: {:?}", result);
    
    sleep(Duration::from_secs(10)).await;
}
