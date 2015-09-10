#!/bin/bash
EXIT_CODES=(1 0 1 1 1 1)
make -C test_output/runtime_checks/
END=`expr ${#EXIT_CODES[@]} - 1`
for i in $(seq 0 $END); do 
	test_output/runtime_checks/./pOut $i 1 >> /dev/null
	if [[ ${EXIT_CODES[i]} != $? ]]; then
		echo "FAILED ON $i"
		exit 1
	fi
done

exit 0
