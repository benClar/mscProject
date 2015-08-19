CFLAGS = -O3 -Wall -pedantic -std=c99 
INCS = /Users/benjaminclarke/Project/DSL/testing/v1/prince_dsl/prince_dsl.h /Users/benjaminclarke/Project/LIB/BS_LIB.h /Users/benjaminclarke/Project/DSL/testing/v1/prince_dsl/prince_dsl_tests.h
TARGET = /Users/benjaminclarke/Project/DSL/testing/v1/prince_dsl/prince_dsl_tests
SOURCES = /Users/benjaminclarke/Project/DSL/testing/v1/prince_dsl/prince_dsl.c $(TARGET).c /Users/benjaminclarke/Project/LIB/BS_LIB.c
EVAL_TARGET = /Users/benjaminclarke/Project/DSL/testing/v1/prince_dsl/prince_dsl_timer
EVAL_SOURCE = /Users/benjaminclarke/Project/DSL/testing/v1/prince_dsl/prince_dsl.c $(EVAL_TARGET).c /Users/benjaminclarke/Project/LIB/BS_LIB.c
EVAL_INCS = /Users/benjaminclarke/Project/DSL/testing/v1/prince_dsl/prince_dsl.h /Users/benjaminclarke/Project/LIB/BS_LIB.h /Users/benjaminclarke/Project/DSL/testing/v1/prince_dsl/prince_dsl_timer.h
CC = gcc
all: $(TARGET)

$(TARGET):  $(SOURCES) $(INCS)
	$(CC) $(SOURCES) -o /Users/benjaminclarke/Project/DSL/testing/v1/prince_dsl/pOut  $(CFLAGS) $(LIBS)

eval: $(EVAL_TARGET)
$(EVAL_TARGET):  $(EVAL_SOURCE) $(EVAL_INCS)
	$(CC) $(EVAL_SOURCE) -o evalOut  $(CFLAGS) $(LIBS)

