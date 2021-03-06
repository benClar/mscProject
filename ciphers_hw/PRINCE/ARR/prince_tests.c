/*---------- Standard Headers -----------*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

/*---------- Custom Headers	-----------*/

#include "prince_tests.h"


int main() {
	sput_start_testing();
	// sput_enter_suite("Prince Test 1");
	// sput_run_test(prince_test_1);
	// sput_enter_suite("Prince Test 2");
	// sput_run_test(prince_test_2);
	sput_enter_suite("Prince Test 3");
	sput_run_test(prince_test_3);
	sput_enter_suite("Prince Test 4");
	sput_run_test(prince_test_4);
	sput_finish_testing();
	return sput_get_return_value();
}

void prince_test_1()	{
	uint32_t exp_res[64] = {0,1,0,1,1,0,1,1,0,1,0,1,0,0,0,0,0,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1,0,1,0,0,1,1,0,1,1,0,0,1,1,1,0,1,0,1,0,0,1,0,0,0,0,0,0,1,1,0};
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

	enc(RC, state, key_0, key_1);
	for(int slice = 0; slice < 32; slice++)	{
		for(bit = 0; bit < 64; bit++)	{
			sput_fail_unless(((state[bit] >> slice) & 0x1) == exp_res[63 - bit],"prince Test 1");
		}
		printf("\n");
	}
}

void prince_test_2()	{
	uint32_t exp_res[64] = {0,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,0,1,0,0,0,0,0,0,1,0,1,1,0,0,0,0,0,1,0,1,0,1,0,1,1,0,1,0,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1};
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
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
	enc(RC, state, key_0, key_1);
	for(int slice = 0; slice < 32; slice++)	{
		for(bit = 0; bit < 64; bit++)	{
			sput_fail_unless(((state[bit] >> slice) & 0x1) == exp_res[63 - bit],"prince Test 2");
		}
		printf("\n");
	}
}

void prince_test_3() {
	uint32_t exp_res[64] = {1,0,0,1,1,1,1,1,1,0,1,1,0,1,0,1,0,0,0,1,1,0,0,1,0,0,1,1,0,1,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,0,1,0,0,1,0,0};
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key_0[64] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
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
	enc(RC, state, key_0, key_1);
	for(int slice = 0; slice < 32; slice++)	{
		for(bit = 0; bit < 64; bit++)	{
			sput_fail_unless(((state[bit] >> slice) & 0x1) == exp_res[bit],"prince Test 3");
		}
		printf("\n");
	}
}

void prince_test_4() {
	uint32_t exp_res[64] = {0,1,1,1,1,0,0,0,1,0,1,0,0,1,0,1,0,1,0,0,1,1,0,0,1,0,1,1,1,1,1,0,0,1,1,1,0,0,1,1,0,1,1,1,1,0,1,1,1,0,1,1,0,1,1,1,1,1,1,0,1,1,1,1};
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key_0[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key_1[64] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
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
	enc(RC, state, key_0, key_1);
	for(int slice = 0; slice < 32; slice++)	{
		for(bit = 0; bit < 64; bit++)	{
			sput_fail_unless(((state[bit] >> slice) & 0x1) == exp_res[bit],"prince Test 4");
		}
	}
}
