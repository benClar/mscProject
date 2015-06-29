from pyparsing import Literal, Word, nums, ParseException, Forward, alphas,\
    Suppress, Group, ZeroOrMore, Keyword, alphanums, NotAny, CharsNotIn, \
    OneOrMore, Optional, delimitedList, StringEnd, oneOf, srange, Combine, \
    infixNotation, opAssoc, White, ParserElement, operatorPrecedence, ParseResults
import unittest
from Semantic_analyser import Semantic_analyser
from AST import *
ParserElement.enablePackrat()


class Parser(object):

    def __init__(self):
        self.semantic_analyser = Semantic_analyser()
        self._AST = AST()

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
        self.ID_ = NotAny(self.int_ ^ self.bit_ ^ self.false_ ^ self.true_ ^ self.if_ ^ self.for_ ^ self.sbox_) + Word(alphas + '_', alphanums + '_')
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
        self.seq_range = Forward()
        #  #######Operands

        self.sbox_call = Group((self.ID ^ self.seq_val) + ~White() + Literal(".") + ~White() + self.sbox_ + ~White() +
                               self.l_bracket + (self.ID ^ self.int_value) + self.r_bracket)

        self.operand = self.seq_index_select | self.seq_val | self.function_call | self.ID | self.int_value | self.cast | self.bit_val
        self.seq_val.setParseAction(lambda t: ['Seq_val'] + [t.asList()])
        self.seq_index_select.setParseAction(lambda t: ['index_select'] + [t.asList()])
        self.function_call.setParseAction(lambda t: ['function_call'] + [t.asList()])
        self.ID.setParseAction(lambda t: ['ID'] + [t.asList()])
        self.int_value.setParseAction(lambda t: ['Int_val'] + [t.asList()])
        self.cast.setParseAction(lambda t: ['cast'] + [t.asList()])
        self.bit_val.setParseAction(lambda t: ['Bit_val'] + [t.asList()])
        self.seq_range.setParseAction(lambda t: ['seq_range'] + [t.asList()])
        #  #######Expressions

        self.expr = Group(infixNotation(Group(self.operand), [(self.bitwise_op, 2, opAssoc.LEFT, self.nest_operand_pairs),
                                                              (self.comparison_op, 2, opAssoc.LEFT, self.nest_operand_pairs),
                                                              (self.log_op, 2, opAssoc.LEFT, self.nest_operand_pairs),
                                                              (self.arith_op, 2, opAssoc.LEFT, self.nest_operand_pairs)]))

        # self.expr.setParseAction(self.AST.expr)
        self.int_size = self.int_("decl") + ~White() + Suppress(self.l_bracket) + self.expr + Suppress(self.r_bracket)

        self.seq_range << self.expr + Suppress(Literal(":")) + self.expr

        self.seq_index_select << self.ID("ID") + ~White() +\
            Suppress(self.l_sq_b) + Group(delimitedList(self.expr ^ Group(Group(self.seq_range))))("index") + Suppress(self.r_sq_b)

        self.seq_val << Suppress(self.l_sq_b) + Optional(Group(delimitedList(self.expr))) + Suppress(self.r_sq_b)

        self.seq_ << (self.int_size ^ self.bit_)("type") +\
            Group(OneOrMore(~White() + Suppress(self.l_sq_b) + self.expr + Suppress(self.r_sq_b)))("seq_size")

        self.function_call << self.ID("function_name") + ~White() + Suppress(self.l_bracket) +\
            Optional(Group(delimitedList(self.expr)))("param_list") + Suppress(self.r_bracket)

        self.cast << Suppress(self.l_bracket) + Group((self.seq_ | self.int_size | self.bit_)) +\
            Suppress(self.r_bracket) + (self.expr)("target")
        #  ####### Declarations

        self.id_set = Group((Group(self.seq_index_select) | self.ID_) + self.eq_set + self.expr)
        self.id_set.setParseAction(self.AST.id_set)

        self.int_decl = Group(self.int_size + delimitedList(Group((self.ID_("ID") + self.eq_set + self.expr("set_value")) |
                              self.ID_("ID")))("value"))  # NOQA
        self.int_decl.setParseAction(self.AST.int_decl)
        self.bit_decl = Group(self.bit_("decl") + delimitedList(Group(self.ID_("ID")) ^
                              Group(self.ID_("ID") + self.eq_set + self.expr("set_value")))("value"))
        self.bit_decl.setParseAction(self.AST.bit_decl)
        self.seq_decl = Group(self.seq_("decl") + Group(self.ID)("ID") + Optional(self.eq_set + Group(self.expr))("value"))
        self.seq_decl.setParseAction(self.AST.seq_decl)
        self.decl = self.bit_decl | self.int_decl | self.seq_decl

        # ###### Statements

        self.return_stmt = Group(self.return_ + self.expr)
        self.return_stmt.setParseAction(self.AST.return_stmt)

        self.function_decl = Group((self.int_ ^ self.bit_ ^ self.seq_)("return_type") + Group(self.ID) +
                                   Suppress(self.l_bracket) + Group(Optional(delimitedList(Group((self.seq_ ^ self.int_ ^ self.bit_) + Group(self.ID)))))("func_param") +
                                   Suppress(self.r_bracket) + Suppress(self.l_brace) + Group(self.stmt)("body") + Suppress(self.r_brace))
        self.function_decl.setParseAction(self.AST.function_decl)

        # self.terminator.setParseAction(self.AST.terminator)
        self.for_init = Literal('(')
        self.for_init.setParseAction(self.AST.begin_for)

        self.for_terminator = Literal(';')
        self.for_terminator.setParseAction(self.AST.for_terminator)

        self.for_increment = Literal(';')
        self.for_increment.setParseAction(self.AST.for_increment)

        self.terminator_expr = Group(infixNotation(Group(self.operand), [(self.bitwise_op, 2, opAssoc.LEFT, self.nest_operand_pairs),
                                                              (self.comparison_op, 2, opAssoc.LEFT, self.nest_operand_pairs),
                                                              (self.log_op, 2, opAssoc.LEFT, self.nest_operand_pairs),
                                                              (self.arith_op, 2, opAssoc.LEFT, self.nest_operand_pairs)]))

        self.terminator_expr.setParseAction(self.AST.terminator_expr)
        self.for_body = Literal('{')
        self.for_body.setParseAction(self.AST.for_body)

        self.end_for = Literal('}')
        self.end_for.setParseAction(self.AST.end_for)

        self.for_loop << Group(self.for_ + ~White() + Suppress(self.for_init) +
                               Optional(delimitedList(self.decl ^ self.id_set))("init") + Suppress(self.for_terminator) +
                               Optional(self.terminator_expr) + Suppress(self.for_increment) +
                               Optional(delimitedList(self.id_set))("increm") + Suppress(self.r_bracket) +
                               Suppress(self.for_body) + self.stmt("loop_body") + Suppress(self.end_for))
        # self.for_loop.setParseAction(self.AST.for_loop)

        self.if_condition = Suppress(self.l_bracket) + self.expr + Suppress(self.r_bracket)
        self.if_condition.setParseAction(self.AST.if_cond)

        self.if_.setParseAction(self.AST.begin_if)
        self.if_body_st = Literal('{')
        self.if_body_st.setParseAction(self.AST.if_body_st)
        self.if_body_end = Literal('}')
        self.if_body_end.setParseAction(self.AST.if_body_end)
        self.if_stmt = Group(self.if_ + self.if_condition("if_cond") + Suppress(self.if_body_st) + Group(self.stmt).setResultsName("body") + Suppress(self.if_body_end))

        # self.if_stmt.setParseAction(self.AST.if_cond)

        self.stmt << ZeroOrMore(self.decl + Suppress(self.term_st)
                                | self.function_decl
                                | self.id_set + Suppress(self.term_st)
                                | self.expr + Suppress(self.term_st)
                                | self.for_loop
                                | self.if_stmt
                                | self.return_stmt + Suppress(self.term_st)
                                | self.sbox_call + Suppress(self.term_st))

        self.grammar_test = self.stmt + StringEnd()  # Allows single statements to be parsed

        self.grammar = self.function_decl + StringEnd()

    def nest_operand_pairs(self, tokens):
        tokens = tokens[0]
        ret = ParseResults(tokens[:3])
        remaining = iter(tokens[3:])
        done = False
        while not done:
            next_pair = (next(remaining, None), next(remaining, None))
            if next_pair == (None, None):
                done = True
                break
            ret = ParseResults([ret])
            ret += ParseResults(list(next_pair))
        return [ret]

    @property
    def AST(self):
        return self._AST

    @AST.setter
    def AST(self, value):
        self._AST = value

    def analyse_tree_test(self, AST):
        return self.semantic_analyser.analyse(AST)

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

    def parse_test_AST_semantic(self, data_in):
        """Parses single statements and returns AST"""
        try:
            self.grammar_test.parseString(data_in)
        except ParseException as details:
            print("The following error occured:")
            print(details)
            return False
        return self.AST

    def parse_test_integration(self, data_in):
        """Only Parses Statements in functions"""
        try:
            res = self.grammar.parseString(data_in)
        except ParseException as details:
            print("The following error occured:")
            print(details)
            return False
        # if type(res[0]) is not bool:
            # print(res[0].dump())
        return [res, True]

    def parse(self, data_in):
        return self.grammar.parseString(data_in)


