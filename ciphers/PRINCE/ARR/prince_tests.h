#ifndef TEST_Prince_tests_h
#define TEST_Prince_tests_h

#include "dsl_lib.h"
#include "prince.h"

/*testing*/
void run_tests();
void run_PRINCE_tests();
void test_gen_block_matrix();
int test_for_basic_m0(uint8_t *m);
int test_for_basic_m1(uint8_t *m);
int test_for_basic_m2(uint8_t *m);
int test_for_basic_m3(uint8_t *m);
void block_m_tester(uint8_t *M_block, int start);
void sbox_tests();
#endif
