from pyparsing import Literal, Word, nums, ParseException, Forward, alphas,\
    Suppress, Group, ZeroOrMore, Keyword, alphanums, NotAny, CharsNotIn, \
    OneOrMore, Optional, delimitedList, StringEnd, oneOf, srange, Combine, \
    infixNotation, opAssoc, White, ParserElement, operatorPrecedence, ParseResults
from Syntax_tree import *

ParserElement.enablePackrat()


class Parser(object):
    """Lexical and Syntax analysis"""
    @property
    def semantic_analyser(self):
        return self._AST.semantic_analyser

    def __init__(self):
        self._AST = Syntax_tree()

        # keywords
        self.int_ = Keyword('Int')
        self.false_ = Keyword('False')
        self.true_ = Keyword('True')
        self.bit_ = Combine(Optional(Literal("@")) + Keyword('Bit'))
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
        self.bit_xor = Keyword('^')
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

        self.decl = self.bit_decl ^ self.int_decl ^ self.seq_decl

        # ###### Statements

        self.return_stmt = Group(self.return_ + self.expr)
        self.return_stmt.setParseAction(self.AST.return_stmt)

        self.function_start = Literal("{")
        self.function_start.setParseAction(self.AST.function_start)
        self.function_end = Literal("}")
        self.function_decl = Group((Group(self.seq_) | Group(self.int_size) | Group(self.bit_) | Group(self.void_))("return_type") + Group(self.ID)("func_ID") +
                                   Suppress(self.l_bracket) + Group(Optional(delimitedList(Group((self.seq_ | self.int_size | self.bit_) + Group(self.ID)))))("func_param") +  # NOQA
                                   Suppress(self.r_bracket) + Suppress(self.function_start) + Group(self.stmt)("body") + Suppress(self.r_brace))
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
        self.single_expr = self.expr + Suppress(self.term_st)
        self.single_expr.setParseAction(self.AST.stand_alone_expr)

        self.stmt << ZeroOrMore(self.decl + Suppress(self.term_st)
                                ^ self.function_decl
                                ^ self.id_set + Suppress(self.term_st)
                                ^ self.single_expr
                                ^ self.for_loop
                                ^ self.if_stmt
                                ^ self.return_stmt + Suppress(self.term_st)
                                ^ self.sbox_call + Suppress(self.term_st))

        self.grammar_test = self.stmt + StringEnd()  # Allows single statements to be parsed

        self.grammar = ZeroOrMore(self.function_decl
                                  ^ self.seq_decl + Suppress(self.term_st)) + StringEnd()

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
        """Prod parsing entry point"""
        self.grammar.parseString(data_in)
        if self.semantic_analyser.analyse(self.AST, True) is True:
            return self.semantic_analyser.IR.translate()

