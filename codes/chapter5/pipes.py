from multiprocessing import Pipe
from threading import Thread, current_thread
from multiprocessing.connection import Connection

class Writer(Thread):
    def __init__(self, conn):
        super().__init__()
        self.conn: Connection = conn
        self.name = "Writer"

    def run(self) -> None:
        print(f"{current_thread().name}: Writing data to pipe")
        self.conn.send("Rubber duck")


class Reader(Thread):
    def __init__(self, conn):
        super().__init__()
        self.conn: Connection = conn
        self.name = "Reader"

    def run(self) -> None:
        print(f"{current_thread().name}: Reading data from pipe")
        data = self.conn.recv()
        print(f"{current_thread().name}: Read data: {data}")

def main() -> None:
    read_conn, write_conn = Pipe()
    reader = Reader(read_conn)
    writer = Writer(write_conn)

    threads = [reader, writer]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