class TestParser(unittest.TestCase):  
    pass
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
        self.assertEqual(par.parse_test_unit("Bit c, d = function(1,2,3,4);")[1], True)
        self.assertEqual(par.parse_test_unit("Bit c, d = function();")[1], True)
        self.assertEqual(par.parse_test_unit("Bit c, d = function(1,2,(3*5) << (4 * 5)) + function_2(1,2,(3*5) << (4 * 5));")[1], True)
        self.assertEqual(par.parse_test_unit("Bit c, d = 3 + (1+ 2 + 3) * (2 + (Bit) 3);")[1], True)

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
        self.assertEqual(par.parse_test_unit("Int(10)[4] a;")[1], True)
        self.assertEqual(par.parse_test_unit("Bit[4] b;")[1], True)
        self.assertEqual(par.parse_test_unit("Bit[4][4] c;")[1], True)
        self.assertEqual(par.parse_test_unit("Bit[4][4][4] d;")[1], True)
        self.assertEqual(par.parse_test_unit("Bit[4][4] [4] e;"), False)
        self.assertEqual(par.parse_test_unit("Bit [4][4] f;"), False)
        self.assertEqual(par.parse_test_unit("Bit[4][4] 1;"), False)
        self.assertEqual(par.parse_test_unit("Bit[1][4] f = [[True,False,True,True]];")[1], True)
        self.assertEqual(par.parse_test_unit("Int(10)[3] g = [5*5, function(1,2,3), 4];")[1], True)

    def test_seq_op_parsing(self):
        par = Parser()
        self.assertEqual(par.parse_test_unit("Int(10)[6] b = a[5,6,7,8:10];")[1], True)
        self.assertEqual(par.parse_test_unit("Int(10) a[5,6,7,8:10];"), False)
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
        self.assertEqual(par.parse_test_unit("for(;;){ }")[1], True)

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

    def test_using_expr_parsing(self):
        par = Parser()
        self.assertEqual(par.parse_test_unit("Int(10) a = (5 * 10) + 3 + (3 * 2);")[1], True)

    def test_cast_parsing(self):
        par = Parser()
        par.parse_test_unit("Int(10) a, b;")
        self.assertEqual(par.parse_test_unit("(Int(10)) a;")[1], True)
        self.assertEqual(par.parse_test_unit("(Bit) a;")[1], True)
        self.assertEqual(par.parse_test_unit("(Int(10)[4]) 10;")[1], True)
        self.assertEqual(par.parse_test_unit("(Int(10)[4]) 5 * 3;")[1], True)
        self.assertEqual(par.parse_test_unit("(Int(10)[4]) Bit[10];"), False)
        self.assertEqual(par.parse_test_unit("(Int(10)[4]) Int;"), False)
        self.assertEqual(par.parse_test_unit("(Int(10)[4]) Bit;"), False)

    def test_function_dec_parsing(self):
        par = Parser()
        self.assertEqual(par.parse_test_integration("Int function_1(Int a, Bit b) { Int(10) a = 1; Int(10) b = 2; }")[1], True)


