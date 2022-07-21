import datetime
import logging
import time
from dataclasses import asdict
from typing import Callable, List, Optional

from notion_self_management.client.client import Client
from notion_self_management.task_manager.note import Note
from notion_self_management.task_manager.task import Task

logger = logging.getLogger("TaskManager")


class TaskManager:

    def __init__(
        self,
        data_client: Client[Task],
        note_client: Client[Note],
        maximum_notes: int = 100,
        idempotent_function: Callable[[Task, Note], bool] = lambda t, n: t.update_time == n.update_time,
    ) -> None:
        """
        TaskManager is a core role in this project

        The manager takes two `Client` as it's source

        One Client is for user data, aka Task data.which
        will be created or modified by user.

        The other Client is responsible for log data, aka
        Note data. every modification will be logged. the
        logged data can be used in `event-handlers` or
        `cron-handler`. And can be applied to user data
        in the admin page.

        :param data_client: user data client
        :param note_client: note data client
        :param maximum_note: After a note is taken, TaskManager will check
                             if a task's notes have reach them maximum count.
                             the oldest note will be deleted permanently.
                             `None` means there is not limits.
                             defaults to 100
        :param idempotent_function: when a note is taken, `idempotent_function` is
                                    used to determine weather a note is actually
                                    modified. default idempotent function will com-
                                    pare Task's `update_date` with it's latest note's
                                    `idempotent_function` is a Callable takes a `Note`
                                    instance and a `Task` instance and return bool type.
        """
        self.task_db = data_client
        self.note_db = note_client
        self._maximum_notes = maximum_notes
        self._is_idempotent = idempotent_function

    async def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Get a task by it's task_id
        """
        return await self.task_db.get(task_id)

    # TASKS METHODS
    async def _create_task(self, task: Task) -> Task:
        task = await self.task_db.create(task)
        return task

    async def create_task(self, task: Task) -> Note:
        """
        Create a task
        """
        task = await self._create_task(task)
        return await self.take_note(task)

    async def _update_task(self, task: Task) -> Optional[Task]:
        return await self.task_db.update(task)

    async def update_task(self, task: Task) -> Optional[Note]:
        """
        Update task will return the current note of the task.
        """
        t = await self._update_task(task)
        if not t:
            print(t)
            return
        return await self.take_note(t)

    async def delete_task(self, task: Task) -> Optional[Note]:
        """
        Delete task only change task's active to `False`.
        And a note will be taken to record this update.
        """
        task.active = False
        return await self.update_task(task)

    # NOTES METHODS
    async def get_current_note_by_task(self, task_id: str) -> Optional[Note]:
        """Get the latest Note of a Task"""
        notes = await self.note_db.lists(Note.task_id == task_id, limit=1, order_by=[Note.note_time])
        if not notes:
            return
        return notes[0]

    async def get_note(self, version: str) -> Optional[Note]:
        """
        Get a note by it's version(id)
        """
        return await self.note_db.get(version)

    async def get_following_note(self, version: str) -> Optional[Note]:
        """
        Get a note's following note

        v1 -> v2

        v2 = get_following_note(v1.version)
        """
        notes = await self.note_db.lists(Note.previous == version, limit=1)
        if not notes:
            return
        return notes[0]

    async def _check_maximum(self, note: Note):
        if self._maximum_notes:
            outdate_note = await self.note_db.lists(
                Note.task_id == note.task_id,
                offset=self._maximum_notes,
                order_by=[Note.note_time],
            )
            await self.delete_notes(outdate_note)

    @staticmethod
    def _get_notes_version() -> str:
        """
        a note's version is a sortable
        string.
        default to the string of millisecond
        timestamp.
        """
        return str(int(time.time() * 1000))

    async def take_note(self, task: Task, previous_version: Optional[str] = None) -> Note:
        """
        Take note is idempotent. Which means a task *only* can be
        noted if the idempotent function return `False`, otherwise,
        `take_note` will consider the Task is the same as current
        Task.

        default idempotent function will check weather Task's
        `update_time` equals to latest Note's.

        a previous note can be passed which means we want to rebuild
        the chain of note. this happens when we revert the task to the
        specified version of note and continue to edit on the this version
        of the task.

        ```text
        v1 - v2 - v3 - v4
                       ^(head)

        revert to v2

        v1 - v2 - v3 - v4
             ^(head)

        continue to edit.
                 - v3 - v4  we should delete this whole branch
                |
        v1 - v2 - v3'
                   ^(head)
        ```

        :param task: task which will be noted.
        :param previous_version: a truncate point.
        """
        if previous_version:
            previous_note = await self.get_note(previous_version)
        else:
            previous_note = await self.get_current_note_by_task(task.task_id)

        # if idempotent_function define the task is not modified, return current
        # latest note back.
        if previous_note and self._is_idempotent(task, previous_note):
            return previous_note

        previous = previous_note and previous_note.version or None
        note = Note(version=self._get_notes_version(),
                    note_time=datetime.datetime.now(),
                    previous=previous,
                    **asdict(task))  # type: ignore

        if previous is not None:
            deleted_notes = await self.note_db.lists_all(Note.note_time > previous)
            await self.delete_notes(deleted_notes)

        return await self.note_db.create(note)

    async def delete_notes(
        self,
        notes: List[Note],
        check_dependency=True,
    ) -> bool:
        """
        delete a note *permanently* it will cause a broken
        chain of notes.

        ```text
        v1 -> v2 -> v3
        ```

        if v2 is deleted, v3's dependency is broken.

        return true if deleted perform successfully.

        :param notes: notes which need to be deleted
        :param check_dependency: check if version dependency will broke
                                 current we perform check forcibly.
        """
        if not check_dependency:
            logger.warning("dependency check will be perform forcibly")

        notes.sort(key=lambda x: x.note_time)
        previous = None  # type: Note
        for n in notes:
            if previous and previous.version != n.previous:
                return False  # not continuous notes
            previous = n

        if previous:  # check
            if await self.get_following_note(previous.version):  # raise if the last has a following note
                return False

        for n in notes:
            await self.note_db.delete(n)

        return True
