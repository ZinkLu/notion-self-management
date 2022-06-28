from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from notion_self_management.client.notion_client.datatypes.color import Color
from notion_self_management.client.notion_client.datatypes.properties import Date
from notion_self_management.client.notion_client.datatypes.user import User


# enums
class MentionType(Enum):
    user = "user"
    page = "page"
    database = "database"
    date = "date"
    link_preview = "link_preview"


class RichTextType(Enum):
    mention = "mention"
    text = "text"
    equation = "equation"


# component
@dataclass
class Annotations:
    bold: bool
    italic: bool
    strikethrough: bool
    underline: bool
    code: bool
    color: Color


@dataclass
class Link:
    type: str  # always url
    url: str


@dataclass
class Text:
    content: str
    link: Optional[Link]


@dataclass
class Mention:
    type: MentionType


@dataclass
class UserMention(Mention):
    user: User


@dataclass
class Reference:
    id: str


@dataclass
class DatabaseMention(Mention):
    database: Reference


@dataclass
class PageMention(Mention):
    page: Reference


@dataclass
class DateMention(Mention):
    date: Date


@dataclass
class TemplateMention(Mention):
    template_mention_date: str  # today/now
    template_mention_user: str  # me


# rich content
@dataclass
class RichContent:
    """https://developers.notion.com/reference/rich-text"""
    plain_text: str
    href: Optional[str]
    annotations: Annotations
    type: RichTextType


@dataclass
class RichText(RichContent):
    """type is text"""
    text: Text


@dataclass
class RichMention(RichContent):
    mention: Union[UserMention, DatabaseMention, DateMention, TemplateMention, PageMention]


# other can be see as RichContent
@dataclass
class Equation:
    expression: str


@dataclass
class LinkPreview:
    url: str
