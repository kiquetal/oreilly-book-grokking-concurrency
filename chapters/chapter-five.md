<!-- Imported from: Readme.md -->
### 📖 Chapter V

- Notes on Chapter V, covering types of communication.

#### 📢 Types of comunication

- interprocess communication (IPC)

##### Shared-memory

Allows one or more tasks to communicate through common memory that appears in all their virtual adress spaces as if they were reading locally.

#### Race Condition and the `continue` statement

A race condition occurs when the timing of events causes unexpected behavior. In the provided `shared_memory.py` example, a race condition exists between the `Producer` and `Consumer` threads.

The `Consumer` could read from a memory location before the `Producer` has had a chance to write to it. Without proper handling, the `Consumer` would read the initial value (`-1`) and incorrectly proceed as if it were valid data.

The `continue` statement solves this by forcing the `Consumer` to wait. If the `Consumer` reads a `-1`, the `continue` statement skips the rest of the loop (including the part that prints the value) and starts the loop over. This ensures the `Consumer` only proceeds when it has read valid data from the `Producer`.


##### Message-passing IPC

In message-passing IPC, each task is identified by a unique name, and 
tasks interact by sending and receving mesages to and from named tasks.
The OS is responsible for delivering messages to the correct task.

Pipe: simplest from of IPC. A pipe is a unidirectional communication channel that can be used for interprocess communication. Data written to the write end of the pipe can be read from the read end of the pipe. If you need bidirectional communication, you can create two pipes.

Unnamed pipe: can only be used by related tasks(ex child-parent processes). Created using the pipe() system call. Unnamed pipes dissapear after the task finish using them.
 Pipe operatios are similar to file operations

Named pipe: Allow transfer of data between tasks according to the FIFO
which means that the first data written to the pipe is the first data read from the pipe.
 Named pipes are created using the mkfifo() system call and can be used by unrelated tasks.
 Named pipes persist after the tasks finish using them until they are deleted.


##### Message Queues

As we've seen, messages queues are used to implement loosely coupled
systems. They are used everywhere.In OSS to schedule processes and in
routers as buffers to store packet before they are processed.



Reading from a pipe is a blocking operation. If a process attempts to read from an empty pipe, it will pause until data becomes available. In the provided `pipes.py` example, the `Reader` thread calls `self.conn.recv()`, which blocks execution until the `Writer` thread sends data using `self.conn.send()`.

##### Unix Domain Sockets - Stream Communication

The implementation in `sockets.py` demonstrates interprocess communication using Unix Domain Sockets (UDS) with stream sockets (SOCK_STREAM). This provides a reliable, connection-oriented communication channel between processes on the same machine.

###### Socket Implementation Details

1. Sender Socket (Client):
```python
client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client.connect(SOCKET_FILE)
```
- Uses `AF_UNIX` for local inter-process communication
- Uses `SOCK_STREAM` for reliable, ordered data delivery
- Connects to the server socket using `connect()`
- Uses `sendall()` to ensure complete message transmission

2. Receiver Socket (Server):
```python
server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_FILE)
server.listen()
conn, addr = server.accept()
```
- Creates a stream socket bound to a filesystem path
- Calls `listen()` to accept incoming connections
- Uses `accept()` to create a new socket for the connection
- Uses `recv()` to receive data from the client

###### Why This Works:

1. Connection Establishment:
   - The server starts first and calls `listen()`
   - The client connects using `connect()`
   - `accept()` creates a new socket specifically for this connection

2. Reliable Communication:
   - SOCK_STREAM provides:
     - Guaranteed delivery
     - In-order message arrival
     - Automatic message boundaries
     - Built-in error checking

3. The While Loop Structure:
```python
while True:
    data = conn.recv(BUFFER_SIZE)
    if not data:
        break
    message = data.decode()
```
This works because:
- `recv()` blocks until data arrives
- An empty return (`not data`) signals connection closure
- Messages are received in the exact order they were sent

4. Connection Cleanup:
   - The socket file is removed before and after use
   - The server closes the connection when the client disconnects
   - Both sockets are properly closed

The implementation uses a sleep call (`time.sleep(1)`) to ensure the receiver is ready before the sender starts, which is a simple but effective way to handle initialization ordering in this example.

###### Understanding Connection Termination

The key to understanding how the receiver knows there's no more data lies in this part of the code:

```python
while True:
    data = conn.recv(BUFFER_SIZE)
    if not data:
        break
    message = data.decode()
```

Here's how the termination process works:

1. Connection Closure Process:
   - When the sender finishes sending all messages, it calls `client.close()`
   - This initiates a proper TCP connection termination (FIN packet)
   - The operating system handles the TCP connection teardown

