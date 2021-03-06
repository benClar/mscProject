import unittest


class Stack(object):
    """Turns list into stack"""

    def __init__(self, *var):
        self.stack = []
        for i in var:
            self.push(i)

    def push(self, var):
        """Add to stack"""
        self.stack.append(var)

    def pop(self):
        """Remove from head of stack"""
        return self.stack.pop()

    def peek(self):
        """Look at head of stack"""
        return self.stack[len(self.stack) - 1]

    def is_empty(self):
        """returns true if stack is empty"""
        if len(self.stack) == 0:
            return True
        return False


class stack_test(unittest.TestCase):

    def test_stack(self):
        s = Stack(1, 2, 3, 4, 5)
        self.assertEqual(s.pop(), 5)
        self.assertEqual(s.peek(), 4)
        s.push(6)
        self.assertEqual(s.peek(), 6)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(stack_test)
    unittest.TextTestRunner(verbosity=2).run(suite)
