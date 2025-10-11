import os
import time
import threading
from threading import Thread

def cpu_water(id: int) -> None:
    name= threading.current_thread().name
    print(f"Thread {name} with ID {id} starting.")
    time.sleep(3)

def display_threads() -> None:
    print("-" * 40)
    print(f"Current process ID: {os.getpid()}")
    print(f"Active threads count: {threading.active_count()}")
    print("Thread details:")
    for thread in threading.enumerate():
        print(thread)

def main(num_threads: int) -> None:
    display_threads()
    print(f"[main]Starting {num_threads} CPU water threads.")
    for i in range(num_threads):
        thread = Thread(target=cpu_water, args=(i,))
        thread.start()
    display_threads()

if __name__ == "__main__":
    main(5)
