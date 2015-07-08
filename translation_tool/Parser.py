from pyparsing import Literal, Word, nums, ParseException, Forward, alphas,\
    Suppress, Group, ZeroOrMore, Keyword, alphanums, NotAny, CharsNotIn, \
    OneOrMore, Optional, delimitedList, StringEnd, oneOf, srange, Combine, \
    infixNotation, opAssoc, White, ParserElement, operatorPrecedence, ParseResults
import unittest
from nose.tools import assert_equals
from Semantic_analyser import Semantic_analyser
from AST import *
import traceback
import sys

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
        self.sbox_ = Keyword('Sbox')
        self.l_shift_ = Keyword('<<')
        self.r_shift_ = Keyword('>>')
        self.circ_l_shift_ = Keyword('<<<')
        self.circ_r_shift_ = Keyword('>>>')
        self.bit_val = self.false_ ^ self.true_
        self.if_ = Keyword('if')
        self.for_ = Keyword('for')
        self.return_ = Keyword('return')
        self.void_ = Keyword('void')
        self.ID = NotAny(self.sbox_ ^ self.int_ ^ self.bit_ ^ self.false_ ^ self.true_ ^ self.if_ ^ self.for_ ^ self.sbox_) + Word(alphas + '_', alphanums + '_')  # NOQA
        self.ID_ = NotAny(self.sbox_ ^ self.int_ ^ self.bit_ ^ self.false_ ^ self.true_ ^ self.if_ ^ self.for_ ^ self.sbox_) + Word(alphas + '_', alphanums + '_')
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
        self.bit_or = Keyword('|')
        self.bit_xor = Literal('^')
        self.bit_not = Literal('~')
        self.eq_compare = Literal('==')
        self.neq_compare = Literal('!=')
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
        self.comparison_op = self.g_than ^ self.ge_than ^ self.l_than ^ self.le_than ^ self.eq_compare ^ self.neq_compare
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
        self.index_select = Forward()
        self.seq_ = Forward()
        self.operand = Forward()
        self.seq_range = Forward()
        #  #######Operands

        self.sbox_call = Group((self.ID ^ self.seq_val) + ~White() + Literal(".") + ~White() + self.sbox_ + ~White() +
                               self.l_bracket + (self.ID ^ self.int_value) + self.r_bracket)

        self.operand = self.index_select | self.seq_val | self.function_call | self.ID | self.int_value | self.cast | self.bit_val
        self.seq_val.setParseAction(lambda t: ['Seq_val'] + [t.asList()])
        self.index_select.setParseAction(lambda t: ['index_select'] + [t.asList()])
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

        # self.expr.setParseAction(self.expr_p)
        self.int_size = Combine(Optional(Literal("@")) + self.int_)("decl") + ~White() + Suppress(self.l_bracket) + self.expr + Suppress(self.r_bracket)

        self.sbox_size = self.sbox_ + ~White() + Suppress(self.l_bracket) + self.expr + Suppress(self.r_bracket)

        self.seq_range << self.expr + Suppress(Literal(":")) + self.expr

        self.seq_val << Suppress(self.l_sq_b) + Optional(Group(delimitedList(self.expr))) + Suppress(self.r_sq_b)

        self.seq_ << (self.int_size | self.bit_ | self.sbox_size)("type") +\
            Group(OneOrMore(~White() + Suppress(self.l_sq_b) + self.expr + Suppress(self.r_sq_b)))("seq_size")

        self.function_call << self.ID("function_name") + ~White() + Suppress(self.l_bracket) +\
            Optional(Group(delimitedList(self.expr)))("param_list") + Suppress(self.r_bracket)

        self.cast << Suppress(self.l_bracket) + Group((self.seq_ | self.int_size | self.bit_)) +\
            Suppress(self.r_bracket) + (self.expr)("target")

        self.index_select << (self.ID("ID") ^ (Suppress(self.l_bracket) + self.cast + Suppress(self.r_bracket))("cast")) + ~White() +\
            Group(OneOrMore(Suppress(self.l_sq_b) + Group(delimitedList(self.expr ^ Group(Group(self.seq_range))))("index") + Suppress(self.r_sq_b)))
        #  ####### Declarations

        self.id_set = Group((Group(self.index_select) | self.ID_) + self.eq_set + self.expr)
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

        self.function_decl = Group((Group(self.seq_) | Group(self.int_size) | Group(self.bit_) | Group(self.void_))("return_type") + Group(self.ID)("func_ID") +
                                   Suppress(self.l_bracket) + Group(Optional(delimitedList(Group((self.seq_ | self.int_size | self.bit_) + Group(self.ID)))))("func_param") +  # NOQA
                                   Suppress(self.r_bracket) + Suppress(self.l_brace) + Group(self.stmt)("body") + Suppress(self.r_brace))
        self.function_decl.setParseAction(self.AST.function_decl)

        self.for_init = Literal('(')
        self.for_init.setParseAction(self.AST.begin_for)

        self.for_terminator = Literal(';')
        self.for_terminator.setParseAction(self.AST.for_terminator)

        self.for_increment = Literal(';')
        self.for_increment.setParseAction(self.AST.for_increment)

        self.terminator_expr = Group(infixNotation(Group(self.operand), [(self.log_op, 2, opAssoc.LEFT, self.nest_operand_pairs),
                                                                         (self.bitwise_op, 2, opAssoc.LEFT, self.nest_operand_pairs),
                                                                         (self.comparison_op, 2, opAssoc.LEFT, self.nest_operand_pairs),
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

        self.if_condition = Suppress(self.l_bracket) + self.expr + Suppress(self.r_bracket)
        self.if_condition.setParseAction(self.AST.if_cond)

        self.if_.setParseAction(self.AST.begin_if)
        self.if_body_st = Literal('{')
        self.if_body_st.setParseAction(self.AST.if_body_st)
        self.if_body_end = Literal('}')
        self.if_body_end.setParseAction(self.AST.if_body_end)
        self.if_stmt = Group(self.if_ + self.if_condition("if_cond") + Suppress(self.if_body_st) + Group(self.stmt).setResultsName("body") + Suppress(self.if_body_end))

        self.stmt << ZeroOrMore(self.decl + Suppress(self.term_st)
                                ^ self.function_decl
                                ^ self.id_set + Suppress(self.term_st)
                                ^ self.expr + Suppress(self.term_st)
                                ^ self.for_loop
                                ^ self.if_stmt
                                ^ self.return_stmt + Suppress(self.term_st)
                                ^ self.sbox_call + Suppress(self.term_st))

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


# class TestParser(unittest.TestCase):

#     def test_int_decl_parsing(self):
#         par = Parser()
#         assert_equals(par.parse_test_unit("Int(10) varName;")[1], True)
#         assert_equals(par.parse_test_unit("Int(123) ee;")[1], True)
#         assert_equals(par.parse_test_unit("Int(123) ff"), False)
#         assert_equals(par.parse_test_unit("Int()"), False)
#         assert_equals(par.parse_test_unit("Int(1) ;"), False)
#         assert_equals(par.parse_test_unit("Int(1) test"), False)
#         assert_equals(par.parse_test_unit("Int"), False)
#         assert_equals(par.parse_test_unit("Int(123) gg,jj,test2;")[1], True)
#         assert_equals(par.parse_test_unit("Int Int;"), False)
#         assert_equals(par.parse_test_unit("Int(10) Integer;")[1], True)
#         assert_equals(par.parse_test_unit("Int(10) kk; Int(20) \
#             ll;")[1], True)
#         assert_equals(par.parse_test_unit("Int(10) mm, nn, oo, pp;")[1], True)
#         assert_equals(par.parse_test_unit("Int(10) qq = 10, rr = 4, ss = 5, tt = \
#             7;")[1], True)
#         assert_equals(par.parse_test_unit("Int(10) uu = 10, j, k = 5,\
#             d;")[1], True)
#         assert_equals(par.parse_test_unit("Int(10) l = 10, m, n = 5, \
#          h;")[1], True)
#         assert_equals(par.parse_test_unit("Int(10) o = 10, p, q = 5, \
#          h"), False)
#         assert_equals(par.parse_test_unit("Int(10) r1 = 10, s1, t1 = 5, u1; Int(10) v1, w1=10, \
#             ll1;")[1], True)
#         assert_equals(par.parse_test_unit("Int(10) dd = 10;")[1], True)
#         assert_equals(par.parse_test_unit("Int (123) zz;"), False)

#     def test_bs_decl_parsing(self):
#         par = Parser()
#         assert_equals(par.parse_test_unit("@Int(10) varName;")[1], True)
#         assert_equals(par.parse_test_unit("@Int(10)[10] varName;")[1], True)
#         assert_equals(par.parse_test_unit("@Int(10)[10][10] varName;")[1], True)

#     def test_bit_decl_parsing(self):
#         par = Parser()
#         assert_equals(par.parse_test_unit("Bit a = True;")[1], True)
#         assert_equals(par.parse_test_unit("Bit b, c, d = True;")[1], True)
#         assert_equals(par.parse_test_unit("Bit Bit, c, d = True;"), False)
#         assert_equals(par.parse_test_unit("Bit c, d = function(1,2,3,4);")[1], True)
#         assert_equals(par.parse_test_unit("Bit c, d = function();")[1], True)
#         assert_equals(par.parse_test_unit("Bit c, d = function(1,2,(3*5) << (4 * 5)) + function_2(1,2,(3*5) << (4 * 5));")[1], True)
#         assert_equals(par.parse_test_unit("Bit c, d = 3 + (1+ 2 + 3) * (2 + (Bit) 3);")[1], True)

#     def test_set_parsing(self):
#         par = Parser()
#         par.parse_test_unit("Int b;")
#         par.parse_test_unit("Bit d, e;")
#         assert_equals(par.parse_test_unit("b = 2;")[1], True)
#         assert_equals(par.parse_test_unit("Int = 2;"), False)
#         assert_equals(par.parse_test_unit("d = False;")[1], True)
#         assert_equals(par.parse_test_unit("e = True;")[1], True)
#         assert_equals(par.parse_test_unit("e = True True;"), False)

#     def test_expr_parsing(self):
#         par = Parser()
#         par.parse_test_unit("Int(10) a, b, c, d, e, r; Bit ff;")
#         assert_equals(par.parse_test_unit("((a > 4) && (b > 5)) || d > 3 || (3 << 3);")[1], True)
#         assert_equals(par.parse_test_unit("[[1,2,3,4],[1,2,3,4]] << 3;")[1], True)
#         assert_equals(par.parse_test_unit("a + b;")[1], True)
#         assert_equals(par.parse_test_unit("a + c + d + e;")[1], True)
#         assert_equals(par.parse_test_unit("a + (c + d) + e;")[1], True)
#         assert_equals(par.parse_test_unit("a + c + d + + e;"), False)
#         assert_equals(par.parse_test_unit("a + c + 4 - e;")[1], True)
#         assert_equals(par.parse_test_unit("a + (c) + 4 - e;")[1], True)
#         assert_equals(par.parse_test_unit("a + (c + 4) - (e + r);")[1], True)
#         assert_equals(par.parse_test_unit("a + ((c + d) + 4) - (e + r);")[1], True)
#         assert_equals(par.parse_test_unit("[1,2,3,4] << 2;")[1], True)
#         assert_equals(par.parse_test_unit("([1,2,3,4] << 2) << c;")[1], True)
#         assert_equals(par.parse_test_unit("a;")[1], True)
#         assert_equals(par.parse_test_unit("1;")[1], True)
#         assert_equals(par.parse_test_unit("True;")[1], True)
#         assert_equals(par.parse_test_unit("False;")[1], True)

#     def test_if_parsing(self):
#         par = Parser()
#         par.parse_test_unit("Int a, b, d, e, g;")
#         assert_equals(par.parse_test_unit("if(a==1) { }")[1], True)  # NOQA

#     def test_seq_decl_parsing(self):
#         par = Parser()
#         assert_equals(par.parse_test_unit("@Int(10)[4] a = [1,2,3,4];")[1], True)
#         assert_equals(par.parse_test_unit("[1,2,3,4];")[1], True)
#         assert_equals(par.parse_test_unit("[5*5, function(1,2,3), 4];")[1], True)
#         assert_equals(par.parse_test_unit("[True,False,True,False,True];")[1], True)
#         assert_equals(par.parse_test_unit("[[True,False,True,False,True],[True,False,True,False,True],[True,False,True,False,True]];")[1], True)
#         assert_equals(par.parse_test_unit("Int(10)[4] a;")[1], True)
#         assert_equals(par.parse_test_unit("Bit[4] b;")[1], True)
#         assert_equals(par.parse_test_unit("Bit[4][4] c;")[1], True)
#         assert_equals(par.parse_test_unit("Bit[4][4][4] d;")[1], True)
#         assert_equals(par.parse_test_unit("Bit[4][4] [4] e;"), False)
#         assert_equals(par.parse_test_unit("Bit [4][4] f;"), False)
#         assert_equals(par.parse_test_unit("Bit[4][4] 1;"), False)
#         assert_equals(par.parse_test_unit("Bit[1][4] f = [[True,False,True,True]];")[1], True)
#         assert_equals(par.parse_test_unit("Int(10)[3] g = [5*5, function(1,2,3), 4];")[1], True)

#     def test_seq_op_parsing(self):
#         par = Parser()
#         assert_equals(par.parse_test_unit("a[5,6,7,8:10] = [1,2,3,4,5,6];")[1], True)
#         assert_equals(par.parse_test_unit("Int(10)[6] b = a[5,6,7,8:10];")[1], True)
#         assert_equals(par.parse_test_unit("Int(10) a[5,6,7,8:10];"), False)
#         assert_equals(par.parse_test_unit("a[5,6,7-8:10];")[1], True)
#         assert_equals(par.parse_test_unit("a[5,6,7,8:10]; b[5,6,7,8:10];")[1], True)
#         assert_equals(par.parse_test_unit("a[5] = 10;")[1], True)
#         assert_equals(par.parse_test_unit("a[5] + a[5];")[1], True)

#     def test_for_parsing(self):
#         par = Parser()
#         par.parse_test_unit("Int b, d, e, g;")
#         par.parse_test_unit("Int[4] l;")
#         assert_equals(par.parse_test_unit("for(Int(10) a = 2; ((a > 4) && (b > 5)) || d > 3; d = 5, d = (e * g))\
#             {\
#                 a = 1;\
#             }")[1], True)
#         assert_equals(par.parse_test_unit("for(Int(10) a = 2; ((a > 4) && (b > 5)) || d > 3; d = 5, d = (e * g))\
#             { \
#                 for(d = 3; d < 5; d = d + 1) {\
#                     a = 1;\
#                 }\
#             }")[1], True)  # NOQA
#         assert_equals(par.parse_test_unit("for(;a < 4;){}")[1], True)
#         assert_equals(par.parse_test_unit("for(l[4] = 6 ;a < 4;){}")[1], True)
#         assert_equals(par.parse_test_unit("for(;;){ }")[1], True)

#     def test_function_call_parsing(self):
#         par = Parser()
#         par.parse_test_unit("Int a, b, e;")
#         assert_equals(par.parse_test_unit("func(a, b, 10, 40);")[1], True)
#         assert_equals(par.parse_test_unit("func(a, b, Int[10] a, 40);"), False)
#         assert_equals(par.parse_test_unit("func(a, b, [1,0,1,1], 40);")[1], True)
#         assert_equals(par.parse_test_unit("func (a, b, [1,0,1,1], 40);"), False)
#         assert_equals(par.parse_test_unit("func(a, b, 5 * 3, e * 6);")[1], True)
#         assert_equals(par.parse_test_unit("func(a, b, 5 * 3, e * 6, func(3));")[1], True)
#         assert_equals(par.parse_test_unit("func(1,2,3,4)"), False)
#         assert_equals(par.parse_test_unit("func(1,2,3,4);")[1], True)

#     def sbox_call_parsing(self):
#         par = Parser()
#         par.parse_test_unit("Int a;")
#         assert_equals(par.parse_test_unit("a.sbox(1);")[1], True)
#         assert_equals(par.parse_test_unit("a.sbox(1 * 1);")[1], True)
#         assert_equals(par.parse_test_unit("a.sbox(a);")[1], True)
#         assert_equals(par.parse_test_unit("a. sbox(a);"), False)
#         assert_equals(par.parse_test_unit("a .sbox(a);"), False)
#         assert_equals(par.parse_test_unit("a.sbo x(a);"), False)
#         assert_equals(par.parse_test_unit("a.sbox (a);"), False)

#     def test_shift_op_parsing(self):
#         par = Parser()
#         par.parse_test_unit("Int a;")
#         assert_equals(par.parse_test_unit("a << 3;")[1], True)
#         assert_equals(par.parse_test_unit("a >> 3;")[1], True)
#         assert_equals(par.parse_test_unit("a <<< 3;")[1], True)
#         assert_equals(par.parse_test_unit("a >>> 3;")[1], True)
#         assert_equals(par.parse_test_unit("10 >> 4;")[1], True)
#         assert_equals(par.parse_test_unit("10 >> 4; a >> 4;")[1], True)
#         assert_equals(par.parse_test_unit("([1,2,3,4] >> 4) >> 2 * 4;")[1], True)
#         assert_equals(par.parse_test_unit("(5 >> 4) >> 2 * 4;")[1], True)

#     def test_using_expr_parsing(self):
#         par = Parser()
#         assert_equals(par.parse_test_unit("Int(10) a = (5 * 10) + 3 + (3 * 2);")[1], True)

#     def test_cast_parsing(self):
#         par = Parser()
#         par.parse_test_unit("Int(10) a, b;")
#         assert_equals(par.parse_test_unit("(Int(10)) a;")[1], True)
#         assert_equals(par.parse_test_unit("(Bit) a;")[1], True)
#         assert_equals(par.parse_test_unit("(Int(10)[4]) 10;")[1], True)
#         assert_equals(par.parse_test_unit("(Int(10)[4]) 5 * 3;")[1], True)
#         assert_equals(par.parse_test_unit("(Int(10)[4]) Bit[10];"), False)
#         assert_equals(par.parse_test_unit("(Int(10)[4]) Int;"), False)
#         assert_equals(par.parse_test_unit("(Int(10)[4]) Bit;"), False)
#         assert_equals(par.parse_test_unit("((Bit[10]) a)[5] = True;")[1], True)
#         assert_equals(par.parse_test_unit("Int(10) a = ((Int(10)) op_1) + ((Int(10)) op_2);")[1], True)
#         assert_equals(par.parse_test_unit("Int(10) a = ((Int(10)) op_1);")[1], True)
#         assert_equals(par.parse_test_unit("Int(10) a = (Bit) op_1;")[1], True)
#         assert_equals(par.parse_test_unit("Int(10) a = (Int(10)[2]) op_1;")[1], True)
#         assert_equals(par.parse_test_unit("Int(10) a = (Int(10)[2][2]) op_1;"), False)
#         assert_equals(par.parse_test_unit("Int(10) a = (Bit[10]) op_1;")[1], True)

#     def test_function_dec_parsing(self):
#         par = Parser()
#         assert_equals(par.parse_test_integration("Int(10) function_1(Int(10) a, Bit b) { Int(10) a = 1; Int(10) b = 2; }")[1], True)

#     def test_index_select_parsing(self):
#         par = Parser()
#         assert_equals(par.parse_test_unit("((Int(10)[4]) a)[3];")[1], True)


# class TestASTTree(unittest.TestCase):

#     def test_bit_decl(self):
#         par = Parser()
#         assert_equals(par.parse_test_unit("Bit c, d = 3 + (1 + 2 + 3) * (2 + (Bit) 3 + 2);")[1], True)
#         assert_equals(par.AST.tree[0].node_type,  DATA_TYPE.BIT_DECL)
#         assert_equals(par.AST.tree[1].node_type, DATA_TYPE.BIT_DECL)
#         assert_equals(par.AST.tree[1].value.node_type, DATA_TYPE.EXPR)
#         assert_equals(len(par.AST.tree[1].value.expressions[0].expressions), 3)
#         assert_equals(par.AST.tree[1].value.expressions[0].expressions[0].expressions[0].value, "3")
#         assert_equals(par.AST.tree[1].value.expressions[0].expressions[1].operator, "*")
#         assert_equals(par.AST.tree[1].value.expressions[0].expressions[0].expressions[2].expressions[0].expressions[0].value, "1")
#         assert_equals(par.AST.tree[1].value.expressions[0].expressions[2].expressions[1].operator, "+")
#         assert_equals(par.AST.tree[1].value.expressions[0].expressions[0].expressions[2].expressions[0].expressions[2].value, "2")
#         assert_equals(par.AST.tree[1].value.expressions[0].expressions[0].expressions[2].expressions[1].operator, "+")
#         assert_equals(par.AST.tree[1].value.expressions[0].expressions[2].expressions[2].target.expressions[0].expressions[0].value, "3")

#     def test_int_decl(self):
#         par = Parser()
#         assert_equals(par.parse_test_unit("Int(10) c = 2 + e * (Bit[4]) function(10,10,b * 5), d = 3, e;")[1], True)
#         assert_equals(par.parse_test_unit("Int(10) c =function(b);")[1], True)
#         assert_equals(par.parse_test_unit("Int(10) c = [1,2,3,4];")[1], True)
#         assert_equals(par.AST.tree[0].node_type,  DATA_TYPE.INT_DECL)
#         assert_equals(par.AST.tree[1].node_type,  DATA_TYPE.INT_DECL)
#         assert_equals(par.AST.tree[2].node_type,  DATA_TYPE.INT_DECL)
#         assert_equals(par.AST.tree[0].ID, "c")
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].expressions[0].value,  "2")
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[1].operator,  "*")
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].expressions[2].ID,  "e")
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[1].operator,  "*")
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[2].node_type, DATA_TYPE.CAST)
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[2].target.expressions[0].ID, "function")
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[2].target.expressions[0].parameters[0].expressions[0].value, "10")

