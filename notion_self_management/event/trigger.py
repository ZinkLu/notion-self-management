from typing import List, Optional, TypeVar

from notion_self_management.event.events import create_task_event, update_task_event, delete_task_event
from notion_self_management.task_manager.note import Note
from notion_self_management.task_manager.task import Task
from notion_self_management.task_manager.task_manager import TaskManager

T = TypeVar("T")


class Trigger:
    """
    Trigger class

    Trigger class is a proxy to `notion_self_management.task_manager.task_manager.TaskManager`.
    if user modify data on "our" side (maybe admin page), instead of using origin TaskManager,
    `Trigger` should be used to send proper events, so that any user modifications Event will be
    sent to `HandlerManager`.

    If user modify data on "third" side (eg., notion application), `Watcher` should do the work.
    """

    def __init__(
        self,
        task_manager: TaskManager,
    ) -> None:
        self.task_manager = task_manager

    async def get_tasks(
        self,
        condition,
        limit=None,
        offset=None,
        order_by=None,
        desc=None,
    ):
        return await self.task_manager.get_tasks(condition, limit, offset, order_by, desc)

    async def get_task_by_id(self, task_id: str) -> Optional[Task]:
        return await self.task_manager.get_task_by_id(task_id)

    async def create_task(self, task: Task) -> Note:
        note = await self.task_manager.create_task(task)
        await create_task_event.emit(note)
        return note

    async def update_task(self, task: Task) -> Optional[Note]:
        note = await self.task_manager.update_task(task)
        if note is not None:
            await update_task_event.emit(note)
        return note

    async def delete_task(self, task: Task) -> Optional[Note]:
        note = await self.task_manager.update_task(task)
        if note is not None:
            await delete_task_event.emit(note)
        return await self.task_manager.delete_task(task)

    # NOTES METHODS
    async def get_current_note_by_task(self, task_id: str) -> Optional[Note]:
        return await self.task_manager.get_current_note_by_task(task_id)

    async def get_note(self, version: str) -> Optional[Note]:
        return await self.task_manager.get_note(version)

    async def get_following_note(self, version: str) -> Optional[Note]:
        return await self.task_manager.get_following_note(version)

    async def take_note(self, task: Task, previous_version: Optional[str] = None) -> Note:
        return await self.task_manager.take_note(task, previous_version)

    async def delete_notes(
        self,
        notes: List[Note],
        check_dependency=True,
    ) -> bool:
        return await self.task_manager.delete_notes(notes, check_dependency)


def get_trigger(task_manager: TaskManager) -> TaskManager:
    return Trigger(task_manager)  # type: ignore
