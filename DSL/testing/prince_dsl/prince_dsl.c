#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "prince_dsl.h"
uint32_t prince_0(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((~D & C & B) | (C & B & ~A) | (~C & ~B & A) | (~D & B & ~A) | (~D & ~C & ~A) | (D & ~B & A));
}
uint32_t prince_1(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((~D & ~C) | (~C & ~B) | (~B & ~A));
}
uint32_t prince_2(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((D & C) | (~B & A) | (D & ~B));
}
uint32_t prince_3(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((~D & ~B) | (D & B & ~A) | (C & ~A));
}
void prince(uint32_t input[4]){
uint32_t temp_0_sbox_out[4];
temp_0_sbox_out[0] = prince_0(input[0], input[1], input[2], input[3]);
temp_0_sbox_out[1] = prince_1(input[0], input[1], input[2], input[3]);
temp_0_sbox_out[2] = prince_2(input[0], input[1], input[2], input[3]);
temp_0_sbox_out[3] = prince_3(input[0], input[1], input[2], input[3]);
input[0] = temp_0_sbox_out[0];
input[1] = temp_0_sbox_out[1];
input[2] = temp_0_sbox_out[2];
input[3] = temp_0_sbox_out[3];
}
uint32_t prince_inv_0(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((C & ~B & ~A) | (~D & ~B) | (C & B & A) | (~D & ~C & ~A));
}
uint32_t prince_inv_1(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((~D & ~C) | (~C & ~B) | (~D & ~B & ~A) | (D & ~B & A));
}
uint32_t prince_inv_2(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((D & C & ~A) | (C & ~B) | (~B & A) | (D & B & ~A));
}
uint32_t prince_inv_3(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return ((~C & ~B & ~A) | (C & ~B & A) | (~D & C) | (C & B & ~A));
}
void prince_inv(uint32_t input[4]){
uint32_t temp_1_sbox_out[4];
temp_1_sbox_out[0] = prince_inv_0(input[0], input[1], input[2], input[3]);
temp_1_sbox_out[1] = prince_inv_1(input[0], input[1], input[2], input[3]);
temp_1_sbox_out[2] = prince_inv_2(input[0], input[1], input[2], input[3]);
temp_1_sbox_out[3] = prince_inv_3(input[0], input[1], input[2], input[3]);
input[0] = temp_1_sbox_out[0];
input[1] = temp_1_sbox_out[1];
input[2] = temp_1_sbox_out[2];
input[3] = temp_1_sbox_out[3];
}
void enc(uint32_t RC[12][64], uint32_t state[64], uint32_t key_0[64], uint32_t key_1[64]){ 
uint32_t key_prime[64] = {0};
uint32_t temp_2__bin[64] = {0};
uint32_t temp_3__bin[64] = {0};
rotate_left(temp_3__bin, key_0, 1, 64);
uint32_t temp_4__bin[64] = {0};
shift_left(temp_4__bin, key_0, 63, 64);
XOR(temp_2__bin, temp_3__bin, temp_4__bin, 64);
key_prime[0] = temp_2__bin[0];
key_prime[1] = temp_2__bin[1];
key_prime[2] = temp_2__bin[2];
key_prime[3] = temp_2__bin[3];
key_prime[4] = temp_2__bin[4];
key_prime[5] = temp_2__bin[5];
key_prime[6] = temp_2__bin[6];
key_prime[7] = temp_2__bin[7];
key_prime[8] = temp_2__bin[8];
key_prime[9] = temp_2__bin[9];
key_prime[10] = temp_2__bin[10];
key_prime[11] = temp_2__bin[11];
key_prime[12] = temp_2__bin[12];
key_prime[13] = temp_2__bin[13];
key_prime[14] = temp_2__bin[14];
key_prime[15] = temp_2__bin[15];
key_prime[16] = temp_2__bin[16];
key_prime[17] = temp_2__bin[17];
key_prime[18] = temp_2__bin[18];
key_prime[19] = temp_2__bin[19];
key_prime[20] = temp_2__bin[20];
key_prime[21] = temp_2__bin[21];
key_prime[22] = temp_2__bin[22];
key_prime[23] = temp_2__bin[23];
key_prime[24] = temp_2__bin[24];
key_prime[25] = temp_2__bin[25];
key_prime[26] = temp_2__bin[26];
key_prime[27] = temp_2__bin[27];
key_prime[28] = temp_2__bin[28];
key_prime[29] = temp_2__bin[29];
key_prime[30] = temp_2__bin[30];
key_prime[31] = temp_2__bin[31];
key_prime[32] = temp_2__bin[32];
key_prime[33] = temp_2__bin[33];
key_prime[34] = temp_2__bin[34];
key_prime[35] = temp_2__bin[35];
key_prime[36] = temp_2__bin[36];
key_prime[37] = temp_2__bin[37];
key_prime[38] = temp_2__bin[38];
key_prime[39] = temp_2__bin[39];
key_prime[40] = temp_2__bin[40];
key_prime[41] = temp_2__bin[41];
key_prime[42] = temp_2__bin[42];
key_prime[43] = temp_2__bin[43];
key_prime[44] = temp_2__bin[44];
key_prime[45] = temp_2__bin[45];
key_prime[46] = temp_2__bin[46];
key_prime[47] = temp_2__bin[47];
key_prime[48] = temp_2__bin[48];
key_prime[49] = temp_2__bin[49];
key_prime[50] = temp_2__bin[50];
key_prime[51] = temp_2__bin[51];
key_prime[52] = temp_2__bin[52];
key_prime[53] = temp_2__bin[53];
key_prime[54] = temp_2__bin[54];
key_prime[55] = temp_2__bin[55];
key_prime[56] = temp_2__bin[56];
key_prime[57] = temp_2__bin[57];
key_prime[58] = temp_2__bin[58];
key_prime[59] = temp_2__bin[59];
key_prime[60] = temp_2__bin[60];
key_prime[61] = temp_2__bin[61];
key_prime[62] = temp_2__bin[62];
key_prime[63] = temp_2__bin[63];
state[0] = state[0] ^ key_0[0];
state[1] = state[1] ^ key_0[1];
state[2] = state[2] ^ key_0[2];
state[3] = state[3] ^ key_0[3];
state[4] = state[4] ^ key_0[4];
state[5] = state[5] ^ key_0[5];
state[6] = state[6] ^ key_0[6];
state[7] = state[7] ^ key_0[7];
state[8] = state[8] ^ key_0[8];
state[9] = state[9] ^ key_0[9];
state[10] = state[10] ^ key_0[10];
state[11] = state[11] ^ key_0[11];
state[12] = state[12] ^ key_0[12];
state[13] = state[13] ^ key_0[13];
state[14] = state[14] ^ key_0[14];
state[15] = state[15] ^ key_0[15];
state[16] = state[16] ^ key_0[16];
state[17] = state[17] ^ key_0[17];
state[18] = state[18] ^ key_0[18];
state[19] = state[19] ^ key_0[19];
state[20] = state[20] ^ key_0[20];
state[21] = state[21] ^ key_0[21];
state[22] = state[22] ^ key_0[22];
state[23] = state[23] ^ key_0[23];
state[24] = state[24] ^ key_0[24];
state[25] = state[25] ^ key_0[25];
state[26] = state[26] ^ key_0[26];
state[27] = state[27] ^ key_0[27];
state[28] = state[28] ^ key_0[28];
state[29] = state[29] ^ key_0[29];
state[30] = state[30] ^ key_0[30];
state[31] = state[31] ^ key_0[31];
state[32] = state[32] ^ key_0[32];
state[33] = state[33] ^ key_0[33];
state[34] = state[34] ^ key_0[34];
state[35] = state[35] ^ key_0[35];
state[36] = state[36] ^ key_0[36];
state[37] = state[37] ^ key_0[37];
state[38] = state[38] ^ key_0[38];
state[39] = state[39] ^ key_0[39];
state[40] = state[40] ^ key_0[40];
state[41] = state[41] ^ key_0[41];
state[42] = state[42] ^ key_0[42];
state[43] = state[43] ^ key_0[43];
state[44] = state[44] ^ key_0[44];
state[45] = state[45] ^ key_0[45];
state[46] = state[46] ^ key_0[46];
state[47] = state[47] ^ key_0[47];
state[48] = state[48] ^ key_0[48];
state[49] = state[49] ^ key_0[49];
state[50] = state[50] ^ key_0[50];
state[51] = state[51] ^ key_0[51];
state[52] = state[52] ^ key_0[52];
state[53] = state[53] ^ key_0[53];
state[54] = state[54] ^ key_0[54];
state[55] = state[55] ^ key_0[55];
state[56] = state[56] ^ key_0[56];
state[57] = state[57] ^ key_0[57];
state[58] = state[58] ^ key_0[58];
state[59] = state[59] ^ key_0[59];
state[60] = state[60] ^ key_0[60];
state[61] = state[61] ^ key_0[61];
state[62] = state[62] ^ key_0[62];
state[63] = state[63] ^ key_0[63];
state[0] = (state[0] ^ RC[0][0]) ^ key_1[0];
state[1] = (state[1] ^ RC[0][1]) ^ key_1[1];
state[2] = (state[2] ^ RC[0][2]) ^ key_1[2];
state[3] = (state[3] ^ RC[0][3]) ^ key_1[3];
state[4] = (state[4] ^ RC[0][4]) ^ key_1[4];
state[5] = (state[5] ^ RC[0][5]) ^ key_1[5];
state[6] = (state[6] ^ RC[0][6]) ^ key_1[6];
state[7] = (state[7] ^ RC[0][7]) ^ key_1[7];
state[8] = (state[8] ^ RC[0][8]) ^ key_1[8];
state[9] = (state[9] ^ RC[0][9]) ^ key_1[9];
state[10] = (state[10] ^ RC[0][10]) ^ key_1[10];
state[11] = (state[11] ^ RC[0][11]) ^ key_1[11];
state[12] = (state[12] ^ RC[0][12]) ^ key_1[12];
state[13] = (state[13] ^ RC[0][13]) ^ key_1[13];
state[14] = (state[14] ^ RC[0][14]) ^ key_1[14];
state[15] = (state[15] ^ RC[0][15]) ^ key_1[15];
state[16] = (state[16] ^ RC[0][16]) ^ key_1[16];
state[17] = (state[17] ^ RC[0][17]) ^ key_1[17];
state[18] = (state[18] ^ RC[0][18]) ^ key_1[18];
state[19] = (state[19] ^ RC[0][19]) ^ key_1[19];
state[20] = (state[20] ^ RC[0][20]) ^ key_1[20];
state[21] = (state[21] ^ RC[0][21]) ^ key_1[21];
state[22] = (state[22] ^ RC[0][22]) ^ key_1[22];
state[23] = (state[23] ^ RC[0][23]) ^ key_1[23];
state[24] = (state[24] ^ RC[0][24]) ^ key_1[24];
state[25] = (state[25] ^ RC[0][25]) ^ key_1[25];
state[26] = (state[26] ^ RC[0][26]) ^ key_1[26];
state[27] = (state[27] ^ RC[0][27]) ^ key_1[27];
state[28] = (state[28] ^ RC[0][28]) ^ key_1[28];
state[29] = (state[29] ^ RC[0][29]) ^ key_1[29];
state[30] = (state[30] ^ RC[0][30]) ^ key_1[30];
state[31] = (state[31] ^ RC[0][31]) ^ key_1[31];
state[32] = (state[32] ^ RC[0][32]) ^ key_1[32];
state[33] = (state[33] ^ RC[0][33]) ^ key_1[33];
state[34] = (state[34] ^ RC[0][34]) ^ key_1[34];
state[35] = (state[35] ^ RC[0][35]) ^ key_1[35];
state[36] = (state[36] ^ RC[0][36]) ^ key_1[36];
state[37] = (state[37] ^ RC[0][37]) ^ key_1[37];
state[38] = (state[38] ^ RC[0][38]) ^ key_1[38];
state[39] = (state[39] ^ RC[0][39]) ^ key_1[39];
state[40] = (state[40] ^ RC[0][40]) ^ key_1[40];
state[41] = (state[41] ^ RC[0][41]) ^ key_1[41];
state[42] = (state[42] ^ RC[0][42]) ^ key_1[42];
state[43] = (state[43] ^ RC[0][43]) ^ key_1[43];
state[44] = (state[44] ^ RC[0][44]) ^ key_1[44];
state[45] = (state[45] ^ RC[0][45]) ^ key_1[45];
state[46] = (state[46] ^ RC[0][46]) ^ key_1[46];
state[47] = (state[47] ^ RC[0][47]) ^ key_1[47];
state[48] = (state[48] ^ RC[0][48]) ^ key_1[48];
state[49] = (state[49] ^ RC[0][49]) ^ key_1[49];
state[50] = (state[50] ^ RC[0][50]) ^ key_1[50];
state[51] = (state[51] ^ RC[0][51]) ^ key_1[51];
state[52] = (state[52] ^ RC[0][52]) ^ key_1[52];
state[53] = (state[53] ^ RC[0][53]) ^ key_1[53];
state[54] = (state[54] ^ RC[0][54]) ^ key_1[54];
state[55] = (state[55] ^ RC[0][55]) ^ key_1[55];
state[56] = (state[56] ^ RC[0][56]) ^ key_1[56];
state[57] = (state[57] ^ RC[0][57]) ^ key_1[57];
state[58] = (state[58] ^ RC[0][58]) ^ key_1[58];
state[59] = (state[59] ^ RC[0][59]) ^ key_1[59];
state[60] = (state[60] ^ RC[0][60]) ^ key_1[60];
state[61] = (state[61] ^ RC[0][61]) ^ key_1[61];
state[62] = (state[62] ^ RC[0][62]) ^ key_1[62];
state[63] = (state[63] ^ RC[0][63]) ^ key_1[63];
first_rounds(state, key_1, RC);
sBox_layer(state);
mPrime(state);
sBox_layer_inv(state);
last_rounds(state, key_1, RC);
state[0] = (RC[11][0] ^ key_1[0]) ^ state[0];
state[1] = (RC[11][1] ^ key_1[1]) ^ state[1];
state[2] = (RC[11][2] ^ key_1[2]) ^ state[2];
state[3] = (RC[11][3] ^ key_1[3]) ^ state[3];
state[4] = (RC[11][4] ^ key_1[4]) ^ state[4];
state[5] = (RC[11][5] ^ key_1[5]) ^ state[5];
state[6] = (RC[11][6] ^ key_1[6]) ^ state[6];
state[7] = (RC[11][7] ^ key_1[7]) ^ state[7];
state[8] = (RC[11][8] ^ key_1[8]) ^ state[8];
state[9] = (RC[11][9] ^ key_1[9]) ^ state[9];
state[10] = (RC[11][10] ^ key_1[10]) ^ state[10];
state[11] = (RC[11][11] ^ key_1[11]) ^ state[11];
state[12] = (RC[11][12] ^ key_1[12]) ^ state[12];
state[13] = (RC[11][13] ^ key_1[13]) ^ state[13];
state[14] = (RC[11][14] ^ key_1[14]) ^ state[14];
state[15] = (RC[11][15] ^ key_1[15]) ^ state[15];
state[16] = (RC[11][16] ^ key_1[16]) ^ state[16];
state[17] = (RC[11][17] ^ key_1[17]) ^ state[17];
state[18] = (RC[11][18] ^ key_1[18]) ^ state[18];
state[19] = (RC[11][19] ^ key_1[19]) ^ state[19];
state[20] = (RC[11][20] ^ key_1[20]) ^ state[20];
state[21] = (RC[11][21] ^ key_1[21]) ^ state[21];
state[22] = (RC[11][22] ^ key_1[22]) ^ state[22];
state[23] = (RC[11][23] ^ key_1[23]) ^ state[23];
state[24] = (RC[11][24] ^ key_1[24]) ^ state[24];
state[25] = (RC[11][25] ^ key_1[25]) ^ state[25];
state[26] = (RC[11][26] ^ key_1[26]) ^ state[26];
state[27] = (RC[11][27] ^ key_1[27]) ^ state[27];
state[28] = (RC[11][28] ^ key_1[28]) ^ state[28];
state[29] = (RC[11][29] ^ key_1[29]) ^ state[29];
state[30] = (RC[11][30] ^ key_1[30]) ^ state[30];
state[31] = (RC[11][31] ^ key_1[31]) ^ state[31];
state[32] = (RC[11][32] ^ key_1[32]) ^ state[32];
state[33] = (RC[11][33] ^ key_1[33]) ^ state[33];
state[34] = (RC[11][34] ^ key_1[34]) ^ state[34];
state[35] = (RC[11][35] ^ key_1[35]) ^ state[35];
state[36] = (RC[11][36] ^ key_1[36]) ^ state[36];
state[37] = (RC[11][37] ^ key_1[37]) ^ state[37];
state[38] = (RC[11][38] ^ key_1[38]) ^ state[38];
state[39] = (RC[11][39] ^ key_1[39]) ^ state[39];
state[40] = (RC[11][40] ^ key_1[40]) ^ state[40];
state[41] = (RC[11][41] ^ key_1[41]) ^ state[41];
state[42] = (RC[11][42] ^ key_1[42]) ^ state[42];
state[43] = (RC[11][43] ^ key_1[43]) ^ state[43];
state[44] = (RC[11][44] ^ key_1[44]) ^ state[44];
state[45] = (RC[11][45] ^ key_1[45]) ^ state[45];
state[46] = (RC[11][46] ^ key_1[46]) ^ state[46];
state[47] = (RC[11][47] ^ key_1[47]) ^ state[47];
state[48] = (RC[11][48] ^ key_1[48]) ^ state[48];
state[49] = (RC[11][49] ^ key_1[49]) ^ state[49];
state[50] = (RC[11][50] ^ key_1[50]) ^ state[50];
state[51] = (RC[11][51] ^ key_1[51]) ^ state[51];
state[52] = (RC[11][52] ^ key_1[52]) ^ state[52];
state[53] = (RC[11][53] ^ key_1[53]) ^ state[53];
state[54] = (RC[11][54] ^ key_1[54]) ^ state[54];
state[55] = (RC[11][55] ^ key_1[55]) ^ state[55];
state[56] = (RC[11][56] ^ key_1[56]) ^ state[56];
state[57] = (RC[11][57] ^ key_1[57]) ^ state[57];
state[58] = (RC[11][58] ^ key_1[58]) ^ state[58];
state[59] = (RC[11][59] ^ key_1[59]) ^ state[59];
state[60] = (RC[11][60] ^ key_1[60]) ^ state[60];
state[61] = (RC[11][61] ^ key_1[61]) ^ state[61];
state[62] = (RC[11][62] ^ key_1[62]) ^ state[62];
state[63] = (RC[11][63] ^ key_1[63]) ^ state[63];
state[0] = state[0] ^ key_prime[0];
state[1] = state[1] ^ key_prime[1];
state[2] = state[2] ^ key_prime[2];
state[3] = state[3] ^ key_prime[3];
state[4] = state[4] ^ key_prime[4];
state[5] = state[5] ^ key_prime[5];
state[6] = state[6] ^ key_prime[6];
state[7] = state[7] ^ key_prime[7];
state[8] = state[8] ^ key_prime[8];
state[9] = state[9] ^ key_prime[9];
state[10] = state[10] ^ key_prime[10];
state[11] = state[11] ^ key_prime[11];
state[12] = state[12] ^ key_prime[12];
state[13] = state[13] ^ key_prime[13];
state[14] = state[14] ^ key_prime[14];
state[15] = state[15] ^ key_prime[15];
state[16] = state[16] ^ key_prime[16];
state[17] = state[17] ^ key_prime[17];
state[18] = state[18] ^ key_prime[18];
state[19] = state[19] ^ key_prime[19];
state[20] = state[20] ^ key_prime[20];
state[21] = state[21] ^ key_prime[21];
state[22] = state[22] ^ key_prime[22];
state[23] = state[23] ^ key_prime[23];
state[24] = state[24] ^ key_prime[24];
state[25] = state[25] ^ key_prime[25];
state[26] = state[26] ^ key_prime[26];
state[27] = state[27] ^ key_prime[27];
state[28] = state[28] ^ key_prime[28];
state[29] = state[29] ^ key_prime[29];
state[30] = state[30] ^ key_prime[30];
state[31] = state[31] ^ key_prime[31];
state[32] = state[32] ^ key_prime[32];
state[33] = state[33] ^ key_prime[33];
state[34] = state[34] ^ key_prime[34];
state[35] = state[35] ^ key_prime[35];
state[36] = state[36] ^ key_prime[36];
state[37] = state[37] ^ key_prime[37];
state[38] = state[38] ^ key_prime[38];
state[39] = state[39] ^ key_prime[39];
state[40] = state[40] ^ key_prime[40];
state[41] = state[41] ^ key_prime[41];
state[42] = state[42] ^ key_prime[42];
state[43] = state[43] ^ key_prime[43];
state[44] = state[44] ^ key_prime[44];
state[45] = state[45] ^ key_prime[45];
state[46] = state[46] ^ key_prime[46];
state[47] = state[47] ^ key_prime[47];
state[48] = state[48] ^ key_prime[48];
state[49] = state[49] ^ key_prime[49];
state[50] = state[50] ^ key_prime[50];
state[51] = state[51] ^ key_prime[51];
state[52] = state[52] ^ key_prime[52];
state[53] = state[53] ^ key_prime[53];
state[54] = state[54] ^ key_prime[54];
state[55] = state[55] ^ key_prime[55];
state[56] = state[56] ^ key_prime[56];
state[57] = state[57] ^ key_prime[57];
state[58] = state[58] ^ key_prime[58];
state[59] = state[59] ^ key_prime[59];
state[60] = state[60] ^ key_prime[60];
state[61] = state[61] ^ key_prime[61];
state[62] = state[62] ^ key_prime[62];
state[63] = state[63] ^ key_prime[63];
}
void  m0(uint32_t *temp_5_bs_return, uint32_t state[16], uint32_t output[16]){ 
output[15] = ((state[11] ^ state[7]) ^ state[3]);
output[14] = ((state[14] ^ state[6]) ^ state[2]);
output[13] = ((state[13] ^ state[9]) ^ state[1]);
output[12] = ((state[12] ^ state[8]) ^ state[4]);
output[11] = ((state[15] ^ state[11]) ^ state[7]);
output[10] = ((state[10] ^ state[6]) ^ state[2]);
output[9] = ((state[13] ^ state[5]) ^ state[1]);
output[8] = ((state[12] ^ state[8]) ^ state[0]);
output[7] = ((state[15] ^ state[11]) ^ state[3]);
output[6] = ((state[14] ^ state[10]) ^ state[6]);
output[5] = ((state[9] ^ state[5]) ^ state[1]);
output[4] = ((state[12] ^ state[4]) ^ state[0]);
output[3] = ((state[15] ^ state[7]) ^ state[3]);
output[2] = ((state[14] ^ state[10]) ^ state[2]);
output[1] = ((state[13] ^ state[9]) ^ state[5]);
output[0] = ((state[8] ^ state[4]) ^ state[0]);
temp_5_bs_return[0] = output[0];
temp_5_bs_return[1] = output[1];
temp_5_bs_return[2] = output[2];
temp_5_bs_return[3] = output[3];
temp_5_bs_return[4] = output[4];
temp_5_bs_return[5] = output[5];
temp_5_bs_return[6] = output[6];
temp_5_bs_return[7] = output[7];
temp_5_bs_return[8] = output[8];
temp_5_bs_return[9] = output[9];
temp_5_bs_return[10] = output[10];
temp_5_bs_return[11] = output[11];
temp_5_bs_return[12] = output[12];
temp_5_bs_return[13] = output[13];
temp_5_bs_return[14] = output[14];
temp_5_bs_return[15] = output[15];
}
void  m1(uint32_t *temp_7_bs_return, uint32_t state[16], uint32_t output[16]){ 
output[15] = ((state[15] ^ state[11]) ^ state[7]);
output[14] = ((state[10] ^ state[6]) ^ state[2]);
output[13] = ((state[13] ^ state[5]) ^ state[1]);
output[12] = ((state[12] ^ state[8]) ^ state[0]);
output[11] = ((state[15] ^ state[11]) ^ state[3]);
output[10] = ((state[14] ^ state[10]) ^ state[6]);
output[9] = ((state[9] ^ state[5]) ^ state[1]);
output[8] = ((state[12] ^ state[4]) ^ state[0]);
output[7] = ((state[15] ^ state[7]) ^ state[3]);
output[6] = ((state[14] ^ state[10]) ^ state[2]);
output[5] = ((state[13] ^ state[9]) ^ state[5]);
output[4] = ((state[8] ^ state[4]) ^ state[0]);
output[3] = ((state[11] ^ state[7]) ^ state[3]);
output[2] = ((state[14] ^ state[6]) ^ state[2]);
output[1] = ((state[13] ^ state[9]) ^ state[1]);
output[0] = ((state[12] ^ state[8]) ^ state[4]);
temp_7_bs_return[0] = output[0];
temp_7_bs_return[1] = output[1];
temp_7_bs_return[2] = output[2];
temp_7_bs_return[3] = output[3];
temp_7_bs_return[4] = output[4];
temp_7_bs_return[5] = output[5];
temp_7_bs_return[6] = output[6];
temp_7_bs_return[7] = output[7];
temp_7_bs_return[8] = output[8];
temp_7_bs_return[9] = output[9];
temp_7_bs_return[10] = output[10];
temp_7_bs_return[11] = output[11];
temp_7_bs_return[12] = output[12];
temp_7_bs_return[13] = output[13];
temp_7_bs_return[14] = output[14];
temp_7_bs_return[15] = output[15];
}
void mPrime(uint32_t state[64]){ 
uint32_t output[16] = {0};
uint32_t temp_9_call[16];
uint32_t temp_10_rnge[(15 - 0) + 1];
extract_bs_range(temp_10_rnge, state, 0, 15);
m0(temp_9_call, temp_10_rnge, output);
state[0] = temp_9_call[0];
state[1] = temp_9_call[1];
state[2] = temp_9_call[2];
state[3] = temp_9_call[3];
state[4] = temp_9_call[4];
state[5] = temp_9_call[5];
state[6] = temp_9_call[6];
state[7] = temp_9_call[7];
state[8] = temp_9_call[8];
state[9] = temp_9_call[9];
state[10] = temp_9_call[10];
state[11] = temp_9_call[11];
state[12] = temp_9_call[12];
state[13] = temp_9_call[13];
state[14] = temp_9_call[14];
state[15] = temp_9_call[15];
uint32_t temp_11_call[16];
uint32_t temp_12_rnge[(31 - 16) + 1];
extract_bs_range(temp_12_rnge, state, 16, 31);
m1(temp_11_call, temp_12_rnge, output);
state[16] = temp_11_call[0];
state[17] = temp_11_call[1];
state[18] = temp_11_call[2];
state[19] = temp_11_call[3];
state[20] = temp_11_call[4];
state[21] = temp_11_call[5];
state[22] = temp_11_call[6];
state[23] = temp_11_call[7];
state[24] = temp_11_call[8];
state[25] = temp_11_call[9];
state[26] = temp_11_call[10];
state[27] = temp_11_call[11];
state[28] = temp_11_call[12];
state[29] = temp_11_call[13];
state[30] = temp_11_call[14];
state[31] = temp_11_call[15];
uint32_t temp_13_call[16];
uint32_t temp_14_rnge[(47 - 32) + 1];
extract_bs_range(temp_14_rnge, state, 32, 47);
m1(temp_13_call, temp_14_rnge, output);
state[32] = temp_13_call[0];
state[33] = temp_13_call[1];
state[34] = temp_13_call[2];
state[35] = temp_13_call[3];
state[36] = temp_13_call[4];
state[37] = temp_13_call[5];
state[38] = temp_13_call[6];
state[39] = temp_13_call[7];
state[40] = temp_13_call[8];
state[41] = temp_13_call[9];
state[42] = temp_13_call[10];
state[43] = temp_13_call[11];
state[44] = temp_13_call[12];
state[45] = temp_13_call[13];
state[46] = temp_13_call[14];
state[47] = temp_13_call[15];
uint32_t temp_15_call[16];
uint32_t temp_16_rnge[(63 - 48) + 1];
extract_bs_range(temp_16_rnge, state, 48, 63);
m0(temp_15_call, temp_16_rnge, output);
state[48] = temp_15_call[0];
state[49] = temp_15_call[1];
state[50] = temp_15_call[2];
state[51] = temp_15_call[3];
state[52] = temp_15_call[4];
state[53] = temp_15_call[5];
state[54] = temp_15_call[6];
state[55] = temp_15_call[7];
state[56] = temp_15_call[8];
state[57] = temp_15_call[9];
state[58] = temp_15_call[10];
state[59] = temp_15_call[11];
state[60] = temp_15_call[12];
state[61] = temp_15_call[13];
state[62] = temp_15_call[14];
state[63] = temp_15_call[15];
}
void sBox_layer(uint32_t state[64]){ 
uint8_t i = 0;
i = 0;
for(;i < 16;) { 
if((i * 4) >= 64){
fprintf(stderr, "Index out of bounds for selection on state\n");
exit(1);
}
if(((i * 4) + 3) >= 64){
fprintf(stderr, "Index out of bounds for selection on state\n");
exit(1);
}
if((i * 4) > ((i * 4) + 3)){
fprintf(stderr, "Start of range cannot be larger than end for index select on state \n");
exit(1);
}
uint32_t temp_24_rnge[(((i * 4) + 3) - (i * 4)) + 1];
extract_bs_range(temp_24_rnge, state, (i * 4), ((i * 4) + 3));
prince(temp_24_rnge);
if((i * 4) >= 64){
fprintf(stderr, "Index out of bounds for selection on state\n");
exit(1);
}
if(((i * 4) + 3) >= 64){
fprintf(stderr, "Index out of bounds for selection on state\n");
exit(1);
}
if((i * 4) > ((i * 4) + 3)){
fprintf(stderr, "Start of range cannot be larger than end for index select on state \n");
exit(1);
}
uint8_t temp_34_init = 0;
uint32_t temp_35_rnge_size = 0;
temp_35_rnge_size = (((i * 4) + 3)-(i * 4)) + 1;
uint8_t temp_40_rng_start = (i * 4);
for(temp_34_init = 0; temp_34_init < temp_35_rnge_size; temp_34_init++, temp_40_rng_start++){
state[temp_40_rng_start] = temp_24_rnge[temp_34_init];
}
i = (i + 1);
} 
}
void sBox_layer_inv(uint32_t state[64]){ 
uint8_t i = 0;
i = 0;
for(;i < 16;) { 
if((i * 4) >= 64){
fprintf(stderr, "Index out of bounds for selection on state\n");
exit(1);
}
if(((i * 4) + 3) >= 64){
fprintf(stderr, "Index out of bounds for selection on state\n");
exit(1);
}
if((i * 4) > ((i * 4) + 3)){
fprintf(stderr, "Start of range cannot be larger than end for index select on state \n");
exit(1);
}
uint32_t temp_48_rnge[(((i * 4) + 3) - (i * 4)) + 1];
extract_bs_range(temp_48_rnge, state, (i * 4), ((i * 4) + 3));
prince_inv(temp_48_rnge);
if((i * 4) >= 64){
fprintf(stderr, "Index out of bounds for selection on state\n");
exit(1);
}
if(((i * 4) + 3) >= 64){
fprintf(stderr, "Index out of bounds for selection on state\n");
exit(1);
}
if((i * 4) > ((i * 4) + 3)){
fprintf(stderr, "Start of range cannot be larger than end for index select on state \n");
exit(1);
}
uint8_t temp_58_init = 0;
uint32_t temp_59_rnge_size = 0;
temp_59_rnge_size = (((i * 4) + 3)-(i * 4)) + 1;
uint8_t temp_64_rng_start = (i * 4);
for(temp_58_init = 0; temp_58_init < temp_59_rnge_size; temp_58_init++, temp_64_rng_start++){
state[temp_64_rng_start] = temp_48_rnge[temp_58_init];
}
i = (i + 1);
} 
}
void shift_rows(uint32_t state[64], uint8_t inverse){ 
uint8_t target = 0;
uint32_t output[64] = {0};
uint32_t temp_65_rnge[(63 - 59) + 1];
extract_bs_range(temp_65_rnge, state, 59, 63);
output[59] = temp_65_rnge[0];
output[60] = temp_65_rnge[1];
output[61] = temp_65_rnge[2];
output[62] = temp_65_rnge[3];
output[63] = temp_65_rnge[4];
uint8_t nibble = 0;
nibble = 1;
for(;nibble < 16;) { 
if(inverse == 0x1) { 
target = ((target + 5) % 16);
} 
if(inverse == 0x0) { 
target = ((target + 13) % 16);
} 
if(((63 - (nibble * 4)) - 3) >= 64){
fprintf(stderr, "Index out of bounds for selection on state\n");
exit(1);
}
if((63 - (nibble * 4)) >= 64){
fprintf(stderr, "Index out of bounds for selection on state\n");
exit(1);
}
if(((63 - (nibble * 4)) - 3) > (63 - (nibble * 4))){
fprintf(stderr, "Start of range cannot be larger than end for index select on state \n");
exit(1);
}
uint32_t temp_81_rnge[((63 - (nibble * 4)) - ((63 - (nibble * 4)) - 3)) + 1];
extract_bs_range(temp_81_rnge, state, ((63 - (nibble * 4)) - 3), (63 - (nibble * 4)));
if(((63 - (target * 4)) - 3) >= 64){
fprintf(stderr, "Index out of bounds for selection on output\n");
exit(1);
}
if((63 - (target * 4)) >= 64){
fprintf(stderr, "Index out of bounds for selection on output\n");
exit(1);
}
if(((63 - (target * 4)) - 3) > (63 - (target * 4))){
fprintf(stderr, "Start of range cannot be larger than end for index select on output \n");
exit(1);
}
uint8_t temp_97_init = 0;
uint32_t temp_98_rnge_size = 0;
temp_98_rnge_size = ((63 - (target * 4))-((63 - (target * 4)) - 3)) + 1;
uint8_t temp_107_rng_start = ((63 - (target * 4)) - 3);
for(temp_97_init = 0; temp_97_init < temp_98_rnge_size; temp_97_init++, temp_107_rng_start++){
output[temp_107_rng_start] = temp_81_rnge[temp_97_init];
}
nibble = (nibble + 1);
} 
state[0] = output[0];
state[1] = output[1];
state[2] = output[2];
state[3] = output[3];
state[4] = output[4];
state[5] = output[5];
state[6] = output[6];
state[7] = output[7];
state[8] = output[8];
state[9] = output[9];
state[10] = output[10];
state[11] = output[11];
state[12] = output[12];
state[13] = output[13];
state[14] = output[14];
state[15] = output[15];
state[16] = output[16];
state[17] = output[17];
state[18] = output[18];
state[19] = output[19];
state[20] = output[20];
state[21] = output[21];
state[22] = output[22];
state[23] = output[23];
state[24] = output[24];
state[25] = output[25];
state[26] = output[26];
state[27] = output[27];
state[28] = output[28];
state[29] = output[29];
state[30] = output[30];
state[31] = output[31];
state[32] = output[32];
state[33] = output[33];
state[34] = output[34];
state[35] = output[35];
state[36] = output[36];
state[37] = output[37];
state[38] = output[38];
state[39] = output[39];
state[40] = output[40];
state[41] = output[41];
state[42] = output[42];
state[43] = output[43];
state[44] = output[44];
state[45] = output[45];
state[46] = output[46];
state[47] = output[47];
state[48] = output[48];
state[49] = output[49];
state[50] = output[50];
state[51] = output[51];
state[52] = output[52];
state[53] = output[53];
state[54] = output[54];
state[55] = output[55];
state[56] = output[56];
state[57] = output[57];
state[58] = output[58];
state[59] = output[59];
state[60] = output[60];
state[61] = output[61];
state[62] = output[62];
state[63] = output[63];
}
void first_rounds(uint32_t state[64], uint32_t key[64], uint32_t RC[11][64]){ 
uint8_t r = 0;
r = 1;
for(;r < 6;) { 
sBox_layer(state);
mPrime(state);
shift_rows(state, 0x0);
state[0] = (RC[r][0] ^ key[0]) ^ state[0];
state[1] = (RC[r][1] ^ key[1]) ^ state[1];
state[2] = (RC[r][2] ^ key[2]) ^ state[2];
state[3] = (RC[r][3] ^ key[3]) ^ state[3];
state[4] = (RC[r][4] ^ key[4]) ^ state[4];
state[5] = (RC[r][5] ^ key[5]) ^ state[5];
state[6] = (RC[r][6] ^ key[6]) ^ state[6];
state[7] = (RC[r][7] ^ key[7]) ^ state[7];
state[8] = (RC[r][8] ^ key[8]) ^ state[8];
state[9] = (RC[r][9] ^ key[9]) ^ state[9];
state[10] = (RC[r][10] ^ key[10]) ^ state[10];
state[11] = (RC[r][11] ^ key[11]) ^ state[11];
state[12] = (RC[r][12] ^ key[12]) ^ state[12];
state[13] = (RC[r][13] ^ key[13]) ^ state[13];
state[14] = (RC[r][14] ^ key[14]) ^ state[14];
state[15] = (RC[r][15] ^ key[15]) ^ state[15];
state[16] = (RC[r][16] ^ key[16]) ^ state[16];
state[17] = (RC[r][17] ^ key[17]) ^ state[17];
state[18] = (RC[r][18] ^ key[18]) ^ state[18];
state[19] = (RC[r][19] ^ key[19]) ^ state[19];
state[20] = (RC[r][20] ^ key[20]) ^ state[20];
state[21] = (RC[r][21] ^ key[21]) ^ state[21];
state[22] = (RC[r][22] ^ key[22]) ^ state[22];
state[23] = (RC[r][23] ^ key[23]) ^ state[23];
state[24] = (RC[r][24] ^ key[24]) ^ state[24];
state[25] = (RC[r][25] ^ key[25]) ^ state[25];
state[26] = (RC[r][26] ^ key[26]) ^ state[26];
state[27] = (RC[r][27] ^ key[27]) ^ state[27];
state[28] = (RC[r][28] ^ key[28]) ^ state[28];
state[29] = (RC[r][29] ^ key[29]) ^ state[29];
state[30] = (RC[r][30] ^ key[30]) ^ state[30];
state[31] = (RC[r][31] ^ key[31]) ^ state[31];
state[32] = (RC[r][32] ^ key[32]) ^ state[32];
state[33] = (RC[r][33] ^ key[33]) ^ state[33];
state[34] = (RC[r][34] ^ key[34]) ^ state[34];
state[35] = (RC[r][35] ^ key[35]) ^ state[35];
state[36] = (RC[r][36] ^ key[36]) ^ state[36];
state[37] = (RC[r][37] ^ key[37]) ^ state[37];
state[38] = (RC[r][38] ^ key[38]) ^ state[38];
state[39] = (RC[r][39] ^ key[39]) ^ state[39];
state[40] = (RC[r][40] ^ key[40]) ^ state[40];
state[41] = (RC[r][41] ^ key[41]) ^ state[41];
state[42] = (RC[r][42] ^ key[42]) ^ state[42];
state[43] = (RC[r][43] ^ key[43]) ^ state[43];
state[44] = (RC[r][44] ^ key[44]) ^ state[44];
state[45] = (RC[r][45] ^ key[45]) ^ state[45];
state[46] = (RC[r][46] ^ key[46]) ^ state[46];
state[47] = (RC[r][47] ^ key[47]) ^ state[47];
state[48] = (RC[r][48] ^ key[48]) ^ state[48];
state[49] = (RC[r][49] ^ key[49]) ^ state[49];
state[50] = (RC[r][50] ^ key[50]) ^ state[50];
state[51] = (RC[r][51] ^ key[51]) ^ state[51];
state[52] = (RC[r][52] ^ key[52]) ^ state[52];
state[53] = (RC[r][53] ^ key[53]) ^ state[53];
state[54] = (RC[r][54] ^ key[54]) ^ state[54];
state[55] = (RC[r][55] ^ key[55]) ^ state[55];
state[56] = (RC[r][56] ^ key[56]) ^ state[56];
state[57] = (RC[r][57] ^ key[57]) ^ state[57];
state[58] = (RC[r][58] ^ key[58]) ^ state[58];
state[59] = (RC[r][59] ^ key[59]) ^ state[59];
state[60] = (RC[r][60] ^ key[60]) ^ state[60];
state[61] = (RC[r][61] ^ key[61]) ^ state[61];
state[62] = (RC[r][62] ^ key[62]) ^ state[62];
state[63] = (RC[r][63] ^ key[63]) ^ state[63];
r = (r + 1);
} 
}
void last_rounds(uint32_t state[64], uint32_t key[64], uint32_t RC[11][64]){ 
uint8_t r = 0;
r = 6;
for(;r < 11;) { 
state[0] = (RC[r][0] ^ key[0]) ^ state[0];
state[1] = (RC[r][1] ^ key[1]) ^ state[1];
state[2] = (RC[r][2] ^ key[2]) ^ state[2];
state[3] = (RC[r][3] ^ key[3]) ^ state[3];
state[4] = (RC[r][4] ^ key[4]) ^ state[4];
state[5] = (RC[r][5] ^ key[5]) ^ state[5];
state[6] = (RC[r][6] ^ key[6]) ^ state[6];
state[7] = (RC[r][7] ^ key[7]) ^ state[7];
state[8] = (RC[r][8] ^ key[8]) ^ state[8];
state[9] = (RC[r][9] ^ key[9]) ^ state[9];
state[10] = (RC[r][10] ^ key[10]) ^ state[10];
state[11] = (RC[r][11] ^ key[11]) ^ state[11];
state[12] = (RC[r][12] ^ key[12]) ^ state[12];
state[13] = (RC[r][13] ^ key[13]) ^ state[13];
state[14] = (RC[r][14] ^ key[14]) ^ state[14];
state[15] = (RC[r][15] ^ key[15]) ^ state[15];
state[16] = (RC[r][16] ^ key[16]) ^ state[16];
state[17] = (RC[r][17] ^ key[17]) ^ state[17];
state[18] = (RC[r][18] ^ key[18]) ^ state[18];
state[19] = (RC[r][19] ^ key[19]) ^ state[19];
state[20] = (RC[r][20] ^ key[20]) ^ state[20];
state[21] = (RC[r][21] ^ key[21]) ^ state[21];
state[22] = (RC[r][22] ^ key[22]) ^ state[22];
state[23] = (RC[r][23] ^ key[23]) ^ state[23];
state[24] = (RC[r][24] ^ key[24]) ^ state[24];
state[25] = (RC[r][25] ^ key[25]) ^ state[25];
state[26] = (RC[r][26] ^ key[26]) ^ state[26];
state[27] = (RC[r][27] ^ key[27]) ^ state[27];
state[28] = (RC[r][28] ^ key[28]) ^ state[28];
state[29] = (RC[r][29] ^ key[29]) ^ state[29];
state[30] = (RC[r][30] ^ key[30]) ^ state[30];
state[31] = (RC[r][31] ^ key[31]) ^ state[31];
state[32] = (RC[r][32] ^ key[32]) ^ state[32];
state[33] = (RC[r][33] ^ key[33]) ^ state[33];
state[34] = (RC[r][34] ^ key[34]) ^ state[34];
state[35] = (RC[r][35] ^ key[35]) ^ state[35];
state[36] = (RC[r][36] ^ key[36]) ^ state[36];
state[37] = (RC[r][37] ^ key[37]) ^ state[37];
state[38] = (RC[r][38] ^ key[38]) ^ state[38];
state[39] = (RC[r][39] ^ key[39]) ^ state[39];
state[40] = (RC[r][40] ^ key[40]) ^ state[40];
state[41] = (RC[r][41] ^ key[41]) ^ state[41];
state[42] = (RC[r][42] ^ key[42]) ^ state[42];
state[43] = (RC[r][43] ^ key[43]) ^ state[43];
state[44] = (RC[r][44] ^ key[44]) ^ state[44];
state[45] = (RC[r][45] ^ key[45]) ^ state[45];
state[46] = (RC[r][46] ^ key[46]) ^ state[46];
state[47] = (RC[r][47] ^ key[47]) ^ state[47];
state[48] = (RC[r][48] ^ key[48]) ^ state[48];
state[49] = (RC[r][49] ^ key[49]) ^ state[49];
state[50] = (RC[r][50] ^ key[50]) ^ state[50];
state[51] = (RC[r][51] ^ key[51]) ^ state[51];
state[52] = (RC[r][52] ^ key[52]) ^ state[52];
state[53] = (RC[r][53] ^ key[53]) ^ state[53];
state[54] = (RC[r][54] ^ key[54]) ^ state[54];
state[55] = (RC[r][55] ^ key[55]) ^ state[55];
state[56] = (RC[r][56] ^ key[56]) ^ state[56];
state[57] = (RC[r][57] ^ key[57]) ^ state[57];
state[58] = (RC[r][58] ^ key[58]) ^ state[58];
state[59] = (RC[r][59] ^ key[59]) ^ state[59];
state[60] = (RC[r][60] ^ key[60]) ^ state[60];
state[61] = (RC[r][61] ^ key[61]) ^ state[61];
state[62] = (RC[r][62] ^ key[62]) ^ state[62];
state[63] = (RC[r][63] ^ key[63]) ^ state[63];
shift_rows(state, 0x1);
mPrime(state);
sBox_layer_inv(state);
r = (r + 1);
} 
}

