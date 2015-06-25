from AST_TYPE import AST_TYPE
from pyparsing import ParseException
import sys


class AST(object):

    ID = 0  # Bit DECL
    BIT_DECL_CONTENT = 2
    BIT_EXPR = 2
    INT_SEQ_CNST = 1
    INT_SEQ_SIZE = 2
    INT_SEQ_VALUE = 5
    BIT_SEQ_SIZE = 1
    BIT_SEQ_VALUE = 4
    ID_SET_VALUE = 2
    INDEX_ID = 1
    INDEX_SET_VALUE = 3
    INDEX_SET_ELEMENTS = 2

    def __init__(self):
        self._tree = []

    def add_node(self, node):
        self.tree.append(node)

    @property
    def tree(self):
        return self._tree

    def bit_decl(self, tokens):
        # print(tokens[0].dump())
        token = tokens[0]
        for decl in token['value']:
            if 'set_value' in decl:
                self.add_node(Bit_decl_ast(decl[AST.ID], decl[AST.BIT_EXPR]))
            else:
                self.add_node(Bit_decl_ast(decl[AST.ID]))

    def int_decl(self, tokens):
        token = tokens[0]
        # print(token.dump())
        for decl in token['value']:
            if 'set_value' in decl:
                self.add_node(Int_decl_ast(decl['ID'][0], token[1], decl[2]))
            else:
                self.add_node(Int_decl_ast(decl['ID'][0], token[1]))

    def seq_decl(self, tokens):
        token = tokens[0]
        if token['type'] == "Int":
            self.int_seq_decl(token)
        elif token['type'] == "Bit":
            self.bit_seq_decl(token)
        else:
            raise ParseException("Unrecognised Token type")

    def int_seq_decl(self, token):
        # print(token.dump())
        if 'value' in token:
            # print(token)
            self.add_node(Seq_decl_ast(token['ID'][1][0], token['type'], token[AST.INT_SEQ_SIZE], token[AST.INT_SEQ_VALUE], token[AST.INT_SEQ_CNST]))
        else:
            pass
            self.add_node(Seq_decl_ast(token['ID'][1][0], token['type'], token[AST.INT_SEQ_SIZE], constraints=token[AST.INT_SEQ_CNST]))

    def bit_seq_decl(self, token):
        # print(token.dump())
        if 'value' in token:
            self.add_node(Seq_decl_ast(token['ID'][1][0], token['type'], token[AST.BIT_SEQ_SIZE], token[AST.BIT_SEQ_VALUE]))
        else:
            self.add_node(Seq_decl_ast(token['ID'][1][0], token['type'], token[AST.BIT_SEQ_SIZE]))

    def id_set(self, tokens):
        token = tokens[0]
        # print(token.dump())
        if token[0][0] == "index_select":
            self.add_node(ID_set_ast(token[0][1][1][0],
                          token[2],
                          token[0][1][2]))
        else:
            self.add_node(ID_set_ast(token[AST.ID], token[AST.ID_SET_VALUE]))


class ID_set_ast(object):

    node_type = AST_TYPE.ID_SET

    def __init__(self, set_id, value, elements=None):
        self._ID = ID_ast(set_id)
        self._value = Expr_ast(value)

        if elements is not None:
            self._elements = Expr_ast(elements)
        else:
            self._elements = None

    @property
    def value(self):
        return self._value

    @property
    def ID(self):
        return self._ID

    @property
    def elements(self):
        return self._elements


class Seq_decl_ast(object):

    node_type = AST_TYPE.SEQ_DECL

    def __init__(self, seq_id, seq_type, size, value=None, constraints=None):
        self._ID = ID_ast(seq_id)
        self._type = seq_type
        if value is not None:
            self._value = Expr_ast(value)
        else:
            self._value = None
        self._size = []
        for s in size:
            self._size.append(Expr_ast(size))

        if constraints is not None:
            self._bit_constraints = Expr_ast(constraints)

    @property
    def size(self):
        return self._size

    @property
    def value(self):
        return self._value

    @property
    def ID(self):
        return self._ID

    @property
    def bit_constraints(self):
        return self._bit_constraints


class Int_decl_ast(object):

    node_type = AST_TYPE.INT_DECL

    def __init__(self, ID, bit_constraints, expr=None):
        self._ID = ID_ast(ID)
        self._bit_constraints = Expr_ast(bit_constraints)
        self._value = Expr_ast(expr)

    @property
    def ID(self):
        return self._ID.ID

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
        return self._ID.ID


