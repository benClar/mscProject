Sbox(4)[16] led = [0xc, 0x5, 0x6, 0xB, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2];
@Int(4) gmMult(@Int(4) a, @Int(4) b) {
    @Int(4) output = 0, a_out = a, b_out = b, GF_R = 0x13, t, mask;
    @Int(1) f;
    @Int(1) high = 0;
    Int(8) bit = 0;
    for(Int(8) degree = 0; degree < 4; degree = degree + 1) {
        f = 0;
        t = b_out & 0x1;
        for(bit = 0; bit < 4; bit = bit + 1)    {
            f[0] = f[0] | t[bit];
        }
        for(bit = 0; bit < 4; bit = bit + 1) {
            mask[bit] = f[0] & a_out[bit];
        }
        output = output ^ (mask & a_out);
        high[0] = a_out[3];
        a_out = a_out << 1;
        for(bit = 0; bit < 4; bit = bit + 1){
            a_out[bit] = a_out[bit] ^ (high[0] & GF_R[bit]);
        }
        b_out = b_out >> 1;
    }
    return output;
}
void MixColumnSerial(@Int(64) state, @Int(4)[16] MDS) {
    @Int(4)[4] column;
    for(Int(8) col = 0; col < 4; col = col + 1)  {
        column[0][0 : 3] = state[col * 4 : col * 4 + 3];
        column[1][0 : 3] = state[((col + 4) * 4) : ((col + 4) * 4) + 3];
        column[2][0 : 3] = state[((col + 8) * 4) : ((col + 8) * 4) + 3];
        column[3][0 : 3] = state[((col + 12) * 4) : ((col + 12) * 4) + 3];
        for(Int(8) col_nibble = 0; col_nibble < 4; col_nibble = col_nibble + 1) {
            state[(col * 4) + (col_nibble * 16) : ((col * 4) + (col_nibble * 16)) + 3] = gmMult(MDS[(col_nibble * 4)], column[0]) ^ gmMult(MDS[(col_nibble * 4) + 1], column[1]) ^ gmMult(MDS[(col_nibble * 4) + 2], column[2]) ^ gmMult(MDS[(col_nibble * 4) + 3], column[3]);
        }
    }
}
void shift_row(@Int(64) state)   {
    state[16 : 31] = state[16 : 31] >>> 4;
    state[32 : 47] = state[32 : 47] >>> 8;
    state[48 : 63] = state[48 : 63] >>> 12;
}
void addConstants(@Int(64) state, @Int(6) constant)  {
    @Int(64) roundConstant;
    for(Int(8) row = 0; row < 4; row = row + 1)  {
        roundConstant[row * 16 : (row * 16) + 3] = row[0:3];
        if(row == 0 || row == 2)    {
            roundConstant[(row * 16) + 4 : (row * 16) + 6] = constant[3,4,5];
        }
        if(row == 1 || row == 3) {
            roundConstant[(row * 16) + 4 : (row * 16) + 6] = constant[0,1,2];
        }
        roundConstant[(row * 16) + 8 : (row * 16) + 15 ] = 0;
    }
        state = state ^ roundConstant;
}
void subCells(@Int(64) state)  {
    for(Int(8) i = 0; i < 16; i = i + 1){
        state[(i * 4) : (i * 4) + 3] = led[state[(i * 4) : (i * 4) + 3]];
    }
}
void step(@Int(64) state, @Int(6) r, @Int(4)[16] MDS){
    addConstants(state, r);
    subCells(state);
    shift_row(state);
    MixColumnSerial(state, MDS);
}
void enc(@Int(64) state, @Int(64) key, @Int(4)[16] MDS, @Int(6)[32] RC){
    for(Int(8) r = 0; r < 32; r = r + 1) {
        if((r % 4) == 0){
            state = state ^ key;
        }
        step(state, RC[r], MDS);
    }
    state = state ^ key;
}