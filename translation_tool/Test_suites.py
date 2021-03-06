import unittest
from nose.tools import assert_equals
from Parser import Parser
from DATA_TYPE import DATA_TYPE
from Data_reader import Data_reader
import subprocess

class TestParser(unittest.TestCase):
    """Unit tests for Syntax Analysis"""
    def test_int_decl_parsing(self):
        par = Parser()
        assert_equals(par.parse_test_unit("Int(10) varName;")[1], True)
        assert_equals(par.parse_test_unit("Int(123) ee;")[1], True)
        assert_equals(par.parse_test_unit("Int(123) ff"), False)
        assert_equals(par.parse_test_unit("Int()"), False)
        assert_equals(par.parse_test_unit("Int(1) ;"), False)
        assert_equals(par.parse_test_unit("Int(1) test"), False)
        assert_equals(par.parse_test_unit("Int"), False)
        assert_equals(par.parse_test_unit("Int(123) gg,jj,test2;")[1], True)
        assert_equals(par.parse_test_unit("Int Int;"), False)
        assert_equals(par.parse_test_unit("Int(10) Integer;")[1], True)
        assert_equals(par.parse_test_unit("Int(10) kk; Int(20) \
            ll;")[1], True)
        assert_equals(par.parse_test_unit("Int(10) mm, nn, oo, pp;")[1], True)
        assert_equals(par.parse_test_unit("Int(10) qq = 10, rr = 4, ss = 5, tt = \
            7;")[1], True)
        assert_equals(par.parse_test_unit("Int(10) uu = 10, j, k = 5,\
            d;")[1], True)
        assert_equals(par.parse_test_unit("Int(10) l = 10, m, n = 5, \
         h;")[1], True)
        assert_equals(par.parse_test_unit("Int(10) o = 10, p, q = 5, \
         h"), False)
        assert_equals(par.parse_test_unit("Int(10) r1 = 10, s1, t1 = 5, u1; Int(10) v1, w1=10, \
            ll1;")[1], True)
        assert_equals(par.parse_test_unit("Int(10) dd = 10;")[1], True)
        assert_equals(par.parse_test_unit("Int (123) zz;"), False)

    def test_bs_decl_parsing(self):
        par = Parser()
        assert_equals(par.parse_test_unit("@Int(10) varName;")[1], True)
        assert_equals(par.parse_test_unit("@Int(10)[10] varName;")[1], True)
        assert_equals(par.parse_test_unit("@Int(10)[10][10] varName;")[1], True)

    def test_bit_decl_parsing(self):
        par = Parser()
        assert_equals(par.parse_test_unit("Bit a = True;")[1], True)
        assert_equals(par.parse_test_unit("Bit b, c, d = True;")[1], True)
        assert_equals(par.parse_test_unit("Bit Bit, c, d = True;"), False)
        assert_equals(par.parse_test_unit("Bit c, d = function(1,2,3,4);")[1], True)
        assert_equals(par.parse_test_unit("Bit c, d = function();")[1], True)
        assert_equals(par.parse_test_unit("Bit c, d = function(1,2,(3*5) << (4 * 5)) + function_2(1,2,(3*5) << (4 * 5));")[1], True)
        assert_equals(par.parse_test_unit("Bit c, d = 3 + (1+ 2 + 3) * (2 + (Bit) 3);")[1], True)

    def test_set_parsing(self):
        par = Parser()
        par.parse_test_unit("Int b;")
        par.parse_test_unit("Bit d, e;")
        assert_equals(par.parse_test_unit("b = 2;")[1], True)
        assert_equals(par.parse_test_unit("Int = 2;"), False)
        assert_equals(par.parse_test_unit("d = False;")[1], True)
        assert_equals(par.parse_test_unit("e = True;")[1], True)
        assert_equals(par.parse_test_unit("e = True True;"), False)

    def test_expr_parsing(self):
        par = Parser()
        par.parse_test_unit("Int(10) a, b, c, d, e, r; Bit ff;")
        assert_equals(par.parse_test_unit("((a > 4) && (b > 5)) || d > 3 || (3 << 3);")[1], True)
        assert_equals(par.parse_test_unit("[[1,2,3,4],[1,2,3,4]] << 3;")[1], True)
        assert_equals(par.parse_test_unit("a + b;")[1], True)
        assert_equals(par.parse_test_unit("a + c + d + e;")[1], True)
        assert_equals(par.parse_test_unit("a + (c + d) + e;")[1], True)
        assert_equals(par.parse_test_unit("a + c + d + + e;"), False)
        assert_equals(par.parse_test_unit("a + c + 4 - e;")[1], True)
        assert_equals(par.parse_test_unit("a + (c) + 4 - e;")[1], True)
        assert_equals(par.parse_test_unit("a + (c + 4) - (e + r);")[1], True)
        assert_equals(par.parse_test_unit("a + ((c + d) + 4) - (e + r);")[1], True)
        assert_equals(par.parse_test_unit("[1,2,3,4] << 2;")[1], True)
        assert_equals(par.parse_test_unit("([1,2,3,4] << 2) << c;")[1], True)
        assert_equals(par.parse_test_unit("a;")[1], True)
        assert_equals(par.parse_test_unit("1;")[1], True)
        assert_equals(par.parse_test_unit("True;")[1], True)
        assert_equals(par.parse_test_unit("False;")[1], True)

    def test_if_parsing(self):
        par = Parser()
        par.parse_test_unit("Int a, b, d, e, g;")
        assert_equals(par.parse_test_unit("if(a==1) { }")[1], True)  # NOQA

    def test_seq_decl_parsing(self):
        par = Parser()
        assert_equals(par.parse_test_unit("@Int(10)[4] a = [1,2,3,4];")[1], True)
        assert_equals(par.parse_test_unit("[1,2,3,4];")[1], True)
        assert_equals(par.parse_test_unit("[5*5, function(1,2,3), 4];")[1], True)
        assert_equals(par.parse_test_unit("[True,False,True,False,True];")[1], True)
        assert_equals(par.parse_test_unit("[[True,False,True,False,True],[True,False,True,False,True],[True,False,True,False,True]];")[1], True)
        assert_equals(par.parse_test_unit("Int(10)[4] a;")[1], True)
        assert_equals(par.parse_test_unit("Bit[4] b;")[1], True)
        assert_equals(par.parse_test_unit("Bit[4][4] c;")[1], True)
        assert_equals(par.parse_test_unit("Bit[4][4][4] d;")[1], True)
        assert_equals(par.parse_test_unit("Bit[4][4] [4] e;"), False)
        assert_equals(par.parse_test_unit("Bit [4][4] f;"), False)
        assert_equals(par.parse_test_unit("Bit[4][4] 1;"), False)
        assert_equals(par.parse_test_unit("Bit[1][4] f = [[True,False,True,True]];")[1], True)
        assert_equals(par.parse_test_unit("Int(10)[3] g = [5*5, function(1,2,3), 4];")[1], True)

    def test_seq_op_parsing(self):
        par = Parser()
        assert_equals(par.parse_test_unit("a[5,6,7,8:10] = [1,2,3,4,5,6];")[1], True)
        assert_equals(par.parse_test_unit("Int(10)[6] b = a[5,6,7,8:10];")[1], True)
        assert_equals(par.parse_test_unit("Int(10) a[5,6,7,8:10];"), False)
        assert_equals(par.parse_test_unit("a[5,6,7-8:10];")[1], True)
        assert_equals(par.parse_test_unit("a[5,6,7,8:10]; b[5,6,7,8:10];")[1], True)
        assert_equals(par.parse_test_unit("a[5] = 10;")[1], True)
        assert_equals(par.parse_test_unit("a[5] + a[5];")[1], True)

    def test_for_parsing(self):
        par = Parser()
        par.parse_test_unit("Int b, d, e, g;")
        par.parse_test_unit("Int[4] l;")
        assert_equals(par.parse_test_unit("for(Int(10) a = 2; ((a > 4) && (b > 5)) || d > 3; d = 5, d = (e * g))\
            {\
                a = 1;\
            }")[1], True)
        assert_equals(par.parse_test_unit("for(Int(10) a = 2; ((a > 4) && (b > 5)) || d > 3; d = 5, d = (e * g))\
            { \
                for(d = 3; d < 5; d = d + 1) {\
                    a = 1;\
                }\
            }")[1], True)  # NOQA
        assert_equals(par.parse_test_unit("for(;a < 4;){}")[1], True)
        assert_equals(par.parse_test_unit("for(l[4] = 6 ;a < 4;){}")[1], True)
        assert_equals(par.parse_test_unit("for(;;){ }")[1], True)

    def test_function_call_parsing(self):
        par = Parser()
        par.parse_test_unit("Int a, b, e;")
        assert_equals(par.parse_test_unit("func(a, b, 10, 40);")[1], True)
        assert_equals(par.parse_test_unit("func(a, b, Int[10] a, 40);"), False)
        assert_equals(par.parse_test_unit("func(a, b, [1,0,1,1], 40);")[1], True)
        assert_equals(par.parse_test_unit("func (a, b, [1,0,1,1], 40);"), False)
        assert_equals(par.parse_test_unit("func(a, b, 5 * 3, e * 6);")[1], True)
        assert_equals(par.parse_test_unit("func(a, b, 5 * 3, e * 6, func(3));")[1], True)
        assert_equals(par.parse_test_unit("func(1,2,3,4)"), False)
        assert_equals(par.parse_test_unit("func(1,2,3,4);")[1], True)

    def sbox_call_parsing(self):
        par = Parser()
        par.parse_test_unit("Int a;")
        assert_equals(par.parse_test_unit("a.sbox(1);")[1], True)
        assert_equals(par.parse_test_unit("a.sbox(1 * 1);")[1], True)
        assert_equals(par.parse_test_unit("a.sbox(a);")[1], True)
        assert_equals(par.parse_test_unit("a. sbox(a);"), False)
        assert_equals(par.parse_test_unit("a .sbox(a);"), False)
        assert_equals(par.parse_test_unit("a.sbo x(a);"), False)
        assert_equals(par.parse_test_unit("a.sbox (a);"), False)

    def test_shift_op_parsing(self):
        par = Parser()
        par.parse_test_unit("Int a;")
        assert_equals(par.parse_test_unit("a << 3;")[1], True)
        assert_equals(par.parse_test_unit("a >> 3;")[1], True)
        assert_equals(par.parse_test_unit("a <<< 3;")[1], True)
        assert_equals(par.parse_test_unit("a >>> 3;")[1], True)
        assert_equals(par.parse_test_unit("10 >> 4;")[1], True)
        assert_equals(par.parse_test_unit("10 >> 4; a >> 4;")[1], True)
        assert_equals(par.parse_test_unit("([1,2,3,4] >> 4) >> 2 * 4;")[1], True)
        assert_equals(par.parse_test_unit("(5 >> 4) >> 2 * 4;")[1], True)

    def test_using_expr_parsing(self):
        par = Parser()
        assert_equals(par.parse_test_unit("Int(10) a = (5 * 10) + 3 + (3 * 2);")[1], True)

    def test_cast_parsing(self):
        par = Parser()
        par.parse_test_unit("Int(10) a, b;")
        assert_equals(par.parse_test_unit("(Int(10)) a;")[1], True)
        assert_equals(par.parse_test_unit("(Bit) a;")[1], True)
        assert_equals(par.parse_test_unit("(Int(10)[4]) 10;")[1], True)
        assert_equals(par.parse_test_unit("(Int(10)[4]) 5 * 3;")[1], True)
        assert_equals(par.parse_test_unit("(Int(10)[4]) Bit[10];"), False)
        assert_equals(par.parse_test_unit("(Int(10)[4]) Int;"), False)
        assert_equals(par.parse_test_unit("(Int(10)[4]) Bit;"), False)
        assert_equals(par.parse_test_unit("((Bit[10]) a)[5] = True;")[1], True)
        assert_equals(par.parse_test_unit("Int(10) a = ((Int(10)) op_1) + ((Int(10)) op_2);")[1], True)
        assert_equals(par.parse_test_unit("Int(10) a = ((Int(10)) op_1);")[1], True)
        assert_equals(par.parse_test_unit("Int(10) a = (Bit) op_1;")[1], True)
        assert_equals(par.parse_test_unit("Int(10) a = (Int(10)[2]) op_1;")[1], True)
        assert_equals(par.parse_test_unit("Int(10) a = (Int(10)[2][2]) op_1;"), False)
        assert_equals(par.parse_test_unit("Int(10) a = (Bit[10]) op_1;")[1], True)

    def test_function_dec_parsing(self):
        par = Parser()
        assert_equals(par.parse_test_integration("Int(10) function_1(Int(10) a, Bit b) { Int(10) a = 1; Int(10) b = 2; }")[1], True)

    def test_index_select_parsing(self):
        par = Parser()
        assert_equals(par.parse_test_unit("((Int(10)[4]) a)[3];")[1], True)


