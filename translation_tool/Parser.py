from pyparsing import Literal, Word, nums, ParseException, Forward, alphas,\
    Suppress, Group, ZeroOrMore, Keyword, alphanums, NotAny, CharsNotIn, \
    OneOrMore, Optional, delimitedList, StringEnd, oneOf, srange, Combine, \
    infixNotation, opAssoc, White, ParserElement
import unittest
from Symbol_Table import Symbol_Table
from Stack import Stack
from IR import IR_Tree, Seq_node, Decl_node, Type_node, Name_node, Literal_node,\
    Tree
ParserElement.enablePackrat()

class Semantic_analyser(object):

    TESTING = 0

    def __init__(self):
        self.initialise()

    def initialise(self):
        self._sym_table = Symbol_Table()
        self._sym_table.add_scope("global")
        self._call_stack = Stack("global")
        self._IR = IR_Tree()
        self.declaration_analysis = {"Int": self.analyse_int_decl}

    @property
    def IR(self):
        return self._IR

    @property
    def sym_table(self):
        return self._sym_table

    @property
    def call_stack(self):
        return self._call_stack

    def is_declared(self, ID):
        """Returns False if ID has not been declared yet"""
        if self.sym_table.id_in(self.call_stack.peek(), ID[0]) == True:  # NOQA
            return True
        else:
            return False

    def analyse_id_set(self, tokens):
        print(tokens[0].dump())
        if self.is_declared(tokens[0]["target"]) is False:
            raise ParseException("Undeclared Symbol")
        target_type = self.sym_table.id_type(self.call_stack.peek(), tokens[0]["target"][0])
        if "bitwise" in tokens[0]:
            if type(tokens[0]['bitwise'][0]) != str:
                if self.seq_correct_type(target_type, tokens[0]['bitwise'][0]) is False:
                    raise ParseException("Incorrect type assignment")
            elif self.type_matches(tokens[0]['type'], tokens[0]['bitwise'][0]) is False:
                raise ParseException("Incorrect type assignment")
        elif "arith" in tokens[0]:
            if target_type != "Int":
                raise ParseException("Incorrect type assignment")
        elif "seq" in tokens[0]:
            if target_type == "Seq":
                expected_seq_type = self.sym_table.id_details(self.call_stack.peek(), tokens[0]["target"])['seq_type']
                if self.seq_correct_type(expected_seq_type, tokens[0]['seq'][0]) is False:
                    raise ParseException("Incorrect type assignment")
            else:
                raise ParseException("Incorrect type assignment")
        elif "bit" in tokens[0]:
            print("bit")  # check if token is bit type
        return tokens

    def type_matches(self, expected, test_value):
        if expected == "Bit":
            if self.is_bit(test_value):
                return True
        elif expected == "Int":
            if self.is_int(test_value):
                return True
        return False

    def value_is_correct_type(self, id_type, value):
        if id_type is "Bit" and self.is_bit(value) is True:
            return True
        if id_type is "Int" and self.is_int(value) is True:
            return True
        return False

    def is_int(self, value):
        '''Checks if value is an int literal or int var'''
        try:
            # pass
            self.convert_base(value)
        except ValueError:
            if self.sym_table.id_type(self.call_stack.peek(), value) is "Int":
                return True
            return False
        return True

    def is_bit(self, value):
        '''Checks if value is a bit literal or bit var'''
        if value == "True" or value == "False":
            return True
        elif self.sym_table.id_type(self.call_stack.peek(), value) is "Bit":
            return True
        else:
            return False

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

    def analyse_constraints(self, value, constraints):
        val = self.convert_base(value)
        if val.bit_length() > int(constraints):
            return False
        else:
            return True

    def add_seq_decl(self, token):
        # print(token)
        if "value" in token:
            self.sym_table.add_seq_id(self.call_stack.peek(), token["ID"][0], token["decl"], token["value"][0])
        else:
            self.sym_table.add_seq_id(self.call_stack.peek(), token["ID"][0], token["decl"])

    def analyse_seq_decl(self, tokens):
        print(tokens[0].dump())
        if self.is_declared(tokens[0]["ID"]) is True:
            raise ParseException("Duplicate Symbol")
        try:
            if tokens[0]["decl"]["type"] is "Bit":
                if self.is_bit_seq(tokens[0]["value"]) is False:
                    raise ParseException("Sequence Value Error")
        except KeyError:
            pass
        self.add_seq_decl(tokens[0])
        return tokens

    def seq_correct_type(self, expected_type, sequence):
        for ele in sequence:
            if type(ele) == str:
                if expected_type == "Bit":
                    if self.is_bit(ele) is False:
                        return False
                elif expected_type == "Int":
                    if self.valid_arith_expr(ele) is False:
                        return False
            else:
                if self.seq_correct_type(expected_type, ele) is False:
                    return False
        return True

    def is_bit_seq(self, sequence):
        for ele in sequence:
            if type(ele) == str:
                if self.is_bit(ele) is False:
                    return False
                return True
            else:
               if self.is_bit_seq(ele) is True:
                return True

    def analyse_bit_decl(self, tokens):
        token = tokens[0]
        # print(token.dump())
        for decl in token["value"]:
            if self.is_declared(decl["ID"]) is True:
                    raise ParseException("Duplicate Symbol")
            self.add_bit_decl(decl)
        return tokens

    def add_bit_decl(self, decl):
        if "value" in decl:
            self.sym_table.add_id(self.call_stack.peek(),
                                  decl['ID'][0],
                                  "Bit",
                                  decl['value'])
        else:
            self.sym_table.add_id(self.call_stack.peek(),
                                  decl['ID'][0],
                                  "Bit")

    # Checking for valid integer expressions
    def valid_arith_expr(self, expr):
        if type(expr) == str:
            if self.is_int(expr) is True:
                return True
            elif self.is_bit(expr) is True:
                return False
            elif self.is_operator(expr):
                return True
            elif self.sym_table.id_in(self.call_stack.peek(), expr) is True and self.sym_table.id_type(self.call_stack.peek(), expr) is "Int":
                return True
            else:
                return False
        if "function_name" in expr:
            return True  # For now.  Have to add functions to sym table first.
        else:
            for operand in expr:
                print("OPERAND:")
                print(operand)
                if self.valid_arith_expr(operand) is False:
                    print("FALSE")
                    return False
        print("TRUE")
        return True

    def analyse_arith_expr(self, tokens):
        if(self.valid_arith_expr(tokens[0])) is False:
            raise ParseException("Invalid Arithemtic expressions")
        return tokens

    def is_operator(self, token):
        if token in "*-/%+":
            return True

    def analyse_int_decl(self, tokens):
        token = tokens[0]
        # print(token.dump())
        for decl in token["values"]:
            print(decl.dump())
            if "seq_bitwise" in decl:
                    raise ParseException("Invalid Int Assignment")
            elif "arith" in decl:
                pass  # can only do arith with ints: No further semantics needed
            if self.is_declared(decl["ID"]) is True:
                    raise ParseException("Duplicate Symbol")
            self.add_int_decl(decl, token)
        print("DONE")
        return tokens

    def test_print(self, tokens):
        print("TEST PRINT")
        print(tokens.dump())

    # ToDO: Don't add value to symbol table.  IR needs to be able to cope with expressions.
    def add_int_decl(self, decl, token):
        self.IR.add(Seq_node())
        if "constraints" in token:
            if "value" in decl:
                self.sym_table.add_int_id(self.call_stack.peek(),
                                          decl["ID"],
                                          str(self.convert_base(decl["value"])),  # NOQA
                                          token["constraints"])
                self.IR.add(Decl_node(Type_node(token["decl"]),
                                      Name_node(decl["ID"][0]),
                                      Literal_node(str(self.convert_base(decl["value"]))),  # NOQA
                                      Literal_node(token["constraints"])))
            else:
                self.sym_table.add_int_id(self.call_stack.peek(),
                                          decl["ID"],
                                          id_constraints=token["constraints"])
                self.IR.add(Decl_node(Type_node(token["decl"]),
                                      Name_node(decl["ID"][0]),
                                      cnst=token["constraints"]))
        else:
            if "value" in decl:
                self.sym_table.add_int_id(self.call_stack.peek(),
                                          decl["ID"],
                                          id_value=str(self.convert_base(decl["value"])))  # NOQA
                self.IR.add(Decl_node(Type_node(token["decl"]),
                                      Name_node(decl["ID"][0]),
                                      value=Literal_node(str(self.convert_base(decl["value"])))))  # NOQA
            else:
                self.sym_table.add_int_id(self.call_stack.peek(),
                                          decl["ID"])
                self.IR.add(Decl_node(Type_node(token["decl"]),
                                      Name_node(decl["ID"][0])))


