typedef struct head *Head;
typedef struct node *Node;

#define PERM_SIZE 4
#define M64_SIZE 4

//m0
#define M0_0 0x0
#define M0_1 0x0
#define M0_2 0x0
#define M0_3 0x0

#define M0_4 0x0
#define M0_5 0x1
#define M0_6 0x0
#define M0_7 0x0

#define M0_8 0x0
#define M0_9 0x0
#define M0_10 0x1
#define M0_11 0x0

#define M0_12 0x0
#define M0_13 0x0
#define M0_14 0x0
#define M0_15 0x1

//m1
#define M1_0 0x1
#define M1_1 0x0
#define M1_2 0x0
#define M1_3 0x0

#define M1_4 0x0
#define M1_5 0x0
#define M1_6 0x0
#define M1_7 0x0

#define M1_8 0x0
#define M1_9 0x0
#define M1_10 0x1
#define M1_11 0x0

#define M1_12 0x0
#define M1_13 0x0
#define M1_14 0x0
#define M1_15 0x1

//m2
#define M2_0 0x1
#define M2_1 0x0
#define M2_2 0x0
#define M2_3 0x0

#define M2_4 0x0
#define M2_5 0x1
#define M2_6 0x0
#define M2_7 0x0

#define M2_8 0x0
#define M2_9 0x0
#define M2_10 0x0
#define M2_11 0x0

#define M2_12 0x0
#define M2_13 0x0
#define M2_14 0x0
#define M2_15 0x1

//m3
#define M3_0 0x1
#define M3_1 0x0
#define M3_2 0x0
#define M3_3 0x0

#define M3_4 0x0
#define M3_5 0x1
#define M3_6 0x0
#define M3_7 0x0

#define M3_8 0x0
#define M3_9 0x0
#define M3_10 0x1
#define M3_11 0x0

#define M3_12 0x0
#define M3_13 0x0
#define M3_14 0x0
#define M3_15 0x0

#define ZERO_SEED 0x0

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
#define KEY_SEED64 (0x0)
#define KEY_SEED65 0x0
#define KEY_SEED66 0x0
#define KEY_SEED67 0x0
#define KEY_SEED68 0x0
#define KEY_SEED69 0x0
#define KEY_SEED70 0x0
#define KEY_SEED71 0x0
#define KEY_SEED72 0x0
#define KEY_SEED73 0x0
#define KEY_SEED74 0x0
#define KEY_SEED75 0x0
#define KEY_SEED76 0x0
#define KEY_SEED77 0x0
#define KEY_SEED78 0x0
#define KEY_SEED79 0x0
#define KEY_SEED80 0x0
#define KEY_SEED81 0x0
#define KEY_SEED82 0x0
#define KEY_SEED83 0x0
#define KEY_SEED84 0x0
#define KEY_SEED85 0x0
#define KEY_SEED86 0x0
#define KEY_SEED87 0x0
#define KEY_SEED88 0x0
#define KEY_SEED89 0x0
#define KEY_SEED90 0x0
#define KEY_SEED91 0x0
#define KEY_SEED92 0x0
#define KEY_SEED93 0x0
#define KEY_SEED94 0x0
#define KEY_SEED95 0x0
#define KEY_SEED96 0x0
#define KEY_SEED97 0x0
#define KEY_SEED98 0x0
#define KEY_SEED99 0x0
#define KEY_SEED100 0x0
#define KEY_SEED101 0x0
#define KEY_SEED102 0x0
#define KEY_SEED103 0x0
#define KEY_SEED104 0x0
#define KEY_SEED105 0x0
#define KEY_SEED106 0x0
#define KEY_SEED107 0x0
#define KEY_SEED108 0x0
#define KEY_SEED109 0x0
#define KEY_SEED110 0x0
#define KEY_SEED111 0x0
#define KEY_SEED112 0x0
#define KEY_SEED113 0x0
#define KEY_SEED114 0x0
#define KEY_SEED115 0x0
#define KEY_SEED116 0x0
#define KEY_SEED117 0x0
#define KEY_SEED118 0x0
#define KEY_SEED119 0x0
#define KEY_SEED120 0x0
#define KEY_SEED121 0x0
#define KEY_SEED122 0x0
#define KEY_SEED123 0x0
#define KEY_SEED124 0x0
#define KEY_SEED125 0x0
#define KEY_SEED126 0x0
#define KEY_SEED127 0x0

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
#define END '\0'


#define RC_0 (0x0000000000000000)
#define RC_1 (0x13198a2e03707344)
#define RC_2 (0xa4093822299f31d0)
#define RC_3 (0x082efa98ec4e6c89)
#define RC_4 (0x452821e638d01377)
#define RC_5 (0xbe5466cf34e90c6c)
#define RC_6 (0x7ef84f78fd955cb1)
#define RC_7 (0x85840851f1ac43aa)
#define RC_8 (0xc882d32f25323c54)
#define RC_9 (0x64a51195e0e3610d)
#define RC_10 (0xd3b5a399ca0c2399)
#define RC_11 (0xc0ac29b7c97c50dd)

uint8_t** key_init();
void key_table_init();
Node new_bs_node();
Head new_bs_var(int size, uint8_t *seed_table);
Head reverse(Head var, int start, int end);
void generate_not_key(uint8_t **key);
int array_size(uint8_t *array);
Head new_bs_head();
Node clone_node(Node n);
Head clone(Head h);
void pairwise_node_swap(Node a,Node b);
void swap_nodes(Head h, Node a, Node b);
void print_var(Head h);
Node get(Head var, int n);
int var_size(Head var);
Head rotate_right(Head var, int shift);
Head rotate_left(Head var, int shift);
Head cut(Head var, int start, int end);
Head right_shift(Head var, int shift_size);
Head left_shift(Head var, int shift_size);
void add(Head var, Node n, char *end);
Head shift(Head var, int shift_size, char *shift_type);
Head XOR(Head a, Head b);
uint8_t sbox_1(uint8_t a, uint8_t b, uint8_t c, uint8_t d);
uint8_t sbox_2(uint8_t a, uint8_t b, uint8_t c, uint8_t d);
uint8_t sbox_3(uint8_t a, uint8_t b, uint8_t c, uint8_t d);
uint8_t sbox_4(uint8_t a, uint8_t b, uint8_t c, uint8_t d);
Head sbox(Head var);
Head k_add(Head sub_key, Head state);
uint8_t* bs_hex(uint64_t hex);
void print_array(uint8_t *array,int size);
void RC_add(Head rc, Head state);
Head *generate_M16_permutation(int start, Head* M_block);
Head **generate_M64_diagonal_matrix(Head *m0, Head *m1, Head *zero);
Head *clone_matrix(Head *m, int size);

