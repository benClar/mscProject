#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "present_dsl.h"
uint32_t present_0(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((D & ~C & ~A) | (~D & B & A) | (D & B & ~A) | (D & C & ~B & A) | (~D & C & ~B & ~A) | (~D & ~C & A));
}
uint32_t present_1(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((~D & B & ~A) | (D & ~B & A) | (D & ~C & ~A) | (D & C & A) | (~D & ~C & B));
}
uint32_t present_2(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((~D & ~C & ~B) | (D & ~B & A) | (D & C & ~B) | (~C & ~B & A) | (~C & B & ~A) | (~D & C & B & A));
}
uint32_t present_3(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((D & ~C & B) | (~C & B & A) | (~D & C & B) | (D & ~C & A) | (~D & ~B & ~A) | (~D & C & ~A));
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
void pLayer(uint32_t state[64]){ 
uint8_t target_bit;
uint32_t temp[64] = {0};
temp[0] = state[0];
temp[1] = state[1];
temp[2] = state[2];
temp[3] = state[3];
temp[4] = state[4];
temp[5] = state[5];
temp[6] = state[6];
temp[7] = state[7];
temp[8] = state[8];
temp[9] = state[9];
temp[10] = state[10];
temp[11] = state[11];
temp[12] = state[12];
temp[13] = state[13];
temp[14] = state[14];
temp[15] = state[15];
temp[16] = state[16];
temp[17] = state[17];
temp[18] = state[18];
temp[19] = state[19];
temp[20] = state[20];
temp[21] = state[21];
temp[22] = state[22];
temp[23] = state[23];
temp[24] = state[24];
temp[25] = state[25];
temp[26] = state[26];
temp[27] = state[27];
temp[28] = state[28];
temp[29] = state[29];
temp[30] = state[30];
temp[31] = state[31];
temp[32] = state[32];
temp[33] = state[33];
temp[34] = state[34];
temp[35] = state[35];
temp[36] = state[36];
temp[37] = state[37];
temp[38] = state[38];
temp[39] = state[39];
temp[40] = state[40];
temp[41] = state[41];
temp[42] = state[42];
temp[43] = state[43];
temp[44] = state[44];
temp[45] = state[45];
temp[46] = state[46];
temp[47] = state[47];
temp[48] = state[48];
temp[49] = state[49];
temp[50] = state[50];
temp[51] = state[51];
temp[52] = state[52];
temp[53] = state[53];
temp[54] = state[54];
temp[55] = state[55];
temp[56] = state[56];
temp[57] = state[57];
temp[58] = state[58];
temp[59] = state[59];
temp[60] = state[60];
temp[61] = state[61];
temp[62] = state[62];
temp[63] = state[63];
uint8_t bit;
bit = 0;
for(;bit < 64;) { 
target_bit = ((16 * bit) % 63);
if(bit == 63) { 
target_bit = 63;
} 
state[target_bit] = temp[bit];
bit = (bit + 1);
} 
}
void generate_round_keys(uint32_t key[80], uint32_t round_keys[32][64]){ 
uint8_t round;
round = 1;
for(;round < 33;) { 
uint32_t temp_5_rnge[(79 - 16) + 1];
extract_bs_range(temp_5_rnge, key, 16, 79);
round_keys[(round - 1)][0] = temp_5_rnge[0];
round_keys[(round - 1)][1] = temp_5_rnge[1];
round_keys[(round - 1)][2] = temp_5_rnge[2];
round_keys[(round - 1)][3] = temp_5_rnge[3];
round_keys[(round - 1)][4] = temp_5_rnge[4];
round_keys[(round - 1)][5] = temp_5_rnge[5];
round_keys[(round - 1)][6] = temp_5_rnge[6];
round_keys[(round - 1)][7] = temp_5_rnge[7];
round_keys[(round - 1)][8] = temp_5_rnge[8];
round_keys[(round - 1)][9] = temp_5_rnge[9];
round_keys[(round - 1)][10] = temp_5_rnge[10];
round_keys[(round - 1)][11] = temp_5_rnge[11];
round_keys[(round - 1)][12] = temp_5_rnge[12];
round_keys[(round - 1)][13] = temp_5_rnge[13];
round_keys[(round - 1)][14] = temp_5_rnge[14];
round_keys[(round - 1)][15] = temp_5_rnge[15];
round_keys[(round - 1)][16] = temp_5_rnge[16];
round_keys[(round - 1)][17] = temp_5_rnge[17];
round_keys[(round - 1)][18] = temp_5_rnge[18];
round_keys[(round - 1)][19] = temp_5_rnge[19];
round_keys[(round - 1)][20] = temp_5_rnge[20];
round_keys[(round - 1)][21] = temp_5_rnge[21];
round_keys[(round - 1)][22] = temp_5_rnge[22];
round_keys[(round - 1)][23] = temp_5_rnge[23];
round_keys[(round - 1)][24] = temp_5_rnge[24];
round_keys[(round - 1)][25] = temp_5_rnge[25];
round_keys[(round - 1)][26] = temp_5_rnge[26];
round_keys[(round - 1)][27] = temp_5_rnge[27];
round_keys[(round - 1)][28] = temp_5_rnge[28];
round_keys[(round - 1)][29] = temp_5_rnge[29];
round_keys[(round - 1)][30] = temp_5_rnge[30];
round_keys[(round - 1)][31] = temp_5_rnge[31];
round_keys[(round - 1)][32] = temp_5_rnge[32];
round_keys[(round - 1)][33] = temp_5_rnge[33];
round_keys[(round - 1)][34] = temp_5_rnge[34];
round_keys[(round - 1)][35] = temp_5_rnge[35];
round_keys[(round - 1)][36] = temp_5_rnge[36];
round_keys[(round - 1)][37] = temp_5_rnge[37];
round_keys[(round - 1)][38] = temp_5_rnge[38];
round_keys[(round - 1)][39] = temp_5_rnge[39];
round_keys[(round - 1)][40] = temp_5_rnge[40];
round_keys[(round - 1)][41] = temp_5_rnge[41];
round_keys[(round - 1)][42] = temp_5_rnge[42];
round_keys[(round - 1)][43] = temp_5_rnge[43];
round_keys[(round - 1)][44] = temp_5_rnge[44];
round_keys[(round - 1)][45] = temp_5_rnge[45];
round_keys[(round - 1)][46] = temp_5_rnge[46];
round_keys[(round - 1)][47] = temp_5_rnge[47];
round_keys[(round - 1)][48] = temp_5_rnge[48];
round_keys[(round - 1)][49] = temp_5_rnge[49];
round_keys[(round - 1)][50] = temp_5_rnge[50];
round_keys[(round - 1)][51] = temp_5_rnge[51];
round_keys[(round - 1)][52] = temp_5_rnge[52];
round_keys[(round - 1)][53] = temp_5_rnge[53];
round_keys[(round - 1)][54] = temp_5_rnge[54];
round_keys[(round - 1)][55] = temp_5_rnge[55];
round_keys[(round - 1)][56] = temp_5_rnge[56];
round_keys[(round - 1)][57] = temp_5_rnge[57];
round_keys[(round - 1)][58] = temp_5_rnge[58];
round_keys[(round - 1)][59] = temp_5_rnge[59];
round_keys[(round - 1)][60] = temp_5_rnge[60];
round_keys[(round - 1)][61] = temp_5_rnge[61];
round_keys[(round - 1)][62] = temp_5_rnge[62];
round_keys[(round - 1)][63] = temp_5_rnge[63];
uint32_t temp_7__bin[80] = {0};
rotate_right(temp_7__bin, key, 61, 80);
key[0] = temp_7__bin[0];
key[1] = temp_7__bin[1];
key[2] = temp_7__bin[2];
key[3] = temp_7__bin[3];
key[4] = temp_7__bin[4];
key[5] = temp_7__bin[5];
key[6] = temp_7__bin[6];
key[7] = temp_7__bin[7];
key[8] = temp_7__bin[8];
key[9] = temp_7__bin[9];
key[10] = temp_7__bin[10];
key[11] = temp_7__bin[11];
key[12] = temp_7__bin[12];
key[13] = temp_7__bin[13];
key[14] = temp_7__bin[14];
key[15] = temp_7__bin[15];
key[16] = temp_7__bin[16];
key[17] = temp_7__bin[17];
key[18] = temp_7__bin[18];
key[19] = temp_7__bin[19];
key[20] = temp_7__bin[20];
key[21] = temp_7__bin[21];
key[22] = temp_7__bin[22];
key[23] = temp_7__bin[23];
key[24] = temp_7__bin[24];
key[25] = temp_7__bin[25];
key[26] = temp_7__bin[26];
key[27] = temp_7__bin[27];
key[28] = temp_7__bin[28];
key[29] = temp_7__bin[29];
key[30] = temp_7__bin[30];
key[31] = temp_7__bin[31];
key[32] = temp_7__bin[32];
key[33] = temp_7__bin[33];
key[34] = temp_7__bin[34];
key[35] = temp_7__bin[35];
key[36] = temp_7__bin[36];
key[37] = temp_7__bin[37];
key[38] = temp_7__bin[38];
key[39] = temp_7__bin[39];
key[40] = temp_7__bin[40];
key[41] = temp_7__bin[41];
key[42] = temp_7__bin[42];
key[43] = temp_7__bin[43];
key[44] = temp_7__bin[44];
key[45] = temp_7__bin[45];
key[46] = temp_7__bin[46];
key[47] = temp_7__bin[47];
key[48] = temp_7__bin[48];
key[49] = temp_7__bin[49];
key[50] = temp_7__bin[50];
key[51] = temp_7__bin[51];
key[52] = temp_7__bin[52];
key[53] = temp_7__bin[53];
key[54] = temp_7__bin[54];
key[55] = temp_7__bin[55];
key[56] = temp_7__bin[56];
key[57] = temp_7__bin[57];
key[58] = temp_7__bin[58];
key[59] = temp_7__bin[59];
key[60] = temp_7__bin[60];
key[61] = temp_7__bin[61];
key[62] = temp_7__bin[62];
key[63] = temp_7__bin[63];
key[64] = temp_7__bin[64];
key[65] = temp_7__bin[65];
key[66] = temp_7__bin[66];
key[67] = temp_7__bin[67];
key[68] = temp_7__bin[68];
key[69] = temp_7__bin[69];
key[70] = temp_7__bin[70];
key[71] = temp_7__bin[71];
key[72] = temp_7__bin[72];
key[73] = temp_7__bin[73];
key[74] = temp_7__bin[74];
key[75] = temp_7__bin[75];
key[76] = temp_7__bin[76];
key[77] = temp_7__bin[77];
key[78] = temp_7__bin[78];
key[79] = temp_7__bin[79];
uint32_t temp_8_rnge[(79 - 76) + 1];
extract_bs_range(temp_8_rnge, key, 76, 79);
present(temp_8_rnge);
key[76] = temp_8_rnge[0];
key[77] = temp_8_rnge[1];
key[78] = temp_8_rnge[2];
key[79] = temp_8_rnge[3];
uint32_t temp_9__bin[(19 - 15) + 1] = {0};
uint32_t temp_10_rnge[(19 - 15) + 1];
extract_bs_range(temp_10_rnge, key, 15, 19);
uint8_t  temp_11_extracted = 0;
uint8_t temp_12_int_rng_start  = 0;
uint8_t  temp_14_target_bit = 0;
for(;temp_12_int_rng_start < 5;temp_12_int_rng_start++, temp_14_target_bit++){
temp_11_extracted |= ((round >> temp_12_int_rng_start)  << temp_14_target_bit);
}
uint32_t temp_15_casted_bs[(19 - 15) + 1];
int_to_bitsliced(temp_15_casted_bs, temp_11_extracted, (19 - 15) + 1);
XOR(temp_9__bin, temp_10_rnge, temp_15_casted_bs, 80);
key[15] = temp_9__bin[0];
key[16] = temp_9__bin[1];
key[17] = temp_9__bin[2];
key[18] = temp_9__bin[3];
key[19] = temp_9__bin[4];
round = (round + 1);
} 
}
void sBox_layer(uint32_t state[64]){ 
uint8_t i;
i = 0;
for(;i < 16;) { 
uint32_t temp_17_rnge[(((i * 4) + 3) - (i * 4)) + 1];
extract_bs_range(temp_17_rnge, state, (i * 4), ((i * 4) + 3));
present(temp_17_rnge);
uint8_t temp_21_init = 0;
uint32_t temp_22_rnge_size = 0;
temp_22_rnge_size = (((i * 4) + 3)-(i * 4)) + 1;
uint8_t temp_27_rng_start = (i * 4);
for(temp_21_init = 0; temp_21_init < temp_22_rnge_size; temp_21_init++, temp_27_rng_start++){
state[temp_27_rng_start] = temp_17_rnge[temp_21_init];
}
i = (i + 1);
} 
}
void enc(uint32_t key[80], uint32_t state[64]){ 
uint32_t round_keys[32][64];
generate_round_keys(key, round_keys);
uint8_t round;
round = 0;
for(;round < 31;) { 
uint32_t temp_29__bin[64] = {0};
XOR(temp_29__bin, state, round_keys[round], 64);
state[0] = temp_29__bin[0];
state[1] = temp_29__bin[1];
state[2] = temp_29__bin[2];
state[3] = temp_29__bin[3];
state[4] = temp_29__bin[4];
state[5] = temp_29__bin[5];
state[6] = temp_29__bin[6];
state[7] = temp_29__bin[7];
state[8] = temp_29__bin[8];
state[9] = temp_29__bin[9];
state[10] = temp_29__bin[10];
state[11] = temp_29__bin[11];
state[12] = temp_29__bin[12];
state[13] = temp_29__bin[13];
state[14] = temp_29__bin[14];
state[15] = temp_29__bin[15];
state[16] = temp_29__bin[16];
state[17] = temp_29__bin[17];
state[18] = temp_29__bin[18];
state[19] = temp_29__bin[19];
state[20] = temp_29__bin[20];
state[21] = temp_29__bin[21];
state[22] = temp_29__bin[22];
state[23] = temp_29__bin[23];
state[24] = temp_29__bin[24];
state[25] = temp_29__bin[25];
state[26] = temp_29__bin[26];
state[27] = temp_29__bin[27];
state[28] = temp_29__bin[28];
state[29] = temp_29__bin[29];
state[30] = temp_29__bin[30];
state[31] = temp_29__bin[31];
state[32] = temp_29__bin[32];
state[33] = temp_29__bin[33];
state[34] = temp_29__bin[34];
state[35] = temp_29__bin[35];
state[36] = temp_29__bin[36];
state[37] = temp_29__bin[37];
state[38] = temp_29__bin[38];
state[39] = temp_29__bin[39];
state[40] = temp_29__bin[40];
state[41] = temp_29__bin[41];
state[42] = temp_29__bin[42];
state[43] = temp_29__bin[43];
state[44] = temp_29__bin[44];
state[45] = temp_29__bin[45];
state[46] = temp_29__bin[46];
state[47] = temp_29__bin[47];
state[48] = temp_29__bin[48];
state[49] = temp_29__bin[49];
state[50] = temp_29__bin[50];
state[51] = temp_29__bin[51];
state[52] = temp_29__bin[52];
state[53] = temp_29__bin[53];
state[54] = temp_29__bin[54];
state[55] = temp_29__bin[55];
state[56] = temp_29__bin[56];
state[57] = temp_29__bin[57];
state[58] = temp_29__bin[58];
state[59] = temp_29__bin[59];
state[60] = temp_29__bin[60];
state[61] = temp_29__bin[61];
state[62] = temp_29__bin[62];
state[63] = temp_29__bin[63];
sBox_layer(state);
pLayer(state);
round = (round + 1);
} 
uint32_t temp_30__bin[64] = {0};
XOR(temp_30__bin, state, round_keys[31], 64);
state[0] = temp_30__bin[0];
state[1] = temp_30__bin[1];
state[2] = temp_30__bin[2];
state[3] = temp_30__bin[3];
state[4] = temp_30__bin[4];
state[5] = temp_30__bin[5];
state[6] = temp_30__bin[6];
state[7] = temp_30__bin[7];
state[8] = temp_30__bin[8];
state[9] = temp_30__bin[9];
state[10] = temp_30__bin[10];
state[11] = temp_30__bin[11];
state[12] = temp_30__bin[12];
state[13] = temp_30__bin[13];
state[14] = temp_30__bin[14];
state[15] = temp_30__bin[15];
state[16] = temp_30__bin[16];
state[17] = temp_30__bin[17];
state[18] = temp_30__bin[18];
state[19] = temp_30__bin[19];
state[20] = temp_30__bin[20];
state[21] = temp_30__bin[21];
state[22] = temp_30__bin[22];
state[23] = temp_30__bin[23];
state[24] = temp_30__bin[24];
state[25] = temp_30__bin[25];
state[26] = temp_30__bin[26];
state[27] = temp_30__bin[27];
state[28] = temp_30__bin[28];
state[29] = temp_30__bin[29];
state[30] = temp_30__bin[30];
state[31] = temp_30__bin[31];
state[32] = temp_30__bin[32];
state[33] = temp_30__bin[33];
state[34] = temp_30__bin[34];
state[35] = temp_30__bin[35];
state[36] = temp_30__bin[36];
state[37] = temp_30__bin[37];
state[38] = temp_30__bin[38];
state[39] = temp_30__bin[39];
state[40] = temp_30__bin[40];
state[41] = temp_30__bin[41];
state[42] = temp_30__bin[42];
state[43] = temp_30__bin[43];
state[44] = temp_30__bin[44];
state[45] = temp_30__bin[45];
state[46] = temp_30__bin[46];
state[47] = temp_30__bin[47];
state[48] = temp_30__bin[48];
state[49] = temp_30__bin[49];
state[50] = temp_30__bin[50];
state[51] = temp_30__bin[51];
state[52] = temp_30__bin[52];
state[53] = temp_30__bin[53];
state[54] = temp_30__bin[54];
state[55] = temp_30__bin[55];
state[56] = temp_30__bin[56];
state[57] = temp_30__bin[57];
state[58] = temp_30__bin[58];
state[59] = temp_30__bin[59];
state[60] = temp_30__bin[60];
state[61] = temp_30__bin[61];
state[62] = temp_30__bin[62];
state[63] = temp_30__bin[63];
}

