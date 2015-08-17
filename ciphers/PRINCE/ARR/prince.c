/*---------- Standard Headers -----------*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
/*---------- Custom Headers	-----------*/

#include "prince.h"
#include "sput.h"


uint32_t (*enc(uint32_t RC[12][64], uint32_t state[64],uint32_t key_0[64],uint32_t key_1[64]))	{

	uint32_t key_0_not[64];
	uint32_t key_circ[64];
	uint32_t key_shift[64] = {0}; 
	rotate_right(key_circ, key_0, 1, 64);
	shift_right(key_shift, key_0, 63, 64);
	key_0_not[0] = key_circ[0] ^ key_shift[0];
	key_0_not[1] = key_circ[1] ^ key_shift[1];
	key_0_not[2] = key_circ[2] ^ key_shift[2];
	key_0_not[3] = key_circ[3] ^ key_shift[3];
	key_0_not[4] = key_circ[4] ^ key_shift[4];
	key_0_not[5] = key_circ[5] ^ key_shift[5];
	key_0_not[6] = key_circ[6] ^ key_shift[6];
	key_0_not[7] = key_circ[7] ^ key_shift[7];
	key_0_not[8] = key_circ[8] ^ key_shift[8];
	key_0_not[9] = key_circ[9] ^ key_shift[9];
	key_0_not[10] = key_circ[10] ^ key_shift[10];
	key_0_not[11] = key_circ[11] ^ key_shift[11];
	key_0_not[12] = key_circ[12] ^ key_shift[12];
	key_0_not[13] = key_circ[13] ^ key_shift[13];
	key_0_not[14] = key_circ[14] ^ key_shift[14];
	key_0_not[15] = key_circ[15] ^ key_shift[15];
	key_0_not[16] = key_circ[16] ^ key_shift[16];
	key_0_not[17] = key_circ[17] ^ key_shift[17];
	key_0_not[18] = key_circ[18] ^ key_shift[18];
	key_0_not[19] = key_circ[19] ^ key_shift[19];
	key_0_not[20] = key_circ[20] ^ key_shift[20];
	key_0_not[21] = key_circ[21] ^ key_shift[21];
	key_0_not[22] = key_circ[22] ^ key_shift[22];
	key_0_not[23] = key_circ[23] ^ key_shift[23];
	key_0_not[24] = key_circ[24] ^ key_shift[24];
	key_0_not[25] = key_circ[25] ^ key_shift[25];
	key_0_not[26] = key_circ[26] ^ key_shift[26];
	key_0_not[27] = key_circ[27] ^ key_shift[27];
	key_0_not[28] = key_circ[28] ^ key_shift[28];
	key_0_not[29] = key_circ[29] ^ key_shift[29];
	key_0_not[30] = key_circ[30] ^ key_shift[30];
	key_0_not[31] = key_circ[31] ^ key_shift[31];
	key_0_not[32] = key_circ[32] ^ key_shift[32];
	key_0_not[33] = key_circ[33] ^ key_shift[33];
	key_0_not[34] = key_circ[34] ^ key_shift[34];
	key_0_not[35] = key_circ[35] ^ key_shift[35];
	key_0_not[36] = key_circ[36] ^ key_shift[36];
	key_0_not[37] = key_circ[37] ^ key_shift[37];
	key_0_not[38] = key_circ[38] ^ key_shift[38];
	key_0_not[39] = key_circ[39] ^ key_shift[39];
	key_0_not[40] = key_circ[40] ^ key_shift[40];
	key_0_not[41] = key_circ[41] ^ key_shift[41];
	key_0_not[42] = key_circ[42] ^ key_shift[42];
	key_0_not[43] = key_circ[43] ^ key_shift[43];
	key_0_not[44] = key_circ[44] ^ key_shift[44];
	key_0_not[45] = key_circ[45] ^ key_shift[45];
	key_0_not[46] = key_circ[46] ^ key_shift[46];
	key_0_not[47] = key_circ[47] ^ key_shift[47];
	key_0_not[48] = key_circ[48] ^ key_shift[48];
	key_0_not[49] = key_circ[49] ^ key_shift[49];
	key_0_not[50] = key_circ[50] ^ key_shift[50];
	key_0_not[51] = key_circ[51] ^ key_shift[51];
	key_0_not[52] = key_circ[52] ^ key_shift[52];
	key_0_not[53] = key_circ[53] ^ key_shift[53];
	key_0_not[54] = key_circ[54] ^ key_shift[54];
	key_0_not[55] = key_circ[55] ^ key_shift[55];
	key_0_not[56] = key_circ[56] ^ key_shift[56];
	key_0_not[57] = key_circ[57] ^ key_shift[57];
	key_0_not[58] = key_circ[58] ^ key_shift[58];
	key_0_not[59] = key_circ[59] ^ key_shift[59];
	key_0_not[60] = key_circ[60] ^ key_shift[60];
	key_0_not[61] = key_circ[61] ^ key_shift[61];
	key_0_not[62] = key_circ[62] ^ key_shift[62];
	key_0_not[63] = key_circ[63] ^ key_shift[63];

	state[0] ^= key_0[0];
	state[1] ^= key_0[1];
	state[2] ^= key_0[2];
	state[3] ^= key_0[3];
	state[4] ^= key_0[4];
	state[5] ^= key_0[5];
	state[6] ^= key_0[6];
	state[7] ^= key_0[7];
	state[8] ^= key_0[8];
	state[9] ^= key_0[9];
	state[10] ^= key_0[10];
	state[11] ^= key_0[11];
	state[12] ^= key_0[12];
	state[13] ^= key_0[13];
	state[14] ^= key_0[14];
	state[15] ^= key_0[15];
	state[16] ^= key_0[16];
	state[17] ^= key_0[17];
	state[18] ^= key_0[18];
	state[19] ^= key_0[19];
	state[20] ^= key_0[20];
	state[21] ^= key_0[21];
	state[22] ^= key_0[22];
	state[23] ^= key_0[23];
	state[24] ^= key_0[24];
	state[25] ^= key_0[25];
	state[26] ^= key_0[26];
	state[27] ^= key_0[27];
	state[28] ^= key_0[28];
	state[29] ^= key_0[29];
	state[30] ^= key_0[30];
	state[31] ^= key_0[31];
	state[32] ^= key_0[32];
	state[33] ^= key_0[33];
	state[34] ^= key_0[34];
	state[35] ^= key_0[35];
	state[36] ^= key_0[36];
	state[37] ^= key_0[37];
	state[38] ^= key_0[38];
	state[39] ^= key_0[39];
	state[40] ^= key_0[40];
	state[41] ^= key_0[41];
	state[42] ^= key_0[42];
	state[43] ^= key_0[43];
	state[44] ^= key_0[44];
	state[45] ^= key_0[45];
	state[46] ^= key_0[46];
	state[47] ^= key_0[47];
	state[48] ^= key_0[48];
	state[49] ^= key_0[49];
	state[50] ^= key_0[50];
	state[51] ^= key_0[51];
	state[52] ^= key_0[52];
	state[53] ^= key_0[53];
	state[54] ^= key_0[54];
	state[55] ^= key_0[55];
	state[56] ^= key_0[56];
	state[57] ^= key_0[57];
	state[58] ^= key_0[58];
	state[59] ^= key_0[59];
	state[60] ^= key_0[60];
	state[61] ^= key_0[61];
	state[62] ^= key_0[62];
	state[63] ^= key_0[63];

	state[0] ^= (key_1[0] ^ RC[0][0]);
	state[1] ^= (key_1[1] ^ RC[0][1]);
	state[2] ^= (key_1[2] ^ RC[0][2]);
	state[3] ^= (key_1[3] ^ RC[0][3]);
	state[4] ^= (key_1[4] ^ RC[0][4]);
	state[5] ^= (key_1[5] ^ RC[0][5]);
	state[6] ^= (key_1[6] ^ RC[0][6]);
	state[7] ^= (key_1[7] ^ RC[0][7]);
	state[8] ^= (key_1[8] ^ RC[0][8]);
	state[9] ^= (key_1[9] ^ RC[0][9]);
	state[10] ^= (key_1[10] ^ RC[0][10]);
	state[11] ^= (key_1[11] ^ RC[0][11]);
	state[12] ^= (key_1[12] ^ RC[0][12]);
	state[13] ^= (key_1[13] ^ RC[0][13]);
	state[14] ^= (key_1[14] ^ RC[0][14]);
	state[15] ^= (key_1[15] ^ RC[0][15]);
	state[16] ^= (key_1[16] ^ RC[0][16]);
	state[17] ^= (key_1[17] ^ RC[0][17]);
	state[18] ^= (key_1[18] ^ RC[0][18]);
	state[19] ^= (key_1[19] ^ RC[0][19]);
	state[20] ^= (key_1[20] ^ RC[0][20]);
	state[21] ^= (key_1[21] ^ RC[0][21]);
	state[22] ^= (key_1[22] ^ RC[0][22]);
	state[23] ^= (key_1[23] ^ RC[0][23]);
	state[24] ^= (key_1[24] ^ RC[0][24]);
	state[25] ^= (key_1[25] ^ RC[0][25]);
	state[26] ^= (key_1[26] ^ RC[0][26]);
	state[27] ^= (key_1[27] ^ RC[0][27]);
	state[28] ^= (key_1[28] ^ RC[0][28]);
	state[29] ^= (key_1[29] ^ RC[0][29]);
	state[30] ^= (key_1[30] ^ RC[0][30]);
	state[31] ^= (key_1[31] ^ RC[0][31]);
	state[32] ^= (key_1[32] ^ RC[0][32]);
	state[33] ^= (key_1[33] ^ RC[0][33]);
	state[34] ^= (key_1[34] ^ RC[0][34]);
	state[35] ^= (key_1[35] ^ RC[0][35]);
	state[36] ^= (key_1[36] ^ RC[0][36]);
	state[37] ^= (key_1[37] ^ RC[0][37]);
	state[38] ^= (key_1[38] ^ RC[0][38]);
	state[39] ^= (key_1[39] ^ RC[0][39]);
	state[40] ^= (key_1[40] ^ RC[0][40]);
	state[41] ^= (key_1[41] ^ RC[0][41]);
	state[42] ^= (key_1[42] ^ RC[0][42]);
	state[43] ^= (key_1[43] ^ RC[0][43]);
	state[44] ^= (key_1[44] ^ RC[0][44]);
	state[45] ^= (key_1[45] ^ RC[0][45]);
	state[46] ^= (key_1[46] ^ RC[0][46]);
	state[47] ^= (key_1[47] ^ RC[0][47]);
	state[48] ^= (key_1[48] ^ RC[0][48]);
	state[49] ^= (key_1[49] ^ RC[0][49]);
	state[50] ^= (key_1[50] ^ RC[0][50]);
	state[51] ^= (key_1[51] ^ RC[0][51]);
	state[52] ^= (key_1[52] ^ RC[0][52]);
	state[53] ^= (key_1[53] ^ RC[0][53]);
	state[54] ^= (key_1[54] ^ RC[0][54]);
	state[55] ^= (key_1[55] ^ RC[0][55]);
	state[56] ^= (key_1[56] ^ RC[0][56]);
	state[57] ^= (key_1[57] ^ RC[0][57]);
	state[58] ^= (key_1[58] ^ RC[0][58]);
	state[59] ^= (key_1[59] ^ RC[0][59]);
	state[60] ^= (key_1[60] ^ RC[0][60]);
	state[61] ^= (key_1[61] ^ RC[0][61]);
	state[62] ^= (key_1[62] ^ RC[0][62]);
	state[63] ^= (key_1[63] ^ RC[0][63]);
	first_rounds(state, RC, key_1);

	sBox(state, 0);
	mprime(state);
	sBox(state, 1);

	last_rounds(state, RC, key_1);
	state[0] ^= (key_1[0] ^ RC[11][0]);
	state[1] ^= (key_1[1] ^ RC[11][1]);
	state[2] ^= (key_1[2] ^ RC[11][2]);
	state[3] ^= (key_1[3] ^ RC[11][3]);
	state[4] ^= (key_1[4] ^ RC[11][4]);
	state[5] ^= (key_1[5] ^ RC[11][5]);
	state[6] ^= (key_1[6] ^ RC[11][6]);
	state[7] ^= (key_1[7] ^ RC[11][7]);
	state[8] ^= (key_1[8] ^ RC[11][8]);
	state[9] ^= (key_1[9] ^ RC[11][9]);
	state[10] ^= (key_1[10] ^ RC[11][10]);
	state[11] ^= (key_1[11] ^ RC[11][11]);
	state[12] ^= (key_1[12] ^ RC[11][12]);
	state[13] ^= (key_1[13] ^ RC[11][13]);
	state[14] ^= (key_1[14] ^ RC[11][14]);
	state[15] ^= (key_1[15] ^ RC[11][15]);
	state[16] ^= (key_1[16] ^ RC[11][16]);
	state[17] ^= (key_1[17] ^ RC[11][17]);
	state[18] ^= (key_1[18] ^ RC[11][18]);
	state[19] ^= (key_1[19] ^ RC[11][19]);
	state[20] ^= (key_1[20] ^ RC[11][20]);
	state[21] ^= (key_1[21] ^ RC[11][21]);
	state[22] ^= (key_1[22] ^ RC[11][22]);
	state[23] ^= (key_1[23] ^ RC[11][23]);
	state[24] ^= (key_1[24] ^ RC[11][24]);
	state[25] ^= (key_1[25] ^ RC[11][25]);
	state[26] ^= (key_1[26] ^ RC[11][26]);
	state[27] ^= (key_1[27] ^ RC[11][27]);
	state[28] ^= (key_1[28] ^ RC[11][28]);
	state[29] ^= (key_1[29] ^ RC[11][29]);
	state[30] ^= (key_1[30] ^ RC[11][30]);
	state[31] ^= (key_1[31] ^ RC[11][31]);
	state[32] ^= (key_1[32] ^ RC[11][32]);
	state[33] ^= (key_1[33] ^ RC[11][33]);
	state[34] ^= (key_1[34] ^ RC[11][34]);
	state[35] ^= (key_1[35] ^ RC[11][35]);
	state[36] ^= (key_1[36] ^ RC[11][36]);
	state[37] ^= (key_1[37] ^ RC[11][37]);
	state[38] ^= (key_1[38] ^ RC[11][38]);
	state[39] ^= (key_1[39] ^ RC[11][39]);
	state[40] ^= (key_1[40] ^ RC[11][40]);
	state[41] ^= (key_1[41] ^ RC[11][41]);
	state[42] ^= (key_1[42] ^ RC[11][42]);
	state[43] ^= (key_1[43] ^ RC[11][43]);
	state[44] ^= (key_1[44] ^ RC[11][44]);
	state[45] ^= (key_1[45] ^ RC[11][45]);
	state[46] ^= (key_1[46] ^ RC[11][46]);
	state[47] ^= (key_1[47] ^ RC[11][47]);
	state[48] ^= (key_1[48] ^ RC[11][48]);
	state[49] ^= (key_1[49] ^ RC[11][49]);
	state[50] ^= (key_1[50] ^ RC[11][50]);
	state[51] ^= (key_1[51] ^ RC[11][51]);
	state[52] ^= (key_1[52] ^ RC[11][52]);
	state[53] ^= (key_1[53] ^ RC[11][53]);
	state[54] ^= (key_1[54] ^ RC[11][54]);
	state[55] ^= (key_1[55] ^ RC[11][55]);
	state[56] ^= (key_1[56] ^ RC[11][56]);
	state[57] ^= (key_1[57] ^ RC[11][57]);
	state[58] ^= (key_1[58] ^ RC[11][58]);
	state[59] ^= (key_1[59] ^ RC[11][59]);
	state[60] ^= (key_1[60] ^ RC[11][60]);
	state[61] ^= (key_1[61] ^ RC[11][61]);
	state[62] ^= (key_1[62] ^ RC[11][62]);
	state[63] ^= (key_1[63] ^ RC[11][63]);
	state[0] ^= key_0_not[0];
	state[1] ^= key_0_not[1];
	state[2] ^= key_0_not[2];
	state[3] ^= key_0_not[3];
	state[4] ^= key_0_not[4];
	state[5] ^= key_0_not[5];
	state[6] ^= key_0_not[6];
	state[7] ^= key_0_not[7];
	state[8] ^= key_0_not[8];
	state[9] ^= key_0_not[9];
	state[10] ^= key_0_not[10];
	state[11] ^= key_0_not[11];
	state[12] ^= key_0_not[12];
	state[13] ^= key_0_not[13];
	state[14] ^= key_0_not[14];
	state[15] ^= key_0_not[15];
	state[16] ^= key_0_not[16];
	state[17] ^= key_0_not[17];
	state[18] ^= key_0_not[18];
	state[19] ^= key_0_not[19];
	state[20] ^= key_0_not[20];
	state[21] ^= key_0_not[21];
	state[22] ^= key_0_not[22];
	state[23] ^= key_0_not[23];
	state[24] ^= key_0_not[24];
	state[25] ^= key_0_not[25];
	state[26] ^= key_0_not[26];
	state[27] ^= key_0_not[27];
	state[28] ^= key_0_not[28];
	state[29] ^= key_0_not[29];
	state[30] ^= key_0_not[30];
	state[31] ^= key_0_not[31];
	state[32] ^= key_0_not[32];
	state[33] ^= key_0_not[33];
	state[34] ^= key_0_not[34];
	state[35] ^= key_0_not[35];
	state[36] ^= key_0_not[36];
	state[37] ^= key_0_not[37];
	state[38] ^= key_0_not[38];
	state[39] ^= key_0_not[39];
	state[40] ^= key_0_not[40];
	state[41] ^= key_0_not[41];
	state[42] ^= key_0_not[42];
	state[43] ^= key_0_not[43];
	state[44] ^= key_0_not[44];
	state[45] ^= key_0_not[45];
	state[46] ^= key_0_not[46];
	state[47] ^= key_0_not[47];
	state[48] ^= key_0_not[48];
	state[49] ^= key_0_not[49];
	state[50] ^= key_0_not[50];
	state[51] ^= key_0_not[51];
	state[52] ^= key_0_not[52];
	state[53] ^= key_0_not[53];
	state[54] ^= key_0_not[54];
	state[55] ^= key_0_not[55];
	state[56] ^= key_0_not[56];
	state[57] ^= key_0_not[57];
	state[58] ^= key_0_not[58];
	state[59] ^= key_0_not[59];
	state[60] ^= key_0_not[60];
	state[61] ^= key_0_not[61];
	state[62] ^= key_0_not[62];
	state[63] ^= key_0_not[63];
	return state;
}

