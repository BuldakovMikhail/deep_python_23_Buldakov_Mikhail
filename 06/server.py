import socket
import sys
from urllib.request import urlopen
import threading
from queue import Queue

from bs4 import BeautifulSoup
from collections import Counter
import json


GL_PROC_URL = 0


def parse_argv():
    workers_count = sys.argv[sys.argv.index("-w") + 1]
    keys_count = sys.argv[sys.argv.index("-k") + 1]
    return int(workers_count), int(keys_count)


def get_most_common_words(resp, keys_count):
    soup = BeautifulSoup(resp, "html.parser")
    text = soup.get_text().split()
    temp = dict(Counter(text).most_common(keys_count))
    return temp


def scraping_url(queue, keys_count):
    global GL_PROC_URL

    while True:
        connect = queue.get()
        if connect is None:
            queue.put(connect)
            break

        data = connect.recv(1024)
        if data:
            url = data.decode()
            resp = urlopen(url)

            most_common = get_most_common_words(resp, keys_count)

            connect.sendall(json.dumps(most_common).encode())
            GL_PROC_URL += 1
            print(f"Обработано: {GL_PROC_URL}")


def run_workers(n_threads, keys_count, queue):
    threads = [
        threading.Thread(
            target=scraping_url,
            name=f"worker-{i}",
            args=(queue, keys_count),
        )
        for i in range(n_threads)
    ]

    for th in threads:
        th.start()


def run_server(host, port, workers_count=10, keys_count=5):
    server_address = (host, port)
    queue = Queue()

    run_workers(workers_count, keys_count, queue)
    with socket.create_server(server_address) as sock:
        while True:
            connect, _ = sock.accept()
            queue.put(connect)


if __name__ == "__main__":
    workers_count, keys_count = parse_argv()
    run_server(socket.gethostname(), 5000, workers_count, keys_count)