class TestASTTree(unittest.TestCase):
    pass
    def test_bit_decl(self):
        par = Parser()
        self.assertEqual(par.parse_test_unit("Bit c, d = 3 + (1 + 2 + 3) * (2 + (Bit) 3 + 2);")[1], True)
        self.assertEqual(par.AST.tree[0].node_type,  AST_TYPE.BIT_DECL)
        self.assertEqual(par.AST.tree[1].node_type, AST_TYPE.BIT_DECL)
        self.assertEqual(par.AST.tree[1].value.node_type, AST_TYPE.EXPR)
        self.assertEqual(len(par.AST.tree[1].value.expressions[0].expressions), 3)
        self.assertEqual(par.AST.tree[1].value.expressions[0].expressions[0].expressions[0].value, "3")
        self.assertEqual(par.AST.tree[1].value.expressions[0].expressions[1].operator, "*")
        self.assertEqual(par.AST.tree[1].value.expressions[0].expressions[0].expressions[2].expressions[0].expressions[0].value, "1")
        self.assertEqual(par.AST.tree[1].value.expressions[0].expressions[2].expressions[1].operator, "+")
        self.assertEqual(par.AST.tree[1].value.expressions[0].expressions[0].expressions[2].expressions[0].expressions[2].value, "2")
        self.assertEqual(par.AST.tree[1].value.expressions[0].expressions[0].expressions[2].expressions[1].operator, "+")
        self.assertEqual(par.AST.tree[1].value.expressions[0].expressions[2].expressions[2].target.expressions[0].expressions[0].value, "3")

    def test_int_decl(self):
        par = Parser()
        self.assertEqual(par.parse_test_unit("Int(10) c = 2 + e * (Bit[4]) function(10,10,b * 5), d = 3, e;")[1], True)
        self.assertEqual(par.parse_test_unit("Int(10) c =function(b);")[1], True)
        self.assertEqual(par.parse_test_unit("Int(10) c = [1,2,3,4];")[1], True)
        self.assertEqual(par.AST.tree[0].node_type,  AST_TYPE.INT_DECL)
        self.assertEqual(par.AST.tree[1].node_type,  AST_TYPE.INT_DECL)
        self.assertEqual(par.AST.tree[2].node_type,  AST_TYPE.INT_DECL)
        self.assertEqual(par.AST.tree[0].ID, "c")
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[0].expressions[0].value,  "2")
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[1].operator,  "*")
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[0].expressions[2].ID,  "e")
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[1].operator,  "*")
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[2].node_type, AST_TYPE.CAST)
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[2].target.expressions[0].ID.ID, "function")
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[2].target.expressions[0].parameters[0].expressions[0].value, "10")

    def test_int_seq_decl(self):
        par = Parser()
        self.assertEqual(par.parse_test_unit("Int(10)[5] a = [1,function(1,2,3),function(), (1*2*3) << 4, d + e];")[1], True)
        self.assertEqual(par.parse_test_unit("Int(10)[2][2] f = [[1,2],[3,4]];")[1], True)
        self.assertEqual(par.parse_test_unit("Int(10)[2][2][2] f = [[[[1 * 2 * 3,2],[(Int(10)) [1,2,3,4],3]]],[[[5,6],[7,8]]]];")[1], True)
        self.assertEqual(par.parse_test_unit("[1,2,3,4];")[1], True)
        self.assertEqual(par.parse_test_unit("Int(10)[1][2] b = [[],[]];")[1], True)
        self.assertEqual(par.parse_test_unit("Int(10)[5] b = c[1,2,3:5];")[1], True)
        self.assertEqual(par.parse_test_unit("Int(10)[5] b;")[1], True)
        self.assertEqual(par.AST.tree[0].ID.ID, "a")
        self.assertEqual(par.AST.tree[0].bit_constraints.expressions[0].value, "10")
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[0].node_type, AST_TYPE.SEQ_VAL)
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[0].value[0].expressions[0].value, "1")
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[0].value[1].expressions[0].parameters[0].expressions[0].value, "1")
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[0].value[3].expressions[0].expressions[0].expressions[0].expressions[0].value, "1")
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[0].value[3].expressions[0].expressions[0].expressions[1].operator, "*")
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[0].value[3].expressions[0].expressions[0].expressions[0].expressions[2].value, "2")
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[0].value[3].expressions[0].expressions[1].operator, "<<")
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[0].value[3].expressions[0].expressions[2].value, "4")
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[0].value[4].expressions[0].expressions[0].ID, "d")
        self.assertEqual(par.parse_test_unit("Int(10) z = b[1 * 4];")[1], True)
        self.assertEqual(par.AST.tree[6].ID, "z")
        self.assertEqual(par.AST.tree[6].value.expressions[0].ID.ID, "b")
        self.assertEqual(par.AST.tree[6].value.expressions[0].indices[0].expressions[0].expressions[0].value, "1")
        self.assertEqual(par.AST.tree[6].value.expressions[0].indices[0].expressions[0].expressions[1].operator, "*")
        self.assertEqual(par.AST.tree[6].value.expressions[0].indices[0].expressions[0].expressions[2].value, "4")
        self.assertEqual(par.parse_test_unit("Int(10) a = 2;")[1], True)

    def test_bit_seq_decl(self):
        par = Parser()
        self.assertEqual(par.parse_test_unit("Bit[5] b = [True, False, True, False];")[1], True)
        self.assertEqual(par.parse_test_unit("Bit[1][2] b = [[True, False, True, False],[True, False, True, False]];")[1], True)
        self.assertEqual(par.parse_test_unit("Bit[1][2] b = [[],[]];")[1], True)
        self.assertEqual(par.parse_test_unit("Bit[1] b = [];")[1], True)
        self.assertEqual(par.parse_test_unit("Bit[1] b;")[1], True)
        self.assertEqual(par.AST.tree[0].node_type, AST_TYPE.SEQ_DECL)
        self.assertEqual(par.AST.tree[0].size[0].expressions[0].value, "5")
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[0].value[0].expressions[0].value, "True")
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[0].value[1].expressions[0].value, "False")

    def test_id_set(self):
        par = Parser()
        self.assertEqual(par.parse_test_unit("a = b + 10 * function(a, b);")[1], True)
        self.assertEqual(par.parse_test_unit("a = [];")[1], True)
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[0].expressions[0].ID, "b")
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[1].operator, "*")
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[2].parameters[0].expressions[0].ID, "a")
        self.assertEqual(par.AST.tree[0].value.expressions[0].expressions[2].parameters[1].expressions[0].ID, "b")
        self.assertEqual(par.parse_test_unit("a[1,2,3,4:5] = (Bit[4]) b + 10 * function(a, b);")[1], True)
        self.assertEqual(par.AST.tree[2].elements.expressions[0].expressions[0].value, "1")
        self.assertEqual(par.AST.tree[2].elements.expressions[1].expressions[0].value, "2")
        self.assertEqual(par.AST.tree[2].elements.expressions[3].expressions[0].start.expressions[0].value, "4")
        self.assertEqual(par.AST.tree[2].value.expressions[0].target.expressions[0].expressions[2].node_type, AST_TYPE.FUNCTION_CALL)

    def test_func_decl(self):
        par = Parser()
        self.assertEqual(par.parse_test_integration("Int function_1(Int a, Bit b) { Int(10) a = 1; Int(10) b = 2; Int(10) c = 0xa; }")[1], True)
        self.assertEqual(par.AST.tree[0].ID.ID, "function_1")
        self.assertEqual(len(par.AST._statements), 0)
        self.assertEqual(par.AST.tree[0].stmts[0].value.expressions[0].value, '1')
        self.assertEqual(par.AST.tree[0].stmts[1].value.expressions[0].value, '2')
        self.assertEqual(par.AST.tree[0].stmts[2].value.expressions[0].value, '10')

    def test_return_stmt(self):
        par = Parser()
        self.assertEqual(par.parse_test_unit("return a * b * c * 10;")[1], True)
        self.assertEqual(par.AST.tree[0].node_type, AST_TYPE.RETURN_STMT)
        self.assertEqual(par.AST.tree[0].expr.expressions[0].expressions[0].expressions[0].expressions[0].ID, "a")
        self.assertEqual(par.AST.tree[0].expr.expressions[0].expressions[0].expressions[1].operator, "*")

    def test_for_loop(self):
        par = Parser()
        self.assertEqual(par.parse_test_unit("for(Int(10) a = 5, Bit f = False; a < 5 && d < 5; a = a + 1, b = b + 3) { b = b <<< 1; z = b + 19; }")[1], True)
        self.assertEqual(par.parse_test_unit("for(;;) { }")[1], True)
        self.assertEqual(par.AST.tree[0].node_type, AST_TYPE.FOR_LOOP)
        self.assertEqual(par.AST.tree[1].node_type, AST_TYPE.FOR_LOOP)
        self.assertEqual(par.AST.tree[0].terminator[0].expressions[0].expressions[1].operator, "&&")
        self.assertEqual(par.AST.tree[0].body[0].node_type, AST_TYPE.ID_SET)
        self.assertEqual(par.AST.tree[0].body[0].ID, "b")

    def test_if_stmt(self):
        par = Parser()
        self.assertEqual(par.parse_test_unit("if(i > 3) { b = b + 1; c = d + 3; } if(d < 4) { z = z + 1; kk = k + 3; }")[1], True)
        self.assertEqual(par.AST.tree[0].node_type, AST_TYPE.IF_STMT)
        self.assertEqual(par.AST.tree[1].node_type, AST_TYPE.IF_STMT)
        self.assertEqual(par.AST.tree[0].condition[0].expressions[0].expressions[0].expressions[0].ID, "i")
        par = Parser()
        self.assertEqual(par.parse_test_unit("if(i > 3) { if(d < 4) { z = z + 1; kk = k + 3; } } ")[1], True)
        self.assertEqual(par.AST.tree[0].body[0].condition[0].expressions[0].expressions[0].expressions[0].ID, "d")

