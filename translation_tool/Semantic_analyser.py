from Symbol_Table import Symbol_Table
from Stack import Stack
# from IR import IR_Tree, Seq_node, Decl_node, Type_node, Name_node, Literal_node,\
#     Tree
from pyparsing import ParseException
from AST_TYPE import AST_TYPE
from Translator import Translator


class Semantic_analyser(object):

    node_type_lookup = {AST_TYPE.INT_DECL: lambda self, node: self.analyse_int_decl(node),
                        AST_TYPE.BIT_DECL: lambda self, node: self.analyse_bit_decl(node),
                        AST_TYPE.ID_SET: lambda self, node: self.analyse_ID_set(node),
                        AST_TYPE.FUNC_DECL: lambda self, node: self.analyse_func_decl(node),
                        AST_TYPE.IF_STMT: lambda self, node: self.analyse_if_stmt_decl(node),
                        AST_TYPE.FOR_LOOP: lambda self, node: self.analyse_for_loop_decl(node),
                        AST_TYPE.SEQ_INT_DECL: lambda self, node: self.analyse_int_seq(node),
                        AST_TYPE.SEQ_BIT_DECL: lambda self, node: self.analyse_bit_seq(node),
                        AST_TYPE.BS_SEQ_INT_DECL: lambda self, node: self.analyse_int_seq(node),
                        AST_TYPE.BS_INT_DECL: lambda self, node: self.analyse_int_decl(node)}

    def __init__(self):
        self.initialise()

    def initialise(self):
        self._sym_table = Symbol_Table()
        self._translator = Translator()

    @property
    def translator(self):
        return self._translator

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

    def analyse_int_decl(self, node):
        try:
            if node.value is not None:
                if self.value_matches_expected(self.expr_type_is(node.value), node.node_type) is False or self.expr_type_is(node.bit_constraints) != AST_TYPE.INT_VAL:
                    raise ParseException(str(self.expr_type_is(node.value)) + " value not as expected for " + str(node.node_type) + " assignment")
                    return False
            self.sym_table.add_id(node.ID, AST_TYPE.decl_to_value(node.node_type))
            # self.translator.translate_int_decl(node, self.sym_table)
            return True
        except ParseException as details:
            print(details)
            return False

    def analyse_bit_decl(self, node):
        try:
            if node.value is not None:
                if self.expr_type_is(node.value) != AST_TYPE.BIT_VAL:
                    return False
            self.sym_table.add_bit_id(node.ID)
            return True
        except ParseException as details:
            print(details)
            return False

    def analyse_seq_decl(self, node):
        if node.type == AST_TYPE.SEQ_INT_VAL or node.type == AST_TYPE.BS_SEQ_INT_VAL:
            return self.analyse_int_seq(node)
        elif node.type == AST_TYPE.SEQ_BIT_VAL:
            return self.analyse_bit_seq(node)
        else:
            print("Unknown Sequence Type")
            return False

    def analyse_bit_seq(self, node):
        if self.analyse_array_size(node) is True:
            if self.expr_type_is(node.value) != AST_TYPE.SEQ_BIT_VAL:
                return False
        self.sym_table.add_id(node.ID, node.node_type)
        return True

    def analyse_int_seq(self, node):
        if self.analyse_array_size(node) is True:
            try:
                if self.expr_type_is(node.bit_constraints) != AST_TYPE.INT_VAL or self.expr_type_is(node.value) != AST_TYPE.SEQ_INT_VAL:
                    return False
            except AttributeError:
                pass
        self.sym_table.add_id(node.ID, node.node_type)
        # self.translator.translate_int_seq_decl(node, self.sym_table)
        return True

    def seq_type_is(self, seq_value):
        values = []
        for i in seq_value.value:
            # print("CURR SEQUENCE MEMBER:")
            # print(i)
            # print("______")
            curr = self.expr_type_is(i)
            # print("SEQUENCE TYPE")
            # print(curr)
            # print("_____")
            if curr == AST_TYPE.SEQ_VAL:
                values += self.seq_value_type(i)
            else:
                values.append(curr)
        # print("SEQ VAL")
        # print(set(values))
        return set(values)

    def analyse_seq_val_type(self, seq_val):
        seq_type = self.seq_type_is(seq_val)
        seq_val.seq_type = list(seq_type)[0]
        if len(seq_type) > 1:
            raise ParseException("Combined Types in sequence")
        elif list(seq_type)[0] == AST_TYPE.INT_VAL:
            return AST_TYPE.SEQ_INT_VAL
        elif list(seq_type)[0] == AST_TYPE.BIT_VAL:
            return AST_TYPE.SEQ_BIT_VAL
        elif list(seq_type)[0] == AST_TYPE.SEQ_INT_VAL or list(seq_type)[0] == AST_TYPE.SEQ_BIT_VAL:
            return list(seq_type)[0]
        else:
            raise ParseException("Unknown Sequence Type")

    def analyse_array_size(self, node):
        for size_param in node.size:
            if self.expr_type_is(size_param) != AST_TYPE.INT_VAL:
                return False
        return True

    def analyse_ID_set(self, node):
        if self.value_matches_expected(self.expr_type_is(node.value), self.sym_table.id_type(node.ID)) is False:
            raise ParseException(str(self.expr_type_is(node.value)) + " cannot be assigned to variable of type " + str(self.sym_table.id_type(node.ID)))
            return False
        return True

    def expr_type_is(self, expression):
        # print("WHOLE EXPR TO ANAL")
        # print(expression.expressions)
        # print("_______")
        expr_types = {}
        for i, expr in enumerate(expression.expressions):
            # print("CURR OPERAND:")
            # print(expr)
            # print("_______")
            if expr.node_type == AST_TYPE.INT_VAL:
                expr_types["OPERAND_" + str(len(expr_types))] = AST_TYPE.INT_VAL
            elif expr.node_type == AST_TYPE.SEQ_VAL:
                expr_types["OPERAND_" + str(len(expr_types))] = self.analyse_seq_val_type(expr)
            elif expr.node_type == AST_TYPE.BIT_VAL:
                expr_types["OPERAND_" + str(len(expr_types))] = AST_TYPE.BIT_VAL
            elif expr.node_type == AST_TYPE.SHIFT_OP or expr.node_type == AST_TYPE.ARITH_OP or expr.node_type == AST_TYPE.BITWISE_OP or expr.node_type == AST_TYPE.COMP_OP:
                expr_types["OP"] = expr.node_type
            elif expr.node_type == AST_TYPE.EXPR:
                expr.ret_type = self.expr_type_is(expr)
                expr_types["OPERAND_" + str(len(expr_types))] = expr.ret_type
            elif expr.node_type == AST_TYPE.ID:
                expr.ID_type = self.sym_table.id_type(expr.ID)
                expr_types["OPERAND_" + str(len(expr_types))] = expr.ID_type
            elif expr.node_type == AST_TYPE.FUNCTION_CALL:
                expr_types["OPERAND_" + str(len(expr_types))] = self.analyse_func_call(expr)
            if len(expr_types) == 3:
                if self.sub_expr_valid(expr_types) is True:
                    expr_types = self.reduce_sub_expr(expr_types)
                else:
                    raise ParseException("cannot combine a " + str(expr_types['OPERAND_0']) + " value with a " +
                                         str(expr_types['OPERAND_2']) + " in " + str(expr_types['OP']) + " Operation")
        if len(expr_types) != 1:
            print(expr_types)
            raise ParseException("Internal Error")
        # print("RETURNING")
        # print(expr_types["OPERAND_0"])
        # print("____")
        return expr_types["OPERAND_0"]

    def analyse_func_call(self, node):
        for i, p in enumerate(node.parameters):
            if self.value_matches_expected(self.expr_type_is(p), self.sym_table.f_table[node.ID]['parameters'][i].node_type) is False:
                raise ParseException(str(self.expr_type_is(p)) + " does not equal " + str(self.sym_table.f_table[node.ID]['parameters'][i].node_type))
                return False
        return self.sym_table.f_table[node.ID]['return_type']

    def value_matches_expected(self, result_value, expected_value):
        allowed_values = {AST_TYPE.INT_DECL: [AST_TYPE.INT_VAL, AST_TYPE.BS_INT_VAL],
                          AST_TYPE.BIT_DECL: [AST_TYPE.BIT_VAL],
                          AST_TYPE.BS_INT_DECL: [AST_TYPE.INT_VAL, AST_TYPE.BS_INT_VAL],
                          AST_TYPE.BS_INT_VAL: [AST_TYPE.INT_VAL, AST_TYPE.BS_INT_VAL],
                          AST_TYPE.INT_VAL: [AST_TYPE.INT_VAL, AST_TYPE.BS_INT_VAL],
                          AST_TYPE.BIT_VAL: [AST_TYPE.BIT_VAL]}
        if result_value in allowed_values[expected_value]:
            return True
        return False

    def analyse_if_stmt_decl(self, node):
        self.sym_table.add_scope()
        for c in node.condition:
            self.expr_type_is(c)
        for stmt in node.body:
            if Semantic_analyser.node_type_lookup[stmt.node_type](self, stmt) is False:
                    return False
        self.sym_table.leave_scope()
        return True

    def analyse_for_loop_decl(self, node):
        self.sym_table.add_scope()
        for i in node.initializer:
            if Semantic_analyser.node_type_lookup[i.node_type](self, i) is False:
                return False
        for t in node.terminator:
            self.expr_type_is(t)

        for i in node.increment:
            if self.analyse_ID_set(i) is False:
                return False

        for stmt in node.body:
            if Semantic_analyser.node_type_lookup[stmt.node_type](self, stmt) is False:
                return False
        # self.translator.translate_for_loop(node, self.sym_table)
        self.sym_table.leave_scope()
        return True

    def scope(self):
        return self.call_stack.peek()

    def sub_expr_valid(self, expression):
        if expression['OP'] is AST_TYPE.ARITH_OP:
            return self.arith_expr_valid(expression)
        elif expression['OP'] is AST_TYPE.SHIFT_OP:
            return self.shift_expr_valid(expression)
        elif expression['OP'] is AST_TYPE.BITWISE_OP:
            return self.bitwise_expr_valid(expression)
        elif expression['OP'] is AST_TYPE.COMP_OP:
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
        if expression['OPERAND_2'] == AST_TYPE.INT_VAL:
            return True

    def arith_expr_valid(self, expression):

        if self.value_matches_expected(expression['OPERAND_0'], expression['OPERAND_2']):
            return True

    def reduce_sub_expr(self, expression):
        if expression['OP'] is AST_TYPE.ARITH_OP:
            return {'OPERAND_0': self.reduce_arith_op(expression)}
        if expression['OP'] is AST_TYPE.SHIFT_OP:
            return {'OPERAND_0': expression['OPERAND_0']}
        if expression['OP'] is AST_TYPE.BITWISE_OP:
            return {'OPERAND_0': expression['OPERAND_0']}
        if expression['OP'] is AST_TYPE.COMP_OP:
            return {'OPERAND_0': AST_TYPE.BIT_VAL}
        else:
            raise ParseException("Unrecognised operator")

    def reduce_arith_op(self, expression):
        if expression['OPERAND_0'] == AST_TYPE.BS_INT_VAL or expression['OPERAND_2'] == AST_TYPE.BS_INT_VAL:
            return AST_TYPE.BS_INT_VAL
        else:
            return AST_TYPE.INT_VAL

    def analyse_func_decl(self, node):
        self.sym_table.add_scope()
        self.sym_table.add_function(node.ID, node.parameters, node.return_value)
        for s in node.stmts:
            if Semantic_analyser.node_type_lookup[s.node_type](self, s) is False:
                    return False
        self.sym_table.leave_scope()
        return True

    def analyse(self, AST):
        try:
            for node in AST.tree:
                if Semantic_analyser.node_type_lookup[node.node_type](self, node) is False:
                    return False
        except ParseException as details:
            print(details)
            return False
        return True