#     def test_bs_decl(self):
#         par = Parser()
#         assert_equals(par.parse_test_unit("@Int(10) varName;")[1], True)
#         assert_equals(par.AST.tree[0].node_type, DATA_TYPE.BS_INT_DECL)
#         assert_equals(par.parse_test_unit("Int(10) varName;")[1], True)
#         assert_equals(par.AST.tree[1].node_type, DATA_TYPE.INT_DECL)
#         assert_equals(par.parse_test_unit("@Int(10)[10] varName;")[1], True)
#         assert_equals(par.AST.tree[2].node_type, DATA_TYPE.BS_SEQ_INT_DECL)
#         assert_equals(par.parse_test_unit("Int(10)[10] varName;")[1], True)
#         assert_equals(par.AST.tree[3].node_type, DATA_TYPE.SEQ_INT_DECL)
#         assert_equals(par.parse_test_unit("Bit[10] varName;")[1], True)
#         assert_equals(par.AST.tree[4].node_type, DATA_TYPE.SEQ_BIT_DECL)

#     def test_int_seq_decl(self):
#         par = Parser()
#         assert_equals(par.parse_test_unit("Int(10)[5] a = [1,function(1,2,3),function(), (1*2*3) << 4, d + e];")[1], True)
#         assert_equals(par.parse_test_unit("Int(10)[2][2] f = [[1,2],[3,4]];")[1], True)
#         assert_equals(par.parse_test_unit("Int(10)[2][2][2] f = [[[[1 * 2 * 3,2],[(Int(10)) [1,2,3,4],3]]],[[[5,6],[7,8]]]];")[1], True)
#         assert_equals(par.parse_test_unit("[1,2,3,4];")[1], True)
#         assert_equals(par.parse_test_unit("Int(10)[1][2] b = [[],[]];")[1], True)
#         assert_equals(par.parse_test_unit("Int(10)[5] b = c[1,2,3:5];")[1], True)
#         assert_equals(par.parse_test_unit("Int(10)[5] b;")[1], True)
#         assert_equals(par.AST.tree[0].ID, "a")
#         assert_equals(par.AST.tree[0].bit_constraints.expressions[0].value, "10")
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].node_type, DATA_TYPE.SEQ_VAL)
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[0].expressions[0].value, "1")
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[1].expressions[0].parameters[0].expressions[0].value, "1")
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[3].expressions[0].expressions[0].expressions[0].expressions[0].value, "1")
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[3].expressions[0].expressions[0].expressions[1].operator, "*")
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[3].expressions[0].expressions[0].expressions[0].expressions[2].value, "2")
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[3].expressions[0].expressions[1].operator, "<<")
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[3].expressions[0].expressions[2].value, "4")
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[4].expressions[0].expressions[0].ID, "d")
#         assert_equals(par.parse_test_unit("Int(10) z = b[1 * 4];")[1], True)
#         assert_equals(par.AST.tree[6].ID, "z")
#         assert_equals(par.AST.tree[6].value.expressions[0].ID, "b")
#         assert_equals(par.AST.tree[6].value.expressions[0].indices[0].expressions[0].expressions[0].expressions[0].value, "1")
#         assert_equals(par.AST.tree[6].value.expressions[0].indices[0].expressions[0].expressions[0].expressions[1].operator, "*")
#         assert_equals(par.AST.tree[6].value.expressions[0].indices[0].expressions[0].expressions[0].expressions[2].value, "4")
#         assert_equals(par.parse_test_unit("Int(10) a = 2;")[1], True)