void first_rounds(uint32_t state[64], uint32_t RC[12][64], uint32_t key_1[64])	{
	for(int r = 1; r < 6; r++)	{
		sBox(state,0);
		mprime(state);
		shift_rows(state,0);
		state[0] ^= (key_1[0] ^ RC[r][0]);
		state[1] ^= (key_1[1] ^ RC[r][1]);
		state[2] ^= (key_1[2] ^ RC[r][2]);
		state[3] ^= (key_1[3] ^ RC[r][3]);
		state[4] ^= (key_1[4] ^ RC[r][4]);
		state[5] ^= (key_1[5] ^ RC[r][5]);
		state[6] ^= (key_1[6] ^ RC[r][6]);
		state[7] ^= (key_1[7] ^ RC[r][7]);
		state[8] ^= (key_1[8] ^ RC[r][8]);
		state[9] ^= (key_1[9] ^ RC[r][9]);
		state[10] ^= (key_1[10] ^ RC[r][10]);
		state[11] ^= (key_1[11] ^ RC[r][11]);
		state[12] ^= (key_1[12] ^ RC[r][12]);
		state[13] ^= (key_1[13] ^ RC[r][13]);
		state[14] ^= (key_1[14] ^ RC[r][14]);
		state[15] ^= (key_1[15] ^ RC[r][15]);
		state[16] ^= (key_1[16] ^ RC[r][16]);
		state[17] ^= (key_1[17] ^ RC[r][17]);
		state[18] ^= (key_1[18] ^ RC[r][18]);
		state[19] ^= (key_1[19] ^ RC[r][19]);
		state[20] ^= (key_1[20] ^ RC[r][20]);
		state[21] ^= (key_1[21] ^ RC[r][21]);
		state[22] ^= (key_1[22] ^ RC[r][22]);
		state[23] ^= (key_1[23] ^ RC[r][23]);
		state[24] ^= (key_1[24] ^ RC[r][24]);
		state[25] ^= (key_1[25] ^ RC[r][25]);
		state[26] ^= (key_1[26] ^ RC[r][26]);
		state[27] ^= (key_1[27] ^ RC[r][27]);
		state[28] ^= (key_1[28] ^ RC[r][28]);
		state[29] ^= (key_1[29] ^ RC[r][29]);
		state[30] ^= (key_1[30] ^ RC[r][30]);
		state[31] ^= (key_1[31] ^ RC[r][31]);
		state[32] ^= (key_1[32] ^ RC[r][32]);
		state[33] ^= (key_1[33] ^ RC[r][33]);
		state[34] ^= (key_1[34] ^ RC[r][34]);
		state[35] ^= (key_1[35] ^ RC[r][35]);
		state[36] ^= (key_1[36] ^ RC[r][36]);
		state[37] ^= (key_1[37] ^ RC[r][37]);
		state[38] ^= (key_1[38] ^ RC[r][38]);
		state[39] ^= (key_1[39] ^ RC[r][39]);
		state[40] ^= (key_1[40] ^ RC[r][40]);
		state[41] ^= (key_1[41] ^ RC[r][41]);
		state[42] ^= (key_1[42] ^ RC[r][42]);
		state[43] ^= (key_1[43] ^ RC[r][43]);
		state[44] ^= (key_1[44] ^ RC[r][44]);
		state[45] ^= (key_1[45] ^ RC[r][45]);
		state[46] ^= (key_1[46] ^ RC[r][46]);
		state[47] ^= (key_1[47] ^ RC[r][47]);
		state[48] ^= (key_1[48] ^ RC[r][48]);
		state[49] ^= (key_1[49] ^ RC[r][49]);
		state[50] ^= (key_1[50] ^ RC[r][50]);
		state[51] ^= (key_1[51] ^ RC[r][51]);
		state[52] ^= (key_1[52] ^ RC[r][52]);
		state[53] ^= (key_1[53] ^ RC[r][53]);
		state[54] ^= (key_1[54] ^ RC[r][54]);
		state[55] ^= (key_1[55] ^ RC[r][55]);
		state[56] ^= (key_1[56] ^ RC[r][56]);
		state[57] ^= (key_1[57] ^ RC[r][57]);
		state[58] ^= (key_1[58] ^ RC[r][58]);
		state[59] ^= (key_1[59] ^ RC[r][59]);
		state[60] ^= (key_1[60] ^ RC[r][60]);
		state[61] ^= (key_1[61] ^ RC[r][61]);
		state[62] ^= (key_1[62] ^ RC[r][62]);
		state[63] ^= (key_1[63] ^ RC[r][63]);
	}
}

