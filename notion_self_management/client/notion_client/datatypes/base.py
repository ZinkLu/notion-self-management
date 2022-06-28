from dataclasses import dataclass
from enum import Enum

from dacite.config import Config
from dacite.core import from_dict


class Base:

    @classmethod
    def from_dict(cls, data: dict):
        return from_dict(cls, data, config=Config(cast=[Enum]))


@dataclass
class PartialUser:
    object: str
    id: str


@dataclass
class NotionObject(Base):
    object: str
    id: str
    created_time: str  # ISO FORMATTER DATETIME str
    created_by: PartialUser
    last_edited_time: str  # ISO FORMATTER DATETIME str
    last_edited_by: PartialUser
    archived: bool
