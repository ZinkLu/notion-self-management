from pathlib import Path

import ujson
from notion_self_management.client.notion_client.datatypes.database import DataBase
from notion_self_management.client.notion_client.datatypes.properties import CreateTimeProperty
from pytest import fixture


@fixture
def database_json() -> dict:
    return ujson.load((Path(__file__).parent / "database.json").open())


def test_deserialized(database_json):
    db = DataBase.from_dict(database_json)
    assert isinstance(db.properties["createTime"], CreateTimeProperty)
