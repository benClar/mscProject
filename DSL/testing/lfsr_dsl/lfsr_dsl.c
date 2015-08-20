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
void lfsr(uint32_t rndm_bits[32], uint32_t state[8]){ 
uint8_t r;
r = 0;
for(;r < 32;) { 
uint32_t temp_2_call;
temp_2_call = generate_bit(state);
rndm_bits[r] = temp_2_call;
r = (r + 1);
} 
}

