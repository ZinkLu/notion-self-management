from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from notion_self_management.expression.utils import dataclass_filter
from notion_self_management.task_manager.task import Task


@dataclass_filter
class Note(Task):
    """
    if task be modify with a existing following,
    the following will be None.

    All Notes whose previous is same but don't have
    the latest create_time will be will be deleted 

    A maximum times of note can be taken should be
    set for performance considerations
    """
    version: str
    note_time: datetime
    previous: Optional[str]  # a previous version str
    # following: Optional[str]
