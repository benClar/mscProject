from AST_TYPE import AST_TYPE
from pyparsing import ParseException


class AST(object):

    def __init__(self):
        self._tree = []

    def add_node(self, node):
        self.tree.append(node)

    @property
    def tree(self):
        return self._tree

    def id_set(self, tokens):
        # print(tokens)
        pass

    def bit_decl(self, tokens):
        # print(tokens[0].dump())
        token = tokens[0]
        for decl in token['value']:
            if 'set_value' in decl:
                self.add_node(Bit_decl_ast(decl['ID'][0], decl['set_value']))
            else:
                self.add_node(Bit_decl_ast(decl['ID'][0]))

    def int_decl(self, tokens):
        token = tokens[0]
        # print(token.dump())
        for decl in token['value']:
            if 'set_value' in decl:
                self.add_node(Int_decl_ast(decl['ID'][0], token['constraints'], decl['set_value']))
            else:
                self.add_node(Int_decl_ast(decl['ID'][0], token['constraints']))

    def seq_decl(self, tokens):
        token = tokens[0]
        if token['type'] == "Int":
            self.int_seq_decl(token)
        elif token['type'] == "Bit":
            pass
        else:
            raise ParseException("Unrecognised Token type")

    def int_seq_decl(self, token):
        print("HERE")
        print(token.dump())
        if 'value' in token:
            print("VALUE IN")
            self.add_node(Seq_decl_ast(token['ID'][1], token['type'], token['seq_size'], token[5], token['constraints']))
        else:
            self.add_node(Seq_decl_ast(token['ID'][1], token['type'], token['seq_size'], constraints=token['constraints']))


class Seq_decl_ast(object):

    node_type = AST_TYPE.SEQ_DECL

    def __init__(self, seq_id, seq_type, size, value=None, constraints=None):
        self._id = ID_ast(seq_id)
        self._type = seq_type
        if value is not None:
            # print(value)
            self._value = Expr_ast(value)
        else:
            self._value = None
        self._size = Expr_ast(size)
        if constraints is not None:
            self._bit_constraints = Expr_ast(constraints)

    @property
    def value(self):
        return self._value
    

class Int_decl_ast(object):

    node_type = AST_TYPE.INT_DECL

    def __init__(self, ID, bit_constraints, expr=None):
        self._ID = ID_ast(ID)
        self._bit_constraints = Expr_ast(bit_constraints)
        self._value = Expr_ast(expr)

    @property
    def ID(self):
        return self._ID

    @property
    def bit_constraints(self):
        return self._bit_constraints

    @property
    def value(self):
        return self._value


class Bit_decl_ast(object):

    node_type = AST_TYPE.BIT_DECL

    def __init__(self, ID, value=None):

        self._ID = ID_ast(ID)
        self._value = Expr_ast(value)

    @property
    def value(self):
        return self._value

    @property
    def ID(self):
        return self._ID


