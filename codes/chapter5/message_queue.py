import queue
import threading
import time
from typing import List

# A thread-safe message queue
message_queue = queue.Queue()

class Producer(threading.Thread):
    def __init__(self, messages: List[str]) -> None:
        super().__init__()
        self.messages = messages
        self.name = "Producer"

    def run(self) -> None:
        for msg in self.messages:
            print(f"{threading.current_thread().name}: Sending message: {msg}")
            message_queue.put(msg)
            time.sleep(1)  # Simulate some processing time
        # Send sentinel to signal end of messages
        message_queue.put(None)

class Consumer(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Consumer"

    def run(self) -> None:
        while True:
            # Block until a message is available
            message = message_queue.get()
            
            # Check for sentinel value
            if message is None:
                print(f"{threading.current_thread().name}: No more messages.")
                message_queue.task_done()
                break
                
            print(f"{threading.current_thread().name}: Received message: {message}")
            # Mark the message as processed
            message_queue.task_done()
            time.sleep(0.5)  # Simulate message processing

def main() -> None:
    # Messages to be sent
    messages = [
        "Hello from the queue!",
        "Processing message 1",
        "Processing message 2",
        "Final message"
    ]

    # Create producer and consumer threads
    producer = Producer(messages)
    consumer = Consumer()

    # Start threads
    consumer.start()  # Start consumer first to wait for messages
    time.sleep(0.1)  # Small delay to ensure consumer is ready
    producer.start()

    # Wait for producer to finish sending
    producer.join()
    
    # Wait for all messages to be processed
    message_queue.join()
    
    # Wait for consumer to finish
    consumer.join()

    print("All messages have been processed!")

if __name__ == "__main__":
    main()
