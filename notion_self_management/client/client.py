from typing import Generic, List, Optional, TypeVar

from notion_self_management.expression.base_condition import ConditionType
from notion_self_management.expression.variable import Variable
from notion_self_management.task_manager.note import Note
from notion_self_management.task_manager.task import Task

T = TypeVar("T", Note, Task)


class Client(Generic[T]):

    async def create(self, t: T) -> T:
        return NotImplemented

    async def delete(self, t: T) -> Optional[T]:
        return NotImplemented

    async def hard_delete(self, t: T):
        return NotImplemented

    async def update(self, t: T) -> Optional[T]:
        return NotImplemented

    # for get
    async def get(self, t_id: str) -> Optional[T]:
        return NotImplemented

    async def lists(
        self,
        conditions: ConditionType,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Variable]] = None,
        desc: bool = False,
    ) -> List[T]:
        return NotImplemented

    async def lists_all(self, conditions: ConditionType) -> List[T]:
        return NotImplemented
