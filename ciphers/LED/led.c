    
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "led.h"

// int main(){
//     // gm_bs_test();
//     run();
//     // run_led_tests();
// }

// void tests()  {
//   run_lib_tests();  
//   run_led_tests();
// }


// void run()  {
//     KEY_SIZE_CNS = malloc(8 *sizeof(uint8_t));
//     KEY_SIZE_CNS = bitslice(KEY_SIZE,8);
//     init_RC();
//     init_mds();
//     int r = 0; 
//     for(r = 0; r < 32; r++)  {
//         if(!r%4)    {
//             addRoundKey(state,key);
//         }
//         step(state,r);
//     }
//     addRoundKey(state,key);
//     printf("fin: ");
//     hex_print(state,16,64);
// }

void enc(uint32_t state[64], uint32_t key[64], uint32_t MDS[16][4], uint32_t RC[32][6]) {
    int r = 0; 
    // for(r = 0; r < 32; r++)  {
    //     if(!r%4)    {
    //         state[0] ^= key[0];
    //         state[1] ^= key[1];
    //         state[2] ^= key[2];
    //         state[3] ^= key[3];
    //         state[4] ^= key[4];
    //         state[5] ^= key[5];
    //         state[6] ^= key[6];
    //         state[7] ^= key[7];
    //         state[8] ^= key[8];
    //         state[9] ^= key[9];
    //         state[10] ^= key[10];
    //         state[11] ^= key[11];
    //         state[12] ^= key[12];
    //         state[13] ^= key[13];
    //         state[14] ^= key[14];
    //         state[15] ^= key[15];
    //         state[16] ^= key[16];
    //         state[17] ^= key[17];
    //         state[18] ^= key[18];
    //         state[19] ^= key[19];
    //         state[20] ^= key[20];
    //         state[21] ^= key[21];
    //         state[22] ^= key[22];
    //         state[23] ^= key[23];
    //         state[24] ^= key[24];
    //         state[25] ^= key[25];
    //         state[26] ^= key[26];
    //         state[27] ^= key[27];
    //         state[28] ^= key[28];
    //         state[29] ^= key[29];
    //         state[30] ^= key[30];
    //         state[31] ^= key[31];
    //         state[32] ^= key[32];
    //         state[33] ^= key[33];
    //         state[34] ^= key[34];
    //         state[35] ^= key[35];
    //         state[36] ^= key[36];
    //         state[37] ^= key[37];
    //         state[38] ^= key[38];
    //         state[39] ^= key[39];
    //         state[40] ^= key[40];
    //         state[41] ^= key[41];
    //         state[42] ^= key[42];
    //         state[43] ^= key[43];
    //         state[44] ^= key[44];
    //         state[45] ^= key[45];
    //         state[46] ^= key[46];
    //         state[47] ^= key[47];
    //         state[48] ^= key[48];
    //         state[49] ^= key[49];
    //         state[50] ^= key[50];
    //         state[51] ^= key[51];
    //         state[52] ^= key[52];
    //         state[53] ^= key[53];
    //         state[54] ^= key[54];
    //         state[55] ^= key[55];
    //         state[56] ^= key[56];
    //         state[57] ^= key[57];
    //         state[58] ^= key[58];
    //         state[59] ^= key[59];
    //         state[60] ^= key[60];
    //         state[61] ^= key[61];
    //         state[62] ^= key[62];
    //         state[63] ^= key[63];
    //     }
        step(state,RC[r]);
//     }
//     state[0] ^= key[0];
//     state[1] ^= key[1];
//     state[2] ^= key[2];
//     state[3] ^= key[3];
//     state[4] ^= key[4];
//     state[5] ^= key[5];
//     state[6] ^= key[6];
//     state[7] ^= key[7];
//     state[8] ^= key[8];
//     state[9] ^= key[9];
//     state[10] ^= key[10];
//     state[11] ^= key[11];
//     state[12] ^= key[12];
//     state[13] ^= key[13];
//     state[14] ^= key[14];
//     state[15] ^= key[15];
//     state[16] ^= key[16];
//     state[17] ^= key[17];
//     state[18] ^= key[18];
//     state[19] ^= key[19];
//     state[20] ^= key[20];
//     state[21] ^= key[21];
//     state[22] ^= key[22];
//     state[23] ^= key[23];
//     state[24] ^= key[24];
//     state[25] ^= key[25];
//     state[26] ^= key[26];
//     state[27] ^= key[27];
//     state[28] ^= key[28];
//     state[29] ^= key[29];
//     state[30] ^= key[30];
//     state[31] ^= key[31];
//     state[32] ^= key[32];
//     state[33] ^= key[33];
//     state[34] ^= key[34];
//     state[35] ^= key[35];
//     state[36] ^= key[36];
//     state[37] ^= key[37];
//     state[38] ^= key[38];
//     state[39] ^= key[39];
//     state[40] ^= key[40];
//     state[41] ^= key[41];
//     state[42] ^= key[42];
//     state[43] ^= key[43];
//     state[44] ^= key[44];
//     state[45] ^= key[45];
//     state[46] ^= key[46];
//     state[47] ^= key[47];
//     state[48] ^= key[48];
//     state[49] ^= key[49];
//     state[50] ^= key[50];
//     state[51] ^= key[51];
//     state[52] ^= key[52];
//     state[53] ^= key[53];
//     state[54] ^= key[54];
//     state[55] ^= key[55];
//     state[56] ^= key[56];
//     state[57] ^= key[57];
//     state[58] ^= key[58];
//     state[59] ^= key[59];
//     state[60] ^= key[60];
//     state[61] ^= key[61];
//     state[62] ^= key[62];
//     state[63] ^= key[63];
}

