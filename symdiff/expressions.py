"""
Expression classes for symbolic differentiation.

This module contains the classes that represent mathematical expressions
for symbolic differentiation.
"""

from dataclasses import dataclass
from functools import reduce

Number = int | float


@dataclass
class Expression:
    """Base class for all expressions."""

    def differentiate(self, variable: str) -> "Expression":
        """Differentiate the expression with respect to the given variable."""
        raise NotImplementedError("Subclasses must implement this method")

    def simplify(self) -> "Expression":
        """Simplify the expression."""
        return self


@dataclass
class Constant(Expression):
    """Represents a constant value."""

    value: Number

    def differentiate(self, variable: str) -> Expression:
        """Differentiate a constant (always returns 0)."""
        return Constant(0)

    def __str__(self) -> str:
        """Convert to string, using integer form when possible."""
        return (
            str(int(self.value)) if self.value == int(self.value) else str(self.value)
        )


@dataclass
class Variable(Expression):
    """Represents a variable."""

    name: str

    def differentiate(self, variable: str) -> Expression:
        """Differentiate a variable (returns 1 if same variable, 0 otherwise)."""
        return Constant(1) if self.name == variable else Constant(0)

    def __str__(self) -> str:
        """Convert to string (returns the variable name)."""
        return self.name


@dataclass
class Power(Expression):
    """Represents a variable raised to a power: x^n."""

    variable: Variable
    exponent: Number

    def differentiate(self, variable: str) -> Expression:
        """Differentiate a power expression using the power rule."""
        if self.variable.name != variable:
            return Constant(0)

        if self.exponent == 0:
            return Constant(0)
        elif self.exponent == 1:
            return Constant(1)
        else:
            return Product(
                [Constant(self.exponent), Power(self.variable, self.exponent - 1)]
            ).simplify()

    def __str__(self) -> str:
        """Convert to string, handling special cases for exponents 0 and 1."""
        if self.exponent == 0:
            return "1"
        elif self.exponent == 1:
            return str(self.variable)
        else:
            exponent_str = (
                str(int(self.exponent))
                if self.exponent == int(self.exponent)
                else str(self.exponent)
            )
            return f"{self.variable}^{exponent_str}"

    def simplify(self) -> Expression:
        """Simplify a power expression."""
        if self.exponent == 0:
            return Constant(1)
        if self.exponent == 1:
            return self.variable
        return self


@dataclass
class Negation(Expression):
    """Represents the negation of an expression: -expr."""

    expression: Expression

    def differentiate(self, variable: str) -> Expression:
        """Differentiate a negation using the rule: (-f(x))' = -f'(x)."""
        return Negation(self.expression.differentiate(variable))

    def __str__(self) -> str:
        """Convert to string, adding parentheses around sums."""
        return (
            f"-({self.expression})"
            if isinstance(self.expression, Sum)
            else f"-{self.expression}"
        )

    def simplify(self) -> Expression:
        """Simplify a negation expression."""
        simplified_expr = self.expression.simplify()

        if isinstance(simplified_expr, Constant):
            return Constant(-simplified_expr.value)
        if isinstance(simplified_expr, Negation):
            return simplified_expr.expression
        if isinstance(simplified_expr, Constant) and simplified_expr.value == 0:
            return Constant(0)

        return Negation(simplified_expr)


@dataclass
class Sum(Expression):
    """Represents a sum of expressions."""

    terms: list[Expression]

    def differentiate(self, variable: str) -> Expression:
        """Differentiate a sum using the rule: (f+g)' = f'+g'."""
        derivatives = map(
            lambda term: term.differentiate(variable).simplify(), self.terms
        )
        return Sum(list(derivatives)).simplify()

    def __str__(self) -> str:
        """Convert to string, joining terms with +."""
        return " + ".join(map(str, self.terms))

    def simplify(self) -> Expression:
        """Simplify a sum by removing zeros and combining terms."""
        non_zero_terms = list(
            filter(
                lambda term: not (isinstance(term, Constant) and term.value == 0),
                map(lambda term: term.simplify(), self.terms),
            )
        )

        if not non_zero_terms:
            return Constant(0)
        if len(non_zero_terms) == 1:
            return non_zero_terms[0]

        return Sum(non_zero_terms)


