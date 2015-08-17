CFLAGS = -O3 -Wall -pedantic -std=c99 
INCS = /Users/benjaminclarke/Project/DSL/testing/present_dsl/present_dsl.h /Users/benjaminclarke/Project/LIB/BS_LIB.h /Users/benjaminclarke/Project/DSL/testing/present_dsl/present_dsl_tests.h
TARGET = /Users/benjaminclarke/Project/DSL/testing/present_dsl/present_dsl_tests
SOURCES = $(TARGET).c /Users/benjaminclarke/Project/LIB/BS_LIB.c /Users/benjaminclarke/Project/DSL/testing/present_dsl/present_dsl.c
EVAL_TARGET = /Users/benjaminclarke/Project/DSL/testing/present_dsl/present_dsl_timer
EVAL_SOURCES = $(EVAL_TARGET).c /Users/benjaminclarke/Project/LIB/BS_LIB.c /Users/benjaminclarke/Project/DSL/testing/present_dsl/present_dsl.c
EVAL_INCS = /Users/benjaminclarke/Project/DSL/testing/present_dsl/present_dsl.h /Users/benjaminclarke/Project/LIB/BS_LIB.h /Users/benjaminclarke/Project/DSL/testing/present_dsl/present_dsl_timer.h
CC = gcc
all: $(TARGET)
$(TARGET) $(SOURCES):  $(INCS)
	$(CC) $(SOURCES) -o /Users/benjaminclarke/Project/DSL/testing/present_dsl/pOut  $(CFLAGS) $(LIBS)
eval: $(EVAL_TARGET)
$(EVAL_TARGET) $(EVAL_SOURCES):  $(EVAL_INCS)
	$(CC) $(EVAL_SOURCES) -o /Users/benjaminclarke/Project/DSL/testing/present_dsl/evalOut  $(CFLAGS) $(LIBS)