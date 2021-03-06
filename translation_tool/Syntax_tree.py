from DATA_TYPE import DATA_TYPE
from pyparsing import ParseException
import sys
from Semantic_analyser import Semantic_analyser


class Syntax_tree(object):
    """Turns list of parsed grammar production to syntax nodes"""

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
        # self._statements = []
        self._target = []
        self.add_target({'parent': self, 'target': self._tree})
        self.semantic_analyser = Semantic_analyser()

    def add_target(self, target):
        """Add target for future statements to be appended.

        Args:
        target: Target for statements"""
        self._target.insert(0, target)

    def remove_target(self):
        """Remove Target at top of stack for statements."""
        return self._target.pop(0)

    def add_statement(self, node):
        """Add statement to target node

        Args:
        node: parsed syntax node containing statement to be added to target."""
        self._target[0]['target'].append(node)

    @property
    def target(self):
        return self._target[0]
    
    @property
    def statements(self):
        return self._statements

    @property
    def tree(self):
        """Returns the list of statement nodes for testing if there are no function nodes."""
        # if len(self._tree) == 0:
        #     return self._statements
        # else:
        return self._tree

    def stand_alone_expr(self, tokens):
        """Adds a single expression syntax fragment.

        Args:
        tokens: parsed tokens that make up statement."""
        self.add_statement(Expr_syn_node(tokens[0]))

    def bit_decl(self, tokens):
        """Accepts tokens and constructs a bit declaration syntax fragment.

        Args:
        tokens: parsed tokens that make up statement."""
        token = tokens[0]
        # print(token.dump())
        if token['decl'] == "@Bit":
            decl_type = DATA_TYPE.BS_BIT_DECL
        else:
            decl_type = DATA_TYPE.BIT_DECL
        for decl in token['value']:
            if 'set_value' in decl:
                self.add_statement(Bit_decl_syn_node(decl[Syntax_tree.ID], decl_type, decl[Syntax_tree.BIT_EXPR]))
            else:
                self.add_statement(Bit_decl_syn_node(decl[Syntax_tree.ID], decl_type))

    def int_decl(self, tokens):
        """Accepts tokens and constructs an integer declaration syntax fragment.

        Args:
        tokens: parsed tokens that make up statement."""
        token = tokens[0]
        # print(token.dump())
        if token['decl'] == "@Int":
            decl_type = DATA_TYPE.BS_INT_DECL
        else:
            decl_type = DATA_TYPE.INT_DECL
        for decl in token['value']:
            if 'set_value' in decl:
                self.add_statement(Int_decl_syn_node(decl_type, decl['ID'][0], token[1], decl[2]))
            else:
                self.add_statement(Int_decl_syn_node(decl_type, decl['ID'][0], token[1]))

    def seq_decl(self, tokens):
        """Accepts tokens and constructs an sequence declaration syntax fragment.

        Args:
        tokens: parsed tokens that make up statement."""
        token = tokens[0]
        # print(token.dump())

        if token['type'] == "Int" or token['type'] == "@Int" or token['type'] == "Sbox":
            self.bit_constrained_seq_decl(token)
        elif token['type'] == "Bit":
            self.bit_seq_decl(token)
        else:
            raise ParseException("Unrecognised Token type")

    def begin_for(self, tokens):
        """Creates for statement syntax node and sets it as current target for further statements.

        Args:
        tokens: parsed tokens that make up statement."""
        new_for = for_loop_syn_node()
        self.add_statement(new_for)
        self.add_target({'parent': new_for, 'target': new_for.initializer})

    def for_terminator(self, tokens):
        """Adds terminator as target for next parsed tokens"""
        curr = self.remove_target()['parent']
        self.add_target({'parent': curr, 'target': curr.terminator})

    def for_increment(self, tokens):
        """Adds increment as target for next parsed tokens"""
        curr = self.remove_target()['parent']
        self.add_target({'parent': curr, 'target': curr.increment})

    def for_body(self, tokens):
        """Adds for body as target for next parsed tokens"""
        curr = self.remove_target()['parent']
        self.add_target({'parent': curr, 'target': curr.body})

    def end_for(self, tokens):
        """Removes for loop as target"""
        self.remove_target()

    def terminator_expr(self, tokens):
        """parses terminator expression"""
        token = tokens[0]
        self.add_statement(Expr_syn_node(token))

    # def terminator(self, tokens):
    #     if len(tokens) > 0:
    #         token = tokens[0]
    #         self.add_statement(Expr_syn_node(token))

    def bit_constrained_seq_decl(self, token):
        """Builds syntax node for sequence declarations that have bit widths set"""
        seq_decl_type = None
        # print(token.dump())
        if token['type'] == "@Int":
            seq_decl_type = DATA_TYPE.BS_SEQ_INT_DECL
        elif token['type'] == "Int":
            seq_decl_type = DATA_TYPE.SEQ_INT_DECL
        elif token['type'] == "Sbox":
            seq_decl_type = DATA_TYPE.SBOX_DECL
        else:
            raise ParseException("Unknown Int Seq Type")
        # seq_decl_type
        if 'value' in token:
            self.add_statement(Seq_decl_syn_node(seq_decl_type, token['ID'][1][0], token[Syntax_tree.INT_SEQ_SIZE], token[Syntax_tree.INT_SEQ_VALUE], token[Syntax_tree.INT_SEQ_CNST]))
        else:
            self.add_statement(Seq_decl_syn_node(seq_decl_type, token['ID'][1][0], token[Syntax_tree.INT_SEQ_SIZE], constraints=token[Syntax_tree.INT_SEQ_CNST]))

    def bit_seq_decl(self, token):
        """Builds syntax node for bit sequence declaration"""
        if 'value' in token:
            self.add_statement(Seq_decl_syn_node(DATA_TYPE.SEQ_BIT_DECL, token['ID'][1][0], token[Syntax_tree.BIT_SEQ_SIZE], token[Syntax_tree.BIT_SEQ_VALUE]))
        else:
            self.add_statement(Seq_decl_syn_node(DATA_TYPE.SEQ_BIT_DECL, token['ID'][1][0], token[Syntax_tree.BIT_SEQ_SIZE]))

    def id_set(self, tokens):
        """Builds syntax node for ID set"""
        token = tokens[0]
        # print(token)
        if token[0][0] == "index_select":
            if token[0][1][0] == "cast":
                set_target = index_select_syn_node(Expr_syn_node([token[0][1]]), token[0][1][2])
            elif token[0][1][0] == "ID":
                set_target = index_select_syn_node(ID_syn_node(token[0][1][1][0]), token[0][1][2])
            self.add_statement(ID_set_syn_node(set_target, token[2]))
        else:
            self.add_statement(ID_set_syn_node(ID_syn_node(token[Syntax_tree.ID]), token[Syntax_tree.ID_SET_VALUE]))

    def function_start(self, tokens):
        """Adds function as the target for parsed tokens"""
        new_func = function_declaration_syn_node()
        self.add_statement(new_func)
        self.add_target({'parent': new_func, 'target': new_func.stmts})

    # def function_end(self, tokens):


    def function_decl(self, tokens):
        """Builds syntax node for parsed function and adds it to the
        function table"""
        token = tokens[0]
        params = []
        for p in token['func_param']:
            decl_type = self.param_type(p)
            if decl_type == DATA_TYPE.INT_DECL or decl_type == DATA_TYPE.BS_INT_DECL:
                params.append(Int_decl_syn_node(decl_type, p[2][1][0], p[1]))
            elif decl_type == DATA_TYPE.SEQ_INT_DECL or decl_type == DATA_TYPE.BS_SEQ_INT_DECL or decl_type == DATA_TYPE.SBOX_DECL:
                params.append(Seq_decl_syn_node(decl_type, p[3][1][0], p[2], constraints=p[1]))
            elif decl_type == DATA_TYPE.SEQ_BIT_DECL:
                params.append(Seq_decl_syn_node(decl_type, p[2][1][0], p[1]))
            elif decl_type == DATA_TYPE.BIT_DECL:
                params.append(Bit_decl_syn_node(p[1][1][0], DATA_TYPE.BIT_DECL))
            else:
                raise ParseException("Unknown Param Type")

        self.target['parent'].return_value = self.return_type(token[0])
        self.target['parent'].ID = ID_syn_node(token['func_ID'][1][0])
        self.target['parent'].parameters = params
        self.add_to_function_table(self.target['parent'])
        self.remove_target()


    def add_to_function_table(self, node):
        """Adds function to function table"""
        self.semantic_analyser.sym_table.add_function(node.ID)
        self.add_to_function_table_op(self.semantic_analyser.sym_table.add_function_return, node.return_value, node.ID)  # Adds function return type to function table
        for p in node.parameters:
           self.add_to_function_table_op(self.semantic_analyser.sym_table.add_function_parameter, p, node.ID)  # adds parameter information to function table

    def add_to_function_table_op(self, function_table_op, var, ID):
        """Executes function for function table.

        Args:
            function_table_op: function to execute.
            var: node to add
            id: id of function"""
        if var == DATA_TYPE.VOID:
            function_table_op(ID, DATA_TYPE.VOID)
        elif var.node_type == DATA_TYPE.INT_DECL:
            function_table_op(ID, DATA_TYPE.INT_DECL, constraints=var.bit_constraints)
        elif var.node_type == DATA_TYPE.BS_INT_DECL:
            function_table_op(ID, DATA_TYPE.BS_INT_DECL, constraints=var.bit_constraints)
        elif var.node_type == DATA_TYPE.SEQ_INT_DECL:
            function_table_op(ID, DATA_TYPE.SEQ_INT_DECL, constraints=var.bit_constraints, size=var.size)
        elif var.node_type == DATA_TYPE.BS_SEQ_INT_DECL:
            function_table_op(ID, DATA_TYPE.BS_SEQ_INT_DECL, constraints=var.bit_constraints, size=var.size)
        elif var.node_type == DATA_TYPE.SEQ_BIT_DECL:
            function_table_op(ID, DATA_TYPE.SEQ_INT_DECL, size=var.size)
        elif var.node_type == DATA_TYPE.BIT_DECL:
            function_table_op(ID, DATA_TYPE.BIT_DECL)
        elif var.node_type == DATA_TYPE.SBOX_DECL:
            function_table_op(ID, DATA_TYPE.SBOX_DECL, constraints=var.bit_constraints.expressions[0].value, size=var.size)
        elif var.node_type == DATA_TYPE.BS_BIT_DECL:
            function_table_op(ID, DATA_TYPE.BS_BIT_DECL)
        else:
            raise ParseException("Internal Error: Unrecognised var type for f table op " + str(var.node_type))

    def param_type(self, param):
        """converts string type of param to correct type representation"""
        if param[0] == "@Int":
            if self.is_sequence(param):
                return DATA_TYPE.BS_SEQ_INT_DECL
            else:
                return DATA_TYPE.BS_INT_DECL
        elif param[0] == "Int":
            if self.is_sequence(param):
                return DATA_TYPE.SEQ_INT_DECL
            else:
                return DATA_TYPE.INT_DECL
        elif param[0] == "Bit":
            if self.is_sequence(param):
                return DATA_TYPE.SEQ_BIT_DECL
            else:
                return DATA_TYPE.BIT_DECL
        elif param[0] == "Sbox":
            if self.is_sequence(param):
                return DATA_TYPE.SBOX_DECL
            else:
                raise ParseException("Sbox type must be sequence of integers")

    def return_type(self, param):
        """Converts string representation of return type to syntax node"""
        if param[0] == "@Int":
            if self.is_sequence(param):
                return Seq_decl_syn_node(DATA_TYPE.BS_SEQ_INT_DECL, None, size=param[2], constraints=param[1])
            else:
                return Int_decl_syn_node(DATA_TYPE.BS_INT_DECL, None, param[1])
        elif param[0] == "Int":
            if self.is_sequence(param):
                # print(param[1])
                return Seq_decl_syn_node(DATA_TYPE.SEQ_INT_DECL, None, size=param[2], constraints=param[1])
            else:
                return Int_decl_syn_node(DATA_TYPE.INT_DECL, None, param[1])
        elif param[0] == "Bit":
            if self.is_sequence(param):
                return Seq_decl_syn_node(DATA_TYPE.SEQ_BIT_DECL, None, param[1])
            else:
                return Bit_decl_syn_node(None, DATA_TYPE.BIT_DECL)
        elif param[0] == "@Bit":
            if self.is_sequence(param):
                return Seq_decl_syn_node(DATA_TYPE.SEQ_BS_BIT_DECL, None, param[1])
            else:
                return Bit_decl_syn_node(None, DATA_TYPE.BS_BIT_DECL)
        elif param[0] == "void":
            return DATA_TYPE.VOID
        else:
            raise ParseException("Internal error: Unknown return type")

    def is_sequence(self, param):
        if 'seq_size' in param:
            return True
        return False

    def return_stmt(self, tokens):
        """builds syntax node for return statement"""
        token = tokens[0]
        self.add_statement(return_stmt_syn_node(token[1]))

    def if_cond(self, tokens):
        """Adds if condition to target node"""
        self.add_statement(Expr_syn_node(tokens))

    def begin_if(self, tokens):
        """Sets if node as target for parsed tokens"""
        new_if = if_stmt_syn_node()
        self.add_statement(new_if)
        self.add_target({'parent': new_if, 'target': new_if.condition})

    def if_body_st(self, tokens):
        """Adds if body as target for parsed tokens """
        curr_node = self.remove_target()['parent']
        self.add_target({'parent': curr_node, 'target': curr_node.body})

    def if_body_end(self, tokens):
        """removes if node as target"""
        self.remove_target()


