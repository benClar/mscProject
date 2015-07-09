from DATA_TYPE import DATA_TYPE
from pyparsing import ParseException


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
        return ret

    def translate_header(self):
        if self.return_value == DATA_TYPE.VOID:
            return "void " + self.translate_name()
        elif self.return_value.node_type == DATA_TYPE.BS_INT_DECL:
            return "uint32_t (*" + self.translate_name() + self.translate_parameters() + ")[" + self.return_value.constraints.translate() + "]"

    def translate_body(self):
        ret = "{ \n"
        for stmt in self.body:
            try:
                ret += "\t" + stmt.translate()
            except TypeError as details:
                print(str(details) + " " + str(stmt.node_type))
            ret += ";\n"
        ret += "}\n \n"
        return ret

    def translate_parameters(self):
        ret = "("
        for p in self.parameters:
            ret += p.translate_as_parameter()
            ret += ", "
        ret = ret[:-3]
        ret += ")"
        return ret

    def translate_name(self):
        return self.ID.translate()


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
            self._constraints = None
        self.node_type = DATA_TYPE.CAST_OP

    @property
    def seq_size(self):
        return self._seq_size

    @property
    def constraints(self):
        return self._constraints

    @property
    def type(self):
        return self._type


# class Index_select(object):

#     def __init__(self, target, indices, base_dim):
#         self._ID = target
#         self._indices = indices
#         self._base_dim = base_dim
#         self.node_type = DATA_TYPE.INDEX_SEL

#     @property
#     def base_dim(self):
#         return self._base_dim

#     @property
#     def ID(self):
#         return self._ID

#     @property
#     def indices(self):
#         return self._indices

#     def is_range(self, indices):
#         for i in indices:
#             try:
#                 if len(i) > 1:
#                     return True
#             except TypeError:
#                 pass
#         return False

    # @property
    # def type(self):
    #     if len(self.indices) < self.base_dim or self.is_range(self.indices):
    #         return self.ID.type
    #     elif len(self.indices) == self.base_dim:
    #         return DATA_TYPE.seq_to_index_sel(self.ID.type)
    #     else:
    #         raise ParseException("Internal error with determing type of selection throw index size")


class Index_select(object):

    def __init__(self, target, indices, output_type=None):
        self.target = target
        self.indices = indices
        self.node_type = DATA_TYPE.SEQ_SELECT
        if output_type is None:
            self._type = self.target.type
        else:
            self._type = output_type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value


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
        return "return " + self.target.translate()


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
        return self.translate_type() + " " + self.ID.translate() + self.translate_size()
        # if self.node_type == DATA_TYPE.SEQ_INT_DECL:
        #     return self.translate_int_seq()
        # elif self.node_type == DATA_TYPE.SEQ_BIT_DECL:
        #     return self.translate_bit_seq()
        # elif self.node_type == DATA_TYPE.BS_SEQ_INT_DECL:
        #     return self.translate_bs_int_seq()
        # else:
        #     raise ParseException("Translation of Unknown Sequence Type attempted")      

    def translate_as_parameter(self):
        if self.node_type == DATA_TYPE.SEQ_INT_DECL:
            return self.translate_int_seq_param()
        elif self.node_type == DATA_TYPE.SEQ_BIT_DECL:
            return self.translate_bit_seq_param()
        elif self.node_type == DATA_TYPE.BS_SEQ_INT_DECL:
            return self.translate_bs_int_seq_param()
        else:
            raise ParseException("Translation of Unknown Sequence Type attempted")

    def translate_int_seq_param(self):
        pass

    def translate_bs_int_seq_param(self):
        pass

    def translate_bit_seq_param(self):
        pass

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
                return False;
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
        if self.value is None:
            return ""
        else:
            return " = " + self.value.translate()

    def translate_as_stmt(self):
        if self.node_type == DATA_TYPE.BS_INT_DECL:
            return "uint32_t " + self.ID.name + "[" + self.constraints.translate() + "]" + self.translate_value()
        elif self.node_type == DATA_TYPE.INT_DECL:
            return "uint32_t " + self.ID.name

    def translate_as_parameter(self):
        if self.node_type == DATA_TYPE.BS_INT_DECL:
            return "uint32_t (*" + self.ID.name + ")[" + self.constraints.translate() + "] "
        elif self.node_type == DATA_TYPE.INT_DECL:
            return "uint32_t " + self.ID.name


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
        ret += ";"
        ret += self.translate_terminator()
        ret += ";"
        ret += self.translate_increment()
        ret += ") \n {"

    def translate_initializer(self):
        pre = ""
        ret = "for("
        for stmt in self.initializer:
            if DATA_TYPE.is_declaration(stmt.node_type):
                pre += stmt.translate() + ";\n"
                print(pre)
            else:
                ret += stmt.translate()

        return pre + ret

    def translate_increment(self):
        pass

    def translate_terminator(self):
        if len(self.increment) > 1:
            raise ParseException("Internal Errror: Several stmts in increment in for loop.")
        return self.terminator[0].translate()


class Binary_operation(object):

    operations_lookup = {DATA_TYPE.COMP_OP: lambda self: self.translate_comparisons()}

    def __init__(self, op_type, operator):
        self._node_type = op_type
        self._operator = operator
        self._left = None
        self._right = None
        self._type = None

    @property
    def node_type(self):
        return self._node_type

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

    def translate_comparisons(self):
        print(self.left.type)
        print(self.right.type)

    def translate(self):
        Binary_operation.operations_lookup[self.node_type](self)