class TestASTTree(unittest.TestCase):
    """Unit tests Checking Syntax Tree is being built correctly"""

    def test_bit_decl(self):
        par = Parser()
        assert_equals(par.parse_test_unit("Bit c, d = 3 + (1 + 2 + 3) * (2 + (Bit) 3 + 2);")[1], True)
        assert_equals(par.AST.tree[0].node_type,  DATA_TYPE.BIT_DECL)
        assert_equals(par.AST.tree[1].node_type, DATA_TYPE.BIT_DECL)
        assert_equals(par.AST.tree[1].value.node_type, DATA_TYPE.EXPR)
        assert_equals(len(par.AST.tree[1].value.expressions[0].expressions), 3)
        assert_equals(par.AST.tree[1].value.expressions[0].expressions[0].expressions[0].value, "3")
        assert_equals(par.AST.tree[1].value.expressions[0].expressions[1].operator, "*")
        assert_equals(par.AST.tree[1].value.expressions[0].expressions[0].expressions[2].expressions[0].expressions[0].value, "1")
        assert_equals(par.AST.tree[1].value.expressions[0].expressions[2].expressions[1].operator, "+")
        assert_equals(par.AST.tree[1].value.expressions[0].expressions[0].expressions[2].expressions[0].expressions[2].value, "2")
        assert_equals(par.AST.tree[1].value.expressions[0].expressions[0].expressions[2].expressions[1].operator, "+")
        assert_equals(par.AST.tree[1].value.expressions[0].expressions[2].expressions[2].target.expressions[0].expressions[0].value, "3")

    def test_int_decl(self):
        par = Parser()
        assert_equals(par.parse_test_unit("Int(10) c = 2 + e * (Bit[4]) function(10,10,b * 5), d = 3, e;")[1], True)
        assert_equals(par.parse_test_unit("Int(10) c =function(b);")[1], True)
        assert_equals(par.parse_test_unit("Int(10) c = [1,2,3,4];")[1], True)
        assert_equals(par.AST.tree[0].node_type,  DATA_TYPE.INT_DECL)
        assert_equals(par.AST.tree[1].node_type,  DATA_TYPE.INT_DECL)
        assert_equals(par.AST.tree[2].node_type,  DATA_TYPE.INT_DECL)
        assert_equals(par.AST.tree[0].ID, "c")
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].expressions[0].value,  "2")
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[1].operator,  "*")
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].expressions[2].ID,  "e")
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[1].operator,  "*")
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[2].node_type, DATA_TYPE.CAST)
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[2].target.expressions[0].ID, "function")
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[2].target.expressions[0].parameters[0].expressions[0].value, "10")

    def test_bs_decl(self):
        par = Parser()
        assert_equals(par.parse_test_unit("@Int(10) varName;")[1], True)
        assert_equals(par.AST.tree[0].node_type, DATA_TYPE.BS_INT_DECL)
        assert_equals(par.parse_test_unit("Int(10) varName;")[1], True)
        assert_equals(par.AST.tree[1].node_type, DATA_TYPE.INT_DECL)
        assert_equals(par.parse_test_unit("@Int(10)[10] varName;")[1], True)
        assert_equals(par.AST.tree[2].node_type, DATA_TYPE.BS_SEQ_INT_DECL)
        assert_equals(par.parse_test_unit("Int(10)[10] varName;")[1], True)
        assert_equals(par.AST.tree[3].node_type, DATA_TYPE.SEQ_INT_DECL)
        assert_equals(par.parse_test_unit("Bit[10] varName;")[1], True)
        assert_equals(par.AST.tree[4].node_type, DATA_TYPE.SEQ_BIT_DECL)

    def test_int_seq_decl(self):
        par = Parser()
        assert_equals(par.parse_test_unit("Int(10)[5] a = [1,function(1,2,3),function(), (1*2*3) << 4, d + e];")[1], True)
        assert_equals(par.parse_test_unit("Int(10)[2][2] f = [[1,2],[3,4]];")[1], True)
        assert_equals(par.parse_test_unit("Int(10)[2][2][2] f = [[[[1 * 2 * 3,2],[(Int(10)) [1,2,3,4],3]]],[[[5,6],[7,8]]]];")[1], True)
        assert_equals(par.parse_test_unit("[1,2,3,4];")[1], True)
        assert_equals(par.parse_test_unit("Int(10)[1][2] b = [[],[]];")[1], True)
        assert_equals(par.parse_test_unit("Int(10)[5] b = c[1,2,3:5];")[1], True)
        assert_equals(par.parse_test_unit("Int(10)[5] b;")[1], True)
        assert_equals(par.AST.tree[0].ID, "a")
        assert_equals(par.AST.tree[0].bit_constraints.expressions[0].value, "10")
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].node_type, DATA_TYPE.SEQ_VAL)
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[0].expressions[0].value, "1")
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[1].expressions[0].parameters[0].expressions[0].value, "1")
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[3].expressions[0].expressions[0].expressions[0].expressions[0].value, "1")
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[3].expressions[0].expressions[0].expressions[1].operator, "*")
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[3].expressions[0].expressions[0].expressions[0].expressions[2].value, "2")
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[3].expressions[0].expressions[1].operator, "<<")
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[3].expressions[0].expressions[2].value, "4")
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[4].expressions[0].expressions[0].ID, "d")
        assert_equals(par.parse_test_unit("Int(10) z = b[1 * 4];")[1], True)
        assert_equals(par.AST.tree[7].ID, "z")
        assert_equals(par.AST.tree[7].value.expressions[0].ID, "b")
        assert_equals(par.AST.tree[7].value.expressions[0].indices[0].expressions[0].expressions[0].expressions[0].value, "1")
        assert_equals(par.AST.tree[7].value.expressions[0].indices[0].expressions[0].expressions[0].expressions[1].operator, "*")
        assert_equals(par.AST.tree[7].value.expressions[0].indices[0].expressions[0].expressions[0].expressions[2].value, "4")
        assert_equals(par.parse_test_unit("Int(10) a = 2;")[1], True)

    def test_bit_seq_decl(self):
        par = Parser()
        assert_equals(par.parse_test_unit("Bit[5] b = [True, False, True, False];")[1], True)
        assert_equals(par.parse_test_unit("Bit[1][2] b = [[True, False, True, False],[True, False, True, False]];")[1], True)
        assert_equals(par.parse_test_unit("Bit[1][2] b = [[],[]];")[1], True)
        assert_equals(par.parse_test_unit("Bit[1] b = [];")[1], True)
        assert_equals(par.parse_test_unit("Bit[1] b;")[1], True)
        assert_equals(par.AST.tree[0].node_type, DATA_TYPE.SEQ_BIT_DECL)
        assert_equals(par.AST.tree[0].size[0].expressions[0].value, "5")
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[0].expressions[0].value, "True")
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].value[1].expressions[0].value, "False")

    def test_id_set(self):
        par = Parser()
        assert_equals(par.parse_test_unit("a = b + 10 * function(a, b);")[1], True)
        assert_equals(par.parse_test_unit("a = [];")[1], True)
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[0].expressions[0].ID, "b")
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[1].operator, "*")
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[2].parameters[0].expressions[0].ID, "a")
        assert_equals(par.AST.tree[0].value.expressions[0].expressions[2].parameters[1].expressions[0].ID, "b")
        assert_equals(par.parse_test_unit("a[1,2,3,4:5] = (Bit[4]) b + 10 * function(a, b);")[1], True)
        assert_equals(par.AST.tree[2].target.indices[0].expressions[0].expressions[0].value, "1")
        assert_equals(par.AST.tree[2].target.indices[0].expressions[1].expressions[0].value, "2")
        assert_equals(par.AST.tree[2].target.indices[0].expressions[3].expressions[0].start.expressions[0].value, "4")
        assert_equals(par.AST.tree[2].value.expressions[0].target.expressions[0].expressions[2].node_type, DATA_TYPE.FUNCTION_CALL)
        assert_equals(par.parse_test_unit("a[1,2][1,2,3,4:5] = (Bit[4]) b + 10 * function(a, b);")[1], True)
        assert_equals(par.parse_test_unit("a[5,6,7,8:10] = [1,2,3,4,5,6];")[1], True)
        assert_equals(par.AST.tree[4].node_type, DATA_TYPE.ID_SET)
        assert_equals(par.AST.tree[4].target.indices[0].expressions[0].expressions[0].value, "5")

    def test_func_decl(self):
        par = Parser()
        assert_equals(par.parse_test_integration("Bit function_1(Int(5) a, Bit b, Int(5)[4][4][4] test, Bit[5] b) { Int(10) a = 1; Int(10) b = 2; Int(10) c = 0xa; }")[1], True)  # NOQA
        assert_equals(par.AST.tree[0].ID, "function_1")
        assert_equals(par.AST.tree[0].stmts[0].value.expressions[0].value, '1')
        assert_equals(par.AST.tree[0].stmts[1].value.expressions[0].value, '2')
        assert_equals(par.AST.tree[0].stmts[2].value.expressions[0].value, '10')
        par = Parser()
        assert_equals(par.parse_test_integration("Bit function_1(Int(5)[4][4][4] test) { Int(10) a = 1; Int(10) b = 2; Int(10) c = 0xa; }")[1], True)  # NOQA

    def test_return_stmt(self):
        par = Parser()
        assert_equals(par.parse_test_unit("return a * b * c * 10;")[1], True)
        assert_equals(par.AST.tree[0].node_type, DATA_TYPE.RETURN_STMT)
        assert_equals(par.AST.tree[0].expr.expressions[0].expressions[0].expressions[0].expressions[0].ID, "a")
        assert_equals(par.AST.tree[0].expr.expressions[0].expressions[0].expressions[1].operator, "*")

    def test_for_loop(self):
        par = Parser()
        assert_equals(par.parse_test_unit("for(Int(10) a = 5, Bit f = False; (a < 5) && (d < 5); a = a + 1, b = b + 3) { b = b <<< 1; z = b + 19; }")[1], True)
        assert_equals(par.parse_test_unit("for(;;) { }")[1], True)
        assert_equals(par.AST.tree[0].node_type, DATA_TYPE.FOR_LOOP)
        assert_equals(par.AST.tree[1].node_type, DATA_TYPE.FOR_LOOP)
        assert_equals(par.AST.tree[0].terminator[0].expressions[0].expressions[1].operator, "&&")
        assert_equals(par.AST.tree[0].body[0].node_type, DATA_TYPE.ID_SET)
        assert_equals(par.AST.tree[0].body[0].target.ID, "b")

    def test_if_stmt(self):
        par = Parser()
        assert_equals(par.parse_test_unit("if(i > 3) { b = b + 1; c = d + 3; } if(d < 4) { z = z + 1; kk = k + 3; }")[1], True)
        assert_equals(par.AST.tree[0].node_type, DATA_TYPE.IF_STMT)
        assert_equals(par.AST.tree[1].node_type, DATA_TYPE.IF_STMT)
        assert_equals(par.AST.tree[0].condition[0].expressions[0].expressions[0].expressions[0].ID, "i")
        par = Parser()
        assert_equals(par.parse_test_unit("if(i > 3) { if(d < 4) { z = z + 1; kk = k + 3; } } ")[1], True)
        assert_equals(par.AST.tree[0].body[0].condition[0].expressions[0].expressions[0].expressions[0].ID, "d")

    def test_casting(self):
        par = Parser()
        assert_equals(par.parse_test_unit("a =(@Int(10)) a;")[1], True)

    def test_indexing(self):
        par = Parser()
        assert_equals(par.parse_test_unit("((Bit[4]) ((Int(5)) a))[5] = True;")[1], True)
        assert_equals(par.parse_test_unit("a[5] = True;")[1], True)

    def test_sbox(self):
        par = Parser()
        assert_equals(par.parse_test_unit("Sbox(4)[16] prince = [0xb, 0xf, 0x3, 0x2, 0xa, 0xc, 0x9, 0x1, 0x6, 0x7, 0x8, 0x0, 0xe, 0x5, 0xd, 0x4];")[1], True)


