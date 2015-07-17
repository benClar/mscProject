/*---------- Standard Headers -----------*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
/*---------- Custom Headers	-----------*/

#include "prince.h"
#include "sput.h"


int main(){
	if(TESTING)	{
		run_tests();
	} else	{
		run();
	}
}

void run()	{

	uint8_t *state = init_state();

	uint8_t key_0[64] = { KEY_SEED63, KEY_SEED62, KEY_SEED61, KEY_SEED60, KEY_SEED59, KEY_SEED58, KEY_SEED57, KEY_SEED56, KEY_SEED55, KEY_SEED54, KEY_SEED53, KEY_SEED52,
				KEY_SEED51, KEY_SEED50, KEY_SEED49, KEY_SEED48, KEY_SEED47, KEY_SEED46, KEY_SEED45, KEY_SEED44, KEY_SEED43, KEY_SEED42, KEY_SEED41, KEY_SEED40,
				KEY_SEED39, KEY_SEED38, KEY_SEED37, KEY_SEED36, KEY_SEED35, KEY_SEED34, KEY_SEED33, KEY_SEED32, KEY_SEED31, KEY_SEED30, KEY_SEED29, KEY_SEED28,
				KEY_SEED27, KEY_SEED26, KEY_SEED25, KEY_SEED24, KEY_SEED23, KEY_SEED22, KEY_SEED21, KEY_SEED20, KEY_SEED19, KEY_SEED18, KEY_SEED17, KEY_SEED16,
				KEY_SEED15, KEY_SEED14, KEY_SEED13, KEY_SEED12, KEY_SEED11, KEY_SEED10, KEY_SEED9, KEY_SEED8, KEY_SEED7, KEY_SEED6, KEY_SEED5, KEY_SEED4,
				KEY_SEED3, KEY_SEED2, KEY_SEED1, KEY_SEED0 };

	uint8_t key_1[64] = {KEY_SEED127, KEY_SEED126, KEY_SEED125, KEY_SEED124, KEY_SEED123, KEY_SEED122, KEY_SEED121, KEY_SEED120, KEY_SEED119, KEY_SEED118, KEY_SEED117, KEY_SEED116,
				KEY_SEED115, KEY_SEED114, KEY_SEED113, KEY_SEED112, KEY_SEED111, KEY_SEED110, KEY_SEED109, KEY_SEED108, KEY_SEED107, KEY_SEED106, KEY_SEED105, KEY_SEED104,
				KEY_SEED103, KEY_SEED102, KEY_SEED101, KEY_SEED100, KEY_SEED99, KEY_SEED98, KEY_SEED97, KEY_SEED96, KEY_SEED95, KEY_SEED94, KEY_SEED93, KEY_SEED92,
				KEY_SEED91, KEY_SEED90, KEY_SEED89, KEY_SEED88, KEY_SEED87, KEY_SEED86, KEY_SEED85, KEY_SEED84, KEY_SEED83, KEY_SEED82, KEY_SEED81, KEY_SEED80,
				KEY_SEED79, KEY_SEED78, KEY_SEED77, KEY_SEED76, KEY_SEED75, KEY_SEED74, KEY_SEED73, KEY_SEED72, KEY_SEED71, KEY_SEED70, KEY_SEED69, KEY_SEED68,
				KEY_SEED67, KEY_SEED66, KEY_SEED65, KEY_SEED64};

	uint8_t *key_0_not = XOR(rotate_right(key_0,64,1),shift_right(key_0,64,63),64);
	uint8_t **RC = (uint8_t**) malloc(12 * sizeof(uint8_t*));

	RC[0] = bitslice(RC_0,64);
	RC[1] = bitslice(RC_1,64);
	RC[2] = bitslice(RC_2,64);
	RC[3] = bitslice(RC_3,64);
	RC[4] = bitslice(RC_4,64);
	RC[5] = bitslice(RC_5,64);
	RC[6] = bitslice(RC_6,64);
	RC[7] = bitslice(RC_7,64);
	RC[8] = bitslice(RC_8,64);
	RC[9] = bitslice(RC_9,64);
	RC[10] = bitslice(RC_10,64);
	RC[11] = bitslice(RC_11,64);

	int r;
	state = XOR(key_0,state,64);

	state = XOR(state,XOR(key_1,RC[0],64),64);

	for(r = 1; r < 6; r++)	{
		state = sBox(state,0);
		state = mprime(state);
		state = shift_rows(state,0);
		state = XOR(state,XOR(key_1,RC[r],64),64); 
	}

	state = sBox(state, 0);
	state = mprime(state);
	state = sBox(state, 1);

	for(r = 6; r < 11; r++)	{
		state = XOR(state,XOR(key_1,RC[r],64),64);
		state = shift_rows(state,1);
		state = mprime(state);
		state = sBox(state,1);
	}

	state = XOR(state,XOR(key_1,RC[11],64),64);
	state = XOR(state,key_0_not,64);
	hex_print(state,16,64);
}

