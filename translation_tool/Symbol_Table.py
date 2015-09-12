import unittest
from pyparsing import ParseException
from DATA_TYPE import DATA_TYPE
from Stack import Stack
import traceback
import sys
from Translation_exceptions import SemanticException

class Symbol_Table(object):
    """Function table and symbol table"""

    def __init__(self):
        self._symbols = Stack()
        self.add_scope()
        self._f_table = {}
        self.var_count = 0

    def print_s_table(self):
        """Printing table for debugging"""
        for i in self.symbols.stack:
            print(self.symbols.peek())

    def add_scope(self):
        """Adds new scope to symbol table"""
        self.symbols.push({})

    def leave_scope(self):
        """Removes scope from symbol table"""
        self.symbols.pop()

    @property
    def global_scope(self):
        """returns global scope"""
        return self._symbols.stack[0]

    @property
    def f_table(self):
        """Stores info on functions"""
        return self._f_table

    @property
    def symbols(self):
        return self._symbols

    def add_bit_id(self, ID, bit_type):
        """Adds bit ID to symbol table"""
        self.add_id(ID, bit_type)

    def add_int_id(self, ID):
        """Adds standard int id to symbol table"""
        self.add_id(ID, DATA_TYPE.INT_VAL)

    # def update_value(self, ID, value):
    #     for scope in self.symbols.stack:
    #         if ID in scope:
    #             scope[ID]["value"] = value
    #             return
    #     raise SemanticException("Tried to update nonexistent ID " + ID)

    def id(self, ID):
        """returns information for requested ID"""
        for scope in self.symbols.stack:
            if ID in scope:
                return scope[ID]
        raise SemanticException("Tried to update nonexistent ID " + ID)

    def add_id(self, ID, id_type, size=None):
        """Adds ID to symbol table"""
        if ID not in self.symbols.peek() and ID not in self.global_scope and ID not in self.f_table.keys():
            self.symbols.peek()[ID] = {}
            self.symbols.peek()[ID]['type'] = id_type
            self.symbols.peek()[ID]['f_param'] = False
        else:
            raise SemanticException("Redeclaration of symbol")

    def dimension(self, ID):
        """Returns size dimensions for sequence ID"""
        return len(self.id(ID)['size'])

    def add_function(self, func_ID):
        """Adds function to function table, setting up structure required for needed info"""
        if func_ID not in self.f_table:
            self.f_table[func_ID] = {}
            self.f_table[func_ID]["return"] = {}
            self.f_table[func_ID]["parameters"] = []
        else:
            raise ParseException("Redeclaration of function")

    def add_function_parameter(self, func_ID, param_type, constraints=None, size=None):
        """Adds information about parameter to function table entry"""
        self.f_table[func_ID]["parameters"].append({"type": DATA_TYPE.decl_to_value(param_type), "size": size, "constraints": constraints})

    def add_function_return(self, func_ID, return_type, constraints=None, size=None):
        """Adds information about return type to function table entry"""
        self.f_table[func_ID]["return"]["type"] = DATA_TYPE.decl_to_value(return_type)
        self.f_table[func_ID]["return"]["size"] = size
        self.f_table[func_ID]["return"]["constraints"] = constraints

    # def link_node(self, ID, node):
    #     for scope in self.symbols.stack:
    #         if ID in scope:
    #             scope[ID]["node"] = node
    #             return
    #     raise InternalException("Internal Error: Tried to link node to non existent symbol")

    def id_type(self, ID):
        """Returns type of given ID"""
        # print(ID)
        for scope in self.symbols.stack:
            if ID in scope:
                return scope[ID]["type"]
        raise SemanticException("Symbol " + ID + " Does not exist")
