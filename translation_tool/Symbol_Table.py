import unittest
from pyparsing import ParseException
from AST_TYPE import AST_TYPE
from Stack import Stack

class Symbol_Table(object):

    def __init__(self):
        self._symbols = Stack()
        self.add_scope()
        self._f_table = {}
    # def add_scope(self, scope):
    #     self.table[scope] = {}

    def print_s_table(self):
        for i in self.symbols.stack:
            print(self.symbols.peek())

    def add_scope(self):
        self.symbols.push({})

    def leave_scope(self):
        self.symbols.pop()

    @property
    def f_table(self):
        return self._f_table

    @property
    def symbols(self):
        return self._symbols

    def add_bit_id(self, ID):
        self.add_id(ID, AST_TYPE.BIT_VAL)

    # def add_int_id(self, scope, ID):
    #     self.add_id(scope, ID, AST_TYPE.INT_VAL)

    def add_int_id(self, ID):
        self.add_id(ID, AST_TYPE.INT_VAL)

    def update_value(self, ID, value):
        for scope in self.symbols.stack:
            if ID in scope:
                scope[ID]["value"] = value
                return
        raise ParseException("Tried to update nonexistent ID")

    def id(self, ID):
        for scope in self.symbols.stack:
            if ID in scope:
                return scope[ID]
        raise ParseException("Tried to update nonexistent ID")

    def add_id(self, ID, id_type):
        if ID not in self.symbols.peek():
            self.symbols.peek()[ID] = {}
            self.symbols.peek()[ID]['type'] = id_type
        else:
            raise ParseException("Redeclaration of symbol")

    # def add_seq_id(self, scope, ID, id_type, id_value=None):
    #     self.add_id(scope, ID, "Seq", id_value)
    #     self.table[scope][ID[0]]["seq_type"] = id_type["type"]
    #     seq = []
    #     for i in id_type["seq_size"]:
    #         seq.append(i)

    #     print(seq)
    #     self.table[scope][ID[0]]["dimension"] = seq

    def add_function(self, func_ID, parameters, return_type):
        if func_ID not in self.f_table:
            self.f_table[func_ID] = {}
            self.f_table[func_ID]["return_type"] = return_type
            self.f_table[func_ID]["parameters"] = []
            for p in parameters:
                self.f_table[func_ID]["parameters"].append(p)
                self.add_id(p.ID, AST_TYPE.decl_to_value(p.node_type))
        else:
            raise ParseException("Redeclaration of function")

    def link_node(self, ID, node):
        for scope in self.symbols.stack:
            if ID in scope:
                scope[ID]["node"] = node
                return
        raise ParseException("Internal Error: Tried to link node to non existent symbol")

    # def add_id(self, scope, ID, id_type):
    #     if scope in self.table:
    #         if ID not in self.table[scope]:
    #             self.table[scope][ID] = {}
    #             self.table[scope][ID]["type"] = id_type
    #         else:
    #             raise ParseException("Redeclaration of symbol")
    #     else:
    #         raise ParseException("Scope Does Not Exist")

    # def update_id(self, scope, ID, value):
    #     self.table[scope][ID]["value"] = value

    def id_type(self, ID):
        for scope in self.symbols.stack:
            if ID in scope:
                return scope[ID]["type"]
        raise ParseException("Symbol " + ID + " Does not exist")

    # def id_details(self, scope, ID):
    #     return self.table[scope][ID]

    # def id_in(self, scope, ID):
    #     """Returns true if ID exists in symbol table"""
    #     if ID in self.table[scope]:
    #         return True
    #     else:
    #         return False


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
