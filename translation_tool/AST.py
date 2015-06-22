class AST(object):

    def __init__(self):
        self._tree = []

    def add_node(self, node):
        self.tree.append(node)

    @property
    def tree(self):
        return self._tree

    def id_set(self, tokens):
        # print(tokens)
        pass

    def bit_decl(self, tokens):
        print(tokens[0].dump())
        token = tokens[0]
        # for decl in token['value']:
        #     if 'function_name' in decl:
        #         self.add_node(bit_decl(decl['id'][0]))

    def expr(self, tokens):
        print(tokens[0])

class bit_decl(object):

    def __init__(self, ID, value=None):
        self._ID = ID
        self._value = value

class expr(object):

    def __init__(self, expr=None):
        self._e1
        self._e2
        eval(expr)
        pass

    def eval(expr):
        for i in expr:
            print(i)

