from notion_self_management.task_manager.task_manager import TaskManager


class Watcher:
    """
    Watcher class

    Watcher will poll data from `notion_self_management.task_manager.task_manager.TaskManager`
    if user modify data from "third" side (eg., notion application), any updated data will be
    captured for a period of time, and proper Event will be sent to `HandlerManager`.
    """

    def __init__(self, task_manager: TaskManager, ) -> None:
        pass
