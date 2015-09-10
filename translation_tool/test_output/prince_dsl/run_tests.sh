#!/bin/bash
make -C test_output/prince_dsl/
test_output/prince_dsl/./pOut 1 >> /dev/null

exit $?
