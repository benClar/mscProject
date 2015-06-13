/*---------- Standard Headers -----------*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

/*---------- Custom Headers	-----------*/

#include "prince_tests.h"
#include "sput.h"


void run_PRINCE_tests()	{
	sput_start_testing();
	sput_enter_suite("Test gen_block_matrix");
	sput_run_test(test_gen_block_matrix);
	sput_enter_suite("Sbox tests");
	sput_run_test(sbox_tests);
	sput_finish_testing();
}

void run_tests()	{
	run_lib_tests();
	run_PRINCE_tests();
}

void sbox_tests()	{
	uint8_t *input = malloc(4 * sizeof(uint8_t));
	input[0] = 1;
	input[1] = 0;
	input[2] = 0;
	input[3] = 0;
	input = sBox_nibble(input,0);
	sput_fail_unless(input[0] == 0,"Sbox tests");
	sput_fail_unless(input[1] == 1,"Sbox tests");
	sput_fail_unless(input[2] == 1,"Sbox tests");
	sput_fail_unless(input[3] == 0,"Sbox tests");
	input[0] = 0;
	input[1] = 0;
	input[2] = 0;
	input[3] = 0;
	input = sBox_nibble(input,1);
	sput_fail_unless(input[0] == 1,"Sbox tests - 0");
	sput_fail_unless(input[1] == 0,"Sbox tests");
	sput_fail_unless(input[2] == 1,"Sbox tests");
	sput_fail_unless(input[3] == 1,"Sbox tests");

	input[0] = 0;
	input[1] = 0;
	input[2] = 0;
	input[3] = 1;

	input = sBox_nibble(input,1);
	sput_fail_unless(input[0] == 0,"Sbox tests - 1");
	sput_fail_unless(input[1] == 1,"Sbox tests");
	sput_fail_unless(input[2] == 1,"Sbox tests");
	sput_fail_unless(input[3] == 1,"Sbox tests");

	input[0] = 0;
	input[1] = 0;
	input[2] = 1;
	input[3] = 0;
	input = sBox_nibble(input,1);
	sput_fail_unless(input[0] == 0,"Sbox tests - 2");
	sput_fail_unless(input[1] == 0,"Sbox tests");
	sput_fail_unless(input[2] == 1,"Sbox tests");
	sput_fail_unless(input[3] == 1,"Sbox tests");

	input[0] = 0;
	input[1] = 0;
	input[2] = 1;
	input[3] = 1;
	input = sBox_nibble(input,1);
	sput_fail_unless(input[0] == 0,"Sbox tests - 3");
	sput_fail_unless(input[1] == 0,"Sbox tests");
	sput_fail_unless(input[2] == 1,"Sbox tests");
	sput_fail_unless(input[3] == 0,"Sbox tests");

	input[0] = 0;
	input[1] = 1;
	input[2] = 0;
	input[3] = 0;
	input = sBox_nibble(input,1);
	sput_fail_unless(input[0] == 1,"Sbox tests - 4");
	sput_fail_unless(input[1] == 1,"Sbox tests");
	sput_fail_unless(input[2] == 1,"Sbox tests");
	sput_fail_unless(input[3] == 1,"Sbox tests");

	input[0] = 0;
	input[1] = 1;
	input[2] = 0;
	input[3] = 1;
	input = sBox_nibble(input,1);
	sput_fail_unless(input[0] == 1,"Sbox tests - 5");
	sput_fail_unless(input[1] == 1,"Sbox tests");
	sput_fail_unless(input[2] == 0,"Sbox tests");
	sput_fail_unless(input[3] == 1,"Sbox tests");

	input[0] = 0;
	input[1] = 1;
	input[2] = 1;
	input[3] = 0;
	input = sBox_nibble(input,1);
	sput_fail_unless(input[0] == 1,"Sbox tests - 6");
	sput_fail_unless(input[1] == 0,"Sbox tests");
	sput_fail_unless(input[2] == 0,"Sbox tests");
	sput_fail_unless(input[3] == 0,"Sbox tests");

	input[0] = 0;
	input[1] = 1;
	input[2] = 1;
	input[3] = 1;
	input = sBox_nibble(input,1);
	sput_fail_unless(input[0] == 1,"Sbox tests - 7");
	sput_fail_unless(input[1] == 0,"Sbox tests");
	sput_fail_unless(input[2] == 0,"Sbox tests");
	sput_fail_unless(input[3] == 1,"Sbox tests");

	input[0] = 1;
	input[1] = 0;
	input[2] = 0;
	input[3] = 0;
	input = sBox_nibble(input,1);
	sput_fail_unless(input[0] == 1,"Sbox tests - 8");
	sput_fail_unless(input[1] == 0,"Sbox tests");
	sput_fail_unless(input[2] == 1,"Sbox tests");
	sput_fail_unless(input[3] == 0,"Sbox tests");

	input[0] = 1;
	input[1] = 0;
	input[2] = 0;
	input[3] = 1;
	input = sBox_nibble(input,1);
	sput_fail_unless(input[0] == 0,"Sbox tests - 9");
	sput_fail_unless(input[1] == 1,"Sbox tests");
	sput_fail_unless(input[2] == 1,"Sbox tests");
	sput_fail_unless(input[3] == 0,"Sbox tests");

	input[0] = 1;
	input[1] = 0;
	input[2] = 1;
	input[3] = 0;
	input = sBox_nibble(input,1);
	sput_fail_unless(input[0] == 0,"Sbox tests - 10");
	sput_fail_unless(input[1] == 1,"Sbox tests");
	sput_fail_unless(input[2] == 0,"Sbox tests");
	sput_fail_unless(input[3] == 0,"Sbox tests");

	input[0] = 1;
	input[1] = 0;
	input[2] = 1;
	input[3] = 1;
	input = sBox_nibble(input,1);
	sput_fail_unless(input[0] == 0,"Sbox tests - 11");
	sput_fail_unless(input[1] == 0,"Sbox tests");
	sput_fail_unless(input[2] == 0,"Sbox tests");
	sput_fail_unless(input[3] == 0,"Sbox tests");

	input[0] = 1;
	input[1] = 1;
	input[2] = 0;
	input[3] = 0;
	input = sBox_nibble(input,1);
	sput_fail_unless(input[0] == 0,"Sbox tests - 12");
	sput_fail_unless(input[1] == 1,"Sbox tests ");
	sput_fail_unless(input[2] == 0,"Sbox tests");
	sput_fail_unless(input[3] == 1,"Sbox tests");

	input[0] = 1;
	input[1] = 1;
	input[2] = 0;
	input[3] = 1;
	input = sBox_nibble(input,1);
	sput_fail_unless(input[0] == 1,"Sbox tests - 13");
	sput_fail_unless(input[1] == 1,"Sbox tests");
	sput_fail_unless(input[2] == 1,"Sbox tests");
	sput_fail_unless(input[3] == 0,"Sbox tests");

	input[0] = 1;
	input[1] = 1;
	input[2] = 1;
	input[3] = 0;
	input = sBox_nibble(input,1);
	sput_fail_unless(input[0] == 1,"Sbox tests - 14");
	sput_fail_unless(input[1] == 1,"Sbox tests");
	sput_fail_unless(input[2] == 0,"Sbox tests");
	sput_fail_unless(input[3] == 0,"Sbox tests");
	input[0] = 1;
	input[1] = 1;
	input[2] = 1;
	input[3] = 1;
	input = sBox_nibble(input,1);
	sput_fail_unless(input[0] == 0,"Sbox tests - 15");
	sput_fail_unless(input[1] == 0,"Sbox tests");
	sput_fail_unless(input[2] == 0,"Sbox tests");
	sput_fail_unless(input[3] == 1,"Sbox tests");
}