uint8_t *m0(uint8_t *data)	{
	uint8_t *ret = malloc(16 * sizeof(int));
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
    return ret;
}

uint8_t *m1(uint8_t *data)	{
	uint8_t *ret = malloc(16 * sizeof(int));
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
    return ret;
}

uint8_t *mprime(uint8_t *state)	{
	uint8_t *result = malloc(64 * sizeof(uint8_t));
	memcpy(result,m0(sub_array(state,0,15)),16 * sizeof(uint8_t));
	memcpy(result + 16,m1(sub_array(state,16,31)),16 * sizeof(uint8_t));
	memcpy(result + 32,m1(sub_array(state,32,47)),16 * sizeof(uint8_t));
	memcpy(result + 48,m0(sub_array(state,48,63)),16 * sizeof(uint8_t));	
	return result;
}

uint8_t* sBox(uint8_t *input, int invert)	{
	uint8_t *output = (uint8_t*) malloc(64*sizeof(uint8_t));
	uint8_t *current = (uint8_t*) malloc(4*sizeof(uint8_t));
	int nibble;
	for(nibble = 0; nibble < 16; nibble++)	{
		memcpy(current,&(input[nibble * 4]),4*sizeof(uint8_t));
		current = sBox_nibble(current,invert);
		memcpy(&(output[nibble * 4]),current,4 * sizeof(uint8_t));
	}
	return output;
}

uint8_t* sBox_nibble(uint8_t *current,int invert)	{
	 	uint8_t *output = malloc(4 * sizeof(uint8_t));
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
		return output;	
}

uint8_t *shift_rows(uint8_t *input, int inverse)	{
	uint8_t *output = calloc(64,sizeof(uint8_t));
	int target = 0, nibble;
	for(nibble = 0; nibble < 16;  nibble++)	{
		memcpy(&(output[target * 4]),&(input[nibble * 4]),4*sizeof(uint8_t));
		if(inverse)	{
			target = (target + 5) % 16;
		} else	{
			target = (target + 13) % 16;
		}
	}

	return output;
}

uint8_t inv_sbox_1(uint8_t *input)	{
	 return (((~input[A] & input[B]) | (~input[B] & ~input[C] & ~input[D]) | (input[B] & ~input[C] & input[D]) | (input[B] & input[C] & ~input[D])) & 1);
}

uint8_t inv_sbox_2(uint8_t *input)	{
	return (((~input[C] & input[D]) | (input[B] & ~input[C]) | (input[A] & input[C] & ~input[D])) & 1);
}

uint8_t inv_sbox_3(uint8_t *input)	{
	 return (((~input[A] & ~input[B]) | (~input[B] & ~input[C]) | (~input[A] & ~input[C] & ~input[D]) | (input[A] & ~input[C] & input[D])) & 1);
}

