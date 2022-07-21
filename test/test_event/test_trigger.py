from notion_self_management.event.trigger import Trigger
from notion_self_management.event.events import create_task
from notion_self_management.task_manager.task import Task
from notion_self_management.task_manager.task_manager import TaskManager

a = lambda n: print("create task")


async def test_trigger(dummy_task_manager: TaskManager, dummy_task: Task):
    create_task.connect(a)
    trigger = Trigger(task_manager=dummy_task_manager)
    await trigger.create_task(dummy_task)
