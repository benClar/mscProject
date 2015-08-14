#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "present_tests.h"

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

	uint32_t exp_res[64] = {1,1,1,0,0,1,1,1,0,0,1,0,1,1,0,0,0,1,0,0,0,1,1,0,1,1,0,0,0,0,0,0,1,1,1,1,0,1,0,1,1,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,1,0,0,1};
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key[80] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
	int bit;
	int slice;

	clock_t start, end, result = 0;

	for(int run = 0; run < 100000; run++)	{
		start = mach_absolute_time();
		enc(key, state);
		end = mach_absolute_time();
		result += (end - start);
		for(bit = 0; bit < 64; bit++)	{
			state[bit] = 0;
		}
		for(bit = 0; bit < 80; bit++)	{
			key[bit] = 0xffffffff;
		}
	}
	printf("%lu\n", result / 100000);

	// end = clock();
	// cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
	// printf("cpu time used : %f \n", cpu_time_used);

}

void present_test_2()	{
	uint32_t exp_res[64] = {0,1,0,1,0,1,0,1,0,1,1,1,1,0,0,1,1,1,0,0,0,0,0,1,0,0,1,1,1,0,0,0,0,1,1,1,1,0,1,1,0,0,1,0,0,0,1,0,1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,1};
	uint32_t state[64] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t key[80] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	int bit;
	enc(key, state);
	for(bit = 0; bit < 64; bit++)	{
		sput_fail_unless(state[bit] == exp_res[bit],"present Test 2");
	}
}

void present_test_3()	{
	uint32_t exp_res[64] = {1,0,1,0,0,0,0,1,0,0,0,1,0,0,1,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,0,0,1,0,1,1,1,1,0,1,1,0,1,0,0,0,0,1,0,0,0,0,0,1,0,1,1,1,1,0,1,1};
	uint32_t state[64] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
	uint32_t key[80] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	int bit;
	enc(key, state);
	for(bit = 0; bit < 64; bit++)	{
		sput_fail_unless(state[bit] == exp_res[bit],"present Test 3");
	}
}

void present_test_4()	{
	uint32_t exp_res[64] = {0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,1,1,0,1,1,1,0,0,1,1,0,1,0,0,1,1,0,0,1,0,0,0,0,1,0,0,1,1,0,0,1,0,0,0,0,1,0,0,0,0,1,1,0,1,0,0,1,0};
	uint32_t state[64] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
	uint32_t key[80] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
	int bit;
	enc(key, state);
	for(bit = 0; bit < 64; bit++)	{
		sput_fail_unless(state[bit] == exp_res[bit],"present Test 4");
	}
}
