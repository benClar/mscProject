#ifndef TEST_Dsl_lib_h
#define TEST_Dsl_lib_h
#define GF_POLY       0x13

#define TESTING 0
#define log_err(M, ...) fprintf(stderr, "[ERROR] (%s:%d:) " M "\n", __FILE__, __LINE__, ##__VA_ARGS__)

void extract_bs_range(uint8_t *target, uint8_t *source, int start, int finish);
uint8_t *shift(uint8_t *input, int var_size, int shift, char *op);
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
int compare(uint8_t *a, uint8_t *b, int size);
uint8_t *matrix_column(uint8_t *matrix, int col_width, int row_width, int col, int area);
int array_position(int curr_row, int curr_col, int row_width);
void hex_print(uint8_t *state, int row_width, int area);
int bits_in(int value);
void shift_right_2(uint8_t *target, uint8_t *source, int var_size, int shift);
void shift_left_2(uint8_t *target, uint8_t *source, int var_size, int shift);
void bitslice_add(uint32_t *output, uint32_t *A, uint32_t *B, int width);
// uint8_t **clone_square_matrix(uint8_t **input, int length, int ele_size);
// void print_sq_matrix(uint8_t **m, int length);
// int compare_sq_matrix(uint8_t **a, uint8_t **b, int length);

/*testing*/
void run_lib_tests();
void rotate_tests();
void shift_tests();
void test_bitslice();
void test_matrix_column();
void test_array_position();
// void test_sq_matrix_clone();

#endif
