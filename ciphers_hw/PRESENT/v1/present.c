/*---------- Standard Headers -----------*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include "debug.h"
/*---------- Custom Headers	-----------*/

/*---------- Symbolic Constants  -----------*/

#define LEFTSHIFT	61	//!size of left shift for key
#define KEYSIZE		80	//! Size of the key
#define LSB_BITS	64	//!Number of bits of the key held in the LSB key variable
#define	MSB_BITS	KEYSIZE - LSB_BITS	//!Number of bits of the key held in the MSB key variable	
#define BUF_SIZE	65 
#define ROUNDS		32

/*---------- Main -----------*/

char *int2bin(uint64_t a, char *buffer, int buf_size) {
    buffer += (buf_size - 1);

    for (int i = 63; i >= 0; i--) {
        *buffer-- = (a & 1) + '0';

        a >>= 1;
    }

    return buffer;
}

int main(){

    char buffer[BUF_SIZE];
    buffer[BUF_SIZE - 1] = '\0';
	uint64_t roundKeys[ROUNDS];
	uint64_t keyMSB = 0x0;
	//keyLSB |= 0xFFFFFFFFFFFFFFFF;
	uint64_t keyLSB = 0x0;
	//keyMSB |= 0x00000000000000000000FFFF; //Setting key
	uint64_t counter = 0;  //!Round counter
	int sBoxCount;
	uint64_t roundKey = 0x0;
	uint64_t state = 0x0;
	uint64_t extract = 0xF; //! and with state to get 4 LSB 
	//state |= 0x10E9AA5F; //! Setting initial plaintext
	int8_t sBox[16] = {12,5,6,11,9,0,10,13,3,14,15,8,4,7,1,2};
	uint64_t temp;
	uint64_t newState = 0x0;
	int i;
	//!Generate Round Keys : Key Schedule
	for(i = 0; i < ROUNDS; i++)	{
		//! Left Rotation by 61
		temp = keyLSB;
		keyLSB <<=  LEFTSHIFT;  //<<61
		keyLSB |= keyMSB <<= (LEFTSHIFT - (MSB_BITS)); // <<45
		keyLSB |= temp >> (LSB_BITS - ( LEFTSHIFT - (MSB_BITS))); //! >> 19 
		keyMSB = (temp >> (LSB_BITS - LEFTSHIFT)) & 0xFFFF;	//! >> 3

		//! putting 4 MSB through Sbox lookup
		temp = keyMSB >> ((MSB_BITS) - 4);
		temp = sBox[temp] << ((MSB_BITS) - 4);
		keyMSB &= 0x0FFF;
		keyMSB |= temp;

		//! XORing counter with bits 19-15 of key
		keyLSB ^= ((i + 1) << (19 - 4));
		roundKeys[i] = keyLSB;
	}
	for(counter = 0; counter < ROUNDS - 1; counter++)	{
		//!addRoundKey
		//roundKey ^= state;
		state ^= roundKeys[counter];
	
		//!sBoxLayer for current block
		for(sBoxCount = 0; sBoxCount < 16; sBoxCount++)	{
        	//int2bin(state, buffer, BUF_SIZE - 1);
		    //printf("state: \n  %s \n", buffer);
        	//int2bin(state & extract, buffer, BUF_SIZE - 1);
		    //printf("Extracted state: \n  %s \n", buffer);
			temp = state & extract; //!temp stores 4 LSB of state
			state >>= 4;
        	//int2bin(state, buffer, BUF_SIZE - 1);
		    //printf("shifted state: \n  %s \n", buffer);
			temp = sBox[temp]; // sBox translation for chunk
			//printf("temp sbox value: %llu \n",temp);
			newState = newState << 4; //! Making room for next 4 bits
        	//int2bin(newState, buffer, BUF_SIZE - 1);
		    //printf("new state with room: \n  %s \n", buffer);
			newState |= temp; //! concatonating temp onto 4 LSB of newState
        	//int2bin(newState, buffer, BUF_SIZE - 1);
		    //printf("new state concatonated: \n  %s \n", buffer);
		}
		state = newState;
		temp = 0x0;
		newState = 0x0;

		//!pLayer for current block
		for(int k = 0; k < 64; k++)	{
			int position = (16*k) % 63;	
			if(k == 63)	{
				position = 63;
			}
			temp |= (((state >> k) & 0x1) << position);
		}
		state = temp;
	}
	state ^= roundKeys[31];
	printf("%llu\n",state);
}
