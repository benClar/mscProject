#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "led_dsl.h"
void mPrime(uint32_t state[64]){ 
uint32_t a[16] = {0};
uint32_t b[16] = {0};
uint32_t c[16] = {0};
uint32_t temp_2__bin[16] = {0};
uint32_t temp_3__bin[16] = {0};
bitslice_bitwise(temp_3__bin, b, c, 16, "^");
bitslice_bitwise(temp_2__bin, a, temp_3__bin, 16, "^");
c[0] = temp_2__bin[0];
c[1] = temp_2__bin[1];
c[2] = temp_2__bin[2];
c[3] = temp_2__bin[3];
c[4] = temp_2__bin[4];
c[5] = temp_2__bin[5];
c[6] = temp_2__bin[6];
c[7] = temp_2__bin[7];
c[8] = temp_2__bin[8];
c[9] = temp_2__bin[9];
c[10] = temp_2__bin[10];
c[11] = temp_2__bin[11];
c[12] = temp_2__bin[12];
c[13] = temp_2__bin[13];
c[14] = temp_2__bin[14];
c[15] = temp_2__bin[15];
}

