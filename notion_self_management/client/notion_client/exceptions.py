class NotionClientException(Exception):
    msg = "A Problem happened to Notion"


class NoSuchDataBase(NotionClientException):
    msg = ("The dataBase does not exist, "
           "or the id is not a database,"
           "or the extension doesn't have"
           "access to the database. check"
           "the docs to solve this issue")


class UnauthorizedException(NotionClientException):
    msg = ("Extension API Key is invalid, Please"
           "check https://developers.notion.com/docs"
           "to get more information")


class RateLimitException(NotionClientException):
    msg = ("you have reach Notion's Rate limits, Please check "
           "https://developers.notion.com/reference/request-limits "
           "to get more information")


class ArchivedObjectException(NotionClientException):
    msg = "Notion's object has been archived"