from AST_TYPE import AST_TYPE
import unittest
from nose.tools import assert_equals
from pyparsing import ParseException


class Translator:

    node_type_lookup = {AST_TYPE.INT_DECL: lambda self, node: self.translate_int_decl(node),
                        AST_TYPE.BIT_DECL: lambda self, node: self.translate_bit_decl(node),
                        AST_TYPE.ID_SET: lambda self, node: self.translate_ID_set(node),
                        AST_TYPE.SEQ_DECL: lambda self, node: self.translate_seq_decl(node),
                        AST_TYPE.FUNC_DECL: lambda self, node: self.translate_func_decl(node),
                        AST_TYPE.IF_STMT: lambda self, node: self.translate_if_stmt_decl(node),
                        AST_TYPE.FOR_LOOP: lambda self, node: self.translate_for_loop_decl(node)}

    def translate_for_loop(self, node, sym_table):
        translation = ""
        for expr in node.initializer:
            if expr.node_type == AST_TYPE.BIT_DECL:
                pass
            elif expr.node_type == AST_TYPE.INT_DECL:
                translation += self.translate_int_decl(expr, sym_table)
            elif expr.node_type == AST_TYPE.SEQ_DECL:
                pass
        for i in node.terminator:
            print("TERM")
            translation += self.translate_expr(i)

    def translate_int_decl(self, node, sym_table):
        translation = ""
        try:
            sym_table.update_value(node.ID, self.eval_expr(node.value, sym_table))
            translation += "uint8_t " + node.ID + " = " + self.translate_expr(node.value) + ";"
            print(translation)
        except AttributeError:
            translation += "uint8_t " + node.ID + ";"
            print(translation)
        sym_table.link_node(node.ID, node)
        return translation

    def translate_expr(self, node):
        tran_expr = ""
        print("Expr:")
        print(node.expressions)
        print("___")
        if len(node.expressions == 3):
            self.translate_sub_expr(node.expressions)
        elif len(node.expressions == 1):
            for expr in node.expressions:
                if expr.node_type == AST_TYPE.INT_VAL:
                    tran_expr += expr.value
                elif expr.node_type == AST_TYPE.EXPR:
                    tran_expr += self.translate_expr(expr)
        else:
            raise ParseException("Internal Error: Unexpected expression length")

        return tran_expr

    def translate_sub_expr(self, expression):
        trans_sub__expr = ""
        if expression[1].node_type is AST_TYPE.COMP:
            self.translate_comp_operation(expression)

    def translate_comp_operation(self, expression):
        if expression[0].node_type == AST_TYPE.INT_VAL or expression[0].node_type == AST_TYPE.BIT_VAL or expression[0].ID_type == AST_TYPE.INT_VAL or expression[0].ID_type == AST_TYPE.BIT_VAL:
            pass
        elif expression[0].node_type == AST_TYPE.SEQ_VAL:
            self.translate_seq_comparison(expression)
        elif expression[0].node_type == AST_TYPE.EXPR:
            pass

    def translate_seq_comparison(self, expression):
        if expression[0].seq_type == AST_TYPE.SEQ_INT_VAL:
            pass
        if expression[0].seq_type == AST_TYPE.SEQ_BIT_VAL:
            pass
        elif expression[0].seq_type == AST_TYPE.BS_SEQ_INT_VAL:
            pass       

    def translate_int_seq_decl(self, node, sym_table):
        try:
            sym_table.update_value(node.ID.ID, self.eval_seq_val(node.value.expressions[0].expressions[0].value, sym_table))
            if node.type == AST_TYPE.BS_SEQ_INT_VAL:
                sym_table.update_value(node.ID.ID, self.bit_slice(sym_table.id(node.ID.ID)["value"], int(self.eval_expr(node.bit_constraints, sym_table))))
            translation = "uint8_t " + ("*" * len(node.size)) + node.ID.ID + "= malloc(" + self.eval_expr(node.size[0], sym_table) + "* sizeof(uint8_t));\n"
            for ele in range(int(self.eval_expr(node.size[0], sym_table))):
                translation += node.ID.ID + "[" + str(ele) + "]" + " = " + sym_table.id(node.ID.ID)["value"][ele] + "\n"
            print(translation)
        except AttributeError:
            translation = "uint8_t " + ("*" * len(node.size)) + node.ID.ID + "= malloc(" + self.eval_expr(node.size[0], sym_table) + "* sizeof(uint8_t));\n"
            print(translation)
        sym_table.link_node(node.ID.ID, node)

    def bit_slice(self, value, width):
        output = []
        output += [0] * width
        for bit in reversed(range(width)):
            for i, val in enumerate(value):
                output[width - bit - 1] <<= 1
                output[width - bit - 1] |= ((int(val) >> bit) & 0x1)
        output = [str(i) for i in output]
        return output

    def eval_seq_val(self, value, sym_table):
        evaluated_val = []
        for i in value:
            evaluated_val.append(self.eval_expr(i, sym_table))
        return evaluated_val

    def eval_expr(self, expression, sym_table):
        expr_eval = ""
        for expr in expression.expressions:
            if expr.node_type == AST_TYPE.INT_VAL:
                expr_eval += expr.value
            elif expr.node_type == AST_TYPE.EXPR:
                expr_eval += self.eval_expr(self, expr)
            elif expr.node_type == AST_TYPE.ID:
                expr_eval += sym_table.id(expr.ID)["value"]
            else:
                print(expr.node_type)
                raise ParseException("Unrecognised node type")
        return expr_eval


class testTranslatorUnit(unittest.TestCase):

    def test_bit_slice(self):
        t = Translator()
        assert_equals(t.bit_slice(['1', '2', '3', '4'], 4), [0, 1, 6, 10])
        assert_equals(t.bit_slice(['1', '2', '3', '4', '5', '6', '7', '8'], 8), [0, 0, 0, 0, 1, 30, 102, 170])
