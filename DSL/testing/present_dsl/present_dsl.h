#include "../../../LIB/BS_LIB.h"

void pLayer(uint32_t state[64]);
void generate_round_keys(uint32_t key[80], uint32_t round_keys[32][64]);
void sBox_layer(uint32_t state[64]);
void present(uint32_t input[4]);
uint32_t present_0(uint32_t A, uint32_t B, uint32_t C, uint32_t D);
uint32_t present_1(uint32_t A, uint32_t B, uint32_t C, uint32_t D);
uint32_t present_2(uint32_t A, uint32_t B, uint32_t C, uint32_t D);
uint32_t present_3(uint32_t A, uint32_t B, uint32_t C, uint32_t D);
uint32_t  (*enc(uint32_t key[80], uint32_t state[64]));
