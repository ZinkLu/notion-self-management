from collections import OrderedDict, deque
from typing import Any, List, Optional, Tuple, TypeVar, Union

from notion_self_management.expression.const import empty, false, true
from notion_self_management.expression.expression import Expression
from notion_self_management.expression.formula import BasicValue, Value
from notion_self_management.expression.ops import BoolOperator, BoolOperatorInv, LogicalOperator
from typing_extensions import Self

ConstClass = TypeVar('ConstClass', true, false)

ConditionType = Union["Condition", "ConditionList", true, false, ConstClass]


class Condition(Expression):

    def __init__(
        self,
        op: BoolOperator,
        left: Union[BasicValue, "Variable"],
        right: Union[BasicValue, "Variable"],
    ):
        """
        Condition is a bool binary operation like `a == 1`
        Where `a` is a Variable class and `1` is a true value.

        The binary also can be operated with two variables like
        `a == b`.

        a bool binary operation always have a left and right
        """
        self.op = op
        self.left = left
        self.right = right

    def to_json(self) -> str:
        return super().to_json()

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return super().from_json(json_str)

    def __and__(self, other: ConditionType) -> "ConditionList":
        """
        perform a logic `and` operation.

        `&` `|` `~` have higher priority than `==` or `<` `>`
        so it's necessary to have a parentheses when using
        this.

        ```python
        a = Variable("a", int)
        b = Variable("b", int)

        condition_list = (a == 1) & (b == 1)
        ```
        """
        return ConditionList(LogicalOperator.and_, [self, other])

    def __or__(self, other: ConditionType) -> "ConditionList":
        """
        perform a logic `or` operation.

        `&` `|` `~` have higher priority than `==` or `<` `>`
        so it's necessary to have a parentheses when using
        this.

        ```python
        a = Variable("a", int)
        b = Variable("b", int)

        condition_list = (a == 1) | (b == 1)
        ```
        """
        return ConditionList(LogicalOperator.or_, [self, other])

    def __invert__(self) -> "Condition":
        """
        perform a logic `not` operation.

        `&` `|` `~` have higher priority than `==` or `<` `>`
        so it's necessary to have a parentheses when using
        this.

        ```python
        a = Variable("a", int)
        b = Variable("b", int)

        condition_list = ~(a == 1) # a != 1
        ```
        """
        return self.not_()

    def not_(self) -> "Condition":
        return Condition(BoolOperatorInv[self.op], self.left, self.right)

    @staticmethod
    def _get_variable_bind(v: "Variable", values: dict):
        eval_value = values.get(v.name, empty)
        if eval_value is empty:
            raise ValueError(f"variable {v.name} is unbound during compute")
        return eval_value

    def evaluate(self, **values: BasicValue) -> bool:
        from notion_self_management.expression.variable import Variable
        eval_left, eval_right = self.left, self.right

        if isinstance(eval_right, Variable):
            eval_right = self._get_variable_bind(eval_right, values)

        if isinstance(eval_left, Variable):
            eval_left = self._get_variable_bind(eval_left, values)

        return self.op.value(eval_left, eval_right)

    def __str__(self) -> str:
        return f"{self.left} {self.op} {self.right}"


class ConditionList(Expression):

    def __init__(self, op: LogicalOperator, clauses: List[ConditionType]) -> None:
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
        self.op = op
        self.clauses = clauses
        self._inv = False

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return super().from_json(json_str)

    def to_json(self) -> str:
        return super().to_json()

    def evaluate(self, **values) -> bool:
        """
        compute a logical expression.

        all variable must be bound.

        :params: values: dict contains Variable's bind value.
        :return: logical expression result.
        :rtype: bool
        """
        res = False
        if self.op == LogicalOperator.and_:
            res = all((c.evaluate(**values) for c in self.clauses))
        elif self.op == LogicalOperator.or_:
            res = any((c.evaluate(**values) for c in self.clauses))

        return (not res) if self._inv else res

    def __and__(self, other: ConditionType) -> "ConditionList":
        """
        perform a logic `and` operation.

        `&` `|` `~` have higher priority than `==` or `<` `>`
        so it's necessary to have a parentheses when using
        this.

        ```python
        a = Variable("a", int)
        b = Variable("b", int)

        condition_list = (a == 1) & ((b == 1) | ( a == 2)) & (b == 2)
        # a = 1 and ( b = 1 or a = 2) and b = 2
        ```
        """
        return ConditionList(LogicalOperator.and_, [self, other])

    def __or__(self, other: ConditionType) -> ConditionType:
        """
        See `ConditionList.__and__`
        """
        return ConditionList(LogicalOperator.or_, [self, other])

    def not_(self):
        ins = ConditionList(self.op, self.clauses)
        ins._inv = True
        return ins

    def __invert__(self):
        return self.not_()

    def __str__(self) -> str:
        return f"{self._inv and 'not' or ''}{self.clauses}"


def and_(*args: ConditionType) -> ConditionList:
    """
    `Condition.__and__()` can only have one ConditionType,
    It's useful when put a list of ConditionTypes together.

    ```python
    a = Variable("a", int)
    b = Variable("b", int)
    c = Variable("c", int)

    cl = and_(a == 1, b == 2, c == 3)

    print(cl.evaluate(a=1, b=2, c=3)) # true
    ```

    """
    arg = list(args)
    if len(args) == 1:
        arg.insert(0, true)

    return ConditionList(LogicalOperator.and_, arg)


def or_(*args: ConditionType) -> ConditionList:
    """
    `Condition.__or__()` can only have one ConditionType,
    It's useful when put a list of ConditionTypes together.

    ```python
    a = Variable("a", int)
    b = Variable("b", int)
    c = Variable("c", int)

    cl = or_(a == 1, b == 2, c == 3)

    print(cl.evaluate(a=1, b=1, c=1)) # return true
    ```
    """
    arg = list(args)
    if len(args) == 1:
        arg.insert(0, false)

    return ConditionList(LogicalOperator.or_, list(args))
