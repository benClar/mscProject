CFLAGS = -O4 -Wall -pedantic -std=c99 
INCS = prince_dsl.h
TARGET = prince_dsl
SOURCES = $(TARGET).c ../../LIB/BS_LIB.c
CC = gcc
all: $(TARGET)

$(TARGET) $(SOURCES):  $(INCS)
	$(CC) $(SOURCES) -o pOut  $(CFLAGS) $(LIBS)


clean:
	rm -f $(TARGET)

run: all
	$(TARGET) 