void last_rounds(uint32_t state[64], uint32_t RC[12][64], uint32_t key_1[64])	{
	for(int r = 6; r < 11; r++)	{
		state[0] ^= (key_1[0] ^ RC[r][0]);
		state[1] ^= (key_1[1] ^ RC[r][1]);
		state[2] ^= (key_1[2] ^ RC[r][2]);
		state[3] ^= (key_1[3] ^ RC[r][3]);
		state[4] ^= (key_1[4] ^ RC[r][4]);
		state[5] ^= (key_1[5] ^ RC[r][5]);
		state[6] ^= (key_1[6] ^ RC[r][6]);
		state[7] ^= (key_1[7] ^ RC[r][7]);
		state[8] ^= (key_1[8] ^ RC[r][8]);
		state[9] ^= (key_1[9] ^ RC[r][9]);
		state[10] ^= (key_1[10] ^ RC[r][10]);
		state[11] ^= (key_1[11] ^ RC[r][11]);
		state[12] ^= (key_1[12] ^ RC[r][12]);
		state[13] ^= (key_1[13] ^ RC[r][13]);
		state[14] ^= (key_1[14] ^ RC[r][14]);
		state[15] ^= (key_1[15] ^ RC[r][15]);
		state[16] ^= (key_1[16] ^ RC[r][16]);
		state[17] ^= (key_1[17] ^ RC[r][17]);
		state[18] ^= (key_1[18] ^ RC[r][18]);
		state[19] ^= (key_1[19] ^ RC[r][19]);
		state[20] ^= (key_1[20] ^ RC[r][20]);
		state[21] ^= (key_1[21] ^ RC[r][21]);
		state[22] ^= (key_1[22] ^ RC[r][22]);
		state[23] ^= (key_1[23] ^ RC[r][23]);
		state[24] ^= (key_1[24] ^ RC[r][24]);
		state[25] ^= (key_1[25] ^ RC[r][25]);
		state[26] ^= (key_1[26] ^ RC[r][26]);
		state[27] ^= (key_1[27] ^ RC[r][27]);
		state[28] ^= (key_1[28] ^ RC[r][28]);
		state[29] ^= (key_1[29] ^ RC[r][29]);
		state[30] ^= (key_1[30] ^ RC[r][30]);
		state[31] ^= (key_1[31] ^ RC[r][31]);
		state[32] ^= (key_1[32] ^ RC[r][32]);
		state[33] ^= (key_1[33] ^ RC[r][33]);
		state[34] ^= (key_1[34] ^ RC[r][34]);
		state[35] ^= (key_1[35] ^ RC[r][35]);
		state[36] ^= (key_1[36] ^ RC[r][36]);
		state[37] ^= (key_1[37] ^ RC[r][37]);
		state[38] ^= (key_1[38] ^ RC[r][38]);
		state[39] ^= (key_1[39] ^ RC[r][39]);
		state[40] ^= (key_1[40] ^ RC[r][40]);
		state[41] ^= (key_1[41] ^ RC[r][41]);
		state[42] ^= (key_1[42] ^ RC[r][42]);
		state[43] ^= (key_1[43] ^ RC[r][43]);
		state[44] ^= (key_1[44] ^ RC[r][44]);
		state[45] ^= (key_1[45] ^ RC[r][45]);
		state[46] ^= (key_1[46] ^ RC[r][46]);
		state[47] ^= (key_1[47] ^ RC[r][47]);
		state[48] ^= (key_1[48] ^ RC[r][48]);
		state[49] ^= (key_1[49] ^ RC[r][49]);
		state[50] ^= (key_1[50] ^ RC[r][50]);
		state[51] ^= (key_1[51] ^ RC[r][51]);
		state[52] ^= (key_1[52] ^ RC[r][52]);
		state[53] ^= (key_1[53] ^ RC[r][53]);
		state[54] ^= (key_1[54] ^ RC[r][54]);
		state[55] ^= (key_1[55] ^ RC[r][55]);
		state[56] ^= (key_1[56] ^ RC[r][56]);
		state[57] ^= (key_1[57] ^ RC[r][57]);
		state[58] ^= (key_1[58] ^ RC[r][58]);
		state[59] ^= (key_1[59] ^ RC[r][59]);
		state[60] ^= (key_1[60] ^ RC[r][60]);
		state[61] ^= (key_1[61] ^ RC[r][61]);
		state[62] ^= (key_1[62] ^ RC[r][62]);
		state[63] ^= (key_1[63] ^ RC[r][63]);
		shift_rows(state,1);
		mprime(state);
		sBox(state,1);
	}
}


