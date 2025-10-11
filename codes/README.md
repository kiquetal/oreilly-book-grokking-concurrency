# Python Environment Setup Instructions

This directory contains code examples for the "Grokking Concurrency" book. Follow these instructions to set up a Python environment for running the examples.

## Setting Up a Python Virtual Environment

### Prerequisites
- Python 3.10.5
- pip (Python package installer)

### Steps to Create and Activate a Virtual Environment

#### On Linux/macOS:
```bash
# Navigate to the codes directory
cd /path/to/codes

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Verify the environment is active (should show the Python version)
python --version

# Install required dependencies
pip install -r requirements.txt  # (if a requirements.txt file exists)
```

#### On Windows:
```cmd
# Navigate to the codes directory
cd \path\to\codes

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate

# Verify the environment is active (should show the Python version)
python --version

# Install required dependencies
pip install -r requirements.txt  # (if a requirements.txt file exists)
```

### Deactivating the Environment
When you're done working with the examples, you can deactivate the virtual environment:
```bash
deactivate
```

## Creating a requirements.txt File
If you need to create a requirements.txt file for the project:

1. Ensure your virtual environment is activated
2. Install the necessary packages using pip
3. Generate the requirements.txt file:
```bash
pip freeze > requirements.txt
```

## Running Code Examples
After setting up and activating your virtual environment, you can run the code examples in this directory.

Example:
```bash
python example_file.py
```

## Code Explanations Index

