import asyncio 
import time 
from concurrent.futures import ProcessPoolExecutor

async def fetch_data(sec):
    print(f"Start to fetch data {sec}")
    asyncio.sleep(sec)
    print(f" Fetched data {sec}")
    return sec * 100

async def main():
    # Run in threads
    task1 = asyncio.create_task(asyncio.to_thread(fetch_data, 1))
    task2 = asyncio.create_task(asyncio.to_thead(fetch_data, 2))
    result1 = await task1
    print("Thread 1 fully completed")
    result2 = await task2
    print("Thread 2 fully completed")

    # Run in process pool
    loop = asyncio.get_running_loop() 

    with ProcessPoolExecutor() as executor:
        task1 = loop.run_in_executor(executor, fetch_data, 1)
        task2 = loop.run_in_executor(executor, fetch_data, 2)

        result1 = await task1
        print("Process 1 fully completed")
        result2 = await task2
        print("Process 2 fully completed")

    return [result1, result2]

# if __name__ == "main":

t1 = time.perf_counter()
print(asyncio.run(main()))

t2 = time.perf_counter()
print(f"Time taken: {t2 - t1}")