CFLAGS = -O3 -Wall -pedantic -std=c99 
INCS = led_dsl.h ../../out/BS_LIB.h led_dsl_tests.h
TARGET = led_dsl_tests
SOURCES = led_dsl.c $(TARGET).c ../../out/BS_LIB.c
EVAL_TARGET = led_dsl_timer
EVAL_SOURCES = $(EVAL_TARGET).c ../../out/BS_LIB.c led_dsl.c
EVAL_INCS = led_dsl.h ../../out/BS_LIB.h led_dsl_timer.h
CC = gcc
all: $(TARGET)
$(TARGET):  $(SOURCES) $(INCS)
	$(CC) $(SOURCES) -o pOut  $(CFLAGS) $(LIBS)

eval: $(EVAL_TARGET)
$(EVAL_TARGET):  $(EVAL_SOURCES) $(EVAL_INCS)
	$(CC) $(EVAL_SOURCES) -o evalOut  $(CFLAGS) $(LIBS)