class if_stmt_syn_node(object):
    """syntax node representing if statements"""

    node_type = DATA_TYPE.IF_STMT

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


class return_stmt_syn_node(object):
    """Syntax node representing return statements"""

    node_type = DATA_TYPE.RETURN_STMT

    def __init__(self, expr):
        self._expr = Expr_syn_node(expr)

    @property
    def expr(self):
        return self._expr


class function_declaration_syn_node(object):
    """Syntax node representing function declaration"""

    node_type = DATA_TYPE.FUNC_DECL

    # def __init__(self, return_value, ID, parameters):
    def __init__(self):
        self._stmts = []
        self._ID = None
        self._parameters = None
        self.return_value = None
        # self._ID = ID_ast(ID)
        # self._parameters = parameters
        # self.return_value = return_value

    @property
    def stmts(self):
        return self._stmts

    def add_statement(self, stmt):
        self.stmts.append(stmt)

    @property
    def ID(self):
        return self._ID.ID

    @ID.setter
    def ID(self, value):
        self._ID = value

    @stmts.setter
    def stmts(self, value):
        self._stmts = value

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        self._parameters = value


class for_loop_syn_node(object):
    """syntax node representing for loop"""

    node_type = DATA_TYPE.FOR_LOOP

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


class ID_set_syn_node(object):
    """Syntax node representing set operation"""

    node_type = DATA_TYPE.ID_SET

    def __init__(self, target, value):
        self._target = target
        self._value = Expr_syn_node(value)

    @property
    def value(self):
        return self._value

    @property
    def target(self):
        return self._target

    def set_type(self):
        return self.target.node_type


