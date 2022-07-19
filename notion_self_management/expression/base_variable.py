from typing import Type

from notion_self_management.expression.base import Expression


class BaseVariable(Expression):

    def __init__(self, type: Type, name: str = "") -> None:
        """
        :param name: Name of the variable, like `create_time`
        :param type: Type of the variable it could be any basic python
                     type such as Dict, List, set...
        """
        self.name = name
        self.type = type
        super().__init__()


class Const(BaseVariable):

    def __new__(cls, *args, **kwargs):
        """Const is a singleton"""
        if getattr(cls, "instance", None) is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        return
