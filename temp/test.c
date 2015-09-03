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