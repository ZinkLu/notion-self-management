from typing import Generic, List, Optional, TypeVar

from notion_self_management.expression.bool_expression import ConditionType
from notion_self_management.task_manager.note import Note
from notion_self_management.task_manager.task import Task

T = TypeVar("T", Note, Task)


class Client(Generic[T]):

    def create(self, t: T) -> T:
        return NotImplemented

    def delete(self, t: T) -> Optional[T]:
        return NotImplemented

    def hard_delete(self, t: T):
        return NotImplemented

    def update(self, t: T) -> Optional[T]:
        return NotImplemented

    # for get
    def get(self, t_id: str) -> Optional[T]:
        return NotImplemented

    def lists(
        self,
        conditions: ConditionType,
        limit: int,
        offset: int = 0,
        order_by: Optional[str] = None,
    ) -> List[T]:
        ...

    def lists_all(self, conditions: ConditionType) -> List[T]:
        ...
