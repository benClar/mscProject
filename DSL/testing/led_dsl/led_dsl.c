#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "led_dsl.h"
uint32_t led_0(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return (((~D & B & A) | (D & B & ~A) | (~D & C & ~B & ~A) | (D & C & ~B & A) | (D & ~C & ~A) | (~D & ~C & A)) & 0x1);
}
uint32_t led_1(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return (((D & ~C & ~B) | (~D & ~C & B) | (D & C & A) | (~C & B & ~A) | (~D & B & ~A) | (D & ~B & A)) & 0x1);
}
uint32_t led_2(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return (((~C & ~B & A) | (~C & B & ~A) | (~D & C & B & A) | (D & ~B & A) | (D & C & ~B) | (~D & ~C & ~B)) & 0x1);
}
uint32_t led_3(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {
return (((~D & B & A) | (~D & C & B) | (D & ~C & A) | (~D & C & ~A) | (~D & ~B & ~A) | (D & ~C & B) | (~C & B & A)) & 0x1);
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
uint32_t temp_1_cast_bs_val[4];
int_to_bitsliced(temp_1_cast_bs_val, 19, 4);
GF_R[0] = temp_1_cast_bs_val[0];
GF_R[1] = temp_1_cast_bs_val[1];
GF_R[2] = temp_1_cast_bs_val[2];
GF_R[3] = temp_1_cast_bs_val[3];
uint32_t t[4] = {0};
uint32_t f[1] = {0};
uint32_t high[1] = {0};
uint32_t temp_2_cast_bs_val[1];
int_to_bitsliced(temp_2_cast_bs_val, 0, 1);
high[0] = temp_2_cast_bs_val[0];
uint32_t mask[4] = {0};
uint8_t bit;
bit = 0;
uint32_t temp_3_cast_bs_val[4];
int_to_bitsliced(temp_3_cast_bs_val, 0, 4);
output[0] = temp_3_cast_bs_val[0];
output[1] = temp_3_cast_bs_val[1];
output[2] = temp_3_cast_bs_val[2];
output[3] = temp_3_cast_bs_val[3];
uint8_t degree;
degree = 0;
for(;degree < 4;) { 
uint32_t temp_5_cast_bs_val[1];
int_to_bitsliced(temp_5_cast_bs_val, 0, 1);
f[0] = temp_5_cast_bs_val[0];
uint32_t temp_6__bin[8] = {0};
uint32_t temp_7_casted_bs[8]= {0};
int_to_bitsliced(temp_7_casted_bs, 1, 8);
bitslice_bitwise(temp_6__bin, b_out, temp_7_casted_bs, 8, "&");
t[0] = temp_6__bin[0];
t[1] = temp_6__bin[1];
t[2] = temp_6__bin[2];
t[3] = temp_6__bin[3];
bit = 0;
for(;bit < 4;) { 
uint32_t temp_9__bin = 0;
uint32_t  temp_10_extracted[1] = {0};
temp_10_extracted[0] = f[0];
uint32_t  temp_11_extracted[1] = {0};
temp_11_extracted[0] = t[bit];
temp_9__bin = temp_10_extracted[0] | temp_11_extracted[0];
f[0] = temp_9__bin;
uint32_t temp_8__bin = 0;
temp_8__bin = bit + 1;
bit = temp_8__bin;
} 
bit = 0;
for(;bit < 4;) { 
uint32_t temp_13__bin = 0;
uint32_t  temp_14_extracted[1] = {0};
temp_14_extracted[0] = f[0];
uint32_t  temp_15_extracted[1] = {0};
temp_15_extracted[0] = a_out[bit];
temp_13__bin = temp_14_extracted[0] & temp_15_extracted[0];
mask[bit] = temp_13__bin;
uint32_t temp_12__bin = 0;
temp_12__bin = bit + 1;
bit = temp_12__bin;
} 
uint32_t temp_16__bin[4] = {0};
uint32_t temp_17__bin[4] = {0};
bitslice_bitwise(temp_17__bin, mask, a_out, 4, "&");
bitslice_bitwise(temp_16__bin, output, temp_17__bin, 4, "^");
output[0] = temp_16__bin[0];
output[1] = temp_16__bin[1];
output[2] = temp_16__bin[2];
output[3] = temp_16__bin[3];
uint32_t  temp_18_extracted[1] = {0};
temp_18_extracted[0] = a_out[3];
high[0] = temp_18_extracted[0];
uint32_t temp_19__bin[8] = {0};
bitslice_shift(temp_19__bin, a_out, 1, 8, "<<");
a_out[0] = temp_19__bin[0];
a_out[1] = temp_19__bin[1];
a_out[2] = temp_19__bin[2];
a_out[3] = temp_19__bin[3];
bit = 0;
for(;bit < 4;) { 
uint32_t temp_21__bin = 0;
uint32_t  temp_22_extracted[1] = {0};
temp_22_extracted[0] = a_out[bit];
uint32_t temp_23__bin = 0;
uint32_t  temp_24_extracted[1] = {0};
temp_24_extracted[0] = high[0];
uint32_t  temp_25_extracted[1] = {0};
temp_25_extracted[0] = GF_R[bit];
temp_23__bin = temp_24_extracted[0] & temp_25_extracted[0];
temp_21__bin = temp_22_extracted[0] ^ temp_23__bin;
a_out[bit] = temp_21__bin;
uint32_t temp_20__bin = 0;
temp_20__bin = bit + 1;
bit = temp_20__bin;
} 
uint32_t temp_26__bin[8] = {0};
bitslice_shift(temp_26__bin, b_out, 1, 8, ">>");
b_out[0] = temp_26__bin[0];
b_out[1] = temp_26__bin[1];
b_out[2] = temp_26__bin[2];
b_out[3] = temp_26__bin[3];
uint32_t temp_4__bin = 0;
temp_4__bin = degree + 1;
degree = temp_4__bin;
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
uint32_t temp_29__bin = 0;
temp_29__bin = col * 4;
uint32_t temp_30__bin = 0;
uint32_t temp_31__bin = 0;
temp_31__bin = col * 4;
temp_30__bin = temp_31__bin + 3;
uint32_t temp_28_rnge[((temp_30__bin - temp_29__bin) + 1) + 1];
extract_bs_range(temp_28_rnge, state, temp_29__bin, temp_30__bin);
uint8_t temp_32_init = 0;
uint32_t temp_33_rnge_size = 0;
temp_33_rnge_size = (3-0) + 1;
uint8_t temp_34_rng_start = 0;
for(temp_32_init = 0; temp_32_init < temp_33_rnge_size; temp_32_init++, temp_34_rng_start++){
column[0][temp_34_rng_start] = temp_28_rnge[temp_32_init];
}
uint32_t temp_36__bin = 0;
uint32_t temp_37__bin = 0;
temp_37__bin = col + 4;
temp_36__bin = temp_37__bin * 4;
uint32_t temp_38__bin = 0;
uint32_t temp_39__bin = 0;
uint32_t temp_40__bin = 0;
temp_40__bin = col + 4;
temp_39__bin = temp_40__bin * 4;
temp_38__bin = temp_39__bin + 3;
uint32_t temp_35_rnge[((temp_38__bin - temp_36__bin) + 1) + 1];
extract_bs_range(temp_35_rnge, state, temp_36__bin, temp_38__bin);
uint8_t temp_41_init = 0;
uint32_t temp_42_rnge_size = 0;
temp_42_rnge_size = (3-0) + 1;
uint8_t temp_43_rng_start = 0;
for(temp_41_init = 0; temp_41_init < temp_42_rnge_size; temp_41_init++, temp_43_rng_start++){
column[1][temp_43_rng_start] = temp_35_rnge[temp_41_init];
}
uint32_t temp_45__bin = 0;
uint32_t temp_46__bin = 0;
temp_46__bin = col + 8;
temp_45__bin = temp_46__bin * 4;
uint32_t temp_47__bin = 0;
uint32_t temp_48__bin = 0;
uint32_t temp_49__bin = 0;
temp_49__bin = col + 8;
temp_48__bin = temp_49__bin * 4;
temp_47__bin = temp_48__bin + 3;
uint32_t temp_44_rnge[((temp_47__bin - temp_45__bin) + 1) + 1];
extract_bs_range(temp_44_rnge, state, temp_45__bin, temp_47__bin);
uint8_t temp_50_init = 0;
uint32_t temp_51_rnge_size = 0;
temp_51_rnge_size = (3-0) + 1;
uint8_t temp_52_rng_start = 0;
for(temp_50_init = 0; temp_50_init < temp_51_rnge_size; temp_50_init++, temp_52_rng_start++){
column[2][temp_52_rng_start] = temp_44_rnge[temp_50_init];
}
uint32_t temp_54__bin = 0;
uint32_t temp_55__bin = 0;
temp_55__bin = col + 12;
temp_54__bin = temp_55__bin * 4;
uint32_t temp_56__bin = 0;
uint32_t temp_57__bin = 0;
uint32_t temp_58__bin = 0;
temp_58__bin = col + 12;
temp_57__bin = temp_58__bin * 4;
temp_56__bin = temp_57__bin + 3;
uint32_t temp_53_rnge[((temp_56__bin - temp_54__bin) + 1) + 1];
extract_bs_range(temp_53_rnge, state, temp_54__bin, temp_56__bin);
uint8_t temp_59_init = 0;
uint32_t temp_60_rnge_size = 0;
temp_60_rnge_size = (3-0) + 1;
uint8_t temp_61_rng_start = 0;
for(temp_59_init = 0; temp_59_init < temp_60_rnge_size; temp_59_init++, temp_61_rng_start++){
column[3][temp_61_rng_start] = temp_53_rnge[temp_59_init];
}
uint8_t col_nibble;
col_nibble = 0;
for(;col_nibble < 4;) { 
uint32_t  temp_66_extracted[4] = {0};
uint32_t temp_67__bin = 0;
temp_67__bin = col_nibble * 4;
temp_66_extracted[0] = MDS[temp_67__bin][0];
temp_66_extracted[1] = MDS[temp_67__bin][1];
temp_66_extracted[2] = MDS[temp_67__bin][2];
temp_66_extracted[3] = MDS[temp_67__bin][3];
uint32_t  temp_68_extracted[4] = {0};
temp_68_extracted[0] = column[0][0];
temp_68_extracted[1] = column[0][1];
temp_68_extracted[2] = column[0][2];
temp_68_extracted[3] = column[0][3];
gmMult(a, temp_66_extracted, temp_68_extracted);
uint32_t  temp_73_extracted[4] = {0};
uint32_t temp_74__bin = 0;
uint32_t temp_75__bin = 0;
temp_75__bin = col_nibble * 4;
temp_74__bin = temp_75__bin + 1;
temp_73_extracted[0] = MDS[temp_74__bin][0];
temp_73_extracted[1] = MDS[temp_74__bin][1];
temp_73_extracted[2] = MDS[temp_74__bin][2];
temp_73_extracted[3] = MDS[temp_74__bin][3];
uint32_t  temp_76_extracted[4] = {0};
temp_76_extracted[0] = column[1][0];
temp_76_extracted[1] = column[1][1];
temp_76_extracted[2] = column[1][2];
temp_76_extracted[3] = column[1][3];
gmMult(b, temp_73_extracted, temp_76_extracted);
uint32_t  temp_81_extracted[4] = {0};
uint32_t temp_82__bin = 0;
uint32_t temp_83__bin = 0;
temp_83__bin = col_nibble * 4;
temp_82__bin = temp_83__bin + 2;
temp_81_extracted[0] = MDS[temp_82__bin][0];
temp_81_extracted[1] = MDS[temp_82__bin][1];
temp_81_extracted[2] = MDS[temp_82__bin][2];
temp_81_extracted[3] = MDS[temp_82__bin][3];
uint32_t  temp_84_extracted[4] = {0};
temp_84_extracted[0] = column[2][0];
temp_84_extracted[1] = column[2][1];
temp_84_extracted[2] = column[2][2];
temp_84_extracted[3] = column[2][3];
gmMult(c, temp_81_extracted, temp_84_extracted);
uint32_t  temp_89_extracted[4] = {0};
uint32_t temp_90__bin = 0;
uint32_t temp_91__bin = 0;
temp_91__bin = col_nibble * 4;
temp_90__bin = temp_91__bin + 3;
temp_89_extracted[0] = MDS[temp_90__bin][0];
temp_89_extracted[1] = MDS[temp_90__bin][1];
temp_89_extracted[2] = MDS[temp_90__bin][2];
temp_89_extracted[3] = MDS[temp_90__bin][3];
uint32_t  temp_92_extracted[4] = {0};
temp_92_extracted[0] = column[3][0];
temp_92_extracted[1] = column[3][1];
temp_92_extracted[2] = column[3][2];
temp_92_extracted[3] = column[3][3];
gmMult(d, temp_89_extracted, temp_92_extracted);
uint32_t temp_93__bin[4] = {0};
uint32_t temp_94__bin[4] = {0};
uint32_t temp_95__bin[4] = {0};
bitslice_bitwise(temp_95__bin, a, b, 4, "^");
bitslice_bitwise(temp_94__bin, temp_95__bin, c, 4, "^");
bitslice_bitwise(temp_93__bin, temp_94__bin, d, 4, "^");
uint8_t temp_96_init = 0;
uint32_t temp_97_rnge_size = 0;
uint32_t temp_98__bin = 0;
uint32_t temp_99__bin = 0;
temp_99__bin = col * 4;
uint32_t temp_100__bin = 0;
temp_100__bin = col_nibble * 16;
temp_98__bin = temp_99__bin + temp_100__bin;
uint32_t temp_101__bin = 0;
uint32_t temp_102__bin = 0;
uint32_t temp_103__bin = 0;
temp_103__bin = col * 4;
uint32_t temp_104__bin = 0;
temp_104__bin = col_nibble * 16;
temp_102__bin = temp_103__bin + temp_104__bin;
temp_101__bin = temp_102__bin + 3;
temp_97_rnge_size = (temp_101__bin-temp_98__bin) + 1;
uint32_t temp_105__bin = 0;
uint32_t temp_106__bin = 0;
temp_106__bin = col * 4;
uint32_t temp_107__bin = 0;
temp_107__bin = col_nibble * 16;
temp_105__bin = temp_106__bin + temp_107__bin;
uint8_t temp_108_rng_start = temp_105__bin;
for(temp_96_init = 0; temp_96_init < temp_97_rnge_size; temp_96_init++, temp_108_rng_start++){
state[temp_108_rng_start] = temp_93__bin[temp_96_init];
}
uint32_t temp_62__bin = 0;
temp_62__bin = col_nibble + 1;
col_nibble = temp_62__bin;
} 
uint32_t temp_27__bin = 0;
temp_27__bin = col + 1;
col = temp_27__bin;
} 
}
void shift_row(uint32_t state[64]){ 
uint32_t temp_109__bin[(31 - 16) + 1] = {0};
uint32_t temp_110_rnge[((31 - 16) + 1) + 1];
extract_bs_range(temp_110_rnge, state, 16, 31);
bitslice_shift(temp_109__bin, temp_110_rnge, 4, (31 - 16) + 1, ">>>");
uint8_t temp_111_init = 0;
uint32_t temp_112_rnge_size = 0;
temp_112_rnge_size = (31-16) + 1;
uint8_t temp_113_rng_start = 16;
for(temp_111_init = 0; temp_111_init < temp_112_rnge_size; temp_111_init++, temp_113_rng_start++){
state[temp_113_rng_start] = temp_109__bin[temp_111_init];
}
uint32_t temp_114__bin[(47 - 32) + 1] = {0};
uint32_t temp_115_rnge[((47 - 32) + 1) + 1];
extract_bs_range(temp_115_rnge, state, 32, 47);
bitslice_shift(temp_114__bin, temp_115_rnge, 8, (47 - 32) + 1, ">>>");
uint8_t temp_116_init = 0;
uint32_t temp_117_rnge_size = 0;
temp_117_rnge_size = (47-32) + 1;
uint8_t temp_118_rng_start = 32;
for(temp_116_init = 0; temp_116_init < temp_117_rnge_size; temp_116_init++, temp_118_rng_start++){
state[temp_118_rng_start] = temp_114__bin[temp_116_init];
}
uint32_t temp_119__bin[(63 - 48) + 1] = {0};
uint32_t temp_120_rnge[((63 - 48) + 1) + 1];
extract_bs_range(temp_120_rnge, state, 48, 63);
bitslice_shift(temp_119__bin, temp_120_rnge, 12, (63 - 48) + 1, ">>>");
uint8_t temp_121_init = 0;
uint32_t temp_122_rnge_size = 0;
temp_122_rnge_size = (63-48) + 1;
uint8_t temp_123_rng_start = 48;
for(temp_121_init = 0; temp_121_init < temp_122_rnge_size; temp_121_init++, temp_123_rng_start++){
state[temp_123_rng_start] = temp_119__bin[temp_121_init];
}
}
void addConstants(uint32_t state[64], uint32_t constant[6]){ 
uint32_t roundConstant[64] = {0};
uint8_t row;
row = 0;
for(;row < 4;) { 
uint8_t  temp_125_extracted = 0;
uint8_t temp_126_int_rng_start  = 0;
uint8_t  temp_128_target_bit = 0;
for(;temp_126_int_rng_start < 3;temp_126_int_rng_start++, temp_128_target_bit++){
temp_125_extracted |= (((row >> temp_126_int_rng_start) & 0x1) << temp_128_target_bit);
}
uint32_t temp_130__bin = 0;
temp_130__bin = row * 16;
uint32_t temp_131__bin = 0;
uint32_t temp_132__bin = 0;
temp_132__bin = row * 16;
temp_131__bin = temp_132__bin + 3;
uint32_t temp_129_cast_bs_seq[(temp_131__bin - temp_130__bin) + 1];
int_to_bitsliced(temp_129_cast_bs_seq, temp_125_extracted, (temp_131__bin - temp_130__bin) + 1);
uint8_t temp_133_init = 0;
uint32_t temp_134_rnge_size = 0;
uint32_t temp_135__bin = 0;
temp_135__bin = row * 16;
uint32_t temp_136__bin = 0;
uint32_t temp_137__bin = 0;
temp_137__bin = row * 16;
temp_136__bin = temp_137__bin + 3;
temp_134_rnge_size = (temp_136__bin-temp_135__bin) + 1;
uint32_t temp_138__bin = 0;
temp_138__bin = row * 16;
uint8_t temp_139_rng_start = temp_138__bin;
for(temp_133_init = 0; temp_133_init < temp_134_rnge_size; temp_133_init++, temp_139_rng_start++){
roundConstant[temp_139_rng_start] = temp_129_cast_bs_seq[temp_133_init];
}
if(row == 0 || row == 2) { 
uint32_t temp_140_rnge[((5 - 3) + 1) + 1];
extract_bs_range(temp_140_rnge, constant, 3, 5);
uint8_t temp_141_init = 0;
uint32_t temp_142_rnge_size = 0;
uint32_t temp_143__bin = 0;
uint32_t temp_144__bin = 0;
temp_144__bin = row * 16;
temp_143__bin = temp_144__bin + 4;
uint32_t temp_145__bin = 0;
uint32_t temp_146__bin = 0;
temp_146__bin = row * 16;
temp_145__bin = temp_146__bin + 6;
temp_142_rnge_size = (temp_145__bin-temp_143__bin) + 1;
uint32_t temp_147__bin = 0;
uint32_t temp_148__bin = 0;
temp_148__bin = row * 16;
temp_147__bin = temp_148__bin + 4;
uint8_t temp_149_rng_start = temp_147__bin;
for(temp_141_init = 0; temp_141_init < temp_142_rnge_size; temp_141_init++, temp_149_rng_start++){
roundConstant[temp_149_rng_start] = temp_140_rnge[temp_141_init];
}
} 
if(row == 1 || row == 3) { 
uint32_t temp_150_rnge[((2 - 0) + 1) + 1];
extract_bs_range(temp_150_rnge, constant, 0, 2);
uint8_t temp_151_init = 0;
uint32_t temp_152_rnge_size = 0;
uint32_t temp_153__bin = 0;
uint32_t temp_154__bin = 0;
temp_154__bin = row * 16;
temp_153__bin = temp_154__bin + 4;
uint32_t temp_155__bin = 0;
uint32_t temp_156__bin = 0;
temp_156__bin = row * 16;
temp_155__bin = temp_156__bin + 6;
temp_152_rnge_size = (temp_155__bin-temp_153__bin) + 1;
uint32_t temp_157__bin = 0;
uint32_t temp_158__bin = 0;
temp_158__bin = row * 16;
temp_157__bin = temp_158__bin + 4;
uint8_t temp_159_rng_start = temp_157__bin;
for(temp_151_init = 0; temp_151_init < temp_152_rnge_size; temp_151_init++, temp_159_rng_start++){
roundConstant[temp_159_rng_start] = temp_150_rnge[temp_151_init];
}
} 
uint32_t temp_161__bin = 0;
uint32_t temp_162__bin = 0;
temp_162__bin = row * 16;
temp_161__bin = temp_162__bin + 8;
uint32_t temp_163__bin = 0;
uint32_t temp_164__bin = 0;
temp_164__bin = row * 16;
temp_163__bin = temp_164__bin + 15;
uint32_t temp_160_cast_bs_seq[(temp_163__bin - temp_161__bin) + 1];
int_to_bitsliced(temp_160_cast_bs_seq, 0, (temp_163__bin - temp_161__bin) + 1);
uint8_t temp_165_init = 0;
uint32_t temp_166_rnge_size = 0;
uint32_t temp_167__bin = 0;
uint32_t temp_168__bin = 0;
temp_168__bin = row * 16;
temp_167__bin = temp_168__bin + 8;
uint32_t temp_169__bin = 0;
uint32_t temp_170__bin = 0;
temp_170__bin = row * 16;
temp_169__bin = temp_170__bin + 15;
temp_166_rnge_size = (temp_169__bin-temp_167__bin) + 1;
uint32_t temp_171__bin = 0;
uint32_t temp_172__bin = 0;
temp_172__bin = row * 16;
temp_171__bin = temp_172__bin + 8;
uint8_t temp_173_rng_start = temp_171__bin;
for(temp_165_init = 0; temp_165_init < temp_166_rnge_size; temp_165_init++, temp_173_rng_start++){
roundConstant[temp_173_rng_start] = temp_160_cast_bs_seq[temp_165_init];
}
uint32_t temp_124__bin = 0;
temp_124__bin = row + 1;
row = temp_124__bin;
} 
uint32_t temp_174__bin[64] = {0};
bitslice_bitwise(temp_174__bin, state, roundConstant, 64, "^");
state[0] = temp_174__bin[0];
state[1] = temp_174__bin[1];
state[2] = temp_174__bin[2];
state[3] = temp_174__bin[3];
state[4] = temp_174__bin[4];
state[5] = temp_174__bin[5];
state[6] = temp_174__bin[6];
state[7] = temp_174__bin[7];
state[8] = temp_174__bin[8];
state[9] = temp_174__bin[9];
state[10] = temp_174__bin[10];
state[11] = temp_174__bin[11];
state[12] = temp_174__bin[12];
state[13] = temp_174__bin[13];
state[14] = temp_174__bin[14];
state[15] = temp_174__bin[15];
state[16] = temp_174__bin[16];
state[17] = temp_174__bin[17];
state[18] = temp_174__bin[18];
state[19] = temp_174__bin[19];
state[20] = temp_174__bin[20];
state[21] = temp_174__bin[21];
state[22] = temp_174__bin[22];
state[23] = temp_174__bin[23];
state[24] = temp_174__bin[24];
state[25] = temp_174__bin[25];
state[26] = temp_174__bin[26];
state[27] = temp_174__bin[27];
state[28] = temp_174__bin[28];
state[29] = temp_174__bin[29];
state[30] = temp_174__bin[30];
state[31] = temp_174__bin[31];
state[32] = temp_174__bin[32];
state[33] = temp_174__bin[33];
state[34] = temp_174__bin[34];
state[35] = temp_174__bin[35];
state[36] = temp_174__bin[36];
state[37] = temp_174__bin[37];
state[38] = temp_174__bin[38];
state[39] = temp_174__bin[39];
state[40] = temp_174__bin[40];
state[41] = temp_174__bin[41];
state[42] = temp_174__bin[42];
state[43] = temp_174__bin[43];
state[44] = temp_174__bin[44];
state[45] = temp_174__bin[45];
state[46] = temp_174__bin[46];
state[47] = temp_174__bin[47];
state[48] = temp_174__bin[48];
state[49] = temp_174__bin[49];
state[50] = temp_174__bin[50];
state[51] = temp_174__bin[51];
state[52] = temp_174__bin[52];
state[53] = temp_174__bin[53];
state[54] = temp_174__bin[54];
state[55] = temp_174__bin[55];
state[56] = temp_174__bin[56];
state[57] = temp_174__bin[57];
state[58] = temp_174__bin[58];
state[59] = temp_174__bin[59];
state[60] = temp_174__bin[60];
state[61] = temp_174__bin[61];
state[62] = temp_174__bin[62];
state[63] = temp_174__bin[63];
}
void subCells(uint32_t state[64]){ 
uint8_t i;
i = 0;
for(;i < 16;) { 
uint32_t temp_177__bin = 0;
temp_177__bin = i * 4;
uint32_t temp_178__bin = 0;
uint32_t temp_179__bin = 0;
temp_179__bin = i * 4;
temp_178__bin = temp_179__bin + 3;
uint32_t temp_176_rnge[((temp_178__bin - temp_177__bin) + 1) + 1];
extract_bs_range(temp_176_rnge, state, temp_177__bin, temp_178__bin);
led(temp_176_rnge);
uint8_t temp_180_init = 0;
uint32_t temp_181_rnge_size = 0;
uint32_t temp_182__bin = 0;
temp_182__bin = i * 4;
uint32_t temp_183__bin = 0;
uint32_t temp_184__bin = 0;
temp_184__bin = i * 4;
temp_183__bin = temp_184__bin + 3;
temp_181_rnge_size = (temp_183__bin-temp_182__bin) + 1;
uint32_t temp_185__bin = 0;
temp_185__bin = i * 4;
uint8_t temp_186_rng_start = temp_185__bin;
for(temp_180_init = 0; temp_180_init < temp_181_rnge_size; temp_180_init++, temp_186_rng_start++){
state[temp_186_rng_start] = temp_176_rnge[temp_180_init];
}
uint32_t temp_175__bin = 0;
temp_175__bin = i + 1;
i = temp_175__bin;
} 
}
void step(uint32_t state[64], uint32_t r[6], uint32_t MDS[16][4]){ 
addConstants(state, r);
subCells(state);
shift_row(state);
MixColumnSerial(state, MDS);
}
uint32_t  (*enc(uint32_t state[64], uint32_t key[64], uint32_t MDS[16][4], uint32_t RC[32][6])){ 
uint8_t r;
r = 0;
for(;r < 32;) { 
uint32_t temp_188__bin = 0;
temp_188__bin = r % 4;
if(temp_188__bin == 0) { 
uint32_t temp_189__bin[64] = {0};
bitslice_bitwise(temp_189__bin, state, key, 64, "^");
state[0] = temp_189__bin[0];
state[1] = temp_189__bin[1];
state[2] = temp_189__bin[2];
state[3] = temp_189__bin[3];
state[4] = temp_189__bin[4];
state[5] = temp_189__bin[5];
state[6] = temp_189__bin[6];
state[7] = temp_189__bin[7];
state[8] = temp_189__bin[8];
state[9] = temp_189__bin[9];
state[10] = temp_189__bin[10];
state[11] = temp_189__bin[11];
state[12] = temp_189__bin[12];
state[13] = temp_189__bin[13];
state[14] = temp_189__bin[14];
state[15] = temp_189__bin[15];
state[16] = temp_189__bin[16];
state[17] = temp_189__bin[17];
state[18] = temp_189__bin[18];
state[19] = temp_189__bin[19];
state[20] = temp_189__bin[20];
state[21] = temp_189__bin[21];
state[22] = temp_189__bin[22];
state[23] = temp_189__bin[23];
state[24] = temp_189__bin[24];
state[25] = temp_189__bin[25];
state[26] = temp_189__bin[26];
state[27] = temp_189__bin[27];
state[28] = temp_189__bin[28];
state[29] = temp_189__bin[29];
state[30] = temp_189__bin[30];
state[31] = temp_189__bin[31];
state[32] = temp_189__bin[32];
state[33] = temp_189__bin[33];
state[34] = temp_189__bin[34];
state[35] = temp_189__bin[35];
state[36] = temp_189__bin[36];
state[37] = temp_189__bin[37];
state[38] = temp_189__bin[38];
state[39] = temp_189__bin[39];
state[40] = temp_189__bin[40];
state[41] = temp_189__bin[41];
state[42] = temp_189__bin[42];
state[43] = temp_189__bin[43];
state[44] = temp_189__bin[44];
state[45] = temp_189__bin[45];
state[46] = temp_189__bin[46];
state[47] = temp_189__bin[47];
state[48] = temp_189__bin[48];
state[49] = temp_189__bin[49];
state[50] = temp_189__bin[50];
state[51] = temp_189__bin[51];
state[52] = temp_189__bin[52];
state[53] = temp_189__bin[53];
state[54] = temp_189__bin[54];
state[55] = temp_189__bin[55];
state[56] = temp_189__bin[56];
state[57] = temp_189__bin[57];
state[58] = temp_189__bin[58];
state[59] = temp_189__bin[59];
state[60] = temp_189__bin[60];
state[61] = temp_189__bin[61];
state[62] = temp_189__bin[62];
state[63] = temp_189__bin[63];
} 
uint32_t  temp_191_extracted[6] = {0};
temp_191_extracted[0] = RC[r][0];
temp_191_extracted[1] = RC[r][1];
temp_191_extracted[2] = RC[r][2];
temp_191_extracted[3] = RC[r][3];
temp_191_extracted[4] = RC[r][4];
temp_191_extracted[5] = RC[r][5];
step(state, temp_191_extracted, MDS);
uint32_t temp_187__bin = 0;
temp_187__bin = r + 1;
r = temp_187__bin;
} 
uint32_t temp_192__bin[64] = {0};
bitslice_bitwise(temp_192__bin, state, key, 64, "^");
state[0] = temp_192__bin[0];
state[1] = temp_192__bin[1];
state[2] = temp_192__bin[2];
state[3] = temp_192__bin[3];
state[4] = temp_192__bin[4];
state[5] = temp_192__bin[5];
state[6] = temp_192__bin[6];
state[7] = temp_192__bin[7];
state[8] = temp_192__bin[8];
state[9] = temp_192__bin[9];
state[10] = temp_192__bin[10];
state[11] = temp_192__bin[11];
state[12] = temp_192__bin[12];
state[13] = temp_192__bin[13];
state[14] = temp_192__bin[14];
state[15] = temp_192__bin[15];
state[16] = temp_192__bin[16];
state[17] = temp_192__bin[17];
state[18] = temp_192__bin[18];
state[19] = temp_192__bin[19];
state[20] = temp_192__bin[20];
state[21] = temp_192__bin[21];
state[22] = temp_192__bin[22];
state[23] = temp_192__bin[23];
state[24] = temp_192__bin[24];
state[25] = temp_192__bin[25];
state[26] = temp_192__bin[26];
state[27] = temp_192__bin[27];
state[28] = temp_192__bin[28];
state[29] = temp_192__bin[29];
state[30] = temp_192__bin[30];
state[31] = temp_192__bin[31];
state[32] = temp_192__bin[32];
state[33] = temp_192__bin[33];
state[34] = temp_192__bin[34];
state[35] = temp_192__bin[35];
state[36] = temp_192__bin[36];
state[37] = temp_192__bin[37];
state[38] = temp_192__bin[38];
state[39] = temp_192__bin[39];
state[40] = temp_192__bin[40];
state[41] = temp_192__bin[41];
state[42] = temp_192__bin[42];
state[43] = temp_192__bin[43];
state[44] = temp_192__bin[44];
state[45] = temp_192__bin[45];
state[46] = temp_192__bin[46];
state[47] = temp_192__bin[47];
state[48] = temp_192__bin[48];
state[49] = temp_192__bin[49];
state[50] = temp_192__bin[50];
state[51] = temp_192__bin[51];
state[52] = temp_192__bin[52];
state[53] = temp_192__bin[53];
state[54] = temp_192__bin[54];
state[55] = temp_192__bin[55];
state[56] = temp_192__bin[56];
state[57] = temp_192__bin[57];
state[58] = temp_192__bin[58];
state[59] = temp_192__bin[59];
state[60] = temp_192__bin[60];
state[61] = temp_192__bin[61];
state[62] = temp_192__bin[62];
state[63] = temp_192__bin[63];
return state;
}

