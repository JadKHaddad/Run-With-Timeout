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
