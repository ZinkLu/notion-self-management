import logging
import os
import time
from functools import cached_property
from typing import Dict, Tuple
from urllib import parse

import httpx
from notion_self_management.client.client import Client
from notion_self_management.client.notion_client import apis
from notion_self_management.client.notion_client import exceptions as e
from notion_self_management.client.notion_client.datatypes.database import DataBase

logger = logging.getLogger("NotionClient")


class AsyncClient(httpx.AsyncClient):
    """
    a simple proxy to check if reach Notion's
    API rate limits and log verbose to request
    if needed
    """

    async def request(self, *args, **kwargs):
        s = time.time()
        logger.debug(f"sending request to Notion API args is {args}, kwargs is {kwargs}")
        res = await super().request(*args, **kwargs)
        logger.debug(f"receive notion's response content is {res.content},"
                     f" status is {res.status_code}, "
                     f"spend {time.time() - s} seconds")
        if res.status_code == 429:
            raise e.RateLimitException
        return res


class Notion(Client):

    @cached_property
    def notion_header(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.api_token}", "Notion-Version": f"{self.notion_version}"}

    async def retrieve_database_schema(self):
        """
        database_id should get a valid notion database object
        check:
        - if the object exists or
        - a database(not a linked database, page or block) or
        - did api_token have access to this database
        all these issues will lead to ``404`` from Notion
        """
        logger.debug("checking if database is available")
        res = await self.client.get(
            parse.urljoin(self.base_url, apis.RETRIEVE_DATABASE.format(database_id=self.database_id)),
            headers=self.notion_header,
        )
        if res.status_code != 200:
            logger.error(f"checking database failed, status is {res.status_code}, content is {res.content}")

        if res.status_code == 404:
            raise e.NoSuchDataBase()
        if res.status_code == 401:
            raise e.UnauthorizedException()

        db = DataBase.from_dict(res.json())  # DB should not change until fresh

        if db.archived:
            raise e.ArchivedObjectException()

        self.db = db

    def __init__(
        self,
        api_token: str,
        database_id: str,
        base_url: str = "https://api.notion.com",
        notion_version: str = "2022-02-22",
    ) -> None:
        """
        use Notion's database as datasource

        ```python
        notion = Notion(os.env.get("API", "DB_ID"))
        await notion.get_rows()
        ```

        Notion client will check if `database_id` exists 
        or not a other type object of notion.

        :param api_token: Notion apiToken which can be create from
                        https://www.notion.so/my-integrations
        :param database_id: database id is notion
        :param base_url: Notion's base url. it could be any 
                        mirror(or CDN) of Notion API if you 
                        reach Notion's API limits frequently
                        https://developers.notion.com/reference/request-limits
        """
        self.base_url = base_url
        self.api_token = api_token
        self.database_id = database_id
        self.notion_version = notion_version
        self.client = AsyncClient(headers=self.notion_header)
        self.db = None

    def __await__(self):
        return self.retrieve_database_schema().__await__()

    def get(self, Id: str):
        ...
