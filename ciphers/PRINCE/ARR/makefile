CFLAGS = -O4 -Wall -pedantic -std=c99 
INCS = ../../../LIB/BS_LIB.h prince.h prince_tests.h
TARGET = prince_tests
SOURCES = ../../../LIB/BS_LIB.c prince.c $(TARGET).c 
CC = gcc
all: $(TARGET)

$(TARGET) $(SOURCES):  $(INCS)
	$(CC) $(SOURCES) -o pOut  $(CFLAGS) $(LIBS)


clean:
	rm -f $(TARGET)

run: all
	$(TARGET) 
