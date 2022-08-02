from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

from notion_self_management.expression.utils import dataclass_filter


@dataclass_filter
@dataclass
class Task:
    task_id: str

    create_time: datetime
    update_time: datetime
    create_by: str  # this will not be used
    update_by: str  # this will not be used

    title: str
    content: str
    status: str
    due_date: datetime
    start_date: datetime
    tags: List[str]
    is_done: bool
    active: bool
    percent: int
    extras_field: Dict[str, Any]

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Task):
            return False
        return self.task_id == __o.task_id

    def __hash__(self) -> int:
        return hash(self.task_id)