class Seq_decl_syn_node(object):
    """Syntax node representing sequence declarations"""

    def __init__(self, seq_decl_type, seq_id, size, value=None, constraints=None):
        self.node_type = seq_decl_type
        self._ID = ID_syn_node(seq_id)
        if value is not None:
            self._value = Expr_syn_node(value)
        else:
            self._value = None
        self._size = []
        for s in size:
            self._size.append(Expr_syn_node(s))

        if constraints is not None:
            self._bit_constraints = Expr_syn_node(constraints)
        else:
            self._bit_constraints = None

    @property
    def size(self):
        return self._size

    @property
    def value(self):
        return self._value

    @property
    def ID(self):
        return self._ID.ID

    @property
    def bit_constraints(self):
        return self._bit_constraints


class Int_decl_syn_node(object):
    """Syntax node representing int declaration"""

    def __init__(self, decl_type, ID, bit_constraints, expr=None):
        self.node_type = decl_type
        if ID is not None:
            self._ID = ID_syn_node(ID)
        else:
            self._ID = ID
        self._bit_constraints = Expr_syn_node(bit_constraints)
        if expr is not None:
            self._value = Expr_syn_node(expr)
        else:
            self._value = None

    @property
    def ID(self):
        if self._ID is not None:
            return self._ID.ID
        else:
            return None

    @property
    def bit_constraints(self):
        return self._bit_constraints

    @property
    def value(self):
        return self._value


