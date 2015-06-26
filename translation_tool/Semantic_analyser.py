from Symbol_Table import Symbol_Table
from Stack import Stack
# from IR import IR_Tree, Seq_node, Decl_node, Type_node, Name_node, Literal_node,\
#     Tree
from pyparsing import ParseException
from AST_TYPE import AST_TYPE


class Semantic_analyser(object):

    node_type_lookup = {AST_TYPE.INT_DECL: lambda self, node: self.analyse_int_decl(node),
                        AST_TYPE.BIT_DECL: lambda self, node: self.analyse_bit_decl(node),
                        AST_TYPE.ID_SET: lambda self, node: self.analyse_ID_set(node),
                        AST_TYPE.SEQ_DECL: lambda self, node: self.analyse_seq_decl(node)}

    def __init__(self):
        self.initialise()

    def initialise(self):
        self._sym_table = Symbol_Table()
        self._sym_table.add_scope("global")
        self._call_stack = Stack("global")
        # self._IR = IR_Tree()

    @property
    def IR(self):
        return self._IR

    @property
    def sym_table(self):
        return self._sym_table

    @property
    def call_stack(self):
        return self._call_stack

    # # ToDO: Don't add value to symbol table.  IR needs to be able to cope with expressions.
    # def add_int_decl(self, decl, token):
    #     self.IR.add(Seq_node())
    #     if "constraints" in token:
    #         if "value" in decl:
    #             self.sym_table.add_int_id(self.call_stack.peek(),
    #                                       decl["ID"],
    #                                       str(self.convert_base(decl["value"])),  # NOQA
    #                                       token["constraints"])
    #             self.IR.add(Decl_node(Type_node(token["decl"]),
    #                                   Name_node(decl["ID"][0]),
    #                                   Literal_node(str(self.convert_base(decl["value"]))),  # NOQA
    #                                   Literal_node(token["constraints"])))
    #         else:
    #             self.sym_table.add_int_id(self.call_stack.peek(),
    #                                       decl["ID"],
    #                                       id_constraints=token["constraints"])
    #             self.IR.add(Decl_node(Type_node(token["decl"]),
    #                                   Name_node(decl["ID"][0]),
    #                                   cnst=token["constraints"]))
    #     else:
    #         if "value" in decl:
    #             self.sym_table.add_int_id(self.call_stack.peek(),
    #                                       decl["ID"],
    #                                       id_value=str(self.convert_base(decl["value"])))  # NOQA
    #             self.IR.add(Decl_node(Type_node(token["decl"]),
    #                                   Name_node(decl["ID"][0]),
    #                                   value=Literal_node(str(self.convert_base(decl["value"])))))  # NOQA
    #         else:
    #             self.sym_table.add_int_id(self.call_stack.peek(),
    #                                       decl["ID"])
    #             self.IR.add(Decl_node(Type_node(token["decl"]),
    #                                   Name_node(decl["ID"][0])))

    # def is_declared(self, ID):
    #     """Returns False if ID has not been declared yet"""
    #     if self.sym_table.id_in(self.call_stack.peek(), ID[0]) == True:  # NOQA
    #         return True
    #     else:
    #         return False

    # def analyse_id_set(self, tokens):
    #     print(tokens[0].dump())
    #     if self.is_declared(tokens[0]["target"]) is False:
    #         raise ParseException("Undeclared Symbol")
    #     target_type = self.sym_table.id_type(self.call_stack.peek(), tokens[0]["target"][0])
    #     if "bitwise" in tokens[0]:
    #         if type(tokens[0]['bitwise'][0]) != str:
    #             if self.seq_correct_type(target_type, tokens[0]['bitwise'][0]) is False:
    #                 raise ParseException("Incorrect type assignment")
    #         elif self.type_matches(tokens[0]['type'], tokens[0]['bitwise'][0]) is False:
    #             raise ParseException("Incorrect type assignment")
    #     elif "arith" in tokens[0]:
    #         if target_type != "Int":
    #             raise ParseException("Incorrect type assignment")
    #     elif "seq" in tokens[0]:
    #         if target_type == "Seq":
    #             expected_seq_type = self.sym_table.id_details(self.call_stack.peek(), tokens[0]["target"])['seq_type']
    #             if self.seq_correct_type(expected_seq_type, tokens[0]['seq'][0]) is False:
    #                 raise ParseException("Incorrect type assignment")
    #         else:
    #             raise ParseException("Incorrect type assignment")
    #     elif "bit" in tokens[0]:
    #         print("bit")  # check if token is bit type
    #     return tokens

    # def type_matches(self, expected, test_value):
    #     if expected == "Bit":
    #         if self.is_bit(test_value):
    #             return True
    #     elif expected == "Int":
    #         if self.is_int(test_value):
    #             return True
    #     return False

    # def value_is_correct_type(self, id_type, value):
    #     if id_type is "Bit" and self.is_bit(value) is True:
    #         return True
    #     if id_type is "Int" and self.is_int(value) is True:
    #         return True
    #     return False

    # def is_int(self, value):
    #     '''Checks if value is an int literal or int var'''
    #     try:
    #         # pass
    #         self.convert_base(value)
    #     except ValueError:
    #         if self.sym_table.id_type(self.call_stack.peek(), value) is "Int":
    #             return True
    #         return False
    #     return True

    # def is_bit(self, value):
    #     '''Checks if value is a bit literal or bit var'''
    #     if value == "True" or value == "False":
    #         return True
    #     elif self.sym_table.id_type(self.call_stack.peek(), value) is "Bit":
    #         return True
    #     else:
    #         return False

    # def convert_base(self, val):
    #     if len(val) > 1 and val[1] == 'x':
    #         return int(val, 16)
    #     elif len(val) > 1 and val[1] == 'b':
    #         return int(val, 2)
    #     else:
    #         return int(val)

    def convert_base_to_str(self, tokens):
        return str(self.convert_base(tokens[0]))

    def convert_to_bin_str(self, val):
        if len(val) > 1 and val[1] == 'x':
            return str(int(val, 16)).zfill((len(val) - 2) - len(int(val, 16)) * 4)
        elif len(val) > 1 and val[1] == 'b':
            return str(int(val, 2)).zfill((len(val) - 2) - len(int(val, 2)))
        else:
            return str(int(val)).zfill((len(val)) - len(int(val)))

    # def analyse_constraints(self, value, constraints):
    #     val = self.convert_base(value)
    #     if val.bit_length() > int(constraints):
    #         return False
    #     else:
    #         return True

    # def add_seq_decl(self, token):
    #     # print(token)
    #     if "value" in token:
    #         self.sym_table.add_seq_id(self.call_stack.peek(), token["ID"][0], token["decl"], token["value"][0])
    #     else:
    #         self.sym_table.add_seq_id(self.call_stack.peek(), token["ID"][0], token["decl"])

    # def analyse_seq_decl(self, tokens):
    #     print(tokens[0].dump())
    #     if self.is_declared(tokens[0]["ID"]) is True:
    #         raise ParseException("Duplicate Symbol")
    #     try:
    #         if tokens[0]["decl"]["type"] is "Bit":
    #             if self.is_bit_seq(tokens[0]["value"]) is False:
    #                 raise ParseException("Sequence Value Error")
    #     except KeyError:
    #         pass
    #     self.add_seq_decl(tokens[0])
    #     return tokens

    # def seq_correct_type(self, expected_type, sequence):
    #     for ele in sequence:
    #         if type(ele) == str:
    #             if expected_type == "Bit":
    #                 if self.is_bit(ele) is False:
    #                     return False
    #             elif expected_type == "Int":
    #                 if self.valid_arith_expr(ele) is False:
    #                     return False
    #         else:
    #             if self.seq_correct_type(expected_type, ele) is False:
    #                 return False
    #     return True

    # def is_bit_seq(self, sequence):
    #     for ele in sequence:
    #         if type(ele) == str:
    #             if self.is_bit(ele) is False:
    #                 return False
    #             return True
    #         else:
    #            if self.is_bit_seq(ele) is True:
    #             return True

    # def analyse_bit_decl(self, tokens):
    #     token = tokens[0]
    #     # print(token.dump())
    #     for decl in token["value"]:
    #         if self.is_declared(decl["ID"]) is True:
    #                 raise ParseException("Duplicate Symbol")
    #         self.add_bit_decl(decl)
    #     return tokens

    # def add_bit_decl(self, decl):
    #     if "value" in decl:
    #         self.sym_table.add_id(self.call_stack.peek(),
    #                               decl['ID'][0],
    #                               "Bit",
    #                               decl['value'])
    #     else:
    #         self.sym_table.add_id(self.call_stack.peek(),
    #                               decl['ID'][0],
    #                               "Bit")

    # # Checking for valid integer expressions
    # def valid_arith_expr(self, expr):
    #     if type(expr) == str:
    #         if self.is_int(expr) is True:
    #             return True
    #         elif self.is_bit(expr) is True:
    #             return False
    #         elif self.is_operator(expr):
    #             return True
    #         elif self.sym_table.id_in(self.call_stack.peek(), expr) is True and self.sym_table.id_type(self.call_stack.peek(), expr) is "Int":
    #             return True
    #         else:
    #             return False
    #     if "function_name" in expr:
    #         return True  # For now.  Have to add functions to sym table first.
    #     else:
    #         for operand in expr:
    #             if self.valid_arith_expr(operand) is False:
    #                 return False
    #     return True

    # def analyse_arith_expr(self, tokens):
    #     if(self.valid_arith_expr(tokens[0])) is False:
    #         raise ParseException("Invalid Arithemtic expressions")
    #     return tokens

    # def is_operator(self, token):
    #     if token in "*-/%+":
    #         return True

    # def analyse_int_decl(self, tokens):
    #     token = tokens[0]
    #     # print(token.dump())
    #     for decl in token["values"]:
    #         print(decl.dump())
    #         if "seq_bitwise" in decl:
    #                 raise ParseException("Invalid Int Assignment")
    #         elif "arith" in decl:
    #             pass  # can only do arith with ints: No further semantics needed
    #         if self.is_declared(decl["ID"]) is True:
    #                 raise ParseException("Duplicate Symbol")
    #         self.add_int_decl(decl, token)
    #     print("DONE")
    #     return tokens

    def analyse_int_decl(self, node):
        try:
            if node.value is not None:
                if self.expr_type_is(node.value) != AST_TYPE.INT_VAL or self.expr_type_is(node.bit_constraints) != AST_TYPE.INT_VAL:
                    return False
            self.sym_table.add_int_id(self.scope(), node)
            return True
        except ParseException as details:
            print(details)
            return False

    def analyse_bit_decl(self, node):
        try:
            if node.value is not None:
                if self.expr_type_is(node.value) != AST_TYPE.BIT_VAL:
                    return False
            self.sym_table.add_bit_id(self.scope(), node)
            return True
        except ParseException as details:
            print(details)
            return False

    def analyse_seq_decl(self, node):
        if node.type == "Int":
            return self.analyse_int_seq(node)
        elif node.type == "Bit":
            return self.analyse_bit_seq(node)
        else:
            print("Unknown Sequence Type")
            return False

    def analyse_bit_seq(self, node):
        pass

    def analyse_int_seq(self, node):
        if self.analyse_array_size(node) is True:
            if self.expr_type_is(node.value) != AST_TYPE.SEQ_INT_VAL:
                return False
        self.sym_table.add_id(self.scope(), node.ID, AST_TYPE.SEQ_INT_VAL)
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
        if self.expr_type_is(node.value) != self.sym_table.id_type(self.scope(), node):
            raise ParseException("Incorrect data type assignment")
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
            elif expr.node_type == AST_TYPE.SHIFT_OP or expr.node_type == AST_TYPE.ARITH_OP or expr.node_type == AST_TYPE.BITWISE_OP:
                    expr_types["OP"] = expr.node_type
            elif expr.node_type == AST_TYPE.EXPR:
                expr_types["OPERAND_" + str(len(expr_types))] = self.expr_type_is(expr)
            elif expr.node_type == AST_TYPE.ID:
                expr_types["OPERAND_" + str(len(expr_types))] = self.id_type(expr)
            if len(expr_types) == 3:
                if self.sub_expr_valid(expr_types) is True:
                    expr_types = self.reduce_sub_expr(expr_types)
                else:
                    raise ParseException("Invalid Expression")
        if len(expr_types) != 1:
            print(expr_types)
            raise ParseException("Internal Error")
        # print("RETURNING")
        # print(expr_types["OPERAND_0"])
        # print("____")
        return expr_types["OPERAND_0"]

    def id_type(self, id_node):
        return self.sym_table.id_type(self.scope(), id_node)

    def scope(self):
        return self.call_stack.peek()

    def sub_expr_valid(self, expression):
        if expression['OP'] is AST_TYPE.ARITH_OP:
            return self.arith_expr_valid(expression)
        if expression['OP'] is AST_TYPE.SHIFT_OP:
            return self.shift_expr_valid(expression)
        if expression['OP'] is AST_TYPE.BITWISE_OP:
            return self.bitwise_expr_valid(expression)

    def bitwise_expr_valid(self, expression):
        if expression['OPERAND_0'] == expression['OPERAND_2']:
            return True

    def shift_expr_valid(self, expression):
        if expression['OPERAND_2'] == AST_TYPE.INT_VAL:
            return True

    def arith_expr_valid(self, expression):
        if expression['OPERAND_0'] == AST_TYPE.INT_VAL and expression['OPERAND_2'] == AST_TYPE.INT_VAL:
            return True

    def reduce_sub_expr(self, expression):
        if expression['OP'] is AST_TYPE.ARITH_OP:
            return {'OPERAND_0': AST_TYPE.INT_VAL}
        if expression['OP'] is AST_TYPE.SHIFT_OP:
            return {'OPERAND_0': expression['OPERAND_0']}
        if expression['OP'] is AST_TYPE.BITWISE_OP:
            return {'OPERAND_0': expression['OPERAND_0']}

    def analyse(self, AST):
        try:
            for node in AST.tree:
                if Semantic_analyser.node_type_lookup[node.node_type](self, node) is False:
                    return False
        except ParseException as details:
            print(details)
            return False
        return True
