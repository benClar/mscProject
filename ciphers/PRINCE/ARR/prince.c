/*---------- Standard Headers -----------*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
/*---------- Custom Headers	-----------*/

#include "prince.h"
#include "sput.h"


int main(){
	if(TESTING)	{
		run_tests();
	} else	{
		run();
	}
}

void run()	{
	uint8_t key_0[64] = {KEY_SEED64, KEY_SEED63, KEY_SEED62, KEY_SEED61, KEY_SEED60, KEY_SEED59, KEY_SEED58, KEY_SEED57, KEY_SEED56, KEY_SEED55, KEY_SEED54, KEY_SEED53, KEY_SEED52,
				KEY_SEED51, KEY_SEED50, KEY_SEED49, KEY_SEED48, KEY_SEED47, KEY_SEED46, KEY_SEED45, KEY_SEED44, KEY_SEED43, KEY_SEED42, KEY_SEED41, KEY_SEED40,
				KEY_SEED39, KEY_SEED38, KEY_SEED37, KEY_SEED36, KEY_SEED35, KEY_SEED34, KEY_SEED33, KEY_SEED32, KEY_SEED31, KEY_SEED30, KEY_SEED29, KEY_SEED28,
				KEY_SEED27, KEY_SEED26, KEY_SEED25, KEY_SEED24, KEY_SEED23, KEY_SEED22, KEY_SEED21, KEY_SEED20, KEY_SEED19, KEY_SEED18, KEY_SEED17, KEY_SEED16,
				KEY_SEED15, KEY_SEED14, KEY_SEED13, KEY_SEED12, KEY_SEED11, KEY_SEED10, KEY_SEED9, KEY_SEED8, KEY_SEED7, KEY_SEED6, KEY_SEED5, KEY_SEED4,
				KEY_SEED3, KEY_SEED2, KEY_SEED0};

	uint8_t key_1[64] = {KEY_SEED127, KEY_SEED126, KEY_SEED125, KEY_SEED124, KEY_SEED123, KEY_SEED122, KEY_SEED121, KEY_SEED120, KEY_SEED119, KEY_SEED118, KEY_SEED117, KEY_SEED116,
				KEY_SEED115, KEY_SEED114, KEY_SEED113, KEY_SEED112, KEY_SEED111, KEY_SEED110, KEY_SEED109, KEY_SEED108, KEY_SEED107, KEY_SEED106, KEY_SEED105, KEY_SEED104,
				KEY_SEED103, KEY_SEED102, KEY_SEED101, KEY_SEED100, KEY_SEED99, KEY_SEED98, KEY_SEED97, KEY_SEED96, KEY_SEED95, KEY_SEED94, KEY_SEED93, KEY_SEED92,
				KEY_SEED91, KEY_SEED90, KEY_SEED89, KEY_SEED88, KEY_SEED87, KEY_SEED86, KEY_SEED85, KEY_SEED84, KEY_SEED83, KEY_SEED82, KEY_SEED81, KEY_SEED80,
				KEY_SEED79, KEY_SEED78, KEY_SEED77, KEY_SEED76, KEY_SEED75, KEY_SEED74, KEY_SEED73, KEY_SEED72, KEY_SEED71, KEY_SEED70, KEY_SEED69, KEY_SEED68,
				KEY_SEED67, KEY_SEED66, KEY_SEED65, KEY_SEED64};

	uint8_t *key_0_not = XOR(rotate_right(key_0,64,1),shift_right(key_0,64,63),64);
	uint8_t **RC = (uint8_t**) malloc(12 * sizeof(uint8_t*));

	RC[0] = bitslice(RC_0,64);
	RC[1] = bitslice(RC_1,64);
	RC[2] = bitslice(RC_2,64);
	RC[3] = bitslice(RC_3,64);
	RC[4] = bitslice(RC_4,64);
	RC[5] = bitslice(RC_5,64);
	RC[6] = bitslice(RC_6,64);
	RC[7] = bitslice(RC_7,64);
	RC[8] = bitslice(RC_8,64);
	RC[9] = bitslice(RC_9,64);
	RC[10] = bitslice(RC_10,64);
	RC[11] = bitslice(RC_11,64);

	uint8_t **M = gen_basic_blocks();
}

