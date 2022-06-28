from typing import Any, Dict
from typing_extensions import Self

from notion_self_management.expression.expression import Expression
from notion_self_management.expression.formula import BasicValue, Formula


class BindVariable(Expression):

    def __init__(
            self,
            variable: str,  # type:ignore
            value: BasicValue,  # type:ignore
    ) -> None:
        self.variable = variable
        self.value = value
        super().__init__()

    def evaluate(self) -> Dict[str, Any]:
        if isinstance(self.value, Formula):
            return {self.variable: Formula()}
        return {self.variable: self.variable}

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """for deserialize"""
        return NotImplemented

    def to_json(self) -> str:
        """for persistence"""
        return NotImplemented
