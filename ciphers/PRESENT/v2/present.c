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

uint8_t *rotate(uint8_t *key, int var_size ,int shift)    {
    reverse(key, 0, var_size - 1);
    reverse(key, 0, var_size - shift - 1);
    reverse(key, var_size - shift, var_size - 1);
    return key;
}

void test_rotate()	{
		uint8_t test[80] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,
						17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,
						33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,
						49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,
						65,66,67,68,69,70,71,72,73,74,75,76,77,78,79};
		reverse(test,0,79);
		sput_fail_unless(test[0] == 79,"reverse");
		sput_fail_unless(test[79] == 0,"reverse");
		rotate(test,80,61);
		sput_fail_unless(test[0] == 18,"rotate by 61");
		sput_fail_unless(test[1] == 17,"rotate by 61");
		sput_fail_unless(test[78] == 20,"rotate by 61");
		sput_fail_unless(test[79] == 19,"rotate by 61");

}

uint8_t *keyXOR(uint8_t *key, int round)	{
	key[79 - 19] ^= (round >>4 & 1);
	key[79 - 18] ^= (round >>3 & 1);
	key[79 - 17] ^= (round >>2 & 1);
	key[79 - 16] ^= (round >>1 & 1);
	key[79 - 15] ^= (round & 1);
	return key;
}

void test_keyXOR()	{
	uint8_t test[80] = { 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
				0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
				0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
				0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
				0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0	};

	keyXOR(test,4);
	sput_fail_unless(test[60] == 0,"key XOR");
	sput_fail_unless(test[61] == 0,"key XOR");
	sput_fail_unless(test[62] == 1,"key XOR");
	sput_fail_unless(test[63] == 0,"key XOR");
	sput_fail_unless(test[64] == 0,"key XOR");
	keyXOR(test,5);
	sput_fail_unless(test[60] == 0,"key XOR");
	sput_fail_unless(test[61] == 0,"key XOR");
	sput_fail_unless(test[62] == 0,"key XOR");
	sput_fail_unless(test[63] == 0,"key XOR");
	sput_fail_unless(test[64] == 1,"key XOR");
	keyXOR(test,31);
	sput_fail_unless(test[60] == 1,"key XOR");
	sput_fail_unless(test[61] == 1,"key XOR");
	sput_fail_unless(test[62] == 1,"key XOR");
	sput_fail_unless(test[63] == 1,"key XOR");
	sput_fail_unless(test[64] == 0,"key XOR");
}

int generateRoundKey(uint8_t *key, uint8_t *subKey, int round) {
    int keyBit;
    for(keyBit = 0; keyBit < 64; keyBit++)   {
        subKey[ keyBit ] = key[ keyBit ];
    }
    rotate(key,KEY_SIZE,61);
    memcpy(&key[0],sBox(key[0],key[1],key[2],key[3]),4);
	keyXOR(key,round);
    return 1;
}

uint8_t* sBox(uint8_t a,uint8_t b,uint8_t c,uint8_t d)	{
	uint8_t input[4] = {a,b,c,d};
	uint8_t *output = (uint8_t*) malloc(4*sizeof(uint8_t));
	output[0] = sbox_1(input);
	output[1] = sbox_2(input);
	output[2] = sbox_3(input);
	output[3] = sbox_4(input);
	return output;
}

uint8_t* sBox_array_input(uint8_t *input)	{
	uint8_t *output = (uint8_t*) malloc(4*sizeof(uint8_t));
	output[0] = sbox_1(input);
	output[1] = sbox_2(input);
	output[2] = sbox_3(input);
	output[3] = sbox_4(input);
	return output;
}