void m0(uint32_t ret[16], uint32_t data[16])	{
    ret[ 0] = data[4] ^ data[ 8] ^ data[12];
    ret[ 1] = data[1] ^ data[ 9] ^ data[13];
    ret[ 2] = data[2] ^ data[ 6] ^ data[14];
    ret[ 3] = data[3] ^ data[ 7] ^ data[11];
    ret[ 4] = data[0] ^ data[ 4] ^ data[ 8];
    ret[ 5] = data[5] ^ data[ 9] ^ data[13];
    ret[ 6] = data[2] ^ data[10] ^ data[14];
    ret[ 7] = data[3] ^ data[ 7] ^ data[15];
    ret[ 8] = data[0] ^ data[ 4] ^ data[12];
    ret[ 9] = data[1] ^ data[ 5] ^ data[ 9];
    ret[10] = data[6] ^ data[10] ^ data[14];
    ret[11] = data[3] ^ data[11] ^ data[15];
    ret[12] = data[0] ^ data[ 8] ^ data[12];
    ret[13] = data[1] ^ data[ 5] ^ data[13];
    ret[14] = data[2] ^ data[ 6] ^ data[10];
    ret[15] = data[7] ^ data[11] ^ data[15];
}

void m1(uint32_t ret[16], uint32_t data[16])	{
    ret[ 0] = data[0] ^ data[ 4] ^ data[ 8];
    ret[ 1] = data[5] ^ data[ 9] ^ data[13];
    ret[ 2] = data[2] ^ data[10] ^ data[14];
    ret[ 3] = data[3] ^ data[ 7] ^ data[15];
    ret[ 4] = data[0] ^ data[ 4] ^ data[12];
    ret[ 5] = data[1] ^ data[ 5] ^ data[ 9];
    ret[ 6] = data[6] ^ data[10] ^ data[14];
    ret[ 7] = data[3] ^ data[11] ^ data[15];
    ret[ 8] = data[0] ^ data[ 8] ^ data[12];
    ret[ 9] = data[1] ^ data[ 5] ^ data[13];
    ret[10] = data[2] ^ data[ 6] ^ data[10];
    ret[11] = data[7] ^ data[11] ^ data[15];
    ret[12] = data[4] ^ data[ 8] ^ data[12];
    ret[13] = data[1] ^ data[ 9] ^ data[13];
    ret[14] = data[2] ^ data[ 6] ^ data[14];
    ret[15] = data[3] ^ data[ 7] ^ data[11];
}

