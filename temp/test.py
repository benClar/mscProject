from pyparsing import Literal, Word, nums, ParseException, Forward, alphas,\
    Suppress, Group, ZeroOrMore, Keyword, alphanums, NotAny, CharsNotIn, \
    OneOrMore, Optional, delimitedList, StringEnd, oneOf
import unittest

class Parser(object):

    def test_act(tokens):
        Parser.semantic_analyser.analyse_int_decl(tokens)

    # keywords
    def __init__(self):
        self.ID = Word(alphas + '_', alphanums + '_')

        # Other Tokens
        self.stmt = Forward()
        self.eq_set = Literal('=')("set")
        self.id_set = self.ID + self.eq_set + (Word(nums)("value"))
        self.id_set.setParseAction(self.test_act)
        self.stmt << OneOrMore(self.id_set)
        self.grammar = self.stmt + StringEnd()

    def test_act(self,tokens):
        print(tokens.dump())

    def parse(self, data_in):
        return self.grammar.parseString(data_in)


class TestParser(unittest.TestCase):

    def test_int_decl_parsing(self):
        p = Parser()
        p.parse("a = 2")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
    unittest.TextTestRunner(verbosity=2).run(suite)