class TestSemanticAnalysis(unittest.TestCase):
    """Unit tests Checking Semantic Analysis"""

    def test_int_decl(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(10) a = 10;\
                                                                        Int(8) b = a;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 4 << [1,2,3,4] << 2;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 4 << 3 << 2;")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10;")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10; Int(10) a = 20;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10; Int(10) b = 20;")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10; Int(10) b = a;")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = False;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10 + False << 4;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a; Int(10) b = a;")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(10) a; @Int(10) b = a + 3;")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(10) a; Int(10) b = 3 + 3 * (4 << a);")), True)

    def test_semantic_expr(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit a = 1;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10 * 2) b = 1;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8) b = 0; b = [True, False];")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8) c = [True,False,True,False,True];")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8) c = 0; c[0] = True;")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8) c = 0; c[0] = 1;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8) c = 0; c[1,2,3,0] = [True, False, True, True];")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8) c = 0; c[1,2,3,0] = 1 * True;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8) c = [True,False,True,False] + [True,False,True,True];")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("5 * [1,2,3,4];")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8) b; b = [[True, False, True, True]] + [True, False, True, True];")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8) b; b = [[True, False, True, True]] ^ [True, False, True, True];")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(8) a = 10; @Int(8) b = 10; @Int(8) c = a / b;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8) a = 10; @Int(8) b = 10; @Int(8) c = a / b;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8) a = 10; @Int(8) b = 10; @Int(8) c = a + b;")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8) a = 10; @Int(8) b = 10; @Int(8) c = a * b;")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8) a = 10; @Int(8) b = 10; @Int(8) c = a % b;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(8) a = 10; @Int(8) b = 10; @Int(8) c = a - b;")), True)

    def test_bit_decl(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit a = False;")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit a = 1;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit a = False + False;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit a = False; Bit a = True;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit a; Bit b = a;")), True)

    def test_mixing_bit_int(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Bit b = True;")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Bit b = True; Int(10) c = b;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Bit b = True; Int(10) c = 5 * (b);")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Int(10) b = 10; Int(10) c = 5 * (b);")), True)

    def test_id_set(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(10) a; Int(10) b; b = a;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Int(10) b = a;")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Int(10) b = a; Bit c = b;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Int(10) b = a * 10 * 3 << 4;")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 5;  Bit d = False; Int(10) b = a * 10 * 3 << d;")), False)

    def test_seq_decl(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2][2] a = [[1,2],[3,4]]; ")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2][2] a = [[False,2],[3,4]]; ")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[4] a = [1, 2, 3, 4]; ")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2] a = [1]; ")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2] a = [1,2,3,4] ^ [1,2,3,4];")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2] a = ([1,2,3,4] ^ [1,2,3,4]) ^ ([1,2,3,4] ^ [1,2,3,4]);")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2] a = ([1,2,3,4] ^ [1,2,3,4]) ^ ([1,2,3,4] << 4);")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2] a = ([1,2,3,4] ^ [1,2,3,4]) ^ ([[1],[2],[3],[4]] << 4);")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[2] b = [1,2]; Int(10)[2] a = ([1,2,3,4] ^ [1,2,3,4]) ^ ([1,2,3,4] << b[0]);")), False)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) b = 3; Int(10)c = 4; Int(10)[2] a = [b,2,c,4] ^ [1,2,b * 2,4];")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) b = 3; Int(10)c = 4; Bit d = False; Int(10)[2] a = [b,d,c,4] ^ [1,2,b,4];")), False)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[4] a = [1,2,3,4];")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(a * a)[4] a = [1,2,3,4];")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10)[4] a = [1,2,3,4]; Int(10) c; c = a;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[4] a = [True,False,True,False];")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[4] a = [True,False,True,False,[True, False]];")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[4] a = [1,False,True,False];")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[4][4] a = [[True,False,True,False],[True,False,True,False]];")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[2][2] a = [[[1],[2]],[[1],[2]]];")), False)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[2][2][1] a = [[[1],[2]],[[1],[2]]];")), True)  # NOQA

    def test_bs_seq_decl(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(10)[10] a = [1,2,3,4,5,6,7,8,9,10]; ")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(10)[2][2] a = [[1,2], [3,4]]; ")), True)

    def test_if_stmt(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) a = 4; if((4 > 4) && (4 < 6)) { a = 10; }")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(4) a = 4; if((a > 4) && (4 < 6)) { a = 10; }")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(4) a = 4; if((a > a) && (4 < 6)) { a = 10; }")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(4) a = 4; Bit d = True; if((d == d) && (4 < 6)) { a = 10; }")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(4) a = 4; Bit d = True; if((d <= d) && (4 < 6)) { a = 10; }")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(4) a = 4; Bit d = True; if((d != d) && (4 < 6)) { a = 10; }")), True)

    def test_for_loop(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("for(Int(10) i = 5, Bit b = False; b != True; i = i + 5) { b = True; }")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("for(Int(10) i = 5, Bit b = False; b != True; i = i + 5) { b = True; } b = True;")), False)  # NOQA b is out of scope!
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit b; for(Int(10) i = 5; b != True; i = i + 5) { b = True; } b = True;")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit b; for(Int(10) i = 5; b != True; i = i + 5) { b = True; } b = 10;")), False)

    def test_func_decl(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8) test_func(Int(8) a, Bit c, Bit[5] e) { Int(10) d = 1;  Bit b = False; return d;}")), True)  # NOQA
        assert_equals(par.semantic_analyser.sym_table.f_table['test_func']['return']['type'], DATA_TYPE.INT_VAL)

    def test_func_call(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) test_func(Int(10) a) { Int(10) d = test_func(test_func(10)) + 20; return d;}")), True)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit test_func(Int(10) a) { Int(10) d = 10; return True;}")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit test_func1(Int(10) a) { a = a + 10; return False; }\
                                                                            Int(10) test_func(Int(10) a) { Int(10) d = test_func(test_func1(10)) + 20; return d;}")), False)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(10) test_func2(Bit a) { @Int(10) d = 39; return d;}\
                                                                            void test_func3(Bit a) { @Int(10) i = test_func2(False); }")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(10) test_func2(@Int(8) c) { c = 4 + 39; return c;}")), True)

