#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "present_dsl_tests.h"

int main() {
	sput_start_testing();
	sput_enter_suite("Present Test 1");
	sput_run_test(present_test_1);
	// sput_enter_suite("Present Test 2");
	// sput_run_test(present_test_2);
	// sput_enter_suite("Present Test 3");
	// sput_run_test(present_test_3);	
	// sput_enter_suite("Present Test 4");
	// sput_run_test(present_test_4);
	sput_finish_testing();
	return sput_get_return_value();
}


void present_test_1()	{
	uint32_t exp_res[64] = {1,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,1,1,0,1,0,1,1,1,1,0,0,0,0,0,0,1,1,0,1,1,0,0,0,1,0,0,0,1,1,0,1,0,0,1,1,1,0,0,1,1,1};
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key[80] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
	int bit;
	clock_t start, end;
	// double cpu_time_used;
	// start = clock();
	start = mach_absolute_time();
	// uint64_t test =  mach_absolute_time();
	enc(key, state);
	end = mach_absolute_time();

	printf("%lu\n", end - start);
	// end = clock();
	// cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
	// printf("cpu time used : %f \n", cpu_time_used);

	// for(bit = 0; bit < 64; bit++)	{
	// 	sput_fail_unless(state[bit] == exp_res[bit],"present Test 1");
	// }
}

void present_test_2()	{
	uint32_t exp_res[64] = {1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,1,0,0,1,1,0,1,1,1,1,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,1,1,1,0,0,1,1,1,1,0,1,0,1,0,1,0,1,0};
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key[80] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	int bit;
	enc(key, state);
	for(bit = 0; bit < 64; bit++)	{
		sput_fail_unless(state[bit] == exp_res[bit],"present Test 1");
	}
}

void present_test_3()	{
	uint32_t exp_res[64] = {1,1,0,1,1,1,1,0,1,0,0,0,0,0,1,0,0,0,0,1,0,1,1,0,1,1,1,1,0,1,0,0,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,0,1,0,0,1,0,0,0,1,0,0,0,0,1,0,1};
	uint32_t state[64] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
	uint32_t key[80] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	int bit;
	enc(key, state);
	for(bit = 0; bit < 64; bit++)	{
		sput_fail_unless(state[bit] == exp_res[bit],"present Test 1");
	}
}

void present_test_4()	{
	uint32_t exp_res[64] = {0,1,0,0,1,0,1,1,0,0,0,0,1,0,0,0,0,1,0,0,1,1,0,0,1,0,0,0,0,1,0,0,1,1,0,0,1,0,1,1,0,0,1,1,1,0,1,1,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0};
	uint32_t state[64] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
	uint32_t key[80] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
	int bit;
	enc(key, state);
	for(bit = 0; bit < 64; bit++)	{
		sput_fail_unless(state[bit] == exp_res[bit],"present Test 1");
	}
}
