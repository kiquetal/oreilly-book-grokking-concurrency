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


