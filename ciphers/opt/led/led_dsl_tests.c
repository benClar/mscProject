#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "led_dsl_tests.h"

/*data stored in little endian fashion 0-th bit = 0-th element i.e. produced cipher texts are 'backwards'.
https://docs.google.com/viewer?a=v&pid=sites&srcid=ZGVmYXVsdGRvbWFpbnxsZWRibG9ja2NpcGhlcnxneDoxYmQ4ODY1MGY1MDhlNjk2 */

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
	//ciphertext: EFBBBD6D368B8999
	//key:0x0000000000000000
	//plaintext: 0x0000000000000000
	uint32_t exp_res[64] = {0,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,0,1,1,0,1,1,0,1,0,1,1,1,1,0,0,0,1,1,0,0,0,0,1,1,1,0,1,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1};
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	int bit;
	int slice;
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

	enc(state, key, MDS, RC);

	for(slice = 0; slice < 32; slice++)	{
		for(bit = 0; bit < 64; bit++)	{
			sput_fail_unless(((state[bit] >> slice) & 0x1) == exp_res[bit],"LED Test 2");
		}
	}
}

void led_test_2()	{
	//ciphertext: FDD6FB8945F81456
	//key: 0x123456789abcdef
	//plaintext: 0x123456789abcdef
	uint32_t exp_res[64] = {1,1,1,1,1,0,1,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,0,1,0,0,0,1,0,0,1,0,1,0,1,0,1,1,1,1,0,0,0,1,1,0,0,0,0,0,1,0,1,0,1,0,0,1,1,0};
	uint32_t state[64] = {0,0,0,0,0xffffffff,0,0,0,0,0xffffffff,0,0,0xffffffff,0xffffffff,0,0,0,0,0xffffffff,0,0xffffffff,0,0xffffffff,0,0,0xffffffff,0xffffffff,0,0xffffffff,0xffffffff,0xffffffff,0,0,0,0,0xffffffff,0xffffffff,0,0,0xffffffff,0,0xffffffff,0,0xffffffff,0xffffffff,0xffffffff,0,0xffffffff,0,0,0xffffffff,0xffffffff,0xffffffff,0,0xffffffff,0xffffffff,0,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	uint32_t key[64] = {0,0,0,0,0xffffffff,0,0,0,0,0xffffffff,0,0,0xffffffff,0xffffffff,0,0,0,0,0xffffffff,0,0xffffffff,0,0xffffffff,0,0,0xffffffff,0xffffffff,0,0xffffffff,0xffffffff,0xffffffff,0,0,0,0,0xffffffff,0xffffffff,0,0,0xffffffff,0,0xffffffff,0,0xffffffff,0xffffffff,0xffffffff,0,0xffffffff,0,0,0xffffffff,0xffffffff,0xffffffff,0,0xffffffff,0xffffffff,0,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	uint32_t MDS[16][4] = {{0}};
	uint32_t RC[32][6] = {{0}};
	int bit;
	int slice;
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

	enc(state, key, MDS, RC);
	for(slice = 0; slice < 32; slice++)	{
		for(bit = 0; bit < 64; bit++)	{
			sput_fail_unless(((state[bit] >> slice) & 0x1) == exp_res[bit],"LED Test 2");
		}
	}

}
