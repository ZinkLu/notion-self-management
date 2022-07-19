import operator as op

from notion_self_management.expression.base_formula import Formula, Number


# some built in Formula
class Add(Formula):
    return_type = Number
    arg_types = [Number, Number]
    func = op.add


class Sub(Formula):
    return_type = Number
    arg_types = [Number, Number]
    func = op.sub


class Mul(Formula):
    return_type = Number
    arg_types = [Number, Number]
    func = op.sub


class Div(Formula):
    return_type = Number
    arg_types = [Number, Number]
    func = op.truediv


class Concat(Formula):
    return_type = str
    arg_types = [str, str]
    func = op.add


class Replace(Formula):
    return_type = str
    arg_types = [str, str, str]

    @staticmethod
    def func(x, y, z):
        return str.replace(x, y, z)


if __name__ == "__main__":
    Replace()
