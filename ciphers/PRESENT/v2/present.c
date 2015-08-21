/*---------- Standard Headers -----------*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
/*---------- Custom Headers	-----------*/

#include "debug.h"
#include "present.h"
#include "sput.h"

/*---------- Symbolic Constants  -----------*/


/*---------- Main -----------*/

void keyXOR(uint32_t key[80], int round)	{
	uint32_t r_bs[5] = {0};
	bitslice(r_bs, round, 5);
	key[79 - 19] ^= r_bs[4];
	key[79 - 18] ^= r_bs[3];
	key[79 - 17] ^= r_bs[2];
	key[79 - 16] ^= r_bs[1];
	key[79 - 15] ^= r_bs[0];
}

int generateRoundKey(uint32_t key[80], uint32_t round_key[32][64]) {
	for(int round = 1; round < 33; round++)	{
	    uint32_t key_temp[80] = {0};
	    uint32_t sbox_temp[4] = {0};
		round_key[round - 1][0] = key[0];
		round_key[round - 1][1] = key[1];
		round_key[round - 1][2] = key[2];
		round_key[round - 1][3] = key[3];
		round_key[round - 1][4] = key[4];
		round_key[round - 1][5] = key[5];
		round_key[round - 1][6] = key[6];
		round_key[round - 1][7] = key[7];
		round_key[round - 1][8] = key[8];
		round_key[round - 1][9] = key[9];
		round_key[round - 1][10] = key[10];
		round_key[round - 1][11] = key[11];
		round_key[round - 1][12] = key[12];
		round_key[round - 1][13] = key[13];
		round_key[round - 1][14] = key[14];
		round_key[round - 1][15] = key[15];
		round_key[round - 1][16] = key[16];
		round_key[round - 1][17] = key[17];
		round_key[round - 1][18] = key[18];
		round_key[round - 1][19] = key[19];
		round_key[round - 1][20] = key[20];
		round_key[round - 1][21] = key[21];
		round_key[round - 1][22] = key[22];
		round_key[round - 1][23] = key[23];
		round_key[round - 1][24] = key[24];
		round_key[round - 1][25] = key[25];
		round_key[round - 1][26] = key[26];
		round_key[round - 1][27] = key[27];
		round_key[round - 1][28] = key[28];
		round_key[round - 1][29] = key[29];
		round_key[round - 1][30] = key[30];
		round_key[round - 1][31] = key[31];
		round_key[round - 1][32] = key[32];
		round_key[round - 1][33] = key[33];
		round_key[round - 1][34] = key[34];
		round_key[round - 1][35] = key[35];
		round_key[round - 1][36] = key[36];
		round_key[round - 1][37] = key[37];
		round_key[round - 1][38] = key[38];
		round_key[round - 1][39] = key[39];
		round_key[round - 1][40] = key[40];
		round_key[round - 1][41] = key[41];
		round_key[round - 1][42] = key[42];
		round_key[round - 1][43] = key[43];
		round_key[round - 1][44] = key[44];
		round_key[round - 1][45] = key[45];
		round_key[round - 1][46] = key[46];
		round_key[round - 1][47] = key[47];
		round_key[round - 1][48] = key[48];
		round_key[round - 1][49] = key[49];
		round_key[round - 1][50] = key[50];
		round_key[round - 1][51] = key[51];
		round_key[round - 1][52] = key[52];
		round_key[round - 1][53] = key[53];
		round_key[round - 1][54] = key[54];
		round_key[round - 1][55] = key[55];
		round_key[round - 1][56] = key[56];
		round_key[round - 1][57] = key[57];
		round_key[round - 1][58] = key[58];
		round_key[round - 1][59] = key[59];
		round_key[round - 1][60] = key[60];
		round_key[round - 1][61] = key[61];
		round_key[round - 1][62] = key[62];
		round_key[round - 1][63] = key[63];

	    rotate_left(key_temp, key, 61, 80);
		key[0] = key_temp[0];
		key[1] = key_temp[1];
		key[2] = key_temp[2];
		key[3] = key_temp[3];
		key[4] = key_temp[4];
		key[5] = key_temp[5];
		key[6] = key_temp[6];
		key[7] = key_temp[7];
		key[8] = key_temp[8];
		key[9] = key_temp[9];
		key[10] = key_temp[10];
		key[11] = key_temp[11];
		key[12] = key_temp[12];
		key[13] = key_temp[13];
		key[14] = key_temp[14];
		key[15] = key_temp[15];
		key[16] = key_temp[16];
		key[17] = key_temp[17];
		key[18] = key_temp[18];
		key[19] = key_temp[19];
		key[20] = key_temp[20];
		key[21] = key_temp[21];
		key[22] = key_temp[22];
		key[23] = key_temp[23];
		key[24] = key_temp[24];
		key[25] = key_temp[25];
		key[26] = key_temp[26];
		key[27] = key_temp[27];
		key[28] = key_temp[28];
		key[29] = key_temp[29];
		key[30] = key_temp[30];
		key[31] = key_temp[31];
		key[32] = key_temp[32];
		key[33] = key_temp[33];
		key[34] = key_temp[34];
		key[35] = key_temp[35];
		key[36] = key_temp[36];
		key[37] = key_temp[37];
		key[38] = key_temp[38];
		key[39] = key_temp[39];
		key[40] = key_temp[40];
		key[41] = key_temp[41];
		key[42] = key_temp[42];
		key[43] = key_temp[43];
		key[44] = key_temp[44];
		key[45] = key_temp[45];
		key[46] = key_temp[46];
		key[47] = key_temp[47];
		key[48] = key_temp[48];
		key[49] = key_temp[49];
		key[50] = key_temp[50];
		key[51] = key_temp[51];
		key[52] = key_temp[52];
		key[53] = key_temp[53];
		key[54] = key_temp[54];
		key[55] = key_temp[55];
		key[56] = key_temp[56];
		key[57] = key_temp[57];
		key[58] = key_temp[58];
		key[59] = key_temp[59];
		key[60] = key_temp[60];
		key[61] = key_temp[61];
		key[62] = key_temp[62];
		key[63] = key_temp[63];
		key[64] = key_temp[64];
		key[65] = key_temp[65];
		key[66] = key_temp[66];
		key[67] = key_temp[67];
		key[68] = key_temp[68];
		key[69] = key_temp[69];
		key[70] = key_temp[70];
		key[71] = key_temp[71];
		key[72] = key_temp[72];
		key[73] = key_temp[73];
		key[74] = key_temp[74];
		key[75] = key_temp[75];
		key[76] = key_temp[76];
		key[77] = key_temp[77];
		key[78] = key_temp[78];
		key[79] = key_temp[79];
	    sbox_temp[0] = key[0];
	    sbox_temp[1] = key[1];
	    sbox_temp[2] = key[2];
	    sbox_temp[3] = key[3];
	    key[0] = sbox_1(sbox_temp);
		key[1] = sbox_2(sbox_temp);
		key[2] = sbox_3(sbox_temp);
		key[3] = sbox_4(sbox_temp);
		keyXOR(key,round);
	}
    return 1;
}

