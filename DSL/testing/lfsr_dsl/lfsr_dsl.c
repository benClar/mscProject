#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "lfsr_dsl.h"
uint32_t  generate_bit(uint32_t state[8]){ 
uint32_t output;
uint32_t input;
output = state[7];
uint32_t temp_0__bin[8] = {0};
shift_right(temp_0__bin, state, 1, 8);
state[0] = temp_0__bin[0];
state[1] = temp_0__bin[1];
state[2] = temp_0__bin[2];
state[3] = temp_0__bin[3];
state[4] = temp_0__bin[4];
state[5] = temp_0__bin[5];
state[6] = temp_0__bin[6];
state[7] = temp_0__bin[7];
input = ((state[0] ^ state[4]) ^ (state[5] ^ state[6]));
state[0] = input;
return output;
}
void  lfsr(uint32_t *temp_1_bs_return, uint32_t state[8]){ 
uint32_t rndm_bits[32] = {0};
uint8_t r = 0;
r = 0;
for(;r < 32;) { 
uint32_t temp_3_call;
temp_3_call = generate_bit(state);
rndm_bits[r] = temp_3_call;
r = (r + 1);
} 
temp_1_bs_return[0] = rndm_bits[0];
temp_1_bs_return[1] = rndm_bits[1];
temp_1_bs_return[2] = rndm_bits[2];
temp_1_bs_return[3] = rndm_bits[3];
temp_1_bs_return[4] = rndm_bits[4];
temp_1_bs_return[5] = rndm_bits[5];
temp_1_bs_return[6] = rndm_bits[6];
temp_1_bs_return[7] = rndm_bits[7];
temp_1_bs_return[8] = rndm_bits[8];
temp_1_bs_return[9] = rndm_bits[9];
temp_1_bs_return[10] = rndm_bits[10];
temp_1_bs_return[11] = rndm_bits[11];
temp_1_bs_return[12] = rndm_bits[12];
temp_1_bs_return[13] = rndm_bits[13];
temp_1_bs_return[14] = rndm_bits[14];
temp_1_bs_return[15] = rndm_bits[15];
temp_1_bs_return[16] = rndm_bits[16];
temp_1_bs_return[17] = rndm_bits[17];
temp_1_bs_return[18] = rndm_bits[18];
temp_1_bs_return[19] = rndm_bits[19];
temp_1_bs_return[20] = rndm_bits[20];
temp_1_bs_return[21] = rndm_bits[21];
temp_1_bs_return[22] = rndm_bits[22];
temp_1_bs_return[23] = rndm_bits[23];
temp_1_bs_return[24] = rndm_bits[24];
temp_1_bs_return[25] = rndm_bits[25];
temp_1_bs_return[26] = rndm_bits[26];
temp_1_bs_return[27] = rndm_bits[27];
temp_1_bs_return[28] = rndm_bits[28];
temp_1_bs_return[29] = rndm_bits[29];
temp_1_bs_return[30] = rndm_bits[30];
temp_1_bs_return[31] = rndm_bits[31];
}

