#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

void bitslice_add(uint32_t *output, uint32_t A[8], uint32_t B[8])	{
	int bit;
	uint32_t carry = 0;
	for(bit = 0; bit < 8; bit++)	{
		output[7 - bit] = ((A[7 - bit] ^ B[7 - bit]) ^ carry);
		carry = ((A[7 - bit] ^ B[7 - bit]) & carry) | (A[7 - bit] & B[7 - bit]);
	}
	output[7 - bit] = carry;
}

void bitslice_mult(uint32_t *output, uint32_t *operand_1, uint32_t *operand_2, int width)	{
	int p_bit, outer_bit, inner_bit;
	uint32_t p[width][width];
	for(outer_bit = 0; outer_bit < width; outer_bit++)	{
		for(inner_bit = 0; inner_bit < width; inner_bit++)	{
			p[outer_bit][inner_bit] = operand_1[outer_bit] & operand_2[inner_bit];
		}
	}
	for(outer_bit = 0; outer_bit < width; outer_bit++)	{
		for(inner_bit = 0, p_bit = outer_bit; p_bit < width; inner_bit++, p_bit++)	{
			output[p_bit] |= p[outer_bit][inner_bit];
		}
	}
}

int main(){
	uint32_t output[16] = {0};
	uint32_t a[16] = {0,1,1,1,0,0,0,1};
	uint32_t b[16] = {0,0,0,0,0,1,0,0};
	bitslice_mult(output,a,b,16);
	for(int i = 15; i >= 0; i--)	{
		printf("%d",output[i]);
	}
	printf("\n");
	return 1;
}
