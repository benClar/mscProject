#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "prince.h"

struct head	{
	Node start;
	Node end;
};

struct node	{
	uint8_t bit;
	Node next;
	Node prev;
};

uint8_t **KEY_SEED = NULL;
uint8_t *STATE_SEED;

int main()	{
	KEY_SEED = (uint8_t**) malloc(2*sizeof(uint8_t*));
	KEY_SEED[0] = malloc(64*sizeof(uint8_t));
	KEY_SEED[1] = malloc(64*sizeof(uint8_t));
	STATE_SEED = malloc(64*sizeof(uint8_t));
	key_table_init();
	// uint8_t seed[10] = {1,2,3,4,5,6,7,8,9,10};

	Head *key = malloc(3*sizeof(key));
	key[0] = new_bs_var(64,KEY_SEED[0]); //k0
	key[1] = XOR(rotate_right(key[0],1),left_shift(key[0],63)); //k0'
	key[2] = new_bs_var(64,KEY_SEED[1]); //k1
	Head state = new_bs_var(64,STATE_SEED);
	k_add(key[2],state);
	print_var(state);
	sbox(state);
	print_var(state);
	return 0;
}

Head k_add(Head sub_key, Head state)	{
	return XOR(sub_key,state);
}

Head sbox(Head var)	{
	int nibble;
	int bit;
	int node;
	int bits[4];
	Node nodes[4];
	for(nibble = 0; nibble < 16; nibble++)	{
		for( bit = 0; bit < 4; bit++)	{
			node = 4 * nibble + bit;
			nodes[bit] = get(var,node);
			bits[bit] = nodes[bit]->bit;
		}
		nodes[0]->bit = sbox_1(bits[0], bits[1], bits[2],bits[3]);
		nodes[1]->bit = sbox_2(bits[0], bits[1], bits[2],bits[3]);
		nodes[2]->bit = sbox_3(bits[0], bits[1], bits[2],bits[3]);
		nodes[3]->bit = sbox_4(bits[0], bits[1], bits[2],bits[3]);
	}
	return var;
}

uint8_t sbox_1(uint8_t a, uint8_t b, uint8_t c, uint8_t d)	{
	return (((~a & ~c) | (b & ~d) | (a & c & ~d)) & 1);
}

uint8_t sbox_2(uint8_t a, uint8_t b, uint8_t c, uint8_t d)	{
	return (((a & b) | (~c & d) | (a & ~c)) & 1);
}

uint8_t sbox_3(uint8_t a, uint8_t b, uint8_t c, uint8_t d)	{
	return (((~a & ~b) | (~c & ~d) |(~a & ~d) | (~b & ~c)) & 1);
}

uint8_t sbox_4(uint8_t a, uint8_t b, uint8_t c, uint8_t d)	{
	return (((b & c) | (a & ~c & d) | (~a & ~b & ~c) | (~a & ~b & ~d)) & 1);
}


Head XOR(Head a, Head b)	{
	Head c = new_bs_var(var_size(a),NULL);
	Node a_curr = a->start;
	Node b_curr = b->start;
	Node c_curr = c->start;

	while(a_curr != NULL && b_curr != NULL)	{
		c_curr->bit = a_curr->bit ^ b_curr->bit;
	 	a_curr = a_curr->next;
		b_curr = b_curr->next;
	 	c_curr = c_curr->next;
	}
	return c;

}

Head rotate_left(Head var, int shift)    {
	int size = var_size(var);
	Head cloned_var = clone(var);
	reverse(cloned_var, 0, size);
	reverse(cloned_var, 0, size - shift);
    reverse(cloned_var, size - shift + 1, size);
    return cloned_var;
}

Head rotate_right(Head var, int shift)    {
	int size = var_size(var);
	Head cloned_var = clone(var);
	reverse(cloned_var, 0, size - 1);
	reverse(cloned_var,shift, size - 1);
	reverse(cloned_var, 0, shift -1);
    return cloned_var;
}

Head reverse(Head var, int start, int end)	{
		// printf("%d \n",start);
		if(start >= end)	{
			return var;
		}

		while(start < end)	{
			Node start_node = get(var,start);
			Node end_node = get(var,end);
			swap_nodes(var,start_node,end_node);
			start++;
			end--;
		}	
		return var;
}