- [Chapter 4: Child Processes and Multiprocessing](#chapter-4-child-processes-and-multiprocessing)
  - [Understanding the Basic Child Process Example](#understanding-the-basic-child-process-example)
  - [Extending the Example: Sending Parameters to Child Processes](#extending-the-example-sending-parameters-to-child-processes)
  - [Multithreading Example](#multithreading-example)
  - [Comparing Threads and Processes](#comparing-threads-and-processes)

## Chapter 4: Child Processes and Multiprocessing

### Understanding the Basic Child Process Example

The `child_processes.py` file demonstrates how to create child processes in Python using the `multiprocessing` module. Here's a breakdown of the original code:

```python
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
```

This code:
1. Imports necessary modules: `os` for process ID functions and `Process` from `multiprocessing`
2. Defines a `run_child()` function that prints the child's process ID and its parent's process ID
3. Defines a `start_parent()` function that creates multiple child processes
4. When run as a script, creates 3 child processes

### Extending the Example: Sending Parameters to Child Processes

While the original code doesn't pass parameters to child processes, you can extend it to do so without modifying the original file. Here's how you can create a new file that builds on the original example:

Create a new file called `child_processes_with_params.py`:

```python
import os
from multiprocessing import Process

# Function with parameters
def run_child_with_params(name: str, number: int) -> None:
    print("Child: I am a child process with PID:", os.getpid())
    print("Child: My parent's PID is:", os.getppid())
    print(f"Child: I received name='{name}' and number={number}")

def start_parent(num_children: int) -> None:
    print("Parent: I am the parent process with PID:", os.getpid())
    print(f"Parent: My parent's PID is: {os.getppid()}")
    
    for i in range(num_children):
        # Create parameters to pass to the child process
        child_name = f"Child-{i}"
        child_number = i * 10
        
        print(f"Starting child process {i} with name='{child_name}', number={child_number}")
        
        # Pass parameters using the args tuple
        p = Process(target=run_child_with_params, args=(child_name, child_number))
        p.start()

if __name__ == "__main__":
    start_parent(3)
```

#### Key Points About Passing Parameters to Child Processes

1. **Modify the Target Function**: Ensure your function accepts parameters:
   ```python
   def run_child_with_params(name: str, number: int) -> None:
   ```

2. **Pass Arguments Using `args` Parameter**: The `args` parameter in the `Process` constructor takes a tuple of arguments:
   ```python
   p = Process(target=run_child_with_params, args=(child_name, child_number))
   ```

3. **Pass Keyword Arguments**: For named parameters, use the `kwargs` parameter:
   ```python
   p = Process(target=run_child_with_params, kwargs={'name': child_name, 'number': child_number})
   ```

4. **Passing Different Data Types**: You can pass various data types including:
   - Basic types (int, float, string, bool)
   - Collections (list, dict, tuple)
   - Custom objects (must be picklable)

5. **Advanced Data Sharing**:
   For more complex data sharing between processes, consider:
   
   - **Using Shared Memory Objects**:
   ```python
   from multiprocessing import Process, Value, Array
   
   def modify_shared(shared_num, shared_arr):
       shared_num.value += 100
       for i in range(len(shared_arr)):
           shared_arr[i] *= 2
   
   if __name__ == "__main__":
       # Create shared objects
       num = Value('i', 0)  # shared integer
       arr = Array('i', [1, 2, 3, 4])  # shared array
       
       p = Process(target=modify_shared, args=(num, arr))
       p.start()
       p.join()
       
       print(f"Shared number: {num.value}")  # Will print: Shared number: 100
       print(f"Shared array: {list(arr)}")   # Will print: Shared array: [2, 4, 6, 8]
   ```
   
   - **Using a Manager**:
   ```python
   from multiprocessing import Process, Manager
   
   def modify_dict(shared_dict):
       shared_dict['new_key'] = 'added by child'
       shared_dict['counter'] += 1
   
   if __name__ == "__main__":
       with Manager() as manager:
           # Create a shared dictionary
           shared_dict = manager.dict({'counter': 0})
           
           p = Process(target=modify_dict, args=(shared_dict,))
           p.start()
           p.join()
           
           print(shared_dict)  # Will print: {'counter': 1, 'new_key': 'added by child'}
   ```

#### Example: Sending Complex Data to Child Processes

```python
import os
import json
from multiprocessing import Process

def process_data(user_data: dict, settings: list) -> None:
    print(f"Child process {os.getpid()} received:")
    print(f"  User: {user_data['name']}, Age: {user_data['age']}")
    print(f"  Settings: {', '.join(settings)}")
    
    # Process the data
    result = {
        'processed_by': os.getpid(),
        'user_age_in_months': user_data['age'] * 12,
        'settings_count': len(settings)
    }
    
    print(f"Processing result: {json.dumps(result)}")

def start_parent() -> None:
    # Complex data to send to child process
    user = {
        'name': 'Alice',
        'age': 30,
        'email': 'alice@example.com'
    }
    
    app_settings = ['debug=True', 'log_level=info', 'max_connections=100']
    
    p = Process(target=process_data, args=(user, app_settings))
    p.start()
    p.join()

if __name__ == "__main__":
    start_parent()
```

#### Important Notes on Process Communication

1. **Data is Copied**: Arguments passed to child processes are serialized and copied, not shared. Modifications in the child won't affect the parent's copy.

2. **Pickling Limitation**: Only picklable objects can be passed as arguments. This excludes certain objects like file handles, database connections, and some class instances.

3. **Performance Considerations**: Passing large amounts of data can be inefficient due to serialization overhead. For large data, consider using shared memory.

4. **Process Synchronization**: When data is shared between processes, proper synchronization is required using locks, semaphores, or other mechanisms from the `multiprocessing` module.

### Multithreading Example

The `multithreading.py` file demonstrates how to create and manage threads in Python using the `threading` module. Here's a breakdown of the code:

```python
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
```

This code:
1. Imports necessary modules: `os`, `time`, `threading` and `Thread` from `threading`
2. Defines a `cpu_water()` function that simulates CPU work (using sleep for demonstration purposes)
3. Defines a `display_threads()` function that shows information about all running threads
4. Defines a `main()` function that creates multiple threads
5. When run as a script, creates 5 threads

#### Key Points About Passing Parameters to Threads

Unlike processes, threads share the same memory space. However, passing parameters to thread functions works similarly:

1. **Defining a Target Function with Parameters**: 
   ```python
   def cpu_water(id: int) -> None:
       name = threading.current_thread().name
       print(f"Thread {name} with ID {id} starting.")
       time.sleep(3)
   ```

2. **Passing Arguments Using `args` Parameter**:
   ```python
   thread = Thread(target=cpu_water, args=(i,))
   ```

3. **Pass Keyword Arguments**: For named parameters, use the `kwargs` parameter:
   ```python
   thread = Thread(target=some_function, kwargs={'name': thread_name, 'number': thread_number})
   ```

4. **Accessing Thread Information**: You can get information about the current thread:
   ```python
   name = threading.current_thread().name
   ```

### Comparing Threads and Processes

Both threads and processes are used for concurrent execution in Python, but they have key differences that make them suitable for different scenarios:

#### Threads (threading module)

**Advantages:**
- **Lightweight**: Threads require fewer resources to create than processes
- **Shared Memory**: All threads within a process share the same memory space, making data sharing easier
- **Fast Creation**: Threads are faster to create than processes
- **Communication**: Thread communication is simpler as they share memory

**Limitations:**
- **Global Interpreter Lock (GIL)**: Python's GIL prevents multiple threads from executing Python bytecode simultaneously, limiting CPU-bound parallelism
- **Harder to Debug**: Shared memory can lead to race conditions and deadlocks
- **Limited Isolation**: Crashes in one thread can affect other threads

**Best for:**
- I/O-bound tasks (network operations, file operations)
- Tasks that require frequent communication
- User interfaces
- When memory usage is a concern

#### Processes (multiprocessing module)

**Advantages:**
- **True Parallelism**: Multiple processes can execute Python code simultaneously, bypassing the GIL
- **Isolation**: Processes have separate memory spaces, preventing one process from affecting others
- **Stability**: A crash in one process doesn't affect other processes
- **Scalability**: Processes can use multiple CPU cores effectively

**Limitations:**
- **Resource Intensive**: Processes require more memory and take longer to create
- **Complex Communication**: Inter-process communication is more complex and requires serialization
- **Overhead**: Data sharing between processes involves copying or special shared memory objects

**Best for:**
- CPU-bound tasks
- Tasks requiring isolation and fault tolerance
- When maximum parallelism is needed
- Long-running background tasks

#### Choosing Between Threads and Processes

Consider these factors when deciding:

1. **Task Type**:
   - **I/O-bound tasks** (waiting for external resources): Use threads
   - **CPU-bound tasks** (heavy computation): Use processes

2. **Data Sharing Requirements**:
   - **Frequent data sharing**: Threads may be more efficient
   - **Independent operations**: Processes provide better isolation

3. **Resource Constraints**:
   - **Limited memory**: Threads have less overhead
   - **Maximum performance**: Processes utilize multiple cores better

4. **Error Handling**:
   - **Need isolation**: Processes prevent errors from spreading
   - **Simplified coordination**: Threads share state more easily

#### Example: When to Use Each Approach

**Use Threads for:**
```python
# Web scraping - I/O bound
def scrape_url(url):
    # Network operations, waiting for responses
    response = requests.get(url)
    return response.text

# Create multiple threads for different URLs
for url in urls:
    thread = Thread(target=scrape_url, args=(url,))
    thread.start()
```

**Use Processes for:**
```python
# Image processing - CPU bound
def process_image(image_path):
    # Heavy computational work
    image = Image.open(image_path)
    # Apply filters and transformations
    return processed_image

# Create multiple processes for different images
for img_path in image_paths:
    process = Process(target=process_image, args=(img_path,))
    process.start()
```
