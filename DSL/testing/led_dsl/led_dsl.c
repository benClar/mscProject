#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "led_dsl.h"
uint32_t led_0(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((~D & ~C & A) | (~D & C & ~B & ~A) | (D & B & ~A) | (D & C & ~B & A) | (~D & B & A) | (D & ~C & ~A));
}
uint32_t led_1(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((D & ~B & A) | (~D & B & ~A) | (D & C & A) | (D & ~C & ~B) | (~D & ~C & B) | (D & ~C & ~A));
}
uint32_t led_2(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((D & ~B & A) | (~D & C & B & A) | (~C & ~B & A) | (D & C & ~B) | (~C & B & ~A) | (~D & ~C & ~B));
}
uint32_t led_3(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((~D & C & ~A) | (~D & ~B & ~A) | (D & ~C & A) | (D & ~C & B) | (~D & C & B) | (~C & B & A));
}
void led(uint32_t input[4]){
uint32_t temp_0_sbox_out[4];
temp_0_sbox_out[0] = led_0(input[0], input[1], input[2], input[3]);
temp_0_sbox_out[1] = led_1(input[0], input[1], input[2], input[3]);
temp_0_sbox_out[2] = led_2(input[0], input[1], input[2], input[3]);
temp_0_sbox_out[3] = led_3(input[0], input[1], input[2], input[3]);
input[0] = temp_0_sbox_out[0];
input[1] = temp_0_sbox_out[1];
input[2] = temp_0_sbox_out[2];
input[3] = temp_0_sbox_out[3];
}
void gmMult(uint32_t output[4], uint32_t a[4], uint32_t b[4]){ 
uint32_t a_out[4] = {0};
a_out[0] = a[0];
a_out[1] = a[1];
a_out[2] = a[2];
a_out[3] = a[3];
uint32_t b_out[4] = {0};
b_out[0] = b[0];
b_out[1] = b[1];
b_out[2] = b[2];
b_out[3] = b[3];
uint32_t GF_R[4] = {0};
GF_R[0]= 0xffffffff;
GF_R[1]= 0xffffffff;
GF_R[2]= 0;
GF_R[3]= 0;
uint32_t t[4] = {0};
uint32_t f[1] = {0};
uint32_t high[1] = {0};
high[0]= 0;
uint32_t mask[4] = {0};
uint8_t bit;
bit = 0;
output[0]= 0;
output[1]= 0;
output[2]= 0;
output[3]= 0;
uint8_t degree;
degree = 0;
for(;degree < 4;) { 
f[0]= 0;
t[0] = b_out[0] & 0xffffffff;
t[1] = b_out[1] & 0x0;
t[2] = b_out[2] & 0x0;
t[3] = b_out[3] & 0x0;
bit = 0;
for(;bit < 4;) { 
f[0] = (f[0] | t[bit]);
bit = (bit + 1);
} 
bit = 0;
for(;bit < 4;) { 
mask[bit] = (f[0] & a_out[bit]);
bit = (bit + 1);
} 
output[0] = output[0] ^ (mask[0] & a_out[0]);
output[1] = output[1] ^ (mask[1] & a_out[1]);
output[2] = output[2] ^ (mask[2] & a_out[2]);
output[3] = output[3] ^ (mask[3] & a_out[3]);
high[0] = a_out[3];
uint32_t temp_4__bin[8] = {0};
bitslice_shift(temp_4__bin, a_out, 1, 8, "<<");
a_out[0] = temp_4__bin[0];
a_out[1] = temp_4__bin[1];
a_out[2] = temp_4__bin[2];
a_out[3] = temp_4__bin[3];
bit = 0;
for(;bit < 4;) { 
a_out[bit] = (a_out[bit] ^ (high[0] & GF_R[bit]));
bit = (bit + 1);
} 
uint32_t temp_6__bin[8] = {0};
bitslice_shift(temp_6__bin, b_out, 1, 8, ">>");
b_out[0] = temp_6__bin[0];
b_out[1] = temp_6__bin[1];
b_out[2] = temp_6__bin[2];
b_out[3] = temp_6__bin[3];
degree = (degree + 1);
} 
}
void MixColumnSerial(uint32_t state[64], uint32_t MDS[16][4]){ 
uint32_t column[4][4];
uint32_t a[4] = {0};
uint32_t b[4] = {0};
uint32_t c[4] = {0};
uint32_t d[4] = {0};
uint8_t col;
col = 0;
for(;col < 4;) { 
column[0][0] = state[(col * 4)];
column[0][1] = state[((col * 4) + 1)];
column[0][2] = state[((col * 4) + 2)];
column[0][3] = state[((col * 4) + 3)];
column[0][0] = state[(col * 4)];
column[1][0] = state[((col + 4) * 4)];
column[1][1] = state[(((col + 4) * 4) + 1)];
column[1][2] = state[(((col + 4) * 4) + 2)];
column[1][3] = state[(((col + 4) * 4) + 3)];
column[2][0] = state[((col + 8) * 4)];
column[2][1] = state[(((col + 8) * 4) + 1)];
column[2][2] = state[(((col + 8) * 4) + 2)];
column[2][3] = state[(((col + 8) * 4) + 3)];
column[3][0] = state[((col + 12) * 4)];
column[3][1] = state[(((col + 12) * 4) + 1)];
column[3][2] = state[(((col + 12) * 4) + 2)];
column[3][3] = state[(((col + 12) * 4) + 3)];
uint8_t col_nibble;
col_nibble = 0;
for(;col_nibble < 4;) { 
gmMult(a, MDS[(col_nibble * 4)], column[0]);
gmMult(b, MDS[((col_nibble * 4) + 1)], column[1]);
gmMult(c, MDS[((col_nibble * 4) + 2)], column[2]);
gmMult(d, MDS[((col_nibble * 4) + 3)], column[3]);
uint32_t temp_64__bin[4] = {0};
uint32_t temp_65__bin[4] = {0};
uint32_t temp_66__bin[4] = {0};
bitslice_bitwise(temp_66__bin, a, b, 4, "^");
bitslice_bitwise(temp_65__bin, temp_66__bin, c, 4, "^");
bitslice_bitwise(temp_64__bin, temp_65__bin, d, 4, "^");
uint8_t temp_67_init = 0;
uint32_t temp_68_rnge_size = 0;
temp_68_rnge_size = ((((col * 4) + (col_nibble * 16)) + 3)-((col * 4) + (col_nibble * 16))) + 1;
uint8_t temp_79_rng_start = ((col * 4) + (col_nibble * 16));
for(temp_67_init = 0; temp_67_init < temp_68_rnge_size; temp_67_init++, temp_79_rng_start++){
state[temp_79_rng_start] = temp_64__bin[temp_67_init];
}
col_nibble = (col_nibble + 1);
} 
col = (col + 1);
} 
}
void shift_row(uint32_t state[64]){ 
uint32_t temp_80__bin[(31 - 16) + 1] = {0};
uint32_t temp_81_rnge[(31 - 16) + 1];
extract_bs_range(temp_81_rnge, state, 16, 31);
bitslice_shift(temp_80__bin, temp_81_rnge, 4, (31 - 16) + 1, ">>>");
state[16] = temp_80__bin[0];
state[17] = temp_80__bin[1];
state[18] = temp_80__bin[2];
state[19] = temp_80__bin[3];
state[20] = temp_80__bin[4];
state[21] = temp_80__bin[5];
state[22] = temp_80__bin[6];
state[23] = temp_80__bin[7];
state[24] = temp_80__bin[8];
state[25] = temp_80__bin[9];
state[26] = temp_80__bin[10];
state[27] = temp_80__bin[11];
state[28] = temp_80__bin[12];
state[29] = temp_80__bin[13];
state[30] = temp_80__bin[14];
state[31] = temp_80__bin[15];
uint32_t temp_82__bin[(47 - 32) + 1] = {0};
uint32_t temp_83_rnge[(47 - 32) + 1];
extract_bs_range(temp_83_rnge, state, 32, 47);
bitslice_shift(temp_82__bin, temp_83_rnge, 8, (47 - 32) + 1, ">>>");
state[32] = temp_82__bin[0];
state[33] = temp_82__bin[1];
state[34] = temp_82__bin[2];
state[35] = temp_82__bin[3];
state[36] = temp_82__bin[4];
state[37] = temp_82__bin[5];
state[38] = temp_82__bin[6];
state[39] = temp_82__bin[7];
state[40] = temp_82__bin[8];
state[41] = temp_82__bin[9];
state[42] = temp_82__bin[10];
state[43] = temp_82__bin[11];
state[44] = temp_82__bin[12];
state[45] = temp_82__bin[13];
state[46] = temp_82__bin[14];
state[47] = temp_82__bin[15];
uint32_t temp_84__bin[(63 - 48) + 1] = {0};
uint32_t temp_85_rnge[(63 - 48) + 1];
extract_bs_range(temp_85_rnge, state, 48, 63);
bitslice_shift(temp_84__bin, temp_85_rnge, 12, (63 - 48) + 1, ">>>");
state[48] = temp_84__bin[0];
state[49] = temp_84__bin[1];
state[50] = temp_84__bin[2];
state[51] = temp_84__bin[3];
state[52] = temp_84__bin[4];
state[53] = temp_84__bin[5];
state[54] = temp_84__bin[6];
state[55] = temp_84__bin[7];
state[56] = temp_84__bin[8];
state[57] = temp_84__bin[9];
state[58] = temp_84__bin[10];
state[59] = temp_84__bin[11];
state[60] = temp_84__bin[12];
state[61] = temp_84__bin[13];
state[62] = temp_84__bin[14];
state[63] = temp_84__bin[15];
}
void addConstants(uint32_t state[64], uint32_t constant[6]){ 
uint32_t roundConstant[64] = {0};
uint8_t row;
row = 0;
for(;row < 4;) { 
uint8_t  temp_87_extracted = 0;
uint8_t temp_88_int_rng_start  = 0;
uint8_t  temp_90_target_bit = 0;
for(;temp_88_int_rng_start < 3;temp_88_int_rng_start++, temp_90_target_bit++){
temp_87_extracted |= ((row >> temp_88_int_rng_start)  << temp_90_target_bit);
}
uint32_t temp_91_cast_bs_seq[(((row * 16) + 3) - (row * 16)) + 1];
int_to_bitsliced(temp_91_cast_bs_seq, temp_87_extracted, (((row * 16) + 3) - (row * 16)) + 1);
uint8_t temp_95_init = 0;
uint32_t temp_96_rnge_size = 0;
temp_96_rnge_size = (((row * 16) + 3)-(row * 16)) + 1;
uint8_t temp_101_rng_start = (row * 16);
for(temp_95_init = 0; temp_95_init < temp_96_rnge_size; temp_95_init++, temp_101_rng_start++){
roundConstant[temp_101_rng_start] = temp_91_cast_bs_seq[temp_95_init];
}
if(row == 0 || row == 2) { 
uint32_t temp_102_rnge[(5 - 3) + 1];
extract_bs_range(temp_102_rnge, constant, 3, 5);
uint8_t temp_103_init = 0;
uint32_t temp_104_rnge_size = 0;
temp_104_rnge_size = (((row * 16) + 6)-((row * 16) + 4)) + 1;
uint8_t temp_111_rng_start = ((row * 16) + 4);
for(temp_103_init = 0; temp_103_init < temp_104_rnge_size; temp_103_init++, temp_111_rng_start++){
roundConstant[temp_111_rng_start] = temp_102_rnge[temp_103_init];
}
} 
if(row == 1 || row == 3) { 
uint32_t temp_112_rnge[(2 - 0) + 1];
extract_bs_range(temp_112_rnge, constant, 0, 2);
uint8_t temp_113_init = 0;
uint32_t temp_114_rnge_size = 0;
temp_114_rnge_size = (((row * 16) + 6)-((row * 16) + 4)) + 1;
uint8_t temp_121_rng_start = ((row * 16) + 4);
for(temp_113_init = 0; temp_113_init < temp_114_rnge_size; temp_113_init++, temp_121_rng_start++){
roundConstant[temp_121_rng_start] = temp_112_rnge[temp_113_init];
}
} 
uint32_t temp_122_cast_bs_seq[(((row * 16) + 15) - ((row * 16) + 8)) + 1];
int_to_bitsliced(temp_122_cast_bs_seq, 0, (((row * 16) + 15) - ((row * 16) + 8)) + 1);
uint8_t temp_127_init = 0;
uint32_t temp_128_rnge_size = 0;
temp_128_rnge_size = (((row * 16) + 15)-((row * 16) + 8)) + 1;
uint8_t temp_135_rng_start = ((row * 16) + 8);
for(temp_127_init = 0; temp_127_init < temp_128_rnge_size; temp_127_init++, temp_135_rng_start++){
roundConstant[temp_135_rng_start] = temp_122_cast_bs_seq[temp_127_init];
}
row = (row + 1);
} 
state[0] = state[0] ^ roundConstant[0];
state[1] = state[1] ^ roundConstant[1];
state[2] = state[2] ^ roundConstant[2];
state[3] = state[3] ^ roundConstant[3];
state[4] = state[4] ^ roundConstant[4];
state[5] = state[5] ^ roundConstant[5];
state[6] = state[6] ^ roundConstant[6];
state[7] = state[7] ^ roundConstant[7];
state[8] = state[8] ^ roundConstant[8];
state[9] = state[9] ^ roundConstant[9];
state[10] = state[10] ^ roundConstant[10];
state[11] = state[11] ^ roundConstant[11];
state[12] = state[12] ^ roundConstant[12];
state[13] = state[13] ^ roundConstant[13];
state[14] = state[14] ^ roundConstant[14];
state[15] = state[15] ^ roundConstant[15];
state[16] = state[16] ^ roundConstant[16];
state[17] = state[17] ^ roundConstant[17];
state[18] = state[18] ^ roundConstant[18];
state[19] = state[19] ^ roundConstant[19];
state[20] = state[20] ^ roundConstant[20];
state[21] = state[21] ^ roundConstant[21];
state[22] = state[22] ^ roundConstant[22];
state[23] = state[23] ^ roundConstant[23];
state[24] = state[24] ^ roundConstant[24];
state[25] = state[25] ^ roundConstant[25];
state[26] = state[26] ^ roundConstant[26];
state[27] = state[27] ^ roundConstant[27];
state[28] = state[28] ^ roundConstant[28];
state[29] = state[29] ^ roundConstant[29];
state[30] = state[30] ^ roundConstant[30];
state[31] = state[31] ^ roundConstant[31];
state[32] = state[32] ^ roundConstant[32];
state[33] = state[33] ^ roundConstant[33];
state[34] = state[34] ^ roundConstant[34];
state[35] = state[35] ^ roundConstant[35];
state[36] = state[36] ^ roundConstant[36];
state[37] = state[37] ^ roundConstant[37];
state[38] = state[38] ^ roundConstant[38];
state[39] = state[39] ^ roundConstant[39];
state[40] = state[40] ^ roundConstant[40];
state[41] = state[41] ^ roundConstant[41];
state[42] = state[42] ^ roundConstant[42];
state[43] = state[43] ^ roundConstant[43];
state[44] = state[44] ^ roundConstant[44];
state[45] = state[45] ^ roundConstant[45];
state[46] = state[46] ^ roundConstant[46];
state[47] = state[47] ^ roundConstant[47];
state[48] = state[48] ^ roundConstant[48];
state[49] = state[49] ^ roundConstant[49];
state[50] = state[50] ^ roundConstant[50];
state[51] = state[51] ^ roundConstant[51];
state[52] = state[52] ^ roundConstant[52];
state[53] = state[53] ^ roundConstant[53];
state[54] = state[54] ^ roundConstant[54];
state[55] = state[55] ^ roundConstant[55];
state[56] = state[56] ^ roundConstant[56];
state[57] = state[57] ^ roundConstant[57];
state[58] = state[58] ^ roundConstant[58];
state[59] = state[59] ^ roundConstant[59];
state[60] = state[60] ^ roundConstant[60];
state[61] = state[61] ^ roundConstant[61];
state[62] = state[62] ^ roundConstant[62];
state[63] = state[63] ^ roundConstant[63];
}
void subCells(uint32_t state[64]){ 
uint8_t i;
i = 0;
for(;i < 16;) { 
uint32_t temp_137_rnge[(((i * 4) + 3) - (i * 4)) + 1];
extract_bs_range(temp_137_rnge, state, (i * 4), ((i * 4) + 3));
led(temp_137_rnge);
uint8_t temp_141_init = 0;
uint32_t temp_142_rnge_size = 0;
temp_142_rnge_size = (((i * 4) + 3)-(i * 4)) + 1;
uint8_t temp_147_rng_start = (i * 4);
for(temp_141_init = 0; temp_141_init < temp_142_rnge_size; temp_141_init++, temp_147_rng_start++){
state[temp_147_rng_start] = temp_137_rnge[temp_141_init];
}
i = (i + 1);
} 
}
void step(uint32_t state[64], uint32_t r[6], uint32_t MDS[16][4]){ 
addConstants(state, r);
subCells(state);
shift_row(state);
MixColumnSerial(state, MDS);
}
void enc(uint32_t state[64], uint32_t key[64], uint32_t MDS[16][4], uint32_t RC[32][6]){ 
uint8_t r;
r = 0;
for(;r < 32;) { 
if((r % 4) == 0) { 
state[0] = state[0] ^ key[0];
state[1] = state[1] ^ key[1];
state[2] = state[2] ^ key[2];
state[3] = state[3] ^ key[3];
state[4] = state[4] ^ key[4];
state[5] = state[5] ^ key[5];
state[6] = state[6] ^ key[6];
state[7] = state[7] ^ key[7];
state[8] = state[8] ^ key[8];
state[9] = state[9] ^ key[9];
state[10] = state[10] ^ key[10];
state[11] = state[11] ^ key[11];
state[12] = state[12] ^ key[12];
state[13] = state[13] ^ key[13];
state[14] = state[14] ^ key[14];
state[15] = state[15] ^ key[15];
state[16] = state[16] ^ key[16];
state[17] = state[17] ^ key[17];
state[18] = state[18] ^ key[18];
state[19] = state[19] ^ key[19];
state[20] = state[20] ^ key[20];
state[21] = state[21] ^ key[21];
state[22] = state[22] ^ key[22];
state[23] = state[23] ^ key[23];
state[24] = state[24] ^ key[24];
state[25] = state[25] ^ key[25];
state[26] = state[26] ^ key[26];
state[27] = state[27] ^ key[27];
state[28] = state[28] ^ key[28];
state[29] = state[29] ^ key[29];
state[30] = state[30] ^ key[30];
state[31] = state[31] ^ key[31];
state[32] = state[32] ^ key[32];
state[33] = state[33] ^ key[33];
state[34] = state[34] ^ key[34];
state[35] = state[35] ^ key[35];
state[36] = state[36] ^ key[36];
state[37] = state[37] ^ key[37];
state[38] = state[38] ^ key[38];
state[39] = state[39] ^ key[39];
state[40] = state[40] ^ key[40];
state[41] = state[41] ^ key[41];
state[42] = state[42] ^ key[42];
state[43] = state[43] ^ key[43];
state[44] = state[44] ^ key[44];
state[45] = state[45] ^ key[45];
state[46] = state[46] ^ key[46];
state[47] = state[47] ^ key[47];
state[48] = state[48] ^ key[48];
state[49] = state[49] ^ key[49];
state[50] = state[50] ^ key[50];
state[51] = state[51] ^ key[51];
state[52] = state[52] ^ key[52];
state[53] = state[53] ^ key[53];
state[54] = state[54] ^ key[54];
state[55] = state[55] ^ key[55];
state[56] = state[56] ^ key[56];
state[57] = state[57] ^ key[57];
state[58] = state[58] ^ key[58];
state[59] = state[59] ^ key[59];
state[60] = state[60] ^ key[60];
state[61] = state[61] ^ key[61];
state[62] = state[62] ^ key[62];
state[63] = state[63] ^ key[63];
} 
step(state, RC[r], MDS);
r = (r + 1);
} 
state[0] = state[0] ^ key[0];
state[1] = state[1] ^ key[1];
state[2] = state[2] ^ key[2];
state[3] = state[3] ^ key[3];
state[4] = state[4] ^ key[4];
state[5] = state[5] ^ key[5];
state[6] = state[6] ^ key[6];
state[7] = state[7] ^ key[7];
state[8] = state[8] ^ key[8];
state[9] = state[9] ^ key[9];
state[10] = state[10] ^ key[10];
state[11] = state[11] ^ key[11];
state[12] = state[12] ^ key[12];
state[13] = state[13] ^ key[13];
state[14] = state[14] ^ key[14];
state[15] = state[15] ^ key[15];
state[16] = state[16] ^ key[16];
state[17] = state[17] ^ key[17];
state[18] = state[18] ^ key[18];
state[19] = state[19] ^ key[19];
state[20] = state[20] ^ key[20];
state[21] = state[21] ^ key[21];
state[22] = state[22] ^ key[22];
state[23] = state[23] ^ key[23];
state[24] = state[24] ^ key[24];
state[25] = state[25] ^ key[25];
state[26] = state[26] ^ key[26];
state[27] = state[27] ^ key[27];
state[28] = state[28] ^ key[28];
state[29] = state[29] ^ key[29];
state[30] = state[30] ^ key[30];
state[31] = state[31] ^ key[31];
state[32] = state[32] ^ key[32];
state[33] = state[33] ^ key[33];
state[34] = state[34] ^ key[34];
state[35] = state[35] ^ key[35];
state[36] = state[36] ^ key[36];
state[37] = state[37] ^ key[37];
state[38] = state[38] ^ key[38];
state[39] = state[39] ^ key[39];
state[40] = state[40] ^ key[40];
state[41] = state[41] ^ key[41];
state[42] = state[42] ^ key[42];
state[43] = state[43] ^ key[43];
state[44] = state[44] ^ key[44];
state[45] = state[45] ^ key[45];
state[46] = state[46] ^ key[46];
state[47] = state[47] ^ key[47];
state[48] = state[48] ^ key[48];
state[49] = state[49] ^ key[49];
state[50] = state[50] ^ key[50];
state[51] = state[51] ^ key[51];
state[52] = state[52] ^ key[52];
state[53] = state[53] ^ key[53];
state[54] = state[54] ^ key[54];
state[55] = state[55] ^ key[55];
state[56] = state[56] ^ key[56];
state[57] = state[57] ^ key[57];
state[58] = state[58] ^ key[58];
state[59] = state[59] ^ key[59];
state[60] = state[60] ^ key[60];
state[61] = state[61] ^ key[61];
state[62] = state[62] ^ key[62];
state[63] = state[63] ^ key[63];
}

