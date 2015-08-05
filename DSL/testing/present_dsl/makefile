CFLAGS = -O4 -Wall -pedantic -std=c99 
INCS = /Users/benjaminclarke/Project/DSL/testing/present_dsl/present_dsl.h /Users/benjaminclarke/Project/LIB/BS_LIB.h
TARGET = /Users/benjaminclarke/Project/DSL/testing/present_dsl/present_dsl
SOURCES = $(TARGET).c /Users/benjaminclarke/Project/LIB/BS_LIB.c
CC = gcc
all: $(TARGET)

$(TARGET) $(SOURCES):  $(INCS)
	$(CC) $(SOURCES) -o /Users/benjaminclarke/Project/DSL/testing/present_dsl/pOut  $(CFLAGS) $(LIBS)


clean:
	rm -f $(TARGET)

run: all
	$(TARGET) 
