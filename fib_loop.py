import asyncio

async def print_fib_loop():
    n0, n1 = 0, 1
    while True:
        print(n1)
        n2 = n0 + n1
        n0, n1 = n1, n2
        await asyncio.sleep(1)

loop = asyncio.get_event_loop()
loop.run_until_complete(print_fib_loop())