void mprime(uint32_t state[64])	{
	uint32_t output[16];
	uint32_t extracted[16];
	extracted[0] = state[0];
	extracted[1] = state[1];
	extracted[2] = state[2];
	extracted[3] = state[3];
	extracted[4] = state[4];
	extracted[5] = state[5];
	extracted[6] = state[6];
	extracted[7] = state[7];
	extracted[8] = state[8];
	extracted[9] = state[9];
	extracted[10] = state[10];
	extracted[11] = state[11];
	extracted[12] = state[12];
	extracted[13] = state[13];
	extracted[14] = state[14];
	extracted[15] = state[15];
	m0(output,extracted);
	state[0] = output[0];
	state[1] = output[1];
	state[2] = output[2];
	state[3] = output[3];
	state[4] = output[4];
	state[5] = output[5];
	state[6] = output[6];
	state[7] = output[7];
	state[8] = output[8];
	state[9] = output[9];
	state[10] = output[10];
	state[11] = output[11];
	state[12] = output[12];
	state[13] = output[13];
	state[14] = output[14];
	state[15] = output[15];
	extracted[0] = state[16];
	extracted[1] = state[17];
	extracted[2] = state[18];
	extracted[3] = state[19];
	extracted[4] = state[20];
	extracted[5] = state[21];
	extracted[6] = state[22];
	extracted[7] = state[23];
	extracted[8] = state[24];
	extracted[9] = state[25];
	extracted[10] = state[26];
	extracted[11] = state[27];
	extracted[12] = state[28];
	extracted[13] = state[29];
	extracted[14] = state[30];
	extracted[15] = state[31];
	m1(output,extracted);
	state[16] = output[0];
	state[17] = output[1];
	state[18] = output[2];
	state[19] = output[3];
	state[20] = output[4];
	state[21] = output[5];
	state[22] = output[6];
	state[23] = output[7];
	state[24] = output[8];
	state[25] = output[9];
	state[26] = output[10];
	state[27] = output[11];
	state[28] = output[12];
	state[29] = output[13];
	state[30] = output[14];
	state[31] = output[15];
	extracted[0] = state[32];
	extracted[1] = state[33];
	extracted[2] = state[34];
	extracted[3] = state[35];
	extracted[4] = state[36];
	extracted[5] = state[37];
	extracted[6] = state[38];
	extracted[7] = state[39];
	extracted[8] = state[40];
	extracted[9] = state[41];
	extracted[10] = state[42];
	extracted[11] = state[43];
	extracted[12] = state[44];
	extracted[13] = state[45];
	extracted[14] = state[46];
	extracted[15] = state[47];
	m1(output,extracted);
	state[32] = output[0];
	state[33] = output[1];
	state[34] = output[2];
	state[35] = output[3];
	state[36] = output[4];
	state[37] = output[5];
	state[38] = output[6];
	state[39] = output[7];
	state[40] = output[8];
	state[41] = output[9];
	state[42] = output[10];
	state[43] = output[11];
	state[44] = output[12];
	state[45] = output[13];
	state[46] = output[14];
	state[47] = output[15];
	extracted[0] = state[48];
	extracted[1] = state[49];
	extracted[2] = state[50];
	extracted[3] = state[51];
	extracted[4] = state[52];
	extracted[5] = state[53];
	extracted[6] = state[54];
	extracted[7] = state[55];
	extracted[8] = state[56];
	extracted[9] = state[57];
	extracted[10] = state[58];
	extracted[11] = state[59];
	extracted[12] = state[60];
	extracted[13] = state[61];
	extracted[14] = state[62];
	extracted[15] = state[63];
	m0(output, extracted);
	state[48] = output[0];
	state[49] = output[1];
	state[50] = output[2];
	state[51] = output[3];
	state[52] = output[4];
	state[53] = output[5];
	state[54] = output[6];
	state[55] = output[7];
	state[56] = output[8];
	state[57] = output[9];
	state[58] = output[10];
	state[59] = output[11];
	state[60] = output[12];
	state[61] = output[13];
	state[62] = output[14];
	state[63] = output[15];	
}

