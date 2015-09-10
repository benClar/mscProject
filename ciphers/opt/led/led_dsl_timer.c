#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "led_dsl_timer.h"

/*Performance Evaluation for LED*/

int main() {
	cipher_constant_time();
	cipher_time();
	addConstants_time();
	subCells_time();
	shift_row_time();
	MixColumnSerial_time();
	gm_mult_time();
}

void cipher_constant_time()	{
	// Runs cipher 1000 times to investigate timings of individual runs
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t MDS[16][4] = {{0}};
	uint32_t RC[32][6] = {{0}};
	bitslice(MDS[0],0x4,4);
	bitslice(MDS[1],0x1,4);
	bitslice(MDS[2],0x2,4);
	bitslice(MDS[3],0x2,4);
	bitslice(MDS[4],0x8,4);
	bitslice(MDS[5],0x6,4);
	bitslice(MDS[6],0x5,4);
	bitslice(MDS[7],0x6,4);
	bitslice(MDS[8],0xB,4);
	bitslice(MDS[9],0xE,4);
	bitslice(MDS[10],0xA,4);
	bitslice(MDS[11],0x9,4);
	bitslice(MDS[12],0x2,4);
	bitslice(MDS[13],0x2,4);
	bitslice(MDS[14],0xF,4);
	bitslice(MDS[15],0xB,4);

	bitslice(RC[0],0x01,6);
	bitslice(RC[1],0x03,6);
	bitslice(RC[2],0x07,6);
	bitslice(RC[3],0x0F,6);
	bitslice(RC[4],0x1F,6);
	bitslice(RC[5],0x3E,6);
	bitslice(RC[6],0x3D,6);
	bitslice(RC[7],0x3B,6);
	bitslice(RC[8],0x37,6);
	bitslice(RC[9],0x2F,6);
	bitslice(RC[10],0x1E,6);
	bitslice(RC[11],0x3C,6);
	bitslice(RC[12],0x39,6);
	bitslice(RC[13],0x33,6);
	bitslice(RC[14],0x27,6);
	bitslice(RC[15],0x0E,6);
	bitslice(RC[16],0x1D,6);
	bitslice(RC[17],0x3A,6);
	bitslice(RC[18],0x35,6);
	bitslice(RC[19],0x2B,6);
	bitslice(RC[20],0x16,6);
	bitslice(RC[21],0x2C,6);
	bitslice(RC[22],0x18,6);
	bitslice(RC[23],0x30,6);
	bitslice(RC[24],0x21,6);
	bitslice(RC[25],0x02,6);
	bitslice(RC[26],0x05,6);
	bitslice(RC[27],0x0B,6);
	bitslice(RC[28],0x17,6);
	bitslice(RC[29],0x2E,6);
	bitslice(RC[30],0x1C,6);
	bitslice(RC[31],0x38,6);
	clock_t start, end, result = 0, curr_time =0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);

	for(int run = 0; run < 1000; run++)	{
		start = mach_absolute_time();
		enc(state, key, MDS, RC);
		end = mach_absolute_time();
		curr_time = (end - start);
		result += curr_time;
		for(int bit = 0; bit < 64; bit++)	{
			state[bit] = 0;
		}
		for(int bit = 0; bit < 80; bit++)	{
			key[bit] = 0xffffffff;
		}
	}

	for(int run = 0; run < 1000; run++)	{
		start = mach_absolute_time();
		enc(state, key, MDS, RC);
		end = mach_absolute_time();
		curr_time = (end - start);
		result += curr_time;
		printf("%d %lu a\n",run + 1, (curr_time * info.numer) / info.denom);
		for(int bit = 0; bit < 64; bit++)	{
			state[bit] = 0;
		}
		for(int bit = 0; bit < 80; bit++)	{
			key[bit] = 0xffffffff;
		}
	}

}

void cipher_time(){
	//Run 100000 times to get mean and inter-quartile range
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t MDS[16][4] = {{0}};
	uint32_t RC[32][6] = {{0}};
	bitslice(MDS[0],0x4,4);
	bitslice(MDS[1],0x1,4);
	bitslice(MDS[2],0x2,4);
	bitslice(MDS[3],0x2,4);
	bitslice(MDS[4],0x8,4);
	bitslice(MDS[5],0x6,4);
	bitslice(MDS[6],0x5,4);
	bitslice(MDS[7],0x6,4);
	bitslice(MDS[8],0xB,4);
	bitslice(MDS[9],0xE,4);
	bitslice(MDS[10],0xA,4);
	bitslice(MDS[11],0x9,4);
	bitslice(MDS[12],0x2,4);
	bitslice(MDS[13],0x2,4);
	bitslice(MDS[14],0xF,4);
	bitslice(MDS[15],0xB,4);

	bitslice(RC[0],0x01,6);
	bitslice(RC[1],0x03,6);
	bitslice(RC[2],0x07,6);
	bitslice(RC[3],0x0F,6);
	bitslice(RC[4],0x1F,6);
	bitslice(RC[5],0x3E,6);
	bitslice(RC[6],0x3D,6);
	bitslice(RC[7],0x3B,6);
	bitslice(RC[8],0x37,6);
	bitslice(RC[9],0x2F,6);
	bitslice(RC[10],0x1E,6);
	bitslice(RC[11],0x3C,6);
	bitslice(RC[12],0x39,6);
	bitslice(RC[13],0x33,6);
	bitslice(RC[14],0x27,6);
	bitslice(RC[15],0x0E,6);
	bitslice(RC[16],0x1D,6);
	bitslice(RC[17],0x3A,6);
	bitslice(RC[18],0x35,6);
	bitslice(RC[19],0x2B,6);
	bitslice(RC[20],0x16,6);
	bitslice(RC[21],0x2C,6);
	bitslice(RC[22],0x18,6);
	bitslice(RC[23],0x30,6);
	bitslice(RC[24],0x21,6);
	bitslice(RC[25],0x02,6);
	bitslice(RC[26],0x05,6);
	bitslice(RC[27],0x0B,6);
	bitslice(RC[28],0x17,6);
	bitslice(RC[29],0x2E,6);
	bitslice(RC[30],0x1C,6);
	bitslice(RC[31],0x38,6);
	clock_t start, end;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);

	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		enc(state, key, MDS, RC);
		end = mach_absolute_time();
		printf("%lu\n",(end - start));
		for(int bit = 0; bit < 64; bit++)	{
			state[bit] = 0;
		}
		for(int bit = 0; bit < 80; bit++)	{
			key[bit] = 0xffffffff;
		}
	}
}

