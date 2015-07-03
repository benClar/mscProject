from DATA_TYPE import DATA_TYPE


class IR(object):

    def __init__(self):
        self._IR = []

    def add(self, node):
        self.IR.append(node)

    @property
    def IR(self):
        return self._IR


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


class Cast(object):

    def __init__(self, c_op, c_target):
        self._cast_target = c_target
        self._cast_op = c_op

    @property
    def type(self):
        return self._cast_op.type


class Cast_operation(object):

    def __init__(self, c_type, constraints, size):
        self._type = c_type
        self._constraints = constraints
        self._seq_size = size

    @property
    def seq_size(self):
        return self._seq_size

    @property
    def constraints(self):
        return self._constraints

    @property
    def type(self):
        return self._type


class ID_set(object):

    def __init__(self, var_id, value, id_type):
        self._ID = Name(var_id, id_type)
        self._value = value
        self.node_type = DATA_TYPE.ID_SET

    @property
    def ID(self):
        return self._ID

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


class Bit_literal(object):

    def __init__(self, value):
        self.value = value
        self.type = DATA_TYPE.BIT_VAL


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


