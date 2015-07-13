from DATA_TYPE import DATA_TYPE
from pyparsing import ParseException
import random

class IR(object):

    def __init__(self):
        self._IR = []

    def add(self, node):
        self.IR.append(node)

    @property
    def IR(self):
        return self._IR

    def translate(self):
        ret = ""
        for node in self.IR:
            ret += node.translate()
        return ret


class Function_decl(object):

    def __init__(self, ID, return_type):
        self._ID = Name(ID, None)
        self._return_value = return_type
        self._parameters = []
        self._body = []
        self._node_type = DATA_TYPE.FUNC_DECL

    @property
    def return_type(self):
        if self._return_value == DATA_TYPE.VOID:
            return DATA_TYPE.VOID
        else:
            return self._return_value.ID.type

    @property
    def return_value(self):
        return self._return_value

    @property
    def parameters(self):
        return self._parameters

    @property
    def body(self):
        return self._body

    @property
    def node_type(self):
        return self._node_type

    @property
    def ID(self):
        return self._ID

    def translate(self):
        ret = ""
        ret += self.translate_header()
        ret += self.translate_body()
        ret += "}\n"
        return ret

    def translate_header(self):
        if self.return_value == DATA_TYPE.VOID:
            return "void " + self.translate_name()
        else:
            return self.return_value.translate_type() + " " + self.translate_name() + self.translate_parameters() + self.translate_dimensions()

    def translate_dimensions(self):
        ret = ""
        return_type = self.return_value.ID.type
        if DATA_TYPE.is_seq_type(return_type):
            for i, dim in enumerate(self.return_value.size):
                if i == 0:
                    ret += ")"
                else:
                    ret += "[" + dim.translate() + "]"
        if return_type == DATA_TYPE.BS_SEQ_INT_VAL or return_type == DATA_TYPE.BS_INT_VAL:
            ret += "[" + self.return_value.constraints.translate() + "]"
        return ret

    def translate_body(self):
        ret = "{ \n"
        for stmt in self.body:
            ret += stmt.translate()
        return ret

    def translate_parameters(self):
        ret = "("
        for p in self.parameters:
            ret += p.translate_as_parameter()
            ret += ", "
        ret = ret[:-2]
        ret += ")"
        return ret

    def translate_name(self):
        return_type = self.return_value.ID.type
        if DATA_TYPE.is_seq_type(return_type) or return_type == DATA_TYPE.BS_INT_VAL:
            return "(" + "*" + self.ID.translate()
        elif return_type == DATA_TYPE.INT_VAL or return_type == DATA_TYPE.BIT_VAL:
            return self.ID.translate()
        else:
            raise ParseException("Internal error: Unknown return type")


class If_stmt(object):

    def __init__(self, condition, body=None):
        self._condition = condition
        self._body = []
        self.node_type = DATA_TYPE.IF_STMT

    @property
    def condition(self):
        return self._condition

    @property
    def body(self):
        return self._body

    def add_stmt(self, stmt):
        self._body.append(stmt)

    def translate(self):
        ret = ""
        ret += "if(" + self.condition.translate() + ") { \n"
        ret += self.translate_body()
        ret += "} \n"
        return ret

    def translate_body(self):
        ret = ""
        for stmt in self.body:
            ret += stmt.translate()
        return ret


class Element_range(object):

    node_type = DATA_TYPE.INDEX_RANGE

    def __init__(self, start, finish):
        self._start = start
        self._finish = finish
        self.type = None

    @property
    def start(self):
        return self._start

    @property
    def finish(self):
        return self._finish


class Cast(object):

    def __init__(self, c_op, c_target):
        self._cast_target = c_target
        self._cast_op = c_op
        self.node_type = DATA_TYPE.CAST

    def translate(self):
        return self.operation.translate(self.target)

    @property
    def type(self):
        return self._cast_op.type

    @property
    def target(self):
        return self._cast_target

    @property
    def operation(self):
        return self._cast_op


