#ifndef TEST_Dsl_lib_h
#define TEST_Dsl_lib_h

#define TESTING 1

uint8_t *reverse(uint8_t *array, int start, int end);
uint8_t *rotate_left(uint8_t *key, int var_size ,int shift);
uint8_t *rotate_right(uint8_t *input, int var_size ,int shift);
uint8_t *shift_right(uint8_t *input, int var_size ,int shift);
uint8_t *shift_left(uint8_t *input, int var_size ,int shift);
uint8_t *clone(uint8_t *input, int var_size);
void print_array(uint8_t *array,int size);
uint8_t *clone(uint8_t *input, int var_size);
uint8_t *XOR(uint8_t *a, uint8_t *b, int size);
uint8_t *bitslice(long var, int var_size);
uint8_t **clone_square_matrix(uint8_t **input, int length, int ele_size);
void print_sq_matrix(uint8_t **m, int length);
int compare_sq_matrix(uint8_t **a, uint8_t **b, int length);

/*testing*/
void run_lib_tests();
void rotate_tests();
void shift_tests();
void test_bitslice();
void test_sq_matrix_clone();

#endif
