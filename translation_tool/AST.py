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
        self._statements = []
        self._target = []
        self.add_target({'parent': self, 'target': self._statements})

    def add_target(self, target):
        self._target.insert(0, target)

    def remove_target(self):
        return self._target.pop(0)

    def add_function_node(self, node):
        """Bypasses check and directly adds node to function list"""
        self._tree.append(node)

    def add_statement(self, node):
        # print(self._target[0])
        self._target[0]['target'].append(node)

    @property
    def statements(self):
        return self._statements

    @property
    def tree(self):
        """returns the list of statement nodes for testing if there are no function nodes"""
        if len(self._tree) == 0:
            return self._statements
        else:
            return self._tree

    def bit_decl(self, tokens):
        # print(tokens)
        token = tokens[0]
        for decl in token['value']:
            if 'set_value' in decl:
                self.add_statement(Bit_decl_ast(decl[AST.ID], decl[AST.BIT_EXPR]))
            else:
                self.add_statement(Bit_decl_ast(decl[AST.ID]))

    def int_decl(self, tokens):
        token = tokens[0]
        # print(token.dump())
        if token['decl'] == "@Int":
            decl_type = AST_TYPE.BS_INT_DECL
        else:
            decl_type = AST_TYPE.INT_DECL
        for decl in token['value']:
            if 'set_value' in decl:
                self.add_statement(Int_decl_ast(decl_type, decl['ID'][0], token[1], decl[2]))
            else:
                self.add_statement(Int_decl_ast(decl_type, decl['ID'][0], token[1]))

    def seq_decl(self, tokens):
        token = tokens[0]
        # print(token.dump())
        if token['type'] == "Int" or token['type'] == "@Int":
            self.int_seq_decl(token)
        elif token['type'] == "Bit":
            self.bit_seq_decl(token)
        else:
            raise ParseException("Unrecognised Token type")

    def begin_for(self, tokens):
        new_for = for_loop_ast()
        self.add_statement(new_for)
        self.add_target({'parent': new_for, 'target': new_for.initializer})

    def for_terminator(self, tokens):
        curr = self.remove_target()['parent']
        self.add_target({'parent': curr, 'target': curr.terminator})

    def for_increment(self, tokens):
        curr = self.remove_target()['parent']
        self.add_target({'parent': curr, 'target': curr.increment})

    def for_body(self, tokens):
        curr = self.remove_target()['parent']
        self.add_target({'parent': curr, 'target': curr.body})

    def end_for(self, tokens):
        self.remove_target()

    def terminator_expr(self, tokens):
        token = tokens[0]
        self.add_statement(Expr_ast(token))

    def terminator(self, tokens):
        if len(tokens) > 0:
            token = tokens[0]
            self.add_statement(Expr_ast(token))

    def int_seq_decl(self, token):
        seq_decl_type = None
        # print(token.dump())
        if token['type'] == "@Int":
            seq_decl_type = AST_TYPE.BS_SEQ_INT_DECL
        elif token['type'] == "Int":
            seq_decl_type = AST_TYPE.SEQ_INT_DECL
        else:
            raise ParseException("Unknown Int Seq Type")
        # seq_decl_type
        if 'value' in token:
            self.add_statement(Seq_decl_ast(seq_decl_type, token['ID'][1][0], token['type'], token[AST.INT_SEQ_SIZE], token[AST.INT_SEQ_VALUE], token[AST.INT_SEQ_CNST]))
        else:
            pass
            self.add_statement(Seq_decl_ast(seq_decl_type, token['ID'][1][0], token['type'], token[AST.INT_SEQ_SIZE], constraints=token[AST.INT_SEQ_CNST]))

    def bit_seq_decl(self, token):
        # print(token.dump())
        if 'value' in token:
            self.add_statement(Seq_decl_ast(AST_TYPE.SEQ_BIT_DECL, token['ID'][1][0], token['type'], token[AST.BIT_SEQ_SIZE], token[AST.BIT_SEQ_VALUE]))
        else:
            self.add_statement(Seq_decl_ast(AST_TYPE.SEQ_BIT_DECL, token['ID'][1][0], token['type'], token[AST.BIT_SEQ_SIZE]))

    def id_set(self, tokens):
        token = tokens[0]
        # print(token.dump())
        if token[0][0] == "index_select":
            self.add_statement(ID_set_ast(token[0][1][1][0],
                               token[2],
                               token[0][1][2]))
        else:
            self.add_statement(ID_set_ast(token[AST.ID], token[AST.ID_SET_VALUE]))

    def function_decl(self, tokens):
        token = tokens[0]
        # print(token.dump())
        self.add_function_node(function_declaration_ast(token[0], token[1][1][0], token[2]))
        self.tree[-1].stmts += self.statements[:]
        self.statements.clear()

    def return_stmt(self, tokens):
        token = tokens[0]
        self.add_statement(return_stmt_ast(token[1]))

    def if_cond(self, tokens):
        self.add_statement(Expr_ast(tokens))

    def begin_if(self, tokens):
        new_if = if_stmt_ast()
        self.add_statement(new_if)
        self.add_target({'parent': new_if, 'target': new_if.condition})

    def if_body_st(self, tokens):
        curr_node = self.remove_target()['parent']
        self.add_target({'parent': curr_node, 'target': curr_node.body})

    def if_body_end(self, tokens):
        self.remove_target()