class Cast_operation(object):

    def __init__(self, c_type, constraints, size):
        self._type = c_type
        if len(constraints) > 0:
            self._constraints = constraints
        else:
            self._constraints = None
        if len(size) > 0:
            self._seq_size = size
        else:
            self._seq_size = None
        self.node_type = DATA_TYPE.CAST_OP

    def translate(self, target):
        if self.type == DATA_TYPE.SEQ_BIT_VAL:
            return self.translate_bit_seq_cast(target)
        elif self.type == DATA_TYPE.INT_VAL:
            raise ParseException("INT VAL Cast not yet been done " + str(self.type))

    def translate_bit_seq_cast(self, target):
        if target.type == DATA_TYPE.INT_VAL:
            return "int_to_bit_seq(" + target.translate() + ", " + self.size[0].translate() + ")"
        elif target.type == DATA_TYPE.BS_INT_VAL:
            return target.translate()
        else:
            raise ParseException("Unknown cast target type for bit seq cast " + str(target.type))

    @property
    def seq_size(self):
        return self._seq_size

    @property
    def constraints(self):
        return self._constraints

    @property
    def type(self):
        return self._type


class Index_select(object):

    def __init__(self, target, indices, output_type=None):
        self.target = target
        self.indices = indices
        self.node_type = DATA_TYPE.INDEX_SELECT
        if output_type is None:
            self._type = self.target.type
        else:
            self._type = output_type

    def translate(self):
        if self.target.type == DATA_TYPE.INT_VAL and self.type == DATA_TYPE.BIT_VAL:
            return self.translate_int_bit_select()
        elif self.target.type == DATA_TYPE.SEQ_BIT_VAL and self.type == DATA_TYPE.BIT_VAL:
            return self.select_bit_from_bit_seq()
        if self.target.type == DATA_TYPE.INT_VAL and self.type == DATA_TYPE.SEQ_BIT_VAL:
            if self.is_range():
                return self.extract_bit_range()
        elif self.target.type == DATA_TYPE.BS_INT_VAL and self.type == DATA_TYPE.BIT_VAL:
            return self.translate_BS_int_bit_select()
        elif DATA_TYPE.is_seq_type(self.type):
            if self.is_range():
                return self.extract_range()
            if DATA_TYPE.is_op_type(self.target.node_type):
                return "(" + self.target.translate() + ")"
            return self.target.translate()

    def select_bit_from_bit_seq(self):
        assert len(self.indices[-1]) == 1, "assuming single int val for bit selection"
        return self.target.translate() + self.translate_selection_dim() + "[" + self.indices[-1][0].translate() + "]"

    def extract_bit_range(self):
        """Returns Bit-sliced value from int val range operation"""
        return "extract_bit_range(" + self.target.translate() + ", " + self.indices[-1][0].start.translate() + ", " + self.indices[-1][0].finish.translate() + ")"

    def extract_range(self):
        """Returns range of bits from a sequence (Seq bit, seq int, bs int)"""
        return "extract_range(" + self.target.translate() + ", " + self.translate_selection_dim() + self.indices[-1][0].start.translate() + ", " + self.indices[-1][0].finish.translate() + ")"

    def translate_BS_int_bit_select(self):
        assert len(self.indices) == 1
        assert len(self.indices[0]) == 1
        assert self.indices[0][0].type == DATA_TYPE.INT_VAL
        ret = ""
        ret += self.target.translate() + "[" + self.indices[0][0].translate() + "]"
        return ret

    def translate_int_bit_select(self):
        assert len(self.indices) == 1
        assert len(self.indices[0]) == 1
        assert self.indices[0][0].type == DATA_TYPE.INT_VAL
        ret = ""
        ret += "(" + "(" + self.target.translate() + " >> " + self.indices[0][0].translate() + ")" + " & 0x1" + ")"
        return ret

    def value_is_list(self):
        for dim in self.indices:
            for selection in dim:
                if selection.node_type == DATA_TYPE.INDEX_RANGE:
                    return False
        return True

    def translate_indices(self):
        assert len(self.indices) == 1
        assert len(self.indices[0]) == 1
        return self.indices[0][0].translate()

    def is_range(self):
        if self.indices[-1][0].node_type == DATA_TYPE.INDEX_RANGE:
            assert len(self.indices[-1]) == 1, "Only single range contained in selection"
            return True
        else:
            return False

    def extract_as_sequence(self):
        ret = ""
        rndm_name = self.random_name()
        values = self.translate_list_values(self.indices[-1])
        for dim in self.indices:
            if self.target.type == DATA_TYPE.INT_VAL:
                ret += Int_decl.type_decl_lookup[self.target.constraints.translate()] + " " + rndm_name + "[" + str(len(self.indices[0])) + "]" + "= {" + values + "}"
            elif self.target.type == DATA_TYPE.SEQ_INT_VAL:
                raise ParseException("Lists for Integer sequences not yet implemented")
            elif self.target.type == DATA_TYPE.BS_INT_VAL:
                ret += "uint32_t" + " " + rndm_name + "[" + str(len(self.indices[0])) + "]" + "= {" + values + "}"
            elif self.target.type == DATA_TYPE.BS_SEQ_INT_VAL:
                raise ParseException("Lists for BS INT sequences not yet implemented")
            elif self.target.type == DATA_TYPE.SEQ_BIT_VAL:
                ret += "bool" + " " + rndm_name + "[" + str(len(self.indices[0])) + "]" + "= {" + values + "}"
        return {"temp_seq": ret + "; \n", "name": rndm_name}

    def translate_list_values(self, dim):
        values = ""
        if self.target.type == DATA_TYPE.INT_VAL:
            for selection in dim:
                values += "(" + self.target.translate() + " >> " + selection.translate() + ") & 0x1, "
            values = values[:-2]
        elif self.target.type == DATA_TYPE.BS_INT_VAL:
            for selection in dim:
                values += self.target.translate() + self.translate_selection_dim() + "[" + selection.translate() + "]" + ", "
            values = values[:-2]
        return values

    def random_name(self):
        return random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') + ''.join(random.choice('0123456789ABCDEF') for i in range(15))

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    def translate_selection_dim(self):
        ret =""
        for i, dim in enumerate(self.indices):
            if i == len(self.indices) - 1:
                return ret
            ret += "[" + dim[0].translate() + "]"
        return ret


