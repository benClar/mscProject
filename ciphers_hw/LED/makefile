CFLAGS = -O3 -Wall -pedantic -std=c99 
INCS = led.h ../../LIB/BS_LIB.h led_tests.h
TARGET = led_tests
SOURCES = ../../LIB/BS_LIB.c led.c $(TARGET).c
EVAL_TARGET = led_timer
EVAL_SOURCES = ../../LIB/BS_LIB.c led.c $(EVAL_TARGET).c
EVAL_INCS = ../../LIB/BS_LIB.h led.h led_timer.h
CC = gcc
all: $(TARGET)
$(TARGET): $(SOURCES) $(INCS)
	$(CC) $(SOURCES) -o pOut  $(CFLAGS) $(LIBS)

eval: $(EVAL_TARGET)
$(EVAL_TARGET):	$(EVAL_SOURCES) $(EVAL_INCS)
	$(CC) $(EVAL_SOURCES) -o evalOut  $(CFLAGS) $(LIBS)