class Bit_decl_syn_node(object):
    """Syntax node representing bit declaration"""

    def __init__(self, ID, bit_type, value=None):

        self._ID = ID_syn_node(ID)
        self.node_type = bit_type
        if value is not None:
            self._value = Expr_syn_node(value)
        else:
            self._value = None

    @property
    def value(self):
        return self._value

    @property
    def ID(self):
        if self._ID is not None:
            return self._ID.ID
        else:
            return None


class Expr_syn_node(object):
    """syntax node representing expressions"""

    CONTENT = 1
    OPERAND_ID = 0

    op_lookup = {'*': DATA_TYPE.ARITH_OP,
                 '-': DATA_TYPE.ARITH_OP,
                 '/': DATA_TYPE.ARITH_OP,
                 '%': DATA_TYPE.ARITH_OP,
                 '+': DATA_TYPE.ARITH_OP,
                 '>>': DATA_TYPE.SHIFT_OP,
                 '<<': DATA_TYPE.SHIFT_OP,
                 '>>>': DATA_TYPE.SHIFT_OP,
                 '<<<': DATA_TYPE.SHIFT_OP,
                 '^': DATA_TYPE.BITWISE_OP,
                 '&': DATA_TYPE.BITWISE_OP,
                 '~': DATA_TYPE.BITWISE_OP,
                 '|': DATA_TYPE.BITWISE_OP,
                 '>': DATA_TYPE.COMP_OP,
                 '>=': DATA_TYPE.COMP_OP,
                 '<': DATA_TYPE.COMP_OP,
                 '<=': DATA_TYPE.COMP_OP,
                 '&&': DATA_TYPE.COMP_OP,
                 '==': DATA_TYPE.COMP_OP,
                 '!=': DATA_TYPE.COMP_OP,
                 '||': DATA_TYPE.LOG_OP,
                 '&&': DATA_TYPE.LOG_OP}

    operand_lookup = {'Seq_val': DATA_TYPE.SEQ_VAL,
                      'index_select': DATA_TYPE.INDEX_SELECT,
                      'function_call': DATA_TYPE.FUNCTION_CALL,
                      'ID': DATA_TYPE.ID,
                      'Int_val': DATA_TYPE.INT_VAL,
                      'cast': DATA_TYPE.CAST,
                      'Bit_val': DATA_TYPE.BIT_VAL,
                      'seq_range': DATA_TYPE.INDEX_RANGE}

    node_type = DATA_TYPE.EXPR

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
        """Evaluates passed in expression, recursively creating
        more expression nodes if necessary"""
        for i in expr:
            if self.is_operand(i[0]):
                self.add_operand(i)
            elif self.is_operator(i):
                self.add_operator(i)
            else:
                self.expressions.append(Expr_syn_node(i))

    def is_operand(self, token):
        """Returns true if operand"""
        try:
            return token in Expr_syn_node.operand_lookup
        except TypeError:
            return False

    def add_operand(self, token):
        """Creates node for operand"""
        operand_type = Expr_syn_node.operand_lookup[token[Expr_syn_node.OPERAND_ID]]
        if operand_type == DATA_TYPE.INT_VAL:
            self.expressions.append(Int_literal_syn_node(token[Expr_syn_node.CONTENT][0]))
        elif operand_type == DATA_TYPE.CAST:
            self.expressions.append(cast_syn_node(token[Expr_syn_node.CONTENT][0], token[Expr_syn_node.CONTENT][1]))
        elif operand_type == DATA_TYPE.ID:
            self.expressions.append(ID_syn_node(token[Expr_syn_node.CONTENT][0]))
        elif operand_type == DATA_TYPE.FUNCTION_CALL:
            if len(token[1]) == 3:
                self.expressions.append(Func_call_syn_node(token[Expr_syn_node.CONTENT][1][0], token[Expr_syn_node.CONTENT][2]))
            elif len(token[1]) == 2:
                self.expressions.append(Func_call_syn_node(token[Expr_syn_node.CONTENT][1][0]))
            else:
                raise ParseException("Function Token not as expected")
        elif operand_type == DATA_TYPE.SEQ_VAL:
            try:
                self.expressions.append(seq_value_syn_node(token[Expr_syn_node.CONTENT][0]))
            except IndexError:
                self.expressions.append(seq_value_syn_node())
        elif operand_type == DATA_TYPE.INDEX_SELECT:
            ID = None
            if token[1][0] == "cast":
                ID = Expr_syn_node([token[1]])
            elif token[1][0] == "ID":
                ID = ID_syn_node(token[1][1][0])
            self.add_expr(index_select_syn_node(ID, token[Expr_syn_node.CONTENT][2]))
        elif operand_type == DATA_TYPE.BIT_VAL:
            self.expressions.append(Bit_literal_syn_node(token[Expr_syn_node.CONTENT][0]))
        elif operand_type == DATA_TYPE.INDEX_RANGE:
            self.expressions.append(Seq_range_syn_node(token[Expr_syn_node.CONTENT]))
        else:
            print("ERROR")
            print(token)
            sys.exit(1)

    def is_operator(self, token):
        """returns true is token is operator"""
        # print(token)
        try:
            return token in Expr_syn_node.op_lookup
        except TypeError:
            return False

    def add_operator(self, token):
        """Adds operator"""
        self.expressions.append(Operator_syn_node(token, self.op_type(token)))

    def op_type(self, token):
        """Identfies operator"""
        return Expr_syn_node.op_lookup[token]

    @property
    def expressions(self):
        return self._expressions

    def add_expr(self, expr):
        """Adds an expression to expression node"""
        self.expressions.append(expr)


