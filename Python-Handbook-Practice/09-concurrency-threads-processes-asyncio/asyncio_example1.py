import asyncio 
import time

async def fetch_data(sec):
    print(f"Start to fetch data {sec}")
    await asyncio.sleep(sec)
    print(f" Fetched data {sec}")
    return sec * 100

# Coroutine
async def main():
    print("main called")
    # task1 = fetch_data(1) # cooroutine object
    # task2 = fetch_data(2)

    # Schedule a coroutine to run in event loop
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))

    result1 = await task1 # schedule event loop and run at the same time
    result2 = await task2
    return [result1, result2]


t1 = time.perf_counter()
print(asyncio.run(main()))

t2 = time.perf_counter()
print(f"Time taken: {t2 - t1}")