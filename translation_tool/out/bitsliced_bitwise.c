#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "bitsliced_bitwise.h"
void bitslice_bitwise(){ 
uint32_t a[64] = {0};
uint32_t b[64] = {0};
a[0] = a[0] ^ b[0];
a[1] = a[1] ^ b[1];
a[2] = a[2] ^ b[2];
a[3] = a[3] ^ b[3];
a[4] = a[4] ^ b[4];
a[5] = a[5] ^ b[5];
a[6] = a[6] ^ b[6];
a[7] = a[7] ^ b[7];
a[8] = a[8] ^ b[8];
a[9] = a[9] ^ b[9];
a[10] = a[10] ^ b[10];
a[11] = a[11] ^ b[11];
a[12] = a[12] ^ b[12];
a[13] = a[13] ^ b[13];
a[14] = a[14] ^ b[14];
a[15] = a[15] ^ b[15];
a[16] = a[16] ^ b[16];
a[17] = a[17] ^ b[17];
a[18] = a[18] ^ b[18];
a[19] = a[19] ^ b[19];
a[20] = a[20] ^ b[20];
a[21] = a[21] ^ b[21];
a[22] = a[22] ^ b[22];
a[23] = a[23] ^ b[23];
a[24] = a[24] ^ b[24];
a[25] = a[25] ^ b[25];
a[26] = a[26] ^ b[26];
a[27] = a[27] ^ b[27];
a[28] = a[28] ^ b[28];
a[29] = a[29] ^ b[29];
a[30] = a[30] ^ b[30];
a[31] = a[31] ^ b[31];
a[32] = a[32] ^ b[32];
a[33] = a[33] ^ b[33];
a[34] = a[34] ^ b[34];
a[35] = a[35] ^ b[35];
a[36] = a[36] ^ b[36];
a[37] = a[37] ^ b[37];
a[38] = a[38] ^ b[38];
a[39] = a[39] ^ b[39];
a[40] = a[40] ^ b[40];
a[41] = a[41] ^ b[41];
a[42] = a[42] ^ b[42];
a[43] = a[43] ^ b[43];
a[44] = a[44] ^ b[44];
a[45] = a[45] ^ b[45];
a[46] = a[46] ^ b[46];
a[47] = a[47] ^ b[47];
a[48] = a[48] ^ b[48];
a[49] = a[49] ^ b[49];
a[50] = a[50] ^ b[50];
a[51] = a[51] ^ b[51];
a[52] = a[52] ^ b[52];
a[53] = a[53] ^ b[53];
a[54] = a[54] ^ b[54];
a[55] = a[55] ^ b[55];
a[56] = a[56] ^ b[56];
a[57] = a[57] ^ b[57];
a[58] = a[58] ^ b[58];
a[59] = a[59] ^ b[59];
a[60] = a[60] ^ b[60];
a[61] = a[61] ^ b[61];
a[62] = a[62] ^ b[62];
a[63] = a[63] ^ b[63];
}
void  bitslice_rotate(uint32_t *temp_0_bs_return){ 
uint32_t a[64] = {0};
a[0]= 0;
a[1]= 0xffffffff;
a[2]= 0;
a[3]= 0xffffffff;
a[4]= 0;
a[5]= 0;
a[6]= 0;
a[7]= 0;
a[8]= 0;
a[9]= 0;
a[10]= 0;
a[11]= 0;
a[12]= 0;
a[13]= 0;
a[14]= 0;
a[15]= 0;
a[16]= 0;
a[17]= 0;
a[18]= 0;
a[19]= 0;
a[20]= 0;
a[21]= 0;
a[22]= 0;
a[23]= 0;
a[24]= 0;
a[25]= 0;
a[26]= 0;
a[27]= 0;
a[28]= 0;
a[29]= 0;
a[30]= 0;
a[31]= 0;
a[32]= 0;
a[33]= 0;
a[34]= 0;
a[35]= 0;
a[36]= 0;
a[37]= 0;
a[38]= 0;
a[39]= 0;
a[40]= 0;
a[41]= 0;
a[42]= 0;
a[43]= 0;
a[44]= 0;
a[45]= 0;
a[46]= 0;
a[47]= 0;
a[48]= 0;
a[49]= 0;
a[50]= 0;
a[51]= 0;
a[52]= 0;
a[53]= 0;
a[54]= 0;
a[55]= 0;
a[56]= 0;
a[57]= 0;
a[58]= 0;
a[59]= 0;
a[60]= 0;
a[61]= 0;
a[62]= 0;
a[63]= 0;
uint32_t temp_1__bin[(4 - 0) + 1] = {0};
uint32_t temp_2_rnge[(4 - 0) + 1];
extract_bs_range(temp_2_rnge, a, 0, 4);
rotate_right(temp_1__bin, temp_2_rnge, 1, (4 - 0) + 1);
a[0] = temp_1__bin[0];
a[1] = temp_1__bin[1];
a[2] = temp_1__bin[2];
a[3] = temp_1__bin[3];
a[4] = temp_1__bin[4];
temp_0_bs_return[0] = a[0];
temp_0_bs_return[1] = a[1];
temp_0_bs_return[2] = a[2];
temp_0_bs_return[3] = a[3];
temp_0_bs_return[4] = a[4];
temp_0_bs_return[5] = a[5];
temp_0_bs_return[6] = a[6];
temp_0_bs_return[7] = a[7];
temp_0_bs_return[8] = a[8];
temp_0_bs_return[9] = a[9];
temp_0_bs_return[10] = a[10];
temp_0_bs_return[11] = a[11];
temp_0_bs_return[12] = a[12];
temp_0_bs_return[13] = a[13];
temp_0_bs_return[14] = a[14];
temp_0_bs_return[15] = a[15];
temp_0_bs_return[16] = a[16];
temp_0_bs_return[17] = a[17];
temp_0_bs_return[18] = a[18];
temp_0_bs_return[19] = a[19];
temp_0_bs_return[20] = a[20];
temp_0_bs_return[21] = a[21];
temp_0_bs_return[22] = a[22];
temp_0_bs_return[23] = a[23];
temp_0_bs_return[24] = a[24];
temp_0_bs_return[25] = a[25];
temp_0_bs_return[26] = a[26];
temp_0_bs_return[27] = a[27];
temp_0_bs_return[28] = a[28];
temp_0_bs_return[29] = a[29];
temp_0_bs_return[30] = a[30];
temp_0_bs_return[31] = a[31];
temp_0_bs_return[32] = a[32];
temp_0_bs_return[33] = a[33];
temp_0_bs_return[34] = a[34];
temp_0_bs_return[35] = a[35];
temp_0_bs_return[36] = a[36];
temp_0_bs_return[37] = a[37];
temp_0_bs_return[38] = a[38];
temp_0_bs_return[39] = a[39];
temp_0_bs_return[40] = a[40];
temp_0_bs_return[41] = a[41];
temp_0_bs_return[42] = a[42];
temp_0_bs_return[43] = a[43];
temp_0_bs_return[44] = a[44];
temp_0_bs_return[45] = a[45];
temp_0_bs_return[46] = a[46];
temp_0_bs_return[47] = a[47];
temp_0_bs_return[48] = a[48];
temp_0_bs_return[49] = a[49];
temp_0_bs_return[50] = a[50];
temp_0_bs_return[51] = a[51];
temp_0_bs_return[52] = a[52];
temp_0_bs_return[53] = a[53];
temp_0_bs_return[54] = a[54];
temp_0_bs_return[55] = a[55];
temp_0_bs_return[56] = a[56];
temp_0_bs_return[57] = a[57];
temp_0_bs_return[58] = a[58];
temp_0_bs_return[59] = a[59];
temp_0_bs_return[60] = a[60];
temp_0_bs_return[61] = a[61];
temp_0_bs_return[62] = a[62];
temp_0_bs_return[63] = a[63];
}

