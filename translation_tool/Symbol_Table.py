import unittest
from pyparsing import ParseException
from DATA_TYPE import DATA_TYPE
from Stack import Stack
import traceback
import sys
from Translation_exceptions import SemanticException, InternalException

class Symbol_Table(object):

    def __init__(self):
        self._symbols = Stack()
        self.add_scope()
        self._f_table = {}
        self.var_count = 0

    def print_s_table(self):
        for i in self.symbols.stack:
            print(self.symbols.peek())

    def add_scope(self):
        self.symbols.push({})

    def leave_scope(self):
        self.symbols.pop()

    @property
    def global_scope(self):
        return self._symbols.stack[0]

    @property
    def f_table(self):
        return self._f_table

    @property
    def symbols(self):
        return self._symbols

    def add_bit_id(self, ID, bit_type):
        self.add_id(ID, bit_type)

    def add_int_id(self, ID):
        self.add_id(ID, DATA_TYPE.INT_VAL)

    def update_value(self, ID, value):
        for scope in self.symbols.stack:
            if ID in scope:
                scope[ID]["value"] = value
                return
        raise SemanticException("Tried to update nonexistent ID " + ID)

    def id(self, ID):
        for scope in self.symbols.stack:
            if ID in scope:
                return scope[ID]
        raise SemanticException("Tried to update nonexistent ID " + ID)

    def add_id(self, ID, id_type, size=None):
        if ID not in self.symbols.peek() and ID not in self.global_scope and ID not in self.f_table.keys():
            self.symbols.peek()[ID] = {}
            self.symbols.peek()[ID]['type'] = id_type
            self.symbols.peek()[ID]['f_param'] = False
        else:
            raise SemanticException("Redeclaration of symbol")

    def dimension(self, ID):
        return len(self.id(ID)['size'])

    def add_function(self, func_ID):
        if func_ID not in self.f_table:
            self.f_table[func_ID] = {}
            self.f_table[func_ID]["return"] = {}
            self.f_table[func_ID]["parameters"] = []
        else:
            raise ParseException("Redeclaration of function")

    def add_function_parameter(self, func_ID, param_type, constraints=None, size=None):
        self.f_table[func_ID]["parameters"].append({"type": DATA_TYPE.decl_to_value(param_type), "size": size, "constraints": constraints})

    def add_function_return(self, func_ID, return_type, constraints=None, size=None):
        self.f_table[func_ID]["return"]["type"] = DATA_TYPE.decl_to_value(return_type)
        self.f_table[func_ID]["return"]["size"] = size
        self.f_table[func_ID]["return"]["constraints"] = constraints

    def link_node(self, ID, node):
        for scope in self.symbols.stack:
            if ID in scope:
                scope[ID]["node"] = node
                return
        raise InternalException("Internal Error: Tried to link node to non existent symbol")

    def id_type(self, ID):
        # print(ID)
        for scope in self.symbols.stack:
            if ID in scope:
                return scope[ID]["type"]
        raise SemanticException("Symbol " + ID + " Does not exist")

class TestSymbolTable(unittest.TestCase):

    def test_int_decl(self):
        tab = Symbol_Table()
        tab.add_scope("global")
        self.assertEqual(len(tab.table), 1)
        tab.add_int_id("global", "a", 0, 10)
        self.assertEqual(tab.table["global"]["a"]["value"], 0)
        self.assertEqual(tab.table["global"]["a"]["type"], "Int")
        self.assertEqual(tab.table["global"]["a"]["bit_cnst"], 10)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSymbolTable)
    unittest.TextTestRunner(verbosity=2).run(suite)
