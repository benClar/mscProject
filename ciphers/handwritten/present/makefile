CFLAGS = -O3 -Wall -pedantic -std=c99 
INCS = debug.h present.h present_tests.h
TARGET = present_tests
SOURCES =  present.c $(TARGET).c ../../BS_LIB/BS_LIB.c
EVAL_TARGET = present_timer
EVAL_SOURCES = present.c $(EVAL_TARGET).c ../../BS_LIB/BS_LIB.c
EVAL_INCS = debug.h present.h present_timer.h
CC = gcc
all: $(TARGET)

$(TARGET):  $(SOURCES) $(INCS)
	$(CC) $(SOURCES) -o pOut  $(CFLAGS) $(LIBS)

eval: $(EVAL_TARGET)
$(EVAL_TARGET): $(EVAL_SOURCES) $(EVAL_INCS)
	$(CC) $(EVAL_SOURCES) -o evalOut  $(CFLAGS) $(LIBS)