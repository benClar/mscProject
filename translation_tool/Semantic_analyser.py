from Symbol_Table import Symbol_Table
from Stack import Stack
# from IR import IR_Tree, Seq_node, Decl_node, Type_node, Name_node, Literal_node,\
#     Tree
from pyparsing import ParseException
from DATA_TYPE import DATA_TYPE
from IR import Int_literal, Name, Int_decl, ID_set, Bit_literal, Binary_operation,\
    Cast_operation, Cast, IR, Call, Bit_decl, Seq_decl, Seq_val, If_stmt, For_loop,\
    Function_decl


class Semantic_analyser(object):

    node_type_lookup = {DATA_TYPE.INT_DECL: lambda self, node: self.analyse_int_decl(node),
                        DATA_TYPE.BIT_DECL: lambda self, node: self.analyse_bit_decl(node),
                        DATA_TYPE.ID_SET: lambda self, node: self.analyse_ID_set(node),
                        DATA_TYPE.FUNC_DECL: lambda self, node: self.analyse_func_decl(node),
                        DATA_TYPE.IF_STMT: lambda self, node: self.analyse_if_stmt_decl(node),
                        DATA_TYPE.FOR_LOOP: lambda self, node: self.analyse_for_loop_decl(node),
                        DATA_TYPE.SEQ_INT_DECL: lambda self, node: self.analyse_int_seq(node),
                        DATA_TYPE.SEQ_BIT_DECL: lambda self, node: self.analyse_bit_seq(node),
                        DATA_TYPE.BS_SEQ_INT_DECL: lambda self, node: self.analyse_int_seq(node),
                        DATA_TYPE.BS_INT_DECL: lambda self, node: self.analyse_int_decl(node)}

    def __init__(self):
        self.initialise()

    def initialise(self):
        self._sym_table = Symbol_Table()
        self._IR = IR()

    @property
    def IR(self):
        return self._IR

    @property
    def sym_table(self):
        return self._sym_table

    def convert_base(self, val):
        if len(val) > 1 and val[1] == 'x':
            return int(val, 16)
        elif len(val) > 1 and val[1] == 'b':
            return int(val, 2)
        else:
            return int(val)

    def convert_base_to_str(self, tokens):
        return str(self.convert_base(tokens[0]))

    def convert_to_bin_str(self, val):
        if len(val) > 1 and val[1] == 'x':
            return str(int(val, 16)).zfill((len(val) - 2) - len(int(val, 16)) * 4)
        elif len(val) > 1 and val[1] == 'b':
            return str(int(val, 2)).zfill((len(val) - 2) - len(int(val, 2)))
        else:
            return str(int(val)).zfill((len(val)) - len(int(val)))

    def analyse_ID_set(self, node):
        id_set = ID_set(node.ID, self.expr_type_is(node.value), self.sym_table.id_type(node.ID))
        if self.value_matches_expected(id_set.value.type, id_set.ID.type) is False:
            raise ParseException(str(id_set.value.type) + " cannot be assigned to variable of type " + str(id_set.ID.type))
            return False
        # self.IR.add(id_set)
        return id_set

    def analyse_int_decl(self, node):
        if node.value is not None:
            decl = Int_decl(node.node_type, self.expr_type_is(node.bit_constraints), node.ID, self.expr_type_is(node.value))
        else:
            decl = Int_decl(node.node_type, self.expr_type_is(node.bit_constraints), node.ID)

        try:
            if decl.constraints.value.type == DATA_TYPE.INT_VAL:
                if node.value is not None and self.value_matches_expected(decl.value.type, node.node_type) is False:
                    raise ParseException(str(decl.value.type) + " value not as expected for " + str(node.node_type) + " assignment")
            else:
                raise ParseException("Number of bits must be an int literal")
            self.sym_table.add_id(node.ID, DATA_TYPE.decl_to_value(node.node_type))
            # self.IR.add(decl)
            return decl
        except ParseException as details:
            print(details)
            return False

    def analyse_bit_decl(self, node):
        if node.value is not None:
            decl = Bit_decl(node.ID, self.expr_type_is(node.value))
        else:
            decl = Bit_decl(node.ID)
        try:
            if node.value is not None:
                if decl.value.type != DATA_TYPE.BIT_VAL:
                    return False
            self.sym_table.add_bit_id(node.ID)
            # self.IR.add(decl)
            return decl
        except ParseException as details:
            print(details)
            return False

    def analyse_seq_decl(self, node):
        if node.type == DATA_TYPE.SEQ_INT_VAL or node.type == DATA_TYPE.BS_SEQ_INT_VAL:
            return self.analyse_int_seq(node)
        elif node.type == DATA_TYPE.SEQ_BIT_VAL:
            return self.analyse_bit_seq(node)
        else:
            print("Unknown Sequence Type")
            return False

    def analyse_bit_seq(self, node):
        if node.value is None:
            decl = Seq_decl(node.node_type, self.analyse_array_size(node), node.ID)
        else:
            decl = Seq_decl(node.node_type, self.analyse_array_size(node), node.ID, self.expr_type_is(node.value))
            if decl.value.type != DATA_TYPE.SEQ_BIT_VAL:
                raise ParseException(str(decl.value.type) + " Cannot be assigned to " + str(decl.node_type))
        self.sym_table.add_id(node.ID, decl.ID.type)
        # self.IR.add(decl)
        return decl

    def analyse_int_seq(self, node):
        if node.value is None:
            decl = Seq_decl(node.node_type, self.analyse_array_size(node), node.ID, constraints=self.expr_type_is(node.bit_constraints))
        else:
            decl = Seq_decl(node.node_type, self.analyse_array_size(node), node.ID, self.expr_type_is(node.value), self.expr_type_is(node.bit_constraints))

        if decl.constraints.type != DATA_TYPE.INT_VAL:
            if node.value is not None:
                if decl.value.type != DATA_TYPE.SEQ_INT_VAL or decl.value.type != DATA_TYPE.BS_SEQ_INT_VAL:
                    raise ParseException(str(decl.value.type) + " Cannot be assigned to " + str(decl.node_type))
        self.sym_table.add_id(node.ID, DATA_TYPE.decl_to_value(node.node_type))
        # self.IR.add(decl)
        return decl

    def analyse_array_size(self, node):
        size = []
        for size_param in node.size:
            size.append(self.expr_type_is(size_param))
            if size[-1].type != DATA_TYPE.INT_VAL:
                raise ParseException("Sequence Size Parameter Must be Literal Integers")
        return size

    def seq_type_is(self, seq_value):
        # print("CHECKING NEW SEQ TYPE")
        values = []
        val = Seq_val()
        for i in seq_value.value:
            # print("CURR SEQUENCE MEMBER:")
            # print(i)
            # print("______")
            curr = self.expr_type_is(i)
            val.add_element(curr)
            # print("SEQUENCE TYPE")
            # print(curr)
            # print("_____")
            values.append(curr.type)
        val.type = self.analyse_seq_val_type(list(set(values)))
        return val

    def analyse_seq_val_type(self, seq_val):
        if len(seq_val) > 1:
            raise ParseException("Combined Types in sequence")
        elif seq_val[0] == DATA_TYPE.INT_VAL:
            seq_val = DATA_TYPE.SEQ_INT_VAL
        elif seq_val[0] == DATA_TYPE.BIT_VAL:
            seq_val = DATA_TYPE.SEQ_BIT_VAL
        elif seq_val[0] == DATA_TYPE.SEQ_INT_VAL or seq_val[0] == DATA_TYPE.SEQ_BIT_VAL:
            seq_val = seq_val[0]
        else:
            raise ParseException("Unknown Sequence Type")
        return seq_val

    def expr_type_is(self, expression):
        """Performs Semantic analysis on expression, building IR node"""
        # print("WHOLE EXPR TO ANAL")
        # print(expression.expressions)
        # print("_______")
        expr_types = {}
        IR_expression = []
        for i, expr in enumerate(expression.expressions):
            # print("CURR OPERAND:")
            # print(expr)
            # print("_______")
            if expr.node_type == DATA_TYPE.INT_VAL:
                expr_types["OPERAND_" + str(len(expr_types))] = DATA_TYPE.INT_VAL
                IR_expression.append(Int_literal(expr.value))
            elif expr.node_type == DATA_TYPE.SEQ_VAL:
                IR_expression.append(self.seq_type_is(expr))
                expr_types["OPERAND_" + str(len(expr_types))] = IR_expression[-1].type
            elif expr.node_type == DATA_TYPE.BIT_VAL:
                expr_types["OPERAND_" + str(len(expr_types))] = DATA_TYPE.BIT_VAL
                IR_expression.append(Bit_literal(expr.value))
            elif expr.node_type == DATA_TYPE.SHIFT_OP or expr.node_type == DATA_TYPE.ARITH_OP or expr.node_type == DATA_TYPE.BITWISE_OP or expr.node_type == DATA_TYPE.COMP_OP:  # NOQA
                expr_types["OP"] = expr.node_type
                IR_expression.append(Binary_operation(expr.node_type, expr.operator))
            elif expr.node_type == DATA_TYPE.EXPR:
                IR_expression.append(self.expr_type_is(expr))
                expr_types["OPERAND_" + str(len(expr_types))] = IR_expression[-1].type
            elif expr.node_type == DATA_TYPE.ID:
                IR_expression.append(Name(expr.ID, self.sym_table.id_type(expr.ID)))
                expr_types["OPERAND_" + str(len(expr_types))] = IR_expression[-1].type
            elif expr.node_type == DATA_TYPE.FUNCTION_CALL:
                IR_expression.append(self.analyse_func_call(expr))
                expr_types["OPERAND_" + str(len(expr_types))] = IR_expression[-1].type
            elif expr.node_type == DATA_TYPE.CAST:
                IR_expression.append(self.analyse_cast(expr))
                expr_types["OPERAND_" + str(len(expr_types))] = IR_expression[-1].type
            if len(expr_types) == 3:
                if self.sub_expr_valid(expr_types) is True:
                    expr_types = self.reduce_sub_expr(expr_types)
                    self.clean_up_expr(IR_expression, expr_types)
                else:
                    raise ParseException("cannot combine a " + str(expr_types['OPERAND_0']) + " value with a " +
                                         str(expr_types['OPERAND_2']) + " in " + str(expr_types['OP']) + " Operation")
        if len(IR_expression) != 1:
            print(expr_types)
            raise ParseException("Internal Error")
        return IR_expression[0]

    def clean_up_expr(self, IR_expressions, result_type):
        """Reorders collected expression nodes"""
        left = IR_expressions.pop(0)
        right = IR_expressions.pop(1)
        IR_expressions[0].left = left
        IR_expressions[0].right = right
        IR_expressions[0].type = result_type['OPERAND_0']

    def analyse_cast(self, node):
        cast = Cast(Cast_operation(node.cast_operation.target_type, node.cast_operation.constraints, node.cast_operation.seq_size), self.expr_type_is(node.target))  # NOQA
        return cast

    def analyse_func_call(self, node):
        f_call = Call(node.ID, self.sym_table.f_table[node.ID]['return_type'])
        for i, p in enumerate(node.parameters):
            f_call.add_parameter(self.expr_type_is(p))
            if self.value_matches_expected(f_call.parameters[i].type, self.sym_table.f_table[node.ID]['parameters'][i].node_type) is False:
                raise ParseException(str(self.expr_type_is(p)) + " does not equal " + str(self.sym_table.f_table[node.ID]['parameters'][i].node_type))
                return False
        return f_call

    def value_matches_expected(self, result_value, expected_value):
        """Lookup for allowed assignment types"""
        # Value type -> Allowed to be [ these value types ]
        allowed_values = {DATA_TYPE.INT_DECL: [DATA_TYPE.INT_VAL, DATA_TYPE.BS_INT_VAL],
                          DATA_TYPE.BIT_DECL: [DATA_TYPE.BIT_VAL],
                          DATA_TYPE.BS_INT_DECL: [DATA_TYPE.INT_VAL, DATA_TYPE.BS_INT_VAL],
                          DATA_TYPE.BS_INT_VAL: [DATA_TYPE.INT_VAL, DATA_TYPE.BS_INT_VAL],
                          DATA_TYPE.INT_VAL: [DATA_TYPE.INT_VAL, DATA_TYPE.BS_INT_VAL],
                          DATA_TYPE.BIT_VAL: [DATA_TYPE.BIT_VAL],
                          DATA_TYPE.SEQ_INT_VAL: [DATA_TYPE.SEQ_INT_VAL],
                          DATA_TYPE.SEQ_BIT_VAL: [DATA_TYPE.SEQ_BIT_VAL]}
        if result_value in allowed_values[expected_value]:
            return True
        return False

    def analyse_if_stmt_decl(self, node):
        self.sym_table.add_scope()
        if len(node.condition) > 1:
            raise ParseException("Internal Error: If stmt has more than one condition token")
        if_stmt = If_stmt(self.expr_type_is(node.condition[0]))
        for stmt in node.body:
            if_stmt.add_stmt(self.analyse_sub_stmt(stmt))
        self.sym_table.leave_scope()
        return if_stmt

    def analyse_for_loop_decl(self, node):
        self.sym_table.add_scope()
        for_loop = For_loop()

        for i in node.initializer:
            for_loop.initializer.append(self.analyse_sub_stmt(i))

        for t in node.terminator:
            for_loop.terminator.append(self.expr_type_is(t))

        for i in node.increment:
            for_loop.increment.append(self.analyse_ID_set(i))

        for stmt in node.body:
            for_loop.body.append(self.analyse_sub_stmt(stmt))

        # self.translator.translate_for_loop(node, self.sym_table)
        self.sym_table.leave_scope()
        return for_loop

    def scope(self):
        return self.call_stack.peek()

    def sub_expr_valid(self, expression):
        if expression['OP'] is DATA_TYPE.ARITH_OP:
            return self.arith_expr_valid(expression)
        elif expression['OP'] is DATA_TYPE.SHIFT_OP:
            return self.shift_expr_valid(expression)
        elif expression['OP'] is DATA_TYPE.BITWISE_OP:
            return self.bitwise_expr_valid(expression)
        elif expression['OP'] is DATA_TYPE.COMP_OP:
            return self.comp_expr_valid(expression)
        else:
            raise ParseException("Invalid Operand")

    def comp_expr_valid(self, expression):
        if expression['OPERAND_0'] == expression['OPERAND_2']:
            return True

    def bitwise_expr_valid(self, expression):
        if expression['OPERAND_0'] == expression['OPERAND_2']:
            return True

    def shift_expr_valid(self, expression):
        if expression['OPERAND_2'] == DATA_TYPE.INT_VAL or expression['OPERAND_2'] == DATA_TYPE.BS_INT_VAL:
            return True

    def arith_expr_valid(self, expression):

        if self.value_matches_expected(expression['OPERAND_0'], expression['OPERAND_2']):
            return True

    def reduce_sub_expr(self, expression):
        if expression['OP'] is DATA_TYPE.ARITH_OP:
            return {'OPERAND_0': self.reduce_arith_op(expression)}
        if expression['OP'] is DATA_TYPE.SHIFT_OP:
            return {'OPERAND_0': expression['OPERAND_0']}
        if expression['OP'] is DATA_TYPE.BITWISE_OP:
            return {'OPERAND_0': expression['OPERAND_0']}
        if expression['OP'] is DATA_TYPE.COMP_OP:
            return {'OPERAND_0': DATA_TYPE.BIT_VAL}
        else:
            raise ParseException("Unrecognised operator")

    def reduce_arith_op(self, expression):
        if expression['OPERAND_0'] == DATA_TYPE.BS_INT_VAL or expression['OPERAND_2'] == DATA_TYPE.BS_INT_VAL:
            return DATA_TYPE.BS_INT_VAL
        else:
            return DATA_TYPE.INT_VAL

    def analyse_func_decl(self, node):
        """Performs Semantic Analysis on function declaration and body, creating an IR node if successful"""
        self.sym_table.add_scope()
        func_decl = Function_decl(node.return_value)
        self.sym_table.add_function(node.ID, node.parameters, node.return_value)
        for s in node.stmts:
            func_decl.body.append(self.analyse_sub_stmt(s))
        for p in node.parameters:
            func_decl.parameters.append(self.AST_func_param_to_IR(p))
        self.sym_table.leave_scope()
        return func_decl

    def AST_func_param_to_IR(self, old_decl):
        """Converts AST param node to equivilent IR node"""
        decl = None
        if old_decl.node_type == DATA_TYPE.INT_DECL or old_decl.node_type == DATA_TYPE.BS_INT_DECL:
            decl = Int_decl(old_decl.node_type, self.expr_type_is(old_decl.bit_constraints), old_decl.ID)
        elif old_decl.node_type == DATA_TYPE.SEQ_BIT_DECL:
            decl = Seq_decl(old_decl.node_type, self.analyse_array_size(old_decl), old_decl.ID)
        elif old_decl.node_type == DATA_TYPE.SEQ_INT_VAL or old_decl.node_type == DATA_TYPE.BS_SEQ_INT_VAL:
            decl = Seq_decl(old_decl.node_type, self.analyse_array_size(old_decl), old_decl.ID, constraints=self.expr_type_is(old_decl.bit_constraints))
        elif old_decl.node_type == DATA_TYPE.BIT_DECL:
            decl = Bit_decl(old_decl.ID)
        else:
            raise ParseException("Internal Error: Unknown Parameter Type " + str(old_decl.node_type))
        return decl

    def analyse_sub_stmt(self, node):
        stmt = Semantic_analyser.node_type_lookup[node.node_type](self, node)
        if stmt is False:
            raise ParseException("Error in sub statement")
        return stmt

    def analyse(self, AST):
        try:
            for node in AST.tree:
                result = Semantic_analyser.node_type_lookup[node.node_type](self, node)
                if result is False:
                    return False
                else:
                    self.IR.add(result)
        except ParseException as details:
            print(details)
            return False
        return True
