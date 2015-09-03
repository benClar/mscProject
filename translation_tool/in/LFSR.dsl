@Bit generate_bit(@Int(8) state) {
    @Bit output, input;
    output = state[7];
    state = state << 1;
    input =  (state[0] ^ state[4]) ^ (state[5] ^ state[6]);
    state[0] = input;
    return output;
}
@Int(32) lfsr(@Int(8) state){
    @Int(32)  rndm_bits;
    for(Int(8) r = 0; r < 32; r = r + 1) {
        rndm_bits[r] = generate_bit(state);
    }
    return rndm_bits;
}