class Set(object):

    def __init__(self, target, value):
        self._target = target
        # self._ID = Name(var_id, id_type)
        self._value = value
        self.node_type = DATA_TYPE.ID_SET

    @property
    def target(self):
        return self._target

    @property
    def value(self):
        return self._value

    def translate(self, end=True):
        ret = ""
        if self.target.node_type == DATA_TYPE.INDEX_SELECT:
            if self.target.target.type == DATA_TYPE.BS_INT_VAL and self.value.type == DATA_TYPE.BIT_VAL:
                #Setting single bit on BS int
                self.value.translate()
                ret = self.target.translate() + " = " + self.value.translate()
            elif self.target.target.type == DATA_TYPE.INT_VAL and self.target.type == DATA_TYPE.BIT_VAL:
                # setting single bit on Int
                ret += self.target.target.translate() + " &= " + "(" + self.value.translate() + " << " + self.target.translate_indices() + ")"
            elif DATA_TYPE.is_seq_type(self.target.type):
                ret += self.translate_set_sequence()
            else:
                print("SETTING BIT/ ELEMENT")
        elif self.target.type == DATA_TYPE.INT_VAL and self.value.type == DATA_TYPE.BS_INT_VAL:
            return self.value.translate()
        elif self.target.type == self.value.type:
            ret += self.target.translate() + " = " + self.value.translate()
        else:
            raise ParseException("Unknown assignment of" + str(self.value.type) + " to " + str(self.target.type))
        if end: 
            ret += ";\n"
        return ret

    def translate_set_sequence(self):
        ret = ""
        for i, selection in enumerate(self.target.indices[-1]):
            if selection.node_type == DATA_TYPE.INDEX_RANGE:
                #  Assignment to a range select
                ret += self.translate_range_select_assignment(selection, i)
                    # ret += "range_assignment(" + self.target.translate() + self.target.translate_selection_dim() + ","\
                    #     + self.value.translate() + self.value.translate_selection_dim() + ", " + selection.start.translate() + ", " + selection.finish.translate() + ", " + "); \n"
            else:
                ret += self.target.translate() + self.target.translate_selection_dim() + "[" + selection.translate() + "]" + "=" +\
                    self.value.translate() + self.value.translate_selection_dim() + "[" + str(i) + "]" + "; \n"
        return ret

    def translate_range_select_assignment(self, selection, i):
        """Carries out different translation depending on whether sequence value to be assigned is indexed using a list or a range """
        ret = ""
        if DATA_TYPE.is_op_type(self.value.node_type):
            ret += "sequence_assignment(" + self.target.target.name + self.target.translate_selection_dim() + ","\
                + self.value.translate() + ", " +\
                selection.start.translate() + ", " + selection.finish.translate() +\
                ", 0, " + selection.finish.translate() + "-" + selection.start.translate() + ")"
        elif self.value.is_range():
            ret += "sequence_assignment(" + self.target.target.name + self.target.translate_selection_dim() + ","\
                + self.value.translate() + self.value.translate_selection_dim() + ", " + selection.start.translate() + ", " +\
                selection.finish.translate() + ", " + self.value.indices[-1][0].start.translate() + ", " +\
                self.value.indices[-1][0].finish.translate() + ")"
        elif self.value.value_is_list():
            extraction = self.value.extract_as_sequence()
            ret += extraction["temp_seq"]
            ret += "sequence_assignment(" + self.target.target.name + self.target.translate_selection_dim() + self.target.translate_selection_dim() + ","\
                + extraction['name'] + ", " + selection.start.translate() + ", " +\
                selection.finish.translate() + ", " + selection.start.translate() + ", " +\
                selection.finish.translate() + ")"
        else:
            raise ParseException("Tried to set type of feature not yet implemented....")
        return ret

    # def translate_dimension(self, select_string, current_index, current_index_enumeration):
    #     """Return string with all specific element assignments"""
    #     full_index = ""
    #     ret = ""
    #     for array_select in current_index:
    #         if array_select.node_type == DATA_TYPE.INDEX_RANGE:
    #             pass
    #         else:
    #             ret += "[" + array_select.translate() + "]"
    #         if current_index_enumeration == (len(self.target.indices) - 1):
    #             for element_select in current_index:
    #                 if element_select.node_type == DATA_TYPE.INDEX_RANGE:
    #                     full_index += "range_assignment(" + select_string + "," + self.value.translate() + ", " +\
    #                         element_select.start.translate() + ", " + element_select.finish.translate()

    #         if (len(self.target.indices) - 1) - current_index_enumeration > 0:
    #             self.translate_dimension(select_string, self.indices[current_index_enumeration + 1], current_index_enumeration + 1)