#     def test_bit_seq_decl(self):
#         par = Parser()
#         assert_equals(par.parse_test_unit("Bit[5] b = [True, False, True, False];")[1], True)
#         assert_equals(par.parse_test_unit("Bit[1][2] b = [[True, False, True, False],[True, False, True, False]];")[1], True)
#         assert_equals(par.parse_test_unit("Bit[1][2] b = [[],[]];")[1], True)
#         assert_equals(par.parse_test_unit("Bit[1] b = [];")[1], True)
#         assert_equals(par.parse_test_unit("Bit[1] b;")[1], True)
#         assert_equals(par.AST.tree[0].node_type, DATA_TYPE.SEQ_BIT_DECL)
#         assert_equals(par.AST.tree[0].size[0].expressions[0].value, "5")
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[0].expressions[0].value, "True")
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[1].expressions[0].value, "False")

#     def test_id_set(self):
#         par = Parser()
#         assert_equals(par.parse_test_unit("a = b + 10 * function(a, b);")[1], True)
#         assert_equals(par.parse_test_unit("a = [];")[1], True)
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].expressions[0].ID, "b")
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[1].operator, "*")
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[2].parameters[0].expressions[0].ID, "a")
#         assert_equals(par.AST.tree[0].value.expressions[0].expressions[2].parameters[1].expressions[0].ID, "b")
#         assert_equals(par.parse_test_unit("a[1,2,3,4:5] = (Bit[4]) b + 10 * function(a, b);")[1], True)
#         assert_equals(par.AST.tree[2].target.indices[0].expressions[0].expressions[0].value, "1")
#         assert_equals(par.AST.tree[2].target.indices[0].expressions[1].expressions[0].value, "2")
#         assert_equals(par.AST.tree[2].target.indices[0].expressions[3].expressions[0].start.expressions[0].value, "4")
#         assert_equals(par.AST.tree[2].value.expressions[0].target.expressions[0].expressions[2].node_type, DATA_TYPE.FUNCTION_CALL)
#         assert_equals(par.parse_test_unit("a[1,2][1,2,3,4:5] = (Bit[4]) b + 10 * function(a, b);")[1], True)
#         assert_equals(par.parse_test_unit("a[5,6,7,8:10] = [1,2,3,4,5,6];")[1], True)
#         assert_equals(par.AST.tree[4].node_type, DATA_TYPE.ID_SET)
#         assert_equals(par.AST.tree[4].target.indices[0].expressions[0].expressions[0].value, "5")

