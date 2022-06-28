from dataclasses import dataclass

from notion_self_management.client.notion_client.datatypes.base import NotionObject


@dataclass
class Page(NotionObject):
    ...
    # type: str  # always be Page
