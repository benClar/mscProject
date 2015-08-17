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

int main(){
	uint32_t output[8] = {0};
	uint32_t a[8] = {0,0,1,1,1,0,0,1};
	uint32_t b[8] = {0,0,1,0,1,0,1,0};
	bitslice_add(output,a,b);
	for(int i = 0; i < 8; i++)	{
		printf("%d",output[i]);
	}
	printf("\n");
	return 1;
}
