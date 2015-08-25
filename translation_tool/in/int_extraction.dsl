Int(8) int_XOR_1()    {
    Int(8) a = 0xa, b = 0xd, c;
    c[0] = a[1] ^ b[1];
    return c;
}

Int(8) int_index_set_1()    {
    Int(8) a = 0;
    a[0,1,3] = [True, True, True];
    return a;
}
