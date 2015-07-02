main()	{

	@Int(64)[5] state = (0,1,2,3,4)
	@Int(80)[5] key = (0,0,0,0,0)

    

	Int(64)[32] round_keys = generate_round_keys(key, sBox);
	enc(state, round_keys)


	state ^ round_keys[round];
}

enc(@Int(64) state, @Int[32](64) round_keys)	{
	Int(4)[16] sBox = (0xC,0x5,0x6,0xB,0x9,0x0,0xA,0xD,0x3,0xE,0xF,0x8,0x4,0x7,0x1,0x2);

	for(Int(5) round = 0; round < 31; round = round + 1)	{
		state ^ round_keys[round];
		sBox_layer(state);
		pLayer(state);
	}	
}

pLayer(Sequence state)	{
	int target_bit;
	Sequence temp = Sequence(state);
	for(int bit = 0; bit < 64; bit++)	{
		target_bit = (16*bit) % 63;
		if(bit == 63)	{
			target_bit = 63;
		}
		state[target_bit] = temp[bit];
	}
}

sBox_layer(Bit[] state, Bit[] sBox)	{
	state = sBox.sBox(state);
}

generate_round_keys(@Int(80) key, Int(4)[16] sBox)	{
	@Int(64)[32] round_keys;
	for(Int(5) round = 0; round < 32; round = round + 1)	{
		round_keys[round] = (Bit[80]) key[79:16];
		key = key <<< 61;
		((Bit[80]) key)[79:76] = sBox.sBox((Bit[80]) key[0:3]);
		((Bit[80]) key)[19 : 15] ^= (Bit[5]) round;
	}
	return round_keys;
}