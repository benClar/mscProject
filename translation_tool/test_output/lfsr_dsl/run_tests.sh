#!/bin/bash
make -C test_output/lfsr_dsl/
test_output/lfsr_dsl/./pOut 1 >> /dev/null

exit $?
