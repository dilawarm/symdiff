"""
Core functionality for symbolic differentiation.

This module contains the core functions for symbolic differentiation,
including differentiation, post-processing, and formatting.
"""

import re
from functools import reduce
from typing import Callable, Match

from symdiff.expressions import (
    Constant,
    CustomExpression,
    Expression,
    Negation,
    Product,
    Sum,
)

from .parser import parse_expression


def format_result(expr: Expression) -> Expression:
    """Format the result for better readability."""
    result_str = str(expr).replace("+ -", " - ")

    while "  " in result_str:
        result_str = result_str.replace("  ", " ")

    pattern_handler: Callable[[Match], str] = (
        lambda m: f"{int(m.group(1)) * int(m.group(2))}*{m.group(3)}"
    )
    result_str = re.sub(
        r"(\d+)\*(\d+)\*([a-zA-Z])",
        pattern_handler,
        result_str,
    )

    if result_str != str(expr):
        return CustomExpression(expr, result_str)

    return expr


def post_process(expr: Expression) -> Expression:
    """Apply post-processing steps to improve expression readability."""
    if isinstance(expr, Sum):
        new_terms: list[Expression] = []
        for term in expr.terms:
            if isinstance(term, Product) and len(term.factors) >= 2:
                constants = [f for f in term.factors if isinstance(f, Constant)]
                if len(constants) >= 2:
                    combined_value = reduce(lambda x, y: x * y.value, constants, 1)
                    non_constants = [
                        f for f in term.factors if not isinstance(f, Constant)
                    ]
                    new_terms.append(
                        Product([Constant(combined_value)] + non_constants)
                    )
                else:
                    new_terms.append(term)
            else:
                new_terms.append(term)

        if new_terms != expr.terms:
            return Sum(new_terms).simplify()

    if isinstance(expr, Negation) and isinstance(expr.expression, Product):
        product = expr.expression
        constants = [f for f in product.factors if isinstance(f, Constant)]
        if len(constants) >= 2:
            combined_value = reduce(lambda x, y: x * y.value, constants, 1)
            non_constants = [f for f in product.factors if not isinstance(f, Constant)]
            return Negation(Product([Constant(combined_value)] + non_constants))

    return expr


def differentiate(expression_str: str, variable: str = "x") -> Expression:
    """Differentiate a polynomial expression with respect to a variable."""
    expr = parse_expression(expression_str, variable)
    derivative = expr.differentiate(variable).simplify()
    processed = post_process(derivative)
    return format_result(processed)
