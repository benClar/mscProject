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
uint8_t temp_1_seq_bit_val = 0;
temp_1_seq_bit_val |= (0x1 << (2 - 0));
temp_1_seq_bit_val |= (0x0 << (2 - 1));
temp_1_seq_bit_val |= (0x1 << (2 - 2));
if(((temp_1_seq_bit_val >> 0) & 0x1) == 0 ){
a &= ~(0x1 <<0);
} else if (((temp_1_seq_bit_val >> 0) & 0x1) == 1 ){
a |= (0x1 << 0);
}
if(((temp_1_seq_bit_val >> 1) & 0x1) == 0 ){
a &= ~(0x1 <<1);
} else if (((temp_1_seq_bit_val >> 1) & 0x1) == 1 ){
a |= (0x1 << 1);
}
if(((temp_1_seq_bit_val >> 2) & 0x1) == 0 ){
a &= ~(0x1 <<3);
} else if (((temp_1_seq_bit_val >> 2) & 0x1) == 1 ){
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
uint8_t  temp_4_extracted = 0;
temp_4_extracted ^= (((a >> 0) & 0x1) << 0);
temp_4_extracted ^= (((a >> 1) & 0x1) << 1);
temp_4_extracted ^= (((a >> 2) & 0x1) << 2);
temp_4_extracted ^= (((a >> 3) & 0x1) << 3);
uint32_t temp_5_bit_seq = 0x0;
temp_5_bit_seq = (temp_4_extracted << 3) | (temp_4_extracted >> (4 - 3));
if(((temp_5_bit_seq >> 0) & 0x1) == 0 ){
a &= ~(0x1 <<0);
} else if (((temp_5_bit_seq >> 0) & 0x1) == 1 ){
a |= (0x1 << 0);
}
if(((temp_5_bit_seq >> 1) & 0x1) == 0 ){
a &= ~(0x1 <<1);
} else if (((temp_5_bit_seq >> 1) & 0x1) == 1 ){
a |= (0x1 << 1);
}
if(((temp_5_bit_seq >> 2) & 0x1) == 0 ){
a &= ~(0x1 <<2);
} else if (((temp_5_bit_seq >> 2) & 0x1) == 1 ){
a |= (0x1 << 2);
}
if(((temp_5_bit_seq >> 3) & 0x1) == 0 ){
a &= ~(0x1 <<3);
} else if (((temp_5_bit_seq >> 3) & 0x1) == 1 ){
a |= (0x1 << 3);
}
return a;
}
uint8_t  int_index_set_5(){ 
uint8_t a;
a = 19;
uint8_t  temp_6_extracted = 0;
temp_6_extracted ^= (((a >> 0) & 0x1) << 0);
temp_6_extracted ^= (((a >> 1) & 0x1) << 1);
temp_6_extracted ^= (((a >> 2) & 0x1) << 2);
temp_6_extracted ^= (((a >> 3) & 0x1) << 3);
temp_6_extracted ^= (((a >> 4) & 0x1) << 4);
uint32_t temp_7_bit_seq = 0x0;
temp_7_bit_seq = (temp_6_extracted >> 3) | (temp_6_extracted << (5 - 3));
if(((temp_7_bit_seq >> 0) & 0x1) == 0 ){
a &= ~(0x1 <<0);
} else if (((temp_7_bit_seq >> 0) & 0x1) == 1 ){
a |= (0x1 << 0);
}
if(((temp_7_bit_seq >> 1) & 0x1) == 0 ){
a &= ~(0x1 <<1);
} else if (((temp_7_bit_seq >> 1) & 0x1) == 1 ){
a |= (0x1 << 1);
}
if(((temp_7_bit_seq >> 2) & 0x1) == 0 ){
a &= ~(0x1 <<2);
} else if (((temp_7_bit_seq >> 2) & 0x1) == 1 ){
a |= (0x1 << 2);
}
if(((temp_7_bit_seq >> 3) & 0x1) == 0 ){
a &= ~(0x1 <<3);
} else if (((temp_7_bit_seq >> 3) & 0x1) == 1 ){
a |= (0x1 << 3);
}
if(((temp_7_bit_seq >> 4) & 0x1) == 0 ){
a &= ~(0x1 <<4);
} else if (((temp_7_bit_seq >> 4) & 0x1) == 1 ){
a |= (0x1 << 4);
}
return a;
}
uint8_t  int_index_set_6(){ 
uint8_t a;
a = 19;
uint8_t  temp_8_extracted = 0;
uint8_t temp_9_int_rng_start  = 0;
uint8_t  temp_11_target_bit = 0;
for(;temp_9_int_rng_start < 4;temp_9_int_rng_start++, temp_11_target_bit++){
temp_8_extracted |= ((a >> temp_9_int_rng_start)  << temp_11_target_bit);
}
uint32_t temp_12_bit_seq = 0x0;
temp_12_bit_seq = (temp_8_extracted >> 3) | (temp_8_extracted << ((4 - 0) + 1 - 3));
if(((temp_12_bit_seq >> 0) & 0x1) == 0 ){
a &= ~(0x1 <<0);
} else if (((temp_12_bit_seq >> 0) & 0x1) == 1 ){
a |= (0x1 << 0);
}
if(((temp_12_bit_seq >> 1) & 0x1) == 0 ){
a &= ~(0x1 <<1);
} else if (((temp_12_bit_seq >> 1) & 0x1) == 1 ){
a |= (0x1 << 1);
}
if(((temp_12_bit_seq >> 2) & 0x1) == 0 ){
a &= ~(0x1 <<2);
} else if (((temp_12_bit_seq >> 2) & 0x1) == 1 ){
a |= (0x1 << 2);
}
if(((temp_12_bit_seq >> 3) & 0x1) == 0 ){
a &= ~(0x1 <<3);
} else if (((temp_12_bit_seq >> 3) & 0x1) == 1 ){
a |= (0x1 << 3);
}
if(((temp_12_bit_seq >> 4) & 0x1) == 0 ){
a &= ~(0x1 <<4);
} else if (((temp_12_bit_seq >> 4) & 0x1) == 1 ){
a |= (0x1 << 4);
}
return a;
}
uint8_t  int_index_set_7(){ 
uint8_t a;
a = 0;
uint8_t temp_13_seq_bit_val = 0;
temp_13_seq_bit_val |= (0x1 << (3 - 0));
temp_13_seq_bit_val |= (0x0 << (3 - 1));
temp_13_seq_bit_val |= (0x1 << (3 - 2));
temp_13_seq_bit_val |= (0x1 << (3 - 3));
uint32_t temp_14_rnge_size = 0;
temp_14_rnge_size = (4-0) + 1;
uint32_t temp_16_curr_bit;
uint32_t temp_15_rng_start;
for(temp_16_curr_bit = 0, temp_15_rng_start = 0; temp_15_rng_start < temp_14_rnge_size; temp_15_rng_start++, temp_16_curr_bit++) {
if(((temp_13_seq_bit_val >> temp_15_rng_start) & 0x1) == 0 ){
a &= ~(0x1 <<temp_16_curr_bit);
} else if (((temp_13_seq_bit_val >> temp_15_rng_start) & 0x1) == 1 ){
a |= (0x1 << temp_16_curr_bit);
}
}
return a;
}