2. Receiver Detection:
   - `conn.recv(BUFFER_SIZE)` is a blocking call that:
     - Returns data when messages arrive
     - Returns an empty bytes object (b'') when the sender closes the connection properly
   - `if not data:` catches this empty return, signaling that:
     - The sender has closed their end of the connection
     - No more data will be coming
     - It's safe to break the loop

3. Sequence of Events:
   ```python
   # Sender side
   for msg in messages:
       client.sendall(str.encode(msg))
       time.sleep(1)
   client.close()  # This triggers the termination

   # Receiver side
   data = conn.recv(BUFFER_SIZE)  # Will return empty after sender closes
   if not data:  # This condition becomes True
       break     # Loop exits cleanly
   ```

This is why the code doesn't need explicit message counting or a special "end" message - it relies on the TCP protocol's built-in connection termination handling. The receiver will automatically know there's no more data when the sender closes their socket.

#### Thread Pool Patterns

Reusing threads with a thread pool eliminates the overhead associated with creating new threads and protects against the unexpected failure of the taks, such as an unhandled exception, from terminating the entire program.

##### Thread Pool Worker Loop Behavior

In the `pool.py` implementation, we have a unique situation with the worker thread loop:

```python
def run(self) -> None:
    while True:
        task: Task = self.task_queue.get()
        try:
            func, args, kwargs = task
            func(*args, **kwargs)
        finally:
            self.task_queue.task_done()
```

The worker loop continues indefinitely because:

1. Workers are daemon threads (`worker.daemon = True` in ThreadPool initialization)
   - Daemon threads are automatically terminated when the main program exits
   - They don't need explicit shutdown signals

2. Queue synchronization:
   - `task_queue.get()` blocks until a task is available
   - `task_queue.task_done()` decrements internal counter for `join()`
   - When main thread calls `wait_completion()`, it waits on `task_queue.join()`
   - `join()` blocks until every `put()` item has a matching `task_done()`

3. Program termination sequence:
   - Main thread submits all tasks
   - Calls `wait_completion()` which waits for all tasks to complete
   - When main thread exits, daemon workers are automatically terminated

This design trades off clean shutdown for simplicity:
- No need for explicit shutdown signals
- Workers don't need to check for termination conditions
- Program exits cleanly when work is done due to daemon threads

However, this approach has limitations:
- Workers can't clean up resources before termination
- No graceful shutdown mechanism
- Relies on Python's daemon thread behavior

For more robust applications, you might want to:
- Use non-daemon threads
- Add a sentinel value (like None) to signal shutdown
- Implement explicit shutdown methods

The current implementation is sufficient for simple task processing where clean worker shutdown isn't critical.


##### Message Queue Implementation Details

The `message_queue.py` example demonstrates a thread-safe producer-consumer pattern using Python's `queue.Queue`. This implementation shows how message queues enable safe communication between threads.

###### Key Components:

1. Queue Creation and Management:
```python
message_queue = queue.Queue()  # Thread-safe FIFO queue
```
- Queue is created at module level, shared between threads
- Internally synchronized - no additional locks needed
- FIFO (First In, First Out) ordering of messages

2. Producer Implementation:
```python
def run(self) -> None:
    for msg in self.messages:
        message_queue.put(msg)
    message_queue.put(None)  # Sentinel
```
- Sends messages sequentially
- Uses `put()` to add messages to queue
- Sends `None` as sentinel to signal completion

3. Consumer Implementation:
```python
def run(self) -> None:
    while True:
        message = message_queue.get()  # Blocks until message available
        if message is None:
            message_queue.task_done()
            break
        # Process message
        message_queue.task_done()
```

###### Why This Works:

1. Thread Safety:
   - Queue handles all synchronization internally
   - No race conditions possible
   - Safe for multiple producers/consumers

2. Flow Control:
   - `get()` blocks when queue is empty
   - `put()` blocks if queue has size limit
   - Natural throttling of fast producers

3. Completion Handling:
   - Sentinel value (`None`) signals end
   - `task_done()` tracks processed messages
   - `join()` waits for all messages to be processed

4. Sequence of Events:
   ```python
   consumer.start()   # Start waiting for messages
   producer.start()   # Begin sending messages
   producer.join()    # Wait for producer to finish
   message_queue.join() # Wait for all messages to be processed
   ```

This implementation demonstrates several advantages of message queues:
- Decoupling: Producer and consumer don't need to know about each other
- Buffering: Queue handles temporary differences in processing speeds
- Synchronization: Built-in thread safety
- Flow control: Natural backpressure handling