class Return(object):
    def __init__(self, expr):
        self._target = expr
        self._type = expr.type
        self.node_type = DATA_TYPE.RETURN_STMT

    @property
    def target(self):
        return self._target

    @property
    def type(self):
        return self._type

    def translate(self):
        return "return " + self.target.translate() + ";\n"


class Seq_decl(object):

    def __init__(self, node_type, size, var_id, value=None, constraints=None):
        self._ID = Name(var_id, DATA_TYPE.decl_to_value(node_type))
        self._node_type = node_type
        self._size = size
        self._value = value
        self._constraints = constraints

    @property
    def ID(self):
        return self._ID

    @property
    def node_type(self):
        return self._node_type

    @property
    def size(self):
        return self._size

    @property
    def value(self):
        return self._value

    @property
    def constraints(self):
        return self._constraints

    def translate(self):
        return self.translate_type() + " " + self.ID.translate() + self.translate_size() + "; \n"
        # if self.node_type == DATA_TYPE.SEQ_INT_DECL:
        #     return self.translate_int_seq()
        # elif self.node_type == DATA_TYPE.SEQ_BIT_DECL:
        #     return self.translate_bit_seq()
        # elif self.node_type == DATA_TYPE.BS_SEQ_INT_DECL:
        #     return self.translate_bs_int_seq()
        # else:
        #     raise ParseException("Translation of Unknown Sequence Type attempted")

    def translate_as_parameter(self):
        ret = self.translate_type() + " " + self.ID.translate()
        for dim in self.size:
            ret += "[" + dim.translate() + "]"
        if self.ID.type == DATA_TYPE.BS_SEQ_INT_VAL or self.ID.type == DATA_TYPE.BS_INT_VAL:
            ret += "[" + self.constraints.translate() + "]"
        return ret
        # if self.node_type == DATA_TYPE.SEQ_INT_DECL:
        #     return self.translate_int_seq_param()
        # elif self.node_type == DATA_TYPE.SEQ_BIT_DECL:
        #     return self.translate_bit_seq_param()
        # elif self.node_type == DATA_TYPE.BS_SEQ_INT_DECL:
        #     return self.translate_bs_int_seq_param()
        # else:
        #     raise ParseException("Translation of Unknown Sequence Type attempted")

    def translate_int_seq(self):
        if self.size_is_literal():
            return self.translate_type() + " " + self.ID.translate() + self.translate_size()
        else:
            self.translate_variable_size()

    def translate_size(self):
        if self.size_is_literal():
            ret = self.translate_constant_size()
        else:
            ret = self.translate_variable_size()
        return ret

    def translate_variable_size():
        raise ParseException("Variable size Arrays not yet supported")

    def translate_constant_size(self):
        ret = ""
        for expr in self.size:
            ret += "[" + expr.translate() + "]"
        if self.node_type == DATA_TYPE.BS_SEQ_INT_DECL:
            ret += "[" + self.constraints.translate() + "]"
        return ret

    def size_is_literal(self):
        for expr in self.size:
            if expr.node_type == DATA_TYPE.INT_LITERAL:
                pass
            else:
                return False
        return True

    def translate_type(self):
        if self.node_type == DATA_TYPE.SEQ_INT_DECL or DATA_TYPE.BS_SEQ_INT_DECL:
            return "uint32_t"
        elif self.node_type == DATA_TYPE.SEQ_BIT_DECL:
            return "bool"
        else:
            raise ParseException("Translation of Unknown sequence type attempted")

    def translate_bs_int_seq(self):
        if self.size_is_literal():
            return self.translate_type() + " " + self.ID.translate() + self.translate_size()
        else:
            self.translate_variable_size()

    def translate_bit_seq(self):
        pass


