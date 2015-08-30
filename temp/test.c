#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <assert.h>

void bitslice_add(uint32_t *output, uint32_t *operand_1, uint32_t *operand_2, int width)	{
	int bit;
	uint32_t carry = 0;
	for(bit = 0; bit < width; bit++)	{
		output[bit] = ((operand_1[bit] ^ operand_2[bit]) ^ carry);
		carry = ((operand_1[bit] ^ operand_2[bit]) & carry) | (operand_1[bit] & operand_2[bit]);
	}
	output[bit] = carry;
}

void bitslice_mult(uint32_t *output, uint32_t *operand_1, uint32_t *operand_2, int width)	{
	int outer_bit, inner_bit, target_bit;
	uint32_t accumulate[width];
	for(int init_bit = 0; init_bit < width; init_bit++)	{
		accumulate[init_bit] = 0;
	}
	uint32_t temp[width];
	uint32_t p[width][width];
	for(int outter= 0; outter < width; outter++)	{
		for(int inner= 0; inner < width; inner++)	{
			p[outter][inner] = 0;
		}
	}

	for(outer_bit = 0; outer_bit < width; outer_bit++)	{
		for(inner_bit = 0, target_bit = outer_bit; target_bit < width; inner_bit++,target_bit++)	{
			p[outer_bit][target_bit] = operand_1[outer_bit] & operand_2[inner_bit];
		}
	}
	for(outer_bit = 0; outer_bit < width; outer_bit++)	{
		bitslice_add(temp, p[outer_bit], accumulate, width);
		for(int bit = 0; bit < width; bit++)	{
			accumulate[bit] = temp[bit];
		}
	}
	for(int bit = 0; bit < width; bit++)	{
		output[bit] = accumulate[bit];
	}
}


int main(){
	uint32_t a[32] = {1,1,1,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t b[32] = {1,1,1,0,1,1,1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	uint32_t res[32] = {0};
	bitslice_mult(res, a, b, 32);
	for(int i = 31; i >= 0; i--)	{
		printf("%d",res[i]);
	}
	printf("\n");
}