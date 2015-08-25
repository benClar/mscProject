CFLAGS = -O3 -Wall -pedantic -std=c99 
INCS = BS_LIB.h sbox.h poster_tests.h int_extraction.h bitsliced_bitwise.h
TARGET = poster_tests
SOURCES = $(TARGET).c BS_LIB.c sbox.c int_extraction.c bitsliced_bitwise.c
CC = gcc
all: $(TARGET)
$(TARGET):  $(SOURCES) $(INCS)
	$(CC) $(SOURCES) -o demo_out $(CFLAGS) $(LIBS)