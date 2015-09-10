Int(8) int_index_set_1()    {
    Int(8) a = 10;
    a[3] = a[1];
    return a;
}
Int(8) int_index_set_2()    {
    Int(8) a = 0;
    a[0,1,3] = [True, False, True];
    return a;
}
Int(8) int_index_set_3()    {
    Int(8) a = 5;
    a[0,1,2,3] = a[0,1,2,3] << 1;
    return a;
}
Int(8) int_index_set_4()    {
    Int(8) a = 5;
    a[0,1,2,3] = a[0,1,2,3] <<< 3;
    return a;
}
Int(8) int_index_set_5()    {
    Int(8) a = 19;
    a[0,1,2,3,4] = a[0,1,2,3,4] >>> 3;
    return a;
}
Int(8) int_index_set_6()    {
    Int(8) a = 19;
    a[0,1,2,3,4] = a[0:4] >>> 3;
    return a;
}
Int(8) int_index_set_7()    {
    Int(8) a = 0;
    a[0:4] = [True, False, True, True];
    return a;
}
Int(8) int_index_set_8()    {
    Int(8) a = 0;
    a = [True, False, True, True];
    return a;
}
Int(8) int_index_set_9()    {
    Int(8) a = 0;
    a = [True, False, True, True] + 10;
    return a;
}
Int(8) int_index_set_10()    {
    Int(8) a = 0;
    a = ([True, False, True, True] <<< 1) + 10;
    return a;
}
Int(8) int_index_set_11()    {
    Int(8) a = 7;
    a[0,1,2,3] = a[3,2,1,0];
    return a;
}
Int(8) int_index_set_12()    {
    Int(8) a = 15;
    a[0] = False;
    return a;
}
Int(8) int_index_set_13()    {
    Int(8) a = 14;
    a[0] = True;
    return a;
}
@Int(8)[5][5][10] int_index_set_14(@Int(8)[5][5][10] a)    {
    a[0][0][0][0] = True;
    return a;
}
@Int(8) bs_arith_add()    {
    @Int(8) a = 57;
    @Int(8) b = 49;
    return a + b;
}
@Int(8) bs_arith_sub()    {
    @Int(8) a = 74;
    @Int(8) b = 39;
    return a - b;
}
void seq_bit_extraction(Bit[2][2] input){
    Bit[2][2] a = [[True, False], [True, True]];
    for(Int(8) outer = 0; outer < 2; outer = outer + 1)    {
        for(Int(8) inner = 0; inner < 2; inner = inner + 1)    {
            input[outer][inner] = a[outer][inner];
        }
    }
}
Bit[2][2] return_bits(Bit[2][2] input){
    return input;
}
Int(8) seq_bit_arth(){
    Int(8)[3] a = [10, 9];
    Int(8)[2] b = [6, 7];
    a[2][0,1,2,3,4] = a[0][0,1,2,3,4] + b[0][0,1,2,3,4];
    return a[2];
}
void int_seq_decl(){
    Int(8)[2][2][2] a = [[[0, 9],[0, 9]],[[0, 9],[0, 9]]];
}
void bs_seq_decl(){
    @Int(8)[2][2] a = [[0, 9],[0, 9]];
}
void bs_seq_set(@Int(8)[2][2] a){
    a = [[0, 9],[0, 9]];
}
void int_seq_set(Int(8)[2][2] a){
     a = [[0, 9],[0, 9]];
}
@Int(8) bs_mult_sub()    {
    @Int(32) a = 74;
    @Int(32) b = 390;
    return a * b;
}
void int_to_seq_bit_cast()    {
    Int(8) b = 10;
    Bit[5] a;
    a = b + b;
    }
@Int(8) bs_bit_expr_cast()  {
@Int(8) a;
a[0] = (True ^ False) ^ False;
return a;
}
void bit_to_bs_bit_set()  {
    @Int(8) a;
    Int(8) b;
    a[1] = b[0] ^ (b[1] & b[3]);
}
@Int(8) bit_seq_expr_to_bs(){
    @Int(8)[3] a;
    a[0][1,2,3] = [False, False, True] ^ [True, True, False];
    return a[0];
}
Int(8) bit_seq_expr_rotate(){
    Int(8) a = ([True, True, True] ^ [False, False, True]) <<< 2;
    return a;
}
Int(8) bit_seq_expr_arith(){
    Int(8) a = ([True, True, True] * [False, False, True]) * 2;
    return a;
}
