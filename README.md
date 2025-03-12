![Tests](https://github.com/dilawarm/symdiff/blob/gh-pages/badges/tests-badge.svg)
![Coverage](https://github.com/dilawarm/symdiff/blob/gh-pages/badges/coverage-badge.svg)

# 🧮 symdiff

A symbolic differentiation tool for polynomial expressions.

## 📝 Description

`symdiff` is a Python library that performs symbolic differentiation on polynomial expressions. It parses mathematical expressions into a tree of expression objects and applies differentiation rules to compute derivatives.

## ✨ Features

- Differentiate polynomial expressions
- Interactive command-line interface
- Support for standard mathematical notation
- Simplify derivative expressions

## 🚀 Installation

### Prerequisites

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. Install uv with:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Development Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/dilawarm/symdiff.git
   cd symdiff
   ```

2. Set up a virtual environment (requires Python 3.11+):
   ```sh
   uv run make install
   ```
   
   This will:
   - Create a virtual environment
   - Install all dependencies

3. Activate the virtual environment:
   ```sh
   source .venv/bin/activate
   ```

## 🔍 Usage

### Command Line

```sh
# Differentiate an expression with respect to x
symdiff "x^2 + 2*x + 1"

# Differentiate with respect to a different variable
symdiff "y^3 + 2*y" -v "y"

# Interactive mode
symdiff
```

### As a Library

```python
from symdiff.core import differentiate

result = differentiate("x^2 + 2*x + 1")
print(result) # d/dx(x^2 + 2*x + 1) = 2*x + 2
```

## 🛠️ Development

- Run tests: `uv run make test`
- Check code formatting: `uv run make check`
- Format code: `uv run make format`
- Generate test badges: `uv run make badges`

## 👥 Contributors

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for a list of contributors and information on how to contribute to this project.

## 📄 License

This project is licensed under the terms of the [LICENSE](LICENCE) file included in the repository.
