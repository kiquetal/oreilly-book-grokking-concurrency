import string
import time
import queue
import typing as T
from threading import Thread, current_thread

Callback = T.Callable[..., None]
Task = T.Tuple[Callback, T.Any,T.Any]
TaskQueue = queue.Queue

class Worker(Thread):
    def __init__(self, task_queue: TaskQueue, name: string) -> None:
        super().__init__()
        self.task_queue = task_queue
        self.name = name

    def run(self) -> None:
        while True:
            task: Task = self.task_queue.get()
            try:
                func, args, kwargs = task
                print(f"{current_thread().name}: Executing task {func.__name__} \n ")
                func(*args, **kwargs)
            except Exception as e:
                print(f"{current_thread().name}: Error executing task: {e}")
            self.task_queue.task_done()

class ThreadPool:
    def __init__(self, num_threads: int) -> None:
        self.tasks = queue.Queue(num_threads)
        self.num_threads = num_threads

        for _ in range(num_threads):
            worker = Worker(self.tasks, name=f"Worker-{_}")
            worker.daemon = True
            worker.start()

    def submit(self, func: Callback, *args, **kwargs) -> None:
        self.tasks.put((func, args, kwargs))

    def wait_completion(self) -> None:
        self.tasks.join()

def cpu_waster(i: int) -> None:
    name = current_thread().name
    print(f"Task {i} started by {name}\n")
    time.sleep(2)
    print(f"[Task {i} completed by =>{name}]\n")

def main() -> None:
    num_threads = 10
    pool = ThreadPool(num_threads=num_threads)

    for i in range(num_threads + 5):
        pool.submit(cpu_waster, i)
    print("All tasks submitted.\n")
    pool.wait_completion()
    print(f"All tasks completed by {current_thread().name}")

if __name__ == "__main__":
    main()