class Expr_ast(object):

    op_lookup = {'*': AST_TYPE.ARITH_OP,
                 '-': AST_TYPE.ARITH_OP,
                 '/': AST_TYPE.ARITH_OP,
                 '%': AST_TYPE.ARITH_OP,
                 '+': AST_TYPE.ARITH_OP,
                 '%': AST_TYPE.ARITH_OP,
                 '>>': AST_TYPE.BITWISE_OP,
                 '<<': AST_TYPE.BITWISE_OP,
                 '>>>': AST_TYPE.BITWISE_OP,
                 '<<<': AST_TYPE.BITWISE_OP,
                 '^': AST_TYPE.BITWISE_OP,
                 '&': AST_TYPE.BITWISE_OP,
                 '~': AST_TYPE.BITWISE_OP,
                 '|': AST_TYPE.BITWISE_OP,
                 '>': AST_TYPE.COMP_OP,
                 '>=': AST_TYPE.COMP_OP,
                 '<': AST_TYPE.COMP_OP,
                 '<=': AST_TYPE.COMP_OP,
                 '&&': AST_TYPE.COMP_OP}

    operand_lookup = {'Seq_val': AST_TYPE.SEQ_VAL,
                      'index_select': AST_TYPE.INDEX_SEL,
                      'function_call': AST_TYPE.FUNCTION_CALL,
                      'ID': AST_TYPE.ID,
                      'Int_val': AST_TYPE.INT_VAL,
                      'cast': AST_TYPE.CAST,
                      'Bit_val': AST_TYPE.BIT_VAL}

    node_type = AST_TYPE.EXPR

    def __init__(self, expr=None):
        if expr is not None:
            self._expressions = []
            self.eval(expr)
        else:
            self._expressions = None
        pass

    def eval(self, expr):
        # print("EXPR")
        # print(expr)
        for i in expr:
            # print("TOKEN")
            # print(i)
            if self.is_operand(i[0]):
                self.add_operand(i)
            elif self.is_operator(i):
                self.add_operator(i)
            else:
                self.expressions.append(Expr_ast(i))

    def is_operand(self, token):
        try:
            return token in Expr_ast.operand_lookup
        except TypeError:
            return False

    def add_operand(self, token):
        operand_type = Expr_ast.operand_lookup[token[0]]
        if operand_type == AST_TYPE.INT_VAL:
            self.expressions.append(Int_val_ast(token[1]))
        elif operand_type == AST_TYPE.CAST:
            self.expressions.append(cast_ast(token[1], token[2]))
        elif operand_type == AST_TYPE.ID:
            self.expressions.append(ID_ast(token[1]))
        elif operand_type == AST_TYPE.FUNCTION_CALL:
            if len(token) == 4:
                self.expressions.append(Func_call_ast(token[2], token[3]))
            elif len(token) == 3:
                self.expressions.append(Func_call_ast(token[2]))
            else:
                raise ParseException("Function Token not as expected")
        elif operand_type == AST_TYPE.SEQ_VAL:
            self.expressions.append(seq_value(token))
        elif operand_type == AST_TYPE.INDEX_SEL:
            # print("INDEX SEL")
            self.add_expr(Seq_index_select_ast(token[2], token[3]))
        else:
            print("ERROR")
            print(token)

    def is_operator(self, token):
        try:
            return token in Expr_ast.op_lookup
        except TypeError:
            return False

    def add_operator(self, token):
        self.expressions.append(Operator_ast(token, self.op_type(token)))

    def op_type(self, token):
        return Expr_ast.op_lookup[token]

    @property
    def expressions(self):
        return self._expressions

    def add_expr(self, expr):
        self.expressions.append(expr)


class seq_value(object):

    node_type = AST_TYPE.SEQ_VAL

    def __init__(self, value):
        self._value = []
        if value[0] != "Seq_val":
            raise ParseException("Tried to add non sequence value as parameter")
        else:
            value.pop(0)
        for p in value:
            self._value.append(Expr_ast(p))

    @property
    def value(self):
        return self._value


class Func_call_ast(object):

    node_type = AST_TYPE.FUNCTION_CALL

    def __init__(self, ID, parameters=None):
        self._ID = ID_ast(ID)
        if parameters is not None:
            self._parameters = []
            for p in parameters:
                self._parameters.append(Expr_ast(p))
        else:
            self._parameters = None

    @property
    def ID(self):
        return self._ID

    @property
    def parameters(self):
        return self._parameters


class Operator_ast(object):

    def __init__(self, op, op_type):
        self._operator = op
        self._type = op_type

    @property
    def operator(self):
        return self._operator

    @property
    def type(self):
        return self._type


class Int_val_ast(object):

    node_type = AST_TYPE.INT_VAL

    def __init__(self, int_val):
        self._value = int_val

    @property
    def value(self):
        return self._value

class Seq_index_select_ast(object):

    node_type = AST_TYPE.INDEX_SEL

    def __init__(self, index_sel_id, indices):
        print(index_sel_id)
        print(indices)
        # self._id = index_sel_id
        # self._indices = []
        # for i in indices:
        #     self._indices.append(Expr_ast(i))

class cast_ast(object):

    node_type = AST_TYPE.CAST

    def __init__(self, cast_type, expr):
        self._cast_operation = cast_type
        self._target = Expr_ast(expr)

    @property
    def target(self):
        return self._target


class ID_ast(object):

    node_type = AST_TYPE.ID

    def __init__(self, ID):
        self._ID = ID

    @property
    def ID(self):
        return self._ID
