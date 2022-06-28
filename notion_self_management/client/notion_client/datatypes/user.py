from enum import Enum
from dataclasses import dataclass

from notion_self_management.client.notion_client.datatypes.base import NotionObject


class UserType(Enum):
    bot = "bot"
    person = "person"




@dataclass
class User(NotionObject):
    name: str
    avatar_url: str
    type: UserType  # person or bot
