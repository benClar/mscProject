To build and run the correctness testing suite (*_tests.c files):

	make all
	./pOut

To build and run the performance evaluation suite (*_timer.c files):

	make eval
	./evalOut

Generated ciphers store data in a little-endian fashion 
(element 0 == LSB of test vectors), whilst handwritten 
ciphers store data in a big-endian fashion (element 
0 == MSB of test vector).