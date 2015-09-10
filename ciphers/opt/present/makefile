CFLAGS = -O3 -Wall -pedantic -std=c99 
INCS = present_dsl.h ../../BS_LIB/BS_LIB.h present_dsl_tests.h
TARGET = present_dsl_tests
SOURCES = $(TARGET).c ../../BS_LIB/BS_LIB.c present_dsl.c
EVAL_TARGET = present_dsl_timer
EVAL_SOURCES = $(EVAL_TARGET).c ../../BS_LIB/BS_LIB.c present_dsl.c
EVAL_INCS = present_dsl.h ../../BS_LIB/BS_LIB.h present_dsl_timer.h
CC = gcc
all: $(TARGET)
$(TARGET):  $(SOURCES) $(INCS)
	$(CC) $(SOURCES) -o pOut  $(CFLAGS) $(LIBS)
eval: $(EVAL_TARGET)
$(EVAL_TARGET):  $(EVAL_SOURCES) $(EVAL_INCS)
	$(CC) $(EVAL_SOURCES) -o evalOut  $(CFLAGS) $(LIBS)