#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "lfsr.h"

uint32_t generate_bit(uint32_t state[8])	{
	uint32_t output;
	uint32_t input;
	uint32_t expected_state[8] = {0};
	output = state[0];
	shift_left(expected_state,state,1,8);
	state[0] = expected_state[0];
	state[1] = expected_state[1];
	state[2] = expected_state[2];
	state[3] = expected_state[3];
	state[4] = expected_state[4];
	state[5] = expected_state[5];
	state[6] = expected_state[6];
	state[7] = expected_state[7];
	input = state[7] ^ state[3] ^ state[2] ^ state[1];
	state[7] = input;
	return output;
}

void lfsr(uint32_t output[32], uint32_t state[8])	{
	int bit;
	for(bit = 0; bit < 32; bit++)	{
		output[bit] = generate_bit(state);
	}
}
