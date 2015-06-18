from pyparsing import Literal, Word, nums, ParseException, Forward, alphas,\
    Suppress, Group, ZeroOrMore, Keyword, alphanums, NotAny, CharsNotIn, \
    OneOrMore, Optional, delimitedList, StringEnd, oneOf
import unittest
from Symbol_Table import Symbol_Table
from Stack import Stack
from IR import IR_Tree, Seq_node, Decl_node, Type_node, Name_node, Literal_node,\
    Tree


class Semantic_analyser(object):

    TESTING = 1

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

    def analyse_constraints(self, value, constraints):
        if int(value).bit_length() > int(constraints):
            return False
        else:
            return True

    def is_already_declared(self, ID):
        """Returns False if ID has not been declared yet"""
        print("CHECKING ID:")
        print(ID[0])
        if self.sym_table.id_in(self.call_stack.peek(), ID[0]) == True:  # NOQA
            return True
        else:
            return False

    def analyse_id_set(self, tokens):
        token = tokens[0]
        if self.is_already_declared(token("ID")) is True:
            if Semantic_analyser.TESTING == 1:
                return False
            else:
                raise ParseException("Unknown Value")
        if self.value_is_correct_type(token("ID"), token("value")) is False:
            if Semantic_analyser.TESTING == 1:
                return False
            else:
                raise ParseException("Incorrect Value Type assigned to ID")

    def value_is_correct_type(self, ID, value):
        id_type = self.sym_table.id_type(self.call_stack.peek(), ID)
        if id_type is "Bit" and self.is_bit(value) is True:
            return True
        if id_type is "Int" and self.is_int(value) is True:
            return True
        return False

    def is_int(self, value):
        try:
            int(value)
        except ValueError:
            return False
        return True

    def is_bit(self, value):
        if value == "True" or value == "False":
            return True
        else:
            return False

    def analyse_int_decl(self, tokens):
        token = tokens[0]
        print(token.dump())
        for decl in token["value"]:
            try:
                if self.analyse_constraints(decl["value"], token["constraints"]) is False:  # NOQA
                    raise ParseException("Value bigger than bit constraints")
            except KeyError:
                pass
            except ParseException as details:
                if Semantic_analyser.TESTING == 1:
                    print(details)
                    return False
                else:
                    raise ParseException("Value bigger than bit constraints")
            if self.is_already_declared(decl["ID"]) is True:
                try:
                    raise ParseException("Duplicate Symbol")
                except ParseException as details:
                    if Semantic_analyser.TESTING == 1:
                        return False
                    else:
                        raise ParseException("Duplicate Symbol")  # NOQA
            self.add_int_decl(decl, token)
        return tokens

    def add_int_decl(self, decl, token):
        self.IR.add(Seq_node())
        if "constraints" in token:
            if "value" in decl:
                print("HERE")
                self.sym_table.add_int_id(self.call_stack.peek(),
                                          decl["ID"],
                                          decl["value"],
                                          token["constraints"])
                self.IR.add(Decl_node(Type_node(token["decl"]),
                                      Name_node(decl["ID"][0]),
                                      Literal_node(decl["value"]),
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
                                          id_value=decl["value"])
                self.IR.add(Decl_node(Type_node(token["decl"]),
                                      Name_node(decl["ID"][0]),
                                      value=Literal_node(decl["value"])))
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
        # Other Tokens
        self.stmt = Forward()
        self.l_bracket = Literal(')')
        self.r_bracket = Literal('(')
        self.eq_set = Literal('=')("set")
        self.term_st = Literal(';')
        # self.int_not_constrained = Literal("Int ")
        # self.int_constrained = Word("Int") + Suppress(Literal("(")) + Word(nums) + \
        #     Suppress(Literal(")"))
        # Grammar
        self.var = self.ID ^ Word(nums)

        self.id_set = self.ID + self.eq_set + (Word(nums)("value") ^ self.bit_val) + Suppress(self.term_st)  # NOQA
        # id_set.setParseAction(semantic_analyser.analyse_id_set)

        self.int_decl = Group(self.int_("decl") + Optional(Suppress(self.r_bracket) + Word(nums)("constraints") +  # NOQA
            Suppress(self.l_bracket)) + delimitedList(Group(self.ID("ID")) ^ Group(self.ID("ID") + self.eq_set + Word(nums)("value")))("value")) + Suppress(self.term_st)  # NOQA
        self.int_decl.setParseAction(self.semantic_analyser.analyse_int_decl)
        self.shift = Group(self.var("target") + (self.l_shift_ ^ self.r_shift_ ^ self.circ_l_shift_ ^ self.circ_r_shift_)("shift_op") + self.var) + Suppress(self.term_st)  # NOQA

        self.bit_decl = Group(self.bit_("decl") + delimitedList(Group(self.ID) ^ Group(self.ID + self.eq_set + self.bit_val("value")))("value")) + Suppress(self.term_st)  # NOQA

        self.stmt << OneOrMore(self.int_decl | self.id_set | self.bit_decl | self.shift)  # NOQA
        self.grammar = self.stmt + StringEnd()

    def parse_test_unit(self, data_in):
        try:
            res = self.grammar.parseString(data_in)
        except ParseException as details:
            print(details)
            return False
        # print(res[0].dump())
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

    def test_int_decl_parsing(self):
        par = Parser()
        self.assertEqual(par.parse_test_unit("Int varName;")[1], True)
        self.assertEqual(par.parse_test_unit("Int(123) ee;")[1], True)
        self.assertEqual(par.parse_test_unit("Int(123) ff"), False)
        self.assertEqual(par.parse_test_unit("Int()"), False)
        self.assertEqual(par.parse_test_unit("Int(1) ;"), False)
        self.assertEqual(par.parse_test_unit("Int(1) test"), False)
        self.assertEqual(par.parse_test_unit("Int"), False)
        self.assertEqual(par.parse_test_unit("Int(123) gg,jj,\
            test;")[1], True)
        self.assertEqual(par.parse_test_unit("Int Int;"), False)
        self.assertEqual(par.parse_test_unit("Int Integer;")[1], True)
        self.assertEqual(par.parse_test_unit("Int kk; Int \
            ll;")[1], True)
        self.assertEqual(par.parse_test_unit("Int mm, nn, oo, pp;")[1], True)
        self.assertEqual(par.parse_test_unit("Int qq = 10, rr = 4, ss = 5, tt = \
            7;")[1], True)
        self.assertEqual(par.parse_test_unit("Int uu = 10, j, k = 5,\
            d;")[1], True)
        self.assertEqual(par.parse_test_unit("Int(10) l = 10, m, n = 5, \
         h;")[1], True)
        self.assertEqual(par.parse_test_unit("Int(10) o = 10, p, q = 5, \
         h"), False)
        self.assertEqual(par.parse_test_unit("Int(10) r = 10, s, t = 5, u; Int v, w=10, \
            l;")[1], True)
        self.assertEqual(par.parse_test_unit("Int(10) x; y; z;"), False)
        self.assertEqual(par.parse_test_unit("aa; bb; cc;"), False)
        self.assertEqual(par.parse_test_unit("Int dd = 10;")[1], True)

    def test_set_parsing(self):
        par = Parser()
        self.assertNotEqual(par.parse_test_unit("b = 2;"), False)
        self.assertEqual(par.parse_test_unit("Int = 2;"), False)
        self.assertEqual(par.parse_test_unit("d = False;")[1], True)
        self.assertEqual(par.parse_test_unit("e = True;")[1], True)
        self.assertEqual(par.parse_test_unit("e = blah;"), False)
        self.assertEqual(par.parse_test_unit("e = True True;"), False)

    def test_int_decl_semantics(self):
        sem_a = Semantic_analyser()
        par = Parser()
        self.assertEqual(sem_a.analyse_constraints("10", "2"), False)
        self.assertEqual(sem_a.analyse_constraints(
                         "999999999999999999999999999999999999999999999999999999999999"  # NOQA
                         "999999999999999999999999999999", "2"), False)
        self.assertEqual(par.parse_test_unit("Int a = 10;")[1], True)  # NOQA
        self.assertEqual(par.parse_test_unit("Int d = 10, b = 10, c = 20;")[1], True)  # NOQA
        self.assertEqual(par.parse_test_unit("Int(3) e = 10, f = 10, g = 20;")[0][0], False)  # NOQA
        self.assertEqual(par.parse_test_unit("Int(4) h = 10, h = 10, i = 20;")[0][0], False)  # NOQA
        print(par.semantic_analyser.sym_table.table)
        self.assertEqual(par.parse_test_unit("Int(4) z = 10;")[1], True)
        print(par.semantic_analyser.sym_table.table)
        self.assertEqual(par.parse_test_unit("Int(4) z = 10;")[0][0], False)
        self.assertEqual(par.parse_test_unit("Int(4) k;")[1], True)
        self.assertEqual(par.parse_test_unit("Int(4) k;")[0][0], False)

    def test_bit_decl_parsing(self):
        par = Parser()
        self.assertEqual(par.parse_test_unit("Bit a = True;")[1], True)
        self.assertEqual(par.parse_test_unit("Bit b, c, d = True;")[1], True)
        self.assertEqual(par.parse_test_unit("Bit Bit, c, d = True;"), False)

    def test_shift_op(self):
        par = Parser()
        self.assertEqual(par.parse_test_unit("a << 3;")[1], True)

    def test_id_set_semantics(self):
        sem_a = Semantic_analyser()
        sem_a.sym_table.add_int_id("global", "a")
        self.assertEqual(sem_a.value_is_correct_type("a", "30"), True)
        self.assertEqual(sem_a.value_is_correct_type("a", "False"), False)

    def test_int_decl_IR(self):
        par = Parser()
        self.assertEqual(par.semantic_analyser.IR.root, None)
        self.assertEqual(par.parse_test_unit("Int(4) a= 10;")[1], True)  # NOQA
        print(par.semantic_analyser.IR.output())
        self.assertEqual(par.semantic_analyser.IR.root.type, Tree.SEQ)
        self.assertEqual(par.semantic_analyser.IR.root.left.type, Tree.VAR_DECL)  # NOQA
        self.assertEqual(par.semantic_analyser.IR.root.left.translate(), "uint8_t a[4]={1,0,1,0};")  # NOQA
        self.assertEqual(par.parse_test_unit("Int(2) b=10;")[0][0], False)  # NOQA
        self.assertEqual(par.parse_test_unit("Int c;")[1], True)
        self.assertEqual(par.semantic_analyser.IR.root.right.left.translate(), "uint8_t c[10]={0,0,0,0,0,0,0,0,0,0};")  # NOQA

    def test_add_to_symbol_table(self):
        sem_a = Semantic_analyser()
        sem_a.sym_table.add_int_id("global", "A", "10", "5")
        sem_a.sym_table.add_int_id("global", "B", id_constraints="9")
        sem_a.sym_table.add_int_id("global", "D", id_value="4")
        self.assertEqual(sem_a.sym_table.id_in("global", "A"), True)
        self.assertEqual(sem_a.sym_table.id_in("global", "B"), True)
        self.assertEqual(sem_a.sym_table.id_in("global", "C"), False)
        self.assertEqual(sem_a.sym_table.id_in("global", "D"), True)

    def test_multiple_int_decl_IR(self):
        par = Parser()
        self.assertEqual(par.parse_test_unit("Int(4) a= 10; Int b = 5, c;")[1], True)  # NOQA
        self.assertEqual(par.semantic_analyser.IR.root.type, Tree.SEQ)
        self.assertEqual(par.semantic_analyser.IR.root.left.translate(), "uint8_t a[4]={1,0,1,0};")  # NOQA
        self.assertEqual(par.semantic_analyser.IR.root.right.type, Tree.SEQ)
        self.assertEqual(par.semantic_analyser.IR.root.right.left.translate(), "uint8_t b[10]={0,0,0,0,0,0,0,1,0,1};")  # NOQA
        self.assertEqual(par.semantic_analyser.IR.root.right.right.type, Tree.SEQ)  # NOQA
        self.assertEqual(par.semantic_analyser.IR.root.right.right.left.translate(), "uint8_t c[10]={0,0,0,0,0,0,0,0,0,0};")  # NOQA

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
    unittest.TextTestRunner(verbosity=2).run(suite)













