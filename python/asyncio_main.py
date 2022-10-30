import asyncio
from asyncio.exceptions import TimeoutError


async def fail(arg1, arg2):
    print(arg1, arg2)
    await asyncio.sleep(5)
    return 42


async def scc(arg1, arg2):
    print(arg1, arg2)
    await asyncio.sleep(1)
    return 42


async def err(arg1, arg2):
    print(arg1, arg2)
    await asyncio.sleep(1)
    raise ValueError("A very bad error my friend :>")


async def looping(arg1, arg2):
    print(arg1, arg2)
    while True:
        await asyncio.sleep(1)
        print("looping")


async def main():
    try:
        result = await asyncio.wait_for(err("I am Error", ":D"), timeout=3)
        print(result)
    except TimeoutError:
        print("Timeout")
    except ValueError as e:
        print("ValueError", e)

    try:
        result = await asyncio.wait_for(fail("I will fail", "XD"), timeout=3)
        print(result)
    except TimeoutError:
        print("Timeout")

    try:
        result = await asyncio.wait_for(scc("I wont", ":D"), timeout=3)
        print(result)
    except TimeoutError:
        print("Timeout")

    try:
        result = await asyncio.wait_for(looping("I am a Loop", ":/"),
                                        timeout=3)
        print(result)
    except TimeoutError:
        print("Timeout")
    await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())