CFLAGS = -O4 -Wall -pedantic -std=c99 
INCS = lfsr.h lfsr_tests.h
TARGET = lfsr_tests
SOURCES =  lfsr.c $(TARGET).c ../../../LIB/BS_LIB.c
CC = gcc
all: $(TARGET)

$(TARGET) $(SOURCES):  $(INCS)
	$(CC) $(SOURCES) -o pOut  $(CFLAGS) $(LIBS)


clean:
	rm -f $(TARGET)

run: all
	$(TARGET) 
