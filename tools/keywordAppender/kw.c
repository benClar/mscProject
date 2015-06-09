#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "kw.h"

int main(int argc, char *argv[])	{

	int start = atoi(argv[1]);
	int end = atoi(argv[2]);
	int i, print;
	for(i = 0, print = end; i < end; i++, print++)	{
		printf("M0_%d, ",i);
		if (!(i % 4) && i != 0)	{
			printf("\n");
		}
	}
}
