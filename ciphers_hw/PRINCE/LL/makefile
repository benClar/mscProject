CFLAGS = -O4 -Wall -pedantic -std=c99 
INCS = prince.h
TARGET = prince
SOURCES = $(TARGET).c 
CC = gcc
all: $(TARGET)

$(TARGET) $(SOURCES):  $(INCS)
	$(CC) $(SOURCES) -o pOut  $(CFLAGS) $(LIBS)


clean:
	rm -f $(TARGET)

run: all
	$(TARGET) 
