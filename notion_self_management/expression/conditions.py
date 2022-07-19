import operator as op

from notion_self_management.expression.base_condition import BaseCondition, BaseConditionList, ConditionType
from notion_self_management.expression.consts import false, true


class Condition(BaseCondition):

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
        return All([self, other])

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
        return Any([self, other])

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
        kls = BoolOperatorInv.get(self.__class__, None)  # type: ignore # noqa
        if kls:
            return kls(*self.args)
        instance = self.__class__(*self.args)
        instance._inv = not self._inv
        return instance


class ConditionList(BaseConditionList):

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
        return All([self, other])

    def __or__(self, other: ConditionType) -> ConditionType:
        """
        See `ConditionList.__and__`
        """
        return Any([self, other])

    def not_(self):
        ins = self.__class__(self.args)
        ins._inv = not self._inv
        return ins

    def __invert__(self):
        return self.not_()


class Eq(Condition):
    func = op.eq


class Ne(Condition):
    func = op.ne


class Gt(Condition):
    func = op.gt


class Ge(Condition):
    func = op.ge


class Lt(Condition):
    func = op.lt


class Le(Condition):
    func = op.le


class Contains(Condition):
    func = op.contains


class All(ConditionList):
    func = all


class Any(ConditionList):
    func = any


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
    return All(arg)


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
    return Any(arg)


BoolOperatorInv = {
    Eq: Ne,
    Ne: Eq,
    Gt: Lt,
    Lt: Gt,
    Ge: Le,
    Le: Ge,
}
