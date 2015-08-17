CFLAGS = -O3 -Wall -pedantic -std=c99 
INCS = /Users/benjaminclarke/Project/DSL/testing/led_dsl/led_dsl.h /Users/benjaminclarke/Project/LIB/BS_LIB.h /Users/benjaminclarke/Project/LIB/BS_LIB.h /Users/benjaminclarke/Project/DSL/testing/led_dsl/led_dsl_tests.h
TARGET = /Users/benjaminclarke/Project/DSL/testing/led_dsl/led_dsl_tests
SOURCES = /Users/benjaminclarke/Project/DSL/testing/led_dsl/led_dsl.c $(TARGET).c /Users/benjaminclarke/Project/LIB/BS_LIB.c
EVAL_TARGET = /Users/benjaminclarke/Project/DSL/testing/led_dsl/led_timer
EVAL_SOURCES = $(EVAL_TARGET).c /Users/benjaminclarke/Project/LIB/BS_LIB.c /Users/benjaminclarke/Project/DSL/testing/led_dsl/led_dsl.c
EVAL_INCS = /Users/benjaminclarke/Project/DSL/testing/led_dsl/led_dsl.h /Users/benjaminclarke/Project/LIB/BS_LIB.h /Users/benjaminclarke/Project/LIB/BS_LIB.h /Users/benjaminclarke/Project/DSL/testing/led_dsl/led_timer.h
CC = gcc
all: $(TARGET)
$(TARGET) $(SOURCES):  $(INCS)
	$(CC) $(SOURCES) -o /Users/benjaminclarke/Project/DSL/testing/led_dsl/pOut  $(CFLAGS) $(LIBS)

eval: $(EVAL_TARGET)
$(EVAL_TARGET) $(EVAL_SOURCES):  $(EVAL_INCS)
	$(CC) $(EVAL_SOURCES) -o /Users/benjaminclarke/Project/DSL/testing/led_dsl/evalOut  $(CFLAGS) $(LIBS)
