import asyncio
import datetime
import logging
from threading import Thread

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
        period: float = 5,
        ensure_each_poll: bool = True,
        threaded: bool = False,
    ) -> None:
        """
        :param task_manager: instance of `notion_self_management.task_manager.task_manager.TaskManager`
        :param period: sleeping time during each poll, defaults to 5 second. This value can't be too
                       small in case to reach task_db's limit rate.
        :param ensure_each_poll: In order to emit correct event, Watcher will take updated tasks and
                                exists notes into comparison
                                 
        :param threaded:
        """
        self.task_manager = task_manager
        self.period = period
        self.ensure = ensure_each_poll
        self.threaded = threaded
        self.thread = None
        self.is_cancel = False

    def start_poll(self):
        """
        `start_poll` will add `Watcher` into current event loop
        and start tasks
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
        :param task: _description_
        """
        await asyncio.sleep(0)

    def cancel(self):
        """
        cancel polling
        :param stop_loop: _description_, defaults to False
        :type stop_loop: bool, optional
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
        print(tasks)
        if self.ensure:
            await asyncio.wait([self.trigger_event(t) for t in tasks])
        else:
            for t in tasks:
                loop.create_task(self.trigger_event(t))
