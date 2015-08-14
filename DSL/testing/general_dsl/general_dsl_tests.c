#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "general_dsl_tests.h"
#include "general_dsl.h"

int main() {
	sput_start_testing();
	sput_enter_suite("Int operations tests");
	sput_run_test(general_test_1);
	sput_enter_suite("Int operations tests");
	sput_run_test(general_test_2);
	sput_enter_suite("Int operations tests");
	sput_run_test(general_test_3);
	sput_enter_suite("Int operations tests");
	sput_run_test(general_test_4);	
	sput_enter_suite("Int operations tests");
	sput_run_test(general_test_5);
	sput_enter_suite("Int operations tests");
	sput_run_test(general_test_6);
	sput_enter_suite("Int operations tests");
	sput_run_test(general_test_7);
	sput_finish_testing();
	return sput_get_return_value();
}


void general_test_1()	{
	sput_fail_unless(int_index_set_1() == 2,"General Test 1");
}

void general_test_2()	{
	sput_fail_unless(int_index_set_2() == 9,"General Test 2");
}

void general_test_3()	{
	sput_fail_unless(int_index_set_3() == 10,"General Test 3");
}

void general_test_4()	{
	sput_fail_unless(int_index_set_4() == 10,"General Test 4");
}

void general_test_5()	{
	sput_fail_unless(int_index_set_5()  == 14,"General Test 5");
}

void general_test_6()	{
	sput_fail_unless(int_index_set_6()  == 14,"General Test 5");
}

void general_test_7()	{
	sput_fail_unless(int_index_set_7()  == 11,"General Test 5");
}