uint32_t sbox_1(uint32_t input[4])	{
	return ((~input[A] & ~input[C] & ~input[D] ) | (~input[A] & input[C] & input[D] ) | (input[A] & ~input[B] & input[D]) | (input[A] & ~input[B] & input[C]) | (~input[A] & input[B] & input[C]));
}

uint32_t sbox_2(uint32_t input[4])	{
	return ((~input[B] & input[C] & ~input[D]) | (input[A] & input[B] & ~input[C]) | (~input[B] & ~input[C] & input[D]) | (~input[A] & ~input[B] & ~input[C]) | (~input[A] & input[B] & input[C] & input[D]));
}

uint32_t sbox_3(uint32_t input[4])  {
	return ((input[A] & input[B] & input[D]) | (input[A] & ~input[B] & ~input[C]) | (~input[A] & input[C] & ~input[D]) | (~input[A] & ~input[B] & input[C]) | (input[A] & ~input[B] & ~input[D]));
}

uint32_t sbox_4(uint32_t input[4])  {
	return ((~input[A] & input[C] & input[D] ) | ( input[A] & input[C] & ~input[D] ) | (input[A] & ~input[B] & ~input[D] ) | (~input[A] & ~input[B] & input[D]) | ( ~input[A] & input[B] & ~input[C] & ~input[D]) | (input[A] & input[B] & ~input[C] & input[D]));
}