class Seq_range_syn_node(object):
    """Syntax node for range notation"""

    node_type = DATA_TYPE.INDEX_RANGE

    def __init__(self, seq_range):
        self._start = Expr_syn_node(seq_range[0])
        self._finish = Expr_syn_node(seq_range[1])

    @property
    def start(self):
        return self._start

    @property
    def finish(self):
        return self._finish


class seq_value_syn_node(object):
    """syntax node for sequence value"""

    node_type = DATA_TYPE.SEQ_VAL

    def __init__(self, value=None):
        self._seq_type = None
        if value is not None:
            self._value = []
            for p in value:
                self._value.append(Expr_syn_node(p))
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


class Func_call_syn_node(object):
    """Syntax node for function call"""

    node_type = DATA_TYPE.FUNCTION_CALL

    def __init__(self, ID, parameters=None):
        self._ID = ID_syn_node(ID)
        if parameters is not None:
            self._parameters = []
            for p in parameters:
                self._parameters.append(Expr_syn_node(p))
        else:
            self._parameters = None

    @property
    def ID(self):
        return self._ID.ID

    @property
    def parameters(self):
        return self._parameters


class Operator_syn_node(object):
    """Syntax node representing operator"""

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


class Int_literal_syn_node(object):
    """Syntax node representing integer literals"""

    node_type = DATA_TYPE.INT_VAL

    def __init__(self, int_val):
        self._value = int_val

    @property
    def value(self):
        return self._value

    # def __str__(self):
    #     return (self.value)


