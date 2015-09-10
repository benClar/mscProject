#!/bin/bash
make -C test_output/general_dsl/
test_output/general_dsl/./pOut 1 >> /dev/null

exit $?
