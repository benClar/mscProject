void error_1()	{
	@Int(8)[32] a;
	@Int(8) b;
	a[0][0] = b;
}

Int(64) error_2_return()	{
	Int(64) a;
	return a;
}

void error_3()	{
	Bit a = error_2_return();
}