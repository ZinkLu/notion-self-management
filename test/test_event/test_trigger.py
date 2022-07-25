import asyncio
import time

import pytest
from notion_self_management.event.trigger import Trigger
from notion_self_management.event.watcher import Watcher
from notion_self_management.event.events import create_task_event
from notion_self_management.expression.consts import true
from notion_self_management.task_manager.task import Task
from notion_self_management.task_manager.task_manager import TaskManager

a = lambda n: print("create task")


@create_task_event.connect
async def s(n):
    await asyncio.sleep(0.1)


async def test_trigger(dummy_task_manager: TaskManager, dummy_task: Task):
    s = time.time()
    create_task_event.connect(a)
    trigger = Trigger(task_manager=dummy_task_manager)
    await trigger.create_task(dummy_task)
    assert time.time() - s > 0.1


# @pytest.mark.skip
def test_watcher_1(dummy_task_manager: TaskManager):
    s = time.time()
    a = Watcher(dummy_task_manager, threaded=True, ensure_each_poll=True, period=0.1)
    a.start_poll()
    time.sleep(0.5)
    a.cancel()
    a.thread.join()
    assert time.time() - s > 10.5


def test_watcher_2(dummy_task_manager: TaskManager):
    s = time.time()
    a = Watcher(dummy_task_manager, threaded=True, ensure_each_poll=False, period=0.1)
    a.start_poll()
    time.sleep(0.5)
    a.cancel()
    a.thread.join()
    assert time.time() - s > 5.5


async def test(dummy_task_manager: TaskManager):
    notes = await dummy_task_manager.get_tasks(true())
    print(notes)
