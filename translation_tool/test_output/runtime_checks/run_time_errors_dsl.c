#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "run_time_errors_dsl.h"
void Error_1(){ 
uint8_t a = 0;
a = 7;
uint8_t b = 0;
b = 9;
if(a >= 8){
fprintf(stderr, "Index out of bounds for selection on a\n");
exit(1);
}
if(b >= 8){
fprintf(stderr, "Index out of bounds for selection on a\n");
exit(1);
}
uint8_t  temp_0_extracted = 0;
temp_0_extracted ^= (((a >> a) & 0x1) << 0);
temp_0_extracted ^= (((a >> b) & 0x1) << 1);
if(((temp_0_extracted >> 0) & 0x1) == 0 ){
b &= ~(0x1 <<0);
} else if (((temp_0_extracted >> 0) & 0x1) == 1 ){
b |= (0x1 << 0);
}
if(((temp_0_extracted >> 1) & 0x1) == 0 ){
b &= ~(0x1 <<1);
} else if (((temp_0_extracted >> 1) & 0x1) == 1 ){
b |= (0x1 << 1);
}
if(((temp_0_extracted >> 2) & 0x1) == 0 ){
b &= ~(0x1 <<2);
} else if (((temp_0_extracted >> 2) & 0x1) == 1 ){
b |= (0x1 << 2);
}
if(((temp_0_extracted >> 3) & 0x1) == 0 ){
b &= ~(0x1 <<3);
} else if (((temp_0_extracted >> 3) & 0x1) == 1 ){
b |= (0x1 << 3);
}
if(((temp_0_extracted >> 4) & 0x1) == 0 ){
b &= ~(0x1 <<4);
} else if (((temp_0_extracted >> 4) & 0x1) == 1 ){
b |= (0x1 << 4);
}
}
void Non_Error_2(){ 
uint8_t a = 0;
a = 5;
uint8_t b = 0;
b = 7;
if(a >= 8){
fprintf(stderr, "Index out of bounds for selection on a\n");
exit(1);
}
if(b >= 8){
fprintf(stderr, "Index out of bounds for selection on a\n");
exit(1);
}
uint8_t  temp_1_extracted = 0;
temp_1_extracted ^= (((a >> a) & 0x1) << 0);
temp_1_extracted ^= (((a >> b) & 0x1) << 1);
if(((temp_1_extracted >> 0) & 0x1) == 0 ){
b &= ~(0x1 <<0);
} else if (((temp_1_extracted >> 0) & 0x1) == 1 ){
b |= (0x1 << 0);
}
if(((temp_1_extracted >> 1) & 0x1) == 0 ){
b &= ~(0x1 <<1);
} else if (((temp_1_extracted >> 1) & 0x1) == 1 ){
b |= (0x1 << 1);
}
if(((temp_1_extracted >> 2) & 0x1) == 0 ){
b &= ~(0x1 <<2);
} else if (((temp_1_extracted >> 2) & 0x1) == 1 ){
b |= (0x1 << 2);
}
if(((temp_1_extracted >> 3) & 0x1) == 0 ){
b &= ~(0x1 <<3);
} else if (((temp_1_extracted >> 3) & 0x1) == 1 ){
b |= (0x1 << 3);
}
if(((temp_1_extracted >> 4) & 0x1) == 0 ){
b &= ~(0x1 <<4);
} else if (((temp_1_extracted >> 4) & 0x1) == 1 ){
b |= (0x1 << 4);
}
}
void Error_3(){ 
uint8_t a = 0;
a = 5;
uint8_t b = 0;
b = 2;
if(a >= 8){
fprintf(stderr, "Index out of bounds for selection on a\n");
exit(1);
}
if(b >= 8){
fprintf(stderr, "Index out of bounds for selection on a\n");
exit(1);
}
if(a > b){
fprintf(stderr, "Start of range cannot be larger than end for index select on a \n");
exit(1);
}
uint8_t  temp_2_extracted = 0;
uint8_t temp_3_int_rng_start  = a;
uint8_t  temp_4_target_bit = 0;
for(;temp_3_int_rng_start < b;temp_3_int_rng_start++, temp_4_target_bit++){
temp_2_extracted |= ((a >> temp_3_int_rng_start)  << temp_4_target_bit);
}
if(((temp_2_extracted >> 0) & 0x1) == 0 ){
b &= ~(0x1 <<0);
} else if (((temp_2_extracted >> 0) & 0x1) == 1 ){
b |= (0x1 << 0);
}
if(((temp_2_extracted >> 1) & 0x1) == 0 ){
b &= ~(0x1 <<1);
} else if (((temp_2_extracted >> 1) & 0x1) == 1 ){
b |= (0x1 << 1);
}
if(((temp_2_extracted >> 2) & 0x1) == 0 ){
b &= ~(0x1 <<2);
} else if (((temp_2_extracted >> 2) & 0x1) == 1 ){
b |= (0x1 << 2);
}
if(((temp_2_extracted >> 3) & 0x1) == 0 ){
b &= ~(0x1 <<3);
} else if (((temp_2_extracted >> 3) & 0x1) == 1 ){
b |= (0x1 << 3);
}
if(((temp_2_extracted >> 4) & 0x1) == 0 ){
b &= ~(0x1 <<4);
} else if (((temp_2_extracted >> 4) & 0x1) == 1 ){
b |= (0x1 << 4);
}
}
void Error_4(){ 
uint8_t a = 0;
a = 0;
uint8_t b = 0;
b = 10;
uint8_t  temp_5_extracted = 0;
uint8_t temp_6_int_rng_start  = 0;
uint8_t  temp_7_target_bit = 0;
for(;temp_6_int_rng_start < 3;temp_6_int_rng_start++, temp_7_target_bit++){
temp_5_extracted |= ((a >> temp_6_int_rng_start)  << temp_7_target_bit);
}
if(a >= 8){
fprintf(stderr, "Index out of bounds for selection on b\n");
exit(1);
}
if(b >= 8){
fprintf(stderr, "Index out of bounds for selection on b\n");
exit(1);
}
if(a > b){
fprintf(stderr, "Start of range cannot be larger than end for index select on b \n");
exit(1);
}
uint32_t temp_8_rnge_size = 0;
temp_8_rnge_size = (b-a) + 1;
uint32_t temp_10_curr_bit;
uint32_t temp_9_rng_start;
for(temp_10_curr_bit = a, temp_9_rng_start = 0; temp_9_rng_start < temp_8_rnge_size; temp_9_rng_start++, temp_10_curr_bit++) {
if(((temp_5_extracted >> temp_9_rng_start) & 0x1) == 0 ){
b &= ~(0x1 <<temp_10_curr_bit);
} else if (((temp_5_extracted >> temp_9_rng_start) & 0x1) == 1 ){
b |= (0x1 << temp_10_curr_bit);
}
}
}
void Error_5(){ 
uint8_t a = 0;
a = 0;
uint8_t b = 0;
b = 10;
uint8_t  c[10] = { 0 };
uint8_t  temp_11_extracted = 0;
uint8_t temp_12_int_rng_start  = 0;
uint8_t  temp_13_target_bit = 0;
for(;temp_12_int_rng_start < 3;temp_12_int_rng_start++, temp_13_target_bit++){
temp_11_extracted |= ((a >> temp_12_int_rng_start)  << temp_13_target_bit);
}
if(b >= 10){
fprintf(stderr, "Index out of bounds for selection on c\n");
exit(1);
}
uint32_t temp_14_rnge_size = 0;
temp_14_rnge_size = (3-0) + 1;
uint32_t temp_16_curr_bit;
uint32_t temp_15_rng_start;
for(temp_16_curr_bit = 0, temp_15_rng_start = 0; temp_15_rng_start < temp_14_rnge_size; temp_15_rng_start++, temp_16_curr_bit++) {
if(((temp_11_extracted >> temp_15_rng_start) & 0x1) == 0 ){
c[b] &= ~(0x1 <<temp_16_curr_bit);
} else if (((temp_11_extracted >> temp_15_rng_start) & 0x1) == 1 ){
c[b] |= (0x1 << temp_16_curr_bit);
}
}
}
void Error_6(){ 
uint8_t a = 0;
a = 0;
uint8_t b = 0;
b = 10;
uint8_t  c[10][10] = {{ 0 }};
uint8_t  temp_17_extracted = 0;
temp_17_extracted = (a >> 0) & 0x1;
if(b >= 8){
fprintf(stderr, "Index out of bounds for selection on c\n");
exit(1);
}
if(temp_17_extracted) {
c[8][8] ^= (0x1 << b);
} else if(temp_17_extracted) {
c[8][8] &= ~(0x1 << b);
}
}

