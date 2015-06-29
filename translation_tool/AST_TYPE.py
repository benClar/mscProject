from enum import Enum
from pyparsing import ParseException


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
    COMP_OP = 15,
    INDEX_RANGE = 16,
    ID_SET = 17,
    OP = 18,
    SHIFT_OP = 19,
    SEQ_INT_VAL = 20,
    SEQ_BIT_VAL = 21,
    FUNC_DECL = 22,
    RETURN_STMT = 23,
    FOR_LOOP = 24,
    IF_STMT = 25

    def convert(type_input):
        if type_input == "Int":
            return AST_TYPE.INT_VAL
        elif type_input == "Bit":
            return AST_TYPE.BIT_VAL
        else:
            raise ParseException("Unknown Value Type")