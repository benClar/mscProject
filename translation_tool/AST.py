import unittest
from AST_TYPE import AST_TYPE

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
                self.add_node(Bit_decl_ast(decl['ID'][1], decl['set_value']))
            else:
                self.add_node(Bit_decl_ast(decl['ID']))

    def int_decl(self, tokens):
        token = tokens[0]
        print(token.dump())
        for decl in token['value']:
            if 'set_value' in decl:
                print(decl['ID_'])
                print(token['constraints'])
                print(decl['set_value'])
                # self.add_node(Int_decl_ast(decl['ID']), token['constraints'], decl['set_value'])
            else:                
                print(decl['ID_'])
                print(token['constraints'])
                # self.add_node(Int_decl_ast(decl['ID']), token['constraints'])

class Int_decl_ast(object):

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
        for i in expr:
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


class Operator_ast(object):

    def __init__(self, op, op_type):
        self.operator = op
        self._type = op_type


class Int_val_ast(object):

    node_type = AST_TYPE.INT_VAL

    def __init__(self, int_val):
        self._value = int_val

    @property
    def value(self):
        return self._value


class cast_ast(object):

    def __init__(self, cast_type, expr):
        self.type = cast_type
        self.expr = Expr_ast(expr)


class ID_ast(object):

    node_type = AST_TYPE.ID

    def __init__(self, ID):
        self._ID = ID

