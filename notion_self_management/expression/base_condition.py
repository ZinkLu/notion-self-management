from typing import List, TypeVar, Union

from notion_self_management.expression.base_formula import BasicValue, Formula, Value
from notion_self_management.expression.consts import false, true

ConstClass = TypeVar('ConstClass', true, false)

ConditionType = Union["BaseCondition", "BaseConditionList", true, false, ConstClass]


class BaseCondition(Formula):

    return_type = bool
    arg_types = [BasicValue, BasicValue]
    func = bool

    def __init__(self, *args_variables: Value):
        """
        Condition is a bool binary operation like `a == 1`
        Where `a` is a Variable class and `1` is a true value.

        The binary also can be operated with two variables like
        `a == b`.

        a bool binary operation always have a left and right
        """
        super().__init__(*args_variables)
        self._inv = False

    def evaluate(self, **kwargs) -> bool:
        res = super().evaluate(**kwargs)
        return (not res) if self._inv else res


class BaseConditionList(Formula):
    return_type = bool
    arg_types = [List[ConditionType]]
    func = lambda *args: True  # noqa

    def __init__(self, clauses: List[ConditionType]) -> None:
        """
        a condition list is a bool expression but must have the same operator,
        such as `a & b & c & d` or `a | b | c | d`

        a condition list can be combine to another condition list, such as
        `(a & b)` `(c & d)` can be combine with `|` `(a & b) | (c & d)`

        :param op: logical operator
        :type op: LogicalOperator
        :param clauses: a condition list
        :type clauses: List[ConditionType]
        """
        self.args = clauses
        self._inv = False

    def evaluate(self, **values) -> bool:
        """
        compute a logical expression.

        all variable must be bound.

        :params: values: dict contains Variable's bind value.
        :return: logical expression result.
        :rtype: bool
        """
        res = self.func((c.evaluate(**values) for c in self.args))
        return (not res) if self._inv else res

    def __str__(self) -> str:
        return f"{self._inv and 'not' or ''}{self.args}"
