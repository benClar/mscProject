#include <time.h>
#include <mach/mach.h>
#include <mach/mach_time.h>

#define log_err(M, ...) fprintf(stderr, "[ERROR] (%s:%d:) " M "\n", __FILE__, __LINE__, ##__VA_ARGS__)

void rotate_right(uint32_t *target, uint32_t *source, int shift, int var_size);
void rotate_left(uint32_t *target, uint32_t *source, int shift, int var_size);
void shift_right(uint32_t *target, uint32_t *source, int shift, int var_size);
void shift_left(uint32_t *target, uint32_t *source, int shift, int var_size);
void reverse(uint32_t *target, int start, int end);
void bitslice_shift(uint32_t *target, uint32_t *source, int shift, int var_size, char *op);
void bs_copy(uint32_t *target, uint32_t *source, int size);
void XOR(uint32_t *target, uint32_t *op_1, uint32_t *op_2, int var_size);
void AND(uint32_t *target, uint32_t *op_1, uint32_t *op_2, int var_size);
void OR(uint32_t *target, uint32_t *op_1, uint32_t *op_2, int var_size);
void extract_bs_range(uint32_t *target, uint32_t *source, int start, int finish);
void bitslice_bitwise(uint32_t *target, uint32_t *op_1, uint32_t *op_2, int var_size, char *op);
void bitslice(uint32_t *target, long source, int var_size);
void bitslice_bend(uint32_t *target, long source, int var_size);
void int_to_bitsliced(uint32_t *target, uint32_t source, int var_size);
double get_time();
void hprint(uint32_t *target, int size);
void hex_print(uint32_t *state, int row_width, int area);
void bitslice_add(uint32_t *output, uint32_t *operand_1, uint32_t *operand_2, int width);
void bitslice_subtract(uint32_t *output, uint32_t *operand_1, uint32_t *operand_2, int width);
/*Tests*/

void shift_testing();
void testing();
void reverse_testing();
void bitwise_testing();
void bitslice_testing();
void print(uint32_t *arr, int size);
void rprint(uint32_t *arr, int size);
