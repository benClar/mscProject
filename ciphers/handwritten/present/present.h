#include "../../BS_LIB/BS_LIB.h"



/*----------Symbolic Constants-----------*/
#define KEY_SIZE	80
#define ROUND_KEY_SIZE 64
#define LEFT_SHIFT 61
#define STATE_SIZE 64
#define A 	0	
#define B 	1
#define C 	2
#define D 	3


/*----------Function Prototypes-----------*/
void keyXOR(uint32_t key[80], int round);
int generateRoundKey(uint32_t key[80], uint32_t round_key[32][64]);
uint32_t sbox_1(uint32_t input[4]);
uint32_t sbox_2(uint32_t input[4]);
uint32_t sbox_3(uint32_t input[4]);
uint32_t sbox_4(uint32_t input[4]);
void sBox_layer(uint32_t state[64]);
void pLayer(uint32_t state[64]);
void add_round_key(uint32_t key[64], uint32_t state[64]);
uint32_t (*enc(uint32_t key[80], uint32_t state[64], uint32_t round_key[32][64]));
