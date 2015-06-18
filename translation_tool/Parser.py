from pyparsing import Literal, Word, nums, ParseException, Forward, alphas,\
    Suppress, Group, ZeroOrMore, Keyword, alphanums, NotAny, CharsNotIn, \
    OneOrMore, Optional, delimitedList, StringEnd, oneOf, srange, Combine, \
    infixNotation, opAssoc
import unittest
from Symbol_Table import Symbol_Table
from Stack import Stack
from IR import IR_Tree, Seq_node, Decl_node, Type_node, Name_node, Literal_node,\
    Tree


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

    def is_already_declared(self, ID):
        """Returns False if ID has not been declared yet"""
        if self.sym_table.id_in(self.call_stack.peek(), ID[0]) == True:  # NOQA
            return True
        else:
            return False

    def analyse_id_set(self, tokens):
        token = tokens[0]
        if self.is_already_declared(token("ID")) is True:
            raise ParseException("Unknown Value")
        if self.value_is_correct_type(token("ID"), token("value")) is False:
                raise ParseException("Incorrect Value Type assigned to ID")

    def value_is_correct_type(self, ID, value):
        id_type = self.sym_table.id_type(self.call_stack.peek(), ID)
        if id_type is "Bit" and self.is_bit(value) is True:
            return True
        if id_type is "Int" and self.is_int(value) is True:
            return True
        print("Incorrect Value assigned to type")
        return False

    def is_int(self, value):
        try:
            self.convert_base(value)
            # int(value)
        except ValueError:
            print("Cannot assign non-integer to Int")
            return False
        return True

    def is_bit(self, value):
        if value == "True" or value == "False":
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

    def analyse_int_decl(self, tokens):
        token = tokens[0]
        for decl in token["value"]:
            print(decl.dump())
            try:
                if self.analyse_constraints(decl["value"], token["constraints"]) is False:  # NOQA
                    raise ParseException("Value bigger than bit constraints")
            except KeyError:
                pass
            if self.is_already_declared(decl["ID"]) is True:
                    raise ParseException("Duplicate Symbol")
            self.add_int_decl(decl, token)
        return tokens

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
        self.l_shift_ = Keyword('<<')
        self.r_shift_ = Keyword('>>')
        self.circ_l_shift_ = Keyword('<<<')
        self.circ_r_shift_ = Keyword('>>>')
        self.bit_val = self.false_ ^ self.true_
        self.ID = NotAny(self.int_ ^ self.bit_) + Word(alphas + '_', alphanums + '_')  # NOQA
        self.if_ = Keyword('if')
        self.for_ = Keyword('for')
        # Other Tokens
        self.l_bracket = Literal('(')
        self.r_bracket = Literal(')')
        self.eq_set = Literal('=')("set")
        self.term_st = Literal(';')
        self.b_2_num = Combine(Literal("0b") + Word("01"))
        self.b_16_num = Combine(Literal("0x") + Word(srange("[0-9a-fA-F]")))
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
        self.shift_op = self.l_shift_ ^ self.r_shift_ ^ self.circ_l_shift_ ^ self.circ_r_shift_
        self.arith_op = self.bin_add ^ self.bin_mult ^ self.bin_sub ^ self.bin_mod ^ self.bin_div
        self.bin_op = self.arith_op ^ self.shift_op

        # Grammar
        self.stmt = Forward()
        self.for_loop = Forward()
        self.expr = Forward()
        self.seq_val = Forward()

        self.int_value = self.b_2_num ^ self.b_16_num ^ self.b_10_num
        self.seq_val << Group(self.l_bracket + (delimitedList(self.int_value) ^ delimitedList(self.bit_val) ^ delimitedList(self.seq_val)) + self.r_bracket)

        self.var = self.ID ^ self.int_value ^ self.bit_val ^ self.seq_val

        self.id_set = Group(self.ID("target") + self.eq_set + (self.expr)("value"))

        # id_set.setParseAction(semantic_analyser.analyse_id_set)  # NOQA # Remeber ID must be ID[0]!

        self.int_decl = Group(self.int_("decl") + Optional(Suppress(self.l_bracket) + Word(nums)("constraints") +
            Suppress(self.r_bracket)) + delimitedList(Group(self.ID("ID")) ^ Group(self.ID("ID") + self.eq_set + self.int_value("value")))("value"))  # NOQA
        self.int_decl.setParseAction(self.semantic_analyser.analyse_int_decl)

        self.bit_decl = Group(self.bit_("decl") + delimitedList(Group(self.ID) ^ Group(self.ID + self.eq_set + self.bit_val("value")))("value"))

        self.seq_decl = Group((self.int_ ^ self.bit_) + OneOrMore(Suppress(self.l_sq_b) + Word(nums) + Suppress(self.r_sq_b)) + self.ID)  # + self.ID + Optional(self.eq_set + self.seq_val))

        self.comparison = infixNotation(infixNotation(self.var,  # NOQA
                                                           [(self.comparison_op, 2, opAssoc.LEFT), ]),
                                                           [(self.log_op, 2, opAssoc.LEFT), ])

        self.decl = self.bit_decl ^ self.int_decl ^ self.seq_decl

        self.expr << Group(infixNotation(self.var, [(self.bin_op("Operator"), 2, opAssoc.LEFT), ]))

        self.for_loop << Group(self.for_ + self.l_bracket + Optional(delimitedList(self.decl | self.id_set)) + self.term_st +
                               self.comparison + self.term_st +
                               Optional(delimitedList(self.expr ^ self.id_set)) + self.r_bracket +
                               self.l_brace + self.stmt + self.r_brace)

        self.if_stmt = Group(self.if_ + self.l_bracket + self.comparison + self.r_bracket + self.l_brace + self.stmt + self.r_brace)

        self.stmt << ZeroOrMore(self.decl + Suppress(self.term_st)
                                | self.id_set + Suppress(self.term_st)
                                | self.expr + Suppress(self.term_st)
                                | self.for_loop
                                | self.if_stmt)

        self.grammar = self.stmt + StringEnd()

    def parse_test_unit(self, data_in):
        try:
            res = self.grammar.parseString(data_in)
        except ParseException as details:
            print("The following error occured:")
            print(details)
            return False
        if type(res[0]) is not bool:
            print(res[0].dump())
        return [res, True]

    def parse_test(self, data_in):
        try:
            res = self.grammar.parseString(data_in)
        except ParseException:
            # print(detail)
            pass
        return res

    def parse(self, data_in):
        return self.grammar.parseString(data_in)


