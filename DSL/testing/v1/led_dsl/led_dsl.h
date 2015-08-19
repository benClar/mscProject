#include "../../../../LIB/BS_LIB.h"

void led(uint32_t input[4]);
uint32_t led_0(uint32_t A, uint32_t B, uint32_t C, uint32_t D);
uint32_t led_1(uint32_t A, uint32_t B, uint32_t C, uint32_t D);
uint32_t led_2(uint32_t A, uint32_t B, uint32_t C, uint32_t D);
uint32_t led_3(uint32_t A, uint32_t B, uint32_t C, uint32_t D);
void gmMult(uint32_t output[4], uint32_t a[4], uint32_t b[4]);
void MixColumnSerial(uint32_t state[64], uint32_t MDS[16][4]);
void shift_row(uint32_t state[64]);
void addConstants(uint32_t state[64], uint32_t constant[6]);
void subCells(uint32_t state[64]);
void step(uint32_t state[64], uint32_t r[6], uint32_t MDS[16][4]);
void enc(uint32_t state[64], uint32_t key[64], uint32_t MDS[16][4], uint32_t RC[32][6]);
