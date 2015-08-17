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
	uint32_t output[32][1] = {{0}};
	
	// clock_t start, end, result = 0;

	// for(int run = 0; run < 100000; run++)	{
	// 	start = mach_absolute_time();
		lfsr(output,state);
		// end = mach_absolute_time();
	// 	result += (end - start);
	// 	state[0] = 0;
	// 	state[1] = 0xffffffff;
	// 	state[2] = 0;
	// 	state[3] = 0xffffffff;
	// 	state[4] = 0;
	// 	state[5] = 0xffffffff;
	// 	state[6] = 0;
	// 	state[7] = 0xffffffff;
	// 	for(int bit = 0; bit < 32; bit++)	{
	// 		output[bit][0] = 0;
	// 	}
	// }
	// printf("%lu\n", result / 100000);
	for(int slice = 0; slice < 32; slice++)	{
		for(int bit = 0; bit < 32; bit++)	{
			sput_fail_unless(((output[bit][0] >> slice) & 0x1) == exp_res[bit],"lfsr Test 1");
		}
	}
}


