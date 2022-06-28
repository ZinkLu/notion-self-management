import os
from notion_self_management.client.notion_client.client import Notion
from pytest import mark, fixture


@fixture
def notion_key() -> str:
    return os.environ.get("NOTION_KEY") or ""


@fixture
def notion_database_id() -> str:
    return os.environ.get("NOTION_DATABASE_ID") or ""


async def test_client(notion_key, notion_database_id):
    notion = await Notion(notion_key, notion_database_id)
