#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "present_tests.h"

/* Data stored in big-endian fashion : 0th bit = last element i.e.
http://download.springer.com/static/pdf/68/chp%253A10.1007%252F978-3-540-74735-2_31.pdf?originUrl=http%3A%2F%2Flink.springer.com%2Fchapter%2F10.1007%2F978-3-540-74735-2_31&token2=exp=1442232812~acl=%2Fstatic%2Fpdf%2F68%2Fchp%25253A10.1007%25252F978-3-540-74735-2_31.pdf%3ForiginUrl%3Dhttp%253A%252F%252Flink.springer.com%252Fchapter%252F10.1007%252F978-3-540-74735-2_31*~hmac=98a53cb99566c7a9a6e91d915acfe31b3fd0516bce1547a4be33af11ef8079ab */


int main() {
	sput_start_testing();
	sput_enter_suite("Present Test 1");
	sput_run_test(present_test_1);
	sput_enter_suite("Present Test 2");
	sput_run_test(present_test_2);
	sput_enter_suite("Present Test 3");
	sput_run_test(present_test_3);	
	sput_enter_suite("Present Test 4");
	sput_run_test(present_test_4);
	sput_finish_testing();
	return sput_get_return_value();
}


void present_test_1()	{
	// ciphertext: 0xE72C46C0F5945049
	// key: 0xffffffffffffffffffff
	// plaintext: 0x0000000000000000
	uint32_t exp_res[64] = {1,1,1,0,0,1,1,1,0,0,1,0,1,1,0,0,0,1,0,0,0,1,1,0,1,1,0,0,0,0,0,0,1,1,1,1,0,1,0,1,1,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,1,0,0,1};
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key[80] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	uint32_t round_key[32][64] = {{0}};
	int bit;

	enc(key, state, round_key);
	for(int slice = 0; slice < 32; slice++)	{
		for(bit = 0; bit < 64; bit++)	{
			sput_fail_unless(((state[bit] >> slice) & 0x1) == exp_res[bit],"present Test 1");
		}
	}
}

void present_test_2()	{
	// ciphertext: 0x5579C1387B228445
	// key: 0x00000000000000000000
	// plaintext: 0x0000000000000000
	uint32_t exp_res[64] = {0,1,0,1,0,1,0,1,0,1,1,1,1,0,0,1,1,1,0,0,0,0,0,1,0,0,1,1,1,0,0,0,0,1,1,1,1,0,1,1,0,0,1,0,0,0,1,0,1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,1};
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key[80] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t round_key[32][64] = {{0}};
	int bit;
	enc(key, state, round_key);
	for(int slice = 0; slice < 32; slice++)	{
		for(bit = 0; bit < 64; bit++)	{
			sput_fail_unless(((state[bit] >> slice) & 0x1) == exp_res[bit],"present Test 1");
		}
	}
	// print(exp_res,64);
}

void present_test_3()	{
	// ciphertext: 0xA112FFC72F68417B
	// key: 0x00000000000000000000
	// plaintext: 0xffffffffffffffff
	uint32_t exp_res[64] = {1,0,1,0,0,0,0,1,0,0,0,1,0,0,1,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,0,0,1,0,1,1,1,1,0,1,1,0,1,0,0,0,0,1,0,0,0,0,0,1,0,1,1,1,1,0,1,1};
	uint32_t state[64] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	uint32_t key[80] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t round_key[32][64] = {{0}};
	int bit;
	enc(key, state, round_key);
	for(int slice = 0; slice < 32; slice++)	{
		for(bit = 0; bit < 64; bit++)	{
			sput_fail_unless(((state[bit] >> slice) & 0x1) == exp_res[bit],"present Test 1");
		}
	}
	// print(exp_res,64);
}

void present_test_4()	{
	// ciphertext: 0x3333DCD3213210D2
	// key: 0xffffffffffffffff
	// plaintext: 0xffffffffffffffff
	uint32_t exp_res[64] = {0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,1,1,0,1,1,1,0,0,1,1,0,1,0,0,1,1,0,0,1,0,0,0,0,1,0,0,1,1,0,0,1,0,0,0,0,1,0,0,0,0,1,1,0,1,0,0,1,0};
	uint32_t state[64] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	uint32_t key[80] = {0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0xffffffff};
	uint32_t round_key[32][64] = {{0}};
	int bit;
	enc(key, state, round_key);
	for(int slice = 0; slice < 32; slice++)	{
		for(bit = 0; bit < 64; bit++)	{
			sput_fail_unless(((state[bit] >> slice) & 0x1) == exp_res[bit],"present Test 1");
		}
	}
	// print(exp_res,64);
}
