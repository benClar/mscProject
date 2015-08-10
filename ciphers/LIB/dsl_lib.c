/*---------- Standard Headers -----------*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
/*---------- Custom Headers	-----------*/

#include "dsl_lib.h"
#include "sput.h"


void extract_bs_range(uint8_t *target, uint8_t *source, int start, int finish)	{
	int i;
	for(i = 0; start <= finish; start++)	{
		target[i] = source[start];
	}
}

/*Assumes nibble size of 4*/
void hex_print(uint8_t *state, int row_width, int area)	{

	char hex_lookup[16] = {'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};
	int row, nibble, lookup = 0,bit;
	for(row = 0; row < area/row_width; row++)	{
		for(nibble = 0; nibble < row_width / 4; nibble++)	{
			for(bit = 0; bit < 4; bit++)	{
				lookup = (lookup << 1) ^ state[array_position(row,(nibble * 4) + bit, row_width)];

			}
			printf("%c ",hex_lookup[lookup]);
			lookup = 0;
		}
		printf("\n");
	}

}

uint8_t *rotate_left(uint8_t *input, int var_size ,int shift)    {
	uint8_t *input_copy = clone(input,var_size);
    reverse(input_copy, 0, var_size - 1);
    reverse(input_copy, 0, var_size - shift - 1);
    reverse(input_copy, var_size - shift, var_size - 1);
    return input_copy;
}

uint8_t *bitslice(long var, int var_size)	{
	uint8_t* bs = malloc(var_size * sizeof(uint8_t));
	int bit;
	for(bit = 0; bit < var_size; bit++)	{
		bs[var_size - bit - 1] = ((var >> bit) & 1);
	}
	return bs;
}

int bits_in(int value)	{
    int counter = 0;
    while(value) {
        counter += 1;
        value >>= 1;
    }
    return counter;	
}

void bits_in_test()	{
	sput_fail_unless(bits_in(10) == 4,"Bits_in_test");
	sput_fail_unless(bits_in(10000) == 14,"Bits_in_test");
}

uint8_t *rotate_right(uint8_t *input, int var_size ,int shift)    {
	uint8_t *input_copy = clone(input,var_size);
    reverse(input_copy, 0, var_size - 1);
    reverse(input_copy, 0, shift - 1);
    reverse(input_copy, shift, var_size - 1);
    return input_copy;
}

uint8_t *matrix_column(uint8_t *matrix, int col_width, int row_width, int col, int area)	{
	int t_row = area / row_width,row;
	uint8_t *output = malloc(t_row * (col_width * sizeof(uint8_t)));

	for(row = 0; row < t_row; row++)	{
		memcpy(&(output[array_position(row,0,col_width)]),&(matrix[array_position(row,col * col_width,row_width)]),col_width * sizeof(uint8_t)); 
	}
	return output;
}

int array_position(int curr_row, int curr_col, int row_width)	{
	return ((row_width * curr_row) + curr_col);
}

uint8_t *shift_right(uint8_t *input, int var_size ,int shift)	{
	uint8_t *input_copy = calloc(var_size, sizeof(uint8_t));
	memcpy(input_copy + shift,input,(var_size - shift) * sizeof(uint8_t));
	return input_copy;
}

uint8_t *shift_left(uint8_t *input, int var_size ,int shift)	{
	uint8_t *input_copy = calloc(var_size, sizeof(uint8_t));
	memcpy(input_copy,input + shift,(var_size - shift) * sizeof(uint8_t));
	return input_copy;
}

void shift_right_2(uint8_t *target, uint8_t *source, int var_size, int shift)	{
	memcpy(target + shift, source,(var_size - shift) * sizeof(uint8_t));
}

void shift_left_2(uint8_t *target, uint8_t *source, int var_size, int shift)	{
	memcpy(target, source + shift,(var_size - shift) * sizeof(uint8_t));
}

uint8_t *shift(uint8_t *input, int var_size, int shift, char *op)	{
	if(!strcmp(op, ">>")) {
		return shift_right(input, var_size, shift);
	} else if (!strcmp(op, "<<")) {
		return shift_left(input, var_size, shift);
	} else if (!strcmp(op, ">>>"))	{
		return rotate_right(input, var_size, shift);
	}else if (!strcmp(op, "<<<"))	{
		return rotate_left(input, var_size, shift);
	} else {
		log_err("Unrecognised shift operator");
	}
	return NULL;
}

uint8_t *clone(uint8_t *input, int var_size)	{
	uint8_t *input_copy = malloc(var_size * sizeof(uint8_t));
	memcpy(input_copy,input,var_size * sizeof(uint8_t));
	return input_copy;
}

uint8_t *reverse(uint8_t *array, int start, int end)	{
		while(start < end)	{
			int tmp = array[start];
			array[start] = array[end];
			array[end] = tmp;
			start++;
			end--;
		}	
		return array;
}

/* Only XORS to equal sized vars*/
uint8_t *XOR(uint8_t *a, uint8_t *b, int size)	{
	int bit;
	uint8_t *output = calloc(size,sizeof(uint8_t));
	for(bit = size - 1; bit >= 0; bit--)	{
		output[bit] = a[bit] ^ b[bit];
	}
	return output;
}

uint8_t *AND(uint8_t *a, uint8_t *b, int size)	{
	int bit;
	uint8_t *output = calloc(size,sizeof(uint8_t));
	for(bit = size -1; bit >= 0; bit--)	{
		output[bit] = a[bit] & b[bit];
	}
	return output;
}

int compare(uint8_t *a, uint8_t *b, int size)	{
	int ele;
	for(ele = 0; ele < size; ele++)	{
		if(a[ele] != b[ele])	{
			return 0;
		}
	}
	return 1;
}

void assign(uint8_t *array, int value)	{
	free(array);
	array = bitslice(value,bits_in(value));
}

void print_array(uint8_t *array,int size)	{
	int ele;
	for(ele = 0; ele < size; ele++)	{
		printf("%d", array[ele]);
	}
	printf("\n");
}

/*std implementation GF 24*/
uint8_t gm(uint8_t a, uint8_t b) {
  uint8_t g = 0;
  int i;
  for (i = 0; i < 4; i++) {
    if ( (b & 0x1) == 1 ) { 
        g ^= a;
    }
    uint8_t hbs = (a & 0x8);
    a <<= 0x1;
    if ( hbs == 0x8) { 
        a ^= GF_POLY;
    }
    b >>= 0x1;
  }

  return g;
}

/*testing*/
void run_lib_tests()	{
	sput_start_testing();
	sput_enter_suite("Test Rotate");
	sput_run_test(rotate_tests);
	sput_enter_suite("Test Shift");
	sput_run_test(shift_tests);
	sput_enter_suite("Test bitslice");
	sput_run_test(test_bitslice);
	sput_enter_suite("Test Matrix Column");
	sput_run_test(test_matrix_column);
	sput_enter_suite("Test Array Position Calculator");
	sput_run_test(test_array_position);
	sput_enter_suite("Bits In Test");
	sput_run_test(bits_in_test);
	sput_finish_testing();
}


void rotate_tests()	{
	uint8_t test_right[10] = {1,2,3,4,5,6,7,8,9,10};
	uint8_t test_left[10] = {1,2,3,4,5,6,7,8,9,10};
	uint8_t *result;
	result = rotate_right(test_right,10,3);
	sput_fail_unless(result[0] == 8,"rotate_right test");
	sput_fail_unless(result[1] == 9,"rotate_right test");
	sput_fail_unless(result[2] == 10,"rotate_right test");
	sput_fail_unless(result[3] == 1,"rotate_right test");
	sput_fail_unless(result[4] == 2,"rotate_right test");
	sput_fail_unless(result[5] == 3,"rotate_right test");
	sput_fail_unless(result[6] == 4,"rotate_right test");
	sput_fail_unless(result[7] == 5,"rotate_right test");
	sput_fail_unless(result[8] == 6,"rotate_right test");
	sput_fail_unless(result[9] == 7,"rotate_right test");

	result = rotate_left(test_left,10,3);
	sput_fail_unless(result[0] == 4,"rotate_left test");
	sput_fail_unless(result[1] == 5,"rotate_left test");
	sput_fail_unless(result[2] == 6,"rotate_left test");
	sput_fail_unless(result[3] == 7,"rotate_left test");
	sput_fail_unless(result[4] == 8,"rotate_left test");
	sput_fail_unless(result[5] == 9,"rotate_left test");
	sput_fail_unless(result[6] == 10,"rotate_left test");
	sput_fail_unless(result[7] == 1,"rotate_left test");
	sput_fail_unless(result[8] == 2,"rotate_left test");
	sput_fail_unless(result[9] == 3,"rotate_left test");
}

void shift_tests()	{
	uint8_t test_right[10] = {1,2,3,4,5,6,7,8,9,10};
	uint8_t test_left[10] = {1,2,3,4,5,6,7,8,9,10};
	uint8_t *result;
	result = shift_right(test_right,10,3);
	sput_fail_unless(result[0] == 0,"shift_right test");
	sput_fail_unless(result[1] == 0,"shift_right test");
	sput_fail_unless(result[2] == 0,"shift_right test");
	sput_fail_unless(result[3] == 1,"shift_right test");
	sput_fail_unless(result[4] == 2,"shift_right test");
	sput_fail_unless(result[5] == 3,"shift_right test");
	sput_fail_unless(result[6] == 4,"shift_right test");
	sput_fail_unless(result[7] == 5,"shift_right test");
	sput_fail_unless(result[8] == 6,"shift_right test");
	sput_fail_unless(result[9] == 7,"shift_right test");
	result = shift_left(test_left,10,3);
	sput_fail_unless(result[0] == 4,"shift_left test");
	sput_fail_unless(result[1] == 5,"shift_left test");
	sput_fail_unless(result[2] == 6,"shift_left test");
	sput_fail_unless(result[3] == 7,"shift_left test");
	sput_fail_unless(result[4] == 8,"shift_left test");
	sput_fail_unless(result[5] == 9,"shift_left test");
	sput_fail_unless(result[6] == 10,"shift_left test");
	sput_fail_unless(result[7] == 0,"shift_left test");
	sput_fail_unless(result[8] == 0,"shift_left test");
	sput_fail_unless(result[9] == 0,"shift_left test");
}

void test_bitslice()	{
	uint8_t *result = bitslice(15,4);	
	sput_fail_unless(result[0] == 1,"bitslice test");
	sput_fail_unless(result[1] == 1,"bitslice test");
	sput_fail_unless(result[2] == 1,"bitslice test");
	sput_fail_unless(result[3] == 1,"bitslice test");

	result = bitslice(10,4);
	sput_fail_unless(result[0] == 1,"bitslice test");
	sput_fail_unless(result[1] == 0,"bitslice test");
	sput_fail_unless(result[2] == 1,"bitslice test");
	sput_fail_unless(result[3] == 0,"bitslice test");

}

void test_matrix_column()	{
	uint8_t test_m[16] = {1,2,3,4,
						  5,6,7,8,
						  9,10,11,12,
						  13,14,15,16};
	uint8_t test_m_2[64] = { 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,
					  	17,18,18,20,21,22,23,24,25,26,27,28,29,30,31,32,
					  	33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,
					  	49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64
					  };
	uint8_t *result;
	result = matrix_column(test_m,1,4,0,16);
	sput_fail_unless(result[0] = 1,"Testing Matrix Column");
	sput_fail_unless(result[1] = 5,"Testing Matrix Column");	
	sput_fail_unless(result[2] = 9,"Testing Matrix Column");	
	sput_fail_unless(result[3] = 13,"Testing Matrix Column");
	result = matrix_column(test_m,2,4,1,16);
	sput_fail_unless(result[0] = 3,"Testing Matrix Column");
	sput_fail_unless(result[1] = 4,"Testing Matrix Column");	
	sput_fail_unless(result[2] = 7,"Testing Matrix Column");	
	sput_fail_unless(result[3] = 8,"Testing Matrix Column");	
	sput_fail_unless(result[4] = 11,"Testing Matrix Column");
	sput_fail_unless(result[5] = 12,"Testing Matrix Column");	
	sput_fail_unless(result[6] = 15,"Testing Matrix Column");	
	sput_fail_unless(result[7] = 16,"Testing Matrix Column");
	result = matrix_column(test_m_2,4,16,0,64);		
	sput_fail_unless(result[0] = 1,"Testing Matrix Column");
	sput_fail_unless(result[1] = 2,"Testing Matrix Column");	
	sput_fail_unless(result[2] = 3,"Testing Matrix Column");	
	sput_fail_unless(result[3] = 4,"Testing Matrix Column");	
	sput_fail_unless(result[4] = 17,"Testing Matrix Column");
	sput_fail_unless(result[5] = 18,"Testing Matrix Column");	
	sput_fail_unless(result[6] = 19,"Testing Matrix Column");	
	sput_fail_unless(result[7] = 20,"Testing Matrix Column");
}

void test_array_position()	{
	sput_fail_unless(array_position(0,0,16) == 0,"Array Pos Calculator");
	sput_fail_unless(array_position(1,4,16) == 20,"Array Pos Calculator");
	sput_fail_unless(array_position(1,1,4) == 5,"Array Pos Calculator");
}


// uint8_t  (*gmMult(uint8_t a[8], uint8_t b[8]))[8]{
// 	uint8_t g[8];
// 	g = bitslice(0,8);
// 	uint8_t i = 0;

// 	for(; i < 4; i = i + 1) {
// 		if(b[0] == True) {
// 			g = bitwise_bs(g, a, "^");
// 		}
// 		a = shift(a, 8, 1, "<<");
// 		if(a[3] == True) {
// 			a = bitwise_bs(a, bitslice(19, 8), "^");
// 		}
// 		b = shift(b, 8, 1, ">>");

// 	}
// 	return g;
// }

// uint8_t (*MixColumnSerial(uint8_t state[16][8], uint8_t MDS[16]))[8]{
// 	uint8_t column[4][8];
// 	uint8_t c = 0;

// 	for(; c < 4; c = c + 1) {
// 		column[0][0] = state[c][0];
// 		column[0][1] = state[c][1];
// 		column[0][2] = state[c][2];
// 		column[0][3] = state[c][3];
// 		column[0][4] = state[c][4];
// 		column[0][5] = state[c][5];
// 		column[0][6] = state[c][6];
// 		column[0][7] = state[c][7];
// 		column[1][0] = state[c + 4][0];
// 		column[1][1] = state[c + 4][1];
// 		column[1][2] = state[c + 4][2];
// 		column[1][3] = state[c + 4][3];
// 		column[1][4] = state[c + 4][4];
// 		column[1][5] = state[c + 4][5];
// 		column[1][6] = state[c + 4][6];
// 		column[1][7] = state[c + 4][7];
// 		column[2][0] = state[c + 8][0];
// 		column[2][1] = state[c + 8][1];
// 		column[2][2] = state[c + 8][2];
// 		column[2][3] = state[c + 8][3];
// 		column[2][4] = state[c + 8][4];
// 		column[2][5] = state[c + 8][5];
// 		column[2][6] = state[c + 8][6];
// 		column[2][7] = state[c + 8][7];
// 		column[3][0] = state[c + 12][0];
// 		column[3][1] = state[c + 12][1];
// 		column[3][2] = state[c + 12][2];
// 		column[3][3] = state[c + 12][3];
// 		column[3][4] = state[c + 12][4];
// 		column[3][5] = state[c + 12][5];
// 		column[3][6] = state[c + 12][6];
// 		column[3][7] = state[c + 12][7];
// 	uint8_t r = 0;

// 	for(; r < 4; r = r + 4) {
// 		state[4 * c + r] = bitwise_bs(bitwise_bs(bitwise_bs(gmMult(MDS[4 * c], column[0], gmMult(MDS[4 * c + 1], column[1], "^"), gmMult(MDS[4 * c + 2], column[2], "^"), gmMult(MDS[4 * c + 3], column[3], "^");
// 	}

// 	}
// 	return state;
// }


