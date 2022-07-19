from dataclasses import asdict, dataclass
from datetime import datetime
from io import StringIO
from typing import Union

from notion_self_management.expression.conditions import Condition, ConditionList
from notion_self_management.expression.formula import Concat, Replace
from notion_self_management.expression.utils import dataclass_filter
from notion_self_management.expression.variable import Variable


@dataclass_filter
class Book:
    name = Variable(str)
    author = Variable(str)
    publish_date: datetime


def test_eq():
    f1 = (Book.name == "Python")
    f2 = (Book.name == "Java")
    book = Book(name="Python", author="Lu", publish_date=datetime.now())

    book_dic = asdict(book)
    assert f1.evaluate(**book_dic)
    assert not f2.evaluate(**book_dic)
    assert not (f1 & f2).evaluate(**book_dic)
    assert (f1 | f2).evaluate(**book_dic)


def test_inv_eq():
    f1 = ("Python" == Book.name)
    f2 = ("Java" == Book.name)
    book = Book(name="Python", author="Lu", publish_date=datetime.now())
    book_dic = asdict(book)
    assert f1.evaluate(**book_dic)  # works but lose type hints
    assert not f2.evaluate(**book_dic)
    assert not (f1 & f2).evaluate(**book_dic)
    assert (f1 | f2).evaluate(**book_dic)


def test_not():
    f1 = (Book.name == "Python")
    f2 = (Book.name == "Java")
    book = Book(name="Python", author="Lu", publish_date=datetime.now())

    book_dic = asdict(book)
    assert not f1.not_().evaluate(**book_dic)
    assert (~f2).evaluate(**book_dic)
    assert (f1 & f2).not_().evaluate(**book_dic)
    assert not (~(f1 | f2)).evaluate(**book_dic)


def test_formula():
    book = Book(name="Python", author="Lu", publish_date=datetime.now())
    f1 = Concat(Book.name, Book.author)
    result = f1.evaluate(**asdict(book))
    assert result == "PythonLu"

    f2 = Replace(Book.name, "Python", "Java")
    result = f2.evaluate(**asdict(book))
    assert result == "Java"


def to_sql(expression):
    expression_list = parse_condition_list(expression)
    expression_list.seek(0)
    print(expression_list.read())


def parse_condition_list(expression: Union[ConditionList, Condition], result=None) -> StringIO:
    result = result or StringIO()

    if isinstance(expression, Condition):
        result.write(f"{expression.left.name} {expression.op.value} {expression.right}")
        return result

    tmp = []  # (condition and condition and condition)
    for i in expression.clauses:
        if isinstance(i, Condition):
            tmp.append(f"{i.left.name} {i.op.value} {i.right}")
        elif isinstance(i, ConditionList):
            io = parse_condition_list(i)
            io.seek(0)
            tmp.append(io.read())

    t = f" {expression.op.value} ".join(tmp)
    result.write(f"({t})")
    return result
