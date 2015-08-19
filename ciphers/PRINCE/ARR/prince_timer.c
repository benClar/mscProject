#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "prince_timer.h"

int main() {
	cipher_constant_time();
	// cipher_time();
	// mPrime_time();
	// sBox_layer_time();
	// shift_rows_time();
	// lastRounds_time();
	// firstRounds_time();
}

void cipher_constant_time()	{
uint32_t state[64] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	uint32_t key_0[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key_1[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t RC[12][64];
	int bit;
	bitslice_bend(RC[0],0x0000000000000000, 64);
	bitslice_bend(RC[1],0x13198a2e03707344, 64);
	bitslice_bend(RC[2],0xa4093822299f31d0, 64);
	bitslice_bend(RC[3],0x082efa98ec4e6c89, 64);
	bitslice_bend(RC[4],0x452821e638d01377, 64);
	bitslice_bend(RC[5],0xbe5466cf34e90c6c, 64);
	bitslice_bend(RC[6],0x7ef84f78fd955cb1, 64);
	bitslice_bend(RC[7],0x85840851f1ac43aa, 64);
	bitslice_bend(RC[8],0xc882d32f25323c54, 64);
	bitslice_bend(RC[9],0x64a51195e0e3610d, 64);
	bitslice_bend(RC[10],0xd3b5a399ca0c2399, 64);
	bitslice_bend(RC[11],0xc0ac29b7c97c50dd, 64);
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);
	clock_t start, end, result = 0;
	for(int run = 0; run < 1000; run++)	{
		start = mach_absolute_time();
		enc(RC, state, key_0, key_1);
		end = mach_absolute_time();
		result = end - start;
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
		result = end - start;
		for(bit = 0; bit < 64; bit++)	{
			state[bit] = 0xffffffff;
			key_0[bit] = 0;
			key_1[bit] = 0;
		}
		printf("%d %lu a\n",run + 1, (result * info.numer) / info.denom);
	}
}

void cipher_time(){
	uint32_t state[64] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	uint32_t key_0[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key_1[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t RC[12][64];
	int bit;
	bitslice_bend(RC[0],0x0000000000000000, 64);
	bitslice_bend(RC[1],0x13198a2e03707344, 64);
	bitslice_bend(RC[2],0xa4093822299f31d0, 64);
	bitslice_bend(RC[3],0x082efa98ec4e6c89, 64);
	bitslice_bend(RC[4],0x452821e638d01377, 64);
	bitslice_bend(RC[5],0xbe5466cf34e90c6c, 64);
	bitslice_bend(RC[6],0x7ef84f78fd955cb1, 64);
	bitslice_bend(RC[7],0x85840851f1ac43aa, 64);
	bitslice_bend(RC[8],0xc882d32f25323c54, 64);
	bitslice_bend(RC[9],0x64a51195e0e3610d, 64);
	bitslice_bend(RC[10],0xd3b5a399ca0c2399, 64);
	bitslice_bend(RC[11],0xc0ac29b7c97c50dd, 64);
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);
	clock_t start, end, result = 0, high = 0, low = 0;
	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		enc(RC, state, key_0, key_1);
		end = mach_absolute_time();
		result += end - start;
		for(bit = 0; bit < 64; bit++)	{
			state[bit] = 0xffffffff;
			key_0[bit] = 0;
			key_1[bit] = 0;
		}
		if (result > high)	{
			high = result;
		}
		if (result < low)	{
			low = result;
		}
	}
	printf("cipher time: %lu\n", (result / 100000) * info.numer / info.denom);
	// printf("cipher time high: %lu\n", (high / 100000) * info.numer / info.denom);
	// printf("cipher time low: %lu\n", (low / 100000) * info.numer / info.denom);
}

void mPrime_time()	{
	uint32_t state[64] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	int bit;
	clock_t start, end, result = 0, high = 0, low = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);
	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		mprime(state);
		end = mach_absolute_time();
		result += (end - start);
		for(bit = 0; bit < 64; bit++)	{
			state[bit] = 0xffffffff;
		}
		if (result > high)	{
			high = result;
		}
		if (result < low)	{
			low = result;
		}
	}
	printf("mprime time: %lu\n", (result / 100000) * info.numer / info.denom);
	// printf("mprime high: %lu\n", (high / 100000) * info.numer / info.denom);
	// printf("mprime low: %lu\n", (low / 100000) * info.numer / info.denom);
}

void shift_rows_time()	{
	uint32_t state[64] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	int bit;
	clock_t start, end, result = 0, high = 0, low = 0;
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
		if (result > high)	{
			high = result;
		}
		if (result < low)	{
			low = result;
		}
	}
	printf("shift_rows time: %lu\n", (result / 100000) * info.numer / info.denom);
	// printf("shift_rows high: %lu\n", (high / 100000) * info.numer / info.denom);
	// printf("shift_rows low: %lu\n", (low / 100000) * info.numer / info.denom);
}

void sBox_layer_time()	{
	uint32_t state[64] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	int bit;
	clock_t start, end, result = 0, high = 0, low = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);
	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		sBox(state, 1);
		end = mach_absolute_time();
		result += (end - start);
		for(bit = 0; bit < 64; bit++)	{
			state[bit] = 0xffffffff;
		}
		if (result > high)	{
			high = result;
		}
		if (result < low)	{
			low = result;
		}
	}
	printf("sBox_layer time: %lu\n", (result / 100000) * info.numer / info.denom);
	// printf("sBox_layer high: %lu\n", (high / 100000) * info.numer / info.denom);
	// printf("sBox_layer low: %lu\n", (low / 100000) * info.numer / info.denom);
}

void firstRounds_time()	{
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
	clock_t start, end, result = 0, high = 0, low = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);

	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		first_rounds(state, RC, key_0);
		end = mach_absolute_time();
		result += (end - start);
		for(bit = 0; bit < 64; bit++)	{
			state[bit] = 0xffffffff;
			key_0[bit] = 0;
			key_1[bit] = 0;
		}
		if (result > high)	{
			high = result;
		}
		if (result < low)	{
			low = result;
		}
	}
	printf("first_rounds time: %lu\n", (result / 100000) * info.numer / info.denom);
	// printf("first_rounds high: %lu\n", (high / 100000) * info.numer / info.denom);
	// printf("first_rounds low: %lu\n", (low / 100000) * info.numer / info.denom);
}

void lastRounds_time()	{
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
	clock_t start, end, result = 0, high = 0, low = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);

	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		last_rounds(state, RC, key_0);
		end = mach_absolute_time();
		result += (end - start);
		for(bit = 0; bit < 64; bit++)	{
			state[bit] = 0xffffffff;
			key_0[bit] = 0;
			key_1[bit] = 0;
		}
		if (result > high)	{
			high = result;
		}
		if (result < low)	{
			low = result;
		}
	}

	printf("last_rounds time: %lu\n", (result / 100000) * info.numer / info.denom);
	// printf("last_rounds high: %lu\n", (high / 100000) * info.numer / info.denom);
	// printf("last_rounds low: %lu\n", (low / 100000) * info.numer / info.denom);
}



