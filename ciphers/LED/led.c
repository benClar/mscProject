    
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "led.h"
#include "../LIB/dsl_lib.h"
#include "../LIB/sput.h"

int main(){
    if(TESTING) {
       tests();
    } else  {
        run();
    }
}

void tests()  {
  run_lib_tests();  
  run_led_tests();
}


void run()  {
    KEY_SIZE_CNS = malloc(8 *sizeof(uint8_t));
    KEY_SIZE_CNS = bitslice(KEY_SIZE,8);
    init_RC();
    init_mds();
    int r = 0;
    for(r = 0; r < 32; r++)  {
        if(!r%4)    {
            addRoundKey(state,key);
        }
        step(state,r);
    }
    addRoundKey(state,key);
    hex_print(state,16,64);
}

void step(uint8_t *curr_state, int r) {
    addConstants(curr_state,r);
    subCells(curr_state);
    shiftRow(curr_state);
    mixColumnsSerial(curr_state);
}


void addRoundKey(uint8_t *state, uint8_t *r_key)  {
    XOR(state,r_key,KEY_SIZE);
}

void init_mds() {
    mds = malloc(16 * 16 * (sizeof(uint8_t)));
    int nibble;
    for(nibble = 0; nibble < 16; nibble++)   {
        memcpy(&(mds[NIBBLE_SIZE*nibble]),bitslice(mds_std[nibble],NIBBLE_SIZE),NIBBLE_SIZE * sizeof(uint8_t));
    }
}
void mixColumnsSerial(uint8_t *curr_state)   {
    int col_nibble,col,col_row;
    uint8_t *curr_state_col = malloc(16*sizeof(uint8_t));
    uint8_t *curr_state_nibble = calloc(4,sizeof(uint8_t));
    uint8_t *curr_mds_nibble = malloc(4*sizeof(uint8_t));
    uint8_t *res = calloc(4,sizeof(uint8_t));
    
    for(col = 0; col < 4; col++)   {
        curr_state_col = matrix_column(curr_state,4,16,col,64); //! Select nibble column of state
        for(col_row = 0; col_row < 4; col_row++)    {

            for(col_nibble = 0; col_nibble < 4; col_nibble++)    {

                memcpy(curr_mds_nibble,&(mds[array_position(col_row,col_nibble * NIBBLE_SIZE,16)]),4 * sizeof(uint8_t)); //!Get nibble from MDS
                memcpy(curr_state_nibble,&(curr_state_col[array_position(col_nibble,0,4)]),4 * sizeof(uint8_t)); //! Get nibble from column
                if(col_nibble > 0)  {
                    res = XOR(res,gm_bs(curr_mds_nibble,curr_state_nibble),4);
                } else {
                    res = gm_bs(curr_mds_nibble,curr_state_nibble);
                }
            }
            memcpy(&(curr_state[array_position(col_row,col * NIBBLE_SIZE,16)]),res,4*sizeof(uint8_t));
        }
    }
}                

uint8_t *gm_bs(uint8_t *a, uint8_t *b) {
  uint8_t *a_in = calloc(8,sizeof(uint8_t));
  uint8_t *b_in = calloc(8,sizeof(uint8_t));
  memcpy(&(a_in[4]),a,4);
  memcpy(&(b_in[4]),b,4);
  uint8_t *poly = bitslice(GF_POLY,8);
  uint8_t *g = calloc(8,sizeof(uint8_t));
  int i;
  for (i = 0; i < 4; i++) {
    if (b_in[8 - 1] == 1 ) { 
        g = XOR(g,a_in,8); 
    }

    uint8_t *hbs = AND(a_in,bitslice(0x8,8),8);
    a_in = shift_left(a_in,8,1);
    if (compare(hbs,bitslice(0x8,8),8)) { 
        a_in = XOR(a_in,poly,8);
    }

    b_in = shift_right(b_in,8,1);
  }
  memmove(g,g+4,4*sizeof(uint8_t));
  realloc(g,4 * sizeof(uint8_t));
  return g;
}

