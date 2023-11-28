import sys
from collections import Counter
import asyncio as aio

import aiohttp
from bs4 import BeautifulSoup


def get_most_common_words(resp, keys_count=5):
    soup = BeautifulSoup(resp, "html.parser")
    text = soup.get_text().split()
    temp = dict(Counter(text).most_common(keys_count))
    return temp


async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            text = await resp.read()
            return text


async def fetch_worker(que, answers_collecter):
    while True:
        url = await que.get()
        try:
            resp = await fetch_url(url)

            th = aio.create_task(aio.to_thread(get_most_common_words, resp))
            await th

            # Тут собираем ответы в один коллектор,
            # чтобы его вернуть пользователю, но как вариант,
            # тут можно было прописать print(...)
            # или какой-то другой вывод информации
            print(f"{url=}: {th.result()}")
            answers_collecter.append((url, th.result()))
        except aiohttp.client_exceptions.InvalidURL:
            print(f"{url=}: InvalidURL")
            answers_collecter.append((url, {}))
        except Exception:
            print(f"{url=}: Undefined error occured")
            answers_collecter.append((url, {}))
        finally:
            que.task_done()


async def batch_fetch(fname, workers_count):
    que = aio.Queue(workers_count)
    answers = []

    workers = [
        aio.create_task(fetch_worker(que, answers)) for _ in range(workers_count)
    ]

    with open(fname, "r", encoding="utf-8") as src:
        while url := src.readline():
            await que.put(url)
    await que.join()

    for worker in workers:
        worker.cancel()

    return answers


def parse_argv():
    workers_count = sys.argv[sys.argv.index("-c") + 1]
    file_name = sys.argv[-1]
    return int(workers_count), file_name


if __name__ == "__main__":
    wc, fn = parse_argv()

    loop = aio.new_event_loop()
    aio.set_event_loop(loop)

    loop.run_until_complete(batch_fetch(fn, wc))
