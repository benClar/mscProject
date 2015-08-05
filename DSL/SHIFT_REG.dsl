void main()	{
	
}

void lfsr(@Int(8) state)
	Int(1) output;
	Int(1) input;
	for(int(5) i = 0; i < 32; i = i + 1) {
		output = state[0]
		input =  state[0] ^ ((Bit[8]) state)[4] ^ ((Bit[8]) state)[5] ^ ((Bit[8]) state)[6]
		state = state << 1
		((Bit[8]) state)[7] = input 
	}
}