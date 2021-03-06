#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "led_tests.h"

int main() {
	sput_start_testing();
	sput_enter_suite("LED Test 1");
	sput_run_test(led_test_1);
	sput_enter_suite("LED Test 2");
	sput_run_test(led_test_2);
	sput_finish_testing();
	return sput_get_return_value();
}


void led_test_1()	{
	uint32_t exp_res[64] = {1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,0,1,0,1,1,0,1,1,0,1,0,0,1,1,0,1,1,0,1,0,0,0,1,0,1,1,1,0,0,0,1,0,0,1,1,0,0,1,1,0,0,1};
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	int bit;
	int slice;
	uint32_t MDS[16][4] = {{0}};
	uint32_t RC[32][6] = {{0}};
	bitslice_bend(MDS[0],0x4,4);
	bitslice_bend(MDS[1],0x1,4);
	bitslice_bend(MDS[2],0x2,4);
	bitslice_bend(MDS[3],0x2,4);
	bitslice_bend(MDS[4],0x8,4);
	bitslice_bend(MDS[5],0x6,4);
	bitslice_bend(MDS[6],0x5,4);
	bitslice_bend(MDS[7],0x6,4);
	bitslice_bend(MDS[8],0xB,4);
	bitslice_bend(MDS[9],0xE,4);
	bitslice_bend(MDS[10],0xA,4);
	bitslice_bend(MDS[11],0x9,4);
	bitslice_bend(MDS[12],0x2,4);
	bitslice_bend(MDS[13],0x2,4);
	bitslice_bend(MDS[14],0xF,4);
	bitslice_bend(MDS[15],0xB,4);

	bitslice_bend(RC[0],0x01,6);
	bitslice_bend(RC[1],0x03,6);
	bitslice_bend(RC[2],0x07,6);
	bitslice_bend(RC[3],0x0F,6);
	bitslice_bend(RC[4],0x1F,6);
	bitslice_bend(RC[5],0x3E,6);
	bitslice_bend(RC[6],0x3D,6);
	bitslice_bend(RC[7],0x3B,6);
	bitslice_bend(RC[8],0x37,6);
	bitslice_bend(RC[9],0x2F,6);
	bitslice_bend(RC[10],0x1E,6);
	bitslice_bend(RC[11],0x3C,6);
	bitslice_bend(RC[12],0x39,6);
	bitslice_bend(RC[13],0x33,6);
	bitslice_bend(RC[14],0x27,6);
	bitslice_bend(RC[15],0x0E,6);
	bitslice_bend(RC[16],0x1D,6);
	bitslice_bend(RC[17],0x3A,6);
	bitslice_bend(RC[18],0x35,6);
	bitslice_bend(RC[19],0x2B,6);
	bitslice_bend(RC[20],0x16,6);
	bitslice_bend(RC[21],0x2C,6);
	bitslice_bend(RC[22],0x18,6);
	bitslice_bend(RC[23],0x30,6);
	bitslice_bend(RC[24],0x21,6);
	bitslice_bend(RC[25],0x02,6);
	bitslice_bend(RC[26],0x05,6);
	bitslice_bend(RC[27],0x0B,6);
	bitslice_bend(RC[28],0x17,6);
	bitslice_bend(RC[29],0x2E,6);
	bitslice_bend(RC[30],0x1C,6);
	bitslice_bend(RC[31],0x38,6);
	enc(state, key, MDS, RC);

	for(slice = 0; slice < 32; slice++)	{
		for(bit = 0; bit < 64; bit++)	{
			// printf("%d ", (state[bit] >> slice) & 0x1);
			// sput_fail_unless(state[bit] == exp_res[bit],"LED Test 1");
			sput_fail_unless(((state[bit] >> slice) & 0x1) == exp_res[bit],"LED Test 1");
		}
		printf("\n");
	}
}

