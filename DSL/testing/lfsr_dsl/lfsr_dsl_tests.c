#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "lfsr_dsl_tests.h"

int main() {
	sput_start_testing();
	sput_enter_suite("LFSR Test 1");
	sput_run_test(lfsr_test_1);
	sput_finish_testing();
	return sput_get_return_value();
}

void lfsr_test_1()	{
	uint32_t exp_res[32] = {1,0,1,0,1,0,1,0,0,1,0,1,1,1,1,0,0,1,1,0,1,1,0,0,0,0,0,1,0,0,0,1};
	uint32_t state[8] = {0,0xffffffff,0,0xffffffff,0,0xffffffff,0,0xffffffff};
	uint32_t output[32] = {0};
	
	lfsr(output,state);
	for(int slice = 0; slice < 32; slice++)	{
		for(int bit = 0; bit < 32; bit++)	{
			sput_fail_unless(((output[bit] >> slice) & 0x1) == exp_res[bit],"lfsr Test 1");
		}
	}
}