uint8_t **gen_basic_blocks(uint8_t **M)	{

	uint8_t *M_0 = malloc(16 * sizeof(uint8_t));
	uint8_t *M_1 = malloc(16 * sizeof(uint8_t));
	uint8_t *M_2 = malloc(16 * sizeof(uint8_t));
	uint8_t *M_3 = malloc(16 * sizeof(uint8_t));

	M_0[0] = M0_0; 
	M_0[1] = M0_1;
	M_0[2] = M0_2; 
	M_0[3] = M0_3;
	M_0[4] = M0_4;
	M_0[5] = M0_5;
	M_0[6] = M0_6;
	M_0[7] = M0_7;
	M_0[8] = M0_8;
	M_0[9] = M0_9;
	M_0[10] = M0_10;
	M_0[11] = M0_11;
	M_0[12] = M0_12;
	M_0[13] = M0_13;
	M_0[14] = M0_14;
	M_0[15] = M0_15;

	M_1[0] = M1_0; 
	M_1[1] = M1_1;
	M_1[2] = M1_2; 
	M_1[3] = M1_3;
	M_1[4] = M1_4;
	M_1[5] = M1_5;
	M_1[6] = M1_6;
	M_1[7] = M1_7;
	M_1[8] = M1_8;
	M_1[9] = M1_9;
	M_1[10] = M1_10;
	M_1[11] = M1_11;
	M_1[12] = M1_12;
	M_1[13] = M1_13;
	M_1[14] = M1_14;
	M_1[15] = M1_15;

	M_2[0] = M2_0; 
	M_2[1] = M2_1;
	M_2[2] = M2_2; 
	M_2[3] = M2_3;
	M_2[4] = M2_4;
	M_2[5] = M2_5;
	M_2[6] = M2_6;
	M_2[7] = M2_7;
	M_2[8] = M2_8;
	M_2[9] = M2_9;
	M_2[10] = M2_10;
	M_2[11] = M2_11;
	M_2[12] = M2_12;
	M_2[13] = M2_13;
	M_2[14] = M2_14;
	M_2[15] = M2_15;

	M_3[0] = M3_0; 
	M_3[1] = M3_1;
	M_3[2] = M3_2; 
	M_3[3] = M3_3;
	M_3[4] = M3_4;
	M_3[5] = M3_5;
	M_3[6] = M3_6;
	M_3[7] = M3_7;
	M_3[8] = M3_8;
	M_3[9] = M3_9;
	M_3[10] = M3_10;
	M_3[11] = M3_11;
	M_3[12] = M3_12;
	M_3[13] = M3_13;
	M_3[14] = M3_14;
	M_3[15] = M3_15;

	M[0] = M_0;
	M[1] = M_1;
	M[2] = M_2;
	M[3] = M_3;

	return M;
}

uint8_t*** gen_diagonal_matrix(uint8_t **M_block_0, uint8_t **M_block_1, uint8_t **zero)	{
	int row, col;
	uint8_t ***M_64 = malloc(M64_AREA * sizeof(uint8_t**));
	for(row = 0; row < M64_LNGTH; row++)	{
		for(col = 0; col < M64_WIDTH; col++)	{
			if(col == row)	{
				if(row == 0 || row == 3)	{
					M_64[(row * M64_WIDTH) + col] = clone_square_matrix(M_block_0,BLOCK_M_SIZE,BASIC_BLOCK_ELE);
				} else if (row == 1 || row == 2)	{
					M_64[(row * M64_WIDTH) + col] = clone_square_matrix(M_block_1,BLOCK_M_SIZE,BASIC_BLOCK_ELE);
				}
			} else	{
				M_64[(row* M64_WIDTH) + col] = clone_square_matrix(zero,BLOCK_M_SIZE,BASIC_BLOCK_ELE);
			}
		}
	}
	return M_64;	
}

uint8_t** gen_block_matrix(uint8_t **m_blocks, int start) {
	int row, col, m = start;
	uint8_t **output = malloc(16 * sizeof(uint8_t*));
	for(row = 0; row < BLOCK_M_SIZE; row++)	{
		for(col = 0; col < BLOCK_M_SIZE; col++)	{
			// print_array(m_blocks[m],16);
			output[(row * BLOCK_M_SIZE) + col] = clone(m_blocks[m],16);
			m = (m + 1) % BLOCK_M_SIZE;
		}
		m = (m + 1) % BLOCK_M_SIZE;
		// printf("\n");
	}
	return output;
}

uint8_t* sBox(uint8_t *input)	{
	uint8_t *output = (uint8_t*) malloc(4*sizeof(uint8_t));
	output[0] = sbox_1(input);
	output[1] = sbox_2(input);
	output[2] = sbox_3(input);
	output[3] = sbox_4(input);
	return output;
}

uint8_t sbox_1(uint8_t *input)	{
	return (((~input[A] & ~input[C]) | (input[B] & ~input[D]) | (input[A] & input[C] & ~input[D])) & 1);
}

uint8_t sbox_2(uint8_t *input)	{
	return (((input[A] & input[B]) | (~input[C] & input[D]) | (input[A] & ~input[C])) & 1);
}

uint8_t sbox_3(uint8_t *input)	{
	return (((~input[A] & ~input[B]) | (~input[C] & ~input[D]) |(~input[A] & ~input[D]) | (~input[B] & ~input[C])) & 1);
}

uint8_t sbox_4(uint8_t *input)	{
	return (((input[B] & input[C]) | (input[A] & ~input[C] & input[D]) | (~input[A] & ~input[B] & ~input[C]) | (~input[A] & ~input[B] & ~input[D])) & 1);
}


