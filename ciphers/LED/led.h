typedef struct element *Element;

#define STATE_SEED0 (0x0)
#define STATE_SEED1 (0x0)
#define STATE_SEED2 (0x0)
#define STATE_SEED3 (0x0)
#define STATE_SEED4 (0x0)
#define STATE_SEED5 (0x0)
#define STATE_SEED6 (0x0)
#define STATE_SEED7 (0x0)
#define STATE_SEED8 (0x0)
#define STATE_SEED9 (0x0)
#define STATE_SEED10 (0x0)
#define STATE_SEED11 (0x0)
#define STATE_SEED12 (0x0)
#define STATE_SEED13 (0x0)
#define STATE_SEED14 (0x0)
#define STATE_SEED15 (0x0)
#define STATE_SEED16 (0x0)
#define STATE_SEED17 (0x0)
#define STATE_SEED18 (0x0)
#define STATE_SEED19 (0x0)
#define STATE_SEED20 (0x0)
#define STATE_SEED21 (0x0)
#define STATE_SEED22 (0x0)
#define STATE_SEED23 (0x0)
#define STATE_SEED24 (0x0)
#define STATE_SEED25 (0x0)
#define STATE_SEED26 (0x0)
#define STATE_SEED27 (0x0)
#define STATE_SEED28 (0x0)
#define STATE_SEED29 (0x0)
#define STATE_SEED30 (0x0)
#define STATE_SEED31 (0x0)
#define STATE_SEED32 (0x0)
#define STATE_SEED33 (0x0)
#define STATE_SEED34 (0x0)
#define STATE_SEED35 (0x0)
#define STATE_SEED36 (0x0)
#define STATE_SEED37 (0x0)
#define STATE_SEED38 (0x0)
#define STATE_SEED39 (0x0)
#define STATE_SEED40 (0x0)
#define STATE_SEED41 (0x0)
#define STATE_SEED42 (0x0)
#define STATE_SEED43 (0x0)
#define STATE_SEED44 (0x0)
#define STATE_SEED45 (0x0)
#define STATE_SEED46 (0x0)
#define STATE_SEED47 (0x0)
#define STATE_SEED48 (0x0)
#define STATE_SEED49 (0x0)
#define STATE_SEED50 (0x0)
#define STATE_SEED51 (0x0)
#define STATE_SEED52 (0x0)
#define STATE_SEED53 (0x0)
#define STATE_SEED54 (0x0)
#define STATE_SEED55 (0x0)
#define STATE_SEED56 (0x0)
#define STATE_SEED57 (0x0)
#define STATE_SEED58 (0x0)
#define STATE_SEED59 (0x0)
#define STATE_SEED60 (0x0)
#define STATE_SEED61 (0x0)
#define STATE_SEED62 (0x0)
#define STATE_SEED63 (0x0)


#define KEY_SEED0 (0x0)
#define KEY_SEED1 (0x0)
#define KEY_SEED2 (0x0)
#define KEY_SEED3 (0x0)
#define KEY_SEED4 (0x0)
#define KEY_SEED5 (0x0)
#define KEY_SEED6 (0x0)
#define KEY_SEED7 (0x0)
#define KEY_SEED8 (0x0)
#define KEY_SEED9 (0x0)
#define KEY_SEED10 (0x0)
#define KEY_SEED11 (0x0)
#define KEY_SEED12 (0x0)
#define KEY_SEED13 (0x0)
#define KEY_SEED14 (0x0)
#define KEY_SEED15 (0x0)
#define KEY_SEED16 (0x0)
#define KEY_SEED17 (0x0)
#define KEY_SEED18 (0x0)
#define KEY_SEED19 (0x0)
#define KEY_SEED20 (0x0)
#define KEY_SEED21 (0x0)
#define KEY_SEED22 (0x0)
#define KEY_SEED23 (0x0)
#define KEY_SEED24 (0x0)
#define KEY_SEED25 (0x0)
#define KEY_SEED26 (0x0)
#define KEY_SEED27 (0x0)
#define KEY_SEED28 (0x0)
#define KEY_SEED29 (0x0)
#define KEY_SEED30 (0x0)
#define KEY_SEED31 (0x0)
#define KEY_SEED32 (0x0)
#define KEY_SEED33 (0x0)
#define KEY_SEED34 (0x0)
#define KEY_SEED35 (0x0)
#define KEY_SEED36 (0x0)
#define KEY_SEED37 (0x0)
#define KEY_SEED38 (0x0)
#define KEY_SEED39 (0x0)
#define KEY_SEED40 (0x0)
#define KEY_SEED41 (0x0)
#define KEY_SEED42 (0x0)
#define KEY_SEED43 (0x0)
#define KEY_SEED44 (0x0)
#define KEY_SEED45 (0x0)
#define KEY_SEED46 (0x0)
#define KEY_SEED47 (0x0)
#define KEY_SEED48 (0x0)
#define KEY_SEED49 (0x0)
#define KEY_SEED50 (0x0)
#define KEY_SEED51 (0x0)
#define KEY_SEED52 (0x0)
#define KEY_SEED53 (0x0)
#define KEY_SEED54 (0x0)
#define KEY_SEED55 (0x0)
#define KEY_SEED56 (0x0)
#define KEY_SEED57 (0x0)
#define KEY_SEED58 (0x0)
#define KEY_SEED59 (0x0)
#define KEY_SEED60 (0x0)
#define KEY_SEED61 (0x0)
#define KEY_SEED62 (0x0)
#define KEY_SEED63 (0x0)

#define STATE_SIZE 64
#define KEY_SIZE 64
#define NIBBLE_SIZE 4
#define M0 0x4
#define M1 0x1
#define M2 0x2
#define M3 0x2
#define M4 0x8
#define M5 0x6
#define M6 0x5
#define M7 0x6
#define M8 0xB
#define M9 0xE
#define M10 0xA
#define M11 0x9
#define M12 0x2
#define M13 0x2
#define M14 0xF
#define M15 0xB

#define A 	0	
#define B 	1
#define C 	2
#define D 	3

void sbox_1(uint8_t *input);
void sbox_2(uint8_t *input);
void sbox_3(uint8_t *input);
void sbox_4(uint8_t *input);
uint8_t* subCells(uint8_t *state);
uint8_t** generate_sub_keys(uint8_t *key, int rounds);
uint8_t* generate_sub_key(uint8_t* key, int rnd);
uint8_t* reverse(uint8_t *array, int start, int end);
uint8_t* rotate(uint8_t *state, int shift,int size);
uint8_t* shiftRow(uint8_t *state);
Element* createState();
void initState();
Element* reverse_test(Element *array, int start, int end);
Element* rotate_test(Element *state, int shift, int size);
Element* shiftRow_test(Element *state);
void print_test_state(Element *test_state);
void print_test_row(Element *test_state, int row);
