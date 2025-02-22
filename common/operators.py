from enum import Enum


OP_EQ = "eq"
OP_GT = "gt"
OP_GTE = "gte"
OP_LT = "lt"
OP_LTE = "lte"
OP_IN = "in_"
OP_BETWEEN = "between"
OP_LIKE = "like"
OP_ILIKE = "ilike"
OP_NOT_EQ = "not_eq"
OP_NOT_IN = "not_in"
OP_NOT_LIKE = "not_like"
OP_NOT_BETWEEN = "not_between"

OPERATORS = [
    OP_EQ,
    OP_GT,
    OP_GTE,
    OP_LT,
    OP_LTE,
    OP_IN,
    OP_BETWEEN,
    OP_LIKE,
    OP_ILIKE,
    OP_NOT_EQ,
    OP_NOT_IN,
    OP_NOT_LIKE,
    OP_NOT_BETWEEN,
]


class Operators(str, Enum):
    eq = "__eq__"
    gt = "__gt__"
    lt = "__lt__"
    gte = "__ge__"
    lte = "__le__"
    in_ = "in_"
    startswith = "startswith"
    endswith = "endswith"
    between = "between"
    like = "like"
    ilike = "ilike"
    contains = "contains"
    icontains = "icontains"
    not_eq = "__ne__"
    not_in = "not_in"
    not_like = "not_like"
