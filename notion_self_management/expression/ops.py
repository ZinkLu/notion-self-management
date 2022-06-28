import operator as op
from enum import Enum


class LogicalOperator(Enum):
    and_ = "&"
    or_ = "|"


class BoolOperator(Enum):
    lt = op.lt
    le = op.le
    gt = op.gt
    ge = op.ge
    eq = op.eq
    ne = op.ne


BoolOperatorInv = {
    BoolOperator.ne: BoolOperator.eq,
    BoolOperator.eq: BoolOperator.ne,
    BoolOperator.le: BoolOperator.ge,
    BoolOperator.ge: BoolOperator.le,
    BoolOperator.lt: BoolOperator.gt,
    BoolOperator.gt: BoolOperator.lt,
}
