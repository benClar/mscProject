from enum import Enum
import unittest


class Tree(Enum):
    SEQ = 1
    NAME = 2
    CONST = 3
    VAR_DECL = 4
    INT_TYPE = 5


class IR_Tree(object):

    def __init__(self):
        self._root = None

    @property
    def root(self):
        return self._root

    def clear(self):
        self.root = None

    @root.setter
    def root(self, value):
        self._root = value

    def add(self, node):
        if self.root is None:
            self.root = node
        else:
            self._add(self.root, node)

    def _add(self, current_node, node):
        try:
            if current_node.left is None:
                current_node.left = node
                return True
            elif self._add(current_node.left, node) is True:
                return True
            elif current_node.right is None:
                current_node.right = node
                return True
            elif self._add(current_node.right, node):
                return True
        except AttributeError:
            return False

    def output(self, curr=None, depth=0):
        ret = ""
        if curr is None:
            curr = self.root
        # Print right branch
        try:
            if curr.right is not None:
                ret += self.output(curr.right, depth + 1)
        except AttributeError:
            pass

        # Print own value
        ret += "\n" + ("    "*depth) + str(curr)

        # Print left branch
        try:
            if curr.left is not None:
                ret += self.output(curr.left, depth + 1)
        except AttributeError:
            pass
        return ret


class Seq_node(object):
    """Evaluation goes from left to right"""
    def __init__(self, value=None, left=None, right=None):
        self._right = right
        self._left = left
        self._type = Tree.SEQ
        self._value = value

    def __str__(self):
        return str(self.type) + " " + str(self.value)

    @property
    def value(self):
        return self._value

    @property
    def type(self):
        return self._type

    @property
    def right(self):
        return self._right

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self._left = value

    @right.setter
    def right(self, value):
        self._right = value


class Decl_node(object):
    """Declaration of a variable"""

    DEFAULT_INT_WIDTH = 10
    DEFAULT_INT_VALUE = 0

    def __init__(self, var_type, name, value=None, cnst=None):
        self._name = name
        self._type = Tree.VAR_DECL
        self._var_type = var_type
        if value is None:
            self._value = Literal_node(Decl_node.DEFAULT_INT_VALUE)
        else:
            self._value = value
        if cnst is None:
            self._cnst = Literal_node(Decl_node.DEFAULT_INT_WIDTH)
        else:
            self._cnst = cnst

    def generate_cnst(value):
        if value is None:
            value = Decl_node.DEFAULT_INT_WIDTH
        return Literal_node(str(int(value).bit_length()))

    @property
    def type(self):
        return self._type

    def __str__(self):
        return str(self.type) + " " + str(self.name) + " " + " " + str(self.value)

    @property
    def name(self):
        return self._name

    @property
    def var_type(self):
        return self._var_type

    @property
    def cnst(self):
        return self._cnst

    @property
    def value(self):
        return self._value

    def translate(self):
        padding = int(self.cnst.value) - \
            int(self.value.value).bit_length()
        ret = self.var_type.translate() + " " + self.name.translate() + \
            "[" + self.cnst.translate() + "]" + "=" + "{" + ("0," * padding) + \
            self.value.translate_bs() + "}" + ";"
        if ret[-3] == ",":
            ret = ret[0: -3] + ret[-2:]
        return ret


class Type_node(object):
    """Holds an Type"""
    def __init__(self, value):
        self._type_table = {"Int": Tree.INT_TYPE}
        self._value = value
        self._type = self._type_table[value]
        self._translation_table = {'Int': 'uint8_t'}

    @property
    def value(self):
        return self._value

    @property
    def type(self):
        return self._type

    @property
    def translation_table(self):
        return self._translation_table

    def __str__(self):
        return str(self.type) + " " + self.name

    def translate(self):
        return self.translation_table[self.value]


class Name_node(object):
    """Holds an ID"""
    def __init__(self, name):
        self._name = name
        self._type = Tree.NAME

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    def translate(self):
        return self.name

    def __str__(self):
        return str(self.type) + " " + self.name


class Literal_node(object):
    """Holds Literal Value"""
    def __init__(self, value):
        self._value = value
        self._type = Tree.CONST

    @property
    def value(self):
        return self._value

    @property
    def type(self):
        return self._type

    def __str__(self):
        return str(self.type) + " " + str(self.value)

    def translate(self):
        return str(self.value)

    def translate_bs(self):
        bs = self.bitslice()
        ret = ""
        for i in bs:
            ret += str(i) + ","
        ret = ret[:-1]
        return ret

    def bitslice(self):
        val = int(self._value)
        output = []
        while(val != 0):
            output.insert(0, val & 1)
            val >>= 1
        return output


class TestIRTree(unittest.TestCase):

    def test_add_node(self):
        tree = IR_Tree()
        tree.add(Seq_node(0))
        self.assertEqual(tree.root.type, Tree.SEQ)
        tree.add(Decl_node("Int", Name_node("A"), Literal_node("10")))
        self.assertEqual(tree.root.left.type, Tree.VAR_DECL)
        tree.add(Seq_node(0))
        tree.add(Decl_node("Int", Name_node("A"), Literal_node("10")))
        self.assertEqual(tree.root.right.left.type, Tree.VAR_DECL)

    def test_literal_bitslice(self):
        l = Literal_node(10)
        self.assertEqual(l.bitslice(), [1, 0, 1, 0])
        l = Literal_node(20)
        self.assertEqual(l.bitslice(), [1, 0, 1, 0, 0])

    def test_int_decl(self):
        dec = Decl_node(Type_node("Int"), Name_node("test"), Literal_node("10"), Literal_node("4"))  # NOQA
        self.assertEqual(dec.translate(), "uint8_t test[4]={1,0,1,0};")
        dec = Decl_node(Type_node("Int"), Name_node("test"), Literal_node("4"), Literal_node("6"))  # NOQA
        self.assertEqual(dec.translate(), "uint8_t test[6]={0,0,0,1,0,0};")
        dec = Decl_node(Type_node("Int"), Name_node("test"))
        self.assertEqual(dec.translate(), "uint8_t test[10]={0,0,0,0,0,0,0,0,0,0};")  # NOQA

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIRTree)
    unittest.TextTestRunner(verbosity=2).run(suite)