#     def test_func_decl(self):
#         par = Parser()
#         assert_equals(par.parse_test_integration("Bit function_1(Int(5) a, Bit b, Int(5)[4][4][4] test, Bit[5] b) { Int(10) a = 1; Int(10) b = 2; Int(10) c = 0xa; }")[1], True)  # NOQA
#         assert_equals(par.AST.tree[0].ID, "function_1")
#         assert_equals(len(par.AST._statements), 0)
#         assert_equals(par.AST.tree[0].stmts[0].value.expressions[0].value, '1')
#         assert_equals(par.AST.tree[0].stmts[1].value.expressions[0].value, '2')
#         assert_equals(par.AST.tree[0].stmts[2].value.expressions[0].value, '10')

#     def test_return_stmt(self):
#         par = Parser()
#         assert_equals(par.parse_test_unit("return a * b * c * 10;")[1], True)
#         assert_equals(par.AST.tree[0].node_type, DATA_TYPE.RETURN_STMT)
#         assert_equals(par.AST.tree[0].expr.expressions[0].expressions[0].expressions[0].expressions[0].ID, "a")
#         assert_equals(par.AST.tree[0].expr.expressions[0].expressions[0].expressions[1].operator, "*")

#     def test_for_loop(self):
#         par = Parser()
#         assert_equals(par.parse_test_unit("for(Int(10) a = 5, Bit f = False; (a < 5) && (d < 5); a = a + 1, b = b + 3) { b = b <<< 1; z = b + 19; }")[1], True)
#         assert_equals(par.parse_test_unit("for(;;) { }")[1], True)
#         assert_equals(par.AST.tree[0].node_type, DATA_TYPE.FOR_LOOP)
#         assert_equals(par.AST.tree[1].node_type, DATA_TYPE.FOR_LOOP)
#         assert_equals(par.AST.tree[0].terminator[0].expressions[0].expressions[1].operator, "&&")
#         assert_equals(par.AST.tree[0].body[0].node_type, DATA_TYPE.ID_SET)
#         assert_equals(par.AST.tree[0].body[0].target.ID, "b")