void test_sbox()	{
	uint8_t test_1[4] = {0,0,0,0};
	uint8_t test_2[4] = {0,0,0,1};
	uint8_t test_3[4] = {0,0,1,0};
	uint8_t test_4[4] = {0,0,1,1};
	uint8_t test_5[4] = {0,1,0,0};
	uint8_t test_6[4] = {0,1,0,1};
	uint8_t test_7[4] = {0,1,1,0};
	uint8_t test_8[4] = {0,1,1,1};
	uint8_t test_9[4] = {1,0,0,0};
	uint8_t test_10[4] = {1,0,0,1};
	uint8_t test_11[4] = {1,0,1,0};
	uint8_t test_12[4] = {1,0,1,1};	
	uint8_t test_13[4] = {1,1,0,0};
	uint8_t test_14[4] = {1,1,0,1};
	uint8_t test_15[4] = {1,1,1,0};
	uint8_t test_16[4] = {1,1,1,1};
	uint8_t *output;
	output = sBox_array_input(test_1);
	sput_fail_unless(output[0] == 1,"Sbox Testing 1");
	sput_fail_unless(output[1] == 1,"Sbox Testing 1");
	sput_fail_unless(output[2] == 0,"Sbox Testing 1");
	sput_fail_unless(output[3] == 0,"Sbox Testing 1");
	output = sBox_array_input(test_2);
	sput_fail_unless(output[0] == 0,"Sbox Testing 2");
	sput_fail_unless(output[1] == 1,"Sbox Testing");
	sput_fail_unless(output[2] == 0,"Sbox Testing");
	sput_fail_unless(output[3] == 1,"Sbox Testing");
	output = sBox_array_input(test_3);
	sput_fail_unless(output[0] == 0,"Sbox Testing 3");
	sput_fail_unless(output[1] == 1,"Sbox Testing");
	sput_fail_unless(output[2] == 1,"Sbox Testing");
	sput_fail_unless(output[3] == 0,"Sbox Testing");
	output = sBox_array_input(test_4);
	sput_fail_unless(output[0] == 1,"Sbox Testing 4");
	sput_fail_unless(output[1] == 0,"Sbox Testing");
	sput_fail_unless(output[2] == 1,"Sbox Testing");
	sput_fail_unless(output[3] == 1,"Sbox Testing");
	output = sBox_array_input(test_5);
	sput_fail_unless(output[0] == 1,"Sbox Testing 5");
	sput_fail_unless(output[1] == 0,"Sbox Testing");
	sput_fail_unless(output[2] == 0,"Sbox Testing");
	sput_fail_unless(output[3] == 1,"Sbox Testing");
	output = sBox_array_input(test_6);
	sput_fail_unless(output[0] == 0,"Sbox Testing 6");
	sput_fail_unless(output[1] == 0,"Sbox Testing");
	sput_fail_unless(output[2] == 0,"Sbox Testing");
	sput_fail_unless(output[3] == 0,"Sbox Testing");
	output = sBox_array_input(test_7);
	sput_fail_unless(output[0] == 1,"Sbox Testing 7");
	sput_fail_unless(output[1] == 0,"Sbox Testing");
	sput_fail_unless(output[2] == 1,"Sbox Testing");
	sput_fail_unless(output[3] == 0,"Sbox Testing");
	output = sBox_array_input(test_8);
	sput_fail_unless(output[0] == 1,"Sbox Testing 8");
	sput_fail_unless(output[1] == 1,"Sbox Testing");
	sput_fail_unless(output[2] == 0,"Sbox Testing");
	sput_fail_unless(output[3] == 1,"Sbox Testing");
	output = sBox_array_input(test_9);
	sput_fail_unless(output[0] == 0,"Sbox Testing 9");
	sput_fail_unless(output[1] == 0,"Sbox Testing");
	sput_fail_unless(output[2] == 1,"Sbox Testing");
	sput_fail_unless(output[3] == 1,"Sbox Testing");
	output = sBox_array_input(test_10);
	sput_fail_unless(output[0] == 1,"Sbox Testing 10");
	sput_fail_unless(output[1] == 1,"Sbox Testing");
	sput_fail_unless(output[2] == 1,"Sbox Testing");
	sput_fail_unless(output[3] == 0,"Sbox Testing");
	output = sBox_array_input(test_11);
	sput_fail_unless(output[0] == 1,"Sbox Testing 11");
	sput_fail_unless(output[1] == 1,"Sbox Testing");
	sput_fail_unless(output[2] == 1,"Sbox Testing");
	sput_fail_unless(output[3] == 1,"Sbox Testing");
	output = sBox_array_input(test_12);
	sput_fail_unless(output[0] == 1,"Sbox Testing 12");
	sput_fail_unless(output[1] == 0,"Sbox Testing");
	sput_fail_unless(output[2] == 0,"Sbox Testing");
	sput_fail_unless(output[3] == 0,"Sbox Testing");
	output = sBox_array_input(test_13);
	sput_fail_unless(output[0] == 0,"Sbox Testing 13");
	sput_fail_unless(output[1] == 1,"Sbox Testing");
	sput_fail_unless(output[2] == 0,"Sbox Testing");
	sput_fail_unless(output[3] == 0,"Sbox Testing");
	output = sBox_array_input(test_14);
	sput_fail_unless(output[0] == 0,"Sbox Testing 14");
	sput_fail_unless(output[1] == 1,"Sbox Testing");
	sput_fail_unless(output[2] == 1,"Sbox Testing");
	sput_fail_unless(output[3] == 1,"Sbox Testing");
	output = sBox_array_input(test_15);
	sput_fail_unless(output[0] == 0,"Sbox Testing 15");
	sput_fail_unless(output[1] == 0,"Sbox Testing");
	sput_fail_unless(output[2] == 0,"Sbox Testing");
	sput_fail_unless(output[3] == 1,"Sbox Testing");
	output = sBox_array_input(test_16);
	sput_fail_unless(output[0] == 0,"Sbox Testing 16");
	sput_fail_unless(output[1] == 0,"Sbox Testing");
	sput_fail_unless(output[2] == 1,"Sbox Testing");
	sput_fail_unless(output[3] == 0,"Sbox Testing");
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
	for(bit = 63; bit >= 0; bit-- )	{
		
		int target = ((16*(63 - bit)) % (STATE_SIZE - 1));
		if(bit == 0)	{
			target = 0;
		}	else {
			target = 63-target;
		}
		state[ target] = temp[ bit ];
	}
	free(temp);
}