void pLayer(uint32_t state[64])	{
	int bit;
	uint32_t temp[64];
	temp[0] = state[0];
	temp[1] = state[1];
	temp[2] = state[2];
	temp[3] = state[3];
	temp[4] = state[4];
	temp[5] = state[5];
	temp[6] = state[6];
	temp[7] = state[7];
	temp[8] = state[8];
	temp[9] = state[9];
	temp[10] = state[10];
	temp[11] = state[11];
	temp[12] = state[12];
	temp[13] = state[13];
	temp[14] = state[14];
	temp[15] = state[15];
	temp[16] = state[16];
	temp[17] = state[17];
	temp[18] = state[18];
	temp[19] = state[19];
	temp[20] = state[20];
	temp[21] = state[21];
	temp[22] = state[22];
	temp[23] = state[23];
	temp[24] = state[24];
	temp[25] = state[25];
	temp[26] = state[26];
	temp[27] = state[27];
	temp[28] = state[28];
	temp[29] = state[29];
	temp[30] = state[30];
	temp[31] = state[31];
	temp[32] = state[32];
	temp[33] = state[33];
	temp[34] = state[34];
	temp[35] = state[35];
	temp[36] = state[36];
	temp[37] = state[37];
	temp[38] = state[38];
	temp[39] = state[39];
	temp[40] = state[40];
	temp[41] = state[41];
	temp[42] = state[42];
	temp[43] = state[43];
	temp[44] = state[44];
	temp[45] = state[45];
	temp[46] = state[46];
	temp[47] = state[47];
	temp[48] = state[48];
	temp[49] = state[49];
	temp[50] = state[50];
	temp[51] = state[51];
	temp[52] = state[52];
	temp[53] = state[53];
	temp[54] = state[54];
	temp[55] = state[55];
	temp[56] = state[56];
	temp[57] = state[57];
	temp[58] = state[58];
	temp[59] = state[59];
	temp[60] = state[60];
	temp[61] = state[61];
	temp[62] = state[62];
	temp[63] = state[63];

	for(bit = 63; bit >= 0; bit-- )	{
		int target = ((16 * (63 - bit)) % (STATE_SIZE - 1));
		if(bit == 0)	{
			target = 0;
		}	else {
			target = 63 - target;
		}
		state[ target] = temp[ bit ];
	}
}

void add_round_key(uint32_t key[64], uint32_t state[64])	{
	state[0] ^= key[0];
	state[1] ^= key[1];
	state[2] ^= key[2];
	state[3] ^= key[3];
	state[4] ^= key[4];
	state[5] ^= key[5];
	state[6] ^= key[6];
	state[7] ^= key[7];
	state[8] ^= key[8];
	state[9] ^= key[9];
	state[10] ^= key[10];
	state[11] ^= key[11];
	state[12] ^= key[12];
	state[13] ^= key[13];
	state[14] ^= key[14];
	state[15] ^= key[15];
	state[16] ^= key[16];
	state[17] ^= key[17];
	state[18] ^= key[18];
	state[19] ^= key[19];
	state[20] ^= key[20];
	state[21] ^= key[21];
	state[22] ^= key[22];
	state[23] ^= key[23];
	state[24] ^= key[24];
	state[25] ^= key[25];
	state[26] ^= key[26];
	state[27] ^= key[27];
	state[28] ^= key[28];
	state[29] ^= key[29];
	state[30] ^= key[30];
	state[31] ^= key[31];
	state[32] ^= key[32];
	state[33] ^= key[33];
	state[34] ^= key[34];
	state[35] ^= key[35];
	state[36] ^= key[36];
	state[37] ^= key[37];
	state[38] ^= key[38];
	state[39] ^= key[39];
	state[40] ^= key[40];
	state[41] ^= key[41];
	state[42] ^= key[42];
	state[43] ^= key[43];
	state[44] ^= key[44];
	state[45] ^= key[45];
	state[46] ^= key[46];
	state[47] ^= key[47];
	state[48] ^= key[48];
	state[49] ^= key[49];
	state[50] ^= key[50];
	state[51] ^= key[51];
	state[52] ^= key[52];
	state[53] ^= key[53];
	state[54] ^= key[54];
	state[55] ^= key[55];
	state[56] ^= key[56];
	state[57] ^= key[57];
	state[58] ^= key[58];
	state[59] ^= key[59];
	state[60] ^= key[60];
	state[61] ^= key[61];
	state[62] ^= key[62];
	state[63] ^= key[63];
}

void sBox_layer(uint32_t state[64])	{
	uint32_t nibble[4];
	int nibble_ele, bit_ele;
	for(nibble_ele = 0; nibble_ele < 16; nibble_ele++)	{
		bit_ele = (nibble_ele * 4);
		nibble[0] = state[bit_ele];
		nibble[1] = state[bit_ele + 1];
		nibble[2] = state[bit_ele + 2];
		nibble[3] = state[bit_ele + 3];
	    state[bit_ele] = sbox_1(nibble);
		state[bit_ele + 1] = sbox_2(nibble);
		state[bit_ele + 2] = sbox_3(nibble);
		state[bit_ele + 3] = sbox_4(nibble);
	}
}

uint32_t (*enc(uint32_t key[80], uint32_t state[64], uint32_t round_key[32][64])){
	int round;

	generateRoundKey(key,round_key);

	for(round = 0; round < 31; round++)	{
		add_round_key(round_key[round],state);
		sBox_layer(state);
		pLayer(state);
	}
	add_round_key(round_key[round],state);
	return state;								
}
