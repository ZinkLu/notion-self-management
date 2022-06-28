from typing import Any, Generic, Iterable, TypeVar, Union

from notion_self_management.expression.expression import Expression

Number = Union[int, float]
_BasicValue = Union[str, Number, bool]
BasicValue = Union[_BasicValue, Iterable[_BasicValue]]
Value = Union[BasicValue, "Formula"]


class Formula(Expression):
    return_type = type
    arg_types = []

    def __init__(self, *args_variables):
        # TODO: valid variable types
        self.args = args_variables

    def evaluate(self, *args) -> Any:
        # TODO: valid parameter types
        return


# some built in Formula
class Add(Formula):
    return_type = Number
    arg_types = [Number, Number]

    def evaluate(self, a: Number, b: Number) -> Number:
        return a + b


class Sub(Formula):
    return_type = Number
    arg_types = [Number, Number]

    def evaluate(self, a: Number, b: Number) -> Number:
        return a + b


class Mul(Formula):
    return_type = Number
    arg_types = [Number, Number]


class Div(Formula):
    return_type = Number
    arg_types = [Number, Number]


class Concat(Formula):
    return_type = str
    arg_types = [str, str]
