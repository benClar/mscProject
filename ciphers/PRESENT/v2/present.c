/*---------- Standard Headers -----------*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
/*---------- Custom Headers	-----------*/

#include "debug.h"
#include "present.h"

/*---------- Symbolic Constants  -----------*/

#define KEY_SIZE	80
#define ROUND_KEY_SIZE 64
#define LEFT_SHIFT 61
#define STATE_SIZE 64
#define A 	0	
#define B 	1
#define C 	2
#define D 	3
/*---------- Main -----------*/

char *int2bin(uint64_t a, char *buffer, int buf_size) {
    buffer += (buf_size - 1);

    for (int i = 63; i >= 0; i--) {
        *buffer-- = (a & 1) + '0';

        a >>= 1;
    }

    return buffer;
}

uint8_t *reverse(uint8_t *array, int start, int end)	{

		while(start < end)	{
			int tmp = array[start];
			array[start] = array[end];
			array[end] = tmp;
			start++;
			end--;
		}	
		return array;
}

uint8_t *rotateKey(uint8_t *key)    {
    int shift = LEFT_SHIFT % KEY_SIZE;
    reverse(key, 0, KEY_SIZE - 1);
    reverse(key, 0, KEY_SIZE - shift - 1);
    reverse(key, KEY_SIZE - shift, KEY_SIZE - 1);
    return key;
}

uint8_t *keyXOR(uint8_t *key, int round)	{
	key[19] ^= (round >>4 & 1);
	key[18] ^= (round >>3 & 1);
	key[17] ^= (round >>2 & 1);
	key[16] ^= (round >>1 & 1);
	key[15] ^= (round & 1);

	return key;
}

int generateRoundKey(uint8_t *key, uint8_t **subKey, int round) {
    int keyBit;

    for( keyBit = 0; keyBit < 64  ; keyBit++)   {
        subKey[ round ][ keyBit ] = key[ keyBit ];
    }
    rotateKey(key);
	keyXOR(key,round);
    return 1;
}

uint8_t *sBox(uint8_t *input)	{
	return input;
}

uint8_t sbox_1(uint8_t *input)	{
	return (((~input[A] & ~input[C] & ~input[D] ) | (~input[A] & input[C] & input[D] ) | (input[A] & ~input[B] & input[D]) | (input[A] & ~input[B] & input[C]) | (~input[A] & input[B] & input[C])) & 1);
}

uint8_t sbox_2(uint8_t *input)	{
	return (((~input[B] & input[C] & ~input[D]) | (input[A] & input[B] & ~input[C]) | (~input[B] & ~input[C] & input[D]) | (~input[A] & ~input[B] & ~input[C]) | (~input[A] & input[B] & input[C] & input[D])) & 1);
}

uint8_t sbox_3(uint8_t *input)  {
	return (((input[A] & input[B] & input[D]) | (input[A] & ~input[B] & ~input[C]) | (~input[A] & input[C] & ~input[D]) | (~input[A] & ~input[B] & input[C]) | (input[A] & ~input[B] & ~input[D])) & 1);
}

uint8_t sbox_4(uint8_t *input)  {
	return (((~input[A] & input[C] & input[D] ) | ( input[A] & input[C] & ~input[D] ) | (input[A] & ~input[B] & ~input[D] ) | (~input[A] & ~input[B] & input[D]) | ( ~input[A] & input[B] & ~input[C] & ~input[D]) | (input[A] & input[B] & ~input[C] & input[D])) & 1);
}


void pLayer(uint8_t *state)	{
	int bit;
	uint8_t *temp = (uint8_t*) malloc(STATE_SIZE * sizeof(uint8_t));
	memcpy(temp, state, STATE_SIZE);
	for(bit = 0; bit < STATE_SIZE; bit++ )	{
		int position = (16*bit) % (STATE_SIZE - 1);
		if(bit == 63)	{
			position = 63;
		}	
		printf("%d -> %d \n",bit,position);
		state[ position ] = temp[ bit ];
	}
	free(temp);
}