void test_gen_block_matrix()	{
	uint8_t **M = malloc(4 * sizeof(uint8_t*));
	M = gen_basic_blocks(M);
	// int ele,row,col, matrix;
	sput_fail_unless(test_for_basic_m0(M[0]) == 1,"basic M blocks test");
	sput_fail_unless(test_for_basic_m1(M[1]) == 1,"basic M blocks test");
	sput_fail_unless(test_for_basic_m2(M[2]) == 1,"basic M blocks test");
	sput_fail_unless(test_for_basic_m3(M[3]) == 1,"basic M blocks test");
	sput_fail_unless(test_for_basic_m3(M[2]) == 0,"basic M blocks test");

	// uint8_t *M_block_0 = gen_block_matrix(M,0);
	// uint8_t *M_block_1 = gen_block_matrix(M,1);

	// uint8_t *z_block = malloc(16 * 16 * sizeof(uint8_t*));
	// for(ele = 0; ele < 256; ele++)	{
	// 	z_block[ele] = 0;
	// }
	// uint8_t *dia_m_prime = gen_diagonal_matrix(M_block_0,M_block_1,z_block);

	// uint8_t *dia__m = shift_rows(dia_m_prime);
	// for(ele = 0; ele < 64 * 64;){
	// 	for(matrix = 0; matrix < 4; matrix++)	{
	// 		for(col = 0; col < 16; col++,ele++)	{
	// 			printf("%d", dia_matrix[ele]);
	// 		}
	// 		printf(" ");
	// 	}
	// 	printf("\n");
	// }
}

