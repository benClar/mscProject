#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "present_timer.h"

int main() {
	cipher_time();
	pLayer_time();
	generate_round_keys_time();
	sBox_layer_time();
}

void cipher_time(){
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key[80] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	uint32_t round_keys[32][64] = {{ 0 }};
	clock_t start, end, result = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);

	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		enc(key, state, round_keys);
		end = mach_absolute_time();
		result += (end - start);
		for(int bit = 0; bit < 64; bit++)	{
			state[bit] = 0;
		}
		for(int bit = 0; bit < 80; bit++)	{
			key[bit] = 0xffffffff;
		}
	}
	printf("cipher time: %lu\n", (result / 100000) * info.numer / info.denom);
}

void pLayer_time(){
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	clock_t start, end, result = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);

	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		pLayer(state);
		end = mach_absolute_time();
		result += (end - start);
		for(int bit = 0; bit < 64; bit++)	{
			state[bit] = 0;
		}
	}
	printf("pLayer time: %lu\n", (result / 100000) * info.numer / info.denom);	
}

void generate_round_keys_time()	{
	uint32_t key[80] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	clock_t start, end, result = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);

	for(int run = 0; run < 100000; run++)	{
		uint32_t round_keys[32][64] = {{ 0 }};
		start = mach_absolute_time();
		generateRoundKey(key, round_keys);
		end = mach_absolute_time();
		result += (end - start);
		for(int bit = 0; bit < 80; bit++)	{
			key[bit] = 0xffffffff;
		}
	}
	printf("generate_round_keys time: %lu\n", (result / 100000) * info.numer / info.denom);		
}

void sBox_layer_time()	{
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	clock_t start, end, result = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);

	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		sBox_layer(state);
		end = mach_absolute_time();
		result += (end - start);
		for(int bit = 0; bit < 64; bit++)	{
			state[bit] = 0;
		}
	}
	printf("sbox_Layer time: %lu\n", (result / 100000) * info.numer / info.denom);		
}


