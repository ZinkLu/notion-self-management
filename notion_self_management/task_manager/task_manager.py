from dataclasses import asdict
import datetime
from typing import Optional
from uuid import uuid4
from notion_self_management.client.client import Client
from notion_self_management.task_manager.note import Note
from notion_self_management.task_manager.task import Task


class TaskManager:
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
    """

    def __init__(
        self,
        data_client: Client[Task],
        note_client: Client[Note],
        maximum_note: int = 100,
    ) -> None:
        self.task_db = data_client
        self.note_db = note_client
        self._maximum_note = maximum_note

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """get a task by it's task_id"""
        return self.task_db.get(task_id)

    # TASKS METHODS
    def create_task(self, task: Task) -> Note:
        """create a task"""
        task = self.task_db.create(task)
        return self._take_note(task)

    def update_task(self, task: Task) -> Note:
        """
        update task will return the note of the task.
        which have the extract value of the task.
        """
        self.task_db.update(task)
        return self._take_note(task)

    def delete_task(self, task: Task) -> Note:
        """
        delete task will not take a note
        """
        self.task_db.delete(task)
        return self._take_note(task)

    # NOTES METHODS
    def get_current_note_by_task(self, task_id: str) -> Optional[Note]:
        """get the latest Note of a Task"""
        notes = self.note_db.lists(Note.task_id == task_id, limit=1)
        if not notes:
            return
        return notes[0]

    def _take_note(self, task: Task) -> Note:
        previous_note = self.get_current_note_by_task(task.task_id)
        previous = previous_note and previous_note.version or None
        note = Note(version=str(uuid4()),
                    note_time=datetime.datetime.now(),
                    previous=previous,
                    following=None,
                    **asdict(task))  # type: ignore
        return self.note_db.create(note)
