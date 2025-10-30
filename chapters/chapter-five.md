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
