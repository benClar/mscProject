CFLAGS = -O3 -Wall -pedantic -std=c99 
INCS = general_dsl.h ../../out/BS_LIB.h general_dsl_tests.h
TARGET = general_dsl_tests
SOURCES = $(TARGET).c ../../out/BS_LIB.c general_dsl.c
CC = gcc
all: $(TARGET)

$(TARGET) $(SOURCES):  $(INCS)
	$(CC) $(SOURCES) -o pOut  $(CFLAGS) $(LIBS)


clean:
	rm -f $(TARGET)

run: all
	$(TARGET) 