#     def test_if_stmt(self):
#         par = Parser()
#         assert_equals(par.parse_test_unit("if(i > 3) { b = b + 1; c = d + 3; } if(d < 4) { z = z + 1; kk = k + 3; }")[1], True)
#         assert_equals(par.AST.tree[0].node_type, DATA_TYPE.IF_STMT)
#         assert_equals(par.AST.tree[1].node_type, DATA_TYPE.IF_STMT)
#         assert_equals(par.AST.tree[0].condition[0].expressions[0].expressions[0].expressions[0].ID, "i")
#         par = Parser()
#         assert_equals(par.parse_test_unit("if(i > 3) { if(d < 4) { z = z + 1; kk = k + 3; } } ")[1], True)
#         assert_equals(par.AST.tree[0].body[0].condition[0].expressions[0].expressions[0].expressions[0].ID, "d")

#     def test_casting(self):
#         par = Parser()
#         assert_equals(par.parse_test_unit("a =(@Int(10)) a;")[1], True)

#     def test_indexing(self):
#         par = Parser()
#         assert_equals(par.parse_test_unit("((Bit[4]) ((Int(5)) a))[5] = True;")[1], True)
#         assert_equals(par.parse_test_unit("a[5] = True;")[1], True)

#     def test_sbox(self):
#         par = Parser()
#         assert_equals(par.parse_test_unit("Sbox(4)[16] prince = [0xb, 0xf, 0x3, 0x2, 0xa, 0xc, 0x9, 0x1, 0x6, 0x7, 0x8, 0x0, 0xe, 0x5, 0xd, 0x4];")[1], True)

# class TestSemanticAnalysis(unittest.TestCase):

#     def test_int_decl(self):
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 4 << [1,2,3,4] << 2;")), False)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 4 << 3 << 2;")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10;")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10; Int(10) a = 20;")), False)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10; Int(10) b = 20;")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10; Int(10) b = a;")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = False;")), False)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10 + False << 4;")), False)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a; Int(10) b = a;")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(10) a; Int(10) b = a + 3;")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(10) a; Int(10) b = 3 + 3 * (4 << a);")), True)

#     def test_bit_decl(self):
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit a = False;")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit a = 1;")), False)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit a = False + False;")), False)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit a = False; Bit a = True;")), False)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit a; Bit b = a;")), True)

#     def test_mixing_bit_int(self):
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Bit b = True;")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Bit b = True; Int(10) c = b;")), False)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Bit b = True; Int(10) c = 5 * (b);")), False)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Int(10) b = 10; Int(10) c = 5 * (b);")), True)

#     def test_id_set(self):
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Int(10) b = a;")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Int(10) b = a; Bit c = b;")), False)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Int(10) b = a * 10 * 3 << 4;")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Bit d = False; Int(10) b = a * 10 * 3 << d;")), False)

#     def test_seq_decl(self):
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2][2] a = [[1,2],[3,4]]; ")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2][2] a = [[False,2],[3,4]]; ")), False)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2] a = [1, 2, 3, 4]; ")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2] a = [1]; ")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2] a = [1,2,3,4] ^ [1,2,3,4];")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2] a = ([1,2,3,4] ^ [1,2,3,4]) ^ ([1,2,3,4] ^ [1,2,3,4]);")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2] a = ([1,2,3,4] ^ [1,2,3,4]) ^ ([1,2,3,4] << 4);")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2] a = ([1,2,3,4] ^ [1,2,3,4]) ^ ([[1],[2],[3],[4]] << 4);")), False)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2] b = [1,2]; Int(10)[2] a = ([1,2,3,4] ^ [1,2,3,4]) ^ ([1,2,3,4] << b[0]);")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) b = 3; Int(10)c = 4; Int(10)[2] a = [b,2,c,4] ^ [1,2,b * 2,4];")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) b = 3; Int(10)c = 4; Bit d = False; Int(10)[2] a = [b,d,c,4] ^ [1,2,b,4];")), False)  # NOQA
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[4] a = [1,2,3,4];")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(a * a)[4] a = [1,2,3,4];")), False)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[4] a = [1,2,3,4]; Int(10) c; c = a;")), False)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[4] a = [True,False,True,False];")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[4] a = [True,False,True,False,[True, False]];")), False)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[4] a = [1,False,True,False];")), False)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[4][4] a = [[True,False,True,False],[True,False,True,False]];")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[2][2] a = [[[1],[2]],[[1],[2]]];")), False)  # NOQA
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[2][2][1] a = [[[1],[2]],[[1],[2]]];")), True)  # NOQA

#     def test_bs_seq_decl(self):
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(10)[10] a = [1,2,3,4,5,6,7,8,9,10]; ")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(10)[2][2] a = [[1,2], [3,4]]; ")), True)

#     def test_if_stmt(self):
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) a = 4; if((4 > 4) && (4 < 6)) { a = 10; }")), True)

#     def test_for_loop(self):
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("for(Int(10) i = 5, Bit b = False; b != True; i = i + 5) { b = True; }")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("for(Int(10) i = 5, Bit b = False; b != True; i = i + 5) { b = True; } b = True;")), False)  # NOQA b is out of scope!
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit b; for(Int(10) i = 5; b != True; i = i + 5) { b = True; } b = True;")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit b; for(Int(10) i = 5; b != True; i = i + 5) { b = True; } b = 10;")), False)

#     def test_func_decl(self):
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8) test_func(Int(8) a, Bit c, Bit[5] e) { Int(10) d = 1;  Bit b = False; }")), True)  # NOQA
#         assert_equals(par.semantic_analyser.sym_table.f_table['test_func']['return_type'], DATA_TYPE.INT_VAL)

#     def test_func_call(self):
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) test_func(Int(10) a) { Int(10) d = test_func(test_func(10)) + 20; }")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit test_func(Int(10) a) { Int(10) d = 10; }")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit test_func1(Int(10) a) { a = a + 10; }\
#                                                                             Int(10) test_func(Int(10) a) { Int(10) d = test_func(test_func1(10)) + 20; }")), False)  # NOQA
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) test_func2(Bit a) { Int(10) d = 39; }\
#                                                                             Bit test_func1(Bit a) { Int(10) d = 10; }\
#                                                                             Int(10) test_func(Int(10) a) { Int(10) d = test_func(test_func2(test_func1(False))) + 20; }")), True)  # NOQA
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(10) test_func2(Bit a) { Int(10) d = 39; }\
#                                                                             void test_func3(Bit a) { @Int(10) i = test_func2(False); }")), True)
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(10) test_func2(@Int(8) c) { c = 4 + 39; }")), True)

#     def test_casting(self):
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[4] op_1 = [False, False, False, True];\
#                                                                             Bit[4] op_2 = [False, False, False, True];\
#                                                                             Int(10) a = ((Int(10)) op_1) + ((@Int(10)) op_2);")), True)

#     def test_seq_operations(self):
#         par = Parser()
#         assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) b = 10; Bit[2][10] a; a[1][1,2,3,4:5] = [((Bit[4]) (b + 10))[2]];")), True)


