#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "kw.h"

int main(int argc, char *argv[])	{

	int number = atoi(argv[1]);
	int start = atoi(argv[2]);
	char *word = argv[3];
	int i;
	for(i = 0; i < number; i++, start++)	{
		printf("STATE_SEED[%d] = STATE_SEED%d \n",i,i);
	}
}
