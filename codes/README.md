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

# Create a virtual environment with Python 3.10.5
python3.10 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Verify the environment is active (should show Python 3.10.5)
python --version

# Install required dependencies
pip install -r requirements.txt  # (if a requirements.txt file exists)
```

#### On Windows:
```cmd
# Navigate to the codes directory
cd \path\to\codes

# Create a virtual environment with Python 3.10.5
py -3.10 -m venv venv

# Activate the virtual environment
venv\Scripts\activate

# Verify the environment is active (should show Python 3.10.5)
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

## Chapter Explanations

### Chapter 4: Child Processes and Multiprocessing

The examples in this chapter demonstrate how to work with child processes in Python using the `multiprocessing` module.

#### Passing Variables to Child Processes

In `child_processes.py`, we demonstrate how to pass variables from the parent process to child processes:

```python
# Create a child process and pass variables to it
p = Process(target=run_child, args=(message, number))
p.start()
```

The `args` parameter of the `Process` constructor takes a tuple of arguments to be passed to the target function. These arguments are serialized and sent to the child process.

You can pass any serializable Python object (numbers, strings, lists, dictionaries, etc.) to a child process:

```python
# Example of passing different types of data
data = {
    'name': 'example',
    'values': [1, 2, 3]
}
p = Process(target=some_function, args=(data, 42, "hello"))
p.start()
```

Note that each child process gets its own copy of the variables, so changes made in a child process won't affect the variables in the parent process or other child processes.
