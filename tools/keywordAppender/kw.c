#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "kw.h"

int main(int argc, char *argv[])	{

	int start = atoi(argv[1]);
	int end = atoi(argv[2]);
	int i, print;
	for(i = 0, print = end; i < 64; i++, print++)	{
		printf("#define STATE_SEED%d %d \n ",i,i);
	}
}
