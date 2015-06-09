CFLAGS = -O4 -Wall -pedantic -std=c99 
INCS = dsl_lib.h prince.h prince_tests.h
TARGET = prince
SOURCES = dsl_lib.c prince_tests.c $(TARGET).c 
CC = gcc
all: $(TARGET)

$(TARGET) $(SOURCES):  $(INCS)
	$(CC) $(SOURCES) -o pOut  $(CFLAGS) $(LIBS)


clean:
	rm -f $(TARGET)

run: all
	$(TARGET) 
