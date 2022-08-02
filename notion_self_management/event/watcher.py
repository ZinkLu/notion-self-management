import asyncio
import datetime
import logging
from threading import Thread

from notion_self_management.event.events import create_task_event, delete_task_event, update_task_event
from notion_self_management.task_manager.task import Task
from notion_self_management.task_manager.task_manager import TaskManager

logger = logging.getLogger("watcher")


class Watcher:
    """
    Watcher class

    Watcher will poll data from `notion_self_management.task_manager.task_manager.TaskManager`
    if user modify data from "third" side (eg., notion application), any updated data will be
    captured for a period of time, and proper Event will be sent to `HandlerManager`.
    """

    def __init__(
        self,
        task_manager: TaskManager,
        period: float = 5.0,
        ensure_each_poll: bool = True,
        threaded: bool = False,
    ) -> None:
        """
        :param task_manager: instance of `notion_self_management.task_manager.task_manager.TaskManager`
        :param period: sleeping time during each poll, defaults to 5.0 second. This value can't be too
                       small in case to reach task_db's limit rate.
        :param ensure_each_poll: In order to emit correct event, Watcher will take all updated tasks
                                and exists notes into comparison, which costs time. `ensure_each_poll`
                                tells `Watcher` whether to wait for events or not. If `ensure_each_poll`
                                is False, `Watcher` will only create `Future` and go to the next poll
                                Immediately.
                                **Warning**: Same event can be triggered multiple times if set to True.
        :param threaded: If True,`Watcher` will start a new event loop and poll on another thread,
                         otherwise `Watcher` will attach to current event loop, but won't start
                         current event loop. You must call `asyncio.get_event_loop().run_forever()`
                         manually if current loop is not running.
        """
        self.task_manager = task_manager
        self.period = period
        self.ensure = ensure_each_poll
        self.threaded = threaded
        self.thread = None
        self.is_cancel = False

    def start_poll(self):
        """
        start polling.
        """
        logger.debug(f"watcher {self} start to poll")

        if self.threaded:
            t = Thread(target=self._run)
            self.thread = t
            t.start()
        else:
            self._run()

    def _run(self):
        if self.threaded:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop = asyncio.get_event_loop()
        loop.create_task(self._poll())

        if self.thread:
            loop.run_forever()

    async def trigger_event(self, task: Task):
        """
        `trigger_event` will check the task's notes and
        emit correct event.

        - emit `create_event` when no note related to the task.
        - emit `update_task` when `task_manager._is_idempotent`
                return False.
        - emit `delete_task` when task is confirmed updated and
               `task.is_active` is False while last note's is True.
        """
        exist_note = await self.task_manager.get_current_note_by_task(task.task_id)

        # create
        if not exist_note:
            note = await self.task_manager.take_note(task, None)
            logger.debug(f"trigger create event for task {task}")
            await create_task_event.emit(note)
            return

        note = await self.task_manager.update_task(task)
        if not note:
            logger.error(f"update event trigger failed cause no note related to task {task}")
            return

        # is update occur?
        if self.task_manager._is_idempotent(task, note):
            # no update occurs.
            logger.info(f"task {task} is idempotent skipping..")
            return

        # update occurs
        # delete
        if note.previous is None or (previous := await self.task_manager.get_note(note.previous)) is None:
            logger.error(f"update event trigger failed cause note {note} has no previous version")
            return

        if note.active is False and previous.active is True:
            logger.debug(f"trigger delete event for task {task}")
            await delete_task_event.emit(note)
            return

        # update
        logger.debug(f"trigger update event for task {task}")
        await update_task_event.emit(note)

    def cancel(self):
        """
        Cancel polling.
        If `self.threaded` is True, Watcher will stop the event loop on this own thread.
        """
        self.is_cancel = True

    async def _poll(self):
        """
        `_poll` will query updated task for a period of time.
        If `self.ensure` is true, next poll shall start after
        all updated tasks will have been handled properly.
        If `self.ensure` is false, Watcher will only create
        Future and start another poll immediately.
        """
        gap = datetime.timedelta(seconds=self.period)
        start_time = datetime.datetime.now()
        loop = asyncio.get_event_loop()

        while True:
            if self.is_cancel:
                if self.threaded:
                    loop.stop()
                return
            logger.debug(f"poll user data start, from {start_time} to {start_time + gap}")
            await asyncio.sleep(self.period)
            await self._per_poll(loop, start_time, start_time + gap)
            start_time = start_time + gap  # reset start time

    async def _per_poll(
        self,
        loop: asyncio.AbstractEventLoop,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
    ):
        condition = start_time <= Task.update_time <= end_time
        tasks = await self.task_manager.get_tasks(condition)
        if self.ensure:
            await asyncio.wait([self.trigger_event(t) for t in tasks])
        else:
            for t in tasks:
                loop.create_task(self.trigger_event(t))
