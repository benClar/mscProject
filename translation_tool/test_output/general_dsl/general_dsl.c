#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "general_dsl.h"
uint8_t  int_index_set_1(){ 
uint8_t a = 0;
a = 10;
uint8_t  temp_0_extracted = 0;
temp_0_extracted = (a >> 1) & 0x1;
if(temp_0_extracted) {
a ^= (0x1 << 3);
} else if(temp_0_extracted) {
a &= ~(0x1 << 3);
}
return a;
}
uint8_t  int_index_set_2(){ 
uint8_t a = 0;
a = 0;
uint8_t temp_1_casted_bit_seq = 0;
temp_1_casted_bit_seq |= 0x1 << 0;
temp_1_casted_bit_seq |= 0x1 << 2;
if(((temp_1_casted_bit_seq >> 0) & 0x1) == 0 ){
a &= ~(0x1 <<0);
} else if (((temp_1_casted_bit_seq >> 0) & 0x1) == 1 ){
a |= (0x1 << 0);
}
if(((temp_1_casted_bit_seq >> 1) & 0x1) == 0 ){
a &= ~(0x1 <<1);
} else if (((temp_1_casted_bit_seq >> 1) & 0x1) == 1 ){
a |= (0x1 << 1);
}
if(((temp_1_casted_bit_seq >> 2) & 0x1) == 0 ){
a &= ~(0x1 <<3);
} else if (((temp_1_casted_bit_seq >> 2) & 0x1) == 1 ){
a |= (0x1 << 3);
}
return a;
}
uint8_t  int_index_set_3(){ 
uint8_t a = 0;
a = 5;
uint8_t  temp_2_extracted = 0;
temp_2_extracted ^= (((a >> 0) & 0x1) << 0);
temp_2_extracted ^= (((a >> 1) & 0x1) << 1);
temp_2_extracted ^= (((a >> 2) & 0x1) << 2);
temp_2_extracted ^= (((a >> 3) & 0x1) << 3);
uint32_t temp_3_bit_seq = 0x0;
temp_3_bit_seq = (temp_2_extracted) << 1;
uint32_t temp_4_mask_loop_init = 4;
for(; temp_4_mask_loop_init < 32; temp_4_mask_loop_init++) {
temp_3_bit_seq &= ~(0x1 << temp_4_mask_loop_init);
}
if(((temp_3_bit_seq >> 0) & 0x1) == 0 ){
a &= ~(0x1 <<0);
} else if (((temp_3_bit_seq >> 0) & 0x1) == 1 ){
a |= (0x1 << 0);
}
if(((temp_3_bit_seq >> 1) & 0x1) == 0 ){
a &= ~(0x1 <<1);
} else if (((temp_3_bit_seq >> 1) & 0x1) == 1 ){
a |= (0x1 << 1);
}
if(((temp_3_bit_seq >> 2) & 0x1) == 0 ){
a &= ~(0x1 <<2);
} else if (((temp_3_bit_seq >> 2) & 0x1) == 1 ){
a |= (0x1 << 2);
}
if(((temp_3_bit_seq >> 3) & 0x1) == 0 ){
a &= ~(0x1 <<3);
} else if (((temp_3_bit_seq >> 3) & 0x1) == 1 ){
a |= (0x1 << 3);
}
return a;
}
uint8_t  int_index_set_4(){ 
uint8_t a = 0;
a = 5;
uint8_t  temp_5_extracted = 0;
temp_5_extracted ^= (((a >> 0) & 0x1) << 0);
temp_5_extracted ^= (((a >> 1) & 0x1) << 1);
temp_5_extracted ^= (((a >> 2) & 0x1) << 2);
temp_5_extracted ^= (((a >> 3) & 0x1) << 3);
uint32_t temp_6_bit_seq = 0x0;
temp_6_bit_seq = ((temp_5_extracted) << 3) | ((temp_5_extracted) >> (4 - 3));
uint32_t temp_7_mask_loop_init = 4;
for(; temp_7_mask_loop_init < 32; temp_7_mask_loop_init++) {
temp_6_bit_seq &= ~(0x1 << temp_7_mask_loop_init);
}
if(((temp_6_bit_seq >> 0) & 0x1) == 0 ){
a &= ~(0x1 <<0);
} else if (((temp_6_bit_seq >> 0) & 0x1) == 1 ){
a |= (0x1 << 0);
}
if(((temp_6_bit_seq >> 1) & 0x1) == 0 ){
a &= ~(0x1 <<1);
} else if (((temp_6_bit_seq >> 1) & 0x1) == 1 ){
a |= (0x1 << 1);
}
if(((temp_6_bit_seq >> 2) & 0x1) == 0 ){
a &= ~(0x1 <<2);
} else if (((temp_6_bit_seq >> 2) & 0x1) == 1 ){
a |= (0x1 << 2);
}
if(((temp_6_bit_seq >> 3) & 0x1) == 0 ){
a &= ~(0x1 <<3);
} else if (((temp_6_bit_seq >> 3) & 0x1) == 1 ){
a |= (0x1 << 3);
}
return a;
}
uint8_t  int_index_set_5(){ 
uint8_t a = 0;
a = 19;
uint8_t  temp_8_extracted = 0;
temp_8_extracted ^= (((a >> 0) & 0x1) << 0);
temp_8_extracted ^= (((a >> 1) & 0x1) << 1);
temp_8_extracted ^= (((a >> 2) & 0x1) << 2);
temp_8_extracted ^= (((a >> 3) & 0x1) << 3);
temp_8_extracted ^= (((a >> 4) & 0x1) << 4);
uint32_t temp_9_bit_seq = 0x0;
temp_9_bit_seq = ((temp_8_extracted) >> 3) | ((temp_8_extracted) << (5 - 3));
uint32_t temp_10_mask_loop_init = 5;
for(; temp_10_mask_loop_init < 32; temp_10_mask_loop_init++) {
temp_9_bit_seq &= ~(0x1 << temp_10_mask_loop_init);
}
if(((temp_9_bit_seq >> 0) & 0x1) == 0 ){
a &= ~(0x1 <<0);
} else if (((temp_9_bit_seq >> 0) & 0x1) == 1 ){
a |= (0x1 << 0);
}
if(((temp_9_bit_seq >> 1) & 0x1) == 0 ){
a &= ~(0x1 <<1);
} else if (((temp_9_bit_seq >> 1) & 0x1) == 1 ){
a |= (0x1 << 1);
}
if(((temp_9_bit_seq >> 2) & 0x1) == 0 ){
a &= ~(0x1 <<2);
} else if (((temp_9_bit_seq >> 2) & 0x1) == 1 ){
a |= (0x1 << 2);
}
if(((temp_9_bit_seq >> 3) & 0x1) == 0 ){
a &= ~(0x1 <<3);
} else if (((temp_9_bit_seq >> 3) & 0x1) == 1 ){
a |= (0x1 << 3);
}
if(((temp_9_bit_seq >> 4) & 0x1) == 0 ){
a &= ~(0x1 <<4);
} else if (((temp_9_bit_seq >> 4) & 0x1) == 1 ){
a |= (0x1 << 4);
}
return a;
}
uint8_t  int_index_set_6(){ 
uint8_t a = 0;
a = 19;
uint8_t  temp_11_extracted = 0;
uint8_t temp_12_int_rng_start  = 0;
uint8_t  temp_13_target_bit = 0;
for(;temp_12_int_rng_start < 4;temp_12_int_rng_start++, temp_13_target_bit++){
temp_11_extracted |= ((a >> temp_12_int_rng_start)  << temp_13_target_bit);
}
uint32_t temp_14_bit_seq = 0x0;
temp_14_bit_seq = ((temp_11_extracted) >> 3) | ((temp_11_extracted) << ((4 - 0) + 1 - 3));
uint32_t temp_15_mask_loop_init = (4 - 0) + 1;
for(; temp_15_mask_loop_init < 32; temp_15_mask_loop_init++) {
temp_14_bit_seq &= ~(0x1 << temp_15_mask_loop_init);
}
if(((temp_14_bit_seq >> 0) & 0x1) == 0 ){
a &= ~(0x1 <<0);
} else if (((temp_14_bit_seq >> 0) & 0x1) == 1 ){
a |= (0x1 << 0);
}
if(((temp_14_bit_seq >> 1) & 0x1) == 0 ){
a &= ~(0x1 <<1);
} else if (((temp_14_bit_seq >> 1) & 0x1) == 1 ){
a |= (0x1 << 1);
}
if(((temp_14_bit_seq >> 2) & 0x1) == 0 ){
a &= ~(0x1 <<2);
} else if (((temp_14_bit_seq >> 2) & 0x1) == 1 ){
a |= (0x1 << 2);
}
if(((temp_14_bit_seq >> 3) & 0x1) == 0 ){
a &= ~(0x1 <<3);
} else if (((temp_14_bit_seq >> 3) & 0x1) == 1 ){
a |= (0x1 << 3);
}
if(((temp_14_bit_seq >> 4) & 0x1) == 0 ){
a &= ~(0x1 <<4);
} else if (((temp_14_bit_seq >> 4) & 0x1) == 1 ){
a |= (0x1 << 4);
}
return a;
}
uint8_t  int_index_set_7(){ 
uint8_t a = 0;
a = 0;
uint8_t temp_16_casted_bit_seq = 0;
temp_16_casted_bit_seq |= 0x1 << 0;
temp_16_casted_bit_seq |= 0x1 << 1;
temp_16_casted_bit_seq |= 0x1 << 3;
uint32_t temp_17_rnge_size = 0;
temp_17_rnge_size = (4-0) + 1;
uint32_t temp_19_curr_bit;
uint32_t temp_18_rng_start;
for(temp_19_curr_bit = 0, temp_18_rng_start = 0; temp_18_rng_start < temp_17_rnge_size; temp_18_rng_start++, temp_19_curr_bit++) {
if(((temp_16_casted_bit_seq >> temp_18_rng_start) & 0x1) == 0 ){
a &= ~(0x1 <<temp_19_curr_bit);
} else if (((temp_16_casted_bit_seq >> temp_18_rng_start) & 0x1) == 1 ){
a |= (0x1 << temp_19_curr_bit);
}
}
return a;
}
uint8_t  int_index_set_8(){ 
uint8_t a = 0;
a = 0;
uint8_t temp_20_casted_bit_seq = 0;
temp_20_casted_bit_seq |= 0x1 << 0;
temp_20_casted_bit_seq |= 0x1 << 1;
temp_20_casted_bit_seq |= 0x1 << 3;
a = temp_20_casted_bit_seq;
return a;
}
uint8_t  int_index_set_9(){ 
uint8_t a = 0;
a = 0;
uint8_t temp_22_casted_bit_seq = 0;
temp_22_casted_bit_seq |= 0x1 << 0;
temp_22_casted_bit_seq |= 0x1 << 1;
temp_22_casted_bit_seq |= 0x1 << 3;
uint32_t temp_21__bin = 0;
temp_21__bin = temp_22_casted_bit_seq + 10;
a = temp_21__bin;
return a;
}
uint8_t  int_index_set_10(){ 
uint8_t a = 0;
a = 0;
uint8_t temp_24_casted_bit_seq = 0;
temp_24_casted_bit_seq |= 0x1 << 0;
temp_24_casted_bit_seq |= 0x1 << 1;
temp_24_casted_bit_seq |= 0x1 << 3;
uint32_t temp_25_bit_seq = 0x0;
temp_25_bit_seq = ((temp_24_casted_bit_seq) << 1) | ((temp_24_casted_bit_seq) >> (4 - 1));
uint32_t temp_26_mask_loop_init = 4;
for(; temp_26_mask_loop_init < 32; temp_26_mask_loop_init++) {
temp_25_bit_seq &= ~(0x1 << temp_26_mask_loop_init);
}
uint32_t temp_23__bin = 0;
temp_23__bin = temp_25_bit_seq + 10;
a = temp_23__bin;
return a;
}
uint8_t  int_index_set_11(){ 
uint8_t a = 0;
a = 7;
uint8_t  temp_27_extracted = 0;
temp_27_extracted ^= (((a >> 3) & 0x1) << 0);
temp_27_extracted ^= (((a >> 2) & 0x1) << 1);
temp_27_extracted ^= (((a >> 1) & 0x1) << 2);
temp_27_extracted ^= (((a >> 0) & 0x1) << 3);
if(((temp_27_extracted >> 0) & 0x1) == 0 ){
a &= ~(0x1 <<0);
} else if (((temp_27_extracted >> 0) & 0x1) == 1 ){
a |= (0x1 << 0);
}
if(((temp_27_extracted >> 1) & 0x1) == 0 ){
a &= ~(0x1 <<1);
} else if (((temp_27_extracted >> 1) & 0x1) == 1 ){
a |= (0x1 << 1);
}
if(((temp_27_extracted >> 2) & 0x1) == 0 ){
a &= ~(0x1 <<2);
} else if (((temp_27_extracted >> 2) & 0x1) == 1 ){
a |= (0x1 << 2);
}
if(((temp_27_extracted >> 3) & 0x1) == 0 ){
a &= ~(0x1 <<3);
} else if (((temp_27_extracted >> 3) & 0x1) == 1 ){
a |= (0x1 << 3);
}
return a;
}
uint8_t  int_index_set_12(){ 
uint8_t a = 0;
a = 15;
a &= ~(0x1 << 0);
return a;
}
uint8_t  int_index_set_13(){ 
uint8_t a = 0;
a = 14;
a ^= (0x1 << 0);
return a;
}
uint32_t  (*int_index_set_14(uint32_t a[5][5][10][8]))[5][10][8]{ 
a[0][0][0][0] = 0xffffffff;
return a;
}
void  bs_arith_add(uint32_t *temp_28_bs_return){ 
uint32_t a[8] = {0};
a[0]= 0xffffffff;
a[1]= 0;
a[2]= 0;
a[3]= 0xffffffff;
a[4]= 0xffffffff;
a[5]= 0xffffffff;
a[6]= 0;
a[7]= 0;
uint32_t b[8] = {0};
b[0]= 0xffffffff;
b[1]= 0;
b[2]= 0;
b[3]= 0;
b[4]= 0xffffffff;
b[5]= 0xffffffff;
b[6]= 0;
b[7]= 0;
uint32_t temp_29__bin[8] = {0};
bitslice_add(temp_29__bin, a, b, 8);
temp_28_bs_return[0] = temp_29__bin[0];
temp_28_bs_return[1] = temp_29__bin[1];
temp_28_bs_return[2] = temp_29__bin[2];
temp_28_bs_return[3] = temp_29__bin[3];
temp_28_bs_return[4] = temp_29__bin[4];
temp_28_bs_return[5] = temp_29__bin[5];
temp_28_bs_return[6] = temp_29__bin[6];
temp_28_bs_return[7] = temp_29__bin[7];
}
void  bs_arith_sub(uint32_t *temp_31_bs_return){ 
uint32_t a[8] = {0};
a[0]= 0;
a[1]= 0xffffffff;
a[2]= 0;
a[3]= 0xffffffff;
a[4]= 0;
a[5]= 0;
a[6]= 0xffffffff;
a[7]= 0;
uint32_t b[8] = {0};
b[0]= 0xffffffff;
b[1]= 0xffffffff;
b[2]= 0xffffffff;
b[3]= 0;
b[4]= 0;
b[5]= 0xffffffff;
b[6]= 0;
b[7]= 0;
uint32_t temp_32__bin[8] = {0};
bitslice_subtract(temp_32__bin, a, b, 8);
temp_31_bs_return[0] = temp_32__bin[0];
temp_31_bs_return[1] = temp_32__bin[1];
temp_31_bs_return[2] = temp_32__bin[2];
temp_31_bs_return[3] = temp_32__bin[3];
temp_31_bs_return[4] = temp_32__bin[4];
temp_31_bs_return[5] = temp_32__bin[5];
temp_31_bs_return[6] = temp_32__bin[6];
temp_31_bs_return[7] = temp_32__bin[7];
}
void seq_bit_extraction(uint8_t input[2]){ 
uint8_t a[2] = { 0 };
a[0] |= (0x1 << 1);
a[0] |= (0x0 << 0);
a[1] |= (0x1 << 1);
a[1] |= (0x1 << 0);
uint8_t outer = 0;
outer = 0;
uint8_t  f[2][2] = {{ 0 }};
f[0][0] = 1;
f[0][1] = 2;
f[1][0] = 1;
f[1][1] = 2;
for(;(outer < 2);) { 
uint8_t inner = 0;
inner = 0;
for(;(inner < 2);) { 
if(outer >= 2){
fprintf(stderr, "Index out of bounds for selection on a\n");
exit(1);
}
if(inner >= 2){
fprintf(stderr, "Index out of bounds for selection on a\n");
exit(1);
}
uint8_t temp_36_bit_extracted = 0;
temp_36_bit_extracted |= ((a[outer] >> inner) & 0x1 ) << 0;
if(outer >= 2){
fprintf(stderr, "Index out of bounds for selection on input\n");
exit(1);
}
if(inner >= 2){
fprintf(stderr, "Index out of bounds for selection on input\n");
exit(1);
}
if(temp_36_bit_extracted) {
input[outer] ^= (0x1 << inner);
} else if(temp_36_bit_extracted) {
input[outer] &= ~(0x1 << inner);
}
inner = (inner + 1);
} 
outer = (outer + 1);
} 
}
uint8_t  (*return_bits(uint8_t input[2])){ 
return input;
}
uint8_t  seq_bit_arth(){ 
uint8_t  a[3] = { 0 };
a[0] = 10;
a[1] = 9;
a[2] = 0;
uint8_t  b[2] = { 0 };
b[0] = 6;
b[1] = 7;
uint8_t  temp_38_extracted = 0;
temp_38_extracted ^= (((a[0] >> 0) & 0x1) << 0);
temp_38_extracted ^= (((a[0] >> 1) & 0x1) << 1);
temp_38_extracted ^= (((a[0] >> 2) & 0x1) << 2);
temp_38_extracted ^= (((a[0] >> 3) & 0x1) << 3);
temp_38_extracted ^= (((a[0] >> 4) & 0x1) << 4);
uint8_t  temp_39_extracted = 0;
temp_39_extracted ^= (((b[0] >> 0) & 0x1) << 0);
temp_39_extracted ^= (((b[0] >> 1) & 0x1) << 1);
temp_39_extracted ^= (((b[0] >> 2) & 0x1) << 2);
temp_39_extracted ^= (((b[0] >> 3) & 0x1) << 3);
temp_39_extracted ^= (((b[0] >> 4) & 0x1) << 4);
if((((temp_38_extracted + temp_39_extracted) >> 0) & 0x1) == 0 ){
a[2] &= ~(0x1 <<0);
} else if ((((temp_38_extracted + temp_39_extracted) >> 0) & 0x1) == 1 ){
a[2] |= (0x1 << 0);
}
if((((temp_38_extracted + temp_39_extracted) >> 1) & 0x1) == 0 ){
a[2] &= ~(0x1 <<1);
} else if ((((temp_38_extracted + temp_39_extracted) >> 1) & 0x1) == 1 ){
a[2] |= (0x1 << 1);
}
if((((temp_38_extracted + temp_39_extracted) >> 2) & 0x1) == 0 ){
a[2] &= ~(0x1 <<2);
} else if ((((temp_38_extracted + temp_39_extracted) >> 2) & 0x1) == 1 ){
a[2] |= (0x1 << 2);
}
if((((temp_38_extracted + temp_39_extracted) >> 3) & 0x1) == 0 ){
a[2] &= ~(0x1 <<3);
} else if ((((temp_38_extracted + temp_39_extracted) >> 3) & 0x1) == 1 ){
a[2] |= (0x1 << 3);
}
if((((temp_38_extracted + temp_39_extracted) >> 4) & 0x1) == 0 ){
a[2] &= ~(0x1 <<4);
} else if ((((temp_38_extracted + temp_39_extracted) >> 4) & 0x1) == 1 ){
a[2] |= (0x1 << 4);
}
return a[2];
}
void int_seq_decl(){ 
uint8_t  a[2][2][2] = {{{ 0 }}};
a[0][0][0] = 0;
a[0][0][1] = 9;
a[0][1][0] = 0;
a[0][1][1] = 9;
a[1][0][0] = 0;
a[1][0][1] = 9;
a[1][1][0] = 0;
a[1][1][1] = 9;
}
void bs_seq_decl(){ 
uint32_t a[2][2][8] = {{{ 0 }}};
int_to_bitsliced(a[0][0], 0, 8);
int_to_bitsliced(a[0][1], 9, 8);
int_to_bitsliced(a[1][0], 0, 8);
int_to_bitsliced(a[1][1], 9, 8);
}
void bs_seq_set(uint32_t a[2][2][8]){ 
int_to_bitsliced(a[0][0], 0, 8);
int_to_bitsliced(a[0][1], 9, 8);
int_to_bitsliced(a[1][0], 0, 8);
int_to_bitsliced(a[1][1], 9, 8);
}
void int_seq_set(uint8_t  a[2][2]){ 
a[0][0] = 0;
a[0][1] = 9;
a[1][0] = 0;
a[1][1] = 9;
}
void  bs_mult_sub(uint32_t *temp_40_bs_return){ 
uint32_t a[32] = {0};
a[0]= 0;
a[1]= 0xffffffff;
a[2]= 0;
a[3]= 0xffffffff;
a[4]= 0;
a[5]= 0;
a[6]= 0xffffffff;
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
uint32_t b[32] = {0};
b[0]= 0;
b[1]= 0xffffffff;
b[2]= 0xffffffff;
b[3]= 0;
b[4]= 0;
b[5]= 0;
b[6]= 0;
b[7]= 0xffffffff;
b[8]= 0xffffffff;
b[9]= 0;
b[10]= 0;
b[11]= 0;
b[12]= 0;
b[13]= 0;
b[14]= 0;
b[15]= 0;
b[16]= 0;
b[17]= 0;
b[18]= 0;
b[19]= 0;
b[20]= 0;
b[21]= 0;
b[22]= 0;
b[23]= 0;
b[24]= 0;
b[25]= 0;
b[26]= 0;
b[27]= 0;
b[28]= 0;
b[29]= 0;
b[30]= 0;
b[31]= 0;
uint32_t temp_41__bin[32] = {0};
bitslice_mult(temp_41__bin, a, b, 32);
temp_40_bs_return[0] = temp_41__bin[0];
temp_40_bs_return[1] = temp_41__bin[1];
temp_40_bs_return[2] = temp_41__bin[2];
temp_40_bs_return[3] = temp_41__bin[3];
temp_40_bs_return[4] = temp_41__bin[4];
temp_40_bs_return[5] = temp_41__bin[5];
temp_40_bs_return[6] = temp_41__bin[6];
temp_40_bs_return[7] = temp_41__bin[7];
temp_40_bs_return[8] = temp_41__bin[8];
temp_40_bs_return[9] = temp_41__bin[9];
temp_40_bs_return[10] = temp_41__bin[10];
temp_40_bs_return[11] = temp_41__bin[11];
temp_40_bs_return[12] = temp_41__bin[12];
temp_40_bs_return[13] = temp_41__bin[13];
temp_40_bs_return[14] = temp_41__bin[14];
temp_40_bs_return[15] = temp_41__bin[15];
temp_40_bs_return[16] = temp_41__bin[16];
temp_40_bs_return[17] = temp_41__bin[17];
temp_40_bs_return[18] = temp_41__bin[18];
temp_40_bs_return[19] = temp_41__bin[19];
temp_40_bs_return[20] = temp_41__bin[20];
temp_40_bs_return[21] = temp_41__bin[21];
temp_40_bs_return[22] = temp_41__bin[22];
temp_40_bs_return[23] = temp_41__bin[23];
temp_40_bs_return[24] = temp_41__bin[24];
temp_40_bs_return[25] = temp_41__bin[25];
temp_40_bs_return[26] = temp_41__bin[26];
temp_40_bs_return[27] = temp_41__bin[27];
temp_40_bs_return[28] = temp_41__bin[28];
temp_40_bs_return[29] = temp_41__bin[29];
temp_40_bs_return[30] = temp_41__bin[30];
temp_40_bs_return[31] = temp_41__bin[31];
}
void int_to_seq_bit_cast(){ 
uint8_t b = 0;
b = 10;
uint8_t a =  0 ;
a = (b + b) & 31;
}
void  bs_bit_expr_cast(uint32_t *temp_44_bs_return){ 
uint32_t a[8] = {0};
uint32_t temp_47_casted_bit = 0;
if(((0x1 ^ 0x0) ^ 0x0) == 0x1){
temp_47_casted_bit = 0xffffffff;
} else if(((0x1 ^ 0x0) ^ 0x0) != 0x0){
fprintf(stderr, "Unrecognised bit value to cast.\n");
exit(1);
}
a[0] = temp_47_casted_bit;
temp_44_bs_return[0] = a[0];
temp_44_bs_return[1] = a[1];
temp_44_bs_return[2] = a[2];
temp_44_bs_return[3] = a[3];
temp_44_bs_return[4] = a[4];
temp_44_bs_return[5] = a[5];
temp_44_bs_return[6] = a[6];
temp_44_bs_return[7] = a[7];
}
void bit_to_bs_bit_set(){ 
uint32_t a[8] = {0};
uint8_t b = 0;
uint8_t  temp_50_extracted = 0;
temp_50_extracted = (b >> 0) & 0x1;
uint8_t  temp_52_extracted = 0;
temp_52_extracted = (b >> 1) & 0x1;
uint8_t  temp_53_extracted = 0;
temp_53_extracted = (b >> 3) & 0x1;
uint32_t temp_54_casted_bit = 0;
if((temp_50_extracted ^ (temp_52_extracted & temp_53_extracted)) == 0x1){
temp_54_casted_bit = 0xffffffff;
} else if((temp_50_extracted ^ (temp_52_extracted & temp_53_extracted)) != 0x0){
fprintf(stderr, "Unrecognised bit value to cast.\n");
exit(1);
}
a[1] = temp_54_casted_bit;
}
void  bit_seq_expr_to_bs(uint32_t *temp_55_bs_return){ 
uint32_t a[3][8] = {{ 0 }};
uint8_t temp_56_casted_bit_seq = 0;
temp_56_casted_bit_seq |= 0x1 << 0;
uint8_t temp_57_casted_bit_seq = 0;
temp_57_casted_bit_seq |= 0x1 << 1;
temp_57_casted_bit_seq |= 0x1 << 2;
uint32_t temp_58_cast_bs_seq[3];
int_to_bitsliced(temp_58_cast_bs_seq, (temp_56_casted_bit_seq ^ temp_57_casted_bit_seq), 3);
a[0][1] = temp_58_cast_bs_seq[0];
a[0][2] = temp_58_cast_bs_seq[1];
a[0][3] = temp_58_cast_bs_seq[2];
temp_55_bs_return[0] = a[0][0];
temp_55_bs_return[1] = a[0][1];
temp_55_bs_return[2] = a[0][2];
temp_55_bs_return[3] = a[0][3];
temp_55_bs_return[4] = a[0][4];
temp_55_bs_return[5] = a[0][5];
temp_55_bs_return[6] = a[0][6];
temp_55_bs_return[7] = a[0][7];
}
uint8_t  bit_seq_expr_rotate(){ 
uint8_t a = 0;
uint8_t temp_60_casted_bit_seq = 0;
temp_60_casted_bit_seq |= 0x1 << 0;
temp_60_casted_bit_seq |= 0x1 << 1;
temp_60_casted_bit_seq |= 0x1 << 2;
uint8_t temp_61_casted_bit_seq = 0;
temp_61_casted_bit_seq |= 0x1 << 0;
uint32_t temp_62_bit_seq = 0x0;
temp_62_bit_seq = (((temp_60_casted_bit_seq ^ temp_61_casted_bit_seq)) << 2) | (((temp_60_casted_bit_seq ^ temp_61_casted_bit_seq)) >> (3 - 2));
uint32_t temp_63_mask_loop_init = 3;
for(; temp_63_mask_loop_init < 32; temp_63_mask_loop_init++) {
temp_62_bit_seq &= ~(0x1 << temp_63_mask_loop_init);
}
a = temp_62_bit_seq;
return a;
}
uint8_t  bit_seq_expr_arith(){ 
uint8_t a = 0;
uint8_t temp_66_casted_bit_seq = 0;
temp_66_casted_bit_seq |= 0x1 << 0;
temp_66_casted_bit_seq |= 0x1 << 1;
temp_66_casted_bit_seq |= 0x1 << 2;
uint8_t temp_67_casted_bit_seq = 0;
temp_67_casted_bit_seq |= 0x1 << 0;
a = ((temp_66_casted_bit_seq * temp_67_casted_bit_seq) * 2);
return a;
}
uint8_t  ret_bit(){ 
return 0x1;
}
void get_bit(){ 
uint8_t a = 0;
uint8_t temp_68_bit_call= 0;
temp_68_bit_call = ret_bit();
a = temp_68_bit_call;
}
uint8_t  ret_int(){ 
return 10;
}
void get_int(){ 
uint8_t a = 0;
uint8_t temp_69_int_call= 0;
temp_69_int_call = ret_int();
a = temp_69_int_call;
}
uint8_t  ret_int_in_seq(uint8_t  a[10][10]){ 
return a[0][0];
}
void get_int_1(){ 
uint8_t  b[10][10] = {{ 0 }};
uint8_t a = 0;
uint8_t temp_70_int_call= 0;
temp_70_int_call = ret_int_in_seq(b);
a = temp_70_int_call;
}
void  bs_seq_bit_expr_mult(uint32_t *temp_71_bs_return){ 
uint32_t a[8] = {0};
a[0]= 0xffffffff;
a[1]= 0;
a[2]= 0;
a[3]= 0;
a[4]= 0;
a[5]= 0;
a[6]= 0;
a[7]= 0;
uint8_t b = 0;
uint32_t temp_72__bin[3] = {0};
uint32_t temp_73__bin[3] = {0};
uint32_t  temp_74_extracted[3];
temp_74_extracted[0] = a[0];
temp_74_extracted[1] = a[1];
temp_74_extracted[2] = a[2];
uint8_t  temp_75_extracted = 0;
temp_75_extracted ^= (((b >> 0) & 0x1) << 0);
temp_75_extracted ^= (((b >> 1) & 0x1) << 1);
temp_75_extracted ^= (((b >> 2) & 0x1) << 2);
uint32_t temp_76_casted_bs[3];
int_to_bitsliced(temp_76_casted_bs, temp_75_extracted, 3);
XOR(temp_73__bin, temp_74_extracted, temp_76_casted_bs, 3);
uint32_t temp_77_casted_bs[3];
temp_77_casted_bs[0]= 0;
temp_77_casted_bs[1]= 0xffffffff;
temp_77_casted_bs[2]= 0xffffffff;
bitslice_mult(temp_72__bin, temp_73__bin, temp_77_casted_bs, 3);
a[0] = temp_72__bin[0];
a[1] = temp_72__bin[1];
a[2] = temp_72__bin[2];
temp_71_bs_return[0] = a[0];
temp_71_bs_return[1] = a[1];
temp_71_bs_return[2] = a[2];
temp_71_bs_return[3] = a[3];
temp_71_bs_return[4] = a[4];
temp_71_bs_return[5] = a[5];
temp_71_bs_return[6] = a[6];
temp_71_bs_return[7] = a[7];
}
void  bs_seq_bit_expr_mult_2(uint32_t *temp_79_bs_return){ 
uint32_t a[8] = {0};
a[0]= 0;
a[1]= 0xffffffff;
a[2]= 0;
a[3]= 0;
a[4]= 0;
a[5]= 0;
a[6]= 0;
a[7]= 0;
uint32_t b[8] = {0};
b[0]= 0;
b[1]= 0xffffffff;
b[2]= 0;
b[3]= 0;
b[4]= 0;
b[5]= 0;
b[6]= 0;
b[7]= 0;
uint32_t temp_80__bin[8] = {0};
uint8_t temp_81_casted_bit_seq = 0;
temp_81_casted_bit_seq |= 0x1 << 0;
temp_81_casted_bit_seq |= 0x1 << 2;
uint8_t temp_82_casted_bit_seq = 0;
temp_82_casted_bit_seq |= 0x1 << 0;
uint32_t temp_83_casted_bs[8];
int_to_bitsliced(temp_83_casted_bs, (temp_81_casted_bit_seq ^ temp_82_casted_bit_seq), 8);
bitslice_mult(temp_80__bin, temp_83_casted_bs, b, 8);
a[0] = temp_80__bin[0];
a[1] = temp_80__bin[1];
a[2] = temp_80__bin[2];
a[3] = temp_80__bin[3];
temp_79_bs_return[0] = a[0];
temp_79_bs_return[1] = a[1];
temp_79_bs_return[2] = a[2];
temp_79_bs_return[3] = a[3];
temp_79_bs_return[4] = a[4];
temp_79_bs_return[5] = a[5];
temp_79_bs_return[6] = a[6];
temp_79_bs_return[7] = a[7];
}

