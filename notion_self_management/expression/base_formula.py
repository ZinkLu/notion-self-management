from typing import Any, Callable, Iterable, List, Type, TypeVar, Union

from notion_self_management.expression.base_variable import BaseVariable
from notion_self_management.expression.consts import Const, empty
from notion_self_management.expression.base import Expression

Number = Union[int, float]
BasicValue = Union[str, Number, bool, List[str]]
Value = Union[BasicValue, "Formula", "BaseVariable", "Const"]

BasicValueType = TypeVar("BasicValueType", str, int, float, bool, List[str])
ValueType = TypeVar("ValueType", str, int, float, bool, List[str], "Formula", "BaseVariable", "Const")

ARG_TYPE = ValueType
RETURN_TYPE = ValueType


def is_iterable(obj: Any) -> bool:
    return isinstance(obj, Iterable) and not isinstance(obj, (str, bytes))


class FormulaMeta(type):
    """
    TODO:
    For formula registering
    And runtime type assertion
    """
    ...


class Formula(Expression):
    return_type: Type = object
    arg_types: List[Type] = []
    func: Callable = lambda: empty

    def __init__(self, *args_variables: Value):
        self.args = args_variables

    @staticmethod
    def _get_variable_bind(v: "BaseVariable", values: dict):
        eval_value = values.get(v.name, empty)
        if eval_value is empty:
            raise ValueError(f"variable {v.name} is unbound during compute")
        return eval_value

    @staticmethod
    def bind_args(args, **values: dict) -> List:
        result = list()
        for arg in args:
            if isinstance(arg, BaseVariable):
                arg = Formula._get_variable_bind(arg, values)

            result.append(arg)
        return result

    def __call__(self, *args: Any) -> Any:
        return self.evaluate(*args)

    def evaluate(self, **kwargs) -> Any:
        args = self.bind_args(self.args, **kwargs)
        return self.func(*args)