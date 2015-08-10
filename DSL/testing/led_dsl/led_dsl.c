#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "led_dsl.h"

void gmMult(uint32_t output[8], uint32_t a[8], uint32_t b[8]){
	uint32_t a_out[8];
	a_out[0] = a[0];
	a_out[1] = a[1];
	a_out[2] = a[2];
	a_out[3] = a[3];
	a_out[4] = a[4];
	a_out[5] = a[5];
	a_out[6] = a[6];
	a_out[7] = a[7];
	uint32_t b_out[8];
	b_out[0] = b[0];
	b_out[1] = b[1];
	b_out[2] = b[2];
	b_out[3] = b[3];
	b_out[4] = b[4];
	b_out[5] = b[5];
	b_out[6] = b[6];
	b_out[7] = b[7];
	uint32_t GF_R[8];
	uint32_t temp_0_cast_bs_val[8];
	int_to_bitsliced(temp_0_cast_bs_val, 19, 8);
	GF_R[0] = temp_0_cast_bs_val[0];
	GF_R[1] = temp_0_cast_bs_val[1];
	GF_R[2] = temp_0_cast_bs_val[2];
	GF_R[3] = temp_0_cast_bs_val[3];
	GF_R[4] = temp_0_cast_bs_val[4];
	GF_R[5] = temp_0_cast_bs_val[5];
	GF_R[6] = temp_0_cast_bs_val[6];
	GF_R[7] = temp_0_cast_bs_val[7];
	uint32_t t[8];
	uint32_t f[1];
	uint32_t high[1];
	uint32_t temp_1_cast_bs_val[1];
	int_to_bitsliced(temp_1_cast_bs_val, 0, 1);
	high[0] = temp_1_cast_bs_val[0];
	uint32_t mask[8];
	uint8_t bit;
	bit = 0;
	uint8_t degree;
	degree = 0;
	for(;degree < 4;) {
	printf("A OUT\n");
	rprint(a_out,8);
	printf("B OUT\n");
	rprint(b_out, 8);
	uint32_t temp_3_cast_bs_val[1];
	int_to_bitsliced(temp_3_cast_bs_val, 0, 1);
	f[0] = temp_3_cast_bs_val[0];
	uint32_t temp_4__bin[8] = {0};
	uint32_t temp_5_casted_bs[8]= {0};
	int_to_bitsliced(temp_5_casted_bs, 1, 8);
	bitslice_bitwise(temp_4__bin, b_out, temp_5_casted_bs, 8, "&");
	t[0] = temp_4__bin[0];
	t[1] = temp_4__bin[1];
	t[2] = temp_4__bin[2];
	t[3] = temp_4__bin[3];
	t[4] = temp_4__bin[4];
	t[5] = temp_4__bin[5];
	t[6] = temp_4__bin[6];
	t[7] = temp_4__bin[7];
	bit = 0;
	printf("T\n");
	rprint(t, 8);
	for(;bit < 8;) {
	uint32_t temp_7__bin = 0;
	uint32_t  temp_8_extracted[1] = {0};
	temp_8_extracted[0] = f[0];
	uint32_t  temp_9_extracted[1] = {0};
	temp_9_extracted[0] = t[bit];
	temp_7__bin = temp_8_extracted[0] | temp_9_extracted[0];
	f[0] = temp_7__bin;
	uint32_t temp_6__bin = 0;
	temp_6__bin = bit + 1;
	bit = temp_6__bin;
	}
	printf("FLAG : %d \n", f[0]);
	bit = 0;
	for(;bit < 8;) {
	uint32_t temp_11__bin = 0;
	uint32_t  temp_12_extracted[1] = {0};
	temp_12_extracted[0] = f[0];
	uint32_t  temp_13_extracted[1] = {0};
	temp_13_extracted[0] = a_out[bit];
	temp_11__bin = temp_12_extracted[0] & temp_13_extracted[0];
	mask[bit] = temp_11__bin;
	uint32_t temp_10__bin = 0;
	temp_10__bin = bit + 1;
	bit = temp_10__bin;
	}
	uint32_t temp_14__bin[8] = {0};
	uint32_t temp_15__bin[8] = {0};
	bitslice_bitwise(temp_15__bin, mask, a_out, 8, "&");
	bitslice_bitwise(temp_14__bin, output, temp_15__bin, 8, "^");
	output[0] = temp_14__bin[0];
	output[1] = temp_14__bin[1];
	output[2] = temp_14__bin[2];
	output[3] = temp_14__bin[3];
	output[4] = temp_14__bin[4];
	output[5] = temp_14__bin[5];
	output[6] = temp_14__bin[6];
	output[7] = temp_14__bin[7];
	uint32_t  temp_16_extracted[1] = {0};
	temp_16_extracted[0] = a_out[3];
	high[0] = temp_16_extracted[0];
	uint32_t temp_17__bin[8] = {0};
	bitslice_shift(temp_17__bin, a_out, 1, 8, "<<");
	a_out[0] = temp_17__bin[0];
	a_out[1] = temp_17__bin[1];
	a_out[2] = temp_17__bin[2];
	a_out[3] = temp_17__bin[3];
	a_out[4] = temp_17__bin[4];
	a_out[5] = temp_17__bin[5];
	a_out[6] = temp_17__bin[6];
	a_out[7] = temp_17__bin[7];
	bit = 0;
	for(;bit < 8;) {
	uint32_t temp_19__bin = 0;
	uint32_t  temp_20_extracted[1] = {0};
	temp_20_extracted[0] = a_out[bit];
	uint32_t temp_21__bin = 0;
	uint32_t  temp_22_extracted[1] = {0};
	temp_22_extracted[0] = high[0];
	uint32_t  temp_23_extracted[1] = {0};
	temp_23_extracted[0] = GF_R[bit];
	temp_21__bin = temp_22_extracted[0] & temp_23_extracted[0];
	temp_19__bin = temp_20_extracted[0] ^ temp_21__bin;
	a_out[bit] = temp_19__bin;
	uint32_t temp_18__bin = 0;
	temp_18__bin = bit + 1;
	bit = temp_18__bin;
	}
	uint32_t temp_24__bin[8] = {0};
	bitslice_shift(temp_24__bin, b_out, 1, 8, ">>");
	b_out[0] = temp_24__bin[0];
	b_out[1] = temp_24__bin[1];
	b_out[2] = temp_24__bin[2];
	b_out[3] = temp_24__bin[3];
	b_out[4] = temp_24__bin[4];
	b_out[5] = temp_24__bin[5];
	b_out[6] = temp_24__bin[6];
	b_out[7] = temp_24__bin[7];
	uint32_t temp_2__bin = 0;
	temp_2__bin = degree + 1;
	degree = temp_2__bin;
	}
}

int main()	{
    uint32_t a[8] = {0,1,1,0,0,0,0};
    uint32_t b[8] = {1,1,0,0,0,0,0};
    uint32_t g[8]= {0};
    gmMult(g,a,b);
    rprint(g,8);
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
