#include "../../LIB/BS_LIB.h"

#define A   0   
#define B   1
#define C   2
#define D   3

void enc(uint32_t state[64], uint32_t key[64], uint32_t MDS[16][4], uint32_t RCRC[32][6]);
void step(uint32_t curr_state[64], uint32_t rc[6], uint32_t MDS[16][4]);
void mixColumnsSerial(uint32_t curr_state[64], uint32_t mds[16][4]);
void gm_bs_2(uint32_t g[8], uint32_t a[4], uint32_t b[4]);
void addConstants(uint32_t state[64], uint32_t r_cnst[6]);
void shiftRow(uint32_t curr_state[64]);
uint8_t sbox_1(uint32_t input[4]);
uint8_t sbox_2(uint32_t input[4]);
uint8_t sbox_3(uint32_t input[4]);
uint8_t sbox_4(uint32_t input[4]);
void sBox_array_input(uint32_t output[4], uint32_t input[4]);
void subCells(uint32_t curr_state[64]);
