main()	{

	Sequence key = Sequence(0);
	Sequence state = Sequence(0);
	Sequence key = (false,false,false,false,false);
	Sequence state = Sequence(0);
}

sub_cells(Sequence state, Sequence sBox)	{
	state = sBox.sBox(state);
}

shift_row(Sequence state)	{
	for(int i = 0, int first = 0; int last = 15; i < 4; i = i + 1)	{
		state[first : last] <<< i;
		first = first + 16;
		last = last + 16;
	}
}

