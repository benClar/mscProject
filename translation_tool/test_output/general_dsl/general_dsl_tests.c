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
	sput_enter_suite("Int operations tests");
	sput_run_test(general_test_8);
	sput_enter_suite("Int operations tests");
	sput_run_test(general_test_9);
	sput_enter_suite("Int operations tests");
	sput_run_test(general_test_10);
	sput_enter_suite("Int operations tests");
	sput_run_test(general_test_11);
	sput_enter_suite("Int operations tests");
	sput_run_test(general_test_12);
	sput_enter_suite("Int operations tests");
	sput_run_test(general_test_13);
	sput_enter_suite("Int operations tests");
	sput_run_test(general_test_14);
	sput_enter_suite("Int operations tests");
	sput_run_test(general_test_15);
	sput_enter_suite("bit seq operations tests");
	sput_run_test(bit_seq_extraction_test_16);
	sput_enter_suite("bit seq operations tests");
	sput_run_test(bit_seq_arith_test_17);
	sput_enter_suite("bit seq operations tests");
	sput_run_test(bs_seq_mult_test_18);
	sput_enter_suite("bit seq operations tests");
	sput_run_test(bs_bit_cast_test_19);
	sput_enter_suite("bit seq operations tests");
	sput_run_test(bit_seq_expr_bs_test_20);
	sput_enter_suite("bit seq operations tests");
	sput_run_test(bit_seq_expr_21);
	sput_enter_suite("bit seq operations tests");
	sput_run_test(bit_seq_expr_arith_test_22);
	sput_enter_suite("bit seq operations tests");
	sput_run_test(bs_bit_mult_23);
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
	sput_fail_unless(int_index_set_6()  == 14,"General Test 6");
}

void general_test_7()	{
	sput_fail_unless(int_index_set_7()  == 11,"General Test 7");
}

void general_test_8()	{
	sput_fail_unless(int_index_set_8()  == 11,"General Test 8");
}

void general_test_9()	{
	sput_fail_unless(int_index_set_9()  == 21,"General Test 9");
}

void general_test_10()	{
	sput_fail_unless(int_index_set_10()  == 17,"General Test 10");
}

void general_test_11()	{
	sput_fail_unless(int_index_set_11()  == 14,"General Test 11");
}

void general_test_12()	{
	sput_fail_unless(int_index_set_12()  == 14,"General Test 12");
}

void general_test_13()	{
	sput_fail_unless(int_index_set_13()  == 15,"General Test 13");
}

void general_test_14()	{
	uint32_t expected[8] = {0,1,0,1,0,1,1};
	uint32_t res[8] = {0};
	bs_arith_add(res);
	for(int slice = 0; slice < 32; slice++)	{
		for(int bit = 0; bit < 8; bit++)	{
			sput_fail_unless(((res[bit] >> slice) & 0x1) == expected[bit],"General Test 14");		
		}
		printf("\n");
	}
}

void general_test_15()	{
	uint32_t expected[8] = {1,1,0,0,0,1,0,0};
	uint32_t res[8] = {0};
	bs_arith_sub(res);
	for(int slice = 0; slice < 32; slice++)	{
		for(int bit = 0; bit < 8; bit++)	{
			sput_fail_unless(((res[bit] >> slice) & 0x1) == expected[bit],"General Test 15");		
		}
		printf("\n");
	}
}

void bit_seq_extraction_test_16(){
	uint8_t input[2] = {0};
	seq_bit_extraction(input);
	sput_fail_unless(input[0] == 2,"Seq Bit Test 16");	
	sput_fail_unless(input[1] == 3,"Seq bit Test 16");	
}

void bit_seq_arith_test_17()	{
	sput_fail_unless(seq_bit_arth() == 16, "Seq Bit test 17");
}

void bs_seq_mult_test_18()	{
	uint32_t expected[32] = {0,0,0xffffffff,0xffffffff,0xffffffff,0xffffffff,0,0xffffffff,0,0,0,0,0xffffffff,0xffffffff,0xffffffff,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t res[32] = {0};
	bs_mult_sub(res);
	for(int bit = 0; bit < 32; bit++)	{
		sput_fail_unless(res[bit] ==  expected[bit], "Seq Bit test 18");
	}
}

void bs_bit_cast_test_19()	{
	uint32_t output[8] = {0};
	bs_bit_expr_cast(output);
	sput_fail_unless(output[0] == 0xffffffff, "Bit cast 19");
}

void bit_seq_expr_bs_test_20()	{
	uint32_t output[8] = {0};
	bit_seq_expr_to_bs(output);
	sput_fail_unless(output[0] == 0, "Bit cast 20");
	sput_fail_unless(output[1] == 0xffffffff, "Bit cast 20");
	sput_fail_unless(output[2] == 0xffffffff, "Bit cast 20");
	sput_fail_unless(output[3] == 0xffffffff, "Bit cast 20");
}

void bit_seq_expr_21()	{
	sput_fail_unless(bit_seq_expr_rotate() == 3, "Bit seq expr 21");
}

void bit_seq_expr_arith_test_22()	{
	sput_fail_unless(bit_seq_expr_arith() == 14, "Bit seq expr 22");
}

void bs_bit_mult_23()	{
	uint32_t output[8] = {0};
	bs_seq_bit_expr_mult(output);
	sput_fail_unless(output[0] == 0x0, "bs bit expr 23");
	sput_fail_unless(output[1] == 0xffffffff, "bs bit expr 23");
	sput_fail_unless(output[2] == 0xffffffff, "bs bit expr 23");
	sput_fail_unless(output[3] == 0x0, "bs bit expr 23");
	sput_fail_unless(output[4] == 0x0, "bs bit expr 23");
	sput_fail_unless(output[5] == 0x0, "bs bit expr 23");
	sput_fail_unless(output[6] == 0x0, "bs bit expr 23");
	sput_fail_unless(output[7] == 0x0, "bs bit expr 23");
}
