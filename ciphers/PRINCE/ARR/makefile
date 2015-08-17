CFLAGS = -O4 -Wall -pedantic -std=c99 
INCS = ../../../LIB/BS_LIB.h prince.h prince_tests.h
TARGET = prince_tests
SOURCES = ../../../LIB/BS_LIB.c prince.c $(TARGET).c
EVAL_TARGET = prince_timer
EVAL_SOURCES = prince.c $(EVAL_TARGET).c ../../../LIB/BS_LIB.c
EVAL_INCS = prince.h prince_timer.h
CC = gcc
all: $(TARGET)

$(TARGET) $(SOURCES):  $(INCS)
	$(CC) $(SOURCES) -o pOut  $(CFLAGS) $(LIBS)

eval: $(EVAL_TARGET)
$(EVAL_TARGET) $(EVAL_SOURCES):  $(EVAL_INCS)
	$(CC) $(EVAL_SOURCES) -o evalOut  $(CFLAGS) $(LIBS)
