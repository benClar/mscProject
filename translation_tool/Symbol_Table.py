import unittest


class Symbol_Table(object):

    def __init__(self):
        self._table = {}

    def add_scope(self, scope):
        self.table[scope] = {}

    @property
    def table(self):
        return self._table

    def add_int_id(self, scope, ID, id_value=None, id_constraints=None):
        self.add_id(scope, ID, "Int", id_value)
        self.table[scope][ID[0]]["bit_cnst"] = id_constraints

    def add_seq_id(self, scope, ID, id_type, id_value=None):
        # print(id_value)
        self.add_id(scope, ID, "Seq", id_value)
        self.table[scope][ID[0]]["seq_type"] = id_type["type"]
        seq = []
        for i in id_type["seq_size"]:
            seq.append(i)

        print(seq)
        self.table[scope][ID[0]]["dimension"] = seq

    def add_id(self, scope, ID, id_type, id_value=None):
        if scope in self.table:
            if ID not in self.table[scope]:
                self.table[scope][ID[0]] = {}
                self.table[scope][ID[0]]["type"] = id_type
                self.table[scope][ID[0]]["value"] = id_value
            else:
                raise ValueError("Redeclaration of symbol")
        else:
            raise ValueError("Scope Does Not Exist")

    def update_id(self, scope, ID, value):
        self.table[scope][ID]["value"] = value

    def id_type(self, scope, ID):
        try:
            return self.table[scope][ID]["type"]
        except KeyError:
            return None

    def id_details(self, scope, ID):
        return self.table[scope][ID]

    def id_in(self, scope, ID):
        """Returns true if ID exists in symbol table"""
        if ID in self.table[scope]:
            return True
        else:
            return False


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
