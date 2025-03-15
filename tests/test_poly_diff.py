from symdiff.core import differentiate


def test_constant_differentiation():
    """Test differentiation of constants"""
    assert str(differentiate("5")) == "0"
    assert str(differentiate("3.14")) == "0"


def test_variable_differentiation():
    """Test differentiation of variables"""
    assert str(differentiate("x")) == "1"
    assert str(differentiate("y", variable="y")) == "1"
    assert str(differentiate("y")) == "0"


def test_power_differentiation():
    """Test differentiation of powers"""
    assert str(differentiate("x^0")) == "0"
    assert str(differentiate("x^1")) == "1"
    assert str(differentiate("x^2")) == "2*x"
    assert str(differentiate("x^3")) == "3*x^2"
    assert str(differentiate("x^10")) == "10*x^9"


def test_product_differentiation():
    """Test differentiation of products"""
    assert str(differentiate("2*x")) == "2"
    assert str(differentiate("3*x^2")) == "6*x"
    assert str(differentiate("5*x^3")) == "15*x^2"


def test_sum_differentiation():
    """Test differentiation of sums"""
    assert str(differentiate("x + 1")) == "1"
    assert str(differentiate("x^2 + x")) == "2*x + 1"
    assert str(differentiate("x^2 + 2*x + 1")) == "2*x + 2"


def test_complex_expressions():
    """Test differentiation of more complex expressions"""
    assert str(differentiate("x^3 + 3*x^2 + 3*x + 1")) == "3*x^2 + 6*x + 3"
    assert str(differentiate("2*x^4 + 3*x^3 + 4*x^2")) == "8*x^3 + 9*x^2 + 8*x"
    assert str(differentiate("5*x^3 + 9*x^2 + 18*x^7")) == "15*x^2 + 18*x + 126*x^6"
    assert str(differentiate("5*x^30 + 9*x^2 + 18*x^7")) == "150*x^29 + 18*x + 126*x^6"
    assert str(differentiate("x^0 + x^1")) == "1"
    assert (
        str(differentiate("0.5*x^3 + 1.5*x^2 - 0.1*x^9")) == "1.5*x^2 + 3*x - 0.9*x^8"
    )


def test_negation():
    """Test differentiation of negated expressions"""
    assert str(differentiate("-x")) == "-1"
    assert str(differentiate("-x^2")) == "-2*x"
    assert str(differentiate("-3*x^2")) == "-6*x"
    assert str(differentiate("-1")) == "0"
    assert str(differentiate("-x")) == "-1"


def test_subtraction():
    """Test differentiation of expressions with subtraction"""
    assert str(differentiate("x - 1")) == "1"
    assert str(differentiate("x^2 - x")) == "2*x - 1"
    assert str(differentiate("x^2 - 2*x + 1")) == "2*x - 2"
    assert str(differentiate("x^3 - 3*x^2 + 3*x - 1")) == "3*x^2 - 6*x + 3"


def test_different_variables():
    """Test differentiation with respect to different variables"""
    assert str(differentiate("x", variable="y")) == "0"
    assert str(differentiate("y", variable="y")) == "1"
    assert str(differentiate("y^2", variable="y")) == "2*y"

    assert str(differentiate("x^3", variable="y")) == "0"
    assert str(differentiate("z^5", variable="y")) == "0"

    assert str(differentiate("x^2 + y^2", variable="y")) == "2*y"
    assert str(differentiate("x*y", variable="y")) == "x"
    assert str(differentiate("x*y^2", variable="y")) == "x*2*y"

    assert str(differentiate("x^3 - 5*x + 1", variable="y")) == "0"
    assert str(differentiate("x^2 + 2*x*y + y^2", variable="y")) == "2*x + 2*y"
    assert str(differentiate("x*y + y*z", variable="y")) == "x + z"

    assert str(differentiate("y^3 + y^2 + y", variable="y")) == "3*y^2 + 2*y + 1"
    assert str(differentiate("x*y^2 + y*z^2", variable="y")) == "x*2*y + z^2"


def test_negative_exponents():
    """Test differentiation of expressions with negative exponents"""
    assert str(differentiate("x^-1")) == "-x^-2"
    assert str(differentiate("x^-2")) == "-2*x^-3"
    assert str(differentiate("2*x^-1")) == "-2*x^-2"
    assert str(differentiate("x^-3 + x^2")) == "-3*x^-4 + 2*x"
    assert str(differentiate("x^-0.5")) == "-0.5*x^-1.5"
