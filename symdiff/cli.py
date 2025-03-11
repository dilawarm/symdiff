"""
Command-line interface for the symbolic differentiator.

This module provides a command-line interface for the symbolic differentiator.
"""

import argparse
import sys

from symdiff.core import differentiate


def cli() -> None:
    """Run the command-line interface for the symbolic differentiator."""
    parser = argparse.ArgumentParser(
        description="Symbolic Differentiator for Polynomial Expressions"
    )
    parser.add_argument(
        "expression",
        nargs="?",
        help="Expression to differentiate (e.g., 'x^2 + 2*x + 1')",
    )
    parser.add_argument(
        "-v",
        "--variable",
        default="x",
        help="Variable to differentiate with respect to (default: x)",
    )

    args = parser.parse_args()

    if not args.expression:
        if not sys.stdin.isatty():
            process_stdin(args.variable)
        else:
            run_interactive_mode(args.variable)
        return
    else:
        process_expression(args.expression, args.variable)


def process_stdin(variable: str) -> None:
    """Process expressions from standard input."""
    for line in sys.stdin:
        line = line.strip()
        if not line or line.lower() in ("q", "quit", "exit"):
            continue
        try:
            result = differentiate(line, variable)
            print(f"d/d{variable}({line}) = {result}")
        except ValueError as e:
            print(f"Error: {e}")


def run_interactive_mode(variable: str) -> None:
    """Run an interactive session for entering expressions."""
    print("Symbolic Differentiator for Polynomial Expressions")
    print("=" * 50)
    print("Enter an expression to differentiate (or 'q' to quit):")

    while True:
        try:
            expression = input("> ")
            if expression.lower() in ("q", "quit", "exit"):
                break

            if not expression.strip():
                continue

            result = differentiate(expression, variable)
            print(f"d/d{variable}({expression}) = {result}")
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting...")
            break


def process_expression(expression: str, variable: str) -> None:
    """Process a single expression from command line arguments."""
    try:
        result = differentiate(expression, variable)
        print(f"d/d{variable}({expression}) = {result}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
