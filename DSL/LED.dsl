void main()	{

	Sbox(4)[16] s = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2];

	Int(4)[16] MDS = [0x4,0x1,0x2,0x2,0x8,0x6,0x5,0x6,0xB,0xE,0xA,0x9,0x2,0x2,0xF,0xB];
}

void enc(@Int(4)[16] state, @Int(4)[16] key) {

}

void sub_cells(@Int(4)[16] state, sbox s)	{
	state = s[state];
}

void shift_row(@Int(4)[16] state)	{
		state[0 : 3] <<< 0;
		state[4 : 7] <<< 1;
		state[8 : 11] <<< 2
		state[12 : 15] <<< 3;
}

void addConstants(Bit[] state, Int constant)	{
	Bit[16][4] roundConstant;
	for(nibble = 0; nibble < 16; nibble = nibble + 4)	{
		roundConstant[nibble][0:3] = (Bit[4]) row;
		if(row == 0 || row == 2)	{
			roundConstant[nibble][0:3] = (Bit([4]) constant[5:3];
		} else {
			roundConstant[nibble][0:3] = (Bit([4]) constant[2:0];
		}
		roundConstant[nibble][0:3] = (Bit[4]) 0; //!Setting values accross 2d elements
		roundConstant[nibble + 1][0:3] = (Bit[4]) 0;
		state[nibble] = state[nibble] ^ roundConstant[nibble]; //! Notice that this 2d structure can XOR its elements.
	}
	
}

void MixColumnSerial(Bit[][] state, Int[] MDS)	{
	Bit[16] column;

	for(int c = 0; c < 4; c++)	{	
		column = state[c,c + 4,c + 8,c + 12]; //! Accessing 2d elements: return in single sequence
		for(int r = 0; r < 4; r++)	{
			state[(4*c) + r] = gmMult(MDS[4 * c],(Int) column[0:3]) ^ 
											gmMult(MDS[(4 * c) + 1],(Int) column[4:7]) ^ 
											gmMult(MDS[(4 * c) + 2],(Int) column[8:11]) ^ 
											gmMult(MDS[(4 * c) + 3)],(Int) column[12:15]);
		}
	}
}

Bit[] gmMult(Int a, Int b)	{
	Int(8) g = 0;
	for(Int i = 0; i < 4 i++)	{
		if(b{0} == 1)	{
			g = g ^ a;
		}
		a = a << 1;
		if(a{3} == 1)	{
			a = a ^ GF_POLY;
		}
		b = b>>1;
	}
	return (Bit) g;
}



