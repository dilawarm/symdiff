"""
Parser for mathematical expressions.

This module contains functions for parsing mathematical expressions
into expression objects.
"""

from functools import partial

from symdiff.expressions import (
    Constant,
    Expression,
    Negation,
    Power,
    Product,
    Sum,
    Variable,
)


def parse_factor(factor: str, variable: str) -> Expression:
    """Parse a single factor (power, variable, or constant)."""
    if "^" in factor:
        base, exponent = factor.split("^")
        if base == variable:
            return Power(Variable(variable), float(exponent))
        if base.isalpha():
            return Power(Variable(base), float(exponent))
        try:
            return Constant(float(base) ** float(exponent))
        except ValueError:
            raise ValueError(f"Invalid power expression: {factor}")

    if factor == variable:
        return Variable(variable)

    if factor.isalpha():
        return Variable(factor)

    try:
        return Constant(float(factor))
    except ValueError:
        raise ValueError(f"Invalid expression: {factor}")


def parse_term(term: str, variable: str) -> Expression:
    """Parse a single term (product, power, variable, or constant)."""
    factors = term.split("*")
    if not factors:
        return Constant(0)

    parsed_factors = list(map(partial(parse_factor, variable=variable), factors))

    return parsed_factors[0] if len(parsed_factors) == 1 else Product(parsed_factors)


def parse_expression(expression_str: str, variable: str = "x") -> Expression:
    """Parse a polynomial expression string into an Expression object."""
    expression_str = expression_str.replace(" ", "").replace("-", "+-")
    if expression_str.startswith("+"):
        expression_str = expression_str[1:]

    terms = list(filter(bool, expression_str.split("+")))
    if not terms:
        return Constant(0)

    def parse_with_negation(term: str) -> Expression:
        """Parse a term, handling negation if present."""
        if term.startswith("-"):
            return Negation(parse_term(term[1:], variable))
        return parse_term(term, variable)

    parsed_terms = list(map(parse_with_negation, terms))

    return parsed_terms[0] if len(parsed_terms) == 1 else Sum(parsed_terms)