class Seq_val(object):

    def __init__(self, s_type=None, value=None):
        self._value = []
        if value is not None:
            self._value.append(value)

        self._type = s_type
        self.node_type = DATA_TYPE.SEQ_VAL

    @property
    def value(self):
        return self._value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    def add_element(self, element):
        self._value.append(element)


class Bit_decl(object):

    def __init__(self, var_id, value=None):
        self._ID = Name(var_id, DATA_TYPE.BIT_VAL)
        self._node_type = DATA_TYPE.BIT_DECL
        self._value = value

    @property
    def node_type(self):
        return self._node_type

    @property
    def value(self):
        return self._value

    @property
    def ID(self):
        return self._ID

    def translate(self):
        return "bool " + self.ID.translate() + self.translate_value()

    def translate_value(self):
        if self.value is None:
            return ""
        else:
            return " = " + self.value.translate()

    def translate_as_parameter(self):
        return "bool " + self.ID.translate()


class Int_decl(object):

    type_decl_lookup = {"8": "uint8_t ",
                        "16": "uint16_t ",
                        "32": "uint32_t ",
                        "64": "uint64_t "}

    def __init__(self, n_type, constraints, var_id, value=None):
        self._constraints = constraints
        self._ID = var_id
        self._value = value
        self._node_type = n_type

    @property
    def node_type(self):
        return self._node_type

    @property
    def constraints(self):
        return self._constraints

    @property
    def ID(self):
        return self._ID

    @property
    def value(self):
        return self._value

    def translate(self):
        return self.translate_as_stmt()

    def translate_value(self):
        ret = ""
        if self.value is None:
            return ""
        else:
            if self.node_type == DATA_TYPE.BS_INT_DECL:
                if self.value.type == DATA_TYPE.INT_VAL:
                    return " = bitslice(" + self.value.translate() + "," + self.constraints.value + ")"
                elif self.value.type == DATA_TYPE.BS_INT_VAL:
                    for bit in range(int(self.constraints.translate())):
                        ret += self.ID.translate() + "[" + str(bit) + "] = " + self.translate_value_to_bs(bit) + ";\n"
                    return ret
            else:
                return " = " + self.value.translate()

    def translate_value_to_bs(self, bit):
        assert DATA_TYPE.is_int_val(self.value.type), "Value to translate to bs is integer value in Int DECL"
        if self.value.type == DATA_TYPE.INT_VAL:
            return "(" + self.value.translate() + ")" + ">>" + str(bit) + "& 0x1"
        elif self.value.type == DATA_TYPE.BS_INT_VAL:
            return self.value.translate() + "[" + str(bit) + "]"

    def translate_as_stmt(self):
        ret = ""
        if self.node_type == DATA_TYPE.BS_INT_DECL:
            ret = self.translate_type() + self.ID.translate() + "[" + self.constraints.translate() + "]" + self.translate_value() + ";\n"
        elif self.node_type == DATA_TYPE.INT_DECL:
            ret = self.translate_type() + self.ID.translate() + self.translate_value() + ";\n"
        return ret

    def translate_type(self):
        if self.constraints.translate() in Int_decl.type_decl_lookup:
            if self.node_type == DATA_TYPE.INT_DECL:
                return Int_decl.type_decl_lookup[self.constraints.value]
            elif self.node_type == DATA_TYPE.BS_INT_DECL:
                return "uint32_t "
        else:
            raise ParseException("Custom Size: Not yet implemented")

    def translate_as_parameter(self):
        # print(self.constraints)
        if self.node_type == DATA_TYPE.BS_INT_DECL:
            return self.translate_type() + self.ID.name + "[" + self.constraints.translate() + "]"
        elif self.node_type == DATA_TYPE.INT_DECL:
            return self.translate_type() + self.ID.name


