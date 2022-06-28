from dataclasses import fields, dataclass
from types import MappingProxyType

from typing import Type, TypeVar
from notion_self_management.expression.bool_expression import Condition

from notion_self_management.expression.variable import Variable

# DataClass = TypeVar("DataClass")

IDENT = "__is_filter__"


def dataclass_filter(cls=None, /, *, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False):
    """
    Make a dataclass fields into instance of `notion_self_management.expression.variable.Variable`

    ```python
    @dataclass_filter
    class A:
        a: int

    condition = (A.a == 1) # type: notion_self_management.expression.bool_expression.Condition

    it's also can be use as a python dataclass

    ```python
    a = A(a=1)

    print(a.a) # 1
    ```

    > WARNING
        >> always use a keyword args to init a dataclass.
        Because `__annotations__`  order can be changed
        during modifying the class.
    """

    def wrap(cls):
        # process Variable instance, we must fetch Variable out
        # because dataclass will seen Variable as a filed with
        # default value
        annotations = cls.__dict__.get('__annotations__', {})
        if not hasattr(cls, "__annotations__"):
            cls.__annotations__ = annotations

        # pop all Variable and set then back later
        setback = list()
        for klass in cls.__mro__[-1:0:-1]:
            if hasattr(klass, IDENT):
                keys = [k for k, v in klass.__dict__.items() if isinstance(v, Variable)]
                for k in keys:
                    delattr(klass, k)
                delattr(klass, IDENT)
                setback.append(klass)

        pop_list = []
        for k, v in cls.__dict__.items():
            if isinstance(v, Variable):
                pop_list.append(k)
                annotations[k] = v.type

        [delattr(cls, p) for p in pop_list]

        kls = dataclass(cls, init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash, frozen=frozen)
        setback.append(kls)

        # set back
        for klass in setback:
            setattr(kls, IDENT, True)
            for f in fields(klass):
                setattr(klass, f.name, Variable(f.type, f.name))

        return kls

    if cls is None:
        return wrap

    return wrap(cls)


class DataClassMeta(type):
    """
    TODO: implement this
    DataClassMeta helps create a dataclass
    using `Variable` instance

    ```python
    class A(metaclass=DataClassMeta):
        a = Variable(int)
    ```

    while A is a dataclass and it can have
    api in `Variable`.
    """
    ...