int main(){
	/*
	uint32_t key[ KEY_SIZE ] = { KEY_SEED79, KEY_SEED78, KEY_SEED77,
								KEY_SEED76, KEY_SEED75, KEY_SEED74,
								KEY_SEED73, KEY_SEED72, KEY_SEED71,
								KEY_SEED70, KEY_SEED69, KEY_SEED68,
								KEY_SEED67, KEY_SEED66, KEY_SEED65,
								KEY_SEED64, KEY_SEED63, KEY_SEED62,
								KEY_SEED61, KEY_SEED60, KEY_SEED59,
								KEY_SEED58, KEY_SEED57, KEY_SEED56,
								KEY_SEED55, KEY_SEED54, KEY_SEED53,
								KEY_SEED52, KEY_SEED51, KEY_SEED50,
								KEY_SEED49, KEY_SEED48, KEY_SEED47,
								KEY_SEED46, KEY_SEED45, KEY_SEED44,
								KEY_SEED43, KEY_SEED42, KEY_SEED41,
								KEY_SEED40, KEY_SEED39, KEY_SEED38,
								KEY_SEED37, KEY_SEED36, KEY_SEED35,
								KEY_SEED34, KEY_SEED33, KEY_SEED32,
								KEY_SEED31, KEY_SEED30, KEY_SEED29,
								KEY_SEED28, KEY_SEED27, KEY_SEED26,
								KEY_SEED25, KEY_SEED24, KEY_SEED23,
								KEY_SEED22, KEY_SEED21, KEY_SEED20,
								KEY_SEED19, KEY_SEED18, KEY_SEED17,
								KEY_SEED16, KEY_SEED15, KEY_SEED14,
								KEY_SEED13, KEY_SEED12, KEY_SEED11,
								KEY_SEED10, KEY_SEED9, KEY_SEED8,
								KEY_SEED7, KEY_SEED6, KEY_SEED5,
								KEY_SEED4, KEY_SEED3, KEY_SEED2,
								KEY_SEED1, KEY_SEED0 };
								
	uint8_t state[ STATE_SIZE ] = { STATE_SEED63, STATE_SEED62, STATE_SEED61,
									STATE_SEED60, STATE_SEED59, STATE_SEED58,
									STATE_SEED57, STATE_SEED56, STATE_SEED55,
									STATE_SEED54, STATE_SEED53, STATE_SEED52,
									STATE_SEED51, STATE_SEED50, STATE_SEED49,
									STATE_SEED48, STATE_SEED47, STATE_SEED46,
									STATE_SEED45, STATE_SEED44, STATE_SEED43,
									STATE_SEED42, STATE_SEED41, STATE_SEED40,
									STATE_SEED39, STATE_SEED38, STATE_SEED37,
									STATE_SEED36, STATE_SEED35, STATE_SEED34,
									STATE_SEED33, STATE_SEED32, STATE_SEED31,
									STATE_SEED30, STATE_SEED29, STATE_SEED28,
									STATE_SEED27, STATE_SEED26, STATE_SEED25,
									STATE_SEED24, STATE_SEED23, STATE_SEED22,
									STATE_SEED21, STATE_SEED20, STATE_SEED19,
									STATE_SEED18, STATE_SEED17, STATE_SEED16,
									STATE_SEED15, STATE_SEED14, STATE_SEED13,
									STATE_SEED12, STATE_SEED11, STATE_SEED10,
									STATE_SEED9, STATE_SEED8, STATE_SEED7,
									STATE_SEED6, STATE_SEED5, STATE_SEED4,
									STATE_SEED3, STATE_SEED2, STATE_SEED1,
									STATE_SEED0 };*/
	//pLayer(state);
	uint8_t test_0[4] = {0x0,0x0,0x0,0x0};
	uint8_t test_1[4] = {0x0,0x0,0x0,0x1};
	uint8_t test_2[4] = {0x0,0x0,0x1,0x0};
	uint8_t test_3[4] = {0x0,0x0,0x1,0x1};
	uint8_t test_4[4] = {0x0,0x1,0x0,0x0};
	uint8_t test_5[4] = {0x0,0x1,0x0,0x1};
	uint8_t test_6[4] = {0x0,0x1,0x1,0x0};
	uint8_t test_7[4] = {0x0,0x1,0x1,0x1};
	uint8_t test_8[4] = {0x1,0x0,0x0,0x0};
	uint8_t test_9[4] = {0x1,0x0,0x0,0x1};
	uint8_t test_10[4] = {0x1,0x0,0x1,0x0};
	uint8_t test_11[4] = {0x1,0x0,0x1,0x1};
	uint8_t test_12[4] = {0x1,0x1,0x0,0x0};
	uint8_t test_13[4] = {0x1,0x1,0x0,0x1};
	uint8_t test_14[4] = {0x1,0x1,0x1,0x0};
	uint8_t test_15[4] = {0x1,0x1,0x1,0x1};

	iprint(sbox_1(test_0));
	iprint(sbox_1(test_1));
	iprint(sbox_1(test_2));
	iprint(sbox_1(test_3));
	iprint(sbox_1(test_4));
	iprint(sbox_1(test_5));
	iprint(sbox_1(test_6));
	iprint(sbox_1(test_7));
	iprint(sbox_1(test_8));
	iprint(sbox_1(test_9));
	iprint(sbox_1(test_10));
	iprint(sbox_1(test_11));
	iprint(sbox_1(test_12));
	iprint(sbox_1(test_13));
	iprint(sbox_1(test_14));
	iprint(sbox_1(test_15));

	iprint(sbox_2(test_0));
	iprint(sbox_2(test_1));
	iprint(sbox_2(test_2));
	iprint(sbox_2(test_3));
	iprint(sbox_2(test_4));
	iprint(sbox_2(test_5));
	iprint(sbox_2(test_6));
	iprint(sbox_2(test_7));
	iprint(sbox_2(test_8));
	iprint(sbox_2(test_9));
	iprint(sbox_2(test_10));
	iprint(sbox_2(test_11));
	iprint(sbox_2(test_12));
	iprint(sbox_2(test_13));
	iprint(sbox_2(test_14));
	iprint(sbox_2(test_15));

	iprint(sbox_3(test_0));
	iprint(sbox_3(test_1));
	iprint(sbox_3(test_2));
	iprint(sbox_3(test_3));
	iprint(sbox_3(test_4));
	iprint(sbox_3(test_5));
	iprint(sbox_3(test_6));
	iprint(sbox_3(test_7));
	iprint(sbox_3(test_8));
	iprint(sbox_3(test_9));
	iprint(sbox_3(test_10));
	iprint(sbox_3(test_11));
	iprint(sbox_3(test_12));
	iprint(sbox_3(test_13));
	iprint(sbox_3(test_14));
	iprint(sbox_3(test_15));

	iprint(sbox_4(test_0));
	iprint(sbox_4(test_1));
	iprint(sbox_4(test_2));
	iprint(sbox_4(test_3));
	iprint(sbox_4(test_4));
	iprint(sbox_4(test_5));
	iprint(sbox_4(test_6));
	iprint(sbox_4(test_7));
	iprint(sbox_4(test_8));
	iprint(sbox_4(test_9));
	iprint(sbox_4(test_10));
	iprint(sbox_4(test_11));
	iprint(sbox_4(test_12));
	iprint(sbox_4(test_13));
	iprint(sbox_4(test_14));
	iprint(sbox_4(test_15));
}



    /*uint8_t key[ KEY_SIZE ] = { KEY_SEED0, KEY_SEED1, KEY_SEED2,
                                KEY_SEED3, KEY_SEED4, KEY_SEED5,
                                KEY_SEED6, KEY_SEED7, KEY_SEED8,
                                KEY_SEED9, KEY_SEED10, KEY_SEED11,
                                KEY_SEED12, KEY_SEED13, KEY_SEED14,
                                KEY_SEED15, KEY_SEED16, KEY_SEED17,
                                KEY_SEED18, KEY_SEED19, KEY_SEED20,
                                KEY_SEED21, KEY_SEED22, KEY_SEED23,
                                KEY_SEED24, KEY_SEED25, KEY_SEED26,
                                KEY_SEED27, KEY_SEED28, KEY_SEED29,
                                KEY_SEED30, KEY_SEED31, KEY_SEED32,
                                KEY_SEED33, KEY_SEED34, KEY_SEED35,
                                KEY_SEED36, KEY_SEED37, KEY_SEED38,
                                KEY_SEED39, KEY_SEED40, KEY_SEED41,
                                KEY_SEED42, KEY_SEED43, KEY_SEED44,
                                KEY_SEED45, KEY_SEED46, KEY_SEED47,
                                KEY_SEED48, KEY_SEED49, KEY_SEED50,
                                KEY_SEED51, KEY_SEED52, KEY_SEED53,
                                KEY_SEED54, KEY_SEED55, KEY_SEED56,
                                KEY_SEED57, KEY_SEED58, KEY_SEED59,
                                KEY_SEED60, KEY_SEED61, KEY_SEED62,
                                KEY_SEED63, KEY_SEED64, KEY_SEED65,
                                KEY_SEED66, KEY_SEED67, KEY_SEED68,
                                KEY_SEED69, KEY_SEED70, KEY_SEED71,
                                KEY_SEED72, KEY_SEED73, KEY_SEED74,
                                KEY_SEED75, KEY_SEED76, KEY_SEED77,
                                KEY_SEED78, KEY_SEED79 };*/
