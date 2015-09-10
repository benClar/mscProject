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
uint8_t  temp_5_target_bit = 0;
for(;temp_3_int_rng_start < b;temp_3_int_rng_start++, temp_5_target_bit++){
temp_2_extracted |= ((a >> temp_3_int_rng_start)  << temp_5_target_bit);
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
uint8_t  temp_6_extracted = 0;
uint8_t temp_7_int_rng_start  = 0;
uint8_t  temp_9_target_bit = 0;
for(;temp_7_int_rng_start < 3;temp_7_int_rng_start++, temp_9_target_bit++){
temp_6_extracted |= ((a >> temp_7_int_rng_start)  << temp_9_target_bit);
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
uint32_t temp_10_rnge_size = 0;
temp_10_rnge_size = (b-a) + 1;
uint32_t temp_12_curr_bit;
uint32_t temp_11_rng_start;
for(temp_12_curr_bit = a, temp_11_rng_start = 0; temp_11_rng_start < temp_10_rnge_size; temp_11_rng_start++, temp_12_curr_bit++) {
if(((temp_6_extracted >> temp_11_rng_start) & 0x1) == 0 ){
b &= ~(0x1 <<temp_12_curr_bit);
} else if (((temp_6_extracted >> temp_11_rng_start) & 0x1) == 1 ){
b |= (0x1 << temp_12_curr_bit);
}
}
}
void Error_5(){ 
uint8_t a = 0;
a = 0;
uint8_t b = 0;
b = 10;
uint8_t  c[10] = { 0 };
uint8_t  temp_13_extracted = 0;
uint8_t temp_14_int_rng_start  = 0;
uint8_t  temp_16_target_bit = 0;
for(;temp_14_int_rng_start < 3;temp_14_int_rng_start++, temp_16_target_bit++){
temp_13_extracted |= ((a >> temp_14_int_rng_start)  << temp_16_target_bit);
}
if(b >= 10){
fprintf(stderr, "Index out of bounds for selection on c\n");
exit(1);
}
uint32_t temp_17_rnge_size = 0;
temp_17_rnge_size = (3-0) + 1;
uint32_t temp_19_curr_bit;
uint32_t temp_18_rng_start;
for(temp_19_curr_bit = 0, temp_18_rng_start = 0; temp_18_rng_start < temp_17_rnge_size; temp_18_rng_start++, temp_19_curr_bit++) {
if(((temp_13_extracted >> temp_18_rng_start) & 0x1) == 0 ){
c[b] &= ~(0x1 <<temp_19_curr_bit);
} else if (((temp_13_extracted >> temp_18_rng_start) & 0x1) == 1 ){
c[b] |= (0x1 << temp_19_curr_bit);
}
}
}
void Error_6(){ 
uint8_t a = 0;
a = 0;
uint8_t b = 0;
b = 10;
uint8_t  c[10][10] = {{ 0 }};
uint8_t  temp_20_extracted = 0;
temp_20_extracted = (a >> 0) & 0x1;
if(b >= 8){
fprintf(stderr, "Index out of bounds for selection on c\n");
exit(1);
}
if(temp_20_extracted) {
c[8][8] ^= (0x1 << b);
} else if(temp_20_extracted) {
c[8][8] &= ~(0x1 << b);
}
}