class Int_literal(object):

    def __init__(self, value):
        self.value = value
        self.type = DATA_TYPE.INT_VAL
        self.node_type = DATA_TYPE.INT_LITERAL

    def translate(self):
        return self.value


class Bit_literal(object):

    def __init__(self, value):
        self.value = value
        self.type = DATA_TYPE.BIT_VAL
        self.node_type = DATA_TYPE.BIT_LITERAL

    def translate(self):
        return self.value


class Name(object):

    def __init__(self, name, id_type):
        self._name = name
        self._type = id_type
        self.node_type = DATA_TYPE.ID
        self._constraints = None
        self._size = None

    @property
    def size(self):
        return self._size

    @property
    def constraints(self):
        return self._constraints

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @constraints.setter
    def constraints(self, value):
        self._constraints = value

    @size.setter
    def size(self, value):
        self.size = value

    def translate(self):
        return self.name


class Call(object):

    def __init__(self, f_id, return_type):
        self._f_id = Name(f_id, return_type)
        self._parameters = []

    def add_parameter(self, p):
        self.parameters.append(p)

    @property
    def parameters(self):
        return self._parameters

    @property
    def type(self):
        return self.f_id.type

    @property
    def f_id(self):
        return self._f_id


class For_loop(object):

    def __init__(self):
        self._initializer = []
        self._terminator = []
        self._increment = []
        self._body = []
        self._node_type = DATA_TYPE.FOR_LOOP

    @property
    def node_type(self):
        return self._node_type

    @property
    def initializer(self):
        return self._initializer

    @property
    def terminator(self):
        return self._terminator

    @property
    def increment(self):
        return self._increment

    @property
    def body(self):
        return self._body

    def translate(self):
        ret = ""
        ret += self.translate_initializer()
        ret += "; "
        ret += self.translate_terminator()
        ret += "; "
        ret += self.translate_increment()
        ret += ") { \n"
        ret += self.translate_body()
        ret += "} \n"
        return ret

    def translate_initializer(self):
        pre = ""
        ret = "for("
        for stmt in self.initializer:
            if DATA_TYPE.is_declaration(stmt.node_type):
                pre += stmt.translate() + "\n"
            else:
                ret += stmt.translate() + ", "
        if ret[-2] == ',':
            ret = ret[:-2]
        return pre + ret

    def translate_body(self):
        ret = ""
        for stmt in self.body:
            ret += stmt.translate()
        ret += '\n'
        return ret

    def translate_increment(self):
        ret = ""
        for expr in self.increment:
            ret += expr.translate(False) + ", "
        ret = ret[:-2]
        return ret

    def translate_terminator(self):
        if len(self.increment) > 1:
            raise ParseException("Internal Errror: Several stmts in increment in for loop.")
        return self.terminator[0].translate()


