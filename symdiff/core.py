"""
Core functionality for symbolic differentiation.

This module contains the core functions for symbolic differentiation,
including differentiation and formatting.
"""

import re
from typing import Callable, Match

from symdiff.expressions import (
    CustomExpression,
    Expression,
)
from symdiff.parser import parse_expression


def format_result(expr: Expression) -> Expression:
    """Format the result for better readability."""
    result_str = str(expr).replace("+ -", " - ")

    while "  " in result_str:
        result_str = result_str.replace("  ", " ")

    def float_multiply_handler(match: Match) -> str:
        num1 = float(match.group(1))
        num2 = float(match.group(2))
        var = match.group(3)
        result = num1 * num2
        if result == int(result):
            result = int(result)
        return f"{result}*{var}"

    patterns = [
        r"(\d+\.\d+)\*(\d+)\*([a-zA-Z])",
        r"(\d+)\*(\d+\.\d+)\*([a-zA-Z])",
        r"(\d+\.\d+)\*(\d+\.\d+)\*([a-zA-Z])",
    ]

    for pattern in patterns:
        result_str = re.sub(pattern, float_multiply_handler, result_str)

    int_multiply_handler: Callable[[Match], str] = (
        lambda m: f"{int(m.group(1)) * int(m.group(2))}*{m.group(3)}"
    )
    result_str = re.sub(
        r"(\d+)\*(\d+)\*([a-zA-Z])",
        int_multiply_handler,
        result_str,
    )

    result_str = re.sub(r"(\d+(?:\.\d+)?)\*-", r"-\1*", result_str)

    result_str = result_str.replace("-1*", "-")

    result_str = re.sub(r"(?<![0-9])1\.0\*", "", result_str)
    result_str = re.sub(r"(?<![0-9])1\*", "", result_str)

    if result_str != str(expr):
        return CustomExpression(expr, result_str)

    return expr


def differentiate(expression_str: str, variable: str = "x") -> Expression:
    """Differentiate a polynomial expression with respect to a variable."""
    expr = parse_expression(expression_str, variable)
    derivative = expr.differentiate(variable).simplify()
    return format_result(derivative)
