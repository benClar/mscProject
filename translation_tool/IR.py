class IR(object):

    def __init__(self):
        self._IR = []

    def add(self, node):
        self.IR.append(node)

    @property
    def IR(self):
        return self._IR


class Int_decl(object):

    def __init__(self, n_type, constraints, var_id, value=None):
        self.node_type = n_type
        self.constraints = Int_literal(constraints)
        self.ID = Name(var_id)
        self.value = value


class Int_literal(object):

    def __init__(self, value):
        self.node_type = value


class Name(object):

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

class Binary_operation(object):

    def __init__(self, op_type, operator):
        self._node_type = op_type
        self._operator = operator
        self._left = None
        self._right = None
        self._result = None

    @property
    def result(self):
        return self._result

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

    @result.setter
    def result(self, value):
        self._result = value