class Parser(object):

    def __init__(self):
        self.semantic_analyser = Semantic_analyser()

        # keywords
        self.int_ = Keyword('Int')
        self.false_ = Keyword('False')
        self.true_ = Keyword('True')
        self.bit_ = Keyword('Bit')
        self.sbox_ = Keyword('sbox')
        self.l_shift_ = Keyword('<<')
        self.r_shift_ = Keyword('>>')
        self.circ_l_shift_ = Keyword('<<<')
        self.circ_r_shift_ = Keyword('>>>')
        self.bit_val = self.false_ ^ self.true_
        self.if_ = Keyword('if')
        self.for_ = Keyword('for')
        self.return_ = Keyword('return')
        self.ID = NotAny(self.int_ ^ self.bit_ ^ self.false_ ^ self.true_ ^ self.if_ ^ self.for_ ^ self.sbox_) + Word(alphas + '_', alphanums + '_')  # NOQA
        # Other Tokens
        self.l_bracket = Literal('(')
        self.r_bracket = Literal(')')
        self.eq_set = Literal('=')("set")
        self.term_st = Literal(';')
        self.b_2_num = Combine(Literal("0b") + Word("01"))
        self.b_2_num.setParseAction(self.semantic_analyser.convert_base_to_str)
        self.b_16_num = Combine(Literal("0x") + Word(srange("[0-9a-fA-F]")))
        self.b_16_num.setParseAction(self.semantic_analyser.convert_base_to_str)
        self.b_10_num = Word(nums)
        self.bit_and = Literal('&')
        self.bit_or = Literal('|')
        self.bit_xor = Literal('^')
        self.bit_not = Literal('~')
        self.eq_compare = Literal('==')
        self.l_brace = Literal('{')
        self.r_brace = Literal('}')
        self.bin_add = Literal('+')
        self.bin_mult = Literal('*')
        self.bin_sub = Literal('-')
        self.bin_mod = Literal('%')
        self.bin_div = Literal('/')
        self.g_than = Literal('>')
        self.ge_than = Literal('>=')
        self.l_than = Literal('<')
        self.le_than = Literal('<=')
        self.log_and = Keyword('&&')
        self.log_or = Keyword('||')
        self.l_sq_b = Literal('[')
        self.r_sq_b = Literal(']')

        # Operator Productions
        self.log_op = self.log_and ^ self.log_or
        self.comparison_op = self.g_than ^ self.ge_than ^ self.l_than ^ self.le_than ^ self.eq_compare
        self.arith_op = self.bin_add ^ self.bin_mult ^ self.bin_sub ^ self.bin_mod ^ self.bin_div
        self.bitwise_op = self.bit_and ^ self.bit_or ^ self.bit_xor ^ self.bit_not ^ self.l_shift_ ^ self.r_shift_ ^ self.circ_l_shift_ ^ self.circ_r_shift_

        # Grammar
        self.stmt = Forward()
        self.for_loop = Forward()
        self.cast = Forward()
        self.seq_val = Forward()
        self.int_value = self.b_2_num ^ self.b_16_num ^ self.b_10_num
        self.expr = Forward()
        self.function_call = Forward()
        self.seq_index_select = Forward()
        self.seq_ = Forward()
        self.operand = Forward()
        #  #######Operands

        self.sbox_call = Group((self.ID ^ self.seq_val) + ~White() + Literal(".") + ~White() + self.sbox_ + ~White() +
                               self.l_bracket + (self.ID ^ self.int_value) + self.r_bracket)

        self.cast << Group(Suppress(self.l_bracket) + (self.int_ ^ self.bit_ ^ self.seq_)("dest_type") +
                           Suppress(self.r_bracket) + (self.expr ^ self.seq_val)("target"))

        self.operand = self.seq_index_select | self.seq_val | self.function_call | self.ID | self.int_value | self.cast | self.bit_val

        #  #######Expressions

        # self.bitwise_expr << infixNotation(infixNotation(self.arith_expr ^ self.seq_val,
        #                                                  [(self.bitwise_op, 2, opAssoc.LEFT), ]),
        #                                    [(self.arith_op, 2, opAssoc.LEFT), ])

        # self.arith_expr << infixNotation(self.arith_operand, [(self.arith_op, 2, opAssoc.LEFT), ])

        # self.comparison_expr = infixNotation(infixNotation(self.arith_expr | self.bitwise_expr | self.seq_val,
        #                                                    [(self.comparison_op, 2, opAssoc.LEFT), ]),
        #                                      [(self.log_op, 2, opAssoc.LEFT), ])

        # self.bitwise_expr = infixNotation(self.expr, [(self.bitwise_op, 2, opAssoc.LEFT), ])

        # self.expr = self.arith_expr | self.bitwise_expr | self.seq_val("seq") | self.bit_val("bit")

        self.expr = infixNotation(self.operand, [(self.bitwise_op, 2, opAssoc.LEFT),
                                                 (self.comparison_op, 2, opAssoc.LEFT),
                                                 (self.log_op, 2, opAssoc.LEFT),
                                                 (self.arith_op, 2, opAssoc.LEFT)])

        self.seq_range = Group((self.expr) + Literal(":") + (self.expr))

        self.seq_index_select << self.ID("ID") + ~White() +\
            Suppress(self.l_sq_b) + delimitedList(self.expr ^ self.seq_range)("index") + Suppress(self.r_sq_b)

        self.seq_val << Group((Suppress(self.l_sq_b) + (delimitedList(self.expr)) +
                               Suppress(self.r_sq_b)))

        self.seq_ << (self.int_ ^ self.bit_)("type") +\
            Group(OneOrMore(~White() + Suppress(self.l_sq_b) + (self.expr) + Suppress(self.r_sq_b)))("seq_size")

        self.function_call << Group(self.ID("function_name") + ~White() + Suppress(self.l_bracket) +
                                    delimitedList(self.expr)("param_list") + Suppress(self.r_bracket))

        #  ####### Declarations

        self.id_set = Group((self.seq_index_select | self.ID)("target") + self.eq_set +
                            (self.expr))

        self.int_decl = Group(self.int_("decl") + ~White() + Suppress(self.l_bracket) + self.expr("constraints") + Suppress(self.r_bracket) +
                              delimitedList(Group((self.ID("ID") + self.eq_set + self.expr) |
                              self.ID("ID")))("values"))  # NOQA

        self.bit_decl = Group(self.bit_("decl") + delimitedList(Group(self.ID("ID")) ^ Group(self.ID("ID") + self.eq_set + self.bit_val("value")))("value"))

        self.seq_decl = Group(self.seq_("decl") + self.ID("ID") + Optional(self.eq_set + (self.seq_val("value") ^ self.seq_index_select)))

        self.decl = self.bit_decl | self.int_decl | self.seq_decl

        # ###### Statements

        self.return_stmt = Group(self.return_ + self.expr ^ self.seq_val ^ self.bit_val)

        self.function_decl = Group((self.int_ ^ self.bit_ ^ self.seq_)("return_type") + self.ID +
                                   Suppress(self.l_bracket) + Group(delimitedList((self.seq_ ^ self.int_ ^ self.bit_) + self.ID))("func_param") +
                                   Suppress(self.r_bracket) + Suppress(self.l_brace) + Group(self.stmt)("body") + Suppress(self.r_brace))

        self.for_loop << Group(self.for_ + self.l_bracket + Optional(delimitedList(self.decl ^ self.id_set)) + self.term_st +
                               Optional(self.expr) + self.term_st +
                               Optional(delimitedList(self.expr ^ self.id_set)) + self.r_bracket +
                               self.l_brace + self.stmt + self.r_brace)

        self.if_stmt = Group(self.if_ + self.l_bracket + self.expr + self.r_bracket + self.l_brace + self.stmt + self.r_brace)

        self.stmt << ZeroOrMore(self.decl + Suppress(self.term_st)
                                | self.id_set + Suppress(self.term_st)
                                | self.expr + Suppress(self.term_st)
                                | self.seq_val + Suppress(self.term_st)
                                | self.for_loop
                                | self.if_stmt
                                | self.return_stmt + Suppress(self.term_st)
                                | self.sbox_call + Suppress(self.term_st))

        self.grammar_test = self.stmt + StringEnd()  # Allows single statements to be parsed

        self.grammar = self.function_decl + StringEnd()

        # Semantics
        # self.seq_decl.setParseAction(self.semantic_analyser.analyse_seq_decl)
        # self.bit_decl.setParseAction(self.semantic_analyser.analyse_bit_decl)
        # self.int_decl.setParseAction(self.semantic_analyser.analyse_int_decl)
        # self.arith_expr.setParseAction(self.semantic_analyser.analyse_arith_expr)
        # self.id_set.setParseAction(self.semantic_analyser.analyse_id_set)

    def parse_test_unit(self, data_in):
        """Parses single statements"""
        try:
            res = self.grammar_test.parseString(data_in)
        except ParseException as details:
            print("The following error occured:")
            print(details)
            return False
        if type(res[0]) is not bool:
            pass
            # print(res[0].dump())
        return [res, True]

    def parse_test_integration(self, data_in):
        """Only Parses Statements in functions"""
        try:
            res = self.grammar.parseString(data_in)
        except ParseException as details:
            print("The following error occured:")
            print(details)
            return False
        if type(res[0]) is not bool:
            print(res[0].dump())
        return [res, True]

    def parse(self, data_in):
        return self.grammar.parseString(data_in)


