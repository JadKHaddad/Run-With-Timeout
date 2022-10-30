#include <condition_variable>
#include <iostream>
#include <mutex>
#include <thread>

int my_function_that_might_block(int x)
{
    std::this_thread::sleep_for(std::chrono::seconds(10));
    return 1;
}

template<typename ret, typename T, typename... Rest>
using fn = std::function<ret(T, Rest...)>;

template<typename ret, typename T, typename... Rest>
ret wrap_my_slow_function(fn<ret, T, Rest...> f, T t, Rest... rest)
{
    std::mutex my_mutex;
    std::condition_variable my_condition_var;
    ret result = 0;

    std::unique_lock<std::mutex> my_lock(my_mutex);

    //
    // Spawn a thread to call my_function_that_might_block(). 
    // Pass in the condition variables and result by reference.
    //
    std::thread my_thread([&]() 
    {
        result = f(t, rest...);
        // Unblocks one of the threads currently waiting for this condition.
        my_condition_var.notify_one();
    });

    //
    // Detaches the thread represented by the object from the calling 
    // thread, allowing them to execute independently from each other. B
    //
    my_thread.detach();

    if (my_condition_var.wait_for(my_lock, std::chrono::seconds(1)) == 
            std::cv_status::timeout)  {
        //
        // Throw an exception so the caller knows we failed
        //
        throw std::runtime_error("Timeout");
    }

    return result;    
}

int main()
{
    // Run a function that might block

    try {
        auto f1 = fn<int,int>(my_function_that_might_block);
        wrap_my_slow_function(f1, 42);
        //
        // Success, no timeout
        //
    } catch (std::runtime_error& e) {
        //
        // Do whatever you need here upon timeout failure
        //
        return 1;
    }

    return 0;
}