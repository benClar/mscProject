    
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "led.h"

    struct element {
        int id;
        uint8_t value;
    };

    uint8_t state[ STATE_SIZE ] = { STATE_SEED63, STATE_SEED62, STATE_SEED61, STATE_SEED60, 
                                    STATE_SEED59, STATE_SEED58, STATE_SEED57, STATE_SEED56, 
                                    STATE_SEED55, STATE_SEED54, STATE_SEED53, STATE_SEED52,
                                    STATE_SEED51, STATE_SEED50, STATE_SEED49, STATE_SEED48, 

                                    STATE_SEED47, STATE_SEED46, STATE_SEED45, STATE_SEED44, 
                                    STATE_SEED43, STATE_SEED42, STATE_SEED41, STATE_SEED40,
                                    STATE_SEED39, STATE_SEED38, STATE_SEED37, STATE_SEED36,
                                    STATE_SEED35, STATE_SEED34, STATE_SEED33, STATE_SEED32,

                                    STATE_SEED31, STATE_SEED30, STATE_SEED29, STATE_SEED28,
                                    STATE_SEED27, STATE_SEED26, STATE_SEED25, STATE_SEED24,
                                    STATE_SEED23, STATE_SEED22, STATE_SEED21, STATE_SEED20,
                                    STATE_SEED19, STATE_SEED18, STATE_SEED17, STATE_SEED16,

                                    STATE_SEED15, STATE_SEED14, STATE_SEED13, STATE_SEED12,
                                    STATE_SEED11, STATE_SEED10, STATE_SEED9, STATE_SEED8,
                                    STATE_SEED7, STATE_SEED6, STATE_SEED5, STATE_SEED4,
                                    STATE_SEED3, STATE_SEED2, STATE_SEED1, STATE_SEED0 };

    uint8_t key[ KEY_SIZE ] = { KEY_SEED63, KEY_SEED62, KEY_SEED61, KEY_SEED60,
                                KEY_SEED59, KEY_SEED58, KEY_SEED57, KEY_SEED56, 
                                KEY_SEED55, KEY_SEED54, KEY_SEED53, KEY_SEED52,
                                KEY_SEED51, KEY_SEED50, KEY_SEED49, KEY_SEED48,
                                KEY_SEED47, KEY_SEED46, KEY_SEED45, KEY_SEED44,
                                KEY_SEED43, KEY_SEED42, KEY_SEED41, KEY_SEED40, 
                                KEY_SEED39, KEY_SEED38, KEY_SEED37, KEY_SEED36,
                                KEY_SEED35, KEY_SEED34, KEY_SEED33, KEY_SEED32,
                                KEY_SEED31, KEY_SEED30, KEY_SEED29, KEY_SEED28,
                                KEY_SEED27, KEY_SEED26, KEY_SEED25, KEY_SEED24,
                                KEY_SEED23, KEY_SEED22, KEY_SEED21, KEY_SEED20,
                                KEY_SEED19, KEY_SEED18, KEY_SEED17, KEY_SEED16, 
                                KEY_SEED15, KEY_SEED14, KEY_SEED13, KEY_SEED12,
                                KEY_SEED11, KEY_SEED10, KEY_SEED9, KEY_SEED8,
                                KEY_SEED7, KEY_SEED6, KEY_SEED5, KEY_SEED4,
                                KEY_SEED3, KEY_SEED2, KEY_SEED1, KEY_SEED0 };

    uint8_t mds[ 16 ] = {   M0, M1, M2, M3,
                            M4, M5, M6, M7,
                            M8, M9, M10, M11,
                            M12, M13, M14, M15 
                        };

    int main(){
        // uint8_t array1[16] = {1,2,3,4,
        //                 5,6,7,8,
        //                 9,10,11,12,
        //                 13,14,15,16};
        shiftRow(state);
        // Element *test_state = createState();
        // initState(test_state);
        // print_test_state(test_state);
        // shiftRow_test(test_state);
        // print_test_state(test_state);
    }

    

    void print_test_state(Element *test_state)  {
        int row;
        for(row = 0; row < 4; row++) {
            print_test_row(test_state,row);
        } 
    }

    void print_test_row(Element *test_state, int row)    {
        row *= 16;
        int nibble,bit;
            for(nibble = 0; nibble < 16; nibble+=4)   {
                for(bit = 0; bit < 4; bit++)    {
                    printf("%d,",test_state[row + nibble + bit]->id);
                }
                printf(" ");
            }
        printf("\n");
    }

    uint8_t* shiftRow(uint8_t *state)   {
        uint8_t *row = (uint8_t*) malloc(16 * sizeof(uint8_t));
        int curr_row;
        for(curr_row = 0; curr_row < 4; curr_row++)    {
            memcpy(row,&(state[curr_row * 16]),16);
            rotate(row,curr_row,16);
            memcpy(&(state[curr_row * 16]),row,16);

        }
        return state;
    }

    Element* shiftRow_test(Element *test_state)   {
        Element *row = (Element*) malloc(16 * sizeof(*row));
        int curr_row;
        for(curr_row = 0; curr_row < 4; curr_row++)    {
            memcpy(row,&(test_state[curr_row * 16]),16 * sizeof(*test_state[curr_row * 16]));
            // printf("before: \n");
            // print_test_row(row,0);

            rotate_test(row,curr_row,16);
            memcpy(&(test_state[curr_row * 16]),row,16 * sizeof(*test_state[curr_row * 16]));
            // printf("after: \n");
            // print_test_row(row,0);
        }
        return test_state;
    }



    uint8_t* reverse(uint8_t *array, int start, int end) {
            uint8_t *tmp = (uint8_t*) malloc(NIBBLE_SIZE * sizeof(uint8_t));
            while(start < end)  {
                memcpy(tmp,&(array[start]),NIBBLE_SIZE);
                memcpy(&(array[start]),&(array[end - NIBBLE_SIZE]),NIBBLE_SIZE);
                memcpy(&(array[end - NIBBLE_SIZE]),tmp,NIBBLE_SIZE);
                start += NIBBLE_SIZE;
                end -= NIBBLE_SIZE;
            }   
            return array;
    }

    Element* reverse_test(Element *array, int start, int end) {
            Element *tmp = (Element*) malloc(NIBBLE_SIZE * sizeof(*tmp));
            while(start < end)  {
                memcpy(tmp,&(array[start]),NIBBLE_SIZE * sizeof(*array[start]));
                memcpy(&(array[start]),&(array[end - NIBBLE_SIZE]),NIBBLE_SIZE * sizeof(*array[start]));
                memcpy(&(array[end - NIBBLE_SIZE]),tmp,NIBBLE_SIZE * sizeof(*array[start]));
                start += NIBBLE_SIZE;
                end -= NIBBLE_SIZE;
            }   
            return array;
    }


    uint8_t* rotate(uint8_t *state, int shift, int size)    {
        shift *= 4;
        reverse(state, 0, size);
        reverse(state, 0, size - shift);
        reverse(state, size - shift, size);
        return state;
    }

    Element* rotate_test(Element *test_state, int shift, int size)    {
        shift *= 4;
        reverse_test(test_state, 0, size);
        reverse_test(test_state, 0, size - shift);
        reverse_test(test_state, size - shift, size);
        return test_state;
    }


    void sbox_1(uint8_t *input)  {
        input[A] = (((~input[A] & ~input[C] & ~input[D] ) | 
            (~input[A] & input[C] & input[D] ) | 
            (input[A] & ~input[B] & input[D]) | 
            (input[A] & ~input[B] & input[C]) | 
            (~input[A] & input[B] & input[C])) & 1);
    }

    void sbox_2(uint8_t *input)  {
        input[B] = (((~input[B] & input[C] & ~input[D]) | 
            (input[A] & input[B] & ~input[C]) | 
            (~input[B] & ~input[C] & input[D]) | 
            (~input[A] & ~input[B] & ~input[C]) | 
            (~input[A] & input[B] & input[C] & input[D])) & 1);
    }

    void sbox_3(uint8_t *input)  {
        input[C] = (((input[A] & input[B] & input[D]) | 
            (input[A] & ~input[B] & ~input[C]) | 
            (~input[A] & input[C] & ~input[D]) | 
            (~input[A] & ~input[B] & input[C]) | 
            (input[A] & ~input[B] & ~input[D])) & 1);
    }

    void sbox_4(uint8_t *input)  {
        input[D] = (((~input[A] & input[C] & input[D] ) | 
            ( input[A] & input[C] & ~input[D] ) | 
            (input[A] & ~input[B] & ~input[D] ) | 
            (~input[A] & ~input[B] & input[D]) | 
            ( ~input[A] & input[B] & ~input[C] & ~input[D]) | 
            (input[A] & input[B] & ~input[C] & input[D])) & 1);
    }

    uint8_t* subCells(uint8_t *state)   {
        int current_nibble,  bit;
        int total_nibbles = STATE_SIZE/4;
        uint8_t nibble[4];
        for(current_nibble = 0; current_nibble < total_nibbles; current_nibble++)   {
                for(bit = 0; bit < 4; bit++)    {
                    nibble[bit] = state[current_nibble + bit];
                } 
                sbox_1(nibble);
                sbox_2(nibble);
                sbox_3(nibble);
                sbox_4(nibble);
                for(bit = 0; bit < 4; bit++)    {
                    state[current_nibble + bit] = nibble[bit];
                } 
        }

        return state;
    }

    Element* createState()   {
        Element *s = (Element*) malloc(STATE_SIZE * sizeof(*s));
        int e;
        for(e = 0; e < STATE_SIZE; e++) {
            s[e] = malloc(sizeof(*s[e]));
        }

        return s;
    }

    void initState(Element *s)    {
        int e;
        for(e = 0; e < STATE_SIZE; e++) {
            s[e]->id = e;
            s[e]->value = 0x0;
        }
    }