class Expr_ast(object):

    CONTENT = 1
    OPERAND_ID = 0

    op_lookup = {'*': AST_TYPE.ARITH_OP,
                 '-': AST_TYPE.ARITH_OP,
                 '/': AST_TYPE.ARITH_OP,
                 '%': AST_TYPE.ARITH_OP,
                 '+': AST_TYPE.ARITH_OP,
                 '%': AST_TYPE.ARITH_OP,
                 '>>': AST_TYPE.SHIFT_OP,
                 '<<': AST_TYPE.SHIFT_OP,
                 '>>>': AST_TYPE.SHIFT_OP,
                 '<<<': AST_TYPE.SHIFT_OP,
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
                      'Bit_val': AST_TYPE.BIT_VAL,
                      'seq_range': AST_TYPE.INDEX_RANGE}

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

        operand_type = Expr_ast.operand_lookup[token[Expr_ast.OPERAND_ID]]
        if operand_type == AST_TYPE.INT_VAL:
            self.expressions.append(Int_literal_ast(token[Expr_ast.CONTENT][0]))
        elif operand_type == AST_TYPE.CAST:
            self.expressions.append(cast_ast(token[Expr_ast.CONTENT][0], token[Expr_ast.CONTENT][1]))
        elif operand_type == AST_TYPE.ID:
            self.expressions.append(ID_ast(token[Expr_ast.CONTENT][0]))
        elif operand_type == AST_TYPE.FUNCTION_CALL:
            if len(token[1]) == 3:
                self.expressions.append(Func_call_ast(token[Expr_ast.CONTENT][1][0], token[Expr_ast.CONTENT][2]))
            elif len(token[1]) == 2:
                self.expressions.append(Func_call_ast(token[Expr_ast.CONTENT][1][0]))
            else:
                raise ParseException("Function Token not as expected")
        elif operand_type == AST_TYPE.SEQ_VAL:
            try:
                self.expressions.append(seq_value_ast(token[Expr_ast.CONTENT][0]))
            except IndexError:
                self.expressions.append(seq_value_ast())
        elif operand_type == AST_TYPE.INDEX_SEL:
            self.add_expr(Seq_index_select_ast(token[Expr_ast.CONTENT][1][0], token[Expr_ast.CONTENT][2]))
        elif operand_type == AST_TYPE.BIT_VAL:
            self.expressions.append(Bit_literal_ast(token[Expr_ast.CONTENT][0]))
        elif operand_type == AST_TYPE.INDEX_RANGE:
            self.expressions.append(Seq_range_ast(token[Expr_ast.CONTENT]))
        else:
            print("ERROR")
            print(token)
            sys.exit(1)

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


class Seq_range_ast(object):

    node_type = AST_TYPE.INDEX_RANGE

    def __init__(self, seq_range):

        self._start = Expr_ast(seq_range[0])
        self._finish = Expr_ast(seq_range[1])

    @property
    def start(self):
        return self._start

    @property
    def finish(self):
        return self._finish


class seq_value_ast(object):

    node_type = AST_TYPE.SEQ_VAL

    def __init__(self, value=None):
        if value is not None:
            self._value = []
            for p in value:
                self._value.append(Expr_ast(p))
        else:
            self._value = value

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
        self._node_type = op_type

    @property
    def operator(self):
        return self._operator

    @property
    def type(self):
        return self._type

    @property
    def node_type(self):
        return self._node_type
    


class Int_literal_ast(object):

    node_type = AST_TYPE.INT_VAL

    def __init__(self, int_val):
        self._value = int_val

    @property
    def value(self):
        return self._value

    # def __str__(self):
    #     return (self.value)


class Bit_literal_ast(object):

    node_type = AST_TYPE.BIT_VAL

    def __init__(self, bit_val):
        self._value = bit_val

    @property
    def value(self):
        return self._value


class Seq_index_select_ast(object):

    node_type = AST_TYPE.INDEX_SEL

    def __init__(self, index_sel_id, indices):
        self._ID = ID_ast(index_sel_id)
        self._indices = []
        for i in indices:
            self._indices.append(Expr_ast(i))

    @property
    def ID(self):
        return self._ID

    @property
    def indices(self):
        return self._indices

class Cast_type_ast(object):

    def __init__(self, operation):
        self._target_type = operation[0]
        try:
            self._elements = Expr_ast(operation[1])
            if len(operation[1]) > 1:
                raise ParseException("Can only cast into one dimension array")
        except IndexError:
            self._elements = None


class cast_ast(object):

    node_type = AST_TYPE.CAST

    def __init__(self, cast_type, expr):
        self._cast_operation = Cast_type_ast(cast_type)
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