class if_stmt_ast(object):

    node_type = AST_TYPE.IF_STMT

    def __init__(self):
        self._condition = []
        self._body = []

    @property
    def body(self):
        return self._body

    @property
    def condition(self):
        return self._condition

    @condition.setter
    def condition(self, value):
        self._condition = value


class return_stmt_ast(object):

    node_type = AST_TYPE.RETURN_STMT

    def __init__(self, expr):
        self._expr = Expr_ast(expr)

    @property
    def expr(self):
        return self._expr


class function_declaration_ast(object):

    node_type = AST_TYPE.FUNC_DECL

    def __init__(self, return_value, ID, parameters):
        self._stmts = []
        self._ID = ID_ast(ID)
        self._parameters = []

        for p in parameters:
            self._parameters.append({"param_type": AST_TYPE.convert(p[0]), "param_ID": p[1][1][0]})

        self.return_value = AST_TYPE.convert(return_value)

    @property
    def stmts(self):
        return self._stmts

    def add_statement(self, stmt):
        self.stmts.append(stmt)

    @property
    def ID(self):
        return self._ID

    @stmts.setter
    def stmts(self, value):
        self._stmts = value

    @property
    def parameters(self):
        return self._parameters


class for_loop_ast(object):

    node_type = AST_TYPE.FOR_LOOP

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
        return self._ID.ID

    @property
    def elements(self):
        return self._elements


class Seq_decl_ast(object):

    def __init__(self, deq_decl_type, seq_id, seq_type, size, value=None, constraints=None):
        self.node_type = deq_decl_type
        self._ID = ID_ast(seq_id)
        if value is not None:
            self._value = Expr_ast(value)
        else:
            self._value = None
        self._size = []
        for s in size:
            self._size.append(Expr_ast(s))

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

    def __init__(self, decl_type, ID, bit_constraints, expr=None):
        self.node_type = decl_type
        self._ID = ID_ast(ID)
        self._bit_constraints = Expr_ast(bit_constraints)
        if expr is not None:
            self._value = Expr_ast(expr)
        else:
            self._value = None

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
        if value is not None:
            self._value = Expr_ast(value)
        else:
            self._value = None

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
                 '&&': AST_TYPE.COMP_OP,
                 '==': AST_TYPE.COMP_OP,
                 '!=': AST_TYPE.COMP_OP}

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
        self._ret_value = None
        if expr is not None:
            self._expressions = []
            self.eval(expr)
        else:
            self._expressions = None
        pass

    @property
    def ret_value(self):
        return self._ret_value

    @ret_value.setter
    def setter(self, value):
        self._ret_value = value

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
        self._seq_type = None
        if value is not None:
            self._value = []
            for p in value:
                self._value.append(Expr_ast(p))
        else:
            self._value = value

    @property
    def value(self):
        return self._value

    @property
    def size(self):
        return len(self.value)

    @property
    def seq_type(self):
        return self._seq_type

    @seq_type.setter
    def seq_type(self, value):
        self._seq_type = value


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
        self._ID_type = None

    @property
    def ID_type(self):
        return self._ID_type

    @ID_type.setter
    def ID_type(self, value):
        self._ID_type = value

    @property
    def ID(self):
        return self._ID
