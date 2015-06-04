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

int main()	{
	KEY_SEED = (uint8_t**) malloc(2*sizeof(uint8_t*));
	KEY_SEED[0] = malloc(64*sizeof(uint8_t));
	KEY_SEED[1] = malloc(64*sizeof(uint8_t));

	uint8_t seed[10] = {1,2,3,4,5,6,7,8,9,10};

	Head *key = malloc(3*sizeof(key));
	key_table_init();
	key[0] = new_bs_var(64,KEY_SEED[0]);
	key[1] = new_bs_var(64,KEY_SEED[1]);

	Head cloned_key = clone(key[0]);
	print_var(cloned_key);
	cut(cloned_key,0,63);
	print_var(cloned_key);
	// swap_nodes(cloned_key,cloned_key->start,cloned_key->end);
	// swap_nodes(cloned_key,cloned_key->start->next,cloned_key->end->prev);
	// swap_nodes(cloned_key,cloned_key->start->next->next,cloned_key->end->prev->prev);
	// print_var(cloned_key);
	// size(cloned_key);
	// printf("===\n");
	// reverse(cloned_key,0,63);
	// reverse(cloned_key,5,10);
	// reverse(cloned_key,0,64);
	// Head testVar = new_bs_var(10,seed);
	// print_var(testVar);
	// rotate_right(testVar,1,9);

	return 0;
}

Head rotate_left(Head var, int shift, int size)    {
	Head cloned_var = clone(var);
	reverse(cloned_var, 0, size);
	reverse(cloned_var, 0, size - shift);
    reverse(cloned_var, size - shift + 1, size);
    return cloned_var;
}

Head rotate_right(Head var, int shift, int size)    {
	Head cloned_var = clone(var);
	reverse(cloned_var, 0, shift);
	reverse(cloned_var, shift + 1, size);
    return cloned_var;
}

Head reverse(Head var, int start, int end)	{
		printf("%d \n",start);
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
			h->end = h->start = new_bs_node();
			h->start->bit = seed_table[node_count];
		} else {
			h->end->next = new_bs_node();
			h->end->next->bit = seed_table[node_count];
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

Node new_bs_node()	{
	Node n = (Node) malloc(sizeof(*n));
	n->next = NULL;
	n->prev = NULL;
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
	return 0;
}

Head left_shift(Head var, int shift_size)	{
	Head cloned_var  = clone(var);
	int size = var_size(cloned_var);
	get(var, size - shift_size);
	return cloned_var;
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

Head right_shift(Head var, int shift_size)	{
	return NULL;
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
	// KEY_SEED[1][64] = END;
}
// void generate_not_key(uint8_t **key)	{
// 	key[3] = rotate(KEY_SEED[0],1,64);
// }
