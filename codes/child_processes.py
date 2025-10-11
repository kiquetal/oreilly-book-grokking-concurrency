import os
from multiprocessing import Process
def run_child()->None:
    print("Child: I am a child process with PID:", os.getpid())
    print("Child: My parent's PID is:", os.getppid())
def start_parent(num_children: int)->None:
    print("Parent: I am the parent process with PID:", os.getpid())
    print(f"Parent: My parent's PID is: {os.getppid()}")
    for i in range(num_children):
        print(f"Starting child process {i}")
        p = Process(target=run_child)
        p.start()
if __name__ == "__main__":
    start_parent(3)
