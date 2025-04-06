# LOX Compiler (Python Edition)

Welcome to the LOX Compiler project! This repository contains an implementation of a compiler for the LOX programming language, as described in the book *Crafting Interpreters* by Robert Nystrom.

## Features

- **Interpreter**: Executes LOX code directly.
- **Compiler**: Converts LOX code into bytecode for a virtual machine.
- **Error Handling**: Provides detailed error messages for syntax and runtime issues.
- **Cross-Platform**: Runs on multiple operating systems.

## Getting Started

### Prerequisites

- Install [Python](https://www.python.org/downloads/) version 3.8 or higher.

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/LOX_Compiler_Python.git
    cd LOX_Compiler_Python
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the interpreter:
    ```bash
    python main.py
    ```

## Usage

You can run LOX scripts by passing the file name as an argument:
```bash
python main.py script.lox
```

Alternatively, start the REPL (Read-Eval-Print Loop) by running the program without arguments:
```bash
python main.py
```

## Acknowledgments

- Inspired by the book *Crafting Interpreters* by Robert Nystrom.
- Thanks to the open-source community for their support.

Happy coding!