class test_IR_generation(unittest.TestCase):
    """Unit tests Checking IR tree is being built correctly"""

    def test_int_decl(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10;")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10 + 5;")), True)
        assert_equals(par.semantic_analyser.IR.IR[0].node_type, DATA_TYPE.INT_DECL)
        assert_equals(par.semantic_analyser.IR.IR[0].value.left.value, "10")
        assert_equals(par.semantic_analyser.IR.IR[0].value.right.value, "5")
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = 10 + (5 * 4);")), True)
        assert_equals(par.semantic_analyser.IR.IR[0].value.left.value, "10")
        assert_equals(par.semantic_analyser.IR.IR[0].value.right.operator, "*")
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = False;")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) a = [True, False, True, True];")), True)

    def test_bit_seq_decl(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[2][2] a = [[True,False],[True,False]];")), True)
        assert_equals(par.semantic_analyser.IR.IR[0].node_type, DATA_TYPE.SEQ_BIT_DECL)
        assert_equals(par.semantic_analyser.IR.IR[0].value.type, DATA_TYPE.SEQ_BIT_VAL)
        assert_equals(par.semantic_analyser.IR.IR[0].value.type, DATA_TYPE.SEQ_BIT_VAL)
        assert_equals(par.semantic_analyser.IR.IR[0].value.value[0].value[0].value, "True")
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[4] a;")), True)

    def test_int_seq_decl(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) b = 3; Int(10)c = 4; Int(10)[2][2] a = [[b * 4,5],[c / 5, 5]];")), True)
        assert_equals(par.semantic_analyser.IR.IR[2].value.value[0].value[0].node_type, DATA_TYPE.ARITH_OP)
        assert_equals(par.semantic_analyser.IR.IR[2].value.value[0].value[0].left.name, "b")
        assert_equals(par.semantic_analyser.IR.IR[2].value.value[0].value[0].left.type, DATA_TYPE.INT_VAL)
        assert_equals(par.semantic_analyser.IR.IR[2].value.value[1].value[0].node_type, DATA_TYPE.ARITH_OP)
        assert_equals(par.semantic_analyser.IR.IR[2].value.value[1].value[0].left.name, "c")
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(10) b = 3; Int(10)c = 4; Int(10)[2][2] a = [[b << 3,5],[c / 5, 5]];")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit d = False; Int(10) b = 3; Int(10)c = 4; Int(10)[2][2] a = [[b << d,5],[c / 5, 5]];")), False)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[10][10] ret_func(Int(8)[10][10] a){\
                                                                            return a;\
                                                                        }\
                                                                        void test_ret() {\
                                                                            Int(8)[10][10] b;\
                                                                            Int(8)[10][10] a = ret_func(b);\
                                                                        }\
                                                                        ")), False)
    def test_if_stmt(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) a = 4; if((4 > 4) && (4 < 6)) { a = 10; }")), True)
        assert_equals(par.semantic_analyser.IR.IR[1].node_type, DATA_TYPE.IF_STMT)
        assert_equals(len(par.semantic_analyser.IR.IR), 2)
        assert_equals(par.semantic_analyser.IR.IR[1].body[0].node_type, DATA_TYPE.ID_SET)
        assert_equals(par.semantic_analyser.IR.IR[1].condition.operator, "&&")
        assert_equals(par.semantic_analyser.IR.IR[1].condition.left.operator, ">")
        assert_equals(par.semantic_analyser.IR.IR[1].condition.left.type, DATA_TYPE.BIT_VAL)
        assert_equals(par.semantic_analyser.IR.IR[1].condition.left.left.value, "4")
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) row = 0; if(row == 0 || row == 2)    { }")), True)
        assert_equals(par.semantic_analyser.IR.IR[1].condition.operator, "||")
        assert_equals(par.semantic_analyser.IR.IR[1].condition.left.operator, "==")
        assert_equals(par.semantic_analyser.IR.IR[1].condition.left.right.value, "0")

    def test_for_loop(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("for(Int(8) d, Int(8) a = 0, Int(8)[5] e = [1,2,3,4,5], Bit[4] f; a < 10; a = a + 1, d = d * a) {\
                                                                            d = d << 10;\
                                                                         }")), True)
        assert_equals(par.semantic_analyser.IR.IR[0].node_type, DATA_TYPE.FOR_LOOP)
        assert_equals(par.semantic_analyser.IR.IR[0].initializer[0].node_type, DATA_TYPE.INT_DECL)
        assert_equals(par.semantic_analyser.IR.IR[0].initializer[0].ID.name, "d")
        assert_equals(par.semantic_analyser.IR.IR[0].terminator[0].operator, "<")
        assert_equals(par.semantic_analyser.IR.IR[0].terminator[0].left.name, "a")
        assert_equals(par.semantic_analyser.IR.IR[0].terminator[0].left.type, DATA_TYPE.INT_VAL)
        assert_equals(par.semantic_analyser.IR.IR[0].increment[1].node_type, DATA_TYPE.ID_SET)
        assert_equals(par.semantic_analyser.IR.IR[0].increment[1].value.operator, "*")
        assert_equals(par.semantic_analyser.IR.IR[0].increment[1].value.left.name, "d")
        assert_equals(par.semantic_analyser.IR.IR[0].body[0].node_type, DATA_TYPE.ID_SET)
        assert_equals(par.semantic_analyser.IR.IR[0].body[0].value.type, DATA_TYPE.INT_VAL)
        assert_equals(par.semantic_analyser.IR.IR[0].body[0].value.left.name, "d")

    def test_func_decl(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8) test_func(Int(8) a, Bit c, Bit[5] e, @Int(64) f) { @Int(10) d = (1 + 3) + f;  Bit b = False; return a;}")), True)  # NOQA
        assert_equals(par.semantic_analyser.IR.IR[0].parameters[3].ID.type, DATA_TYPE.BS_INT_VAL)
        assert_equals(par.semantic_analyser.IR.IR[0].body[0].value.type, DATA_TYPE.BS_INT_VAL)
        assert_equals(par.semantic_analyser.IR.IR[0].body[0].value.left.type, DATA_TYPE.INT_VAL)

    def test_index_setting(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[8][8] a = [[1,2,3,4],[5,6,7,8]]; a[3][2] = 5;")), True)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[8] a = [1,2,3,4,5,6,7,8]; a[3][2] = True;")), True)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[8] a = [1,2,3,4,5,6,7,8]; a[3] = [1,2,3,4,5,5];")), False)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[8][4] a = [[1,2,3,4],[5,6,7,8]]; a[3] = [1,2];")), False)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[8][5][10] a = [[[1]],[[5]]]; a[3][3][3] = 1;")), True)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[8][2] a = [1,2,3,4,5,6,7,8]; a[3][3][3] = 1;")), False)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) b = 4; Int(4)[5] a = [1,2,3,4,5];")), True)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) b = 4; Int(4)[5] a = [1,2,3,4,5]; a[b * 4: 4] = 10;")), False)  # NOQA Must assign sequence to range value

    def test_int_index_select(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) a = 10; a[3] = True;")), True)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) a = 10; a[5 : 8] = [True,False,True];")), True)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) a = 10; a[1] = a[2] ^ a[3];")), True)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) a = 10; a[1] = a[2][1] ^ a[3];")), False)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4)[5] a = [1,2,3,4,5]; a[1][1] = a[1][1] ^ a[1][2];")), True)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8) a = 10; a[1] = a[2] ^ a[4] ^ a[6];")), True)  # NOQA
        assert_equals(par.semantic_analyser.IR.IR[1].target.type, DATA_TYPE.BIT_VAL)
        assert_equals(par.semantic_analyser.IR.IR[1].value.left.type, DATA_TYPE.BIT_VAL)
        assert_equals(par.semantic_analyser.IR.IR[1].value.type, DATA_TYPE.BIT_VAL)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) a = 10; a[1] = 1;")), False)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4)[5] a = [1,2,3,4,5]; a[1][5 : 8] = [True,False,True];")), True)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4)[5] a = [1,2,3,4,5]; a[1][5 : 8][4] = [True,False,True];")), False)  # NOQA

    def test_sbox(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Sbox(4)[16] prince = [0xb, 0xf, 0x3, 0x2, 0xa, 0xc, 0x9, 0x1, 0x6, 0x7, 0x8, 0x0, 0xe, 0x5, 0xd, 0x4]; @Int(64) a = 10;\
                                                                            a[0:4] = prince[a[0:4]];")), True)

    def test_LFSR_syntax(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4)[10] a = [1,2,3,4]; a[1] = a[5] ^ a[5] ^ a[5];")), True)  # NOQA
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(8) lfsr(@Int(8) state) {\
                                                                            @Int(1) output;\
                                                                            @Int(1) input;\
                                                                            for(Int(5) i = 0; i < 32; i = i + 1) {\
                                                                                output[0] = state[0];\
                                                                                input[0] =  state[0] ^ state[4] ^ state[5] ^ state[6];\
                                                                                state = state << 1;\
                                                                                state[7] = input[0];\
                                                                             }\
                                                                             return state;\
                                                                        }")), True)  # NOQA
        assert_equals(par.semantic_analyser.IR.IR[0].node_type, DATA_TYPE.FUNC_DECL)

    def test_PRESENT_syntax(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Sbox(4)[16] s = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15];\
                                                                        @Int(64) pLayer(@Int(64) state) {\
                                                                            Int(8) target_bit;\
                                                                            @Int(64) temp = state;\
                                                                            for(Int(8) bit = 0; bit < 64; bit = bit + 1)    {\
                                                                                target_bit = (16*bit) % 63;\
                                                                                if(bit == 63)   {\
                                                                                    target_bit = 63;\
                                                                                }\
                                                                                state[target_bit] = temp[bit];\
                                                                            }\
                                                                            return state;\
                                                                        }\
                                                                        @Int(64) sBox_layer(@Int(64) state)  {\
                                                                            for(Int(4) i = 0; i < 16; i = i + 1){\
                                                                                state[(i * 4) : (i * 4) + 4] = s[state[(i * 4) : (i * 4) + 4]];\
                                                                            }\
                                                                            return state;\
                                                                        }\
                                                                        @Int(64)[32] generate_round_keys(@Int(64)[32] round_keys, @Int(80) key) {\
                                                                            for(Int(5) round = 0; round < 32; round = round + 1)    {\
                                                                                round_keys[round][0: 63] = key[16:79];\
                                                                                key = key <<< 61;\
                                                                                key[76 : 79] = s[key[79:76]];\
                                                                                key[15 : 19] = key[15 : 19] ^ round[0 : 5];\
                                                                            }\
                                                                            return round_keys;\
                                                                        }")), True)

    def test_PRINCE_syntax(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Sbox(4)[16] s = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15];\
                                                                        void enc(@Int(64)[11] RC, @Int(64) state, @Int(64) key_0, @Int(64) key_1) {\
                                                                            @Int(64) key_prime = (key_0 >>> 1) ^ (key_0 >> 63);\
                                                                                state = state ^ key_1;\
                                                                                state = state ^ RC[0];\
                                                                        }\
                                                                        @Int(64) sBox_layer(@Int(64) state)  {\
                                                                            for(Int(4) i = 0; i < 16; i = i + 1){\
                                                                                state[(i * 4) : (i * 4) + 4] = s[state[(i * 4) : (i * 4) + 4]];\
                                                                            }\
                                                                            return state;\
                                                                        }\
                                                                        @Int(16) m1(@Int(16) state)   {\
                                                                            @Int(16) output;\
                                                                            output[ 0] = state[0] ^ state[ 4] ^ state[ 8];\
                                                                            output[ 1] = state[5] ^ state[ 9] ^ state[13];\
                                                                            output[ 2] = state[2] ^ state[10] ^ state[14];\
                                                                            output[ 3] = state[3] ^ state[ 7] ^ state[15];\
                                                                            output[ 4] = state[0] ^ state[ 4] ^ state[12];\
                                                                            output[ 5] = state[1] ^ state[ 5] ^ state[ 9];\
                                                                            output[ 6] = state[6] ^ state[10] ^ state[14];\
                                                                            output[ 7] = state[3] ^ state[11] ^ state[15];\
                                                                            output[ 8] = state[0] ^ state[ 8] ^ state[12];\
                                                                            output[ 9] = state[1] ^ state[ 5] ^ state[13];\
                                                                            output[10] = state[2] ^ state[ 6] ^ state[10];\
                                                                            output[11] = state[7] ^ state[11] ^ state[15];\
                                                                            output[12] = state[4] ^ state[ 8] ^ state[12];\
                                                                            output[13] = state[1] ^ state[ 9] ^ state[13];\
                                                                            output[14] = state[2] ^ state[ 6] ^ state[14];\
                                                                            output[15] = state[3] ^ state[ 7] ^ state[11];\
                                                                            return output;\
                                                                        }\
                                                                        \
                                                                        @Int(16) m0(@Int(16) state)   {\
                                                                            @Int(16) output;\
                                                                            output[ 0] = state[4] ^ state[ 8] ^ state[12];\
                                                                            output[ 1] = state[1] ^ state[ 9] ^ state[13];\
                                                                            output[ 2] = state[2] ^ state[ 6] ^ state[14];\
                                                                            output[ 3] = state[3] ^ state[ 7] ^ state[11];\
                                                                            output[ 4] = state[0] ^ state[ 4] ^ state[ 8];\
                                                                            output[ 5] = state[5] ^ state[ 9] ^ state[13];\
                                                                            output[ 6] = state[2] ^ state[10] ^ state[14];\
                                                                            output[ 7] = state[3] ^ state[ 7] ^ state[15];\
                                                                            output[ 8] = state[0] ^ state[ 4] ^ state[12];\
                                                                            output[ 9] = state[1] ^ state[ 5] ^ state[ 9];\
                                                                            output[10] = state[6] ^ state[10] ^ state[14];\
                                                                            output[11] = state[3] ^ state[11] ^ state[15];\
                                                                            output[12] = state[0] ^ state[ 8] ^ state[12];\
                                                                            output[13] = state[1] ^ state[ 5] ^ state[13];\
                                                                            output[14] = state[2] ^ state[ 6] ^ state[10];\
                                                                            output[15] = state[7] ^ state[11] ^ state[15];\
                                                                            return output;\
                                                                        }\
                                                                        @Int(64) mPrime(@Int(64) state)    {\
                                                                            state[0:15] = m0(state[0:15]);\
                                                                            state[16:31] = m1(state[16:31]);\
                                                                            state[32:47] = m1(state[32:47]);\
                                                                            state[48:63] = m0(state[48:63]);\
                                                                            return state;\
                                                                        }")), True)

    def test_return_type(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[2] feature_testing(Int(8)[2] a){\
                                                                            return a;\
                                                                        }\
                                                                         ")), True);
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(20)[64][64] pLayer(Int(20)[64][64] state) {\
                                                                            return state;\
                                                                        }")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit pLayer(Bit state) {\
                                                                            return state;\
                                                                        }")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[30] pLayer(Bit[30] state) {\
                                                                            return state;\
                                                                        }")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Bit[30][3] pLayer(Bit[30][3] state) {\
                                                                            return state;\
                                                                        }")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("void pLayer(Bit[30][3] state) {\
                                                                        }")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(64) pLayer(@Int(64) state) {\
                                                                            return state;\
                                                                        }")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(64)[30] pLayer(@Int(64)[30] state) {\
                                                                            return state;\
                                                                        }")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(64)[30] pLayer(Bit state) {\
                                                                            return state;\
                                                                        }")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Int(64) pLayer(Int(64)[30] state) {\
                                                                            return state;\
                                                                        }")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[10] ret_func(Int(8)[10][10] a){\
                                                                            return a;\
                                                                        }\
                                                                        ")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8)[10][10] ret_func(Int(8)[10][10] a){\
                                                                            return a;\
                                                                        }\
                                                                        ")), True)


    def test_sbox(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("void test(Int(8) input){\
                                                                    @Int(4) i;\
                                                                    Sbox(4)[16] prince = [0xb, 0xf, 0x3, 0x2, 0xa, 0xc, 0x9, 0x1, 0x6, 0x7, 0x8, 0x0, 0xe, 0x5, 0xd, 0x4];\
                                                                }\
                                                                ")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(4) i;\
                                                                        Sbox(4)[16] prince = [0xb, 0xf, 0x3, i, 0xa, 0xc, 0x9, 0x1, 0x6, 0x7, 0x8, 0x0, 0xe, 0x5, 0xd, 0x4];\
                                                                ")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Sbox(4)[16] prince = [0xb, 0xf, 0x3, 0x2, 0xa, 0xc, 0x9, 0x1, 0x6, 0x7, 0x8, 0x0, 0xe, 0x5, 0xd];")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Sbox(4)[16] prince = [0xb, 0xf, 0x3, 0x2, 0xa, 0xc, 0x9, 0x1, 0x6, 0x7, 0x8, 0x0, 0xe, 0x5, 0xd, 0x4];\
                                                                    void test(Int(8) input){\
                                                                    @Int(4) i;\
                                                                }\
                                                                ")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Sbox(4)[16] prince = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,16];")), False)
        
    def test_sequence_sizes_bounds(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("void range_set()    {\
                                                                            Int(8)[2][2] a = [[1,2],[1,2]];\
                                                                        }\
                                                                        ")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("void range_set()    {\
                                                                            Int(8)[1][2] a = [[1,2,3],[1,2]];\
                                                                        }\
                                                                        ")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("void range_set()    {\
                                                                            Int(8)[2][2] a = [[1,2],[1,2,3]];\
                                                                        }\
                                                                        ")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("void range_set()    {\
                                                                            Int(8)[2][2][2] a = [[[1,2],[1,2]],[[1,2],[1,2]]];\
                                                                        }\
                                                                        ")), True)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("void range_set()    {\
                                                                            Int(8)[2][2][2] a = [[[1,2],[1,2]],[[1,2,4],[1,2]]];\
                                                                        }\
                                                                        ")), False)
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("void range_set()    {\
                                                                            Int(8)[2][2][2][2] b = [[[[1,2],[1,2]],[[1,2],[1,2]]],[[[1,2],[1,2]],[[1,2],[1,2]]]];\
                                                                        }\
                                                                        ")), True)
    def test_indexing(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("void range_set()    {\
                                                                            Int(8)[4][4] a;\
                                                                            Int(8)[4][4] d;\
                                                                            d[2] = a[2];\
                                                                        }\
                                                                        ")), False)

