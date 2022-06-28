from dataclasses import dataclass
from typing import Dict, List, Union, Optional

from notion_self_management.client.notion_client.datatypes.base import NotionObject
from notion_self_management.client.notion_client.datatypes.emoji import Emoji
from notion_self_management.client.notion_client.datatypes.file import ExternalFile, File
from notion_self_management.client.notion_client.datatypes.properties import PROPERTIES
from notion_self_management.client.notion_client.datatypes.rich_text import RichText


@dataclass
class Parent:
    type: str
    page_id: str
    workspace: bool


@dataclass
class DataBase(NotionObject):
    """https://developers.notion.com/reference/database"""
    title: List[RichText]
    cover: Optional[ExternalFile]
    url: str
    icon: Optional[Union[File, Emoji]]
    properties: Dict[str, PROPERTIES]
    description: List[RichText]
