from notion_self_management.expression.expression import Expression
from typing_extensions import Self


class Const(Expression):

    def __new__(cls, *args, **kwargs):
        """Const is a singleton"""
        if getattr(cls, "instance", None) is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def to_json(self) -> str:
        return super().to_json()

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return super().from_json(json_str)


class true(Const):

    def evaluate(self, *args, **kwargs) -> bool:
        return True


class false(Const):

    def evaluate(self, *args, **kwargs) -> bool:
        return False


class empty(Const):
    ...


if __name__ == "__main__":
    assert true() is true()
    assert false() is false()
    assert not (true() is false())
