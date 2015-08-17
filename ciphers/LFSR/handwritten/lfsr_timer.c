#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "lfsr_timer.h"

int main()	{
	program_time();
	generate_bit_time();
}

void program_time()	{
	uint32_t state[8] = {0,0xffffffff,0,0xffffffff,0,0xffffffff,0,0xffffffff};
	uint32_t output[32] = {0};
	
	clock_t start, end, result = 0;

	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		lfsr(output,state);
		end = mach_absolute_time();
		result += (end - start);
		state[0] = 0;
		state[1] = 0xffffffff;
		state[2] = 0;
		state[3] = 0xffffffff;
		state[4] = 0;
		state[5] = 0xffffffff;
		state[6] = 0;
		state[7] = 0xffffffff;
		for(int bit = 0; bit < 32; bit++)	{
			output[bit] = 0;
		}
	}
	printf("lfsr: %lu\n", result / 100000);
}

void generate_bit_time()	{
	uint32_t state[8] = {0,0xffffffff,0,0xffffffff,0,0xffffffff,0,0xffffffff};
	uint32_t output[1] = {0};
	
	clock_t start, end, result = 0;

	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		generate_bit(state);
		end = mach_absolute_time();
		result += (end - start);
		state[0] = 0;
		state[1] = 0xffffffff;
		state[2] = 0;
		state[3] = 0xffffffff;
		state[4] = 0;
		state[5] = 0xffffffff;
		state[6] = 0;
		state[7] = 0xffffffff;
		output[0] = 0;
	}

	printf("generate bit: %lu\n", result / 100000);
}

