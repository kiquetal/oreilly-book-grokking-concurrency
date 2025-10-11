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
