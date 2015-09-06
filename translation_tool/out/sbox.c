#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "sbox.h"
uint32_t present_0(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((D & B & ~A) | (D & C & ~B & A) | (D & ~C & ~A) | (~D & C & ~B & ~A) | (~D & ~C & A) | (~D & B & A));
}
uint32_t present_1(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((~D & B & ~A) | (~C & B & ~A) | (D & ~C & ~A) | (D & C & A) | (~D & ~C & B) | (D & ~B & A));
}
uint32_t present_2(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((~D & C & B & A) | (~C & B & ~A) | (D & C & ~B) | (~C & ~B & A) | (D & ~B & A) | (~D & ~C & ~A));
}
uint32_t present_3(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((~C & B & A) | (~D & C & B) | (~D & ~B & ~A) | (D & ~C & B) | (D & ~C & A) | (~D & C & ~A));
}
void present(uint32_t input[4]){
uint32_t temp_0_sbox_out[4];
temp_0_sbox_out[0] = present_0(input[0], input[1], input[2], input[3]);
temp_0_sbox_out[1] = present_1(input[0], input[1], input[2], input[3]);
temp_0_sbox_out[2] = present_2(input[0], input[1], input[2], input[3]);
temp_0_sbox_out[3] = present_3(input[0], input[1], input[2], input[3]);
input[0] = temp_0_sbox_out[0];
input[1] = temp_0_sbox_out[1];
input[2] = temp_0_sbox_out[2];
input[3] = temp_0_sbox_out[3];
}
void  sbox_test(uint32_t *temp_1_bs_return){ 
uint32_t state[32] = {0};
state[0]= 0;
state[1]= 0;
state[2]= 0;
state[3]= 0;
state[4]= 0;
state[5]= 0;
state[6]= 0;
state[7]= 0;
state[8]= 0;
state[9]= 0;
state[10]= 0;
state[11]= 0;
state[12]= 0;
state[13]= 0;
state[14]= 0;
state[15]= 0;
state[16]= 0;
state[17]= 0;
state[18]= 0;
state[19]= 0;
state[20]= 0;
state[21]= 0;
state[22]= 0;
state[23]= 0;
state[24]= 0;
state[25]= 0;
state[26]= 0;
state[27]= 0;
state[28]= 0;
state[29]= 0;
state[30]= 0;
state[31]= 0;
uint32_t temp_2_rnge[(3 - 0) + 1];
extract_bs_range(temp_2_rnge, state, 0, 3);
present(temp_2_rnge);
state[0] = temp_2_rnge[0];
state[1] = temp_2_rnge[1];
state[2] = temp_2_rnge[2];
state[3] = temp_2_rnge[3];
temp_1_bs_return[0] = state[0];
temp_1_bs_return[1] = state[1];
temp_1_bs_return[2] = state[2];
temp_1_bs_return[3] = state[3];
temp_1_bs_return[4] = state[4];
temp_1_bs_return[5] = state[5];
temp_1_bs_return[6] = state[6];
temp_1_bs_return[7] = state[7];
temp_1_bs_return[8] = state[8];
temp_1_bs_return[9] = state[9];
temp_1_bs_return[10] = state[10];
temp_1_bs_return[11] = state[11];
temp_1_bs_return[12] = state[12];
temp_1_bs_return[13] = state[13];
temp_1_bs_return[14] = state[14];
temp_1_bs_return[15] = state[15];
temp_1_bs_return[16] = state[16];
temp_1_bs_return[17] = state[17];
temp_1_bs_return[18] = state[18];
temp_1_bs_return[19] = state[19];
temp_1_bs_return[20] = state[20];
temp_1_bs_return[21] = state[21];
temp_1_bs_return[22] = state[22];
temp_1_bs_return[23] = state[23];
temp_1_bs_return[24] = state[24];
temp_1_bs_return[25] = state[25];
temp_1_bs_return[26] = state[26];
temp_1_bs_return[27] = state[27];
temp_1_bs_return[28] = state[28];
temp_1_bs_return[29] = state[29];
temp_1_bs_return[30] = state[30];
temp_1_bs_return[31] = state[31];
}