Node get(Head var, int n)	{
	int i = 0;
	Node curr = var->start;
	while(curr != NULL)	{
		if(i == n)	{
			return curr;
		}
		i++;
		curr = curr->next;
	}	
	return curr;
}

int var_size(Head var)	{
	Node curr = var->start;
	int cnt;
	for(cnt = 1; curr->next != NULL; cnt++)	{
		curr = curr->next;	
	}
	return cnt;
}

Head new_bs_head()	{
	Head h = malloc(sizeof(*h));
	h->start = NULL;
	h->end = NULL;
	return h;	
}

Head new_bs_var(int size, uint8_t *seed_table)	{
	int node_count;
	Head h = new_bs_head();
	for(node_count = 0; node_count < size; node_count++)	{
		if(h->start == NULL)	{
			if(seed_table == NULL)	{
				h->end = h->start = new_bs_node(0);
			} else {
				h->end = h->start = new_bs_node(seed_table[node_count]);
			}
		} else {
			if(seed_table == NULL)	{
				h->end->next = new_bs_node(0);
			} else {
				h->end->next = new_bs_node(seed_table[node_count]);
			}
			h->end->next->prev = h->end;
			h->end = h->end->next;
		}
	}
	return h;
}

void print_var(Head h)	{
	Node curr = h->start;
	while(curr != NULL)	{
		printf("%d ",curr->bit);
		curr = curr->next;
	}
	printf("\n");
}

void add(Head var, Node n, char *end)	{
	if(var->start == NULL)	{
		var->start = var->end = n;
	}
	if(!strcmp(end,"MSB"))	{
		n->next = var->start;
		n->next->prev = n;
		var->start = n;
		n->prev = NULL;
	} else if(!strcmp(end,"LSB"))	{
		n->prev = var->end;
		n->prev->next = n;
		var->end = n;
		n->next = NULL;
	}
}

Node new_bs_node(int val)	{
	Node n = (Node) malloc(sizeof(*n));
	n->next = NULL;
	n->prev = NULL;
	n->bit = val;
	return n;
}



void swap_nodes(Head h, Node a, Node b)	{
	Node temp;

	if(h->start == a){
		h->start = b;
	}
	if(h->end == b)	{
		h->end = a;
	}
	if(b->prev == a)	{
		pairwise_node_swap(a,b);
	} else {
		if(a->prev != NULL)	{
			a->prev->next = b;
		}
		b->prev->next = a;
		temp = a->next;
		a->next = b->next;
		b->next = temp;
		temp = b->prev;

		b->prev = a->prev;
		a->prev = temp;
		if(a->next != NULL)	{
			a->next->prev = a;
		}
		b->next->prev = b;
	}
}

void pairwise_node_swap(Node a,Node b)	{
	a->next = b->next;
	b->prev = a->prev;
	a->prev = b;
	b->next = a;
	if(a->next != NULL)	{
		a->next->prev = a;
	}
	if(b->prev != NULL)	{
		b->prev->next = b;
	}
}

int array_size(uint8_t *array)	{
	int i = 0;
	while(array[i] != END)	{
		i++;
	}
	return (i + 1);
}

Head clone(Head h)	{
	Head tmp = new_bs_head();
	Node curr = h->start;
	while(curr != NULL)	{
		if(tmp->start == NULL)	{
			tmp->start = tmp->end = clone_node(curr);
		} else {
			tmp->end->next = clone_node(curr);
			tmp->end->next->prev = tmp->end;
			tmp->end = tmp->end->next;
		}
		curr = curr->next;
	}

	return tmp;
}

Node clone_node(Node n)	{
	Node tmp = malloc(sizeof(*tmp));
	memcpy(tmp,n,sizeof(*n));
	return tmp;
}

Head shift(Head var, int shift_size, char *shift_type)	{
	Head cloned_var  = clone(var);
	if(!strcmp(shift_type,"left"))	{
		left_shift(cloned_var,shift_size);
	} else if(!strcmp(shift_type,"right"))	{
		right_shift(cloned_var,shift_size);
	}
	return cloned_var;
}