void sBox(uint32_t input[64], int invert)	{
	uint32_t current[4];
	int nibble;
	for(nibble = 0; nibble < 16; nibble++)	{
		current[0] = input[nibble * 4];
		current[1] = input[(nibble * 4) + 1];
		current[2] = input[(nibble * 4) + 2];
		current[3] = input[(nibble * 4) + 3];
		sBox_nibble(current,invert);
		input[nibble * 4] = current[0];
		input[(nibble * 4) + 1] = current[1];
		input[(nibble * 4) + 2] = current[2];
		input[(nibble * 4) + 3] = current[3];
	}
}

void sBox_nibble(uint32_t current[4],int invert)	{
	 	uint32_t output[4];
		if(!invert)	{
			output[0] = sbox_1(current);
			output[1] = sbox_2(current);
			output[2] = sbox_3(current);
			output[3] = sbox_4(current);
		} else	{
			output[0] = inv_sbox_1(current);
			output[1] = inv_sbox_2(current);
			output[2] = inv_sbox_3(current);
			output[3] = inv_sbox_4(current);		
		}
		current[0] = output[0];
		current[1] = output[1];
		current[2] = output[2];
		current[3] = output[3];
}

void shift_rows(uint32_t input[64], int inverse)	{
	uint32_t output[64];
	int target = 0, nibble;
	for(nibble = 0; nibble < 16;  nibble++)	{
		output[(target * 4)] = input[(nibble * 4)];
		output[(target * 4) + 1] = input[(nibble * 4) + 1];
		output[(target * 4) + 2] = input[(nibble * 4) + 2];
		output[(target * 4) + 3] = input[(nibble * 4) + 3];
		if(inverse)	{
			target = (target + 5) % 16;
		} else	{
			target = (target + 13) % 16;
		}
	}
	input[0] = output[0];
	input[1] = output[1];
	input[2] = output[2];
	input[3] = output[3];
	input[4] = output[4];
	input[5] = output[5];
	input[6] = output[6];
	input[7] = output[7];
	input[8] = output[8];
	input[9] = output[9];
	input[10] = output[10];
	input[11] = output[11];
	input[12] = output[12];
	input[13] = output[13];
	input[14] = output[14];
	input[15] = output[15];
	input[16] = output[16];
	input[17] = output[17];
	input[18] = output[18];
	input[19] = output[19];
	input[20] = output[20];
	input[21] = output[21];
	input[22] = output[22];
	input[23] = output[23];
	input[24] = output[24];
	input[25] = output[25];
	input[26] = output[26];
	input[27] = output[27];
	input[28] = output[28];
	input[29] = output[29];
	input[30] = output[30];
	input[31] = output[31];
	input[32] = output[32];
	input[33] = output[33];
	input[34] = output[34];
	input[35] = output[35];
	input[36] = output[36];
	input[37] = output[37];
	input[38] = output[38];
	input[39] = output[39];
	input[40] = output[40];
	input[41] = output[41];
	input[42] = output[42];
	input[43] = output[43];
	input[44] = output[44];
	input[45] = output[45];
	input[46] = output[46];
	input[47] = output[47];
	input[48] = output[48];
	input[49] = output[49];
	input[50] = output[50];
	input[51] = output[51];
	input[52] = output[52];
	input[53] = output[53];
	input[54] = output[54];
	input[55] = output[55];
	input[56] = output[56];
	input[57] = output[57];
	input[58] = output[58];
	input[59] = output[59];
	input[60] = output[60];
	input[61] = output[61];
	input[62] = output[62];
	input[63] = output[63];
}

