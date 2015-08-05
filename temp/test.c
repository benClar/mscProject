#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

int main(){
	return 1;
}


void generate_round_keys(uint32_t key[80], uint32_t round_keys[32][64], uint8_t round){
uint8_t round;
round = 0;
for(;round < 32;) {
uint32_t temp_1_rnge[(79 - 16) + 1];
extract_bs_range(temp_1_rnge, key, 16, 79);
uint8_t temp_2_init = 0;
uint32_t temp_3_rnge_size = 0;
temp_3_rnge_size = (63-0) + 1;
uint8_t temp_4_rng_start = 0;
for(temp_2_init = 0; temp_2_init < temp_3_rnge_size; temp_2_init++, temp_4_rng_start++){
round_keys[round][temp_4_rng_start] = temp_1_rnge[temp_2_init];
}
uint32_t temp_5__bin[80] = {0};
bitslice_shift(temp_5__bin, key, 61, 80, "<<<");
key[0] = temp_5__bin[0];
key[1] = temp_5__bin[1];
key[2] = temp_5__bin[2];
key[3] = temp_5__bin[3];
key[4] = temp_5__bin[4];
key[5] = temp_5__bin[5];
key[6] = temp_5__bin[6];
key[7] = temp_5__bin[7];
key[8] = temp_5__bin[8];
key[9] = temp_5__bin[9];
key[10] = temp_5__bin[10];
key[11] = temp_5__bin[11];
key[12] = temp_5__bin[12];
key[13] = temp_5__bin[13];
key[14] = temp_5__bin[14];
key[15] = temp_5__bin[15];
key[16] = temp_5__bin[16];
key[17] = temp_5__bin[17];
key[18] = temp_5__bin[18];
key[19] = temp_5__bin[19];
key[20] = temp_5__bin[20];
key[21] = temp_5__bin[21];
key[22] = temp_5__bin[22];
key[23] = temp_5__bin[23];
key[24] = temp_5__bin[24];
key[25] = temp_5__bin[25];
key[26] = temp_5__bin[26];
key[27] = temp_5__bin[27];
key[28] = temp_5__bin[28];
key[29] = temp_5__bin[29];
key[30] = temp_5__bin[30];
key[31] = temp_5__bin[31];
key[32] = temp_5__bin[32];
key[33] = temp_5__bin[33];
key[34] = temp_5__bin[34];
key[35] = temp_5__bin[35];
key[36] = temp_5__bin[36];
key[37] = temp_5__bin[37];
key[38] = temp_5__bin[38];
key[39] = temp_5__bin[39];
key[40] = temp_5__bin[40];
key[41] = temp_5__bin[41];
key[42] = temp_5__bin[42];
key[43] = temp_5__bin[43];
key[44] = temp_5__bin[44];
key[45] = temp_5__bin[45];
key[46] = temp_5__bin[46];
key[47] = temp_5__bin[47];
key[48] = temp_5__bin[48];
key[49] = temp_5__bin[49];
key[50] = temp_5__bin[50];
key[51] = temp_5__bin[51];
key[52] = temp_5__bin[52];
key[53] = temp_5__bin[53];
key[54] = temp_5__bin[54];
key[55] = temp_5__bin[55];
key[56] = temp_5__bin[56];
key[57] = temp_5__bin[57];
key[58] = temp_5__bin[58];
key[59] = temp_5__bin[59];
key[60] = temp_5__bin[60];
key[61] = temp_5__bin[61];
key[62] = temp_5__bin[62];
key[63] = temp_5__bin[63];
key[64] = temp_5__bin[64];
key[65] = temp_5__bin[65];
key[66] = temp_5__bin[66];
key[67] = temp_5__bin[67];
key[68] = temp_5__bin[68];
key[69] = temp_5__bin[69];
key[70] = temp_5__bin[70];
key[71] = temp_5__bin[71];
key[72] = temp_5__bin[72];
key[73] = temp_5__bin[73];
key[74] = temp_5__bin[74];
key[75] = temp_5__bin[75];
key[76] = temp_5__bin[76];
key[77] = temp_5__bin[77];
key[78] = temp_5__bin[78];
key[79] = temp_5__bin[79];
uint32_t temp_6_rnge[(79 - 76) + 1];
extract_bs_range(temp_6_rnge, key, 76, 79);
present(temp_6_rnge);
uint8_t temp_7_init = 0;
uint32_t temp_8_rnge_size = 0;
temp_8_rnge_size = (79-76) + 1;
uint8_t temp_9_rng_start = 76;
for(temp_7_init = 0; temp_7_init < temp_8_rnge_size; temp_7_init++, temp_9_rng_start++){
key[temp_9_rng_start] = temp_6_rnge[temp_7_init];
}
uint32_t temp_10__bin[(19 - 15) + 1] = {0};
uint32_t temp_11_rnge[(19 - 15) + 1];
extract_bs_range(temp_11_rnge, key, 15, 19);
uint8_t  temp_12_extracted = 0;
uint8_t temp_13_int_rng_start  = 0;
uint8_t  temp_15_target_bit = 0;
for(;temp_13_int_rng_start <= 5;temp_13_int_rng_start++, temp_15_target_bit++){
temp_12_extracted |= (((round >> temp_13_int_rng_start) & 0x1) << temp_15_target_bit);
}
uint32_t temp_16_casted_bs[(19 - 15) + 1]= {0};
int_to_bitsliced(temp_16_casted_bs, temp_12_extracted, (19 - 15) + 1);
bitslice_bitwise(temp_10__bin, temp_11_rnge, temp_16_casted_bs, 80, "^");
uint8_t temp_17_init = 0;
uint32_t temp_18_rnge_size = 0;
temp_18_rnge_size = (19-15) + 1;
uint8_t temp_19_rng_start = 15;
for(temp_17_init = 0; temp_17_init < temp_18_rnge_size; temp_17_init++, temp_19_rng_start++){
key[temp_19_rng_start] = temp_10__bin[temp_17_init];
}
uint8_t  temp_0__bin;
temp_0__bin = round + 1;
round = temp_0__bin;
}
}

// 00000000000000000000000100101100
