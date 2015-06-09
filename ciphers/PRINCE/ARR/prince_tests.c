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
	int row, col;
	sput_fail_unless(test_for_basic_m0(M[0]) == 1,"basic M blocks test");
	sput_fail_unless(test_for_basic_m1(M[1]) == 1,"basic M blocks test");
	sput_fail_unless(test_for_basic_m2(M[2]) == 1,"basic M blocks test");
	sput_fail_unless(test_for_basic_m3(M[3]) == 1,"basic M blocks test");
	sput_fail_unless(test_for_basic_m3(M[2]) == 0,"basic M blocks test");
	uint8_t **M_block_0 = gen_block_matrix(M,0);
	uint8_t **M_block_1 = gen_block_matrix(M,1);
	// block_m_tester(M_block_0,0);
	// block_m_tester(M_block_1,1);

	uint8_t **z_blocks = malloc(4 * sizeof(uint8_t*));
	uint8_t z_var[4] = {0,0,0,0};
	for(row = 0; row < 4; row++)	{
		for(col = 0; col < 4; col++)	{
			z_blocks[row] = clone(z_var,4);
		}
	}
	

	uint8_t **Z_block = gen_block_matrix(z_blocks,0);
	uint8_t ***dia_matrix = gen_diagonal_matrix(M_block_0,M_block_1,Z_block);
	block_m_tester(dia_matrix[0],0);
	block_m_tester(dia_matrix[5],1);
	block_m_tester(dia_matrix[10],1);
	block_m_tester(dia_matrix[15],0);
	// print_sq_matrix(dia_matrix[0],16);
}

void block_m_tester(uint8_t **M_block, int start)	{
	int row, col, m = start;
	for(row = 0; row < BLOCK_M_SIZE; row++)	{
		for(col = 0; col < BLOCK_M_SIZE; col++)	{
			switch(m)	{
				case 0:
					sput_fail_unless(test_for_basic_m0(M_block[(row * BLOCK_M_SIZE) + col]) == 1,"basic M blocks test");
					break;
				case 1:
					sput_fail_unless(test_for_basic_m1(M_block[(row * BLOCK_M_SIZE) + col]) == 1,"basic M blocks test");
					break;
				case 2:
					sput_fail_unless(test_for_basic_m2(M_block[(row * BLOCK_M_SIZE) + col]) == 1,"basic M blocks test");
					break;
				case 3:
					sput_fail_unless(test_for_basic_m3(M_block[(row * BLOCK_M_SIZE) + col]) == 1,"basic M blocks test");
					break;
			}
			m = (m + 1) % BLOCK_M_SIZE;
		}
		m = (m + 1) % BLOCK_M_SIZE;
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
