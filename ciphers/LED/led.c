    
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "led.h"

void enc(uint32_t state[64], uint32_t key[64], uint32_t MDS[16][4], uint32_t RC[32][6]) {
    int r = 0; 
    for(r = 0; r < 32; r++)  {
        if(!(r%4))    {
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
        step(state,RC[r], MDS);
    }
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
void step(uint32_t curr_state[64], uint32_t rc[6], uint32_t MDS[16][4]) {
    addConstants(curr_state,rc);
    subCells(curr_state);
    shiftRow(curr_state);
    mixColumnsSerial(curr_state, MDS);
}
void mixColumnsSerial(uint32_t curr_state[64], uint32_t mds[16][4])   {
    int col = 0,col_row;
    uint32_t column[4][4];
    uint32_t a[8] = {0};
    uint32_t b[8] = {0};
    uint32_t c[8] = {0};
    uint32_t d[8]= {0};
    for(col = 0; col < 4; col++)   {
        column[0][0] = curr_state[col * 4];
        column[0][1] = curr_state[(col * 4) + 1];
        column[0][2] = curr_state[(col * 4) + 2];
        column[0][3] = curr_state[(col * 4) + 3];
        column[1][0] = curr_state[((col * 4) + 16)];
        column[1][1] = curr_state[((col * 4) + 16) + 1];
        column[1][2] = curr_state[((col * 4) + 16) + 2];
        column[1][3] = curr_state[((col * 4) + 16) + 3];
        column[2][0] = curr_state[((col * 4) + 32)];
        column[2][1] = curr_state[((col * 4) + 32) + 1];
        column[2][2] = curr_state[((col * 4) + 32) + 2];
        column[2][3] = curr_state[((col * 4) + 32) + 3];
        column[3][0] = curr_state[((col * 4) + 48)];
        column[3][1] = curr_state[((col * 4) + 48) + 1];
        column[3][2] = curr_state[((col * 4) + 48) + 2];
        column[3][3] = curr_state[((col * 4) + 48) + 3];
        for(col_row = 0; col_row < 4; col_row++)    {
            gm_bs_2(a, column[0], mds[(col_row * 4)]);
            gm_bs_2(b, column[1], mds[(col_row * 4) + 1]);
            gm_bs_2(c, column[2], mds[(col_row * 4) + 2]);
            gm_bs_2(d, column[3], mds[(col_row * 4) + 3]);
            curr_state[(col * 4) + (col_row * 16)] = a[4] ^ b[4] ^ c[4] ^ d[4];
            curr_state[(col * 4) + (col_row * 16) + 1] = a[5] ^ b[5] ^ c[5] ^ d[5];
            curr_state[(col * 4) + (col_row * 16) + 2] = a[6] ^ b[6] ^ c[6] ^ d[6];
            curr_state[(col * 4) + (col_row * 16) + 3] = a[7] ^ b[7] ^ c[7] ^ d[7];
        }
    }
}                
void gm_bs_2(uint32_t g[8], uint32_t a[4], uint32_t b[4]){
    g[0] = 0;
    g[1] = 0;
    g[2] = 0;
    g[3] = 0;
    g[4] = 0;
    g[5] = 0;
    g[6] = 0;
    g[7] = 0;
    uint32_t hbs[1] = {0};
    uint32_t gf_poly[8] = {0,0,0,0xffffffff,0,0,0xffffffff,0xffffffff};
    uint32_t one[8] = {0,0,0,0,0,0,0,0xffffffff};
    uint32_t a_in[8] = {0};
    uint32_t b_in[8] = {0};
    for(int bit = 0; bit < 4; bit++)    {
        a_in[4 + bit] = a[bit];
    }
    for(int bit = 0; bit < 4; bit++)    {
        b_in[4 + bit] = b[bit];
    }
    for(int deg = 0; deg < 4; deg++)    {
        uint32_t f[1] = {0};
        uint32_t m[8] = {0};
        uint32_t t[8] = {0};
        uint32_t temp_a[8] = {0};
        uint32_t temp_b[8] = {0};
        for(int bit = 0; bit <8; bit++) {
            t[bit] = b_in[bit] & one[bit];
        }
        for(int bit = 0; bit < 8; bit++) {
            f[0] = f[0] | t[bit];
        }
        for(int bit = 0; bit < 8; bit++)    {
            m[bit] = f[0] & a_in[bit];
        }
        for(int bit = 0; bit < 8; bit++) {
            g[bit] ^= (m[bit] & a_in[bit]);
        }
        hbs[0] = a_in[7 - 3];
        shift_left(temp_a, a_in, 1, 8);
        for(int bit = 0; bit < 8; bit++)  {
            a_in[bit] = temp_a[bit];
        }
        for(int bit = 0; bit < 8; bit++)    {
            a_in[bit] ^= (hbs[0] & gf_poly[bit]);
        }       
        shift_right(temp_b,b_in, 1, 8);
        for(int bit = 0; bit < 8; bit++)  {
            b_in[bit] = temp_b[bit];
        }
    }
}
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
}
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
        rotate_left(output,row, curr_row * 4, 16);
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
uint32_t sbox_1(uint32_t input[4])  {
    return (~input[A] & ~input[C] & ~input[D] ) | (~input[A] & input[C] & input[D] ) | (input[A] & ~input[B] & input[D]) | (input[A] & ~input[B] & input[C]) | (~input[A] & input[B] & input[C]);
}

uint32_t sbox_2(uint32_t input[4])  {
    return (~input[B] & input[C] & ~input[D]) | (input[A] & input[B] & ~input[C]) | (~input[B] & ~input[C] & input[D]) | (~input[A] & ~input[B] & ~input[C]) | (~input[A] & input[B] & input[C] & input[D]);
}

uint32_t sbox_3(uint32_t input[4])  {
    return (input[A] & input[B] & input[D]) | (input[A] & ~input[B] & ~input[C]) | (~input[A] & input[C] & ~input[D]) | (~input[A] & ~input[B] & input[C]) | (input[A] & ~input[B] & ~input[D]);
}

uint32_t sbox_4(uint32_t input[4])  {
    return (~input[A] & input[C] & input[D] ) | ( input[A] & input[C] & ~input[D] ) | (input[A] & ~input[B] & ~input[D] ) | (~input[A] & ~input[B] & input[D]) | ( ~input[A] & input[B] & ~input[C] & ~input[D]) | (input[A] & input[B] & ~input[C] & input[D]);
}
void sBox_array_input(uint32_t output[4], uint32_t input[4])   {
    output[0] = sbox_1(input);
    output[1] = sbox_2(input);
    output[2] = sbox_3(input);
    output[3] = sbox_4(input);
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