class TestParser(unittest.TestCase):

    # Working With Semantics

    def test_int_decl_parsing(self):
        par = Parser()
        self.assertEqual(par.parse_test_unit("Int(10) varName;")[1], True)
        self.assertEqual(par.parse_test_unit("Int(123) ee;")[1], True)
        self.assertEqual(par.parse_test_unit("Int(123) ff"), False)
        self.assertEqual(par.parse_test_unit("Int()"), False)
        self.assertEqual(par.parse_test_unit("Int(1) ;"), False)
        self.assertEqual(par.parse_test_unit("Int(1) test"), False)
        self.assertEqual(par.parse_test_unit("Int"), False)
        self.assertEqual(par.parse_test_unit("Int(123) gg,jj,test2;")[1], True)
        self.assertEqual(par.parse_test_unit("Int Int;"), False)
        self.assertEqual(par.parse_test_unit("Int(10) Integer;")[1], True)
        self.assertEqual(par.parse_test_unit("Int(10) kk; Int(20) \
            ll;")[1], True)
        self.assertEqual(par.parse_test_unit("Int(10) mm, nn, oo, pp;")[1], True)
        self.assertEqual(par.parse_test_unit("Int(10) qq = 10, rr = 4, ss = 5, tt = \
            7;")[1], True)
        self.assertEqual(par.parse_test_unit("Int(10) uu = 10, j, k = 5,\
            d;")[1], True)
        self.assertEqual(par.parse_test_unit("Int(10) l = 10, m, n = 5, \
         h;")[1], True)
        self.assertEqual(par.parse_test_unit("Int(10) o = 10, p, q = 5, \
         h"), False)
        self.assertEqual(par.parse_test_unit("Int(10) r1 = 10, s1, t1 = 5, u1; Int(10) v1, w1=10, \
            ll1;")[1], True)
        self.assertEqual(par.parse_test_unit("Int(10) dd = 10;")[1], True)
        self.assertEqual(par.parse_test_unit("Int (123) zz;"), False)

    def test_bit_decl_parsing(self):
        par = Parser()
        self.assertEqual(par.parse_test_unit("Bit a = True;")[1], True)
        self.assertEqual(par.parse_test_unit("Bit b, c, d = True;")[1], True)
        self.assertEqual(par.parse_test_unit("Bit Bit, c, d = True;"), False)

    def test_set_parsing(self):
        par = Parser()
        par.parse_test_unit("Int b;")
        par.parse_test_unit("Bit d, e;")
        self.assertEqual(par.parse_test_unit("b = 2;")[1], True)
        self.assertEqual(par.parse_test_unit("Int = 2;"), False)
        self.assertEqual(par.parse_test_unit("d = False;")[1], True)
        self.assertEqual(par.parse_test_unit("e = True;")[1], True)
        self.assertEqual(par.parse_test_unit("e = True True;"), False)

    def test_expr_parsing(self):
        par = Parser()
        par.parse_test_unit("Int(10) a, b, c, d, e, r; Bit ff;")
        self.assertEqual(par.parse_test_unit("((a > 4) && (b > 5)) || d > 3 || (3 << 3);")[1], True)
        self.assertEqual(par.parse_test_unit("[[1,2,3,4],[1,2,3,4]] << 3;")[1], True)
        self.assertEqual(par.parse_test_unit("a + b;")[1], True)
        self.assertEqual(par.parse_test_unit("a + c + d + e;")[1], True)
        self.assertEqual(par.parse_test_unit("a + (c + d) + e;")[1], True)
        self.assertEqual(par.parse_test_unit("a + c + d + + e;"), False)
        self.assertEqual(par.parse_test_unit("a + c + 4 - e;")[1], True)
        self.assertEqual(par.parse_test_unit("a + (c) + 4 - e;")[1], True)
        self.assertEqual(par.parse_test_unit("a + (c + 4) - (e + r);")[1], True)
        self.assertEqual(par.parse_test_unit("a + ((c + d) + 4) - (e + r);")[1], True)
        self.assertEqual(par.parse_test_unit("[1,2,3,4] << 2;")[1], True)
        self.assertEqual(par.parse_test_unit("([1,2,3,4] << 2) << c;")[1], True)
        self.assertEqual(par.parse_test_unit("a;")[1], True)
        self.assertEqual(par.parse_test_unit("1;")[1], True)
        self.assertEqual(par.parse_test_unit("True;")[1], True)
        self.assertEqual(par.parse_test_unit("False;")[1], True)

    def test_if_parsing(self):
        par = Parser()
        par.parse_test_unit("Int a, b, d, e, g;")
        self.assertEqual(par.parse_test_unit("if(a==1) { }")[1], True)  # NOQA

    def test_seq_decl_parsing(self):
        par = Parser()
        self.assertEqual(par.parse_test_unit("[[1,2,3,4,5]];")[1], True)
        self.assertEqual(par.parse_test_unit("[5*5, function(1,2,3), 4];")[1], True)
        self.assertEqual(par.parse_test_unit("[True,False,True,False,True];")[1], True)
        self.assertEqual(par.parse_test_unit("[[True,False,True,False,True],[True,False,True,False,True],[True,False,True,False,True]];")[1], True)
        self.assertEqual(par.parse_test_unit("Int[4] a;")[1], True)
        self.assertEqual(par.parse_test_unit("Bit[4] b;")[1], True)
        self.assertEqual(par.parse_test_unit("Bit[4][4] c;")[1], True)
        self.assertEqual(par.parse_test_unit("Bit[4][4][4] d;")[1], True)
        self.assertEqual(par.parse_test_unit("Bit[4][4] [4] e;"), False)
        self.assertEqual(par.parse_test_unit("Bit [4][4] f;"), False)
        self.assertEqual(par.parse_test_unit("Bit[4][4] 1;"), False)
        self.assertEqual(par.parse_test_unit("Bit[1][4] f = [[True,False,True,True]];")[1], True)
        self.assertEqual(par.parse_test_unit("Int[3] g = [5*5, function(1,2,3), 4];")[1], True)

    def test_seq_op_parsing(self):
        par = Parser()
        self.assertEqual(par.parse_test_unit("Int[6] b = a[5,6,7,8:10];")[1], True)
        self.assertEqual(par.parse_test_unit("Int a[5,6,7,8:10];"), False)
        self.assertEqual(par.parse_test_unit("a[5,6,7-8:10];")[1], True)
        self.assertEqual(par.parse_test_unit("a[5,6,7,8:10]; b[5,6,7,8:10];")[1], True)
        self.assertEqual(par.parse_test_unit("a[5,6,7,8:10] = [1,2,3,4,5,6];")[1], True)
        self.assertEqual(par.parse_test_unit("a[5] = 10;")[1], True)
        self.assertEqual(par.parse_test_unit("a[5] + a[5];")[1], True)

    def test_for_parsing(self):
        par = Parser()
        par.parse_test_unit("Int b, d, e, g;")
        par.parse_test_unit("Int[4] l;")
        self.assertEqual(par.parse_test_unit("for(Int(10) a = 2; ((a > 4) && (b > 5)) || d > 3; d = 5, d = (e * g))\
            {\
                a = 1;\
            }")[1], True)
        self.assertEqual(par.parse_test_unit("for(Int(10) a = 2; ((a > 4) && (b > 5)) || d > 3; d = 5, d = (e * g))\
            { \
                for(d = 3; d < 5; d = d + 1) {\
                    a = 1;\
                }\
            }")[1], True)  # NOQA
        self.assertEqual(par.parse_test_unit("for(;a < 4;){}")[1], True)
        self.assertEqual(par.parse_test_unit("for(l[4] = 6 ;a < 4;){}")[1], True)
        self.assertEqual(par.parse_test_unit("for(;;){}")[1], True)

    def test_function_call_parsing(self):
        par = Parser()
        par.parse_test_unit("Int a, b, e;")
        self.assertEqual(par.parse_test_unit("func(a, b, 10, 40);")[1], True)
        self.assertEqual(par.parse_test_unit("func(a, b, Int[10] a, 40);"), False)
        self.assertEqual(par.parse_test_unit("func(a, b, [1,0,1,1], 40);")[1], True)
        self.assertEqual(par.parse_test_unit("func (a, b, [1,0,1,1], 40);"), False)
        self.assertEqual(par.parse_test_unit("func(a, b, 5 * 3, e * 6);")[1], True)
        self.assertEqual(par.parse_test_unit("func(a, b, 5 * 3, e * 6, func(3));")[1], True)
        self.assertEqual(par.parse_test_unit("func(1,2,3,4)"), False)
        self.assertEqual(par.parse_test_unit("func(1,2,3,4);")[1], True)

    def sbox_call_parsing(self):
        par = Parser()
        par.parse_test_unit("Int a;")
        self.assertEqual(par.parse_test_unit("a.sbox(1);")[1], True)
        self.assertEqual(par.parse_test_unit("a.sbox(1 * 1);")[1], True)
        self.assertEqual(par.parse_test_unit("a.sbox(a);")[1], True)
        self.assertEqual(par.parse_test_unit("a. sbox(a);"), False)
        self.assertEqual(par.parse_test_unit("a .sbox(a);"), False)
        self.assertEqual(par.parse_test_unit("a.sbo x(a);"), False)
        self.assertEqual(par.parse_test_unit("a.sbox (a);"), False)

    def test_shift_op_parsing(self):
        par = Parser()
        par.parse_test_unit("Int a;")
        self.assertEqual(par.parse_test_unit("a << 3;")[1], True)
        self.assertEqual(par.parse_test_unit("a >> 3;")[1], True)
        self.assertEqual(par.parse_test_unit("a <<< 3;")[1], True)
        self.assertEqual(par.parse_test_unit("a >>> 3;")[1], True)
        self.assertEqual(par.parse_test_unit("10 >> 4;")[1], True)
        self.assertEqual(par.parse_test_unit("10 >> 4; a >> 4;")[1], True)
        self.assertEqual(par.parse_test_unit("([1,2,3,4] >> 4) >> 2 * 4;")[1], True)
        self.assertEqual(par.parse_test_unit("(5 >> 4) >> 2 * 4;")[1], True)

    # def test_using_expr_parsing(self):
    #     par = Parser()
    #     self.assertEqual(par.parse_test_unit("Int a = (5 * 10) + 3 + (3 * 2);")[1], True)

    # def test_int_decl_semantics(self):
    #     sem_a = Semantic_analyser()
    #     par = Parser()
        # self.assertEqual(sem_a.analyse_constraints("10", "2"), False)
        # self.assertEqual(sem_a.analyse_constraints(
        #                  "999999999999999999999999999999999999999999999999999999999999"  # NOQA
        #                  "999999999999999999999999999999", "2"), False)
        # par.parse_test_unit("Int zz = 10;")
        # par.parse_test_unit("Bit yy = True;")
        # self.assertEqual(par.parse_test_unit("Int aa = 10;")[1], True)  # NOQA
        # self.assertEqual(par.parse_test_unit("Int a = 4 * zz + (5 * (5 * zz)), kk = 5 * ( 4 / (2 *2));")[1], True)
        # self.assertEqual(par.parse_test_unit("Int j = 4 * zz + (5 * (5 * k)),  l = 5 * ( 4 / (2 * 2));"), False)
        # print(par.parse_test_unit("Int j = 4 * zz + (5 * (5 * k));")[0][0]['values'].dump())
        # self.assertEqual(par.parse_test_unit("Int a = 4 * zz + (5 * (5 * zz)), m = yy * ( 4 / (2 *2));"), False)
        # self.assertEqual(par.parse_test_unit("Int d = 10, b = 10, c = 20;")[1], True)  # NOQA
        # # self.assertEqual(par.parse_test_unit("Int(3) e = 10, f = 10, g = 20;"), False)  # NOQA
        # self.assertEqual(par.parse_test_unit("Int(4) h = 10, h = 10, i = 20;"), False)  # NOQA
        # self.assertEqual(par.parse_test_unit("Int(4) z = 10;")[1], True)
        # self.assertEqual(par.parse_test_unit("Int(4) z = 10;"), False)
        # self.assertEqual(par.parse_test_unit("Int(4) k;")[1], True)
        # self.assertEqual(par.parse_test_unit("Int(4) k;"), False)
        # self.assertEqual(par.parse_test_unit("Int bb = [1,2,3,4] << [4 * 4 * 3 * 4];"), False)  # NOQA
        # self.assertEqual(par.parse_test_unit("Int cc = [1,2,3,4] << 3;"), False)  # NOQA
        # self.assertEqual(par.parse_test_unit("Int dd = (3 << 3) + (3 << 3);")[1], True)  # NOQA
        # self.assertEqual(par.parse_test_unit("Int ee = 4 << 3;")[1], True)  # NOQA
        # self.assertEqual(par.parse_test_unit("Int ff = (4 * 4 * 2 * 3) << 3;")[1], True)  # NOQA

    # def test_id_set_semantics(self):
    #     par = Parser()
    #     par.parse_test_unit("Int a, b, c;")
    #     self.assertEqual(par.semantic_analyser.value_is_correct_type("Int", "30"), True)
    #     self.assertEqual(par.semantic_analyser.value_is_correct_type("Int", "False"), False)
    #     self.assertEqual(par.parse_test_unit("a = b * c * ((4 + 4) - 4);")[1], True)
    #     self.assertEqual(par.parse_test_unit("a = [3,4,2,1] << 3;"), False)


    # def test_arith_expr_semantics(self):
    #     par = Parser()
    #     self.assertEqual(par.parse_test_unit("Int a, b, c;")[1], True)
    #     self.assertEqual(par.parse_test_unit("e = False;"), False)
    #     self.assertEqual(par.parse_test_unit("Bit e = False;")[1], True)
    #     self.assertEqual(par.parse_test_unit("e = True;")[1], True)
    #     self.assertEqual(par.parse_test_unit("(a + 3) * b / c;")[1], True)
    #     self.assertEqual(par.parse_test_unit("b = (a + 3) * b / c;")[1], True)
    #     self.assertEqual(par.parse_test_unit("b = (a + 3) * b / d;"), False)
    #     self.assertEqual(par.parse_test_unit("c = (a + False) * b / d;"), False)
    #     self.assertEqual(par.parse_test_unit("c = (a + e) * b / d;"), False)

    # def test_add_to_symbol_table(self):
    #     sem_a = Semantic_analyser()
    #     sem_a.sym_table.add_int_id("global", "A", "10", "5")
    #     sem_a.sym_table.add_int_id("global", "B", id_constraints="9")
    #     sem_a.sym_table.add_int_id("global", "D", id_value="4")
    #     self.assertEqual(sem_a.sym_table.id_in("global", "A"), True)
    #     self.assertEqual(sem_a.sym_table.id_in("global", "B"), True)
    #     self.assertEqual(sem_a.sym_table.id_in("global", "C"), False)
    #     self.assertEqual(sem_a.sym_table.id_in("global", "D"), True)

    # def test_decl_bit_semantics(self):
    #     par = Parser()
    #     self.assertEqual(par.parse_test_unit("Bit d, e, l = True;")[1], True)
    #     self.assertEqual(par.semantic_analyser.sym_table.table["global"]["d"]["type"], "Bit")
    #     self.assertEqual(par.semantic_analyser.sym_table.table["global"]["d"]["value"], None)
    #     self.assertEqual(par.semantic_analyser.sym_table.table["global"]["l"]["value"], "True")

    # def test_int_bases_semantics(self):
    #     par = Parser()
    #     par.parse_test_unit("Int a, b, c")
    #     self.assertEqual(par.parse_test_unit("a = 0b010101010;")[1], True)
    #     self.assertEqual(par.parse_test_unit("b = 0x345;")[1], True)
    #     self.assertEqual(par.parse_test_unit("c = 0x3b;")[1], True)
    #     self.assertEqual(par.parse_test_unit("b = 0x3D45ef3456a;")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int d = 0x3aab;")[1], True)

    # def test_conv(self):
    #     par = Parser()
    #     sem_a = Semantic_analyser()
    #     self.assertEqual(str(sem_a.convert_base("0b0010")), "2")
    #     self.assertEqual(str(sem_a.convert_base("0x000a")), "10")
    #     self.assertEqual(par.parse_test_unit("0b0010;")[0][0], "2")
    #     self.assertEqual(par.parse_test_unit("Int a = 0b0010;")[0][0]['values'][0]['set_expr'], "2")
    #     self.assertEqual(par.parse_test_unit("Int c = 0b0010, b = 0b0100;")[0][0]['values'][1]['set_expr'], "4")
    #     self.assertEqual(par.parse_test_unit("Int d = 0x000a, e = 0x000a;")[0][0]['values'][1]['set_expr'], "10")

    # def test_seq_decl_semantics(self):
    #     par = Parser()
    #     self.assertEqual(par.parse_test_unit("Int[4] a;")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int[4] b = [2,3,4,5];")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int[2][3] c = [[1,2],[3,4]];")[1], True)
    #     self.assertEqual(par.semantic_analyser.sym_table.id_type("global", "a"), "Seq")
    #     self.assertEqual(par.semantic_analyser.sym_table.table["global"]["a"]["seq_type"], "Int")
    #     self.assertEqual(par.semantic_analyser.sym_table.table["global"]["a"]["seq_type"], "Int")
    #     self.assertEqual(par.semantic_analyser.sym_table.table["global"]["a"]["dimension"][0], "4")
    #     self.assertEqual(len(par.semantic_analyser.sym_table.table["global"]["a"]["dimension"][0]), 1)
    #     self.assertEqual(par.semantic_analyser.sym_table.table["global"]["c"]["dimension"][0], "2")
    #     self.assertEqual(par.semantic_analyser.sym_table.table["global"]["c"]["dimension"][1], "3")
    #     self.assertEqual(len(par.semantic_analyser.sym_table.table["global"]["c"]["dimension"]), 2)
    #     self.assertEqual(par.parse_test_unit("Int[2][2] d = [[1,2],[3,4]];")[1], True)
    #     self.assertEqual(len(par.semantic_analyser.sym_table.table["global"]["d"]["dimension"]), 2)
    #     self.assertEqual(par.parse_test_unit("Int[4] e = [[2 * 2],1,1,1];")[1], True)

    # def test_shift_op_semantics(self):
    #     par = Parser()
    #     self.assertEqual(par.parse_test_unit("Int a; Int[4] b;")[1], True)
    #     self.assertEqual(par.parse_test_unit("a = a << ((4 * 5) << 5);")[1], True)
    #     self.assertEqual(par.parse_test_unit("b = [0,0,1,0] << ((4 * 5) << 5);")[1], True)
    #     print(par.parse_test_unit("a = ([0,0,1,0] << ((4 * 5) << (5 << (6 << 7))));")[0].dump())
    #     self.assertEqual(par.parse_test_unit("a = [[0,0,1,0],[0,0,1,0]] << (4 * 5) << 5 << 6 << 7;"), False)

    # def test_type_matches_semantics(self):
    #     par = Parser()
    #     par.parse_test_unit("Int a, b; Bit c;")
    #     self.assertEqual(par.semantic_analyser.value_is_correct_type("Int", "a"), True)
    #     self.assertEqual(par.semantic_analyser.value_is_correct_type("Bit", "c"), True)

    # def test_sequence_type_check(self):
    #     par = Parser()
    #     self.assertEqual(par.semantic_analyser.seq_correct_type("Bit", ["True", "False", "True", "False"]), True)
    #     self.assertEqual(par.semantic_analyser.seq_correct_type("Bit", [["True", "False", "True", "False"],
    #                                                             ["True", "False", "True", "False"],
    #                                                             ["True", "False", "True", "False"]]), True)
    #     self.assertEqual(par.semantic_analyser.seq_correct_type("Bit", [["True", "100", "True", "False"],
    #                                                             ["True", "False", "True", "False"],
    #                                                             ["True", "False", "True", "False"]]), False)
    #     self.assertEqual(par.semantic_analyser.seq_correct_type("Int", [["10", "100", "20", "30"],
    #                                                             ["10", "100", "20", "30"],
    #                                                             ["10", "100", "20", "30"]]), True)
    #     self.assertEqual(par.semantic_analyser.seq_correct_type("Int", [["10", "100", "20", "30"],
    #                                                             ["True", "100", "True", "False"],
    #                                                             ["10", "100", "20", "30"]]), False)
    #     self.assertEqual(par.semantic_analyser.seq_correct_type("Int", [["10", "100", "20", "30"],
    #                                                             ["10", "100", "20", "30"],
    #                                                             ["10", "100", "20", "False"]]), False)
    # IR generation

    # def test_int_decl_IR(self):
    #     par = Parser()
    #     self.assertEqual(par.semantic_analyser.IR.root, None)
    #     self.assertEqual(par.parse_test_unit("Int(4) a= 10;")[1], True)  # NOQA
    #     self.assertEqual(par.semantic_analyser.IR.root.type, Tree.SEQ)
    #     self.assertEqual(par.semantic_analyser.IR.root.left.type, Tree.VAR_DECL)  # NOQA
    #     self.assertEqual(par.semantic_analyser.IR.root.left.translate(), "uint8_t a[4]={1,0,1,0};")  # NOQA
    #     self.assertEqual(par.parse_test_unit("Int(2) b=10;"), False)  # NOQA
    #     self.assertEqual(par.parse_test_unit("Int c;")[1], True)
    #     self.assertEqual(par.semantic_analyser.IR.root.right.left.translate(), "uint8_t c[10]={0,0,0,0,0,0,0,0,0,0};")  # NOQA

    # def test_multiple_int_decl_IR(self):
    #     par = Parser()
    #     self.assertEqual(par.parse_test_unit("Int(4) a= 10; Int b = 5, c;")[1], True)  # NOQA
    #     self.assertEqual(par.semantic_analyser.IR.root.type, Tree.SEQ)
    #     self.assertEqual(par.semantic_analyser.IR.root.left.translate(), "uint8_t a[4]={1,0,1,0};")  # NOQA
    #     self.assertEqual(par.semantic_analyser.IR.root.right.type, Tree.SEQ)
    #     self.assertEqual(par.semantic_analyser.IR.root.right.left.translate(), "uint8_t b[10]={0,0,0,0,0,0,0,1,0,1};")  # NOQA
    #     self.assertEqual(par.semantic_analyser.IR.root.right.right.type, Tree.SEQ)  # NOQA
    #     self.assertEqual(par.semantic_analyser.IR.root.right.right.left.translate(), "uint8_t c[10]={0,0,0,0,0,0,0,0,0,0};")  # NOQA

    # Broken with semantic checks
    # def test_function_parsing(self):
    #     par = Parser()
    #     self.assertEqual(par.parse_test_integration("Int testFunction(Int a, Bit b, Int[63] c, Int[1][2][3] d) {\
    #         a = 100;\
    #         return a;\
    #         }")[1], True)
    #     self.assertEqual(par.parse_test_integration("Int a;"), False)

    # def test_function_id_set_semantics(self):
    #     par = Parser()
    #     par.parse_test_unit("Int a; Int[4] c;")
    #     self.assertEqual(par.parse_test_unit("a = 1;")[1], True)
    #     self.assertEqual(par.parse_test_unit("b = 1;"), False)
    #     self.assertEqual(par.parse_test_unit("c = [1,0,1,0];")[1], True)
    #     self.assertEqual(par.parse_test_unit("c = [True,0,1,0];"), False)
    #     self.assertEqual(par.parse_test_unit("c = [True,False,False,True];"), False)
    #     self.assertEqual(par.parse_test_unit("b = [True,0,1,0];"), False)
    #     self.assertEqual(par.parse_test_unit("c = [3 * 2, 1, 0, 0];")[1], True)
    #     self.assertEqual(par.parse_test_unit("[3 * 2, [1,3], 0, 0];")[1], True)
    #     self.assertEqual(par.parse_test_unit("c = function(1,2) + function2(1,1);")[1], True)
    #     par.parse_test_unit("Int b;")
    #     self.assertEqual(par.parse_test_unit("b = 1;")[1], True)
    #     par.parse_test_unit("Int[10][10] c;")
    #     self.assertEqual(par.parse_test_unit("Int[10] d = (1,2,3,4);")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int[1][2] e = ((1,2),(1,2),(1,2),(1,2),(1,2),(1,2),(1,2),(1,2));")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int[1][2][4] f = (((1,2),(1,2),(1,2),(1,2)),((1,2),(1,2),(1,2),(1,2)));")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int[1][2] g = (((1,2),(1,2),(1,2),(1,2)),((1,2),(1,2),(1,2),(1,2)));"), False)
    #     self.assertEqual(par.parse_test_unit("Int[1][2] h = ((((1,2),(1,2),(1,2),(1,2)),((1,2),(1,2),(1,2),(1,2))));"), False)
    #     self.assertEqual(par.parse_test_unit("Int[1][2][4] i = (((True,False),(True,False),(True,False),(True,False)),((True,False),(True,False),(True,False),(True,False)));"), False)  # NOQA

    # def test_cast_parsing(self):
    #     par = Parser()
    #     par.parse_test_unit("Int a, b;")
    #     self.assertEqual(par.parse_test_unit("(Int) a;")[1], True)
    #     self.assertEqual(par.parse_test_unit("(Bit) a;")[1], True)
    #     self.assertEqual(par.parse_test_unit("(Int[4]) 10;")[1], True)
    #     self.assertEqual(par.parse_test_unit("(Int[4]) 5 * 3;")[1], True)
    #     self.assertEqual(par.parse_test_unit("(Int[4]) Bit[10];"), False)
    #     self.assertEqual(par.parse_test_unit("(Int[4]) Int;"), False)
    #     self.assertEqual(par.parse_test_unit("(Int[4]) Bit;"), False)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
    unittest.TextTestRunner(verbosity=2).run(suite)
