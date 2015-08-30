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
temp_3_bit_seq = temp_2_extracted << 1;
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
temp_6_bit_seq = (temp_5_extracted << 3) | (temp_5_extracted >> (4 - 3));
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
temp_9_bit_seq = (temp_8_extracted >> 3) | (temp_8_extracted << (5 - 3));
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
uint8_t  temp_14_target_bit = 0;
for(;temp_12_int_rng_start < 4;temp_12_int_rng_start++, temp_14_target_bit++){
temp_11_extracted |= ((a >> temp_12_int_rng_start)  << temp_14_target_bit);
}
uint32_t temp_15_bit_seq = 0x0;
temp_15_bit_seq = (temp_11_extracted >> 3) | (temp_11_extracted << ((4 - 0) + 1 - 3));
uint32_t temp_16_mask_loop_init = (4 - 0) + 1;
for(; temp_16_mask_loop_init < 32; temp_16_mask_loop_init++) {
temp_15_bit_seq &= ~(0x1 << temp_16_mask_loop_init);
}
if(((temp_15_bit_seq >> 0) & 0x1) == 0 ){
a &= ~(0x1 <<0);
} else if (((temp_15_bit_seq >> 0) & 0x1) == 1 ){
a |= (0x1 << 0);
}
if(((temp_15_bit_seq >> 1) & 0x1) == 0 ){
a &= ~(0x1 <<1);
} else if (((temp_15_bit_seq >> 1) & 0x1) == 1 ){
a |= (0x1 << 1);
}
if(((temp_15_bit_seq >> 2) & 0x1) == 0 ){
a &= ~(0x1 <<2);
} else if (((temp_15_bit_seq >> 2) & 0x1) == 1 ){
a |= (0x1 << 2);
}
if(((temp_15_bit_seq >> 3) & 0x1) == 0 ){
a &= ~(0x1 <<3);
} else if (((temp_15_bit_seq >> 3) & 0x1) == 1 ){
a |= (0x1 << 3);
}
if(((temp_15_bit_seq >> 4) & 0x1) == 0 ){
a &= ~(0x1 <<4);
} else if (((temp_15_bit_seq >> 4) & 0x1) == 1 ){
a |= (0x1 << 4);
}
return a;
}
uint8_t  int_index_set_7(){ 
uint8_t a = 0;
a = 0;
uint8_t temp_17_casted_bit_seq = 0;
temp_17_casted_bit_seq |= 0x1 << 0;
temp_17_casted_bit_seq |= 0x1 << 1;
temp_17_casted_bit_seq |= 0x1 << 3;
uint32_t temp_18_rnge_size = 0;
temp_18_rnge_size = (4-0) + 1;
uint32_t temp_20_curr_bit;
uint32_t temp_19_rng_start;
for(temp_20_curr_bit = 0, temp_19_rng_start = 0; temp_19_rng_start < temp_18_rnge_size; temp_19_rng_start++, temp_20_curr_bit++) {
if(((temp_17_casted_bit_seq >> temp_19_rng_start) & 0x1) == 0 ){
a &= ~(0x1 <<temp_20_curr_bit);
} else if (((temp_17_casted_bit_seq >> temp_19_rng_start) & 0x1) == 1 ){
a |= (0x1 << temp_20_curr_bit);
}
}
return a;
}
uint8_t  int_index_set_8(){ 
uint8_t a = 0;
a = 0;
uint8_t temp_21_casted_bit_seq = 0;
temp_21_casted_bit_seq |= 0x1 << 0;
temp_21_casted_bit_seq |= 0x1 << 1;
temp_21_casted_bit_seq |= 0x1 << 3;
a = temp_21_casted_bit_seq;
return a;
}
uint8_t  int_index_set_9(){ 
uint8_t a = 0;
a = 0;
uint8_t temp_23_casted_bit_seq = 0;
temp_23_casted_bit_seq |= 0x1 << 0;
temp_23_casted_bit_seq |= 0x1 << 1;
temp_23_casted_bit_seq |= 0x1 << 3;
uint32_t temp_22__bin = 0;
temp_22__bin = temp_23_casted_bit_seq + 10;
a = temp_22__bin;
return a;
}
uint8_t  int_index_set_10(){ 
uint8_t a = 0;
a = 0;
uint8_t temp_25_casted_bit_seq = 0;
temp_25_casted_bit_seq |= 0x1 << 0;
temp_25_casted_bit_seq |= 0x1 << 1;
temp_25_casted_bit_seq |= 0x1 << 3;
uint32_t temp_26_bit_seq = 0x0;
temp_26_bit_seq = (temp_25_casted_bit_seq << 1) | (temp_25_casted_bit_seq >> (4 - 1));
uint32_t temp_27_mask_loop_init = 4;
for(; temp_27_mask_loop_init < 32; temp_27_mask_loop_init++) {
temp_26_bit_seq &= ~(0x1 << temp_27_mask_loop_init);
}
uint32_t temp_24__bin = 0;
temp_24__bin = temp_26_bit_seq + 10;
a = temp_24__bin;
return a;
}
uint8_t  int_index_set_11(){ 
uint8_t a = 0;
a = 7;
uint8_t  temp_28_extracted = 0;
temp_28_extracted ^= (((a >> 3) & 0x1) << 0);
temp_28_extracted ^= (((a >> 2) & 0x1) << 1);
temp_28_extracted ^= (((a >> 1) & 0x1) << 2);
temp_28_extracted ^= (((a >> 0) & 0x1) << 3);
if(((temp_28_extracted >> 0) & 0x1) == 0 ){
a &= ~(0x1 <<0);
} else if (((temp_28_extracted >> 0) & 0x1) == 1 ){
a |= (0x1 << 0);
}
if(((temp_28_extracted >> 1) & 0x1) == 0 ){
a &= ~(0x1 <<1);
} else if (((temp_28_extracted >> 1) & 0x1) == 1 ){
a |= (0x1 << 1);
}
if(((temp_28_extracted >> 2) & 0x1) == 0 ){
a &= ~(0x1 <<2);
} else if (((temp_28_extracted >> 2) & 0x1) == 1 ){
a |= (0x1 << 2);
}
if(((temp_28_extracted >> 3) & 0x1) == 0 ){
a &= ~(0x1 <<3);
} else if (((temp_28_extracted >> 3) & 0x1) == 1 ){
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
void  bs_arith_add(uint32_t *temp_29_bs_return){ 
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
uint32_t temp_30__bin[8] = {0};
bitslice_add(temp_30__bin, a, b, 8);
temp_29_bs_return[0] = temp_30__bin[0];
temp_29_bs_return[1] = temp_30__bin[1];
temp_29_bs_return[2] = temp_30__bin[2];
temp_29_bs_return[3] = temp_30__bin[3];
temp_29_bs_return[4] = temp_30__bin[4];
temp_29_bs_return[5] = temp_30__bin[5];
temp_29_bs_return[6] = temp_30__bin[6];
temp_29_bs_return[7] = temp_30__bin[7];
}
void  bs_arith_sub(uint32_t *temp_32_bs_return){ 
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
uint32_t temp_33__bin[8] = {0};
bitslice_subtract(temp_33__bin, a, b, 8);
temp_32_bs_return[0] = temp_33__bin[0];
temp_32_bs_return[1] = temp_33__bin[1];
temp_32_bs_return[2] = temp_33__bin[2];
temp_32_bs_return[3] = temp_33__bin[3];
temp_32_bs_return[4] = temp_33__bin[4];
temp_32_bs_return[5] = temp_33__bin[5];
temp_32_bs_return[6] = temp_33__bin[6];
temp_32_bs_return[7] = temp_33__bin[7];
}
void seq_bit_extraction(uint8_t input[2]){ 
uint8_t a[2] = { 0 };
a[0] |= (0x1 << 1);
a[0] |= (0x0 << 0);
a[1] |= (0x1 << 1);
a[1] |= (0x1 << 0);
uint8_t outer = 0;
outer = 0;
for(;outer < 2;) { 
uint8_t inner = 0;
inner = 0;
for(;inner < 2;) { 
if(outer >= 2){
fprintf(stderr, "Index out of bounds for selection on a\n");
exit(1);
}
if(inner >= 2){
fprintf(stderr, "Index out of bounds for selection on a\n");
exit(1);
}
uint8_t temp_37_bit_extracted = 0;
temp_37_bit_extracted |= ((a[outer] >> inner) & 0x1 ) << 0;
if(outer >= 2){
fprintf(stderr, "Index out of bounds for selection on input\n");
exit(1);
}
if(inner >= 2){
fprintf(stderr, "Index out of bounds for selection on input\n");
exit(1);
}
if(temp_37_bit_extracted) {
input[outer] ^= (0x1 << inner);
} else if(temp_37_bit_extracted) {
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
uint8_t  temp_39_extracted = 0;
temp_39_extracted ^= (((a[0] >> 0) & 0x1) << 0);
temp_39_extracted ^= (((a[0] >> 1) & 0x1) << 1);
temp_39_extracted ^= (((a[0] >> 2) & 0x1) << 2);
temp_39_extracted ^= (((a[0] >> 3) & 0x1) << 3);
temp_39_extracted ^= (((a[0] >> 4) & 0x1) << 4);
uint8_t  temp_40_extracted = 0;
temp_40_extracted ^= (((b[0] >> 0) & 0x1) << 0);
temp_40_extracted ^= (((b[0] >> 1) & 0x1) << 1);
temp_40_extracted ^= (((b[0] >> 2) & 0x1) << 2);
temp_40_extracted ^= (((b[0] >> 3) & 0x1) << 3);
temp_40_extracted ^= (((b[0] >> 4) & 0x1) << 4);
if((((temp_39_extracted + temp_40_extracted) >> 0) & 0x1) == 0 ){
a[2] &= ~(0x1 <<0);
} else if ((((temp_39_extracted + temp_40_extracted) >> 0) & 0x1) == 1 ){
a[2] |= (0x1 << 0);
}
if((((temp_39_extracted + temp_40_extracted) >> 1) & 0x1) == 0 ){
a[2] &= ~(0x1 <<1);
} else if ((((temp_39_extracted + temp_40_extracted) >> 1) & 0x1) == 1 ){
a[2] |= (0x1 << 1);
}
if((((temp_39_extracted + temp_40_extracted) >> 2) & 0x1) == 0 ){
a[2] &= ~(0x1 <<2);
} else if ((((temp_39_extracted + temp_40_extracted) >> 2) & 0x1) == 1 ){
a[2] |= (0x1 << 2);
}
if((((temp_39_extracted + temp_40_extracted) >> 3) & 0x1) == 0 ){
a[2] &= ~(0x1 <<3);
} else if ((((temp_39_extracted + temp_40_extracted) >> 3) & 0x1) == 1 ){
a[2] |= (0x1 << 3);
}
if((((temp_39_extracted + temp_40_extracted) >> 4) & 0x1) == 0 ){
a[2] &= ~(0x1 <<4);
} else if ((((temp_39_extracted + temp_40_extracted) >> 4) & 0x1) == 1 ){
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
void  bs_mult_sub(uint32_t *temp_41_bs_return){ 
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
b[0]= 0xffffffff;
b[1]= 0xffffffff;
b[2]= 0xffffffff;
b[3]= 0;
b[4]= 0;
b[5]= 0xffffffff;
b[6]= 0;
b[7]= 0;
b[8]= 0;
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
rprint(b,32);
rprint(a,32);
uint32_t temp_42__bin[32] = {0};
bitslice_mult(temp_42__bin, a, b, 32);
temp_41_bs_return[0] = temp_42__bin[0];
temp_41_bs_return[1] = temp_42__bin[1];
temp_41_bs_return[2] = temp_42__bin[2];
temp_41_bs_return[3] = temp_42__bin[3];
temp_41_bs_return[4] = temp_42__bin[4];
temp_41_bs_return[5] = temp_42__bin[5];
temp_41_bs_return[6] = temp_42__bin[6];
temp_41_bs_return[7] = temp_42__bin[7];
temp_41_bs_return[8] = temp_42__bin[8];
temp_41_bs_return[9] = temp_42__bin[9];
temp_41_bs_return[10] = temp_42__bin[10];
temp_41_bs_return[11] = temp_42__bin[11];
temp_41_bs_return[12] = temp_42__bin[12];
temp_41_bs_return[13] = temp_42__bin[13];
temp_41_bs_return[14] = temp_42__bin[14];
temp_41_bs_return[15] = temp_42__bin[15];
temp_41_bs_return[16] = temp_42__bin[16];
temp_41_bs_return[17] = temp_42__bin[17];
temp_41_bs_return[18] = temp_42__bin[18];
temp_41_bs_return[19] = temp_42__bin[19];
temp_41_bs_return[20] = temp_42__bin[20];
temp_41_bs_return[21] = temp_42__bin[21];
temp_41_bs_return[22] = temp_42__bin[22];
temp_41_bs_return[23] = temp_42__bin[23];
temp_41_bs_return[24] = temp_42__bin[24];
temp_41_bs_return[25] = temp_42__bin[25];
temp_41_bs_return[26] = temp_42__bin[26];
temp_41_bs_return[27] = temp_42__bin[27];
temp_41_bs_return[28] = temp_42__bin[28];
temp_41_bs_return[29] = temp_42__bin[29];
temp_41_bs_return[30] = temp_42__bin[30];
temp_41_bs_return[31] = temp_42__bin[31];
}

