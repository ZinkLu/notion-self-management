from notion_self_management.expression.base_formula import Formula
from notion_self_management.expression.base_variable import BaseVariable
from notion_self_management.expression.conditions import Condition, Eq, Ge, Gt, Le, Lt, Ne


class Variable(BaseVariable):
    """
    Variable class represent a variable, like `a`.

    A value can be assign to variable, like `a = 1`.
    A formula also can be assign to variable, like `a = now()`
    A variable also can be in arithmetic expression like `a + 1`
    While variable can be composed to bool expression, like `a <= 10`, `a in [0, 1, 2]`

    Variable can be seen as a Column in Table.
    """

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
        return Eq(self, __o)

    def __gt__(self, __o: object) -> Condition:
        return Gt(self, __o)

    def __ge__(self, __o: object) -> Condition:
        return Ge(self, __o)

    def __lt__(self, __o: object) -> Condition:
        return Lt(self, __o)

    def __le__(self, __o: object) -> Condition:
        return Le(self, __o)

    def __ne__(self, __o: object) -> Condition:
        return Ne(self, __o)