class test_translation(unittest.TestCase):
    """Unit tests Checking translations are valid"""

    # def test_demo_code(self):
    #     par = Parser()
    #     par.analyse_tree_test(par.parse_test_AST_semantic("@Int(8) bs_seq_bit_expr_mult() {\
    #                                                             @Int(8) a = 1;\
    #                                                             Int(8) b;\
    #                                                             a[0,1,2] = ([True, False, True, True] ^ [True, False, True, True]) * a;\
    #                                                             return a;\
    #                                                         }\
    #                                                     "))
    #     print(par.semantic_analyser.IR.translate()['main'])

    def test_run_time_error(self):
        par = Parser()
        if par.analyse_tree_test(par.parse_test_AST_semantic("void Error_1(){\
                                                            Int(8) a = 7;\
                                                            Int(8) b = 9;\
                                                            b[0,1,2,3,4] = a[a,b];\
                                                        }\
                                                        void Non_Error_2(){\
                                                            Int(8) a = 5;\
                                                            Int(8) b = 7;\
                                                            b[0,1,2,3,4] = a[a,b];\
                                                        }\
                                                        void Error_3(){\
                                                            Int(8) a = 5;\
                                                            Int(8) b = 2;\
                                                            b[0,1,2,3,4] = a[a:b];\
                                                        }\
                                                        void Error_4(){\
                                                            Int(8) a = 0;\
                                                            Int(8) b = 10;\
                                                            b[a:b] = a[0:3];\
                                                        }\
                                                        void Error_5(){\
                                                            Int(8) a = 0;\
                                                            Int(8) b = 10;\
                                                            Int(8)[10] c;\
                                                            c[b][0:3] = a[0:3];\
                                                        }\
                                                        void Error_6(){\
                                                            Int(8) a = 0;\
                                                            Int(8) b = 10;\
                                                            Int(8)[10][10] c;\
                                                            c[8][8][b] = a[0];\
                                                        }\
                                                        ")) is True:
            if Data_reader.write_test("runtime_checks", "run_time_errors_dsl", par.semantic_analyser.IR.translate()) is True:
                assert_equals(subprocess.call(['test_output/runtime_checks/./run_tests.sh']), 0)


    def test_general_operations(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Int(8) int_index_set_1()    {\
                                                                            Int(8) a = 10;\
                                                                            a[3] = a[1];\
                                                                            return a;\
                                                                        }\
                                                                        Int(8) int_index_set_2()    {\
                                                                            Int(8) a = 0;\
                                                                            a[0,1,3] = [True, False, True];\
                                                                            return a;\
                                                                        }\
                                                                        Int(8) int_index_set_3()    {\
                                                                            Int(8) a = 5;\
                                                                            a[0,1,2,3] = a[0,1,2,3] << 1;\
                                                                            return a;\
                                                                        }\
                                                                        Int(8) int_index_set_4()    {\
                                                                            Int(8) a = 5;\
                                                                            a[0,1,2,3] = a[0,1,2,3] <<< 3;\
                                                                            return a;\
                                                                        }\
                                                                        Int(8) int_index_set_5()    {\
                                                                            Int(8) a = 19;\
                                                                            a[0,1,2,3,4] = a[0,1,2,3,4] >>> 3;\
                                                                            return a;\
                                                                        }\
                                                                        Int(8) int_index_set_6()    {\
                                                                            Int(8) a = 19;\
                                                                            a[0,1,2,3,4] = a[0:4] >>> 3;\
                                                                            return a;\
                                                                        }\
                                                                        Int(8) int_index_set_7()    {\
                                                                            Int(8) a = 0;\
                                                                            a[0:4] = [True, False, True, True];\
                                                                            return a;\
                                                                        }\
                                                                        Int(8) int_index_set_8()    {\
                                                                            Int(8) a = 0;\
                                                                            a = [True, False, True, True];\
                                                                            return a;\
                                                                        }\
                                                                        Int(8) int_index_set_9()    {\
                                                                            Int(8) a = 0;\
                                                                            a = [True, False, True, True] + 10;\
                                                                            return a;\
                                                                        }\
                                                                        Int(8) int_index_set_10()    {\
                                                                            Int(8) a = 0;\
                                                                            a = ([True, False, True, True] <<< 1) + 10;\
                                                                            return a;\
                                                                        }\
                                                                        Int(8) int_index_set_11()    {\
                                                                            Int(8) a = 7;\
                                                                            a[0,1,2,3] = a[3,2,1,0];\
                                                                            return a;\
                                                                        }\
                                                                        Int(8) int_index_set_12()    {\
                                                                            Int(8) a = 15;\
                                                                            a[0] = False;\
                                                                            return a;\
                                                                        }\
                                                                        Int(8) int_index_set_13()    {\
                                                                            Int(8) a = 14;\
                                                                            a[0] = True;\
                                                                            return a;\
                                                                        }\
                                                                        @Int(8)[5][5][10] int_index_set_14(@Int(8)[5][5][10] a)    {\
                                                                            a[0][0][0][0] = True;\
                                                                            return a;\
                                                                        }\
                                                                        @Int(8) bs_arith_add()    {\
                                                                            @Int(8) a = 57;\
                                                                            @Int(8) b = 49;\
                                                                            return a + b;\
                                                                        }\
                                                                        @Int(8) bs_arith_sub()    {\
                                                                            @Int(8) a = 74;\
                                                                            @Int(8) b = 39;\
                                                                            return a - b;\
                                                                        }\
                                                                        void seq_bit_extraction(Bit[2][2] input){\
                                                                            Bit[2][2] a = [[True, False], [True, True]];\
                                                                            for(Int(8) outer = 0, Int(8)[2][2] f = [[1,2],[1,2]]; outer < 2; outer = outer + 1)    {\
                                                                                for(Int(8) inner = 0; inner < 2; inner = inner + 1)    {\
                                                                                    input[outer][inner] = a[outer][inner];\
                                                                                }\
                                                                            }\
                                                                        }\
                                                                        Bit[2][2] return_bits(Bit[2][2] input){\
                                                                            return input;\
                                                                        }\
                                                                        Int(8) seq_bit_arth(){\
                                                                            Int(8)[3] a = [10, 9];\
                                                                            Int(8)[2] b = [6, 7];\
                                                                            a[2][0,1,2,3,4] = a[0][0,1,2,3,4] + b[0][0,1,2,3,4];\
                                                                            return a[2];\
                                                                        }\
                                                                        void int_seq_decl(){\
                                                                            Int(8)[2][2][2] a = [[[0, 9],[0, 9]],[[0, 9],[0, 9]]];\
                                                                        }\
                                                                        void bs_seq_decl(){\
                                                                            @Int(8)[2][2] a = [[0, 9],[0, 9]];\
                                                                        }\
                                                                        void bs_seq_set(@Int(8)[2][2] a){\
                                                                            a = [[0, 9],[0, 9]];\
                                                                        }\
                                                                        void int_seq_set(Int(8)[2][2] a){\
                                                                             a = [[0, 9],[0, 9]];\
                                                                        }\
                                                                        @Int(8) bs_mult_sub()    {\
                                                                            @Int(32) a = 74;\
                                                                            @Int(32) b = 390;\
                                                                            return a * b;\
                                                                        }\
                                                                        void int_to_seq_bit_cast()    {\
                                                                            Int(8) b = 10;\
                                                                            Bit[5] a;\
                                                                            a = b + b;\
                                                                            }\
                                                                        @Int(8) bs_bit_expr_cast()  {\
                                                                            @Int(8) a;\
                                                                            a[0] = (True ^ False) ^ False;\
                                                                            return a;\
                                                                        }\
                                                                        void bit_to_bs_bit_set()  {\
                                                                            @Int(8) a;\
                                                                            Int(8) b;\
                                                                            a[1] = b[0] ^ (b[1] & b[3]);\
                                                                        }\
                                                                        @Int(8) bit_seq_expr_to_bs(){\
                                                                            @Int(8)[3] a;\
                                                                            a[0][1,2,3] = [False, False, True] ^ [True, True, False];\
                                                                            return a[0];\
                                                                        }\
                                                                        Int(8) bit_seq_expr_rotate(){\
                                                                            Int(8) a = ([True, True, True] ^ [False, False, True]) <<< 2;\
                                                                            return a;\
                                                                        }\
                                                                        Int(8) bit_seq_expr_arith(){\
                                                                            Int(8) a = ([True, True, True] * [False, False, True]) * 2;\
                                                                            return a;\
                                                                        }\
                                                                        Bit ret_bit(){\
                                                                            return True;\
                                                                        }\
                                                                        void get_bit() {\
                                                                            Bit a = ret_bit();\
                                                                        }\
                                                                        Int(8) ret_int(){\
                                                                            return 10;\
                                                                        }\
                                                                        void get_int() {\
                                                                            Int(8) a = ret_int();\
                                                                        }\
                                                                        Int(8) ret_int_in_seq(Int(8)[10][10] a){\
                                                                            return a[0][0];\
                                                                        }\
                                                                        void get_int_1() {\
                                                                            Int(8)[10][10] b;\
                                                                            Int(8) a = ret_int_in_seq(b);\
                                                                        }\
                                                                        @Int(8) bs_seq_bit_expr_mult() {\
                                                                            @Int(8) a = 1;\
                                                                            Int(8) b;\
                                                                            a[0,1,2] = (a[0,1,2] ^ b[0,1,2]) * 6;\
                                                                            return a;\
                                                                        }\
                                                                        @Int(8) bs_seq_bit_expr_mult_2() {\
                                                                            @Int(8) a = 2;\
                                                                            @Int(8) b = 2;\
                                                                            a[0,1,2,3] = ([True, False, True] ^ [False, False, True]) * b;\
                                                                            return a;\
                                                                        }\
                                                                    ")), True)
        if Data_reader.write_test("general_dsl", "general_dsl", par.semantic_analyser.IR.translate()) is True:
            assert_equals(subprocess.call(['test_output/general_dsl/./run_tests.sh']), 0)
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("")), True)

    def test_LFSR_translation(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("@Bit generate_bit(@Int(8) state) {\
                                                                            @Bit output, input;\
                                                                            output = state[7];\
                                                                            state = state << 1;\
                                                                            input =  (state[0] ^ state[4]) ^ (state[5] ^ state[6]);\
                                                                            state[0] = input;\
                                                                            return output;\
                                                                        }\
                                                                        @Int(32) lfsr(@Int(8) state){\
                                                                            @Int(32)  rndm_bits;\
                                                                            for(Int(8) r = 0; r < 32; r = r + 1) {\
                                                                                rndm_bits[r] = generate_bit(state);\
                                                                            }\
                                                                            return rndm_bits;\
                                                                        }\
                                                                        ")), True)
        assert_equals(Data_reader.write_test("lfsr_dsl", "lfsr_dsl", par.semantic_analyser.IR.translate()), True)
        assert_equals(subprocess.call(['test_output/lfsr_dsl/./run_tests.sh']), 0)

    def test_PRINCE_translation(self):
            par = Parser()
            assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Sbox(4)[16] prince = [0xb, 0xf, 0x3, 0x2, 0xa, 0xc, 0x9, 0x1, 0x6, 0x7, 0x8, 0x0, 0xe, 0x5, 0xd, 0x4];\
                                                                            Sbox(4)[16] prince_inv = [0xb, 0x7, 0x3, 0x2, 0xf, 0xd, 0x8, 0x9, 0xa, 0x6, 0x4, 0x0, 0x5, 0xe, 0xc, 0x1];\
                                                                            void enc(@Int(64)[12] RC, @Int(64) state, @Int(64) key_0, @Int(64) key_1) {\
                                                                                @Int(64) key_prime = (key_0 >>> 1) ^ (key_0 >> 63);\
                                                                                state = state ^ key_0;\
                                                                                state = ((state ^ RC[0]) ^ key_1);\
                                                                                first_rounds(state,key_1,RC);\
                                                                                sBox_layer(state);\
                                                                                mPrime(state);\
                                                                                sBox_layer_inv(state);\
                                                                                last_rounds(state,key_1,RC);\
                                                                                state = ((RC[11] ^ key_1) ^ state);\
                                                                                state = state ^ key_prime;\
                                                                            }\
                                                                            @Int(16) m0(@Int(16) state, @Int(16) output)   {\
                                                                                output[15] = state[11] ^ state[7] ^ state[3];\
                                                                                output[14] = state[14] ^ state[6] ^ state[2];\
                                                                                output[13] = state[13] ^ state[9] ^ state[1];\
                                                                                output[12] = state[12] ^ state[8] ^ state[4];\
                                                                                output[11] = state[15] ^ state[11] ^ state[7];\
                                                                                output[10] = state[10] ^ state[6] ^ state[2];\
                                                                                output[9] = state[13] ^ state[5] ^ state[1];\
                                                                                output[8] = state[12] ^ state[8] ^ state[0];\
                                                                                output[7] = state[15] ^ state[11] ^ state[3];\
                                                                                output[6] = state[14] ^ state[10] ^ state[6];\
                                                                                output[5] = state[9] ^ state[5] ^ state[1];\
                                                                                output[4] = state[12] ^ state[4] ^ state[0];\
                                                                                output[3] = state[15] ^ state[7] ^ state[3];\
                                                                                output[2] = state[14] ^ state[10] ^ state[2];\
                                                                                output[1] = state[13] ^ state[9] ^ state[5];\
                                                                                output[0] = state[8] ^ state[4] ^ state[0];\
                                                                                return output;\
                                                                            }\
                                                                            @Int(16) m1(@Int(16) state, @Int(16) output)   {\
                                                                                output[15] = state[15] ^ state[11] ^ state[7];\
                                                                                output[14] = state[10] ^ state[6] ^ state[2];\
                                                                                output[13] = state[13] ^ state[5] ^ state[1];\
                                                                                output[12] = state[12] ^ state[8] ^ state[0];\
                                                                                output[11] = state[15] ^ state[11] ^ state[3];\
                                                                                output[10] = state[14] ^ state[10] ^ state[6];\
                                                                                output[9] = state[9] ^ state[5] ^ state[1];\
                                                                                output[8] = state[12] ^ state[4] ^ state[0];\
                                                                                output[7] = state[15] ^ state[7] ^ state[3];\
                                                                                output[6] = state[14] ^ state[10] ^ state[2];\
                                                                                output[5] = state[13] ^ state[9] ^ state[5];\
                                                                                output[4] = state[8] ^ state[4] ^ state[0];\
                                                                                output[3] = state[11] ^ state[7] ^ state[3];\
                                                                                output[2] = state[14] ^ state[6] ^ state[2];\
                                                                                output[1] = state[13] ^ state[9] ^ state[1];\
                                                                                output[0] = state[12] ^ state[8] ^ state[4];\
                                                                                return output;\
                                                                            }\
                                                                            void mPrime(@Int(64) state)    {\
                                                                                @Int(16) output;\
                                                                                state[0:15] = m0(state[0:15], output);\
                                                                                state[16:31] = m1(state[16:31], output);\
                                                                                state[32:47] = m1(state[32:47], output);\
                                                                                state[48:63] = m0(state[48:63], output);\
                                                                            }\
                                                                            void sBox_layer(@Int(64) state)  {\
                                                                                for(Int(8) i = 0; i < 16; i = i + 1){\
                                                                                    state[(i * 4) : (i * 4) + 3] = prince[state[(i * 4) : (i * 4) + 3]];\
                                                                                }\
                                                                            }\
                                                                            void sBox_layer_inv(@Int(64) state)  {\
                                                                                for(Int(8) i = 0; i < 16; i = i + 1){\
                                                                                    state[(i * 4) : (i * 4) + 3] = prince_inv[state[(i * 4) : (i * 4) + 3]];\
                                                                                }\
                                                                            }\
                                                                            void shift_rows(@Int(64) state, Bit inverse){\
                                                                                Int(8) target;\
                                                                                @Int(64) output;\
                                                                                output[59 : 63] = state[59 : 63];\
                                                                                for(Int(8) nibble = 1; nibble < 16; nibble = nibble + 1){\
                                                                                    if(inverse == True){\
                                                                                        target = (target + 5) % 16;\
                                                                                    }\
                                                                                    if(inverse == False){\
                                                                                        target = (target + 13) % 16;\
                                                                                    }\
                                                                                    output[(63 - (target * 4)) - 3 : 63 - (target * 4)] = state[(63 - (nibble * 4)) - 3 : 63 - (nibble * 4)];\
                                                                                }\
                                                                                state = output;\
                                                                            }\
                                                                            void first_rounds(@Int(64) state, @Int(64) key, @Int(64)[11] RC){\
                                                                                for(Int(8) r = 1; r < 6; r = r + 1){\
                                                                                    sBox_layer(state);\
                                                                                    mPrime(state);\
                                                                                    shift_rows(state, False);\
                                                                                    state = ((RC[r] ^ key) ^ state);\
                                                                                }\
                                                                            }\
                                                                            void last_rounds(@Int(64) state, @Int(64) key, @Int(64)[11] RC){\
                                                                                for(Int(8) r = 6; r < 11; r = r + 1){\
                                                                                    state = ((RC[r] ^ key) ^ state);\
                                                                                    shift_rows(state, True);\
                                                                                    mPrime(state);\
                                                                                    sBox_layer_inv(state);\
                                                                                }\
                                                                            }\
                                                                            ")), True)
            Data_reader.write_test("prince_dsl", "prince_dsl", par.semantic_analyser.IR.translate())
            assert_equals(subprocess.call(['test_output/prince_dsl/./run_tests.sh']), 0)

    def test_PRESENT_translation(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Sbox(4)[16] present = [0xc, 0x5, 0x6, 0xB, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2];\
                                                                        void pLayer(@Int(64) state) {\
                                                                            Int(8) target_bit;\
                                                                            @Int(64) temp = state;\
                                                                            for(Int(8) bit = 0; bit < 64; bit = bit + 1)    {\
                                                                                target_bit = (16*bit) % 63;\
                                                                                if(bit == 63)   {\
                                                                                    target_bit = 63;\
                                                                                }\
                                                                                state[target_bit] = temp[bit];\
                                                                            }\
                                                                        }\
                                                                        void generate_round_keys(@Int(80) key, @Int(64)[32] round_keys) {\
                                                                                for(Int(8) round = 1; round < 33; round = round + 1)    {\
                                                                                        round_keys[round - 1][0: 63] = key[16:79];\
                                                                                        key = key <<< 61;\
                                                                                        key[76 : 79] = present[key[76:79]];\
                                                                                        key[15 : 19] = key[15 : 19] ^ round[0 : 5];\
                                                                                    }\
                                                                        }\
                                                                        void sBox_layer(@Int(64) state)  {\
                                                                            for(Int(8) i = 0; i < 16; i = i + 1){\
                                                                                state[(i * 4) : (i * 4) + 3] = present[state[(i * 4) : (i * 4) + 3]];\
                                                                            }\
                                                                        }\
                                                                        void enc(@Int(80) key, @Int(64) state, @Int(64)[32] round_keys){\
                                                                            generate_round_keys(key, round_keys);\
                                                                            for(Int(8) round = 0; round < 31; round = round + 1) {\
                                                                                state = state ^ round_keys[round];\
                                                                                sBox_layer(state);\
                                                                                pLayer(state);\
                                                                            }\
                                                                            state = state ^ round_keys[31];\
                                                                      }\
                                                                        ")), True)
        Data_reader.write_test("present_dsl", "present_dsl", par.semantic_analyser.IR.translate())
        assert_equals(subprocess.call(['test_output/present_dsl/./run_tests.sh']), 0)

    def test_LED_translation(self):
        par = Parser()
        assert_equals(par.analyse_tree_test(par.parse_test_AST_semantic("Sbox(4)[16] led = [0xc, 0x5, 0x6, 0xB, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2];\
                                                                        @Int(4) gmMult(@Int(4) a, @Int(4) b) {\
                                                                            @Int(4) output = 0, a_out = a, b_out = b, GF_R = 0x13, t, mask;\
                                                                            @Int(1) f;\
                                                                            @Int(1) high = 0;\
                                                                            Int(8) bit = 0;\
                                                                            for(Int(8) degree = 0; degree < 4; degree = degree + 1) {\
                                                                                f = 0;\
                                                                                t = b_out & 0x1;\
                                                                                for(bit = 0; bit < 4; bit = bit + 1)    {\
                                                                                    f[0] = f[0] | t[bit];\
                                                                                }\
                                                                                for(bit = 0; bit < 4; bit = bit + 1) {\
                                                                                    mask[bit] = f[0] & a_out[bit];\
                                                                                }\
                                                                                output = output ^ (mask & a_out);\
                                                                                high[0] = a_out[3];\
                                                                                a_out = a_out << 1;\
                                                                                for(bit = 0; bit < 4; bit = bit + 1){\
                                                                                    a_out[bit] = a_out[bit] ^ (high[0] & GF_R[bit]);\
                                                                                }\
                                                                                b_out = b_out >> 1;\
                                                                            }\
                                                                            return output;\
                                                                        }\
                                                                        void MixColumnSerial(@Int(64) state, @Int(4)[16] MDS) {\
                                                                            @Int(4)[4] column;\
                                                                            for(Int(8) col = 0; col < 4; col = col + 1)  {\
                                                                                column[0][0 : 3] = state[col * 4 : col * 4 + 3];\
                                                                                column[1][0 : 3] = state[((col + 4) * 4) : ((col + 4) * 4) + 3];\
                                                                                column[2][0 : 3] = state[((col + 8) * 4) : ((col + 8) * 4) + 3];\
                                                                                column[3][0 : 3] = state[((col + 12) * 4) : ((col + 12) * 4) + 3];\
                                                                                for(Int(8) col_nibble = 0; col_nibble < 4; col_nibble = col_nibble + 1) {\
                                                                                    state[(col * 4) + (col_nibble * 16) : ((col * 4) + (col_nibble * 16)) + 3] = gmMult(MDS[(col_nibble * 4)], column[0]) ^ gmMult(MDS[(col_nibble * 4) + 1], column[1]) ^ gmMult(MDS[(col_nibble * 4) + 2], column[2]) ^ gmMult(MDS[(col_nibble * 4) + 3], column[3]);\
                                                                                }\
                                                                            }\
                                                                        }\
                                                                        void shift_row(@Int(64) state)   {\
                                                                            state[16 : 31] = state[16 : 31] >>> 4;\
                                                                            state[32 : 47] = state[32 : 47] >>> 8;\
                                                                            state[48 : 63] = state[48 : 63] >>> 12;\
                                                                        }\
                                                                        void addConstants(@Int(64) state, @Int(6) constant)  {\
                                                                            @Int(64) roundConstant;\
                                                                            for(Int(8) row = 0; row < 4; row = row + 1)  {\
                                                                                roundConstant[row * 16 : (row * 16) + 3] = row[0:3];\
                                                                                if(row == 0 || row == 2)    {\
                                                                                    roundConstant[(row * 16) + 4 : (row * 16) + 6] = constant[3,4,5];\
                                                                                }\
                                                                                if(row == 1 || row == 3) {\
                                                                                    roundConstant[(row * 16) + 4 : (row * 16) + 6] = constant[0,1,2];\
                                                                                }\
                                                                                roundConstant[(row * 16) + 8 : (row * 16) + 15 ] = 0;\
                                                                            }\
                                                                                state = state ^ roundConstant;\
                                                                        }\
                                                                        void subCells(@Int(64) state)  {\
                                                                            for(Int(8) i = 0; i < 16; i = i + 1){\
                                                                                state[(i * 4) : (i * 4) + 3] = led[state[(i * 4) : (i * 4) + 3]];\
                                                                            }\
                                                                        }\
                                                                        void step(@Int(64) state, @Int(6) r, @Int(4)[16] MDS){\
                                                                            addConstants(state, r);\
                                                                            subCells(state);\
                                                                            shift_row(state);\
                                                                            MixColumnSerial(state, MDS);\
                                                                        }\
                                                                        void enc(@Int(64) state, @Int(64) key, @Int(4)[16] MDS, @Int(6)[32] RC){\
                                                                            for(Int(8) r = 0; r < 32; r = r + 1) {\
                                                                                if((r % 4) == 0){\
                                                                                    state = state ^ key;\
                                                                                }\
                                                                                step(state, RC[r], MDS);\
                                                                            }\
                                                                            state = state ^ key;\
                                                                        }\
                                                                        ")), True)
        Data_reader.write_test("led_dsl", "led_dsl", par.semantic_analyser.IR.translate())
        assert_equals(subprocess.call(['test_output/led_dsl/./run_tests.sh']), 0)



