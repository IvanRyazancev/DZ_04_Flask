import requests
from pathlib import Path
import time
import threading
import multiprocessing
import asyncio
import aiohttp


def download(url, start_time, type_: str):
    response = requests.get(url)

    filename = type_ + url.split('/')[-1]
    with open(f"./images/{filename}", 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


def task1(urls: list[str]):
    start_time = time.time()
    threads = []
    for url in urls:
        thread = threading.Thread(target=download, args=[url, start_time, "thread_"])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def task2(urls: list[str]):
    start_time = time.time()
    processes = []
    for url in urls:
        process = multiprocessing.Process(target=download, args=[url, start_time, "process_"])
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


async def download_async(url, start_time, type_: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()

    filename = type_ + url.split('/')[-1]
    with open(f"./images/{filename}", 'wb') as f:
        f.write(content)
    print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


async def task3(urls):
    start_time = time.time()
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(download_async(url, start_time, 'async_'))
        tasks.append(task)
    await asyncio.gather(*tasks)


def main():
    urls = [
        'https://img.razrisyika.ru/kart/15/56951-dzhek-rassel-13.jpg',
        'https://ferret-pet.ru/wp-content/uploads/5/d/8/5d89f4df1e931d002bd6be202220c93e.jpeg',
        'https://lady-dog.ru/wp-content/uploads/0/8/3/083d15f6bbe202da886684403d7792f8.jpeg'
    ]

    # task1(urls)
    # task2(urls)
    asyncio.run(task3(urls))


if __name__ == '__main__':
    main()