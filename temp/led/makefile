CFLAGS = -O4 -Wall -pedantic -std=c99 
INCS = led_old.h ../../ciphers/LIB/dsl_lib.h
TARGET = led_old
SOURCES = ../../ciphers/LIB/dsl_lib.c $(TARGET).c 
CC = gcc
all: $(TARGET)

$(TARGET) $(SOURCES):  $(INCS)
	$(CC) $(SOURCES) -o pOut  $(CFLAGS) $(LIBS)


clean:
	rm -f $(TARGET)

run: all
	$(TARGET) 