void addConstants(uint8_t *state, int r)   {
    uint8_t *cnst = calloc(16 * 16,sizeof(uint8_t));
    uint8_t *zerod = bitslice(0x00,8);
    int row, ele,col;
    for(row = 0,ele = 0; row < 4; row++)    {
        memcpy(&(cnst[array_position(row,0,16)]),bitslice(row,4),4);

        if(row == 0 || row == 2)    {
            memcpy(&(cnst[array_position(row,5,16)]), &(RC[r][(RC_LENGTH - 5) - 1]), 3*sizeof(uint8_t) );
        } else {
            memcpy(&(cnst[array_position(row,5,16)]), &(RC[r][(RC_LENGTH - 2) - 1]), 3*sizeof(uint8_t) );
        }
        memcpy(&(cnst[array_position(row,9,16)]),zerod,8*sizeof(uint8_t));
    }
    for(row = 0; row < 4; row++)    {
        for(col = 0; col<16; col++) {
            state[array_position(row,col,16)] ^= cnst[array_position(row,col,16)];
        }
    }
}

void init_RC() {
    int curr;
    RC = malloc(RC_TOTAL * sizeof(uint8_t*));
    for(curr = 0; curr < RC_TOTAL; curr++)  {
        RC[curr] = bitslice(RC_std[curr],RC_LENGTH);
    }
}

uint8_t* shiftRow(uint8_t *curr_state)   {
    uint8_t *row = (uint8_t*) malloc(16 * sizeof(uint8_t));
    int curr_row;
    for(curr_row = 0; curr_row < 4; curr_row++)    {
        memcpy(row,&(curr_state[array_position(curr_row,0,16)]),16);
        // print_array(row,16);
        row = rotate_left(row,16,curr_row * 4);
        // print_array(row,16);
        memcpy(&(curr_state[curr_row * 16]),row,16);

    }
    return curr_state;
}

uint8_t sbox_1(uint8_t *input)  {
    return (((~input[A] & ~input[C] & ~input[D] ) | (~input[A] & input[C] & input[D] ) | (input[A] & ~input[B] & input[D]) | (input[A] & ~input[B] & input[C]) | (~input[A] & input[B] & input[C])) & 1);
}

uint8_t sbox_2(uint8_t *input)  {
    return (((~input[B] & input[C] & ~input[D]) | (input[A] & input[B] & ~input[C]) | (~input[B] & ~input[C] & input[D]) | (~input[A] & ~input[B] & ~input[C]) | (~input[A] & input[B] & input[C] & input[D])) & 1);
}

uint8_t sbox_3(uint8_t *input)  {
    return (((input[A] & input[B] & input[D]) | (input[A] & ~input[B] & ~input[C]) | (~input[A] & input[C] & ~input[D]) | (~input[A] & ~input[B] & input[C]) | (input[A] & ~input[B] & ~input[D])) & 1);
}

uint8_t sbox_4(uint8_t *input)  {
    return (((~input[A] & input[C] & input[D] ) | ( input[A] & input[C] & ~input[D] ) | (input[A] & ~input[B] & ~input[D] ) | (~input[A] & ~input[B] & input[D]) | ( ~input[A] & input[B] & ~input[C] & ~input[D]) | (input[A] & input[B] & ~input[C] & input[D])) & 1);
}


uint8_t* sBox_array_input(uint8_t *input)   {
    uint8_t *output = (uint8_t*) malloc(4*sizeof(uint8_t));
    output[0] = sbox_1(input);
    output[1] = sbox_2(input);
    output[2] = sbox_3(input);
    output[3] = sbox_4(input);
    return output;
}

void subCells(uint8_t *curr_state)   {
    int nibble_ele,bit_ele;
    uint8_t nibble[4];

    for(nibble_ele = 0; nibble_ele < 16; nibble_ele++)  {
        bit_ele = (nibble_ele * 4);
        memcpy(nibble,&state[bit_ele],4);
        memcpy(&curr_state[bit_ele],sBox_array_input(nibble),4);
    }
}

/* testing */

void run_led_tests()    {
    sput_start_testing();
    sput_enter_suite("gm_bs tests");
    sput_run_test(gm_bs_test); 
    sput_enter_suite("shiftRow tests");
    sput_run_test(shift_row_test); 
}

