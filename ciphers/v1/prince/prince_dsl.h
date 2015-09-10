#include "../../BS_LIB/BS_LIB.h"

void prince(uint32_t input[4]);
uint32_t prince_0(uint32_t A, uint32_t B, uint32_t C, uint32_t D);
uint32_t prince_1(uint32_t A, uint32_t B, uint32_t C, uint32_t D);
uint32_t prince_2(uint32_t A, uint32_t B, uint32_t C, uint32_t D);
uint32_t prince_3(uint32_t A, uint32_t B, uint32_t C, uint32_t D);
void prince_inv(uint32_t input[4]);
uint32_t prince_inv_0(uint32_t A, uint32_t B, uint32_t C, uint32_t D);
uint32_t prince_inv_1(uint32_t A, uint32_t B, uint32_t C, uint32_t D);
uint32_t prince_inv_2(uint32_t A, uint32_t B, uint32_t C, uint32_t D);
uint32_t prince_inv_3(uint32_t A, uint32_t B, uint32_t C, uint32_t D);
uint32_t  (*enc(uint32_t RC[11][64], uint32_t state[64], uint32_t key_0[64], uint32_t key_1[64]));
void m0(uint32_t state[16], uint32_t output[16]);
void m1(uint32_t state[16], uint32_t output[16]);
void mPrime(uint32_t state[64]);
void sBox_layer(uint32_t state[64]);
void sBox_layer_inv(uint32_t state[64]);
void shift_rows(uint32_t state[64], uint32_t output[64], uint8_t inverse);
void first_rounds(uint32_t state[64], uint32_t key[64], uint32_t RC[11][64]);
void last_rounds(uint32_t state[64], uint32_t key[64], uint32_t RC[11][64]);

