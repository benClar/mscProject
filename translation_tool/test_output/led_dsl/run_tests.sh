#!/bin/bash
make -C test_output/led_dsl/
test_output/led_dsl/./pOut 1 >> /dev/null

exit $?
