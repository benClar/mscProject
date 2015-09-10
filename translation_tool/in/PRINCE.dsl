Sbox(4)[16] prince = [0xb, 0xf, 0x3, 0x2, 0xa, 0xc, 0x9, 0x1, 0x6, 0x7, 0x8, 0x0, 0xe, 0x5, 0xd, 0x4];
Sbox(4)[16] prince_inv = [0xb, 0x7, 0x3, 0x2, 0xf, 0xd, 0x8, 0x9, 0xa, 0x6, 0x4, 0x0, 0x5, 0xe, 0xc, 0x1];
void enc(@Int(64)[12] RC, @Int(64) state, @Int(64) key_0, @Int(64) key_1) {
    @Int(64) key_prime = (key_0 >>> 1) ^ (key_0 >> 63);
    state = state ^ key_0;
    state = ((state ^ RC[0]) ^ key_1);
    first_rounds(state,key_1,RC);
    sBox_layer(state);
    mPrime(state);
    sBox_layer_inv(state);
    last_rounds(state,key_1,RC);
    state = ((RC[11] ^ key_1) ^ state);
    state = state ^ key_prime;
}
@Int(16) m0(@Int(16) state, @Int(16) output)   {
    output[15] = state[11] ^ state[7] ^ state[3];
    output[14] = state[14] ^ state[6] ^ state[2];
    output[13] = state[13] ^ state[9] ^ state[1];
    output[12] = state[12] ^ state[8] ^ state[4];
    output[11] = state[15] ^ state[11] ^ state[7];
    output[10] = state[10] ^ state[6] ^ state[2];
    output[9] = state[13] ^ state[5] ^ state[1];
    output[8] = state[12] ^ state[8] ^ state[0];
    output[7] = state[15] ^ state[11] ^ state[3];
    output[6] = state[14] ^ state[10] ^ state[6];
    output[5] = state[9] ^ state[5] ^ state[1];
    output[4] = state[12] ^ state[4] ^ state[0];
    output[3] = state[15] ^ state[7] ^ state[3];
    output[2] = state[14] ^ state[10] ^ state[2];
    output[1] = state[13] ^ state[9] ^ state[5];
    output[0] = state[8] ^ state[4] ^ state[0];
    return output;
}
@Int(16) m1(@Int(16) state, @Int(16) output)   {
    output[15] = state[15] ^ state[11] ^ state[7];
    output[14] = state[10] ^ state[6] ^ state[2];
    output[13] = state[13] ^ state[5] ^ state[1];
    output[12] = state[12] ^ state[8] ^ state[0];
    output[11] = state[15] ^ state[11] ^ state[3];
    output[10] = state[14] ^ state[10] ^ state[6];
    output[9] = state[9] ^ state[5] ^ state[1];
    output[8] = state[12] ^ state[4] ^ state[0];
    output[7] = state[15] ^ state[7] ^ state[3];
    output[6] = state[14] ^ state[10] ^ state[2];
    output[5] = state[13] ^ state[9] ^ state[5];
    output[4] = state[8] ^ state[4] ^ state[0];
    output[3] = state[11] ^ state[7] ^ state[3];
    output[2] = state[14] ^ state[6] ^ state[2];
    output[1] = state[13] ^ state[9] ^ state[1];
    output[0] = state[12] ^ state[8] ^ state[4];
    return output;
}
void mPrime(@Int(64) state)    {
    @Int(16) output;
    state[0:15] = m0(state[0:15], output);
    state[16:31] = m1(state[16:31], output);
    state[32:47] = m1(state[32:47], output);
    state[48:63] = m0(state[48:63], output);
}
void sBox_layer(@Int(64) state)  {
    for(Int(8) i = 0; i < 16; i = i + 1){
        state[(i * 4) : (i * 4) + 3] = prince[state[(i * 4) : (i * 4) + 3]];
    }
}
void sBox_layer_inv(@Int(64) state)  {
    for(Int(8) i = 0; i < 16; i = i + 1){
        state[(i * 4) : (i * 4) + 3] = prince_inv[state[(i * 4) : (i * 4) + 3]];
    }
}
void shift_rows(@Int(64) state, Bit inverse){
    Int(8) target;
    @Int(64) output;
    output[59 : 63] = state[59 : 63];
    for(Int(8) nibble = 1; nibble < 16; nibble = nibble + 1){
        if(inverse == True){
            target = (target + 5) % 16;
        }
        if(inverse == False){
            target = (target + 13) % 16;
        }
        output[(63 - (target * 4)) - 3 : 63 - (target * 4)] = state[(63 - (nibble * 4)) - 3 : 63 - (nibble * 4)];
    }
    state = output;
}
void first_rounds(@Int(64) state, @Int(64) key, @Int(64)[11] RC){
    for(Int(8) r = 1; r < 6; r = r + 1){
        sBox_layer(state);
        mPrime(state);
        shift_rows(state, False);
        state = ((RC[r] ^ key) ^ state);
    }
}
void last_rounds(@Int(64) state, @Int(64) key, @Int(64)[11] RC){
    for(Int(8) r = 6; r < 11; r = r + 1){
        state = ((RC[r] ^ key) ^ state);
        shift_rows(state, True);
        mPrime(state);
        sBox_layer_inv(state);
    }
}
