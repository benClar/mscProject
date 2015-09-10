#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "run_time_errors_dsl_tests.h"

int main(int argc, char *argv[]) {
	if(!strcmp(argv[1], "0"))	{
		Error_1();
	} else if (!strcmp(argv[1], "1")){
		Non_Error_2();
	} else if (!strcmp(argv[1], "2")){
		Error_3();
	} else if(!strcmp(argv[1], "3")) {
		Error_4();
	} else if(!strcmp(argv[1], "4")) {
		Error_5();
	} else if(!strcmp(argv[1], "5"))	{
		Error_6();
	}
	return 0;
}