class Bit_literal_syn_node(object):
    """Syntax node representing bit literals"""

    node_type = DATA_TYPE.BIT_VAL

    def __init__(self, bit_val):
        self._value = bit_val

    @property
    def value(self):
        return self._value


class index_select_syn_node(object):
    """Syntax node represnting index select operations"""

    node_type = DATA_TYPE.INDEX_SELECT

    def __init__(self, target, indices):
        self._target = target
        self._indices = []
        for i in indices:
            self._indices.append(Expr_syn_node(i))

    @property
    def target(self):
            return self._target

    @property
    def ID(self):
        if self._target.node_type == DATA_TYPE.ID:
            return self._target.ID

    @property
    def target_type(self):
        return self._target.node_type

    @property
    def indices(self):
        return self._indices


class Cast_type_syn_node(object):
    """Syntax node representing explicit casts operations"""

    def __init__(self, operation):
        self._target_type = None
        self._constraints = None
        self._seq_size = None
        if operation[0] == "Bit":
            if len(operation) == 1:
                self._target_type = DATA_TYPE.convert(operation[0])
            elif len(operation) == 2:
                self._seq_size = []
                for s in operation[1]:
                    self._seq_size.append(Expr_syn_node(s))
                self._target_type = DATA_TYPE.convert(operation[0], "Seq")
        elif operation[0] == "Int" or operation[0] == "@Int":
            self._constraints = Expr_syn_node(operation[1])
            if len(operation) == 2:
                self._target_type = DATA_TYPE.convert(operation[0])
            elif len(operation) == 3:
                self._seq_size = []
                for s in operation[2]:
                    self._seq_size.append(Expr_syn_node(s))
                self._target_type = DATA_TYPE.convert(operation[0], "Seq")
        # print(">>>")
        # print(self._target_type)
        try:
            self._elements = Expr_syn_node(operation[1])
            if len(operation[2]) > 1:
                raise ParseException("Can only cast into one dimension array")
        except IndexError:
            self._elements = None

    @property
    def seq_size(self):
        return self._seq_size

    @property
    def constraints(self):
        return self._constraints

    @property
    def target_type(self):
        return self._target_type


class cast_syn_node(object):
    """Syntax node holding cast operation and target"""

    node_type = DATA_TYPE.CAST

    def __init__(self, cast_type, expr):
        self._cast_operation = Cast_type_syn_node(cast_type)
        self._target = Expr_syn_node(expr)

    @property
    def target(self):
        return self._target

    @property
    def cast_operation(self):
        return self._cast_operation


class ID_syn_node(object):
    """Syntax node representing IDs"""

    node_type = DATA_TYPE.ID

    def __init__(self, ID):
        self._ID = ID
        # self._ID_type = None

    @property
    def ID_type(self):
        return self._ID_type

    # @ID_type.setter
    # def ID_type(self, value):
    #     self._ID_type = value

    @property
    def ID(self):
        return self._ID