void test_pLayer()	{
	uint8_t test[64] = {63,62,61,60,59,58,57,56,55,54,53,52,
 						51,50,49,48,47,46,45,44,43,42,41,40,
 						39,38,37,36,35,34,33,32,31,30,29,28,
 						27,26,25,24,23,22,21,20,19,18,17,16,
 						15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0};
	pLayer(test);
	sput_fail_unless(test[0] == 63,"pLayer Test");
	sput_fail_unless(test[1] == 59,"pLayer Test");
	sput_fail_unless(test[2] == 55,"pLayer Test");
	sput_fail_unless(test[3] == 51,"pLayer Test");
	sput_fail_unless(test[4] == 47,"pLayer Test");
	sput_fail_unless(test[5] == 43,"pLayer Test");
	sput_fail_unless(test[6] == 39,"pLayer Test");
	sput_fail_unless(test[7] == 35,"pLayer Test");
	sput_fail_unless(test[8] == 31,"pLayer Test");
	sput_fail_unless(test[9] == 27,"pLayer Test");
	sput_fail_unless(test[10] == 23,"pLayer Test");
	sput_fail_unless(test[11] == 19,"pLayer Test");
	sput_fail_unless(test[12] == 15,"pLayer Test");
	sput_fail_unless(test[13] == 11,"pLayer Test");
	sput_fail_unless(test[14] == 7,"pLayer Test");
	sput_fail_unless(test[15] == 3,"pLayer Test");
	sput_fail_unless(test[16] == 62,"pLayer Test");
	sput_fail_unless(test[17] == 58,"pLayer Test");
	sput_fail_unless(test[18] == 54,"pLayer Test");
	sput_fail_unless(test[19] == 50,"pLayer Test");
	sput_fail_unless(test[20] == 46,"pLayer Test");
}

