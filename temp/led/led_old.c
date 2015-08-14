    
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "led_old.h"
#include "../../ciphers/LIB/dsl_lib.h"

int main(){
    // gm_bs_test();
    run();
    // run_led_tests();
}

// void tests()  {
//   run_lib_tests();  
//   run_led_tests();
// }


void run()  {
    KEY_SIZE_CNS = malloc(8 *sizeof(uint8_t));
    KEY_SIZE_CNS = bitslice(KEY_SIZE,8);
    init_RC();
    init_mds();
    int r = 0; 
    // for(r = 0; r < 32; r++)  {
    //     if(!r%4)    {
    //         addRoundKey(state,key);
    //     }
    step(state,r);
    // }
    // addRoundKey(state,key);
    // printf("fin: ");
    // hex_print(state,16,64);
}

void step(uint8_t *curr_state, int r) {
    addConstants(curr_state,r);
    printf("post cnst: ");
    hex_print(curr_state,16,64);
    subCells(curr_state);
    printf("sbox: ");
    hex_print(curr_state,16,64);
    shiftRow(curr_state);
    printf("sr: ");
    hex_print(curr_state,16,64);
    mixColumnsSerial(curr_state);
    printf("mcs: ");
    hex_print(curr_state,16,64);
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
  printf("A: ");
  hex_print(a,4,4);
  printf("B: ");
  hex_print(b,4,4);
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
  memmove(g,g+4,4 * sizeof(uint8_t));
  printf("RES: ");
  hex_print(g,4,8);
  realloc(g,4 * sizeof(uint8_t));
  return g;
}

void gm_bs_2(uint8_t g[8], uint8_t a[4], uint8_t b[4]){
    uint8_t hbs[1] = {0};
    // printf("a: ");
    // hex_print(a,4,4);
    // printf("b: ");
    hex_print(b,4,4);
    uint8_t gf_poly[8] = {0,0,0,1,0,0,1,1};
    uint8_t one[8] = {0,0,0,0,0,0,0,1};
    uint8_t a_in[4] = {0};
    uint8_t b_in[4] = {0};
    for(int bit = 0; bit < 4; bit++)    {
        a_in[4 + bit] = a[bit];
    }
    for(int bit = 0; bit < 4; bit++)    {
        b_in[4 + bit] = b[bit];
    }
    for(int deg = 0; deg < 4; deg++)    {
        uint8_t f[1] = {0};
        uint8_t m[8] = {0};
        uint8_t t[8] = {0};
        uint8_t temp_a[8] = {0};
        uint8_t temp_b[8] = {0};
        for(int bit = 0; bit <8; bit++) {
            t[bit] = b_in[bit] & one[bit];
        }
        for(int bit = 0; bit < 8; bit++) {
            f[0] = f[0] | t[bit];
        }
        for(int bit = 0; bit < 8; bit++)    {
            m[bit] = f[0] & a_in[bit];
        }
        for(int bit = 0; bit <8; bit++) {
            g[bit] ^= (m[bit] & a_in[bit]);
        }
        hbs[0] = a_in[7 - 3];
        shift_left_2(temp_a, a_in, 8, 1);
        for(int bit = 0; bit < 8; bit++)  {
            a_in[bit] = temp_a[bit];
        }
        for(int bit = 0; bit < 8; bit++)    {
            a_in[bit] ^= (hbs[0] & gf_poly[bit]);
        }       
        shift_right_2(temp_b,b_in, 8, 1);
        for(int bit = 0; bit < 8; bit++)  {
            b_in[bit] = temp_b[bit];
        }

    }
    // printf("g: ");
    // hex_print(g,4,8);
}

uint8_t gm_std(uint8_t a, uint8_t b){
  uint8_t g = 0;
  int i;
  for (i = 0; i < 4; i++) {
    if ( (b & 0x1) == 1 ) { 
        g ^= a; 
    }
    uint8_t hbs = (a & 0x8);
    a <<= 0x1;
    if ( hbs == 0x8) { 
        a ^= 0x13; 
    }
    b >>= 0x1;
  }
  return g;

}

uint8_t gm_std_mask(uint8_t a, uint8_t b){
  uint8_t g = 0;
  int i;
  for (i = 0; i < 4; i++) {
    g ^= (a & (b & 0x1));
    uint8_t hbs = (a & 0x8);
    a <<= 0x1;
    a ^= ((hbs * 0x8) & 0x13);
    b >>= 0x1;
  }
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
    // printf("cnst: ");
    // hex_print(cnst,16,64);
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
        row = rotate_left(row,16,curr_row * 4);
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