class test_IR_generation(unittest.TestCase):

    # def test_int_decl(self):
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10;")), True)
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10 + 5;")), True)
    #     assert_equals(par.semantic_analyser.IR.IR[0].node_type, DATA_TYPE.INT_DECL)
    #     assert_equals(par.semantic_analyser.IR.IR[0].value.left.value, "10")
    #     assert_equals(par.semantic_analyser.IR.IR[0].value.right.value, "5")
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10 + (5 * 4);")), True)
    #     assert_equals(par.semantic_analyser.IR.IR[0].value.left.value, "10")
    #     assert_equals(par.semantic_analyser.IR.IR[0].value.right.operator, "*")
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = False;")), False)

    # def test_bit_seq_decl(self):
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[4] a = [[True,False],[True,False]];")), True)
    #     assert_equals(par.semantic_analyser.IR.IR[0].node_type, DATA_TYPE.SEQ_BIT_DECL)
    #     assert_equals(par.semantic_analyser.IR.IR[0].value.type, DATA_TYPE.SEQ_BIT_VAL)
    #     assert_equals(par.semantic_analyser.IR.IR[0].value.type, DATA_TYPE.SEQ_BIT_VAL)
    #     assert_equals(par.semantic_analyser.IR.IR[0].value.value[0].value[0].value, "True")
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[4] a;")), True)

    # def test_int_seq_decl(self):
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) b = 3; Int(10)c = 4; Int(10)[2][2] a = [[b * 4,5],[c / 5, 5]];")), True)
    #     assert_equals(par.semantic_analyser.IR.IR[2].value.value[0].value[0].node_type, DATA_TYPE.ARITH_OP)
    #     assert_equals(par.semantic_analyser.IR.IR[2].value.value[0].value[0].left.name, "b")
    #     assert_equals(par.semantic_analyser.IR.IR[2].value.value[0].value[0].left.type, DATA_TYPE.INT_VAL)
    #     assert_equals(par.semantic_analyser.IR.IR[2].value.value[1].value[0].node_type, DATA_TYPE.ARITH_OP)
    #     assert_equals(par.semantic_analyser.IR.IR[2].value.value[1].value[0].left.name, "c")
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) b = 3; Int(10)c = 4; Int(10)[2][2] a = [[b << 3,5],[c / 5, 5]];")), True)
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit d = False; Int(10) b = 3; Int(10)c = 4; Int(10)[2][2] a = [[b << d,5],[c / 5, 5]];")), False)  # NOQA

    # def test_if_stmt(self):
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) a = 4; if((4 > 4) && (4 < 6)) { a = 10; }")), True)
    #     assert_equals(par.semantic_analyser.IR.IR[1].node_type, DATA_TYPE.IF_STMT)
    #     assert_equals(len(par.semantic_analyser.IR.IR), 2)
    #     assert_equals(par.semantic_analyser.IR.IR[1].body[0].node_type, DATA_TYPE.ID_SET)
    #     assert_equals(par.semantic_analyser.IR.IR[1].condition.operator, "&&")
    #     assert_equals(par.semantic_analyser.IR.IR[1].condition.left.operator, ">")
    #     assert_equals(par.semantic_analyser.IR.IR[1].condition.left.type, DATA_TYPE.BIT_VAL)
    #     assert_equals(par.semantic_analyser.IR.IR[1].condition.left.left.value, "4")
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) row = 0; if(row == 0 || row == 2)    { }")), True)
    #     assert_equals(par.semantic_analyser.IR.IR[1].condition.operator, "||")
    #     assert_equals(par.semantic_analyser.IR.IR[1].condition.left.operator, "==")
    #     assert_equals(par.semantic_analyser.IR.IR[1].condition.left.right.value, "0")

    # def test_for_loop(self):
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("for(Int(8) d, Int(8) a = 0, Int(8)[5] e = [1,2,3,4,5], Bit[4] f; a < 10; a = a + 1, d = d * a) {\
    #                                                                         d = d << 10;\
    #                                                                         e = e << 4;\
    #                                                                         f = f << 4;\
    #                                                                      }")), True)
    #     assert_equals(par.semantic_analyser.IR.IR[0].node_type, DATA_TYPE.FOR_LOOP)
    #     assert_equals(par.semantic_analyser.IR.IR[0].initializer[0].node_type, DATA_TYPE.INT_DECL)
    #     assert_equals(par.semantic_analyser.IR.IR[0].initializer[0].ID.name, "d")
    #     assert_equals(par.semantic_analyser.IR.IR[0].terminator[0].operator, "<")
    #     assert_equals(par.semantic_analyser.IR.IR[0].terminator[0].left.name, "a")
    #     assert_equals(par.semantic_analyser.IR.IR[0].terminator[0].left.type, DATA_TYPE.INT_VAL)
    #     assert_equals(par.semantic_analyser.IR.IR[0].increment[1].node_type, DATA_TYPE.ID_SET)
    #     assert_equals(par.semantic_analyser.IR.IR[0].increment[1].value.operator, "*")
    #     assert_equals(par.semantic_analyser.IR.IR[0].increment[1].value.left.name, "d")
    #     assert_equals(par.semantic_analyser.IR.IR[0].body[0].node_type, DATA_TYPE.ID_SET)
    #     assert_equals(par.semantic_analyser.IR.IR[0].body[0].value.type, DATA_TYPE.INT_VAL)
    #     assert_equals(par.semantic_analyser.IR.IR[0].body[0].value.left.name, "d")
    #     assert_equals(par.semantic_analyser.IR.IR[0].body[2].value.type, DATA_TYPE.SEQ_BIT_VAL)
    #     assert_equals(par.semantic_analyser.IR.IR[0].body[2].value.right.value, "4")

    # def test_func_decl(self):
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8) test_func(Int(8) a, Bit c, Bit[5] e, @Int(64) f) { Int(10) d = (1 + 3) + f;  Bit b = False; }")), True)  # NOQA
    #     assert_equals(par.semantic_analyser.IR.IR[0].parameters[3].ID.type, DATA_TYPE.BS_INT_VAL)
    #     assert_equals(par.semantic_analyser.IR.IR[0].body[0].value.type, DATA_TYPE.BS_INT_VAL)
    #     assert_equals(par.semantic_analyser.IR.IR[0].body[0].value.left.type, DATA_TYPE.INT_VAL)

    # def test_index_setting(self):
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[8][8] a = [[1,2,3,4],[5,6,7,8]]; a[3][2] = 5;")), True)  # NOQA
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[8] a = [1,2,3,4,5,6,7,8]; a[3][2] = True;")), True)  # NOQA
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[8] a = [1,2,3,4,5,6,7,8]; a[3] = [1,2,3,4,5,5];")), False)  # NOQA
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[8][2] a = [[1,2,3,4],[5,6,7,8]]; a[3] = [1,2];")), True)  # NOQA
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[8][2][1] a = [[[1]],[[5]]]; a[3][3][3] = 1;")), True)  # NOQA
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[8][2] a = [1,2,3,4,5,6,7,8]; a[3][3][3] = 1;")), False)  # NOQA
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[8][8] a = [[1,2,3,4],[5,6,7,8]]; a[3][2] = (1 * ((Int(4)) [True, False, True, False])) << 4;")), True)  # NOQA
    #     assert_equals(par.semantic_analyser.IR.IR[1].value.operator, "<<")
    #     assert_equals(par.semantic_analyser.IR.IR[1].value.left.right.type, DATA_TYPE.INT_VAL)
    #     assert_equals(par.semantic_analyser.IR.IR[1].value.left.right.target.value[0].value, "True")
    #     assert_equals(par.semantic_analyser.IR.IR[1].value.left.right.target.value[1].value, "False")
    #     assert_equals(par.semantic_analyser.IR.IR[1].value.left.right.target.value[2].value, "True")
    #     assert_equals(par.semantic_analyser.IR.IR[1].value.left.right.target.value[3].value, "False")
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[8][8] a = [[1,2,3,4],[5,6,7,8]]; a[3] = (1 * ((Int(4)) [True, False, True, True])) << 4;")), False)  # NOQA
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) a = 8; ((Bit[4]) a)[6] = True;")), True)  # NOQA
    #     assert_equals(par.semantic_analyser.IR.IR[1].node_type, DATA_TYPE.ID_SET)
    #     assert_equals(par.semantic_analyser.IR.IR[1].target.target.target.name, "a")
    #     assert_equals(par.semantic_analyser.IR.IR[1].target.target.operation.seq_size[0].value, "4")
    #     assert_equals(par.semantic_analyser.IR.IR[1].target.indices[0][0].value, "6")
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) a = 8; ((Bit[4]) a)[4][4] = True;")), False)  # NOQA
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) b = 4; Int(4)[5] a = [1,2,3,4,5]; a[b * 4: 4] = [10];")), True)  # NOQA
    #     assert_equals(par.semantic_analyser.IR.IR[2].target.type, DATA_TYPE.SEQ_INT_VAL)
    #     assert_equals(par.semantic_analyser.IR.IR[2].value.type, DATA_TYPE.SEQ_INT_VAL)
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) b = 4; Int(4)[5] a = [1,2,3,4,5]; a[b * 4: 4] = 10;")), False)  # NOQA Must assign sequence to range value
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) b = 4; Int(4)[5] a = [1,2,3,4,5]; a[b * 4: 4] = [1,2,3];")), True)  # NOQA
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit b = True; Int(4)[5] a = [1,2,3,4,5]; a[b: 4] = 10;")), False)  # NOQA
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit b = True; Int(4)[5] a = [1,2,3,4,5]; a[((Int(1)) b): 4] = [10];")), True)  # NOQA
    #     assert_equals(par.semantic_analyser.IR.IR[2].target.indices[0][0].start.target.name, "b")

    # def test_int_index_select(self):
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) a = 10; a[5] = True;")), True)  # NOQA
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) a = 10; a[5 : 8] = [True,False,True];")), True)  # NOQA
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) a = 10; a[1] = a[2] ^ a[3];")), True)  # NOQA
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) a = 10; a[1] = a[2][1] ^ a[3];")), False)  # NOQA
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4)[5] a = [1,2,3,4,5]; a[1][1] = a[1][1] ^ a[1][2];")), True)  # NOQA
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) a = 10; a[1] = a[2] ^ a[4] ^ a[6];")), True)  # NOQA
    #     assert_equals(par.semantic_analyser.IR.IR[1].target.type, DATA_TYPE.BIT_VAL)
    #     assert_equals(par.semantic_analyser.IR.IR[1].value.left.type, DATA_TYPE.BIT_VAL)
    #     assert_equals(par.semantic_analyser.IR.IR[1].value.type, DATA_TYPE.BIT_VAL)
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) a = 10; a[1] = 1;")), False)  # NOQA
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4)[5] a = [1,2,3,4,5]; a[1,2,3][5 : 8] = [True,False,True];")), True)  # NOQA
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4)[5] a = [1,2,3,4,5]; a[1,2,3][5 : 8][4] = [True,False,True];")), False)  # NOQA

    # def test_casting(self):
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[4] output; Int(4) Input; Input[0] = ((Int(4)) output)[0];")), True)

    # def test_sbox(self):
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Sbox(4)[16] prince = [0xb, 0xf, 0x3, 0x2, 0xa, 0xc, 0x9, 0x1, 0x6, 0x7, 0x8, 0x0, 0xe, 0x5, 0xd, 0x4]; Int(64) a = 10;\
    #                                                                         a[0:4] = (Bit[4]) prince[a[0:4]];")), True)
    #     assert_equals(par.semantic_analyser.IR.IR[2].value.target.indices[0][0].type, DATA_TYPE.SEQ_BIT_VAL)

    # def test_LFSR_syntax(self):
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4)[4] a = [1,2,3,4]; a[1] = a[5] ^ a[5] ^ a[5];")), True)  # NOQA
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(8) lfsr(@Int(8) state) {\
    #                                                                         Int(1) output;\
    #                                                                         Int(1) input;\
    #                                                                         for(Int(5) i = 0; i < 32; i = i + 1) {\
    #                                                                             output[0] = state[0];\
    #                                                                             input[0] =  state[0] ^ state[4] ^ state[5] ^ state[6];\
    #                                                                             state = state << 1;\
    #                                                                             state[7] = input[0];\
    #                                                                          }\
    #                                                                     }")), True)  # NOQA
    #     assert_equals(par.semantic_analyser.IR.IR[0].node_type, DATA_TYPE.FUNC_DECL)
    #     par = Parser()
    #     assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(8) lfsr(@Int(8) state) {\
    #                                                                         Bit output;\
    #                                                                         Bit input;\
    #                                                                         for(Int(5) i = 0; i < 32; i = i + 1) {\
    #                                                                             output = state[0];\
    #                                                                             input = state[0] ^ state[4] ^ state[5] ^ state[6];\
    #                                                                             state = state << 1;\
    #                                                                             state[7] = input;\
    #                                                                         }\
    #                                                                     }")), True)  # NOQA

    def test_LED_syntax(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(4)[16] shift_row(@Int(4)[16] state)  {\
                                                                            state[0 : 3 ] = state[0 : 3] <<< 0;\
                                                                            state[4 : 7] = state[4 : 7] <<< 1;\
                                                                            state[8 : 11] = state[8 : 11] <<< 2;\
                                                                            state[12 : 15] = state[12 : 15] <<< 3;\
                                                                         }")), True)
        assert_equals(par.semantic_analyser.IR.IR[0].node_type, DATA_TYPE.FUNC_DECL)
        assert_equals(par.semantic_analyser.IR.IR[0].body[0].target.target.name, "state")
        assert_equals(par.semantic_analyser.IR.IR[0].body[0].value.operator, "<<<")
        assert_equals(par.semantic_analyser.IR.IR[0].body[0].value.type, DATA_TYPE.BS_SEQ_INT_VAL)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(64) sBox_layer(@Int(4)[16] state, Sbox(4)[16] s)  {\
                                                                            for(Int(4) i = 0; i < 16; i = i + 1){\
                                                                                state[i] = s[state[i]];\
                                                                            }\
                                                                         }\
                                                                        @Int(4) gmMult(@Int(4) a, @Int(4) b) {\
                                                                            Int(4) g = 0;\
                                                                            for(Int(4) i = 0; i < 4; i = i + 1)   {\
                                                                                if(((Bit[4]) b)[0] == True)   {\
                                                                                    g = g ^ a;\
                                                                                }\
                                                                                a = a << 1;\
                                                                                if(((Bit[4]) a)[3] == True)   {\
                                                                                    a = a ^ 0x13;\
                                                                                }\
                                                                                b = b >> 1;\
                                                                            }\
                                                                        }\
                                                                        @Int(4) MixColumnSerial(@Int(4)[16] state, Int(4)[16] MDS) {\
                                                                            Int(4)[4] column;\
                                                                            for(Int(4) c = 0; c < 4; c = c + 1)  {\
                                                                                column = state[c,c + 4,c + 8,c + 12];\
                                                                                for(Int(4) r = 0; r < 4; r = r + 4)  {\
                                                                                    state[(4*c) + r] = gmMult(MDS[4 * c], column[0]) ^\
                                                                                        gmMult(MDS[(4 * c) + 1],column[1]) ^\
                                                                                        gmMult(MDS[(4 * c) + 2],column[2]) ^\
                                                                                        gmMult(MDS[(4 * c) + 3],column[3]);\
                                                                                }\
                                                                            }\
                                                                        }\
                                                                        @Int(4)[16] addConstants(@Int(4)[16] state, @Int(5) constant)  {\
                                                                            Int(4)[16] roundConstant;\
                                                                            for(Int(4) row = 0; row < 4; row = row + 1)  {\
                                                                                roundConstant[row * 4] = row;\
                                                                                if(row == 0 || row == 2)    {\
                                                                                    roundConstant[(row * 4) + 1] = (Int(4)) constant[3:5];\
                                                                                }\
                                                                                if(row == 1 || row == 3) {\
                                                                                    roundConstant[(row * 4) + 1] = (Int(4)) constant[0:2];\
                                                                                }\
                                                                                roundConstant[(row * 4) + 2] = 0;\
                                                                                roundConstant[(row * 4) + 3] = 0;\
                                                                            }\
                                                                            state = state ^ roundConstant;\
                                                                        }\
                                                                        @Int(4)[16] shift_row(@Int(4)[16] state)   {\
                                                                            state[0 : 3 ] = state[0 : 3] <<< 0;\
                                                                            state[4 : 7] = state[4 : 7] <<< 1;\
                                                                            state[8 : 11] = state[8 : 11] <<< 2;\
                                                                            state[12 : 15] = state[12 : 15] <<< 3;\
                                                                        }")), True)

    def test_PRESENT_syntax(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(64) pLayer(@Int(64) state) {\
                                                                            Int(8) target_bit;\
                                                                            @Int(64) temp = state;\
                                                                            for(Int(8) bit = 0; bit < 64; bit = bit + 1)    {\
                                                                                target_bit = (16*bit) % 63;\
                                                                                if(bit == 63)   {\
                                                                                    target_bit = 63;\
                                                                                }\
                                                                                state[target_bit] = temp[bit];\
                                                                            }\
                                                                        }\
                                                                            void sBox_layer(@Int(64) state, Sbox(4)[16] s)  {\
                                                                                for(Int(4) i = 0; i < 16; i = i + 1){\
                                                                                    state[(i * 4) : (i * 4) + 4] = (Bit[4]) s[state[(i * 4) : (i * 4) + 4]];\
                                                                                }\
                                                                            }\
                                                                        @Int(64)[32] generate_round_keys(@Int(80) key, Int(4)[16] sBox) {\
                                                                            @Int(64)[32] round_keys;\
                                                                            for(Int(5) round = 0; round < 32; round = round + 1)    {\
                                                                                round_keys[round][0: 63] = key[16:79];\
                                                                                key = key <<< 61;\
                                                                                key[76 : 79] = sBox[key[79:76]][0 : 4];\
                                                                                key[15 : 19] = key[15 : 19] ^ round[0 : 5];\
                                                                            }\
                                                                        }")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(64)[32] generate_round_keys(@Int(80) key, Int(4)[16] sBox) {\
                                                                            @Int(64)[32] round_keys;\
                                                                            for(Int(5) round = 0; round < 32; round = round + 1)    {\
                                                                                round_keys[round][0: 63] = key[16:79];\
                                                                                key = key <<< 61;\
                                                                                key[76 : 79] = (Bit[4]) sBox[key[76:79]];\
                                                                                key[15 : 19] = key[15 : 19] ^ round[0 : 5];\
                                                                            }\
                                                                        }")), True)

    def test_PRINCE_syntax(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(64) enc(@Int(64) state, @Int(64) key_0, @Int(64) key_1) {\
                                                                            Int(64)[11] RC= [0x0000000000000000,\
                                                                                            0x13198a2e03707344,\
                                                                                            0xa4093822299f31d0,\
                                                                                            0x082efa98ec4e6c89,\
                                                                                            0x452821e638d01377,\
                                                                                            0xbe5466cf34e90c6c,\
                                                                                            0x7ef84f78fd955cb1,\
                                                                                            0x85840851f1ac43aa,\
                                                                                            0xc882d32f25323c54,\
                                                                                            0x64a51195e0e3610d,\
                                                                                            0xd3b5a399ca0c2399,\
                                                                                            0xc0ac29b7c97c50dd];\
                                                                            @Int(64) key_prime = (key_0 >>> 1) ^ (key_0 >> 63);\
                                                                                state = state ^ key_1;\
                                                                                state = state ^ RC[0];\
                                                                        }\
                                                                        void sBox_layer(@Int(64) state, Sbox(4)[16] s)  {\
                                                                            for(Int(4) i = 0; i < 16; i = i + 1){\
                                                                                state[(i * 4) : (i * 4) + 4] = (Bit[4]) s[state[(i * 4) : (i * 4) + 4]];\
                                                                            }\
                                                                        }\
                                                                        Bit[16] m1(Bit[16] state)   {\
                                                                            Bit[16] output;\
                                                                            output[ 0] = state[0] ^ state[ 4] ^ state[ 8];\
                                                                            output[ 1] = state[5] ^ state[ 9] ^ state[13];\
                                                                            output[ 2] = state[2] ^ state[10] ^ state[14];\
                                                                            output[ 3] = state[3] ^ state[ 7] ^ state[15];\
                                                                            output[ 4] = state[0] ^ state[ 4] ^ state[12];\
                                                                            output[ 5] = state[1] ^ state[ 5] ^ state[ 9];\
                                                                            output[ 6] = state[6] ^ state[10] ^ state[14];\
                                                                            output[ 7] = state[3] ^ state[11] ^ state[15];\
                                                                            output[ 8] = state[0] ^ state[ 8] ^ state[12];\
                                                                            output[ 9] = state[1] ^ state[ 5] ^ state[13];\
                                                                            output[10] = state[2] ^ state[ 6] ^ state[10];\
                                                                            output[11] = state[7] ^ state[11] ^ state[15];\
                                                                            output[12] = state[4] ^ state[ 8] ^ state[12];\
                                                                            output[13] = state[1] ^ state[ 9] ^ state[13];\
                                                                            output[14] = state[2] ^ state[ 6] ^ state[14];\
                                                                            output[15] = state[3] ^ state[ 7] ^ state[11];\
                                                                        }\
                                                                        \
                                                                        Bit[16] m0(Bit[16] state)   {\
                                                                            Bit[16] output;\
                                                                            output[ 0] = state[4] ^ state[ 8] ^ state[12];\
                                                                            output[ 1] = state[1] ^ state[ 9] ^ state[13];\
                                                                            output[ 2] = state[2] ^ state[ 6] ^ state[14];\
                                                                            output[ 3] = state[3] ^ state[ 7] ^ state[11];\
                                                                            output[ 4] = state[0] ^ state[ 4] ^ state[ 8];\
                                                                            output[ 5] = state[5] ^ state[ 9] ^ state[13];\
                                                                            output[ 6] = state[2] ^ state[10] ^ state[14];\
                                                                            output[ 7] = state[3] ^ state[ 7] ^ state[15];\
                                                                            output[ 8] = state[0] ^ state[ 4] ^ state[12];\
                                                                            output[ 9] = state[1] ^ state[ 5] ^ state[ 9];\
                                                                            output[10] = state[6] ^ state[10] ^ state[14];\
                                                                            output[11] = state[3] ^ state[11] ^ state[15];\
                                                                            output[12] = state[0] ^ state[ 8] ^ state[12];\
                                                                            output[13] = state[1] ^ state[ 5] ^ state[13];\
                                                                            output[14] = state[2] ^ state[ 6] ^ state[10];\
                                                                            output[15] = state[7] ^ state[11] ^ state[15];\
                                                                        }\
                                                                        void mPrime(@Int(64) state)    {\
                                                                            state[0:15] = m0(state[0:15]);\
                                                                            state[16:31] = m1(state[16:31]);\
                                                                            state[32:47] = m1(state[32:47]);\
                                                                            state[48:63] = m0(state[48:63]);\
                                                                        }")), True)

# if __name__ == "__main__":
#     suite = unittest.TestLoader().loadTestsFromTestCase(TestASTTree)
#     unittest.TextTestRunner(verbosity=0).run(suite)
#     suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
#     unittest.TextTestRunner(verbosity=0).run(suite)
#     suite = unittest.TestLoader().loadTestsFromTestCase(TestSemanticAnalysisTree)
#     unittest.TextTestRunner(verbosity=0).run(suite)
#     suite = unittest.TestLoader().loadTestsFromTestCase(test_IR_generation)
#     unittest.TextTestRunner(verbosity=0).run(suite)
