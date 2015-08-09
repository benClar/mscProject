#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "led_dsl.h"

void rotate(void *target, void *base, int nmem, int size, int start, int finish) {
	
}

int main()	{
	uint32_t test[5][4] = {{1,1,1,1},{2,2,2,2},{3,3,3,3},{4,4,4,4},{5,5,5,5}};
	uint32_t test_1[3][4];
	memcpy(test_1, &(test[1]),3 * sizeof(test[4]));
	int row;
	int col;
	for(row = 0; row < 3; row++)	{
		for(col = 0; col < 4; col++)	{
			printf("%d",test_1[row][col]);
		}
		printf("\n");
	}
	// printf("%lu\n ",sizeof(test[4]));
	rotate(test_1, test, sizeof(test[4]))

}


// void addConstants(uint32_t state[16][4], uint32_t constant[5]){
// 	uint32_t roundConstant[16][4];
// 	uint8_t row;
// 	row = 0;
// 	uint32_t temp_0_cast_bs_val[4];
// 	int_to_bitsliced(temp_0_cast_bs_val, 0, 4);
// 	uint8_t temp_1_bs_int_start;
// 	uint32_t temp_2__bin = 0;
// 	uint32_t temp_3__bin = 0;
// 	temp_3__bin = row * 4;
// 	temp_2__bin = temp_3__bin + 2;
// 	for(temp_1_bs_int_start = 0; temp_1_bs_int_start < 4; temp_1_bs_int_start++){
// 		roundConstant[temp_2__bin][temp_1_bs_int_start] = temp_0_cast_bs_val[temp_1_bs_int_start];
// 	}
// }