void addConstants_time()	{
	// Mean for add constant function
	uint32_t RC[32][6] = {{0}};
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	bitslice(RC[0],0x01,6);
	bitslice(RC[1],0x03,6);
	bitslice(RC[2],0x07,6);
	bitslice(RC[3],0x0F,6);
	bitslice(RC[4],0x1F,6);
	bitslice(RC[5],0x3E,6);
	bitslice(RC[6],0x3D,6);
	bitslice(RC[7],0x3B,6);
	bitslice(RC[8],0x37,6);
	bitslice(RC[9],0x2F,6);
	bitslice(RC[10],0x1E,6);
	bitslice(RC[11],0x3C,6);
	bitslice(RC[12],0x39,6);
	bitslice(RC[13],0x33,6);
	bitslice(RC[14],0x27,6);
	bitslice(RC[15],0x0E,6);
	bitslice(RC[16],0x1D,6);
	bitslice(RC[17],0x3A,6);
	bitslice(RC[18],0x35,6);
	bitslice(RC[19],0x2B,6);
	bitslice(RC[20],0x16,6);
	bitslice(RC[21],0x2C,6);
	bitslice(RC[22],0x18,6);
	bitslice(RC[23],0x30,6);
	bitslice(RC[24],0x21,6);
	bitslice(RC[25],0x02,6);
	bitslice(RC[26],0x05,6);
	bitslice(RC[27],0x0B,6);
	bitslice(RC[28],0x17,6);
	bitslice(RC[29],0x2E,6);
	bitslice(RC[30],0x1C,6);
	bitslice(RC[31],0x38,6);
	clock_t start, end, result = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);

	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();;
		addConstants(state, RC[0]);
		end = mach_absolute_time();;
		result += (end - start);
		for(int bit = 0; bit < 64; bit++)	{
			state[bit] = 0;
		}
	}
	printf("addConstants time: %lu\n", (result / 100000) * info.numer / info.denom);
}

void subCells_time()	{
	// Mean for subcells function
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	clock_t start, end, result = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);

	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		subCells(state);
		end = mach_absolute_time();
		result += (end - start);
		for(int bit = 0; bit < 64; bit++)	{
			state[bit] = 0;
		}
	}
	printf("Subcells time: %lu\n", (result / 100000) * info.numer / info.denom);
}

void shift_row_time()	{
	// Mean for shift row function
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	clock_t start, end, result = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);

	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		shift_row(state);
		end = mach_absolute_time();
		result += (end - start);
		for(int bit = 0; bit < 64; bit++)	{
			state[bit] = 0;
		}
	}
	printf("shift_row time: %lu\n", (result / 100000) * info.numer / info.denom);
}

void MixColumnSerial_time()	{
	// Mean for MixColumnSerial
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t MDS[16][4] = {{0}};
	bitslice(MDS[0],0x4,4);
	bitslice(MDS[1],0x1,4);
	bitslice(MDS[2],0x2,4);
	bitslice(MDS[3],0x2,4);
	bitslice(MDS[4],0x8,4);
	bitslice(MDS[5],0x6,4);
	bitslice(MDS[6],0x5,4);
	bitslice(MDS[7],0x6,4);
	bitslice(MDS[8],0xB,4);
	bitslice(MDS[9],0xE,4);
	bitslice(MDS[10],0xA,4);
	bitslice(MDS[11],0x9,4);
	bitslice(MDS[12],0x2,4);
	bitslice(MDS[13],0x2,4);
	bitslice(MDS[14],0xF,4);
	bitslice(MDS[15],0xB,4);
	clock_t start, end, result = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);

	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		MixColumnSerial(state, MDS);
		end = mach_absolute_time();
		result += (end - start);
		for(int bit = 0; bit < 64; bit++)	{
			state[bit] = 0;
		}
	}
	printf("MixColumnSerial time: %lu\n", (result / 100000) * info.numer / info.denom);
}

void gm_mult_time()	{
	// Mean gmMult function
	uint32_t op_1[4] = {1,0,1,0};
	uint32_t op_2[4] = {0,0,1,0};
	uint32_t output[4] = {0};
	clock_t start, end, result = 0;
	mach_timebase_info_data_t info;
	mach_timebase_info(&info);

	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		gmMult(output, op_1, op_2);
		end = mach_absolute_time();
		result += (end - start);
		for(int bit = 0; bit < 4; bit++)	{
			output[bit] = 0;
		}
	}
	printf("gm mult time: %lu\n", (result / 100000) * info.numer / info.denom);
}

