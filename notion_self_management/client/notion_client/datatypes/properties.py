from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union

from notion_self_management.client.notion_client.datatypes.color import Color


# Enum
class PropertyType(Enum):
    title = "title"
    rich_text = "rich_text"
    number = "number"
    select = "select"
    multi_select = "multi_select"
    date = "date"
    people = "people"
    files = "files"
    checkbox = "checkbox"
    url = "url"
    email = "email"
    phone_number = "phone_number"
    formula = "formula"
    relation = "relation"
    rollup = "rollup"
    created_time = "created_time"
    created_by = "created_by"
    last_edited_time = "last_edited_time"
    last_edited_by = "last_edited_by"


class NumberFormat(Enum):
    number = "number"
    number_with_commas = "number_with_commas"
    percent = "percent"
    dollar = "dollar"
    canadian_dollar = "canadian_dollar"
    euro = "euro"
    pound = "pound"
    yen = "yen"
    ruble = "ruble"
    rupee = "rupee"
    won = "won"
    yuan = "yuan"
    real = "real"
    lira = "lira"
    rupiah = "rupiah"
    franc = "franc"
    hong_kong_dollar = "hong_kong_dollar"
    new_zealand_dollar = "new_zealand_dollar"
    krona = "krona"
    norwegian_krone = "norwegian_krone"
    mexican_peso = "mexican_peso"
    rand = "rand"
    new_taiwan_dollar = "new_taiwan_dollar"
    danish_krone = "danish_krone"
    zloty = "zloty"
    baht = "baht"
    forint = "forint"
    koruna = "koruna"
    shekel = "shekel"
    chilean_peso = "chilean_peso"
    philippine_peso = "philippine_peso"
    dirham = "dirham"
    colombian_peso = "colombian_peso"
    riyal = "riyal"
    ringgit = "ringgit"
    leu = "leu"
    argentine_peso = "argentine_peso"
    uruguayan_peso = "uruguayan_peso"


class RollupFunctionType(Enum):
    count_all = "count_all"
    count_values = "count_values"
    count_unique_values = "count_unique_values"
    count_empty = "count_empty"
    count_not_empty = "count_not_empty"
    percent_empty = "percent_empty"
    percent_not_empty = "percent_not_empty"
    sum = "sum"
    average = "average"
    median = "median"
    min = "min"
    max = "max"
    range = "range"
    show_original = "show_original"


# component
@dataclass
class Option:
    id: str
    name: str
    color: Color


@dataclass
class EmptyObject:
    pass


# property
@dataclass
class Property:
    id: str
    type: PropertyType
    name: str


@dataclass
class TitleProperty(Property):
    title: EmptyObject


@dataclass
class TextProperty(Property):
    rich_text: EmptyObject


@dataclass
class NumberProperty(Property):
    format: NumberFormat


@dataclass
class SelectProperty(Property):
    options: Option


@dataclass
class MultiSelectProperty(Property):
    options: List[Option]


@dataclass
class DateProperty(Property):
    date: EmptyObject


@dataclass
class PeopleProperty(Property):
    people: EmptyObject


@dataclass
class FilesProperty(Property):
    files: EmptyObject


@dataclass
class CheckboxProperty(Property):
    checkbox: EmptyObject


@dataclass
class URLProperty(Property):
    url: EmptyObject


@dataclass
class EmailProperty(Property):
    email: EmptyObject


@dataclass
class PhoneNumberProperty(Property):
    phone_number: EmptyObject


@dataclass
class FormulaProperty(Property):
    expression: str


@dataclass
class RelationProperty(Property):
    database_id: str
    synced_property_name: Optional[str]
    synced_property_id: Optional[str]


@dataclass
class RollupProperty(Property):
    relation_property_name: str
    relation_property_id: str
    rollup_property_name: str
    rollup_property_id: str
    function: RollupFunctionType


@dataclass
class CreateTimeProperty(Property):
    create_by = EmptyObject


@dataclass
class CreateByProperty(Property):
    create_time = EmptyObject


@dataclass
class LastEditedTimeProperty(Property):
    last_edited_time = EmptyObject


@dataclass
class LastEditedByProperty(Property):
    last_edited_by = EmptyObject


PROPERTIES = Union[TitleProperty, TextProperty, NumberProperty, SelectProperty, MultiSelectProperty, DateProperty,
                   PeopleProperty, FilesProperty, CheckboxProperty, URLProperty, EmailProperty, PhoneNumberProperty,
                   FormulaProperty, RelationProperty, RollupProperty, CreateTimeProperty, CreateByProperty,
                   LastEditedTimeProperty, LastEditedByProperty, ]


@dataclass
class Date:
    start: str
    end: str
    time_zone: str