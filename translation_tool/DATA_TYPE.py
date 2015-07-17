from enum import Enum
from pyparsing import ParseException
import traceback
import sys

class DATA_TYPE(Enum):

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
    IF_STMT = 25,
    BS_INT_VAL = 26,
    BS_SEQ_INT_VAL = 27,
    VOID = 28,
    FUNCTION_PARAM = 29,
    BS_INT_DECL = 30,
    BS_SEQ_INT_DECL = 31,
    SEQ_INT_DECL = 32,
    SEQ_BIT_DECL = 33,
    INDEX_SET = 34,
    INT_LITERAL = 35,
    BIT_LITERAL = 36,
    SEQ_SELECT = 37,
    LOG_OP = 38,
    CAST_OP = 39,
    SBOX_DECL = 40,
    INDEX_SELECT = 41,
    BS_BIT_VAL = 42,
    SEQ_BS_BIT_VAL = 43

    def is_int_val(type_input):
        sequence_types = [DATA_TYPE.INT_VAL, DATA_TYPE.BS_INT_VAL]
        if type_input in sequence_types:
            return True
        return False

    def is_seq_type(type_input):
        sequence_types = [DATA_TYPE.SEQ_INT_VAL, DATA_TYPE.SEQ_BIT_VAL, DATA_TYPE.BS_SEQ_INT_VAL, DATA_TYPE.SBOX_DECL, DATA_TYPE.SEQ_BS_BIT_VAL]
        if type_input in sequence_types:
            return True
        return False

    def is_var(type_input):
        vars_ = [DATA_TYPE.INT_LITERAL, DATA_TYPE.ID, DATA_TYPE.INDEX_SELECT]
        if type_input in vars_:
            return True
        return False

    def is_op_type(type_input):
        op_types = [DATA_TYPE.ARITH_OP, DATA_TYPE.BITWISE_OP, DATA_TYPE.SHIFT_OP, DATA_TYPE.COMP_OP, DATA_TYPE.LOG_OP]
        if type_input in op_types:
            return True
        return False

    def val_to_decl(type_input):
        if type_input == DATA_TYPE.BS_INT_VAL:
            return DATA_TYPE.BS_INT_DECL
        elif type_input == DATA_TYPE.INT_VAL:
            return DATA_TYPE.INT_DECL
        elif type_input == DATA_TYPE.BIT_VAL:
            return DATA_TYPE.BIT_DECL
        elif type_input == DATA_TYPE.SEQ_INT_VAL:
            return DATA_TYPE.SEQ_INT_DECL
        elif type_input == DATA_TYPE.BS_SEQ_INT_VAL:
            return DATA_TYPE.BS_SEQ_INT_DECL
        elif type_input == DATA_TYPE.SEQ_BIT_VAL:
            return DATA_TYPE.SEQ_BIT_DECL
        else:
            traceback.print_stack(file=sys.stdout)
            raise ParseException("Unknown Value Type")  

    def convert(type_input, qualifier=None):
        if type_input == "Int":
            if qualifier == "Seq":
                return DATA_TYPE.SEQ_INT_VAL
            return DATA_TYPE.INT_VAL
        elif type_input == "Bit":
            if qualifier == "Seq":
                return DATA_TYPE.SEQ_BIT_VAL
            return DATA_TYPE.BIT_VAL
        elif type_input == "@Int":
            if qualifier == "Seq":
                return DATA_TYPE.BS_SEQ_INT_VAL
            return DATA_TYPE.BS_INT_VAL
        elif type_input == "void":
            return DATA_TYPE.VOID
        elif type_input == DATA_TYPE.INT_DECL:
            return DATA_TYPE.INT_VAL
        else:
            traceback.print_stack(file=sys.stdout)
            raise ParseException("Unknown Value Type")

    def seq_to_index_sel(type_input):
        if type_input == DATA_TYPE.SEQ_INT_VAL:
            return DATA_TYPE.INT_VAL
        elif type_input == DATA_TYPE.SEQ_BIT_VAL:
            return DATA_TYPE.BIT_VAL
        elif type_input == DATA_TYPE.BS_SEQ_INT_VAL:
            return DATA_TYPE.BS_INT_VAL
        elif type_input == DATA_TYPE.INT_VAL or type_input == DATA_TYPE.BS_INT_VAL:
            return DATA_TYPE.BIT_VAL
        elif type_input == DATA_TYPE.SBOX_DECL:
            return DATA_TYPE.SEQ_BS_BIT_VAL
        elif type_input == DATA_TYPE.SEQ_BS_BIT_VAL:
            return DATA_TYPE.BS_BIT_VAL
        else:
            raise ParseException("Internal Errror: Tried to convert unknown type to sequence selection type " + str(type_input))


    def is_declaration(type_input):
        declarations = [DATA_TYPE.INT_DECL, DATA_TYPE.BIT_DECL, DATA_TYPE.SEQ_BIT_DECL,
                        DATA_TYPE.BS_SEQ_INT_DECL, DATA_TYPE.BS_INT_DECL, DATA_TYPE.SEQ_INT_DECL]
        if type_input in declarations:
            return True
        return False

    def needs_cast(target, value):
        directly_assignable = {DATA_TYPE.INT_VAL: [DATA_TYPE.BS_BIT_VAL, DATA_TYPE.INT_VAL],
                               DATA_TYPE.BS_BIT_VAL: [DATA_TYPE.BS_BIT_VAL, DATA_TYPE.INT_VAL],
                               DATA_TYPE.BS_INT_VAL: [DATA_TYPE.BS_INT_VAL]}
        if value not in directly_assignable[target]:
            return True
        return False

    def decl_to_value(type_input):
        if type_input == DATA_TYPE.BS_INT_DECL:
            return DATA_TYPE.BS_INT_VAL
        elif type_input == DATA_TYPE.INT_DECL:
            return DATA_TYPE.INT_VAL
        elif type_input == DATA_TYPE.BIT_DECL:
            return DATA_TYPE.BIT_VAL
        elif type_input == DATA_TYPE.SEQ_INT_DECL:
            return DATA_TYPE.SEQ_INT_VAL
        elif type_input == DATA_TYPE.BS_SEQ_INT_DECL:
            return DATA_TYPE.BS_SEQ_INT_VAL
        elif type_input == DATA_TYPE.SEQ_BIT_DECL:
            return DATA_TYPE.SEQ_BIT_VAL
        elif type_input == DATA_TYPE.SBOX_DECL:
            return DATA_TYPE.SEQ_BS_BIT_VAL
        else:
            traceback.print_stack(file=sys.stdout)
            raise ParseException("Unknown Value Type")