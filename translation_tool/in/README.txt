This directory contains working DSL source code
that evidences that achieved functionality of 
this project.
Files and included functionality are as follows:
##################################
######Critical functionality######
##################################
	-LED.dsl : DSL for standard expression of LED
	encryption algorithm
	-PRINCE.dsl : DSL for standard expression of PRINCE
	encryption algorithm
	-PRESENT.dsl : DSL for standard expression of PRESENT 
	encryption algorithm
	LFSR.dsl : DSL for standard expression of LFSR (minimum
	project success criteria)
	-errors.dsl : Demonstration of semantic error output
	-sbox.dsl : Demonstration of declaration and use of
	SBOX.
##################################
####Non-Critical functionality####
##################################
	-int_extraction.dsl : Demonstration of intuitive standard
	integer operations
	general.dsl : Demonstrates the following functionality (Evidence
		that this works is included in testing suite 
		Test_suites.test_general_operations()):
		-Setting and selecting single standard int bits(int_index_set_1())
		-Setting list of int bits(int_index_set_2())
		-Rotating subsets of bits(int_index_set_4())
		-Setting Int bits with Sequence of Bits literal(int_index_set_7())
		-Shift operations on selection of a subset of standard int bits(int_index_set_5(), 
		 int_index_set_4())
		-Range operations on standard integer bits (int_index_set_6())
		-implicit casting of sequence of bits to integer (seq_bit_arth(), int_index_set_8())
		-permuting int bits with list index notation
		-Bit-sliced addition, substraction & multiplication (bs_arith_add(), 
	     bs_arith_sub(), bs_mult_sub())
		-return bit-sliced integers(int_index_set_14())
		-casting standard bits to bit-sliced bits(int_index_set_14())
		-Multiple dimension bit sequences declarations (seq_bit_extraction())
		-Multiple dimension bit sequences setting (seq_bit_extraction())
		-More complex standard integer expressions with bit-sequences and
	     rotations(int_index_set_10())
		-bitwise operations on bits (bs_bit_expr_cast(), bit_to_bs_bit_set())
		-bitwise operations on sequences of bits (bit_seq_expr_to_bs())
		-declaring multiple dimension sequences and initialising with nested
		sequence values(int_seq_decl())
		- expressions on selection of subset of bit-sliced bits 
		 (bs_seq_bit_expr_mult())
