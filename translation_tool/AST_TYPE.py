from enum import Enum


class AST_TYPE(Enum):

    SEQ_VAL = 1,
    INT_VAL = 2,
    BIT_VAL = 3,
    CAST = 4,
    FUNCTION_CALL = 5,
    INDEX_SEL = 6,
    ID = 7,
    CONST = 8,
    SEQ_DECL = 9,
    BIT_DECL = 10,
    INT_DECL = 11,
    EXPR = 12,
    ARITH_OP = 13,
    BITWISE_OP = 14,
    COMP_OP = 15
