main()	{
	Sequence key = (false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
					false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
					false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
					false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,true);

	Sequence state = (false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
						false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
						false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
						false,false,false,false);

    Sequence sBox = (0xC,0x5,0x6,0xB,0x9,0x0,0xA,0xD,0x3,0xE,0xF,0x8,0x4,0x7,0x1,0x2);

	Sequence round_keys = generate_round_keys(key, sBox);

	for(int round = 0; round < 31; round = round + 1)	{
		state ^ round_keys[round];
		sBox_layer(state);
		pLayer(state);
	}

	state ^ round_keys[round];
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

sBox_layer(Sequence state, Sequence sBox)	{
	state = sBox.sBox(state);
}

generate_round_keys(Sequence key, Sequence sBox)	{

	for(int round = 0; round < 32; round = round + 1)	{
		Sequence round_keys.add(Sequence(key[0:64]));
		key = key <<< 61;
		key[0:3] = sBox.sBox(key[0:3]);
		key[-19 : -15] ^= round;
	}

	return round_keys;
}