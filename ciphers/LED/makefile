CFLAGS = -O4 -Wall -pedantic -std=c99 
INCS = led.h ../../LIB/BS_LIB.h led_tests.h
TARGET = led_tests
SOURCES = ../../LIB/BS_LIB.c led.c $(TARGET).c
CC = gcc
all: $(TARGET)

$(TARGET) $(SOURCES):  $(INCS)
	$(CC) $(SOURCES) -o pOut  $(CFLAGS) $(LIBS)


clean:
	rm -f $(TARGET)

run: all
	$(TARGET) 
