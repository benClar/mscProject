from ast import *

def run():
    m = Module(body=[Expr(value=BinOp(left=Num(n=1), op=BitXor(), right=Num(n=1)))])
    # Module(body=[Expr(value = BinOp(left=Expr(value=Num(n=1)), op=BitOr(), right=Expr(value=Num(n=1))))])
    walk(m)

if __name__ == "__main__":
    run()