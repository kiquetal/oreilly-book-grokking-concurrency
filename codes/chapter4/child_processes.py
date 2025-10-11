import os
from multiprocessing import Process
def run_child(message: str, number: int) -> None:
    print("Child: I am a child process with PID:", os.getpid())
    print("Child: My parent's PID is:", os.getppid())
    print(f"Child: I received message: '{message}' and number: {number}")
def start_parent(num_children: int) -> None:
    print("Parent: I am the parent process with PID:", os.getpid())
    print(f"Parent: My parent's PID is: {os.getppid()}")
    for i in range(num_children):
        message = f"Hello from parent to child {i}"
        number = i * 10
        print(f"Starting child process {i} with message: '{message}' and number: {number}")
        p = Process(target=run_child, args=(message, number))
        p.start()
if __name__ == "__main__":
    start_parent(3)
