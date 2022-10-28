from queue import Queue, Empty
from threading import Thread
import time


def run_with_timeout(func, timeout, *args, **kwargs):
    q = Queue()

    def wrapper():
        result = func(*args, **kwargs)
        q.put(result)

    thread = Thread(target=wrapper)
    thread.daemon = True
    thread.start()
    data = q.get(timeout=timeout)
    return data


def fail(arg1, arg2):
    print(arg1, arg2)
    time.sleep(6)
    return 42


def succ(arg1, arg2):
    print(arg1, arg2)
    time.sleep(1)
    return 42


if __name__ == "__main__":
    try:
        result = run_with_timeout(fail, 3, "I will fail", "XD")
        print(result)
    except Empty:
        print("Timeout")

    try:
        result = run_with_timeout(succ, 3, "I wont", ":D")
        print(result)
    except Empty:
        print("Timeout")