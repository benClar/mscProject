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
	sput_finish_testing();
}

void run_tests()	{
	run_lib_tests();
	run_PRINCE_tests();
}

void test_gen_block_matrix()	{
	uint8_t **M = malloc(4 * sizeof(uint8_t*));
	M = gen_basic_blocks(M);
	int ele;
	sput_fail_unless(test_for_basic_m0(M[0]) == 1,"basic M blocks test");
	sput_fail_unless(test_for_basic_m1(M[1]) == 1,"basic M blocks test");
	sput_fail_unless(test_for_basic_m2(M[2]) == 1,"basic M blocks test");
	sput_fail_unless(test_for_basic_m3(M[3]) == 1,"basic M blocks test");
	sput_fail_unless(test_for_basic_m3(M[2]) == 0,"basic M blocks test");

	uint8_t *M_block_0 = gen_block_matrix(M,0);
	uint8_t *M_block_1 = gen_block_matrix(M,1);
	block_m_tester(M_block_0,0);
	block_m_tester(M_block_1,1);

	uint8_t *z_block = malloc(16 * 16 * sizeof(uint8_t*));
	for(ele = 0; ele < 256; ele++)	{
		z_block[ele] = 0;
	}
	uint8_t *test_block = malloc(16 * 16 * sizeof(uint8_t*));
	uint8_t *dia_matrix = gen_diagonal_matrix(M_block_0,M_block_1,z_block);
	memcpy(test_block,dia_matrix,256 * sizeof(uint8_t));
	block_m_tester(test_block,0);
	memcpy(test_block,&(dia_matrix[1280]),256 * sizeof(uint8_t));
	block_m_tester(test_block,1);
	memcpy(test_block,&(dia_matrix[2560]),256 * sizeof(uint8_t));
	block_m_tester(test_block,1);
	memcpy(test_block,&(dia_matrix[3840]),256 * sizeof(uint8_t));
	block_m_tester(test_block,0);
}

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
