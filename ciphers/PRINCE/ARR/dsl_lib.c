/*---------- Standard Headers -----------*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
/*---------- Custom Headers	-----------*/

#include "dsl_lib.h"
#include "sput.h"


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

uint8_t *rotate_right(uint8_t *input, int var_size ,int shift)    {
	uint8_t *input_copy = clone(input,var_size);
    reverse(input_copy, 0, var_size - 1);
    reverse(input_copy, 0, shift - 1);
    reverse(input_copy, shift, var_size - 1);
    return input_copy;
}

uint8_t *shift_right(uint8_t *input, int var_size ,int shift)	{
	uint8_t *input_copy = calloc(var_size, sizeof(uint8_t));
	memcpy(input_copy + shift,input,(var_size - shift) * sizeof(uint8_t));
	return input_copy;
}

uint8_t *shift_left(uint8_t *input, int var_size ,int shift)	{
	uint8_t *input_copy = calloc(var_size, sizeof(uint8_t));
	memcpy(input_copy,input,(var_size - shift) * sizeof(uint8_t));
	return input_copy;
}

uint8_t *clone(uint8_t *input, int var_size)	{
	uint8_t *input_copy = malloc(var_size * sizeof(uint8_t));
	memcpy(input_copy,input,var_size * sizeof(uint8_t));
	return input_copy;
}

uint8_t **clone_square_matrix(uint8_t **input, int length, int ele_size)	{
	int row, col;
	uint8_t **cloned_input = malloc((length * length) * sizeof(uint8_t*));
	for(row = 0; row < length; row++)	{
		for(col = 0; col < length; col++)	{
			cloned_input[row * length + col] = clone(input[row * length + col],ele_size);
		}
	}
	return cloned_input;
}

int compare_sq_matrix(uint8_t **a, uint8_t **b, int length)	{
	int row,col;
	for(row = 0; row < length; row++)	{
		for(col =0; col < length; col++)	{
			if(a[row][col] != b[row][col])	{
				return 0;
			}
		}
	}
	return 1;

}

void print_sq_matrix(uint8_t **m, int length)	{
	int row,col;
	for(row = 0; row < length; row++)	{
		for(col =0; col < length; col++)	{
			printf("%d",m[row][col]);
		}
		printf("\n");
	}	
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

uint8_t *XOR(uint8_t *a, uint8_t *b, int size)	{
	int bit;
	uint8_t *output = calloc(size,sizeof(uint8_t));
	for(bit = 0; bit < size; bit++)	{
		output[bit] = a[bit] ^ b[bit];
	}
	return output;
}


void print_array(uint8_t *array,int size)	{
	int ele;
	for(ele = 0; ele < size; ele++)	{
		printf("%d ", array[ele]);
	}
	printf("\n");
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
	sput_enter_suite("Test Matrix Clone");
	sput_run_test(test_sq_matrix_clone);
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
	sput_fail_unless(result[0] == 1,"shift_left test");
	sput_fail_unless(result[1] == 2,"shift_left test");
	sput_fail_unless(result[2] == 3,"shift_left test");
	sput_fail_unless(result[3] == 4,"shift_left test");
	sput_fail_unless(result[4] == 5,"shift_left test");
	sput_fail_unless(result[5] == 6,"shift_left test");
	sput_fail_unless(result[6] == 7,"shift_left test");
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

void test_sq_matrix_clone()	{
	uint8_t **m = calloc(16,sizeof(uint8_t*));
	uint8_t *m_bl = calloc(4,sizeof(uint8_t));
	int ele;
	for(ele = 0; ele < 16; ele++)	{
		m[ele] = clone(m_bl,4);
	}
	m[0][3] = 1;
	uint8_t **m_clone = clone_square_matrix(m,4,4);
	sput_fail_unless(compare_sq_matrix(m,m_clone,4) == 1,"clone matrix test");
}


