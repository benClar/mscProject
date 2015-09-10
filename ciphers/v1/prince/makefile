CFLAGS = -O3 -Wall -pedantic -std=c99 
INCS = prince_dsl.h ../../BS_LIB/BS_LIB.h prince_dsl_tests.h
TARGET = prince_dsl_tests
SOURCES = prince_dsl.c $(TARGET).c ../../BS_LIB/BS_LIB.c
EVAL_TARGET = prince_dsl_timer
EVAL_SOURCE = prince_dsl.c $(EVAL_TARGET).c ../../BS_LIB/BS_LIB.c
EVAL_INCS = prince_dsl.h ../../BS_LIB/BS_LIB.h prince_dsl_timer.h
CC = gcc
all: $(TARGET)

$(TARGET):  $(SOURCES) $(INCS)
	$(CC) $(SOURCES) -o pOut  $(CFLAGS) $(LIBS)

eval: $(EVAL_TARGET)
$(EVAL_TARGET):  $(EVAL_SOURCE) $(EVAL_INCS)
	$(CC) $(EVAL_SOURCE) -o evalOut  $(CFLAGS) $(LIBS)

