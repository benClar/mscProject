CFLAGS = -O3 -Wall -pedantic -std=c99 
INCS = lfsr_dsl.h ../../out/BS_LIB.h lfsr_dsl_tests.h
TARGET = lfsr_dsl_tests
SOURCES = $(TARGET).c ../../out/BS_LIB.c lfsr_dsl.c
EVAL_TARGET = lfsr_dsl_timer
EVAL_SOURCES = $(EVAL_TARGET).c ../../out/BS_LIB.c lfsr_dsl.c
EVAL_INCS = lfsr_dsl.h ../../out/BS_LIB.h lfsr_dsl_timer.h
CC = gcc
all: $(TARGET)

$(TARGET):  $(SOURCES) $(INCS)
	$(CC) $(SOURCES) -o pOut  $(CFLAGS) $(LIBS)

eval: $(EVAL_TARGET)
$(EVAL_TARGET):  $(EVAL_SOURCES) $(EVAL_INCS)
	$(CC) $(EVAL_SOURCES) -o evalOut  $(CFLAGS) $(LIBS) 
