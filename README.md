# Pookie: The Poke-Making Game

Welcome to Pookie, a game about assembling delicious poke bowls for a variety of customers!

## Requirements

-   Python 3.13 or newer

## Setup & Installation

Follow these steps to get the game running on your local machine.

**1. Clone the Repository**

First, clone this repository to your local machine using Git:

```bash
git clone https://github.com/Tuasco/Pookie
cd Pookie
```

**2. Create and Activate the Virtual Environment**

This project uses a virtual environment to manage its dependencies.

* **On Windows:**
    ```bash
    # Create the environment
    py -3.13 -m venv .venv
    # Activate it (using PowerShell)
    .\.venv\Scripts\Activate.ps1
    ```

* **On macOS / Linux:**
    ```bash
    # Create the environment
    python3.13 -m venv .venv
    # Activate it
    source .venv/bin/activate
    ```

**3. Install Dependencies**

Once the environment is activated, you can install all the required packages automatically by running:

```bash
pip install -r requirements.txt
```

## How to Play

With the setup complete and the virtual environment still active, launch the main application:

```bash
python main_window.py
```

Enjoy serving your customers!