void shift_row_test()   {
    uint8_t test_m_2[64] = { 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,
                    17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,
                    33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,
                    49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64 
                  };
    shiftRow(test_m_2);
    print_array(test_m_2,64);
    sput_fail_unless(test_m_2[0]==1,"shift row test");
    sput_fail_unless(test_m_2[1]==2,"shift row test");
    sput_fail_unless(test_m_2[2]==3,"shift row test");
    sput_fail_unless(test_m_2[3]==4,"shift row test");
    sput_fail_unless(test_m_2[4]==5,"shift row test");
    sput_fail_unless(test_m_2[5]==6,"shift row test");
    sput_fail_unless(test_m_2[6]==7,"shift row test");
    sput_fail_unless(test_m_2[7]==8,"shift row test");
    sput_fail_unless(test_m_2[8]==9,"shift row test");
    sput_fail_unless(test_m_2[9]==10,"shift row test");
    sput_fail_unless(test_m_2[10]==11,"shift row test");
    sput_fail_unless(test_m_2[11]==12,"shift row test");
    sput_fail_unless(test_m_2[12]==13,"shift row test");
    sput_fail_unless(test_m_2[13]==14,"shift row test");
    sput_fail_unless(test_m_2[14]==15,"shift row test");
    sput_fail_unless(test_m_2[15]==16,"shift row test");
    sput_fail_unless(test_m_2[16]==21,"shift row test");
    sput_fail_unless(test_m_2[17]==22,"shift row test");
    sput_fail_unless(test_m_2[18]==23,"shift row test");
    sput_fail_unless(test_m_2[19]==24,"shift row test");
    sput_fail_unless(test_m_2[20]==25,"shift row test");
    sput_fail_unless(test_m_2[21]==26,"shift row test");
    sput_fail_unless(test_m_2[22]==27,"shift row test");
    sput_fail_unless(test_m_2[23]==28,"shift row test");
    sput_fail_unless(test_m_2[24]==29,"shift row test");
    sput_fail_unless(test_m_2[25]==30,"shift row test");
    sput_fail_unless(test_m_2[26]==31,"shift row test");
    sput_fail_unless(test_m_2[27]==32,"shift row test");
    sput_fail_unless(test_m_2[28]==17,"shift row test");
    sput_fail_unless(test_m_2[29]==18,"shift row test");
    sput_fail_unless(test_m_2[30]==19,"shift row test");
    sput_fail_unless(test_m_2[31]==20,"shift row test");
    sput_fail_unless(test_m_2[32]==41,"shift row test");
    sput_fail_unless(test_m_2[33]==42,"shift row test");
    sput_fail_unless(test_m_2[34]==43,"shift row test");
    sput_fail_unless(test_m_2[35]==44,"shift row test");
    sput_fail_unless(test_m_2[36]==45,"shift row test");
    sput_fail_unless(test_m_2[37]==46,"shift row test");
    sput_fail_unless(test_m_2[38]==47,"shift row test");
    sput_fail_unless(test_m_2[39]==48,"shift row test");
    sput_fail_unless(test_m_2[40]==33,"shift row test");
    sput_fail_unless(test_m_2[41]==34,"shift row test");
    sput_fail_unless(test_m_2[42]==35,"shift row test");
    sput_fail_unless(test_m_2[43]==36,"shift row test");
    sput_fail_unless(test_m_2[44]==37,"shift row test");
    sput_fail_unless(test_m_2[45]==38,"shift row test");
    sput_fail_unless(test_m_2[46]==39,"shift row test");
    sput_fail_unless(test_m_2[47]==40,"shift row test");
    sput_fail_unless(test_m_2[48]==61,"shift row test");
    sput_fail_unless(test_m_2[49]==62,"shift row test");
    sput_fail_unless(test_m_2[50]==63,"shift row test");
    sput_fail_unless(test_m_2[51]==64,"shift row test");
    sput_fail_unless(test_m_2[52]==49,"shift row test");
    sput_fail_unless(test_m_2[53]==50,"shift row test");
    sput_fail_unless(test_m_2[54]==51,"shift row test");
    sput_fail_unless(test_m_2[55]==52,"shift row test");
    sput_fail_unless(test_m_2[56]==53,"shift row test");
    sput_fail_unless(test_m_2[57]==54,"shift row test");
    sput_fail_unless(test_m_2[58]==55,"shift row test");
    sput_fail_unless(test_m_2[59]==56,"shift row test");
    sput_fail_unless(test_m_2[60]==57,"shift row test");
    sput_fail_unless(test_m_2[61]==58,"shift row test");
    sput_fail_unless(test_m_2[62]==59,"shift row test");
    sput_fail_unless(test_m_2[63]==60,"shift row test");
}

void gm_bs_test()   {
    uint8_t a[4] = {0,1,0,0};
    uint8_t b[4] = {0,0,1,0};
    uint8_t *res = gm_bs(a,b);
    sput_fail_unless(res[0] == 1,"gm_mult test");
    sput_fail_unless(res[1] == 0,"gm_mult test");
    sput_fail_unless(res[2] == 0,"gm_mult test");
    sput_fail_unless(res[3] == 0,"gm_mult test");
}

