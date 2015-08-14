#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "sput.h"
#include "BS_LIB.h"

void print(uint32_t *arr, int size)	{
	int i;
	for(i = 0; i < size; i++)	{
		printf("%d",arr[i]);
	}
	printf("\n");
}

double get_time()	{
	double timeConvert;
		mach_timebase_info_data_t timeBase;
		(void)mach_timebase_info( &timeBase );
		timeConvert = (double)timeBase.numer /
			(double)timeBase.denom /
			1000000000.0;
	return (double)mach_absolute_time( ) * timeConvert;
}

void rprint(uint32_t *arr, int size)	{
	int i;
	for(i = size - 1; i >= 0; i--)	{
		printf("%d",arr[i]);
	}
	printf("\n");
}


void bitslice_bitwise(uint32_t *target, uint32_t *op_1, uint32_t *op_2, int var_size, char *op){
	if(!strcmp(op, "^")) {
		XOR(target, op_1, op_2, var_size);
	} else if (!strcmp(op, "|")) {
		OR(target, op_1, op_2, var_size);
	} else if (!strcmp(op, "&"))	{
		AND(target, op_1, op_2, var_size);
	} else {
		printf("Internal Error: Unrecognised bitwise operator\n");
		exit(1);
	}
}

void XOR(uint32_t *target, uint32_t *op_1, uint32_t *op_2, int var_size)	{
	int bit;
	for(bit = 0; bit < var_size; bit++)	{
		target[bit] = op_1[bit] ^ op_2[bit];
	}
}

void AND(uint32_t *target, uint32_t *op_1, uint32_t *op_2, int var_size)	{
	int bit;
	for(bit = 0; bit < var_size; bit++)	{
		target[bit] = op_1[bit] & op_2[bit];
	}
}

void OR(uint32_t *target, uint32_t *op_1, uint32_t *op_2, int var_size)	{
	int bit;
	for(bit = 0; bit < var_size; bit++)	{
		target[bit] = op_1[bit] | op_2[bit];
	}
}

void rotate_left(uint32_t *target, uint32_t *source, int shift, int var_size)    {
	bs_copy(target, source, var_size);
    reverse(target, 0, var_size - 1);
	reverse(target, var_size - shift, var_size - 1);
    reverse(target, 0, var_size - shift - 1);
    
}

void rotate_right(uint32_t *target, uint32_t *source, int shift, int var_size)    {
	bs_copy(target, source, var_size);
    reverse(target, 0, var_size - 1);
    reverse(target, 0, shift - 1);
    reverse(target, shift, var_size - 1);
}

void shift_right(uint32_t *target, uint32_t *source, int shift, int var_size)	{
	memcpy(target + shift, source,(var_size - shift) * sizeof(uint32_t));
}

void shift_left(uint32_t *target, uint32_t *source, int shift, int var_size)	{
	memcpy(target, source + shift,(var_size - shift) * sizeof(uint32_t));
}

void reverse(uint32_t *target, int start, int end)	{
	while(start < end)	{
		int tmp = target[start];
		target[start] = target[end];
		target[end] = tmp;
		start++;
		end--;
	}
}

void bs_copy(uint32_t *target, uint32_t *source, int size)	{
	int ele;
	for(ele = 0; ele < size; ele++)	{
		target[ele] = source[ele];
	}
}

void int_to_bitsliced(uint32_t *target, uint32_t source, int var_size)	{
	int bit;
	int val;
	for(bit = 0; bit < var_size; bit++)	{
		if ((source >> bit) & 0x1)	{
			val = 0xffffffff;
			// val = 0x1;
		} else {
			val = 0x0;
		}
		target[bit] = val;
	}
	// rprint(target,var_size);
}

void bitslice_shift(uint32_t *target, uint32_t *source, int shift, int var_size, char *op)	{
	if(!strcmp(op, ">>")) {
		shift_left(target, source, var_size, shift);
	} else if (!strcmp(op, "<<")) {
		shift_right(target, source, var_size, shift);
	} else if (!strcmp(op, ">>>"))	{
		rotate_left(target, source, var_size, shift);
	}else if (!strcmp(op, "<<<"))	{
		rotate_right(target, source, var_size, shift);
	} else {
		printf("Internal Error: Unrecognised shift operator\n");
		exit(1);
	}
}

