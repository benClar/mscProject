#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "t.h"
void MixColumnSerial(uint32_t state[64], uint32_t MDS[16][4]){ 
uint32_t column[4][4] = {{ 0 }};
uint8_t col = 0;
col = 0;
for(;col < 4;) { 
uint32_t temp_1_rnge[(((col * 4) + 3) - (col * 4)) + 1];
extract_bs_range(temp_1_rnge, state, (col * 4), ((col * 4) + 3));
column[0][0] = temp_1_rnge[0];
column[0][1] = temp_1_rnge[1];
column[0][2] = temp_1_rnge[2];
column[0][3] = temp_1_rnge[3];
uint32_t temp_5_rnge[((((col + 4) * 4) + 3) - ((col + 4) * 4)) + 1];
extract_bs_range(temp_5_rnge, state, ((col + 4) * 4), (((col + 4) * 4) + 3));
column[1][0] = temp_5_rnge[0];
column[1][1] = temp_5_rnge[1];
column[1][2] = temp_5_rnge[2];
column[1][3] = temp_5_rnge[3];
uint32_t temp_11_rnge[((((col + 8) * 4) + 3) - ((col + 8) * 4)) + 1];
extract_bs_range(temp_11_rnge, state, ((col + 8) * 4), (((col + 8) * 4) + 3));
column[2][0] = temp_11_rnge[0];
column[2][1] = temp_11_rnge[1];
column[2][2] = temp_11_rnge[2];
column[2][3] = temp_11_rnge[3];
uint32_t temp_17_rnge[((((col + 12) * 4) + 3) - ((col + 12) * 4)) + 1];
extract_bs_range(temp_17_rnge, state, ((col + 12) * 4), (((col + 12) * 4) + 3));
column[3][0] = temp_17_rnge[0];
column[3][1] = temp_17_rnge[1];
column[3][2] = temp_17_rnge[2];
column[3][3] = temp_17_rnge[3];
uint8_t col_nibble = 0;
col_nibble = 0;
for(;col_nibble < 4;) { 
col_nibble = (col_nibble + 1);
} 
col = (col + 1);
} 
}