class TestSemanticAnalysisTree(unittest.TestCase):
    pass
    def test_int_decl(self):
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 4 << [1,2,3,4] << 2;")), False)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 4 << 3 << 2;")), True)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10;")), True)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10; Int(10) a = 20;")), False)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10; Int(10) b = 20;")), True)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10; Int(10) b = a;")), True)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = False;")), False)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10 + False << 4;")), False)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a; Int(10) b = a;")), True)


    def test_bit_decl(self):
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Bit a = False;")), True)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Bit a = 1;")), False)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Bit a = False + False;")), False)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Bit a = False; Bit a = True;")), False)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Bit a; Bit b = a;")), True)

    def test_mixing_bit_int(self):
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Bit b = True;")), True)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Bit b = True; Int(10) c = b;")), False)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Bit b = True; Int(10) c = 5 * (b);")), False)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Int(10) b = 10; Int(10) c = 5 * (b);")), True)

    def test_id_set(self):
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Int(10) b = a;")), True)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Int(10) b = a; Bit c = b;")), False)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Int(10) b = a * 10 * 3 << 4;")), True)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Bit d = False; Int(10) b = a * 10 * 3 << d;")), False)

    def test_seq_decl(self):
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2][2] a = [[1,2],[3,4]]; ")), True)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2][2] a = [[False,2],[3,4]]; ")), False)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2] a = [1, 2, 3, 4]; ")), True)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2] a = [1]; ")), True)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2] a = [1,2,3,4] ^ [1,2,3,4];")), True)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) b = 3; Int(10)c = 4; Int(10)[2] a = [b,2,c,4] ^ [1,2,b * 2,4];")), True)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) b = 3; Int(10)c = 4; Bit d = False; Int(10)[2] a = [b,d,c,4] ^ [1,2,b,4];")), False)  # NOQA
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[4] a = [1,2,3,4];")), True)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(a * a)[4] a = [1,2,3,4];")), False)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[4] a = [1,2,3,4]; Int(10) c; c = a;")), False)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[4] a = [True,False,True,False];")), True)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[4] a = [True,False,True,False,[True, False]];")), False)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[4] a = [1,False,True,False];")), False)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[4][4] a = [[True,False,True,False],[True,False,True,False]];")), True)

    def test_if_stmt(self):
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) a = 4; if(4 > 4) { a = 10; }")), True)

    def test_func_decl(self):
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int test_func(Int a) { Int(10) d = 1;  Bit b = False; }")), True)
        self.assertEqual(par.semantic_analyser.sym_table.f_table['test_func']['return_type'], AST_TYPE.INT_VAL)

    def test_func_call(self):
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int test_func(Int a) { Int(10) d = test_func(test_func(10)) + 20; }")), True)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Bit test_func(Int a) { Int(10) d = 10; }")), True)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Bit test_func1(Int a) { a = a + 10; }\
                                                                            Int test_func(Int a) { Int(10) d = test_func(test_func1(10)) + 20; }")), False)
        par = Parser()
        self.assertEqual(par.analyse_tree_test(par.parse_test_AST_semantic("Int test_func2(Bit a) { Int(10) d = 39; }\
                                                                            Bit test_func1(Bit a) { Int(10) d = 10; }\
                                                                            Int test_func(Int a) { Int(10) d = test_func(test_func2(test_func1(False))) + 20; }")), True)  # NOQA

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestASTTree)
    unittest.TextTestRunner(verbosity=0).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
    unittest.TextTestRunner(verbosity=0).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSemanticAnalysisTree)
    unittest.TextTestRunner(verbosity=0).run(suite)