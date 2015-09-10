CFLAGS = -O3 -Wall -pedantic -std=c99 
INCS = lfsr.h lfsr_tests.h
TARGET = lfsr_tests
SOURCES =  lfsr.c $(TARGET).c ../../../LIB/BS_LIB.c
EVAL_TARGET = lfsr_timer
EVAL_SOURCES = lfsr.c $(EVAL_TARGET).c ../../../LIB/BS_LIB.c
EVAL_INCS = lfsr.h lfsr_timer.h
CC = gcc
all: $(TARGET)

$(TARGET): $(SOURCES) $(INCS)
	$(CC) $(SOURCES) -o pOut  $(CFLAGS) $(LIBS)

eval: $(EVAL_TARGET)

$(EVAL_TARGET): $(EVAL_SOURCES) $(EVAL_INCS)
	$(CC) $(EVAL_SOURCES) -o evalOut  $(CFLAGS) $(LIBS) 
