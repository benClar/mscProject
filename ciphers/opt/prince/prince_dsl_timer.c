#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "prince_dsl_timer.h"

int main() {
	cipher_constant_time();
	cipher_time();
	mPrime_time();
	sBox_layer_time();
	shift_rows_time();
	lastRounds_time();
	firstRounds_time();
}

void cipher_constant_time()	{
	// 1000 runs to investigate individual run times
	uint32_t state[64] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	uint32_t key_0[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key_1[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t RC[12][64];
	int bit;
	bitslice(RC[0],0x0000000000000000, 64);
	bitslice(RC[1],0x13198a2e03707344, 64);
	bitslice(RC[2],0xa4093822299f31d0, 64);
	bitslice(RC[3],0x082efa98ec4e6c89, 64);
	bitslice(RC[4],0x452821e638d01377, 64);
	bitslice(RC[5],0xbe5466cf34e90c6c, 64);
	bitslice(RC[6],0x7ef84f78fd955cb1, 64);
	bitslice(RC[7],0x85840851f1ac43aa, 64);
	bitslice(RC[8],0xc882d32f25323c54, 64);
	bitslice(RC[9],0x64a51195e0e3610d, 64);
	bitslice(RC[10],0xd3b5a399ca0c2399, 64);
	bitslice(RC[11],0xc0ac29b7c97c50dd, 64);
	clock_t start, end, curr_time = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);
	for(int run = 0; run < 1000; run++)	{
		start = mach_absolute_time();
		enc(RC, state, key_0, key_1);
		end = mach_absolute_time();
		curr_time = (end - start);
		for(bit = 0; bit < 64; bit++)	{
			state[bit] = 0xffffffff;
			key_0[bit] = 0;
			key_1[bit] = 0;
		}
	}

	for(int run = 0; run < 1000; run++)	{
		start = mach_absolute_time();
		enc(RC, state, key_0, key_1);
		end = mach_absolute_time();
		curr_time = (end - start);
		for(bit = 0; bit < 64; bit++)	{
			state[bit] = 0xffffffff;
			key_0[bit] = 0;
			key_1[bit] = 0;
		}
		printf("%d %lu a\n",run + 1, (curr_time * info.numer) / info.denom);
	}


}

void cipher_time()	{
	// runs of 100000 to get interquartile range, median and mean
	uint32_t state[64] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	uint32_t key_0[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key_1[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t RC[12][64];
	int bit;
	bitslice(RC[0],0x0000000000000000, 64);
	bitslice(RC[1],0x13198a2e03707344, 64);
	bitslice(RC[2],0xa4093822299f31d0, 64);
	bitslice(RC[3],0x082efa98ec4e6c89, 64);
	bitslice(RC[4],0x452821e638d01377, 64);
	bitslice(RC[5],0xbe5466cf34e90c6c, 64);
	bitslice(RC[6],0x7ef84f78fd955cb1, 64);
	bitslice(RC[7],0x85840851f1ac43aa, 64);
	bitslice(RC[8],0xc882d32f25323c54, 64);
	bitslice(RC[9],0x64a51195e0e3610d, 64);
	bitslice(RC[10],0xd3b5a399ca0c2399, 64);
	bitslice(RC[11],0xc0ac29b7c97c50dd, 64);
	clock_t start, end;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);
	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		enc(RC, state, key_0, key_1);
		end = mach_absolute_time();
		printf("%lu\n",(end - start));
		for(bit = 0; bit < 64; bit++)	{
			state[bit] = 0xffffffff;
			key_0[bit] = 0;
			key_1[bit] = 0;
		}
	}

}

void shift_rows_time()	{
	// runs of 100000 to get mean for shift_rows_time function
	uint32_t state[64] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	int bit;
	clock_t start, end, result = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);
	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		shift_rows(state, 1);
		end = mach_absolute_time();
		result += (end - start);
		for(bit = 0; bit < 64; bit++)	{
			state[bit] = 0xffffffff;
		}
	}
	printf("shift_rows time: %lu\n", (result / 100000) * info.numer / info.denom);
}