uint32_t inv_sbox_1(uint32_t input[4])	{
	 return ((~input[A] & input[B]) | (~input[B] & ~input[C] & ~input[D]) | (input[B] & ~input[C] & input[D]) | (input[B] & input[C] & ~input[D]));
}

uint32_t inv_sbox_2(uint32_t input[4])	{
	return ((~input[C] & input[D]) | (input[B] & ~input[C]) | (input[A] & input[C] & ~input[D]));
}

uint32_t inv_sbox_3(uint32_t input[4])	{
	 return ((~input[A] & ~input[B]) | (~input[B] & ~input[C]) | (~input[A] & ~input[C] & ~input[D]) | (input[A] & ~input[C] & input[D]));
}

uint32_t inv_sbox_4(uint32_t input[4])	{
	return ((~input[A] & ~input[C]) | (input[B] & input[C] & input[D]) | (input[B] & ~input[C] & ~input[D]) | (~input[A] & ~input[B] & ~input[D]));
}

uint32_t sbox_1(uint32_t input[4])	{
	return ((~input[A] & ~input[C]) | (input[B] & ~input[D]) | (input[A] & input[C] & ~input[D]));
}

uint32_t sbox_2(uint32_t input[4])	{
	return ((input[A] & input[B]) | (~input[C] & input[D]) | (input[A] & ~input[C]));
}

uint32_t sbox_3(uint32_t input[4])	{
	return ((~input[A] & ~input[B]) | (~input[C] & ~input[D]) | (~input[B] & ~input[C]));
}

uint32_t sbox_4(uint32_t input[4])	{
	return ((input[A] & ~input[C] & input[D]) | (~input[A] & ~input[B] & ~input[C]) | (input[B] & input[C] & ~input[D]) | (~input[A] & input[B] & input[C]) | (~input[A] & ~input[B] & ~input[D]));
}
