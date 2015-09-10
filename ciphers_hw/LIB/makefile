CFLAGS = -O4 -Wall -pedantic -std=c99 
INCS = dsl_lib.h
TARGET = dsl_lib
SOURCES = $(TARGET).c 
CC = gcc
all: $(TARGET)

$(TARGET) $(SOURCES):  $(INCS)
	$(CC) $(SOURCES) -o pOut  $(CFLAGS) $(LIBS)


clean:
	rm -f $(TARGET)

run: all
	$(TARGET) 