void sBox_layer_time()	{
	// runs of 100000 to get mean for sbox time function
	uint32_t state[64] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	int bit;
	clock_t start, end, result = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);
	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		sBox_layer(state);
		end = mach_absolute_time();
		result += (end - start);
		for(bit = 0; bit < 64; bit++)	{
			state[bit] = 0xffffffff;
		}
	}	
	printf("sBox_layer time: %lu\n", (result / 100000) * info.numer / info.denom);
}

void mPrime_time()	{
	// runs of 100000 to get mean mprime function
	uint32_t state[64] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	int bit;
	clock_t start, end, result = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);
	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		mPrime(state);
		end = mach_absolute_time();
		result += (end - start);
		for(bit = 0; bit < 64; bit++)	{
			state[bit] = 0xffffffff;
		}
	}
	printf("mPrime time: %lu\n", (result / 100000) * info.numer / info.denom);
}

void firstRounds_time()	{
	// runs of 100000 to get mean for first rounds function
	uint32_t state[64] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	uint32_t key_0[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key_1[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t RC[12][64];
	int bit;
	bitslice(RC[0],0x0000000000000000, 64);
	bitslice(RC[1],0x13198a2e03707344, 64);
	bitslice(RC[2],0xa4093822299f31d0, 64);
	bitslice(RC[3],0x082efa98ec4e6c89, 64);
	bitslice(RC[4],0x452821e638d01377, 64);
	bitslice(RC[5],0xbe5466cf34e90c6c, 64);
	bitslice(RC[6],0x7ef84f78fd955cb1, 64);
	bitslice(RC[7],0x85840851f1ac43aa, 64);
	bitslice(RC[8],0xc882d32f25323c54, 64);
	bitslice(RC[9],0x64a51195e0e3610d, 64);
	bitslice(RC[10],0xd3b5a399ca0c2399, 64);
	bitslice(RC[11],0xc0ac29b7c97c50dd, 64);
	clock_t start, end, result = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);
	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		first_rounds(state, key_0, RC);
		end = mach_absolute_time();
		result += (end - start);
		for(bit = 0; bit < 64; bit++)	{
			state[bit] = 0xffffffff;
			key_0[bit] = 0;
			key_1[bit] = 0;
		}
	}
	printf("first_rounds time: %lu\n", (result / 100000) * info.numer / info.denom);
}

void lastRounds_time()	{
	// runs of 100000 to get mean for last rounds function
	uint32_t state[64] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	uint32_t key_0[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key_1[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t RC[12][64];
	int bit;
	bitslice(RC[0],0x0000000000000000, 64);
	bitslice(RC[1],0x13198a2e03707344, 64);
	bitslice(RC[2],0xa4093822299f31d0, 64);
	bitslice(RC[3],0x082efa98ec4e6c89, 64);
	bitslice(RC[4],0x452821e638d01377, 64);
	bitslice(RC[5],0xbe5466cf34e90c6c, 64);
	bitslice(RC[6],0x7ef84f78fd955cb1, 64);
	bitslice(RC[7],0x85840851f1ac43aa, 64);
	bitslice(RC[8],0xc882d32f25323c54, 64);
	bitslice(RC[9],0x64a51195e0e3610d, 64);
	bitslice(RC[10],0xd3b5a399ca0c2399, 64);
	bitslice(RC[11],0xc0ac29b7c97c50dd, 64);
	clock_t start, end, result = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);
	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		last_rounds(state, key_0, RC);
		end = mach_absolute_time();
		result += (end - start);
		for(bit = 0; bit < 64; bit++)	{
			state[bit] = 0xffffffff;
			key_0[bit] = 0;
			key_1[bit] = 0;
		}
	}
	printf("last_rounds time: %lu\n", (result / 100000) * info.numer / info.denom);
}
