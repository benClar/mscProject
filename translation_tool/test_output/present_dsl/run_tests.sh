#!/bin/bash
make -C test_output/present_dsl/
test_output/present_dsl/./pOut 1 >> /dev/null

exit $?
