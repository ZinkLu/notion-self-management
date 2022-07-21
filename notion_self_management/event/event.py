from contextvars import ContextVar
from inspect import isawaitable
from typing import Any, Callable, TypedDict
from weakref import WeakSet

from notion_self_management.task_manager.note import Note


class Event:

    def __init__(self, name) -> None:
        self.name = name
        self.handlers = WeakSet()

    def connect(self, handler: Callable[[Note], Any]):
        """
        Handler always takes `notion_self_management.task_manager.note.Note`
        as it's only argument.
        """
        self.handlers.add(handler)

    async def emit(self, note: Note):
        """
        Emit a event
        """
        for h in self.handlers:
            res = h(note)
            if isawaitable(res):
                await res
