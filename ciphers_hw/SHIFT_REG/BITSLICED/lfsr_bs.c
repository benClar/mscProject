#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include "../../LIB/dsl_lib.h"

uint8_t* bitslice_block(uint8_t *input, int width, int input_count);
void lfsr(uint8_t input[8]);

int main()	{
	uint8_t state[8]; 
	uint8_t output[8];
	lfsr(state);
}	

void lfsr(uint8_t state[8])	{
	uint8_t output_bit;
	uint8_t input_bit;
	int rnd;
	for(rnd = 0; rnd < 32; rnd++)	{
		output_bit = state[0];
		input_bit = state[0] ^ state[4] ^ state[5] ^ state[6];
		state = shift_left(state,8,1);
		state[7] = input_bit;
	}	
}

uint8_t* bitslice_block(uint8_t *input, int width, int input_count)	{
	int bit, curr;
	uint8_t *output = malloc(width * sizeof(uint8_t));
	for(bit = width; bit > 0; bit--)	{
		for(curr = 0; curr < input_count; curr++)	{
			output[width - bit] <<= 1;
			output[width - bit] |= ((input[curr] >> (bit - 1)) & 0x1);	
		}
	}
	return output;
}