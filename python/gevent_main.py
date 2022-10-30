from gevent import time, Timeout


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
    with Timeout(3):
        try:
            result = err("I am Error", ":D")
            print(result)
        except ValueError as e:
            print("ValueError", e)

    with Timeout(3):
        try:
            result = fail("I will fail", "XD")
            print(result)
        except Timeout:
            print("Timeout")

    with Timeout(3):
        try:
            result = scc("I wont", ":D")
            print(result)
        except Timeout:
            print("Timeout")

    with Timeout(3):
        try:
            result = looping("I am a Loop", ":/")
            print(result)
        except Timeout:
            print("Timeout")

    time.sleep(10)
