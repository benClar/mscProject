CFLAGS = -O3 -Wall -pedantic -std=c99 
INCS = /Users/benjaminclarke/Project/DSL/testing/general_dsl/general_dsl.h /Users/benjaminclarke/Project/LIB/BS_LIB.h /Users/benjaminclarke/Project/DSL/testing/general_dsl/general_dsl_tests.h
TARGET = /Users/benjaminclarke/Project/DSL/testing/general_dsl/general_dsl_tests
SOURCES = $(TARGET).c /Users/benjaminclarke/Project/LIB/BS_LIB.c /Users/benjaminclarke/Project/DSL/testing/general_dsl/general_dsl.c
CC = gcc
all: $(TARGET)

$(TARGET) $(SOURCES):  $(INCS)
	$(CC) $(SOURCES) -o /Users/benjaminclarke/Project/DSL/testing/general_dsl/pOut  $(CFLAGS) $(LIBS)


clean:
	rm -f $(TARGET)

run: all
	$(TARGET) 
