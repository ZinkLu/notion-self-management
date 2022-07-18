from typing import Type

from notion_self_management.expression.expression import Expression


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