class TestParser(unittest.TestCase):

    # def test_int_decl_parsing(self):
    #     par = Parser()
    #     self.assertEqual(par.parse_test_unit("Int varName;")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int(123) ee;")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int(123) ff"), False)
    #     self.assertEqual(par.parse_test_unit("Int()"), False)
    #     self.assertEqual(par.parse_test_unit("Int(1) ;"), False)
    #     self.assertEqual(par.parse_test_unit("Int(1) test"), False)
    #     self.assertEqual(par.parse_test_unit("Int"), False)
    #     self.assertEqual(par.parse_test_unit("Int(123) gg,jj,test2;")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int Int;"), False)
    #     self.assertEqual(par.parse_test_unit("Int Integer;")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int kk; Int \
    #         ll;")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int mm, nn, oo, pp;")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int qq = 10, rr = 4, ss = 5, tt = \
    #         7;")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int uu = 10, j, k = 5,\
    #         d;")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int(10) l = 10, m, n = 5, \
    #      h;")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int(10) o = 10, p, q = 5, \
    #      h"), False)
    #     self.assertEqual(par.parse_test_unit("Int(10) r1 = 10, s1, t1 = 5, u1; Int v1, w1=10, \
    #         ll1;")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int dd = 10;")[1], True)

    # def test_int_decl_semantics(self):
    #     sem_a = Semantic_analyser()
    #     par = Parser()
    #     self.assertEqual(sem_a.analyse_constraints("10", "2"), False)
    #     self.assertEqual(sem_a.analyse_constraints(
    #                      "999999999999999999999999999999999999999999999999999999999999"  # NOQA
    #                      "999999999999999999999999999999", "2"), False)
    #     self.assertEqual(par.parse_test_unit("Int a = 10;")[1], True)  # NOQA
    #     self.assertEqual(par.parse_test_unit("Int d = 10, b = 10, c = 20;")[1], True)  # NOQA
    #     self.assertEqual(par.parse_test_unit("Int(3) e = 10, f = 10, g = 20;"), False)  # NOQA
    #     self.assertEqual(par.parse_test_unit("Int(4) h = 10, h = 10, i = 20;"), False)  # NOQA
    #     self.assertEqual(par.parse_test_unit("Int(4) z = 10;")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int(4) z = 10;"), False)
    #     self.assertEqual(par.parse_test_unit("Int(4) k;")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int(4) k;"), False)

    # def test_bit_decl_parsing(self):
    #     par = Parser()
    #     self.assertEqual(par.parse_test_unit("Bit a = True;")[1], True)
    #     self.assertEqual(par.parse_test_unit("Bit b, c, d = True;")[1], True)
    #     self.assertEqual(par.parse_test_unit("Bit Bit, c, d = True;"), False)

    # def test_id_set_semantics(self):
    #     sem_a = Semantic_analyser()
    #     sem_a.sym_table.add_int_id("global", "a")
    #     self.assertEqual(sem_a.value_is_correct_type("a", "30"), True)
    #     self.assertEqual(sem_a.value_is_correct_type("a", "False"), False)

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

    # def test_add_to_symbol_table(self):
    #     sem_a = Semantic_analyser()
    #     sem_a.sym_table.add_int_id("global", "A", "10", "5")
    #     sem_a.sym_table.add_int_id("global", "B", id_constraints="9")
    #     sem_a.sym_table.add_int_id("global", "D", id_value="4")
    #     self.assertEqual(sem_a.sym_table.id_in("global", "A"), True)
    #     self.assertEqual(sem_a.sym_table.id_in("global", "B"), True)
    #     self.assertEqual(sem_a.sym_table.id_in("global", "C"), False)
    #     self.assertEqual(sem_a.sym_table.id_in("global", "D"), True)

    # def test_multiple_int_decl_IR(self):
    #     par = Parser()
    #     self.assertEqual(par.parse_test_unit("Int(4) a= 10; Int b = 5, c;")[1], True)  # NOQA
    #     self.assertEqual(par.semantic_analyser.IR.root.type, Tree.SEQ)
    #     self.assertEqual(par.semantic_analyser.IR.root.left.translate(), "uint8_t a[4]={1,0,1,0};")  # NOQA
    #     self.assertEqual(par.semantic_analyser.IR.root.right.type, Tree.SEQ)
    #     self.assertEqual(par.semantic_analyser.IR.root.right.left.translate(), "uint8_t b[10]={0,0,0,0,0,0,0,1,0,1};")  # NOQA
    #     self.assertEqual(par.semantic_analyser.IR.root.right.right.type, Tree.SEQ)  # NOQA
    #     self.assertEqual(par.semantic_analyser.IR.root.right.right.left.translate(), "uint8_t c[10]={0,0,0,0,0,0,0,0,0,0};")  # NOQA

    # def test_shift_op(self):
    #     par = Parser()
    #     self.assertEqual(par.parse_test_unit("a << 3;")[1], True)
    #     self.assertEqual(par.parse_test_unit("a >> 3;")[1], True)
    #     self.assertEqual(par.parse_test_unit("a <<< 3;")[1], True)
    #     self.assertEqual(par.parse_test_unit("a >>> 3;")[1], True)
    #     self.assertEqual(par.parse_test_unit("a > 3;"), False)
    #     self.assertEqual(par.parse_test_unit("10 >> 4;")[1], True)
    #     self.assertEqual(par.parse_test_unit("10 >> 4; a >> 4;")[1], True)

    # def test_set_parsing(self):
    #     par = Parser()
    #     self.assertEqual(par.parse_test_unit("b = 2;")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int = 2;"), False)
    #     self.assertEqual(par.parse_test_unit("d = False;")[1], True)
    #     self.assertEqual(par.parse_test_unit("e = True;")[1], True)
    #     self.assertEqual(par.parse_test_unit("e = True True;"), False)

    # def test_int_bases(self):
    #     par = Parser()
    #     self.assertEqual(par.parse_test_unit("a = 0b010101010;")[1], True)
    #     self.assertEqual(par.parse_test_unit("b = 0x345;")[1], True)
    #     self.assertEqual(par.parse_test_unit("c = 0x3b;")[1], True)
    #     self.assertEqual(par.parse_test_unit("b = 0x3D45ef3456a;")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int d = 0x3aab;")[1], True)
    #     self.assertEqual(par.parse_test_unit("Int(4) e = 0x11;"), False)
    #     self.assertEqual(par.parse_test_unit("Int(4) f = 0b101011;"), False)

    # def test_conv(self):
    #     sem_a = Semantic_analyser()
    #     self.assertEqual(str(sem_a.convert_base("0b0010")), "2")
    #     self.assertEqual(str(sem_a.convert_base("0x000a")), "10")

    # def test_expr_parsing(self):
    #     par = Parser()
    #     self.assertEqual(par.parse_test_unit("a + b;")[1], True)
    #     self.assertEqual(par.parse_test_unit("a + c + d + e;")[1], True)
    #     self.assertEqual(par.parse_test_unit("a + (c + d) + e;")[1], True)
    #     self.assertEqual(par.parse_test_unit("a + c + d + + e;"), False)
    #     self.assertEqual(par.parse_test_unit("a + c + 4 - e;")[1], True)
    #     self.assertEqual(par.parse_test_unit("a + (c) + 4 - e;")[1], True)
    #     self.assertEqual(par.parse_test_unit("a + (c + 4) - (e + r);")[1], True)
    #     self.assertEqual(par.parse_test_unit("a + ((c + d) + 4) - (e + r);")[1], True)
    #     self.assertEqual(par.parse_test_unit("(a >> b) << c;")[1], True)
    #     self.assertEqual(par.parse_test_unit("a;")[1], True)
    #     self.assertEqual(par.parse_test_unit("1;")[1], True)
    #     self.assertEqual(par.parse_test_unit("True;")[1], True)
    #     self.assertEqual(par.parse_test_unit("False;")[1], True)

    # def test_for_parsing(self):
    #     par = Parser()
    #     self.assertEqual(par.parse_test_unit("for(Int a = 2; ((a > 4) && (b > 5)) || d > 3; d = 5, d = (e * g)) { a = 1; }")[1], True)
    #     self.assertEqual(par.parse_test_unit("for(a = 2; ((a > 4) && (b > 5)) || d > 3; d = 5, d = (e * g)) { for(d = 3; d < 5; d = d + 1) { a = 1; } }")[1], True)  # NOQA
    #     self.assertEqual(par.parse_test_unit("for(;a < 4;){}")[1], True)

    # def test_if_parsing(self):
    #     par = Parser()
    #     self.assertEqual(par.parse_test_unit("if(a==1) { for(a = 2; ((a > 4) && (b > 5)) || d > 3; d = 5, d = (e * g)) { for(d = 3; d < 5; d = d + 1) { a = 1; } }  }")[1], True)  # NOQA

    def test_seq_decl_parsing(self):
        par = Parser()
        # self.assertEqual(par.parse_test_unit("(1,2,3,4,5);")[1], True)
        # self.assertEqual(par.parse_test_unit("(True,False,True,False,True);")[1], True)
        # self.assertEqual(par.parse_test_unit("((True,False,True,False,True),(True,False,True,False,True),(True,False,True,False,True));")[1], True)
        # self.assertEqual(par.parse_test_unit("(True,1,2,False);"), False)
        self.assertEqual(par.parse_test_unit("Int[4] a;")[1], True)
        self.assertEqual(par.parse_test_unit("Bit[4] b;")[1], True)
        self.assertEqual(par.parse_test_unit("Bit[4][4] c;")[1], True)
        self.assertEqual(par.parse_test_unit("Bit[4][4][4] c;")[1], True)
        self.assertEqual(par.parse_test_unit("Bit[4][4] [4] c;"), False)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
    unittest.TextTestRunner(verbosity=2).run(suite)







