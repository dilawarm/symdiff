from symdiff.expressions import (
    Constant,
    Negation,
    Power,
    Product,
    Sum,
    Variable,
)
from symdiff.parser import parse_expression


def test_parser():
    """Test the expression parser"""

    assert isinstance(parse_expression("5"), Constant)
    assert str(parse_expression("5")) == "5"

    assert isinstance(parse_expression("x"), Variable)
    assert str(parse_expression("x")) == "x"

    assert isinstance(parse_expression("x^2"), Power)
    assert str(parse_expression("x^2")) == "x^2"

    assert isinstance(parse_expression("2*x"), Product)
    assert str(parse_expression("2*x")) == "2*x"

    assert isinstance(parse_expression("x + 1"), Sum)
    assert str(parse_expression("x + 1")) == "x + 1"

    assert isinstance(parse_expression("-x"), Negation)
    assert str(parse_expression("-x")) == "-x"

    assert str(parse_expression("x - 1")) == "x + -1"

    expr = parse_expression("x^2 + 2*x + 1")
    assert isinstance(expr, Sum)
    assert len(expr.terms) == 3
    assert str(expr) == "x^2 + 2*x + 1"

    expr = parse_expression("x^2 - 2*x + 1")
    assert isinstance(expr, Sum)
    assert len(expr.terms) == 3
    assert str(expr) == "x^2 + -2*x + 1"

    expr = parse_expression("x^-1")
    assert isinstance(expr, Power)
    assert str(expr) == "x^-1"

    expr = parse_expression("x^-2 + 3*x^-1")
    assert isinstance(expr, Sum)
    assert str(expr) == "x^-2 + 3*x^-1"
