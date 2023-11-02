import socket
import sys
import threading
from queue import Queue


def url_send(queue, server_address):
    while True:
        url = queue.get()
        if url is None:
            queue.put(url)
            break
        with socket.create_connection(server_address) as sock:
            sock.settimeout(10)
            message = url.encode()
            sock.sendall(message)
            data = sock.recv(1024)
            mess = data.decode()

        url = url.strip()

        print(f"{url}: {mess}")


def run_exp(n_threads, queue, server_address):
    threads = [
        threading.Thread(
            target=url_send,
            name=f"fetch-{i}",
            args=(queue, server_address),
        )
        for i in range(n_threads)
    ]

    for th in threads:
        th.start()


def create_queue(file):
    queue = Queue()
    with open(file, "r") as src:
        while x := src.readline():
            queue.put(x)
    queue.put(None)

    return queue


def run_clients(host, port, file, threads_count=10):
    server_address = (host, port)
    queue = create_queue(file)
    run_exp(threads_count, queue, server_address)


def parse_argv():
    threads_count = sys.argv[1]
    fname = sys.argv[2]
    return int(threads_count), fname


if __name__ == "__main__":
    tc, fname = parse_argv()
    run_clients(socket.gethostname(), 5000, fname, tc)