void step(uint32_t curr_state[64], uint32_t rc[6]) {
    addConstants(curr_state,rc);
    // printf("cnst: ");
    // hex_print(curr_state,16,64);
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


void mixColumnsSerial(uint32_t curr_state[64], uint32_t mds[16][4])   {
    int col_nibble,col,col_row;
    uint8_t *curr_state_col = malloc(16*sizeof(uint8_t));
    uint8_t *curr_state_nibble = calloc(4,sizeof(uint8_t));
    uint8_t *curr_mds_nibble = malloc(4*sizeof(uint8_t));
    uint32_t res[8] = 0;
    uint32_t column[4][4];
    for(col = 0; col < 4; col++)   {
        column[0][0] = curr_state[col * 4]
        column[0][1] = curr_state[(col * 4) + 1]
        column[0][2] = curr_state[(col * 4) + 2]
        column[0][2] = curr_state[(col * 4) + 3]
        column[1][0] = curr_state[((col * 4) + 16)]
        column[1][1] = curr_state[((col * 4) + 16) + 1]
        column[1][2] = curr_state[((col * 4) + 16) + 2]
        column[1][2] = curr_state[((col * 4) + 16) + 3]
        column[2][0] = curr_state[((col * 4) + 32)]
        column[2][1] = curr_state[((col * 4) + 32) + 1]
        column[2][2] = curr_state[((col * 4) + 32) + 2]
        column[2][2] = curr_state[((col * 4) + 32) + 3]
        column[3][0] = curr_state[((col * 4) + 48)]
        column[3][1] = curr_state[((col * 4) + 48) + 1]
        column[3][2] = curr_state[((col * 4) + 48) + 2]
        column[3][2] = curr_state[((col * 4) + 48) + 3]
        for(col_row = 0; col_row < 4; col_row++)    {
            for(col_nibble = 0; col_nibble < 4; col_nibble++)    {

                // memcpy(curr_mds_nibble,&(mds[array_position(col_row,col_nibble * NIBBLE_SIZE,16)]),4 * sizeof(uint8_t)); //!Get nibble from MDS
                memcpy(curr_state_nibble,&(curr_state_col[array_position(col_nibble,0,4)]),4 * sizeof(uint8_t)); //! Get nibble from column
                if(col_nibble > 0)  {
                    res = XOR(res,gm_bs(curr_mds_nibble,curr_state_nibble),4);
                } else {
                    res = gm_bs(curr_mds_nibble,curr_state_nibble);
                }
            }
            // memcpy(&(curr_state[array_position(col_row,col * NIBBLE_SIZE,16)]),res,4*sizeof(uint8_t));
        }
    }
}                

// uint8_t *gm_bs(uint8_t *a, uint8_t *b) {
//   uint8_t *a_in = calloc(8,sizeof(uint8_t));
//   uint8_t *b_in = calloc(8,sizeof(uint8_t));
//   memcpy(&(a_in[4]),a,4);
//   memcpy(&(b_in[4]),b,4);
//   uint8_t *poly = bitslice(GF_POLY,8);
//   uint8_t *g = calloc(8,sizeof(uint8_t));
//   int i;
//   for (i = 0; i < 4; i++) {
//     if (b_in[8 - 1] == 1 ) { 
//         g = XOR(g,a_in,8); 
//     }

//     uint8_t *hbs = AND(a_in,bitslice(0x8,8),8);
//     a_in = shift_left(a_in,8,1);
//     if (compare(hbs,bitslice(0x8,8),8)) { 
//         a_in = XOR(a_in,poly,8);
//     }

//     b_in = shift_right(b_in,8,1);
//   }
//   memmove(g,g+4,4 * sizeof(uint8_t));
//   realloc(g,4 * sizeof(uint8_t));
//   return g;
// }

void gm_bs_2(uint32_t g[8], uint32_t a[4], uint32_t b[4]){
    uint8_t hbs[1] = {0};
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
        hbs[0] = a_in[3];
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
}

// uint8_t gm_std(uint8_t a, uint8_t b){
//   uint8_t g = 0;
//   int i;
//   for (i = 0; i < 4; i++) {
//     if ( (b & 0x1) == 1 ) { 
//         g ^= a; 
//     }
//     uint8_t hbs = (a & 0x8);
//     a <<= 0x1;
//     if ( hbs == 0x8) { 
//         a ^= 0x13; 
//     }
//     b >>= 0x1;
//   }
//   return g;

// }

void addConstants(uint32_t state[64], uint32_t r_cnst[6])   {
    uint32_t cnst[64] = {0};
    uint32_t row_temp[4] = {0};
    int row, ele;
    for(row = 0,ele = 0; row < 4; row++)    {
        bitslice_bend(row_temp,row,4);
        cnst[row * 16] = row_temp[0];
        cnst[(row * 16) + 1] = row_temp[1];
        cnst[(row * 16) + 2] = row_temp[2];
        cnst[(row * 16) + 3] = row_temp[3];
        if(row == 0 || row == 2)    {
            cnst[(row * 16) + 5] = r_cnst[5 - 5];
            cnst[(row * 16) + 6] = r_cnst[5 - 4];
            cnst[(row * 16) + 7] = r_cnst[5 - 3];
        } else {
            cnst[(row * 16) + 5] = r_cnst[5 - 2];
            cnst[(row * 16) + 6] = r_cnst[5 - 1];
            cnst[(row * 16) + 7] = r_cnst[5 - 0];
        }
            cnst[8] = 0x0;
            cnst[9] = 0x0;
            cnst[10] = 0x0;
            cnst[11] = 0x0;
            cnst[12] = 0x0;
            cnst[13] = 0x0;
            cnst[14] = 0x0;
            cnst[15] = 0x0;
    }
    state[0] ^= cnst[0];
    state[1] ^= cnst[1];
    state[2] ^= cnst[2];
    state[3] ^= cnst[3];
    state[4] ^= cnst[4];
    state[5] ^= cnst[5];
    state[6] ^= cnst[6];
    state[7] ^= cnst[7];
    state[8] ^= cnst[8];
    state[9] ^= cnst[9];
    state[10] ^= cnst[10];
    state[11] ^= cnst[11];
    state[12] ^= cnst[12];
    state[13] ^= cnst[13];
    state[14] ^= cnst[14];
    state[15] ^= cnst[15];
    state[16] ^= cnst[16];
    state[17] ^= cnst[17];
    state[18] ^= cnst[18];
    state[19] ^= cnst[19];
    state[20] ^= cnst[20];
    state[21] ^= cnst[21];
    state[22] ^= cnst[22];
    state[23] ^= cnst[23];
    state[24] ^= cnst[24];
    state[25] ^= cnst[25];
    state[26] ^= cnst[26];
    state[27] ^= cnst[27];
    state[28] ^= cnst[28];
    state[29] ^= cnst[29];
    state[30] ^= cnst[30];
    state[31] ^= cnst[31];
    state[32] ^= cnst[32];
    state[33] ^= cnst[33];
    state[34] ^= cnst[34];
    state[35] ^= cnst[35];
    state[36] ^= cnst[36];
    state[37] ^= cnst[37];
    state[38] ^= cnst[38];
    state[39] ^= cnst[39];
    state[40] ^= cnst[40];
    state[41] ^= cnst[41];
    state[42] ^= cnst[42];
    state[43] ^= cnst[43];
    state[44] ^= cnst[44];
    state[45] ^= cnst[45];
    state[46] ^= cnst[46];
    state[47] ^= cnst[47];
    state[48] ^= cnst[48];
    state[49] ^= cnst[49];
    state[50] ^= cnst[50];
    state[51] ^= cnst[51];
    state[52] ^= cnst[52];
    state[53] ^= cnst[53];
    state[54] ^= cnst[54];
    state[55] ^= cnst[55];
    state[56] ^= cnst[56];
    state[57] ^= cnst[57];
    state[58] ^= cnst[58];
    state[59] ^= cnst[59];
    state[60] ^= cnst[60];
    state[61] ^= cnst[61];
    state[62] ^= cnst[62];
    state[63] ^= cnst[63];
    hex_print(state, 16, 64);
}

// void init_RC() {
//     int curr;
//     RC = malloc(RC_TOTAL * sizeof(uint8_t*));
//     for(curr = 0; curr < RC_TOTAL; curr++)  {
//         RC[curr] = bitslice(RC_std[curr],RC_LENGTH);
//     }
// }

void shiftRow(uint32_t curr_state[64])   {
    uint32_t row[16];
    int curr_row;
    for(curr_row = 0; curr_row < 4; curr_row++)    {
        uint32_t output[16] = {0};
        row[0] = curr_state[(curr_row * 16) + 0];
        row[1] = curr_state[(curr_row * 16) + 1];
        row[2] = curr_state[(curr_row * 16) + 2];
        row[3] = curr_state[(curr_row * 16) + 3];
        row[4] = curr_state[(curr_row * 16) + 4];
        row[5] = curr_state[(curr_row * 16) + 5];
        row[6] = curr_state[(curr_row * 16) + 6];
        row[7] = curr_state[(curr_row * 16) + 7];
        row[8] = curr_state[(curr_row * 16) + 8];
        row[9] = curr_state[(curr_row * 16) + 9];
        row[10] = curr_state[(curr_row * 16) + 10];
        row[11] = curr_state[(curr_row * 16) + 11];
        row[12] = curr_state[(curr_row * 16) + 12];
        row[13] = curr_state[(curr_row * 16) + 13];
        row[14] = curr_state[(curr_row * 16) + 14];
        row[15] = curr_state[(curr_row * 16) + 15];
        rotate_left(output,row, 16, curr_row * 4);
        curr_state[(curr_row * 16) + 0] = output[0];
        curr_state[(curr_row * 16) + 1] = output[1];
        curr_state[(curr_row * 16) + 2] = output[2];
        curr_state[(curr_row * 16) + 3] = output[3];
        curr_state[(curr_row * 16) + 4] = output[4];
        curr_state[(curr_row * 16) + 5] = output[5];
        curr_state[(curr_row * 16) + 6] = output[6];
        curr_state[(curr_row * 16) + 7] = output[7];
        curr_state[(curr_row * 16) + 8] = output[8];
        curr_state[(curr_row * 16) + 9] = output[9];
        curr_state[(curr_row * 16) + 10] = output[10];
        curr_state[(curr_row * 16) + 11] = output[11];
        curr_state[(curr_row * 16) + 12] = output[12];
        curr_state[(curr_row * 16) + 13] = output[13];
        curr_state[(curr_row * 16) + 14] = output[14];
        curr_state[(curr_row * 16) + 15] = output[15];
    }
}

uint8_t sbox_1(uint32_t input[4])  {
    return (((~input[A] & ~input[C] & ~input[D] ) | (~input[A] & input[C] & input[D] ) | (input[A] & ~input[B] & input[D]) | (input[A] & ~input[B] & input[C]) | (~input[A] & input[B] & input[C])) & 1);
}

uint8_t sbox_2(uint32_t input[4])  {
    return (((~input[B] & input[C] & ~input[D]) | (input[A] & input[B] & ~input[C]) | (~input[B] & ~input[C] & input[D]) | (~input[A] & ~input[B] & ~input[C]) | (~input[A] & input[B] & input[C] & input[D])) & 1);
}

uint8_t sbox_3(uint32_t input[4])  {
    return (((input[A] & input[B] & input[D]) | (input[A] & ~input[B] & ~input[C]) | (~input[A] & input[C] & ~input[D]) | (~input[A] & ~input[B] & input[C]) | (input[A] & ~input[B] & ~input[D])) & 1);
}

uint8_t sbox_4(uint32_t input[4])  {
    return (((~input[A] & input[C] & input[D] ) | ( input[A] & input[C] & ~input[D] ) | (input[A] & ~input[B] & ~input[D] ) | (~input[A] & ~input[B] & input[D]) | ( ~input[A] & input[B] & ~input[C] & ~input[D]) | (input[A] & input[B] & ~input[C] & input[D])) & 1);
}


void sBox_array_input(uint32_t output[4], uint32_t input[4])   {
    output[0] = sbox_1(input);
    output[1] = sbox_2(input);
    output[2] = sbox_3(input);
    output[3] = sbox_4(input);
    input[0] = output[0];
    input[1] = output[1];
    input[2] = output[2];
    input[3] = output[3];
}

void subCells(uint32_t curr_state[64])   {
    int nibble_ele,bit_ele;
    uint32_t nibble[4];
    uint32_t result[4];

    for(nibble_ele = 0; nibble_ele < 16; nibble_ele++)  {
        bit_ele = (nibble_ele * 4);
        nibble[0] = curr_state[bit_ele];
        nibble[1] = curr_state[bit_ele + 1];
        nibble[2] = curr_state[bit_ele + 2];
        nibble[3] = curr_state[bit_ele + 3];
        sBox_array_input(result,nibble);
        curr_state[bit_ele] = result[0];
        curr_state[bit_ele + 1] = result[1];
        curr_state[bit_ele + 2] = result[2];
        curr_state[bit_ele + 3] = result[3];
    }
}

/* testing */

// void run_led_tests()    {
//     sput_start_testing();
//     sput_enter_suite("gm_bs tests");
//     sput_run_test(gm_bs_test); 
// //     sput_enter_suite("shiftRow tests");
// //     sput_run_test(shift_row_test); 
// }

// void shift_row_test()   {
//     uint8_t test_m_2[64] = { 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,
//                     17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,
//                     33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,
//                     49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64 
//                   };
//     shiftRow(test_m_2);
//     print_array(test_m_2,64);
//     sput_fail_unless(test_m_2[0]==1,"shift row test");
//     sput_fail_unless(test_m_2[1]==2,"shift row test");
//     sput_fail_unless(test_m_2[2]==3,"shift row test");
//     sput_fail_unless(test_m_2[3]==4,"shift row test");
//     sput_fail_unless(test_m_2[4]==5,"shift row test");
//     sput_fail_unless(test_m_2[5]==6,"shift row test");
//     sput_fail_unless(test_m_2[6]==7,"shift row test");
//     sput_fail_unless(test_m_2[7]==8,"shift row test");
//     sput_fail_unless(test_m_2[8]==9,"shift row test");
//     sput_fail_unless(test_m_2[9]==10,"shift row test");
//     sput_fail_unless(test_m_2[10]==11,"shift row test");
//     sput_fail_unless(test_m_2[11]==12,"shift row test");
//     sput_fail_unless(test_m_2[12]==13,"shift row test");
//     sput_fail_unless(test_m_2[13]==14,"shift row test");
//     sput_fail_unless(test_m_2[14]==15,"shift row test");
//     sput_fail_unless(test_m_2[15]==16,"shift row test");
//     sput_fail_unless(test_m_2[16]==21,"shift row test");
//     sput_fail_unless(test_m_2[17]==22,"shift row test");
//     sput_fail_unless(test_m_2[18]==23,"shift row test");
//     sput_fail_unless(test_m_2[19]==24,"shift row test");
//     sput_fail_unless(test_m_2[20]==25,"shift row test");
//     sput_fail_unless(test_m_2[21]==26,"shift row test");
//     sput_fail_unless(test_m_2[22]==27,"shift row test");
//     sput_fail_unless(test_m_2[23]==28,"shift row test");
//     sput_fail_unless(test_m_2[24]==29,"shift row test");
//     sput_fail_unless(test_m_2[25]==30,"shift row test");
//     sput_fail_unless(test_m_2[26]==31,"shift row test");
//     sput_fail_unless(test_m_2[27]==32,"shift row test");
//     sput_fail_unless(test_m_2[28]==17,"shift row test");
//     sput_fail_unless(test_m_2[29]==18,"shift row test");
//     sput_fail_unless(test_m_2[30]==19,"shift row test");
//     sput_fail_unless(test_m_2[31]==20,"shift row test");
//     sput_fail_unless(test_m_2[32]==41,"shift row test");
//     sput_fail_unless(test_m_2[33]==42,"shift row test");
//     sput_fail_unless(test_m_2[34]==43,"shift row test");
//     sput_fail_unless(test_m_2[35]==44,"shift row test");
//     sput_fail_unless(test_m_2[36]==45,"shift row test");
//     sput_fail_unless(test_m_2[37]==46,"shift row test");
//     sput_fail_unless(test_m_2[38]==47,"shift row test");
//     sput_fail_unless(test_m_2[39]==48,"shift row test");
//     sput_fail_unless(test_m_2[40]==33,"shift row test");
//     sput_fail_unless(test_m_2[41]==34,"shift row test");
//     sput_fail_unless(test_m_2[42]==35,"shift row test");
//     sput_fail_unless(test_m_2[43]==36,"shift row test");
//     sput_fail_unless(test_m_2[44]==37,"shift row test");
//     sput_fail_unless(test_m_2[45]==38,"shift row test");
//     sput_fail_unless(test_m_2[46]==39,"shift row test");
//     sput_fail_unless(test_m_2[47]==40,"shift row test");
//     sput_fail_unless(test_m_2[48]==61,"shift row test");
//     sput_fail_unless(test_m_2[49]==62,"shift row test");
//     sput_fail_unless(test_m_2[50]==63,"shift row test");
//     sput_fail_unless(test_m_2[51]==64,"shift row test");
//     sput_fail_unless(test_m_2[52]==49,"shift row test");
//     sput_fail_unless(test_m_2[53]==50,"shift row test");
//     sput_fail_unless(test_m_2[54]==51,"shift row test");
//     sput_fail_unless(test_m_2[55]==52,"shift row test");
//     sput_fail_unless(test_m_2[56]==53,"shift row test");
//     sput_fail_unless(test_m_2[57]==54,"shift row test");
//     sput_fail_unless(test_m_2[58]==55,"shift row test");
//     sput_fail_unless(test_m_2[59]==56,"shift row test");
//     sput_fail_unless(test_m_2[60]==57,"shift row test");
//     sput_fail_unless(test_m_2[61]==58,"shift row test");
//     sput_fail_unless(test_m_2[62]==59,"shift row test");
//     sput_fail_unless(test_m_2[63]==60,"shift row test");
// }

// void gm_bs_test()   {
//     uint8_t a[4] = {1,0,0,0};
//     uint8_t b[4] = {1,1,0,0};
//     uint8_t g[8]= {0};
//     uint8_t *res = gm_bs(a,b);
//     gm_bs_2(g,a,b);
//     printf("RES\n");
//     print_array(g,8);
//     // print_array(res,4);
//     printf("RES: %d \n",gm_std(8,12));
    // printf("%d\n",gm_std_mask(8,10));
    // sput_fail_unless(res[0] == 1,"gm_mult test");
    // sput_fail_unless(res[1] == 0,"gm_mult test");
    // sput_fail_unless(res[2] == 0,"gm_mult test");
    // sput_fail_unless(res[3] == 0,"gm_mult test");
// }

