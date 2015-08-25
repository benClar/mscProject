#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "int_extraction.h"
uint8_t  int_XOR_1(){ 
uint8_t a = 0;
a = 10;
uint8_t b = 0;
b = 13;
uint8_t c = 0;
uint8_t  temp_1_extracted = 0;
temp_1_extracted = (a >> 1) & 0x1;
uint8_t  temp_2_extracted = 0;
temp_2_extracted = (b >> 1) & 0x1;
if((temp_1_extracted ^ temp_2_extracted)) {
c ^= (0x1 << 0);
} else if((temp_1_extracted ^ temp_2_extracted)) {
c &= ~(0x1 << 0);
}
return c;
}
uint8_t  int_index_set_1(){ 
uint8_t a = 0;
a = 0;
uint8_t temp_3_casted_bit_seq = 0;
temp_3_casted_bit_seq |= 0x1 << 0;
temp_3_casted_bit_seq |= 0x1 << 1;
temp_3_casted_bit_seq |= 0x1 << 2;
if(((temp_3_casted_bit_seq >> 0) & 0x1) == 0 ){
a &= ~(0x1 <<0);
} else if (((temp_3_casted_bit_seq >> 0) & 0x1) == 1 ){
a |= (0x1 << 0);
}
if(((temp_3_casted_bit_seq >> 1) & 0x1) == 0 ){
a &= ~(0x1 <<1);
} else if (((temp_3_casted_bit_seq >> 1) & 0x1) == 1 ){
a |= (0x1 << 1);
}
if(((temp_3_casted_bit_seq >> 2) & 0x1) == 0 ){
a &= ~(0x1 <<3);
} else if (((temp_3_casted_bit_seq >> 2) & 0x1) == 1 ){
a |= (0x1 << 3);
}
return a;
}

