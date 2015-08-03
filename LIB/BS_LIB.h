#define log_err(M, ...) fprintf(stderr, "[ERROR] (%s:%d:) " M "\n", __FILE__, __LINE__, ##__VA_ARGS__)

void rotate_left(uint32_t *target, uint32_t *source, int var_size, int shift);
void rotate_right(uint32_t *target, uint32_t *source, int var_size, int shift);
void shift_right(uint32_t *target, uint32_t *source, int var_size, int shift);
void shift_left(uint32_t *target, uint32_t *source, int var_size, int shift);
void reverse(uint32_t *target, int start, int end);
void bitslice_shift(uint32_t *target, uint32_t *source, int shift, int var_size, char *op);
void bs_copy(uint32_t *target, uint32_t *source, int size);
void XOR(uint32_t *target, uint32_t *op_1, uint32_t *op_2, int var_size);
void AND(uint32_t *target, uint32_t *op_1, uint32_t *op_2, int var_size);
void OR(uint32_t *target, uint32_t *op_1, uint32_t *op_2, int var_size);
void extract_bs_range(uint32_t *target, uint32_t *source, int start, int finish);
void bitslice_bitwise(uint32_t *target, uint32_t *op_1, uint32_t *op_2, int var_size, char *op);
/*Tests*/

void shift_testing();
void testing();
void reverse_testing();
void bitwise_testing();
void bitslice_testing();
