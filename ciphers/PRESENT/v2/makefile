CFLAGS = -O4 -Wall -pedantic -std=c99 
INCS = debug.h present.h present_tests.h
TARGET = present_tests
SOURCES =  present.c $(TARGET).c ../../../LIB/BS_LIB.c
CC = gcc
all: $(TARGET)

$(TARGET) $(SOURCES):  $(INCS)
	$(CC) $(SOURCES) -o pOut  $(CFLAGS) $(LIBS)


clean:
	rm -f $(TARGET)

run: all
	$(TARGET) 
