#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "present_dsl.h"
uint32_t present_0(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return (((~D & B & A) | (~D & ~C & A) | (D & B & ~A) | (D & C & ~B & A) | (~D & C & ~B & ~A) | (D & ~C & ~A)) & 0x1);
}
uint32_t present_1(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return (((D & C & A) | (~D & ~C & B) | (~D & B & ~A) | (~C & B & ~A) | (D & ~B & A) | (D & ~C & ~B)) & 0x1);
}
uint32_t present_2(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return (((~D & ~C & ~A) | (~C & B & ~A) | (~C & ~B & A) | (D & C & ~B) | (~D & C & B & A) | (D & ~B & A)) & 0x1);
}
uint32_t present_3(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return (((~D & B & A) | (~D & ~B & ~A) | (D & ~C & B) | (~D & C & ~A) | (D & ~C & A) | (~D & C & B)) & 0x1);
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
uint32_t temp[64];
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
uint32_t temp_2__bin = 0;
uint32_t temp_3__bin = 0;
temp_3__bin = 16 * bit;
temp_2__bin = temp_3__bin % 63;
target_bit = temp_2__bin;
if(bit == 63) { 
target_bit = 63;
} 
uint32_t  temp_4_extracted[1] = {0};
temp_4_extracted[0] = temp[bit];
state[target_bit] = temp_4_extracted[0];
uint32_t temp_1__bin = 0;
temp_1__bin = bit + 1;
bit = temp_1__bin;
} 
}
void generate_round_keys(uint32_t key[80], uint32_t round_keys[32][64]){ 
uint8_t round;
round = 1;
for(;round < 33;) {
uint32_t temp_6_rnge[(79 - 16) + 1];
extract_bs_range(temp_6_rnge, key, 16, 79);
uint8_t temp_7_init = 0;
uint32_t temp_8_rnge_size = 0;
temp_8_rnge_size = (63-0) + 1;
uint8_t temp_9_rng_start = 0;
for(temp_7_init = 0; temp_7_init < temp_8_rnge_size; temp_7_init++, temp_9_rng_start++){
uint32_t temp_10__bin = 0;
temp_10__bin = round - 1;
round_keys[temp_10__bin][temp_9_rng_start] = temp_6_rnge[temp_7_init];
}
uint32_t temp_11__bin[80] = {0};
bitslice_shift(temp_11__bin, key, 61, 80, "<<<");
key[0] = temp_11__bin[0];
key[1] = temp_11__bin[1];
key[2] = temp_11__bin[2];
key[3] = temp_11__bin[3];
key[4] = temp_11__bin[4];
key[5] = temp_11__bin[5];
key[6] = temp_11__bin[6];
key[7] = temp_11__bin[7];
key[8] = temp_11__bin[8];
key[9] = temp_11__bin[9];
key[10] = temp_11__bin[10];
key[11] = temp_11__bin[11];
key[12] = temp_11__bin[12];
key[13] = temp_11__bin[13];
key[14] = temp_11__bin[14];
key[15] = temp_11__bin[15];
key[16] = temp_11__bin[16];
key[17] = temp_11__bin[17];
key[18] = temp_11__bin[18];
key[19] = temp_11__bin[19];
key[20] = temp_11__bin[20];
key[21] = temp_11__bin[21];
key[22] = temp_11__bin[22];
key[23] = temp_11__bin[23];
key[24] = temp_11__bin[24];
key[25] = temp_11__bin[25];
key[26] = temp_11__bin[26];
key[27] = temp_11__bin[27];
key[28] = temp_11__bin[28];
key[29] = temp_11__bin[29];
key[30] = temp_11__bin[30];
key[31] = temp_11__bin[31];
key[32] = temp_11__bin[32];
key[33] = temp_11__bin[33];
key[34] = temp_11__bin[34];
key[35] = temp_11__bin[35];
key[36] = temp_11__bin[36];
key[37] = temp_11__bin[37];
key[38] = temp_11__bin[38];
key[39] = temp_11__bin[39];
key[40] = temp_11__bin[40];
key[41] = temp_11__bin[41];
key[42] = temp_11__bin[42];
key[43] = temp_11__bin[43];
key[44] = temp_11__bin[44];
key[45] = temp_11__bin[45];
key[46] = temp_11__bin[46];
key[47] = temp_11__bin[47];
key[48] = temp_11__bin[48];
key[49] = temp_11__bin[49];
key[50] = temp_11__bin[50];
key[51] = temp_11__bin[51];
key[52] = temp_11__bin[52];
key[53] = temp_11__bin[53];
key[54] = temp_11__bin[54];
key[55] = temp_11__bin[55];
key[56] = temp_11__bin[56];
key[57] = temp_11__bin[57];
key[58] = temp_11__bin[58];
key[59] = temp_11__bin[59];
key[60] = temp_11__bin[60];
key[61] = temp_11__bin[61];
key[62] = temp_11__bin[62];
key[63] = temp_11__bin[63];
key[64] = temp_11__bin[64];
key[65] = temp_11__bin[65];
key[66] = temp_11__bin[66];
key[67] = temp_11__bin[67];
key[68] = temp_11__bin[68];
key[69] = temp_11__bin[69];
key[70] = temp_11__bin[70];
key[71] = temp_11__bin[71];
key[72] = temp_11__bin[72];
key[73] = temp_11__bin[73];
key[74] = temp_11__bin[74];
key[75] = temp_11__bin[75];
key[76] = temp_11__bin[76];
key[77] = temp_11__bin[77];
key[78] = temp_11__bin[78];
key[79] = temp_11__bin[79];
uint32_t temp_12_rnge[(79 - 76) + 1];
extract_bs_range(temp_12_rnge, key, 76, 79);
present(temp_12_rnge);
uint8_t temp_13_init = 0;
uint32_t temp_14_rnge_size = 0;
temp_14_rnge_size = (79-76) + 1;
uint8_t temp_15_rng_start = 76;
for(temp_13_init = 0; temp_13_init < temp_14_rnge_size; temp_13_init++, temp_15_rng_start++){
key[temp_15_rng_start] = temp_12_rnge[temp_13_init];
}
uint32_t temp_16__bin[(19 - 15) + 1] = {0};
uint32_t temp_17_rnge[(19 - 15) + 1];
extract_bs_range(temp_17_rnge, key, 15, 19);
uint8_t  temp_18_extracted = 0;
uint8_t temp_19_int_rng_start  = 0;
uint8_t  temp_21_target_bit = 0;
for(;temp_19_int_rng_start < 5;temp_19_int_rng_start++, temp_21_target_bit++){
temp_18_extracted |= (((round >> temp_19_int_rng_start) & 0x1) << temp_21_target_bit);
}
uint32_t temp_22_casted_bs[(19 - 15) + 1]= {0};
int_to_bitsliced(temp_22_casted_bs, temp_18_extracted, (19 - 15) + 1);
bitslice_bitwise(temp_16__bin, temp_17_rnge, temp_22_casted_bs, 80, "^");
uint8_t temp_23_init = 0;
uint32_t temp_24_rnge_size = 0;
temp_24_rnge_size = (19-15) + 1;
uint8_t temp_25_rng_start = 15;
for(temp_23_init = 0; temp_23_init < temp_24_rnge_size; temp_23_init++, temp_25_rng_start++){
key[temp_25_rng_start] = temp_16__bin[temp_23_init];
}
uint32_t temp_5__bin = 0;
temp_5__bin = round + 1;
round = temp_5__bin;
} 
}
void sBox_layer(uint32_t state[64]){ 
uint8_t i;
i = 0;
for(;i < 16;) { 
uint32_t temp_28__bin = 0;
temp_28__bin = i * 4;
uint32_t temp_29__bin = 0;
uint32_t temp_30__bin = 0;
temp_30__bin = i * 4;
temp_29__bin = temp_30__bin + 3;
uint32_t temp_27_rnge[(temp_29__bin - temp_28__bin) + 1];
extract_bs_range(temp_27_rnge, state, temp_28__bin, temp_29__bin);
present(temp_27_rnge);
uint8_t temp_31_init = 0;
uint32_t temp_32_rnge_size = 0;
uint32_t temp_33__bin = 0;
temp_33__bin = i * 4;
uint32_t temp_34__bin = 0;
uint32_t temp_35__bin = 0;
temp_35__bin = i * 4;
temp_34__bin = temp_35__bin + 3;
temp_32_rnge_size = (temp_34__bin-temp_33__bin) + 1;
uint32_t temp_36__bin = 0;
temp_36__bin = i * 4;
uint8_t temp_37_rng_start = temp_36__bin;
for(temp_31_init = 0; temp_31_init < temp_32_rnge_size; temp_31_init++, temp_37_rng_start++){
state[temp_37_rng_start] = temp_27_rnge[temp_31_init];
}
uint32_t temp_26__bin = 0;
temp_26__bin = i + 1;
i = temp_26__bin;
} 
}
uint32_t  (*enc(uint32_t key[80], uint32_t state[64])){ 
uint32_t round_keys[32][64];
generate_round_keys(key, round_keys);
uint8_t round;
round = 0;
for(;round < 31;) { 
uint32_t temp_39__bin[64] = {0};
uint32_t  temp_40_extracted[64] = {0};
temp_40_extracted[0] = round_keys[round][0];
temp_40_extracted[1] = round_keys[round][1];
temp_40_extracted[2] = round_keys[round][2];
temp_40_extracted[3] = round_keys[round][3];
temp_40_extracted[4] = round_keys[round][4];
temp_40_extracted[5] = round_keys[round][5];
temp_40_extracted[6] = round_keys[round][6];
temp_40_extracted[7] = round_keys[round][7];
temp_40_extracted[8] = round_keys[round][8];
temp_40_extracted[9] = round_keys[round][9];
temp_40_extracted[10] = round_keys[round][10];
temp_40_extracted[11] = round_keys[round][11];
temp_40_extracted[12] = round_keys[round][12];
temp_40_extracted[13] = round_keys[round][13];
temp_40_extracted[14] = round_keys[round][14];
temp_40_extracted[15] = round_keys[round][15];
temp_40_extracted[16] = round_keys[round][16];
temp_40_extracted[17] = round_keys[round][17];
temp_40_extracted[18] = round_keys[round][18];
temp_40_extracted[19] = round_keys[round][19];
temp_40_extracted[20] = round_keys[round][20];
temp_40_extracted[21] = round_keys[round][21];
temp_40_extracted[22] = round_keys[round][22];
temp_40_extracted[23] = round_keys[round][23];
temp_40_extracted[24] = round_keys[round][24];
temp_40_extracted[25] = round_keys[round][25];
temp_40_extracted[26] = round_keys[round][26];
temp_40_extracted[27] = round_keys[round][27];
temp_40_extracted[28] = round_keys[round][28];
temp_40_extracted[29] = round_keys[round][29];
temp_40_extracted[30] = round_keys[round][30];
temp_40_extracted[31] = round_keys[round][31];
temp_40_extracted[32] = round_keys[round][32];
temp_40_extracted[33] = round_keys[round][33];
temp_40_extracted[34] = round_keys[round][34];
temp_40_extracted[35] = round_keys[round][35];
temp_40_extracted[36] = round_keys[round][36];
temp_40_extracted[37] = round_keys[round][37];
temp_40_extracted[38] = round_keys[round][38];
temp_40_extracted[39] = round_keys[round][39];
temp_40_extracted[40] = round_keys[round][40];
temp_40_extracted[41] = round_keys[round][41];
temp_40_extracted[42] = round_keys[round][42];
temp_40_extracted[43] = round_keys[round][43];
temp_40_extracted[44] = round_keys[round][44];
temp_40_extracted[45] = round_keys[round][45];
temp_40_extracted[46] = round_keys[round][46];
temp_40_extracted[47] = round_keys[round][47];
temp_40_extracted[48] = round_keys[round][48];
temp_40_extracted[49] = round_keys[round][49];
temp_40_extracted[50] = round_keys[round][50];
temp_40_extracted[51] = round_keys[round][51];
temp_40_extracted[52] = round_keys[round][52];
temp_40_extracted[53] = round_keys[round][53];
temp_40_extracted[54] = round_keys[round][54];
temp_40_extracted[55] = round_keys[round][55];
temp_40_extracted[56] = round_keys[round][56];
temp_40_extracted[57] = round_keys[round][57];
temp_40_extracted[58] = round_keys[round][58];
temp_40_extracted[59] = round_keys[round][59];
temp_40_extracted[60] = round_keys[round][60];
temp_40_extracted[61] = round_keys[round][61];
temp_40_extracted[62] = round_keys[round][62];
temp_40_extracted[63] = round_keys[round][63];
bitslice_bitwise(temp_39__bin, state, temp_40_extracted, 64, "^");
state[0] = temp_39__bin[0];
state[1] = temp_39__bin[1];
state[2] = temp_39__bin[2];
state[3] = temp_39__bin[3];
state[4] = temp_39__bin[4];
state[5] = temp_39__bin[5];
state[6] = temp_39__bin[6];
state[7] = temp_39__bin[7];
state[8] = temp_39__bin[8];
state[9] = temp_39__bin[9];
state[10] = temp_39__bin[10];
state[11] = temp_39__bin[11];
state[12] = temp_39__bin[12];
state[13] = temp_39__bin[13];
state[14] = temp_39__bin[14];
state[15] = temp_39__bin[15];
state[16] = temp_39__bin[16];
state[17] = temp_39__bin[17];
state[18] = temp_39__bin[18];
state[19] = temp_39__bin[19];
state[20] = temp_39__bin[20];
state[21] = temp_39__bin[21];
state[22] = temp_39__bin[22];
state[23] = temp_39__bin[23];
state[24] = temp_39__bin[24];
state[25] = temp_39__bin[25];
state[26] = temp_39__bin[26];
state[27] = temp_39__bin[27];
state[28] = temp_39__bin[28];
state[29] = temp_39__bin[29];
state[30] = temp_39__bin[30];
state[31] = temp_39__bin[31];
state[32] = temp_39__bin[32];
state[33] = temp_39__bin[33];
state[34] = temp_39__bin[34];
state[35] = temp_39__bin[35];
state[36] = temp_39__bin[36];
state[37] = temp_39__bin[37];
state[38] = temp_39__bin[38];
state[39] = temp_39__bin[39];
state[40] = temp_39__bin[40];
state[41] = temp_39__bin[41];
state[42] = temp_39__bin[42];
state[43] = temp_39__bin[43];
state[44] = temp_39__bin[44];
state[45] = temp_39__bin[45];
state[46] = temp_39__bin[46];
state[47] = temp_39__bin[47];
state[48] = temp_39__bin[48];
state[49] = temp_39__bin[49];
state[50] = temp_39__bin[50];
state[51] = temp_39__bin[51];
state[52] = temp_39__bin[52];
state[53] = temp_39__bin[53];
state[54] = temp_39__bin[54];
state[55] = temp_39__bin[55];
state[56] = temp_39__bin[56];
state[57] = temp_39__bin[57];
state[58] = temp_39__bin[58];
state[59] = temp_39__bin[59];
state[60] = temp_39__bin[60];
state[61] = temp_39__bin[61];
state[62] = temp_39__bin[62];
state[63] = temp_39__bin[63];
sBox_layer(state);
pLayer(state);
uint32_t temp_38__bin = 0;
temp_38__bin = round + 1;
round = temp_38__bin;
} 
uint32_t temp_41__bin[64] = {0};
uint32_t  temp_42_extracted[64] = {0};
temp_42_extracted[0] = round_keys[31][0];
temp_42_extracted[1] = round_keys[31][1];
temp_42_extracted[2] = round_keys[31][2];
temp_42_extracted[3] = round_keys[31][3];
temp_42_extracted[4] = round_keys[31][4];
temp_42_extracted[5] = round_keys[31][5];
temp_42_extracted[6] = round_keys[31][6];
temp_42_extracted[7] = round_keys[31][7];
temp_42_extracted[8] = round_keys[31][8];
temp_42_extracted[9] = round_keys[31][9];
temp_42_extracted[10] = round_keys[31][10];
temp_42_extracted[11] = round_keys[31][11];
temp_42_extracted[12] = round_keys[31][12];
temp_42_extracted[13] = round_keys[31][13];
temp_42_extracted[14] = round_keys[31][14];
temp_42_extracted[15] = round_keys[31][15];
temp_42_extracted[16] = round_keys[31][16];
temp_42_extracted[17] = round_keys[31][17];
temp_42_extracted[18] = round_keys[31][18];
temp_42_extracted[19] = round_keys[31][19];
temp_42_extracted[20] = round_keys[31][20];
temp_42_extracted[21] = round_keys[31][21];
temp_42_extracted[22] = round_keys[31][22];
temp_42_extracted[23] = round_keys[31][23];
temp_42_extracted[24] = round_keys[31][24];
temp_42_extracted[25] = round_keys[31][25];
temp_42_extracted[26] = round_keys[31][26];
temp_42_extracted[27] = round_keys[31][27];
temp_42_extracted[28] = round_keys[31][28];
temp_42_extracted[29] = round_keys[31][29];
temp_42_extracted[30] = round_keys[31][30];
temp_42_extracted[31] = round_keys[31][31];
temp_42_extracted[32] = round_keys[31][32];
temp_42_extracted[33] = round_keys[31][33];
temp_42_extracted[34] = round_keys[31][34];
temp_42_extracted[35] = round_keys[31][35];
temp_42_extracted[36] = round_keys[31][36];
temp_42_extracted[37] = round_keys[31][37];
temp_42_extracted[38] = round_keys[31][38];
temp_42_extracted[39] = round_keys[31][39];
temp_42_extracted[40] = round_keys[31][40];
temp_42_extracted[41] = round_keys[31][41];
temp_42_extracted[42] = round_keys[31][42];
temp_42_extracted[43] = round_keys[31][43];
temp_42_extracted[44] = round_keys[31][44];
temp_42_extracted[45] = round_keys[31][45];
temp_42_extracted[46] = round_keys[31][46];
temp_42_extracted[47] = round_keys[31][47];
temp_42_extracted[48] = round_keys[31][48];
temp_42_extracted[49] = round_keys[31][49];
temp_42_extracted[50] = round_keys[31][50];
temp_42_extracted[51] = round_keys[31][51];
temp_42_extracted[52] = round_keys[31][52];
temp_42_extracted[53] = round_keys[31][53];
temp_42_extracted[54] = round_keys[31][54];
temp_42_extracted[55] = round_keys[31][55];
temp_42_extracted[56] = round_keys[31][56];
temp_42_extracted[57] = round_keys[31][57];
temp_42_extracted[58] = round_keys[31][58];
temp_42_extracted[59] = round_keys[31][59];
temp_42_extracted[60] = round_keys[31][60];
temp_42_extracted[61] = round_keys[31][61];
temp_42_extracted[62] = round_keys[31][62];
temp_42_extracted[63] = round_keys[31][63];
bitslice_bitwise(temp_41__bin, state, temp_42_extracted, 64, "^");
state[0] = temp_41__bin[0];
state[1] = temp_41__bin[1];
state[2] = temp_41__bin[2];
state[3] = temp_41__bin[3];
state[4] = temp_41__bin[4];
state[5] = temp_41__bin[5];
state[6] = temp_41__bin[6];
state[7] = temp_41__bin[7];
state[8] = temp_41__bin[8];
state[9] = temp_41__bin[9];
state[10] = temp_41__bin[10];
state[11] = temp_41__bin[11];
state[12] = temp_41__bin[12];
state[13] = temp_41__bin[13];
state[14] = temp_41__bin[14];
state[15] = temp_41__bin[15];
state[16] = temp_41__bin[16];
state[17] = temp_41__bin[17];
state[18] = temp_41__bin[18];
state[19] = temp_41__bin[19];
state[20] = temp_41__bin[20];
state[21] = temp_41__bin[21];
state[22] = temp_41__bin[22];
state[23] = temp_41__bin[23];
state[24] = temp_41__bin[24];
state[25] = temp_41__bin[25];
state[26] = temp_41__bin[26];
state[27] = temp_41__bin[27];
state[28] = temp_41__bin[28];
state[29] = temp_41__bin[29];
state[30] = temp_41__bin[30];
state[31] = temp_41__bin[31];
state[32] = temp_41__bin[32];
state[33] = temp_41__bin[33];
state[34] = temp_41__bin[34];
state[35] = temp_41__bin[35];
state[36] = temp_41__bin[36];
state[37] = temp_41__bin[37];
state[38] = temp_41__bin[38];
state[39] = temp_41__bin[39];
state[40] = temp_41__bin[40];
state[41] = temp_41__bin[41];
state[42] = temp_41__bin[42];
state[43] = temp_41__bin[43];
state[44] = temp_41__bin[44];
state[45] = temp_41__bin[45];
state[46] = temp_41__bin[46];
state[47] = temp_41__bin[47];
state[48] = temp_41__bin[48];
state[49] = temp_41__bin[49];
state[50] = temp_41__bin[50];
state[51] = temp_41__bin[51];
state[52] = temp_41__bin[52];
state[53] = temp_41__bin[53];
state[54] = temp_41__bin[54];
state[55] = temp_41__bin[55];
state[56] = temp_41__bin[56];
state[57] = temp_41__bin[57];
state[58] = temp_41__bin[58];
state[59] = temp_41__bin[59];
state[60] = temp_41__bin[60];
state[61] = temp_41__bin[61];
state[62] = temp_41__bin[62];
state[63] = temp_41__bin[63];
return state;
}

