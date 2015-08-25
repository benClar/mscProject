#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "led_dsl.h"
uint32_t led_0(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((~D & C & ~B & ~A) | (~D & B & A) | (D & C & ~B & A) | (D & B & ~A) | (~D & ~C & A) | (D & ~C & ~A));
}
uint32_t led_1(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((D & C & A) | (~D & ~C & B) | (D & ~B & A) | (D & ~C & ~B) | (~D & B & ~A) | (~C & B & ~A));
}
uint32_t led_2(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((~D & ~C & ~A) | (D & ~B & A) | (~C & ~B & A) | (~D & C & B & A) | (D & C & ~B) | (~C & B & ~A));
}
uint32_t led_3(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((~D & C & B) | (~C & B & A) | (~D & ~B & ~A) | (~D & C & ~A) | (D & ~C & A) | (D & ~C & B));
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
void  gmMult(uint32_t *temp_1_bs_return, uint32_t a[4], uint32_t b[4]){ 
uint32_t output[4] = {0};
output[0]= 0;
output[1]= 0;
output[2]= 0;
output[3]= 0;
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
uint32_t mask[4] = {0};
uint32_t f[1] = {0};
uint32_t high[1] = {0};
high[0]= 0;
uint8_t bit = 0;
bit = 0;
uint8_t degree = 0;
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
uint32_t temp_5__bin[8] = {0};
shift_right(temp_5__bin, a_out, 1, 8);
a_out[0] = temp_5__bin[0];
a_out[1] = temp_5__bin[1];
a_out[2] = temp_5__bin[2];
a_out[3] = temp_5__bin[3];
bit = 0;
for(;bit < 4;) { 
a_out[bit] = (a_out[bit] ^ (high[0] & GF_R[bit]));
bit = (bit + 1);
} 
uint32_t temp_7__bin[8] = {0};
shift_left(temp_7__bin, b_out, 1, 8);
b_out[0] = temp_7__bin[0];
b_out[1] = temp_7__bin[1];
b_out[2] = temp_7__bin[2];
b_out[3] = temp_7__bin[3];
degree = (degree + 1);
} 
temp_1_bs_return[0] = output[0];
temp_1_bs_return[1] = output[1];
temp_1_bs_return[2] = output[2];
temp_1_bs_return[3] = output[3];
}
void MixColumnSerial(uint32_t state[64], uint32_t MDS[16][4]){ 
uint32_t column[4][4] = {{ 0 }};
uint8_t col = 0;
col = 0;
for(;col < 4;) { 
uint32_t temp_10_rnge[(((col * 4) + 3) - (col * 4)) + 1];
extract_bs_range(temp_10_rnge, state, (col * 4), ((col * 4) + 3));
column[0][0] = temp_10_rnge[0];
column[0][1] = temp_10_rnge[1];
column[0][2] = temp_10_rnge[2];
column[0][3] = temp_10_rnge[3];
uint32_t temp_14_rnge[((((col + 4) * 4) + 3) - ((col + 4) * 4)) + 1];
extract_bs_range(temp_14_rnge, state, ((col + 4) * 4), (((col + 4) * 4) + 3));
column[1][0] = temp_14_rnge[0];
column[1][1] = temp_14_rnge[1];
column[1][2] = temp_14_rnge[2];
column[1][3] = temp_14_rnge[3];
uint32_t temp_20_rnge[((((col + 8) * 4) + 3) - ((col + 8) * 4)) + 1];
extract_bs_range(temp_20_rnge, state, ((col + 8) * 4), (((col + 8) * 4) + 3));
column[2][0] = temp_20_rnge[0];
column[2][1] = temp_20_rnge[1];
column[2][2] = temp_20_rnge[2];
column[2][3] = temp_20_rnge[3];
uint32_t temp_26_rnge[((((col + 12) * 4) + 3) - ((col + 12) * 4)) + 1];
extract_bs_range(temp_26_rnge, state, ((col + 12) * 4), (((col + 12) * 4) + 3));
column[3][0] = temp_26_rnge[0];
column[3][1] = temp_26_rnge[1];
column[3][2] = temp_26_rnge[2];
column[3][3] = temp_26_rnge[3];
uint8_t col_nibble = 0;
col_nibble = 0;
for(;col_nibble < 4;) { 
uint32_t temp_33__bin[4] = {0};
uint32_t temp_34__bin[4] = {0};
uint32_t temp_35__bin[4] = {0};
uint32_t temp_36_call[4];
gmMult(temp_36_call, MDS[(col_nibble * 4)], column[0]);
uint32_t temp_38_call[4];
gmMult(temp_38_call, MDS[((col_nibble * 4) + 1)], column[1]);
XOR(temp_35__bin, temp_36_call, temp_38_call, 4);
uint32_t temp_41_call[4];
gmMult(temp_41_call, MDS[((col_nibble * 4) + 2)], column[2]);
XOR(temp_34__bin, temp_35__bin, temp_41_call, 4);
uint32_t temp_44_call[4];
gmMult(temp_44_call, MDS[((col_nibble * 4) + 3)], column[3]);
XOR(temp_33__bin, temp_34__bin, temp_44_call, 4);
uint8_t temp_47_init = 0;
uint32_t temp_48_rnge_size = 0;
temp_48_rnge_size = ((((col * 4) + (col_nibble * 16)) + 3)-((col * 4) + (col_nibble * 16))) + 1;
uint8_t temp_59_rng_start = ((col * 4) + (col_nibble * 16));
for(temp_47_init = 0; temp_47_init < temp_48_rnge_size; temp_47_init++, temp_59_rng_start++){
state[temp_59_rng_start] = temp_33__bin[temp_47_init];
}
col_nibble = (col_nibble + 1);
} 
col = (col + 1);
} 
}
void shift_row(uint32_t state[64]){ 
uint32_t temp_60__bin[(31 - 16) + 1] = {0};
uint32_t temp_61_rnge[(31 - 16) + 1];
extract_bs_range(temp_61_rnge, state, 16, 31);
rotate_left(temp_60__bin, temp_61_rnge, 4, (31 - 16) + 1);
state[16] = temp_60__bin[0];
state[17] = temp_60__bin[1];
state[18] = temp_60__bin[2];
state[19] = temp_60__bin[3];
state[20] = temp_60__bin[4];
state[21] = temp_60__bin[5];
state[22] = temp_60__bin[6];
state[23] = temp_60__bin[7];
state[24] = temp_60__bin[8];
state[25] = temp_60__bin[9];
state[26] = temp_60__bin[10];
state[27] = temp_60__bin[11];
state[28] = temp_60__bin[12];
state[29] = temp_60__bin[13];
state[30] = temp_60__bin[14];
state[31] = temp_60__bin[15];
uint32_t temp_62__bin[(47 - 32) + 1] = {0};
uint32_t temp_63_rnge[(47 - 32) + 1];
extract_bs_range(temp_63_rnge, state, 32, 47);
rotate_left(temp_62__bin, temp_63_rnge, 8, (47 - 32) + 1);
state[32] = temp_62__bin[0];
state[33] = temp_62__bin[1];
state[34] = temp_62__bin[2];
state[35] = temp_62__bin[3];
state[36] = temp_62__bin[4];
state[37] = temp_62__bin[5];
state[38] = temp_62__bin[6];
state[39] = temp_62__bin[7];
state[40] = temp_62__bin[8];
state[41] = temp_62__bin[9];
state[42] = temp_62__bin[10];
state[43] = temp_62__bin[11];
state[44] = temp_62__bin[12];
state[45] = temp_62__bin[13];
state[46] = temp_62__bin[14];
state[47] = temp_62__bin[15];
uint32_t temp_64__bin[(63 - 48) + 1] = {0};
uint32_t temp_65_rnge[(63 - 48) + 1];
extract_bs_range(temp_65_rnge, state, 48, 63);
rotate_left(temp_64__bin, temp_65_rnge, 12, (63 - 48) + 1);
state[48] = temp_64__bin[0];
state[49] = temp_64__bin[1];
state[50] = temp_64__bin[2];
state[51] = temp_64__bin[3];
state[52] = temp_64__bin[4];
state[53] = temp_64__bin[5];
state[54] = temp_64__bin[6];
state[55] = temp_64__bin[7];
state[56] = temp_64__bin[8];
state[57] = temp_64__bin[9];
state[58] = temp_64__bin[10];
state[59] = temp_64__bin[11];
state[60] = temp_64__bin[12];
state[61] = temp_64__bin[13];
state[62] = temp_64__bin[14];
state[63] = temp_64__bin[15];
}
void addConstants(uint32_t state[64], uint32_t constant[6]){ 
uint32_t roundConstant[64] = {0};
uint8_t row = 0;
row = 0;
for(;row < 4;) { 
uint8_t  temp_67_extracted = 0;
uint8_t temp_68_int_rng_start  = 0;
uint8_t  temp_70_target_bit = 0;
for(;temp_68_int_rng_start < 3;temp_68_int_rng_start++, temp_70_target_bit++){
temp_67_extracted |= ((row >> temp_68_int_rng_start)  << temp_70_target_bit);
}
uint32_t temp_71_cast_bs_seq[(((row * 16) + 3) - (row * 16)) + 1];
int_to_bitsliced(temp_71_cast_bs_seq, temp_67_extracted, (((row * 16) + 3) - (row * 16)) + 1);
uint8_t temp_75_init = 0;
uint32_t temp_76_rnge_size = 0;
temp_76_rnge_size = (((row * 16) + 3)-(row * 16)) + 1;
uint8_t temp_81_rng_start = (row * 16);
for(temp_75_init = 0; temp_75_init < temp_76_rnge_size; temp_75_init++, temp_81_rng_start++){
roundConstant[temp_81_rng_start] = temp_71_cast_bs_seq[temp_75_init];
}
if(row == 0 || row == 2) { 
uint32_t temp_82_rnge[(5 - 3) + 1];
extract_bs_range(temp_82_rnge, constant, 3, 5);
uint8_t temp_83_init = 0;
uint32_t temp_84_rnge_size = 0;
temp_84_rnge_size = (((row * 16) + 6)-((row * 16) + 4)) + 1;
uint8_t temp_91_rng_start = ((row * 16) + 4);
for(temp_83_init = 0; temp_83_init < temp_84_rnge_size; temp_83_init++, temp_91_rng_start++){
roundConstant[temp_91_rng_start] = temp_82_rnge[temp_83_init];
}
} 
if(row == 1 || row == 3) { 
uint32_t temp_92_rnge[(2 - 0) + 1];
extract_bs_range(temp_92_rnge, constant, 0, 2);
uint8_t temp_93_init = 0;
uint32_t temp_94_rnge_size = 0;
temp_94_rnge_size = (((row * 16) + 6)-((row * 16) + 4)) + 1;
uint8_t temp_101_rng_start = ((row * 16) + 4);
for(temp_93_init = 0; temp_93_init < temp_94_rnge_size; temp_93_init++, temp_101_rng_start++){
roundConstant[temp_101_rng_start] = temp_92_rnge[temp_93_init];
}
} 
uint32_t temp_102_cast_bs_seq[(((row * 16) + 15) - ((row * 16) + 8)) + 1];
int_to_bitsliced(temp_102_cast_bs_seq, 0, (((row * 16) + 15) - ((row * 16) + 8)) + 1);
uint8_t temp_107_init = 0;
uint32_t temp_108_rnge_size = 0;
temp_108_rnge_size = (((row * 16) + 15)-((row * 16) + 8)) + 1;
uint8_t temp_115_rng_start = ((row * 16) + 8);
for(temp_107_init = 0; temp_107_init < temp_108_rnge_size; temp_107_init++, temp_115_rng_start++){
roundConstant[temp_115_rng_start] = temp_102_cast_bs_seq[temp_107_init];
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
uint8_t i = 0;
i = 0;
for(;i < 16;) { 
uint32_t temp_117_rnge[(((i * 4) + 3) - (i * 4)) + 1];
extract_bs_range(temp_117_rnge, state, (i * 4), ((i * 4) + 3));
led(temp_117_rnge);
uint8_t temp_121_init = 0;
uint32_t temp_122_rnge_size = 0;
temp_122_rnge_size = (((i * 4) + 3)-(i * 4)) + 1;
uint8_t temp_127_rng_start = (i * 4);
for(temp_121_init = 0; temp_121_init < temp_122_rnge_size; temp_121_init++, temp_127_rng_start++){
state[temp_127_rng_start] = temp_117_rnge[temp_121_init];
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
uint8_t r = 0;
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