Head right_shift(Head var, int shift_size)	{
	int size = var_size(var);
	int i;
	cut(var,size - shift_size, size - 1);
	for(i = 0; i < shift_size; i++)	{
		add(var,new_bs_node(0),"MSB");
	}
	return NULL;
}

Head left_shift(Head var, int shift_size)	{
	int size = var_size(var);
	int i;
	cut(var,0,shift_size - 1);
	for(i = 0; i < shift_size; i++)	{
		add(var,new_bs_node(0),"LSB");
	}
	return var;
}

Head cut(Head var, int start, int end)	{
	Node start_node = get(var,start);
	Node end_node = get(var,end);
	Node temp;
	if(end_node->next != NULL)	{
		end_node->next->prev = start_node->prev;
	} else {
		var->end = start_node->prev;
	}
	if(start_node->prev != NULL)	{
		start_node->prev->next = end_node->next;
	} else {
		var->start = end_node->next;
	}
	while(start_node != end_node)	{
		temp = start_node->next;
		free(start_node);
		start_node = temp;
	}
	return var;
}


void key_table_init()	{

	KEY_SEED[0][0] = KEY_SEED0;
	KEY_SEED[0][1] = KEY_SEED1;
	KEY_SEED[0][2] = KEY_SEED2;
	KEY_SEED[0][3] = KEY_SEED3;
	KEY_SEED[0][4] = KEY_SEED4;
	KEY_SEED[0][5] = KEY_SEED5;
	KEY_SEED[0][6] = KEY_SEED6;
	KEY_SEED[0][7] = KEY_SEED7;
	KEY_SEED[0][8] = KEY_SEED8;
	KEY_SEED[0][9] = KEY_SEED9;
	KEY_SEED[0][10] = KEY_SEED10;
	KEY_SEED[0][11] = KEY_SEED11;
	KEY_SEED[0][12] = KEY_SEED12;
	KEY_SEED[0][13] = KEY_SEED13;
	KEY_SEED[0][14] = KEY_SEED14;
	KEY_SEED[0][15] = KEY_SEED15;
	KEY_SEED[0][16] = KEY_SEED16;
	KEY_SEED[0][17] = KEY_SEED17;
	KEY_SEED[0][18] = KEY_SEED18;
	KEY_SEED[0][19] = KEY_SEED19;
	KEY_SEED[0][20] = KEY_SEED20;
	KEY_SEED[0][21] = KEY_SEED21;
	KEY_SEED[0][22] = KEY_SEED22;
	KEY_SEED[0][23] = KEY_SEED23;
	KEY_SEED[0][24] = KEY_SEED24;
	KEY_SEED[0][25] = KEY_SEED25;
	KEY_SEED[0][26] = KEY_SEED26;
	KEY_SEED[0][27] = KEY_SEED27;
	KEY_SEED[0][28] = KEY_SEED28;
	KEY_SEED[0][29] = KEY_SEED29;
	KEY_SEED[0][30] = KEY_SEED30;
	KEY_SEED[0][31] = KEY_SEED31;
	KEY_SEED[0][32] = KEY_SEED32;
	KEY_SEED[0][33] = KEY_SEED33;
	KEY_SEED[0][34] = KEY_SEED34;
	KEY_SEED[0][35] = KEY_SEED35;
	KEY_SEED[0][36] = KEY_SEED36;
	KEY_SEED[0][37] = KEY_SEED37;
	KEY_SEED[0][38] = KEY_SEED38;
	KEY_SEED[0][39] = KEY_SEED39;
	KEY_SEED[0][40] = KEY_SEED40;
	KEY_SEED[0][41] = KEY_SEED41;
	KEY_SEED[0][42] = KEY_SEED42;
	KEY_SEED[0][43] = KEY_SEED43;
	KEY_SEED[0][44] = KEY_SEED44;
	KEY_SEED[0][45] = KEY_SEED45;
	KEY_SEED[0][46] = KEY_SEED46;
	KEY_SEED[0][47] = KEY_SEED47;
	KEY_SEED[0][48] = KEY_SEED48;
	KEY_SEED[0][49] = KEY_SEED49;
	KEY_SEED[0][50] = KEY_SEED50;
	KEY_SEED[0][51] = KEY_SEED51;
	KEY_SEED[0][52] = KEY_SEED52;
	KEY_SEED[0][53] = KEY_SEED53;
	KEY_SEED[0][54] = KEY_SEED54;
	KEY_SEED[0][55] = KEY_SEED55;
	KEY_SEED[0][56] = KEY_SEED56;
	KEY_SEED[0][57] = KEY_SEED57;
	KEY_SEED[0][58] = KEY_SEED58;
	KEY_SEED[0][59] = KEY_SEED59;
	KEY_SEED[0][60] = KEY_SEED60;
	KEY_SEED[0][61] = KEY_SEED61;
	KEY_SEED[0][62] = KEY_SEED62;
	KEY_SEED[0][63] = KEY_SEED63;
	// KEY_SEED[0][64] = END;

	KEY_SEED[1][0] = KEY_SEED64;
	KEY_SEED[1][1] = KEY_SEED65;
	KEY_SEED[1][2] = KEY_SEED66;
	KEY_SEED[1][3] = KEY_SEED67;
	KEY_SEED[1][4] = KEY_SEED68;
	KEY_SEED[1][5] = KEY_SEED69;
	KEY_SEED[1][6] = KEY_SEED70;
	KEY_SEED[1][7] = KEY_SEED71;
	KEY_SEED[1][8] = KEY_SEED72;
	KEY_SEED[1][9] = KEY_SEED73;
	KEY_SEED[1][10] = KEY_SEED74;
	KEY_SEED[1][11] = KEY_SEED75;
	KEY_SEED[1][12] = KEY_SEED76;
	KEY_SEED[1][13] = KEY_SEED77;
	KEY_SEED[1][14] = KEY_SEED78;
	KEY_SEED[1][15] = KEY_SEED79;
	KEY_SEED[1][16] = KEY_SEED80;
	KEY_SEED[1][17] = KEY_SEED81;
	KEY_SEED[1][18] = KEY_SEED82;
	KEY_SEED[1][19] = KEY_SEED83;
	KEY_SEED[1][20] = KEY_SEED84;
	KEY_SEED[1][21] = KEY_SEED85;
	KEY_SEED[1][22] = KEY_SEED86;
	KEY_SEED[1][23] = KEY_SEED87;
	KEY_SEED[1][24] = KEY_SEED88;
	KEY_SEED[1][25] = KEY_SEED89;
	KEY_SEED[1][26] = KEY_SEED90;
	KEY_SEED[1][27] = KEY_SEED91;
	KEY_SEED[1][28] = KEY_SEED92;
	KEY_SEED[1][29] = KEY_SEED93;
	KEY_SEED[1][30] = KEY_SEED94;
	KEY_SEED[1][31] = KEY_SEED95;
	KEY_SEED[1][32] = KEY_SEED96;
	KEY_SEED[1][33] = KEY_SEED97;
	KEY_SEED[1][34] = KEY_SEED98;
	KEY_SEED[1][35] = KEY_SEED99;
	KEY_SEED[1][36] = KEY_SEED100;
	KEY_SEED[1][37] = KEY_SEED101;
	KEY_SEED[1][38] = KEY_SEED102;
	KEY_SEED[1][39] = KEY_SEED103;
	KEY_SEED[1][40] = KEY_SEED104;
	KEY_SEED[1][41] = KEY_SEED105;
	KEY_SEED[1][42] = KEY_SEED106;
	KEY_SEED[1][43] = KEY_SEED107;
	KEY_SEED[1][44] = KEY_SEED108;
	KEY_SEED[1][45] = KEY_SEED109;
	KEY_SEED[1][46] = KEY_SEED110;
	KEY_SEED[1][47] = KEY_SEED111;
	KEY_SEED[1][48] = KEY_SEED112;
	KEY_SEED[1][49] = KEY_SEED113;
	KEY_SEED[1][50] = KEY_SEED114;
	KEY_SEED[1][51] = KEY_SEED115;
	KEY_SEED[1][52] = KEY_SEED116;
	KEY_SEED[1][53] = KEY_SEED117;
	KEY_SEED[1][54] = KEY_SEED118;
	KEY_SEED[1][55] = KEY_SEED119;
	KEY_SEED[1][56] = KEY_SEED120;
	KEY_SEED[1][57] = KEY_SEED121;
	KEY_SEED[1][58] = KEY_SEED122;
	KEY_SEED[1][59] = KEY_SEED123;
	KEY_SEED[1][60] = KEY_SEED124;
	KEY_SEED[1][61] = KEY_SEED125;
	KEY_SEED[1][62] = KEY_SEED126;
	KEY_SEED[1][63] = KEY_SEED127;

	STATE_SEED[0] = STATE_SEED0;
	STATE_SEED[1] = STATE_SEED1;
	STATE_SEED[2] = STATE_SEED2;
	STATE_SEED[3] = STATE_SEED3;
	STATE_SEED[4] = STATE_SEED4;
	STATE_SEED[5] = STATE_SEED5;
	STATE_SEED[6] = STATE_SEED6;
	STATE_SEED[7] = STATE_SEED7;
	STATE_SEED[8] = STATE_SEED8;
	STATE_SEED[9] = STATE_SEED9;
	STATE_SEED[10] = STATE_SEED10;
	STATE_SEED[11] = STATE_SEED11;
	STATE_SEED[12] = STATE_SEED12;
	STATE_SEED[13] = STATE_SEED13;
	STATE_SEED[14] = STATE_SEED14;
	STATE_SEED[15] = STATE_SEED15;
	STATE_SEED[16] = STATE_SEED16;
	STATE_SEED[17] = STATE_SEED17;
	STATE_SEED[18] = STATE_SEED18;
	STATE_SEED[19] = STATE_SEED19;
	STATE_SEED[20] = STATE_SEED20;
	STATE_SEED[21] = STATE_SEED21;
	STATE_SEED[22] = STATE_SEED22;
	STATE_SEED[23] = STATE_SEED23;
	STATE_SEED[24] = STATE_SEED24;
	STATE_SEED[25] = STATE_SEED25;
	STATE_SEED[26] = STATE_SEED26;
	STATE_SEED[27] = STATE_SEED27;
	STATE_SEED[28] = STATE_SEED28;
	STATE_SEED[29] = STATE_SEED29;
	STATE_SEED[30] = STATE_SEED30;
	STATE_SEED[31] = STATE_SEED31;
	STATE_SEED[32] = STATE_SEED32;
	STATE_SEED[33] = STATE_SEED33;
	STATE_SEED[34] = STATE_SEED34;
	STATE_SEED[35] = STATE_SEED35;
	STATE_SEED[36] = STATE_SEED36;
	STATE_SEED[37] = STATE_SEED37;
	STATE_SEED[38] = STATE_SEED38;
	STATE_SEED[39] = STATE_SEED39;
	STATE_SEED[40] = STATE_SEED40;
	STATE_SEED[41] = STATE_SEED41;
	STATE_SEED[42] = STATE_SEED42;
	STATE_SEED[43] = STATE_SEED43;
	STATE_SEED[44] = STATE_SEED44;
	STATE_SEED[45] = STATE_SEED45;
	STATE_SEED[46] = STATE_SEED46;
	STATE_SEED[47] = STATE_SEED47;
	STATE_SEED[48] = STATE_SEED48;
	STATE_SEED[49] = STATE_SEED49;
	STATE_SEED[50] = STATE_SEED50;
	STATE_SEED[51] = STATE_SEED51;
	STATE_SEED[52] = STATE_SEED52;
	STATE_SEED[53] = STATE_SEED53;
	STATE_SEED[54] = STATE_SEED54;
	STATE_SEED[55] = STATE_SEED55;
	STATE_SEED[56] = STATE_SEED56;
	STATE_SEED[57] = STATE_SEED57;
	STATE_SEED[58] = STATE_SEED58;
	STATE_SEED[59] = STATE_SEED59;
	STATE_SEED[60] = STATE_SEED60;
	STATE_SEED[61] = STATE_SEED61;
	STATE_SEED[62] = STATE_SEED62;
	STATE_SEED[63] = STATE_SEED63;

	// KEY_SEED[1][64] = END;
}