/*Doesnt work with new blocks*/
void block_m_tester(uint8_t *M_block, int start)	{
	int ele, col, m = start;
	uint8_t *test_M = malloc(16 * sizeof(uint8_t));
	for(ele = 0; ele < 256;)	{
		for(col = 0; col < 4; col++,ele+=16){
			memcpy(test_M,&(M_block[ele]),16 * sizeof(uint8_t));
			switch(m)	{
				case 0:
					sput_fail_unless(test_for_basic_m0(test_M) == 1,"M block test");
					break;
				case 1:
					sput_fail_unless(test_for_basic_m1(test_M) == 1,"M block test");
					break;
				case 2:
					sput_fail_unless(test_for_basic_m2(test_M) == 1,"M block test");
					break;
				case 3:
					sput_fail_unless(test_for_basic_m3(test_M) == 1,"M block test");
					break;
			}
			m = (m + 1) % BASIC_BLOCK_NUM;
		}
		m = (m + 1) % BASIC_BLOCK_NUM;
	}
}

int test_for_basic_m0(uint8_t *m)	{
	uint8_t row_1[4] = {0,0,0,0};
	uint8_t row_2[4] = {0,1,0,0};
	uint8_t row_3[4] = {0,0,1,0};
	uint8_t row_4[4] = {0,0,0,1};
	uint8_t *test_rows[4] = {row_1,row_2,row_3,row_4};
	int row,col;

	for(row = 0; row < 4; row++)	{
		for (col = 0; col < 4; col++)	{
			if(m[4 * row + col] != test_rows[row][col])	{
				return 0;
			}
		}
	}
	return 1;
}

int test_for_basic_m1(uint8_t *m)	{
	uint8_t row_1[4] = {1,0,0,0};
	uint8_t row_2[4] = {0,0,0,0};
	uint8_t row_3[4] = {0,0,1,0};
	uint8_t row_4[4] = {0,0,0,1};
	uint8_t *test_rows[4] = {row_1,row_2,row_3,row_4};
	int row,col;

	for(row = 0; row < 4; row++)	{
		for (col = 0; col < 4; col++)	{
			if(m[4 * row + col] != test_rows[row][col])	{
				return 0;
			}
		}
	}
	return 1;
}

int test_for_basic_m2(uint8_t *m)	{
	uint8_t row_1[4] = {1,0,0,0};
	uint8_t row_2[4] = {0,1,0,0};
	uint8_t row_3[4] = {0,0,0,0};
	uint8_t row_4[4] = {0,0,0,1};
	uint8_t *test_rows[4] = {row_1,row_2,row_3,row_4};
	int row,col;

	for(row = 0; row < 4; row++)	{
		for (col = 0; col < 4; col++)	{
			if(m[4 * row + col] != test_rows[row][col])	{
				return 0;
			}
		}
	}
	return 1;
}

int test_for_basic_m3(uint8_t *m)	{
	uint8_t row_1[4] = {1,0,0,0};
	uint8_t row_2[4] = {0,1,0,0};
	uint8_t row_3[4] = {0,0,1,0};
	uint8_t row_4[4] = {0,0,0,0};
	uint8_t *test_rows[4] = {row_1,row_2,row_3,row_4};
	int row,col;

	for(row = 0; row < 4; row++)	{
		for (col = 0; col < 4; col++)	{
			if(m[4 * row + col] != test_rows[row][col])	{
				return 0;
			}
		}
	}
	return 1;
}
