from multiprocessing import Pipe
from threading import Thread, current_thread
from multiprocessing.connection import Connection

class Writer(Thread):
    def __init__(self, conn):
        super().__init__()
        self.conn: Connection = conn
        self.name = "Writer"

    def run(self) -> None:
        print(f"{current_thread().name}: Sending rubber duck...")
        self.conn.send("Rubber duck")


class Reader(Thread):
    def __init__(self, conn):
        super().__init__()
        self.conn: Connection = conn
        self.name = "Reader"

    def run(self) -> None:
        print(f"{current_thread().name}: Reading...")
        data = self.conn.recv()
        print(f"{current_thread().name}: Received: {data}")

def main() -> None:
    read_conn, write_conn = Pipe()
    reader = Reader(read_conn)
    writer = Writer(write_conn)

    threads = [writer,reader]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
