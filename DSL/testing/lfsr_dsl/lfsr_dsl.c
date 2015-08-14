#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "lfsr_dsl.h"
void  generate_bit(uint32_t *temp_0_bs_return, uint32_t state[8]){ 
uint32_t output[1] = {0};
uint32_t input[1] = {0};
output[0] = state[7];
uint32_t temp_1__bin[8] = {0};
shift_right(temp_1__bin, state, 1, 8);
state[0] = temp_1__bin[0];
state[1] = temp_1__bin[1];
state[2] = temp_1__bin[2];
state[3] = temp_1__bin[3];
state[4] = temp_1__bin[4];
state[5] = temp_1__bin[5];
state[6] = temp_1__bin[6];
state[7] = temp_1__bin[7];
input[0] = ((state[0] ^ state[4]) ^ (state[5] ^ state[6]));
state[0] = input[0];
temp_0_bs_return[0] = output[0];
}
void lfsr(uint32_t rndm_bits[32][1], uint32_t state[8]){ 
uint8_t r;
r = 0;
for(;r < 32;) { 
uint32_t temp_4_call[1];
generate_bit(temp_4_call, state);
rndm_bits[r][0] = temp_4_call[0];
r = (r + 1);
} 
}

