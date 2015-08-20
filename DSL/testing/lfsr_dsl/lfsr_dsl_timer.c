#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "lfsr_dsl_timer.h"

int main()	{
	// cipher_constant_time();
	// program_time();
	generate_bit_time();
}

void cipher_constant_time()	{
	uint32_t state[8] = {0,0xffffffff,0,0xffffffff,0,0xffffffff,0,0xffffffff};
	uint32_t output[32][1] = {{0}};
	clock_t start, end, curr_time = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);
	for(int run = 0; run < 1000; run++)	{
		start = mach_absolute_time();
		lfsr(output,state);
		end = mach_absolute_time();
		curr_time = (end - start);
		state[0] = 0;
		state[1] = 0xffffffff;
		state[2] = 0;
		state[3] = 0xffffffff;
		state[4] = 0;
		state[5] = 0xffffffff;
		state[6] = 0;
		state[7] = 0xffffffff;
		for(int bit = 0; bit < 32; bit++)	{
			output[bit][0] = 0;
		}
	}

	for(int run = 0; run < 1000; run++)	{
		start = mach_absolute_time();
		lfsr(output,state);
		end = mach_absolute_time();
		curr_time = (end - start);
		state[0] = 0;
		state[1] = 0xffffffff;
		state[2] = 0;
		state[3] = 0xffffffff;
		state[4] = 0;
		state[5] = 0xffffffff;
		state[6] = 0;
		state[7] = 0xffffffff;
		for(int bit = 0; bit < 32; bit++)	{
			output[bit][0] = 0;
		}
		printf("%d %lu a\n",run + 1, (curr_time * info.numer) / info.denom);
	}
}

void program_time()	{
	uint32_t state[8] = {0,0xffffffff,0,0xffffffff,0,0xffffffff,0,0xffffffff};
	uint32_t output[32][1] = {{0}};
	clock_t start, end, result = 0, high = 0, low = 0xffffffffffffffff, curr_time = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);
	for(int run = 0; run < 1000; run++)	{
	}

	for(int run = 0; run < 1000; run++)	{
		start = mach_absolute_time();
		lfsr(output,state);
		end = mach_absolute_time();
		curr_time = (end - start);
		result += curr_time;
		state[0] = 0;
		state[1] = 0xffffffff;
		state[2] = 0;
		state[3] = 0xffffffff;
		state[4] = 0;
		state[5] = 0xffffffff;
		state[6] = 0;
		state[7] = 0xffffffff;
		for(int bit = 0; bit < 32; bit++)	{
			output[bit][0] = 0;
		}
		if (curr_time > 5000)	{
			high = curr_time;
		}
		if (curr_time < low)	{
			low = curr_time;
		}
	}
	printf("lfsr time: %lu\n", (result / 100000) * info.numer / info.denom);
	printf("lfsr high: %lu\n", (high * info.numer) / info.denom);
	printf("lfsr low: %lu\n", (low * info.numer) / info.denom);
}

void generate_bit_time()	{
	uint32_t state[8] = {0,0xffffffff,0,0xffffffff,0,0xffffffff,0,0xffffffff};
	uint32_t output[1] = {0};
	clock_t start, end, result = 0, high = 0, low = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);

	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();;
		generate_bit(output, state);
		end = mach_absolute_time();;
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
		if (result > high)	{
			high = result;
		}
		if (result < low)	{
			low = result;
		}
	}
	printf("generate time: %lu\n", (result / 100000) * info.numer / info.denom);
	// printf("generate high: %lu\n", (high / 100000) * info.numer / info.denom);
	// printf("generate low: %lu\n", (low / 100000) * info.numer / info.denom);
}

