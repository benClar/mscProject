#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "general_dsl.h"
uint8_t  int_index_set_1(){ 
uint8_t a;
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
uint8_t a;
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
uint8_t a;
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
uint8_t a;
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
uint8_t a;
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
uint8_t a;
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
uint8_t a;
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
uint8_t a;
a = 0;
uint8_t temp_21_casted_bit_seq = 0;
temp_21_casted_bit_seq |= 0x1 << 0;
temp_21_casted_bit_seq |= 0x1 << 1;
temp_21_casted_bit_seq |= 0x1 << 3;
uint8_t temp_22_casted_bit_seq = 0;
temp_22_casted_bit_seq |= 0x1 << 0;
temp_22_casted_bit_seq |= 0x1 << 1;
temp_22_casted_bit_seq |= 0x1 << 3;
a = temp_22_casted_bit_seq;
return a;
}
uint8_t  int_index_set_9(){ 
uint8_t a;
a = 0;
uint8_t temp_24_casted_bit_seq = 0;
temp_24_casted_bit_seq |= 0x1 << 0;
temp_24_casted_bit_seq |= 0x1 << 1;
temp_24_casted_bit_seq |= 0x1 << 3;
a = (temp_24_casted_bit_seq + 10);
return a;
}
uint8_t  int_index_set_10(){ 
uint8_t a;
a = 0;
uint8_t temp_26_casted_bit_seq = 0;
temp_26_casted_bit_seq |= 0x1 << 0;
temp_26_casted_bit_seq |= 0x1 << 1;
temp_26_casted_bit_seq |= 0x1 << 3;
uint32_t temp_27_bit_seq = 0x0;
temp_27_bit_seq = (temp_26_casted_bit_seq << 1) | (temp_26_casted_bit_seq >> (4 - 1));
uint32_t temp_28_mask_loop_init = 4;
for(; temp_28_mask_loop_init < 32; temp_28_mask_loop_init++) {
temp_27_bit_seq &= ~(0x1 << temp_28_mask_loop_init);
}
a = (temp_27_bit_seq + 10);
return a;
}
uint8_t  int_index_set_11(){ 
uint8_t a;
a = 7;
uint8_t  temp_29_extracted = 0;
temp_29_extracted ^= (((a >> 3) & 0x1) << 0);
temp_29_extracted ^= (((a >> 2) & 0x1) << 1);
temp_29_extracted ^= (((a >> 1) & 0x1) << 2);
temp_29_extracted ^= (((a >> 0) & 0x1) << 3);
if(((temp_29_extracted >> 0) & 0x1) == 0 ){
a &= ~(0x1 <<0);
} else if (((temp_29_extracted >> 0) & 0x1) == 1 ){
a |= (0x1 << 0);
}
if(((temp_29_extracted >> 1) & 0x1) == 0 ){
a &= ~(0x1 <<1);
} else if (((temp_29_extracted >> 1) & 0x1) == 1 ){
a |= (0x1 << 1);
}
if(((temp_29_extracted >> 2) & 0x1) == 0 ){
a &= ~(0x1 <<2);
} else if (((temp_29_extracted >> 2) & 0x1) == 1 ){
a |= (0x1 << 2);
}
if(((temp_29_extracted >> 3) & 0x1) == 0 ){
a &= ~(0x1 <<3);
} else if (((temp_29_extracted >> 3) & 0x1) == 1 ){
a |= (0x1 << 3);
}
return a;
}
uint8_t  int_index_set_12(){ 
uint8_t a;
a = 15;
a &= ~(0x1 << 0);
return a;
}
uint8_t  int_index_set_13(){ 
uint8_t a;
a = 14;
a ^= (0x1 << 0);
return a;
}
uint32_t  (*int_index_set_14(uint32_t a[5][5][10][8]))[5][10][8]{ 
a[0][0][0][0] = 0xffffffff;
return a;
}

