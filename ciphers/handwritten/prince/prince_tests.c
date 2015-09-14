/*---------- Standard Headers -----------*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

/*---------- Custom Headers	-----------*/

#include "prince_tests.h"

/* Data stored in little-endian fashion : 0th bit = 0th element i.e. produced cipher texts are 'backwards'.
http://download.springer.com/static/pdf/68/chp%253A10.1007%252F978-3-540-74735-2_31.pdf?originUrl=http%3A%2F%2Flink.springer.com%2Fchapter%2F10.1007%2F978-3-540-74735-2_31&token2=exp=1442232812~acl=%2Fstatic%2Fpdf%2F68%2Fchp%25253A10.1007%25252F978-3-540-74735-2_31.pdf%3ForiginUrl%3Dhttp%253A%252F%252Flink.springer.com%252Fchapter%252F10.1007%252F978-3-540-74735-2_31*~hmac=98a53cb99566c7a9a6e91d915acfe31b3fd0516bce1547a4be33af11ef8079ab */

int main() {
	sput_start_testing();
	sput_enter_suite("Prince Test 1");
	sput_run_test(prince_test_1);
	sput_enter_suite("Prince Test 2");
	sput_run_test(prince_test_2);
	sput_enter_suite("Prince Test 3");
	sput_run_test(prince_test_3);
	sput_enter_suite("Prince Test 4");
	sput_run_test(prince_test_4);
	sput_finish_testing();
	return sput_get_return_value();
}

void prince_test_1()	{
	// cipher Text: 0x604AE6CA03C20ADA
	// plaintext: 0xffffffffffffffff
	// k0:0x0000000000000000
	// k1: 0x0000000000000000
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
	}
}


void prince_test_2()	{
	// cipher Text: 0x818665AA0D02DFDA
	// plaintext: 0x0000000000000000
	// k0:0x0000000000000000
	// k1: 0x0000000000000000
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
	// cipher Text: 0x9FB51935FC3DF524
	// plaintext: 0x0000000000000000
	// k0:0xffffffffffffffff
	// k1: 0x0000000000000000
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
	}
}

void prince_test_4() {
	// cipher Text: 0x78A54CBE737BB7EF
	// plaintext: 0x0000000000000000
	// k0:0x0000000000000000
	// k1: 0xffffffffffffffff
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
