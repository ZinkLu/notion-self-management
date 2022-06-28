from ast import List
from typing import Any, Iterable, Type, TypeVar, Union

from notion_self_management.expression.bind import BindVariable
from notion_self_management.expression.bool_expression import Condition
from notion_self_management.expression.expression import Expression
from notion_self_management.expression.formula import BasicValue, Formula
from notion_self_management.expression.ops import BoolOperator


class Variable:
    """
    Variable class represent a variable, like `a`.

    A value can be assign to variable, like `a = 1`.
    A formula also can be assign to variable, like `a = now()`
    A variable also can be in arithmetic expression like `a + 1`
    While variable can be composed to bool expression, like `a <= 10`, `a in [0, 1, 2]`

    Variable can be seen as a Column in Table.
    """

    def __init__(self, type: Type, name: str = "") -> None:
        """
        :param name: Name of the variable, like `create_time`
        :param type: Type of the variable it could be any basic python
                     type such as Dict, List, set...
        """
        self.name = name
        self.type = type
        super().__init__()

    # assignment will get a assignment expression which can be compute later
    def bind(self, value: BasicValue) -> BindVariable:
        """
        assign a valid value to this variable.
        """
        if isinstance(value, Formula):
            if self.type != value.return_type:
                raise TypeError(f"Can't set variable {self.name} to type {value.return_type}")
        elif self.type != type(value):
            raise TypeError(f"Can't set variable {self.name} to type {type(value)}")

        return BindVariable(self.name, value)

    # arithmetic will return a formula
    def __add__(self) -> Formula:
        ...

    def __sub__(self) -> Formula:
        ...

    def __div__(self) -> Formula:
        ...

    def __mul__(self) -> Formula:
        ...

    # bool will return Condition
    def __eq__(self, __o: object) -> Condition:
        return Condition(BoolOperator.eq, self, __o)

    def __gt__(self, __o: object) -> Condition:
        return Condition(BoolOperator.gt, self, __o)

    def __ge__(self, __o: object) -> Condition:
        return Condition(BoolOperator.ge, self, __o)

    def __lt__(self, __o: object) -> Condition:
        return Condition(BoolOperator.lt, self, __o)

    def __le__(self, __o: object) -> Condition:
        return Condition(BoolOperator.le, self, __o)

    def __ne__(self, __o: object) -> Condition:
        return Condition(BoolOperator.ne, self, __o)
