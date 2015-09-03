#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include "poster_tests.h"

int main()	{
	// sbox_demo();
	// int_extraction();
	bs_bitwise_demo();
}

void bs_bitwise_demo()	{
	uint32_t demo_1[64] = {0};
	bitslice_rotate(demo_1);
	printf("### 01010 rotated left by 1 ###\n");
	bs_print(demo_1,64); // Should equal 10100
}

void sbox_demo()	{
	uint32_t demo_1[4] = {0xffffffff,0,0,0};  // 0x1
	uint32_t demo_2[4] = {0,0,0xffffffff,0};  // 0x4
	uint32_t demo_3[4] = {0,0xffffffff,0xffffffff,0};  //0x6
	uint32_t demo_4[32] = {0};  //0xC
	printf("### Substituting 1 for 5 ###\n");
	present(demo_1);
	bs_print(demo_1, 4);
	printf("### Substituting 4 for 9 ###\n");
	present(demo_2);
	bs_print(demo_2, 4);
	printf("### Substituting 6 for 10 ###\n");
	present(demo_3);
	bs_print(demo_3, 4);
	printf("### Running bits 0 to 3 through sbox ###\n");
	sbox_test(demo_4);
	bs_print(demo_4,32);
}

void int_extraction()	{
	printf("### XORing bit 1 of 0xa (1011) and 0xd (1101) ###\n");
	printf("%d\n",int_XOR_1()); //Should be 1
	printf("### Setting the 0th, 1st and 3rd bits of 0x0 to True ###\n");
	printf("%d\n",int_index_set_1()); // Should be 11
}

void bs_print(uint32_t *var, uint32_t size)	{
	for(int slice = 0; slice < 32; slice++){
		for(int bit = 0; bit < size; bit++)	{
			printf("%d ",(var[(size - bit) - 1] >> slice) & 0x1);
		}
		printf("\n");
	}
}
