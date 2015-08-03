int main()	{
	Int(64)[11] RC= [0x0000000000000000,
					0x13198a2e03707344,
					0xa4093822299f31d0, 
					0x082efa98ec4e6c89,
					0x452821e638d01377,
					0xbe5466cf34e90c6c,
					0x7ef84f78fd955cb1,
					0x85840851f1ac43aa,
					0xc882d32f25323c54,
					0x64a51195e0e3610d,
					0xd3b5a399ca0c2399,
					0xc0ac29b7c97c50dd];
	Int[16](4) sBox = (0xb, 0xf, 0x3, 0x2, 0xa, 0xc, 0x9, 0x1, 
         0x6, 0x7, 0x8, 0x0, 0xe, 0x5, 0xd, 0x4);
    Int[16](4) sBox_inv = (0xb, 0x7, 0x3, 0x2, 0xf, 0xd, 0x8, 0x9, 
            0xa, 0x6, 0x4, 0x0, 0x5, 0xe, 0xc, 0x1);
    Bit[ key_0 = (
	false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
	false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
	false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
	false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false);

    Bit[64] key_1 = (
	false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
	false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
	false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
	false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false);

	bit[64] key_prime = (key_0 >>> 1) ^ (key_0 >>63);

	Bit[64] state =(
	false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
	false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
	false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
	false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false);

	state = state ^ key_1;
	state = state ^ RC[0];
	for(Int round = 1; round < 6; round = round + 1)	{
		sBox(state,sBox);
	}

}

void sBox_layer(Bit[] state, Int[][] sbox)	{
	state = sbox.sbox(state);
}

void mPrime(Bit[] state)	{
	state[0:15] = m0(state[0:15]);
	state[16:31] = m0(state[16:31]);
	state[32:47] = m0(state[32:47]);
	state[48:63] = m0(state[48:63]);
}

Bit[16] m1(Bit[16] state)	{
	Bit[16] output;
    output[ 0] = state[0] ^ state[ 4] ^ state[ 8];
    output[ 1] = state[5] ^ state[ 9] ^ state[13];
    output[ 2] = state[2] ^ state[10] ^ state[14];
    output[ 3] = state[3] ^ state[ 7] ^ state[15];
    output[ 4] = state[0] ^ state[ 4] ^ state[12];
    output[ 5] = state[1] ^ state[ 5] ^ state[ 9];
    output[ 6] = state[6] ^ state[10] ^ state[14];
    output[ 7] = state[3] ^ state[11] ^ state[15];
    output[ 8] = state[0] ^ state[ 8] ^ state[12];
    output[ 9] = state[1] ^ state[ 5] ^ state[13];
    output[10] = state[2] ^ state[ 6] ^ state[10];
    output[11] = state[7] ^ state[11] ^ state[15];
    output[12] = state[4] ^ state[ 8] ^ state[12];
    output[13] = state[1] ^ state[ 9] ^ state[13];
    output[14] = state[2] ^ state[ 6] ^ state[14];
    output[15] = state[3] ^ state[ 7] ^ state[11];
    return output;
}

Bit[] m0(Bit[] state)	{
	Bit[16] output;
    output[ 0] = state[4] ^ state[ 8] ^ state[12]
    output[ 1] = state[1] ^ state[ 9] ^ state[13]
    output[ 2] = state[2] ^ state[ 6] ^ state[14]
    output[ 3] = state[3] ^ state[ 7] ^ state[11]
    output[ 4] = state[0] ^ state[ 4] ^ state[ 8]
    output[ 5] = state[5] ^ state[ 9] ^ state[13]
    output[ 6] = state[2] ^ state[10] ^ state[14]
    output[ 7] = state[3] ^ state[ 7] ^ state[15]
    output[ 8] = state[0] ^ state[ 4] ^ state[12]
    output[ 9] = state[1] ^ state[ 5] ^ state[ 9]
    output[10] = state[6] ^ state[10] ^ state[14]
    output[11] = state[3] ^ state[11] ^ state[15]
    output[12] = state[0] ^ state[ 8] ^ state[12]
    output[13] = state[1] ^ state[ 5] ^ state[13]
    output[14] = state[2] ^ state[ 6] ^ state[10]
    output[15] = state[7] ^ state[11] ^ state[15]
}
