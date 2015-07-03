from enum import Enum
from pyparsing import ParseException
from AST_TYPE import AST_TYPE


class IR_TYPE(Enum):
    INT_LITERAL = 0
    ARITH_OP = 1,
    BITWISE_OP = 2,
    COMP_OP = 3,
    SHIFT_OP = 4,
    BIT_LITERAL = 5

    def AST_to_IR(ast_in):
        if ast_in == AST_TYPE.ARITH_OP:
            return IR_TYPE.ARITH_OP
        if ast_in == AST_TYPE.BITWISE_OP:
            return IR_TYPE.BITWISE_OP
        if ast_in == AST_TYPE.BITWISE_OP:
            return IR_TYPE.BITWISE_OP
        if ast_in == AST_TYPE.SHIFT_OP:
            return IR_TYPE.SHIFT_OP
        else:
            raise ParseException("Tried to convert unknown AST TYPE" + str(ast_in))