void hprint(uint32_t *target, int size){
	char hex_lookup[16] = {'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};
	int output;
	for(int nibble = 0; nibble < size/4; nibble++, output = 0)	{
		for(int bit = 0; bit < 4; bit++)	{
			output ^= (target[(nibble * 4 ) + bit] << bit);
		}
		printf("%c",hex_lookup[output]);
	}
	printf("\n");
}

void extract_bs_range(uint32_t *target, uint32_t *source, int start, int finish)	{
	int i;
	for(i = 0; start <= finish; i++, start++)	{
		target[i] = source[start];
	}

}

void bitslice(uint32_t *target, long source, int var_size)	{
	int bit;
	for(bit = 0; bit < var_size; bit++)	{
		if ((source >> bit) & 1)	{
			// target[bit] = 0x1;
			target[bit] = 0xffffffff;
		} else	{
			target[bit] = 0;
		}
	}
}

void bitslice_bend(uint32_t *target, long source, int var_size)	{
	int bit;
	for(bit = 0; bit < var_size; bit++)	{
		if ((source >> bit) & 1)	{
			target[(var_size - bit) - 1] = 0x1;
			// target[(var_size - bit) - 1] = 0xffffffff;
		} else {
			target[var_size - bit - 1] = 0;
		}
	}
}

void hex_print(uint32_t *state, int row_width, int area)	{

	char hex_lookup[16] = {'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};
	int row, nibble, lookup = 0,bit;
	for(row = 0; row < area/row_width; row++)	{
		for(nibble = 0; nibble < row_width / 4; nibble++)	{
			for(bit = 0; bit < 4; bit++)	{
				lookup = (lookup << 1) ^ state[(row_width * row) + (nibble * 4) + bit];
			}
			printf("%c",hex_lookup[lookup]);
			lookup = 0;
		}
	}
	printf("\n");

}

/*Tests*/

// int main(){
// 	testing();
// }

void testing(){
	sput_start_testing();
	sput_enter_suite("Testing Bit Array Reverse");
	sput_run_test(reverse_testing);
	sput_enter_suite("Testing Bit Array Shifts");
	sput_run_test(shift_testing);
	sput_enter_suite("Testing Bit Array Bitwise");
	sput_run_test(bitwise_testing);
	sput_enter_suite("Testing Bit-Slicing");
	sput_run_test(bitslice_testing);
	sput_finish_testing();
}

void bitwise_testing()	{
	uint32_t op_1[5] = {1,1,1,1,1};
	uint32_t op_2[5] = {1,0,1,0,1};
	uint32_t test_1_tar[5];
	bitslice_bitwise(test_1_tar, op_1, op_2, 5, "^");
	sput_fail_unless(test_1_tar[0] == 0,"XOR Test");
	sput_fail_unless(test_1_tar[1] == 1,"XOR Test");
	sput_fail_unless(test_1_tar[2] == 0,"XOR Test");
	sput_fail_unless(test_1_tar[3] == 1,"XOR Test");
	sput_fail_unless(test_1_tar[4] == 0,"XOR Test");
	uint32_t test_2_tar[5];
	bitslice_bitwise(test_2_tar, op_1, op_2, 5, "&");
	sput_fail_unless(test_2_tar[0] == 1,"AND Test");
	sput_fail_unless(test_2_tar[1] == 0,"AND Test");
	sput_fail_unless(test_2_tar[2] == 1,"AND Test");
	sput_fail_unless(test_2_tar[3] == 0,"AND Test");
	sput_fail_unless(test_2_tar[4] == 1,"AND Test");
	uint32_t test_3_tar[5];
	bitslice_bitwise(test_3_tar, op_1, op_2, 5, "|");
	sput_fail_unless(test_3_tar[0] == 1,"OR Test");
	sput_fail_unless(test_3_tar[1] == 1,"OR Test");
	sput_fail_unless(test_3_tar[2] == 1,"OR Test");
	sput_fail_unless(test_3_tar[3] == 1,"OR Test");
	sput_fail_unless(test_3_tar[4] == 1,"OR Test");
}

void shift_testing(){
	uint32_t test_source[5] = {0,1,0,0,1};
	uint32_t test_1_tar[5] = {0};
	bitslice_shift(test_1_tar, test_source, 3, 5,"<<<");
	sput_fail_unless(test_1_tar[0] == 0,"Left Circular Shift Test");
	sput_fail_unless(test_1_tar[1] == 0,"Left Circular Shift Test");
	sput_fail_unless(test_1_tar[2] == 1,"Left Circular Shift Test");
	sput_fail_unless(test_1_tar[3] == 0,"Left Circular Shift Test");
	sput_fail_unless(test_1_tar[4] == 1,"Left Circular Shift Test");
	uint32_t test_2_tar[5] = {0};
	bitslice_shift(test_2_tar, test_source, 3, 5,">>>");
	sput_fail_unless(test_2_tar[0] == 0,"Right Circular Shift Test");
	sput_fail_unless(test_2_tar[1] == 1,"Right Circular Shift Test");
	sput_fail_unless(test_2_tar[2] == 0,"Right Circular Shift Test");
	sput_fail_unless(test_2_tar[3] == 1,"Right Circular Shift Test");
	sput_fail_unless(test_2_tar[4] == 0,"Right Circular Shift Test");
	uint32_t test_3_tar[5] = {0};
	bitslice_shift(test_3_tar, test_source, 3, 5,"<<");
	sput_fail_unless(test_3_tar[0] == 0,"Left Shift Test");
	sput_fail_unless(test_3_tar[1] == 0,"Left Shift Test");
	sput_fail_unless(test_3_tar[2] == 0,"Left Shift Test");
	sput_fail_unless(test_3_tar[3] == 0,"Left Shift Test");
	sput_fail_unless(test_3_tar[4] == 1,"Left Shift Test");
}

void reverse_testing(){
	uint32_t test_source[9] = {0,1,2,3,4,5,6,7,8};
	uint32_t test_1_tar[9] = {0};
	bs_copy(test_1_tar, test_source, 9);
	reverse(test_1_tar, 0, 8);
	sput_fail_unless(test_1_tar[0] == 8,"Full Reverse");
	sput_fail_unless(test_1_tar[1] == 7,"Full Reverse");
	sput_fail_unless(test_1_tar[2] == 6,"Full Reverse");
	sput_fail_unless(test_1_tar[3] == 5,"Full Reverse");
	sput_fail_unless(test_1_tar[4] == 4,"Full Reverse");
	sput_fail_unless(test_1_tar[5] == 3,"Full Reverse");
	sput_fail_unless(test_1_tar[6] == 2,"Full Reverse");
	sput_fail_unless(test_1_tar[7] == 1,"Full Reverse");
	sput_fail_unless(test_1_tar[8] == 0,"Full Reverse");
	uint32_t test_2_tar[9] = {0};
	bs_copy(test_2_tar, test_source, 9);
	reverse(test_2_tar, 0, 3);
	sput_fail_unless(test_2_tar[0] == 3,"Partial Reverse");
	sput_fail_unless(test_2_tar[1] == 2,"Partial Reverse");
	sput_fail_unless(test_2_tar[2] == 1,"Partial Reverse");
	sput_fail_unless(test_2_tar[3] == 0,"Partial Reverse");
	sput_fail_unless(test_2_tar[4] == 4,"Partial Reverse");
	sput_fail_unless(test_2_tar[5] == 5,"Partial Reverse");
	sput_fail_unless(test_2_tar[6] == 6,"Partial Reverse");
	sput_fail_unless(test_2_tar[7] == 7,"Partial Reverse");
	sput_fail_unless(test_2_tar[8] == 8,"Partial Reverse");
}

void bitslice_testing()	{
	uint32_t RC[11][64];
	bitslice(RC[1], 0x13198a2e03707344, 64);
	sput_fail_unless(RC[1][35] == 1,"Bitsliced");
	sput_fail_unless(RC[1][36] == 0,"Bitsliced");
	sput_fail_unless(RC[1][37] == 1,"Bitsliced");
	sput_fail_unless(RC[1][38] == 0,"Bitsliced");
	sput_fail_unless(RC[1][39] == 0,"Bitsliced");
	sput_fail_unless(RC[1][40] == 0,"Bitsliced");
	sput_fail_unless(RC[1][41] == 1,"Bitsliced");
	sput_fail_unless(RC[1][42] == 0,"Bitsliced");
}