void add_round_key(uint8_t *key, uint8_t *state)	{
	int bit;
	for(bit = 0; bit < 64; bit++)	{
		state[bit] = key[bit] ^ state[bit];
	}
}

void print_array(uint8_t *array,int size)	{
	int ele;
	for(ele = 0; ele < size; ele++)	{
		printf("%d", array[ele]);
	}
	printf("\n");
}

void test_present()	{
	sput_start_testing();
	sput_enter_suite("Test Rotate");
	sput_run_test(test_rotate);
	sput_enter_suite("Test keyXOR");
	sput_run_test(test_keyXOR);
	sput_enter_suite("Test pLayer");
	sput_run_test(test_pLayer);
	sput_enter_suite("Test sbox");
	sput_run_test(test_sbox);
	sput_finish_testing();
}

int main(){
	uint8_t key[ KEY_SIZE ] = { KEY_SEED79, KEY_SEED78, KEY_SEED77, KEY_SEED76, KEY_SEED75, KEY_SEED74,
								KEY_SEED73, KEY_SEED72, KEY_SEED71, KEY_SEED70, KEY_SEED69, KEY_SEED68,
								KEY_SEED67, KEY_SEED66, KEY_SEED65, KEY_SEED64, KEY_SEED63, KEY_SEED62,
								KEY_SEED61, KEY_SEED60, KEY_SEED59, KEY_SEED58, KEY_SEED57, KEY_SEED56,
								KEY_SEED55, KEY_SEED54, KEY_SEED53, KEY_SEED52, KEY_SEED51, KEY_SEED50,
								KEY_SEED49, KEY_SEED48, KEY_SEED47, KEY_SEED46, KEY_SEED45, KEY_SEED44,
								KEY_SEED43, KEY_SEED42, KEY_SEED41, KEY_SEED40, KEY_SEED39, KEY_SEED38,
								KEY_SEED37, KEY_SEED36, KEY_SEED35, KEY_SEED34, KEY_SEED33, KEY_SEED32,
								KEY_SEED31, KEY_SEED30, KEY_SEED29, KEY_SEED28, KEY_SEED27, KEY_SEED26,
								KEY_SEED25, KEY_SEED24, KEY_SEED23, KEY_SEED22, KEY_SEED21, KEY_SEED20,
								KEY_SEED19, KEY_SEED18, KEY_SEED17, KEY_SEED16, KEY_SEED15, KEY_SEED14,
								KEY_SEED13, KEY_SEED12, KEY_SEED11, KEY_SEED10, KEY_SEED9, KEY_SEED8,
								KEY_SEED7, KEY_SEED6, KEY_SEED5, KEY_SEED4, KEY_SEED3, KEY_SEED2,
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
									STATE_SEED0 };

	uint8_t **round_key = (uint8_t**) malloc(32 * sizeof(uint8_t*));
	int round_key_ele, round, bit_ele, nibble_ele;
	uint8_t nibble[4];
	// test_present();

	for(round_key_ele = 1; round_key_ele < 33; round_key_ele++)	{
		round_key[round_key_ele - 1] = (uint8_t*) malloc(64 * sizeof(uint8_t));
		generateRoundKey(key,round_key[round_key_ele - 1],round_key_ele);
	}

	// print_array(state,64);	

	for(round = 0; round < 31; round++)	{
		add_round_key(round_key[round],state);
		//sbox layer
		for(nibble_ele = 0; nibble_ele < 16; nibble_ele++)	{
			bit_ele = (nibble_ele * 4);
			memcpy(nibble,&state[bit_ele],4);
			memcpy(&state[bit_ele],sBox_array_input(nibble),4);
		}
		pLayer(state);
	}

	add_round_key(round_key[round],state);
	print_array(state,64);									
}