class Binary_operation(object):

    operations_lookup = {DATA_TYPE.COMP_OP: lambda self: self.translate_comparisons(),
                         DATA_TYPE.ARITH_OP: lambda self: self.translate_arithmetic(),
                         DATA_TYPE.BITWISE_OP: lambda self: self.translate_bitwise(),
                         DATA_TYPE.SHIFT_OP: lambda self: self.translate_shift()}

    def __init__(self, op_type, operator):
        self._node_type = op_type
        self._operator = operator
        self._left = None
        self._right = None
        self._type = None
        # self._constraints = None

    @property
    def node_type(self):
        return self._node_type

    # @constraints.setter
    # def constraints(self, value):
    #     self._constraints = value

    # @property
    # def constraints(self):
    #     return self._constraints

    @property
    def operator(self):
        return self._operator

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def right(self):
        return self._right

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self._left = value

    @right.setter
    def right(self, value):
        self._right = value

    @type.setter
    def type(self, value):
        self._type = value

    def translate_shift(self):
        assert self.right.type == DATA_TYPE.INT_VAL, "Shift input should always be integer value"
        if self.left.type == DATA_TYPE.INT_VAL:
            ret = self.translate_int_shift()
        elif self.left.type == DATA_TYPE.BS_INT_VAL:
            ret = self.translate_bs_shift()
        return ret

    # def determine_result_size(self):
    #     if self.right.constraints is not None and self.left.constraints is not None:
    #         if int(self.right.constraints) >= int(self.left.constraints):
    #             self.constraints = self.right.constraints
    #             return self.right.constraints
    #         else:
    #             self.constraints = self.left.constraints
    #             return self.left.constraints
    #     raise ParseException("Target Has no constraints")

    def translate_bs_shift(self):
        ret = ""
        ret += "shift(" + self.left.translate() + ", " + self.left.constraints.translate() + ", " + self.right.translate() + ", " + "\"" + self.operator + "\"" + ")"
        return ret

    def translate_int_shift(self):
        ret = ""
        ret += self.left.translate() + " " + self.operator + " " + self.left.translate()
        return ret

    def translate_bitwise(self):
        if self.right.type == DATA_TYPE.BIT_VAL and self.left.type == DATA_TYPE.BIT_VAL:
            return self.translate_bit_val_bitwise()
        elif self.right.type == DATA_TYPE.SEQ_BIT_VAL and self.left.type == DATA_TYPE.SEQ_BIT_VAL:
            return self.translate_bit_seq_bitwise()
        elif DATA_TYPE.is_int_val(self.left.type) and DATA_TYPE.is_int_val(self.right.type):
            return self.translate_int_val_bitwise()

    def translate_int_val_bitwise(self):
        ret = ""
        if self.left.type == DATA_TYPE.BS_INT_VAL and self.right.type != DATA_TYPE.BS_INT_VAL:
            ret += "bitwise_bs(" + self.left.translate() + ", " + "bitslice(" + self.right.translate() + ", " + self.right.constraints.translate() +\
                "), \"" + self.operator + "\")"
        elif self.left.type != DATA_TYPE.BS_INT_VAL and self.right.type == DATA_TYPE.BS_INT_VAL:
            ret += "bitwise_bs(" + "bitslice(" + self.left.translate() + "," + self.left.constraints + "), " + self.right.translate() + ", \"" + self.operator + "\" )"
        elif self.left.type != DATA_TYPE.BS_INT_VAL and self.right.type != DATA_TYPE.BS_INT_VAL:
            ret += self.left.translate() + " \"" + self.operator + "\" " + self.right.translate()
        else:
            ret += "bitwise_bs(" + self.left.translate() + ", " + self.right.translate() + ", \"" + self.operator + "\")"
        return ret

    def translate_bit_seq_bitwise(self):
        return "seq_bitwise(" + self.left.translate() + ", " + self.right.translate() + ", " + "\"" + self.operator + "\"" + ")"

    def translate_arithmetic(self):
        if DATA_TYPE.is_int_val(self.right.type) and DATA_TYPE.is_int_val(self.left.type):
            return self.translate_int_val_arithmetic()

    def translate_comparisons(self):
        if DATA_TYPE.is_int_val(self.right.type) and DATA_TYPE.is_int_val(self.left.type):
            return self.translate_int_val_compare()
        if self.left.type == DATA_TYPE.BIT_VAL and self.right.type == DATA_TYPE.BIT_VAL:
            return self.translate_bit_compare()

    def translate_bit_compare(self):
        return self.left.translate() + " " + self.operator + " " + self.right.translate()

    def translate_bit_val_bitwise(self):
        ret = self.left.translate() + " " + self.operator + " " + self.right.translate()
        ret = "(" + ret + ")"
        return ret

    def translate_int_val_arithmetic(self):
        if self.right.type == DATA_TYPE.BS_INT_VAL and self.left.type != DATA_TYPE.BS_INT_VAL:
            ret = "arith_bs(bitslice(" + self.left.translate() + "," + self.left.constraints.translate() + ")," + self.right.translate() + "," + self.operator + ")"
        elif self.left.type == DATA_TYPE.BS_INT_VAL and self.right.type != DATA_TYPE.BS_INT_VAL:
            ret = "arith_bs(" + self.left.translate() + "," + "bitslice(" + self.right.translate() + "," + self.right.constraints.translate() + ")" + "," + self.operator + ")"
        elif self.left.type == DATA_TYPE.BS_INT_VAL and self.right.type == DATA_TYPE.BS_INT_VAL:
            ret = "arith_bs(" + self.left.translate() + "," + self.right.constraints() + "," + self.operator + ")"
        else:
            ret = self.left.translate() + " " + self.operator + " " + self.right.translate()
        return ret

    def translate_int_val_compare(self):
        if self.right.type == DATA_TYPE.BS_INT_VAL and self.left.type != DATA_TYPE.BS_INT_VAL:
            ret = "compare_bs(bitslice(" + self.left.translate() + "," + self.left.constraints.translate() + ")," + self.right.translate() + "," + self.operator + ")"
        elif self.left.type == DATA_TYPE.BS_INT_VAL and self.right.type != DATA_TYPE.BS_INT_VAL:
            ret = "compare_bs(" + self.left.translate() + "," + "bitslice(" + self.right.translate() + "," + self.right.constraints.translate() + ")" + "," + self.operator + ")"
        else:
            ret = self.left.translate() + " " + self.operator + " " + self.right.translate()
        return ret

    def translate(self):
        return Binary_operation.operations_lookup[self.node_type](self)


