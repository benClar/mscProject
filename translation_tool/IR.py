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


class Function_decl(object):

    def __init__(self, return_type):
        self._return_value = return_type
        self._parameters = []
        self._body = []
        self._node_type = DATA_TYPE.FUNC_DECL

    @property
    def return_type(self):
        return self._return_type

    @property
    def parameters(self):
        return self._parameters

    @property
    def body(self):
        return self._body

    @property
    def node_type(self):
        return self._node_type


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

class Seq_range(object):

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
        self.node_type = DATA_TYPE.CAST

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

    def __init__(self, target, indices, base_dim):
        self._ID = target
        self._indices = indices
        self._base_dim = base_dim
        self.node_type = DATA_TYPE.INDEX_SEL

    @property
    def base_dim(self):
        return self._base_dim

    @property
    def ID(self):
        return self._ID

    @property
    def indices(self):
        return self._indices

    def is_range(self, indices):
        for i in indices:
            try:
                if len(i) > 1:
                    return True
            except TypeError:
                pass
        return False

    @property
    def type(self):
        if len(self.indices) < self.base_dim or self.is_range(self.indices):
            return self.ID.type
        elif len(self.indices) == self.base_dim:
            return DATA_TYPE.seq_to_index_sel(self.ID.type)
        else:
            raise ParseException("Internal error with determing type of selection throw index size")


class Seq_select(object):

    def __init__(self, target, indices):
        self.target = target
        self.indices = indices
        self.node_type = DATA_TYPE.SEQ_SELECT

    @property
    def type(self):
        return self.target.type

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


class Int_decl(object):

    def __init__(self, n_type, constraints, var_id, value=None):
        self._constraints = Int_literal(constraints)
        self._ID = Name(var_id, DATA_TYPE.decl_to_value(n_type))
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


class Int_literal(object):

    def __init__(self, value):
        self.value = value
        self.type = DATA_TYPE.INT_VAL
        self.node_type = DATA_TYPE.INT_LITERAL


class Bit_literal(object):

    def __init__(self, value):
        self.value = value
        self.type = DATA_TYPE.BIT_VAL
        self.node_type = DATA_TYPE.BIT_LITERAL


class Name(object):

    def __init__(self, name, id_type):
        self._name = name
        self._type = id_type

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value


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


class Binary_operation(object):

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


