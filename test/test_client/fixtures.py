from dataclasses import asdict
from datetime import datetime, timedelta
from typing import List, Optional

import pytest
from notion_self_management.client.client import Client
from notion_self_management.task_manager.note import Note
from notion_self_management.task_manager.task import Task
from notion_self_management.task_manager.task_manager import TaskManager


@pytest.fixture
def dummy_task_manager():
    return TaskManager(DummyClient(), DummyClient())


@pytest.fixture
def dummy_task():
    return Task(
        task_id="1",
        create_time=datetime.now(),
        update_time=datetime.now(),
        create_by="dummy",
        update_by="dummy",
        title="task1",
        content="ajfjs",
        status="done",
        tags=[],
        due_date=datetime.now() + timedelta(days=7),
        start_date=datetime.now(),
        active=True,
        percent=100,
        is_done=True,
        extras_field={},
    )


@pytest.fixture()
def dummy_note(dummy_task: Task):
    return Note(
        **asdict(dummy_task),
        version="001",
        note_time=datetime.now(),
        previous=None,
    )


class DummyClient(Client[Note]):

    async def create(self, t: Note) -> Note:
        return t

    async def delete(self, t: Note) -> Optional[Note]:
        return None

    async def hard_delete(self, t: Note):
        return t

    async def update(self, t: Note) -> Optional[Note]:
        return t

    # for get
    async def get(self, t_id: str) -> Optional[Note]:
        return None

    async def lists(
        self,
        conditions,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by=None,
        desc: bool = False,
    ) -> List[Note]:
        return []

    async def lists_all(self, conditions) -> List[Note]:
        return []
