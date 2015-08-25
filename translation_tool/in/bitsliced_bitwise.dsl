void bitslice_bitwise()	{
	@Int(64) a, b;
	a = a ^ b;
}

@Int(64) bitslice_rotate()	{
	@Int(64) a = 0xa;
	a[0 : 4] = a[0 : 4] <<< 1;
	return a;
}