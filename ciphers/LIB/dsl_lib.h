#ifndef TEST_Dsl_lib_h
#define TEST_Dsl_lib_h
#define GF_POLY       0x13

#define TESTING 0
#define log_err(M, ...) fprintf(stderr, "[ERROR] (%s:%d:) " M "\n", __FILE__, __LINE__, ##__VA_ARGS__)

void extract_bs_range(uint32_t *target, uint32_t *source, int start, int finish);
uint32_t *shift(uint32_t *input, int var_size, int shift, char *op);
uint32_t *reverse(uint32_t *array, int start, int end);
uint32_t *rotate_left(uint32_t *key, int var_size ,int shift);
uint32_t *rotate_right(uint32_t *input, int var_size ,int shift);
uint32_t *shift_right(uint32_t *input, int var_size ,int shift);
uint32_t *shift_left(uint32_t *input, int var_size ,int shift);
uint32_t *clone(uint32_t *input, int var_size);
void print_array(uint32_t *array,int size);
uint32_t *clone(uint32_t *input, int var_size);
uint32_t *XOR(uint32_t *a, uint32_t *b, int size);
uint32_t *bitslice(long var, int var_size);
int compare(uint32_t *a, uint32_t *b, int size);
uint32_t *matrix_column(uint32_t *matrix, int col_width, int row_width, int col, int area);
int array_position(int curr_row, int curr_col, int row_width);
void hex_print(uint32_t *state, int row_width, int area);
int bits_in(int value);
// uint32_t **clone_square_matrix(uint32_t **input, int length, int ele_size);
// void print_sq_matrix(uint32_t **m, int length);
// int compare_sq_matrix(uint32_t **a, uint32_t **b, int length);

/*testing*/
void run_lib_tests();
void rotate_tests();
void shift_tests();
void test_bitslice();
void test_matrix_column();
void test_array_position();
// void test_sq_matrix_clone();

#endif
