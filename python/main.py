from queue import Queue, Empty
from threading import Thread
import time


def run_with_timeout(func, timeout, *args, **kwargs):
    q = Queue()

    def wrapper():
        try:
            result = func(*args, **kwargs)
            q.put(result)
        except Exception as e:
            q.put(e)

    thread = Thread(target=wrapper)
    thread.daemon = True
    thread.start()
    data = q.get(timeout=timeout)
    if isinstance(data, Exception):
        raise data
    return data


def fail(arg1, arg2):
    print(arg1, arg2)
    time.sleep(6)
    return 42


def scc(arg1, arg2):
    print(arg1, arg2)
    time.sleep(1)
    return 42


def err(arg1, arg2):
    print(arg1, arg2)
    time.sleep(1)
    raise ValueError("A very bad error my friend :>")


def looping(arg1, arg2):
    print(arg1, arg2)
    while True:
        time.sleep(1)
        print("looping")


if __name__ == "__main__":
    try:
        result = run_with_timeout(err, 3, "I am Error", ":D")
        print(result)
    except Empty:
        print("Timeout")
    except ValueError as e:
        print("ValueError", e)

    try:
        result = run_with_timeout(fail, 3, "I will fail", "XD")
        print(result)
    except Empty:
        print("Timeout")

    try:
        result = run_with_timeout(scc, 3, "I wont", ":D")
        print(result)
    except Empty:
        print("Timeout")

    # Notice that `looping` will time out, but will keep on looping, so `run_with_timeout` will not terminate the thread
    # Connection delays, etc. will cause a timeout, but the thread will keep on running until it is FINISHED!
    # Getting `Timeout` means that the program has ignored the thread, the thread is not FINISHED!
    # Use with caution!
    # Use Asyncio instead!
    try:
        result = run_with_timeout(looping, 3, "I am a Loop", ":/")
        print(result)
    except Empty:
        print("Timeout")
        # You can still exit though
        # exit(1)
    time.sleep(10)
