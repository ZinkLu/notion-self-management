from abc import ABC, abstractmethod
from typing import Any

from typing_extensions import Self


class Expression(ABC):
    """
    Expression Class
    An expression can be one of these sub expression:
        1. bool expression. a bool expression can be used in two ways.
            - if variable is bind. The bool expression will finally return a true or false to tell if a event will be
                trigger or not
            - if variable is not bind. The bool expression can be seen as a filter.
        2. formula. a arithmetic operation or a built in function.
        3. cron. a cron expression can compute next time.
    """

    @classmethod
    @abstractmethod
    def from_json(cls, json_str: str) -> Self:
        """for deserialize"""
        return NotImplemented

    @abstractmethod
    def to_json(self) -> str:
        """for persistence"""
        return NotImplemented

    def evaluate(self, *args, **kwargs) -> Any:
        ...