void led_test_2()	{
	uint32_t exp_res[64] = {1,1,1,1,1,1,0,1,1,1,0,1,0,1,1,0,1,1,1,1,1,0,1,1,1,0,0,1,1,0,0,0,0,1,0,0,0,1,0,1,1,1,1,1,1,0,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,1,1,0};
	uint32_t state[64] = {0,0,0,0,0,0,0,0xffffffff,0,0,0xffffffff,0,0,0,0xffffffff,0xffffffff,0,0xffffffff,0,0,0,0xffffffff,0,0xffffffff,0,0xffffffff,0xffffffff,0,0,0xffffffff,0xffffffff,0xffffffff, 0xffffffff,0,0,0, 0xffffffff,0,0,0xffffffff,0xffffffff,0,0xffffffff,0,0xffffffff,0,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0,0,0xffffffff,0xffffffff,0,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	uint32_t key[64] =   {0,0,0,0,0,0,0,0xffffffff,0,0,0xffffffff,0,0,0,0xffffffff,0xffffffff,0,0xffffffff,0,0,0,0xffffffff,0,0xffffffff,0,0xffffffff,0xffffffff,0,0,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0,0,0,0xffffffff,0,0,0xffffffff,0xffffffff,0,0xffffffff,0,0xffffffff,0,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0,0,0xffffffff,0xffffffff,0,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	uint32_t MDS[16][4] = {{0}};
	uint32_t RC[32][6] = {{0}};
	int bit;
	int slice;
	bitslice_bend(MDS[0],0x4,4);
	bitslice_bend(MDS[1],0x1,4);
	bitslice_bend(MDS[2],0x2,4);
	bitslice_bend(MDS[3],0x2,4);
	bitslice_bend(MDS[4],0x8,4);
	bitslice_bend(MDS[5],0x6,4);
	bitslice_bend(MDS[6],0x5,4);
	bitslice_bend(MDS[7],0x6,4);
	bitslice_bend(MDS[8],0xB,4);
	bitslice_bend(MDS[9],0xE,4);
	bitslice_bend(MDS[10],0xA,4);
	bitslice_bend(MDS[11],0x9,4);
	bitslice_bend(MDS[12],0x2,4);
	bitslice_bend(MDS[13],0x2,4);
	bitslice_bend(MDS[14],0xF,4);
	bitslice_bend(MDS[15],0xB,4);

	bitslice_bend(RC[0],0x01,6);
	bitslice_bend(RC[1],0x03,6);
	bitslice_bend(RC[2],0x07,6);
	bitslice_bend(RC[3],0x0F,6);
	bitslice_bend(RC[4],0x1F,6);
	bitslice_bend(RC[5],0x3E,6);
	bitslice_bend(RC[6],0x3D,6);
	bitslice_bend(RC[7],0x3B,6);
	bitslice_bend(RC[8],0x37,6);
	bitslice_bend(RC[9],0x2F,6);
	bitslice_bend(RC[10],0x1E,6);
	bitslice_bend(RC[11],0x3C,6);
	bitslice_bend(RC[12],0x39,6);
	bitslice_bend(RC[13],0x33,6);
	bitslice_bend(RC[14],0x27,6);
	bitslice_bend(RC[15],0x0E,6);
	bitslice_bend(RC[16],0x1D,6);
	bitslice_bend(RC[17],0x3A,6);
	bitslice_bend(RC[18],0x35,6);
	bitslice_bend(RC[19],0x2B,6);
	bitslice_bend(RC[20],0x16,6);
	bitslice_bend(RC[21],0x2C,6);
	bitslice_bend(RC[22],0x18,6);
	bitslice_bend(RC[23],0x30,6);
	bitslice_bend(RC[24],0x21,6);
	bitslice_bend(RC[25],0x02,6);
	bitslice_bend(RC[26],0x05,6);
	bitslice_bend(RC[27],0x0B,6);
	bitslice_bend(RC[28],0x17,6);
	bitslice_bend(RC[29],0x2E,6);
	bitslice_bend(RC[30],0x1C,6);
	bitslice_bend(RC[31],0x38,6);

	enc(state, key, MDS, RC);
	for(slice = 0; slice < 32; slice++)	{
		for(bit = 0; bit < 64; bit++)	{
			sput_fail_unless(((state[bit] >> slice) & 0x1) == exp_res[bit],"LED Test 2");
		}
	}
}

