from notion_self_management.expression.base_variable import Const


class true(Const):
    name = "true"
    type = bool

    def evaluate(self, *args, **kwargs) -> bool:
        return True


class false(Const):
    name = "false"
    type = bool

    def evaluate(self, *args, **kwargs) -> bool:
        return False


class empty(Const):
    name = "false"
    type = bool

    def evaluate(self, *args, **kwargs) -> None:
        return


if __name__ == "__main__":
    assert true() is true()
    assert false() is false()
    assert not (true() is false())