@dataclass
class Product(Expression):
    """Represents a product of expressions."""

    factors: list[Expression]

    def differentiate(self, variable: str) -> Expression:
        """Differentiate a product using the product rule."""
        if not self.factors:
            return Constant(0)

        if len(self.factors) == 1:
            return self.factors[0].differentiate(variable).simplify()

        if len(self.factors) == 2:
            a, b = self.factors
            return Sum(
                [
                    Product([a.differentiate(variable), b]),
                    Product([a, b.differentiate(variable)]),
                ]
            ).simplify()

        result_terms = [
            Product(
                [
                    factor.differentiate(variable) if i == j else factor
                    for j, factor in enumerate(self.factors)
                ]
            ).simplify()
            for i in range(len(self.factors))
        ]

        return Sum(result_terms).simplify()

    def __str__(self) -> str:
        """Convert to string, handling special cases for 0 and 1."""
        if any(isinstance(f, Constant) and f.value == 0 for f in self.factors):
            return "0"

        non_one_factors = list(
            filter(
                lambda f: not (isinstance(f, Constant) and f.value == 1), self.factors
            )
        )

        if not non_one_factors:
            return "1"
        if len(non_one_factors) == 1:
            return str(non_one_factors[0])

        constants = list(filter(lambda f: isinstance(f, Constant), non_one_factors))
        non_constants = list(
            filter(lambda f: not isinstance(f, Constant), non_one_factors)
        )

        if constants:
            product = reduce(lambda x, y: x * y.value, constants, 1)

            if product == 0:
                return "0"

            product_str = str(int(product) if product == int(product) else product)

            if not non_constants:
                return product_str
            if len(non_constants) == 1:
                return f"{product_str}*{non_constants[0]}"

            return f"{product_str}*{self._join_factors(non_constants)}"

        return self._join_factors(non_one_factors)

    def _join_factors(self, factors: list[Expression]) -> str:
        """Join factors with * operator."""
        return "*".join(map(str, factors))

    def simplify(self) -> Expression:
        """Simplify a product by handling special cases and combining constants."""
        if not self.factors:
            return Constant(0)

        simplified_factors = list(map(lambda f: f.simplify(), self.factors))

        if any(isinstance(f, Constant) and f.value == 0 for f in simplified_factors):
            return Constant(0)

        non_one_factors = list(
            filter(
                lambda f: not (isinstance(f, Constant) and f.value == 1),
                simplified_factors,
            )
        )

        if not non_one_factors:
            return Constant(1)
        if len(non_one_factors) == 1:
            return non_one_factors[0]

        constants = list(filter(lambda f: isinstance(f, Constant), non_one_factors))
        non_constants = list(
            filter(lambda f: not isinstance(f, Constant), non_one_factors)
        )

        if constants:
            constant_product = reduce(lambda x, y: x * y.value, constants, 1)

            if constant_product == 0:
                return Constant(0)
            if constant_product == 1 and non_constants:
                return (
                    Product(non_constants)
                    if len(non_constants) > 1
                    else non_constants[0]
                )
            if not non_constants:
                return Constant(constant_product)

            return Product([Constant(constant_product)] + non_constants)

        return Product(non_one_factors)


@dataclass
class CustomExpression(Expression):
    """A wrapper for expressions with custom string representation."""

    expr: Expression
    custom_str: str

    def differentiate(self, variable: str) -> Expression:
        """Delegate differentiation to the wrapped expression."""
        return self.expr.differentiate(variable)

    def __str__(self) -> str:
        """Return the custom string representation."""
        return self.custom_str

    def simplify(self) -> Expression:
        """Return self as it's already in simplified form."""
        return self
