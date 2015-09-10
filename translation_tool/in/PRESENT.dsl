Sbox(4)[16] present = [0xc, 0x5, 0x6, 0xB, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2];
void pLayer(@Int(64) state) {
    Int(8) target_bit;
    @Int(64) temp = state;
    for(Int(8) bit = 0; bit < 64; bit = bit + 1)    {
        target_bit = (16*bit) % 63;
        if(bit == 63)   {
            target_bit = 63;
        }
        state[target_bit] = temp[bit];
    }
}
void generate_round_keys(@Int(80) key, @Int(64)[32] round_keys) {
        for(Int(8) round = 1; round < 33; round = round + 1)    {
                round_keys[round - 1][0: 63] = key[16:79];
                key = key <<< 61;
                key[76 : 79] = present[key[76:79]];
                key[15 : 19] = key[15 : 19] ^ round[0 : 5];
            }
}
void sBox_layer(@Int(64) state)  {
    for(Int(8) i = 0; i < 16; i = i + 1){
        state[(i * 4) : (i * 4) + 3] = present[state[(i * 4) : (i * 4) + 3]];
    }
}
void enc(@Int(80) key, @Int(64) state, @Int(64)[32] round_keys){
    generate_round_keys(key, round_keys);
    for(Int(8) round = 0; round < 31; round = round + 1) {
        state = state ^ round_keys[round];
        sBox_layer(state);
        pLayer(state);
    }
    state = state ^ round_keys[31];
}