uint8_t inv_sbox_4(uint8_t *input)	{
	return (((~input[A] & ~input[C]) | (input[B] & input[C] & input[D]) | (input[B] & ~input[C] & ~input[D]) | (~input[A] & ~input[B] & ~input[D])) & 1);
}



uint8_t sbox_1(uint8_t *input)	{
	return (((~input[A] & ~input[C]) | (input[B] & ~input[D]) | (input[A] & input[C] & ~input[D])) & 1);
}

uint8_t sbox_2(uint8_t *input)	{
	return (((input[A] & input[B]) | (~input[C] & input[D]) | (input[A] & ~input[C])) & 1);
}

uint8_t sbox_3(uint8_t *input)	{
	return (((~input[A] & ~input[B]) | (~input[C] & ~input[D]) | (~input[B] & ~input[C])) & 1);
}

uint8_t sbox_4(uint8_t *input)	{
	return (((input[A] & ~input[C] & input[D]) | (~input[A] & ~input[B] & ~input[C]) | (input[B] & input[C] & ~input[D]) | (~input[A] & input[B] & input[C]) | (~input[A] & ~input[B] & ~input[D]))  & 1);
}

uint8_t *init_state(){
	uint8_t *output = calloc(STATE_SIZE,sizeof(uint8_t));
	output[0] = STATE_SEED63;
	output[1] = STATE_SEED62;
	output[2] = STATE_SEED61;
	output[3] = STATE_SEED60;
	output[4] = STATE_SEED59;
	output[5] = STATE_SEED58;
	output[6] = STATE_SEED57;
	output[7] = STATE_SEED56;
	output[8] = STATE_SEED55;
	output[9] = STATE_SEED54;
	output[10] = STATE_SEED53;
	output[11] = STATE_SEED52;
	output[12] = STATE_SEED51;
	output[13] = STATE_SEED50;
	output[14] = STATE_SEED49;
	output[15] = STATE_SEED48;
	output[16] = STATE_SEED47;
	output[17] = STATE_SEED46;
	output[18] = STATE_SEED45;
	output[19] = STATE_SEED44;
	output[20] = STATE_SEED43;
	output[21] = STATE_SEED42;
	output[22] = STATE_SEED41;
	output[23] = STATE_SEED40;
	output[24] = STATE_SEED39;
	output[25] = STATE_SEED38;
	output[26] = STATE_SEED37;
	output[27] = STATE_SEED36;
	output[28] = STATE_SEED35;
	output[29] = STATE_SEED34;
	output[30] = STATE_SEED33;
	output[31] = STATE_SEED32;
	output[32] = STATE_SEED31;
	output[33] = STATE_SEED30;
	output[34] = STATE_SEED29;
	output[35] = STATE_SEED28;
	output[36] = STATE_SEED27;
	output[37] = STATE_SEED26;
	output[38] = STATE_SEED25;
	output[39] = STATE_SEED24;
	output[40] = STATE_SEED23;
	output[41] = STATE_SEED22;
	output[42] = STATE_SEED21;
	output[43] = STATE_SEED20;
	output[44] = STATE_SEED19;
	output[45] = STATE_SEED18;
	output[46] = STATE_SEED17;
	output[47] = STATE_SEED16;
	output[48] = STATE_SEED15;
	output[49] = STATE_SEED14;
	output[50] = STATE_SEED13;
	output[51] = STATE_SEED12;
	output[52] = STATE_SEED11;
	output[53] = STATE_SEED10;
	output[54] = STATE_SEED9;
	output[55] = STATE_SEED8;
	output[56] = STATE_SEED7;
	output[57] = STATE_SEED6;
	output[58] = STATE_SEED5;
	output[59] = STATE_SEED4;
	output[60] = STATE_SEED3;
	output[61] = STATE_SEED2;
	output[62] = STATE_SEED1;
	output[63] = STATE_SEED0;
	return output;

}


