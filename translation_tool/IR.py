from DATA_TYPE import DATA_TYPE
from pyparsing import ParseException
import random
from quine_mccluskey.qm import QuineMcCluskey
import itertools
from Translation_exceptions import SemanticException, InternalException, Unimplemented_functionality_errors
import sys

class Sym_count(object):
    """Stores a count of the number of temporary variables created."""
    def __init__(self):
        self.count = 0


class IR(object):
    """Stores IR nodes."""

    def __init__(self):
        self._IR = []
        self.sym_count = Sym_count()

    def add(self, node):
        self.IR.append(node)

    @property
    def IR(self):
        return self._IR

    def translate(self):
        """Iterates through all IR nodes and stores their code emissions"""
        result = {'main': "", 'header': ""}
        try:
            for node in self.IR:
                node_res = node.translate(self.sym_count)
                if 'emit' in node_res:
                    result['main'] += node_res['emit']
                else:
                    result['main'] += node_res
                if node.node_type == DATA_TYPE.FUNC_DECL:
                    result['header'] += node.translate_header(self.sym_count) + ";\n"
                elif node.node_type == DATA_TYPE.SBOX_DECL:
                    result['header'] += node.translate_header(self.sym_count)
            return result
        except Exception as details:
            Unimplemented_functionality_errors.functionality_err(node, details)


class Function_decl(object):
    """Intermediate Representation node that stores function declaration statements."""

    def __init__(self, ID, return_type):
        self._ID = Name(ID, None)
        self._return_value = return_type
        self._parameters = []
        self._body = []
        self._node_type = DATA_TYPE.FUNC_DECL
        self.return_param = None

    @property
    def return_type(self):
        """Accessor for node return type."""
        if self._return_value == DATA_TYPE.VOID:
            return DATA_TYPE.VOID
        else:
            return self._return_value.ID.type

    @property
    def return_value(self):
        """Accessor for node representing return type of function."""
        return self._return_value

    @property
    def parameters(self):
        """Accessor for node parameters."""
        return self._parameters

    @property
    def body(self):
        """Accessor for statement nodes making up function body."""
        return self._body

    @property
    def node_type(self):
        """Accessor for node_type"""
        return self._node_type

    @property
    def ID(self):
        return self._ID

    def translate(self, sym_count):
        """Translates node.

        Args:
        sym_count"""
        ret = ""
        ret += self.translate_header(sym_count)
        body_result = self.translate_body(sym_count)
        ret = body_result['emit'] + ret
        ret += body_result['result']
        ret += "}\n"
        return ret

    def translate_header(self, sym_count):
        """Translates the header of the function node
        Args:
        sym_count: Count of temp vars in the program"""
        if self.return_value == DATA_TYPE.VOID:
            return "void " + self.translate_name() + self.translate_parameters(sym_count)
        elif self.return_value.node_type == DATA_TYPE.BS_INT_DECL:
            self.return_param = Target_factory.name(sym_count, "bs_return")
            return "void " + " " + self.translate_name() + self.translate_parameters(sym_count, "uint32_t *" + self.return_param) + self.translate_dimensions()
        else:
            return self.return_value.translate_type() + " " + self.translate_name() + self.translate_parameters(sym_count) + self.translate_dimensions()

    def translate_dimensions(self):
        """Translate any required dimensions for header"""
        ret = ""
        return_type = self.return_value.ID.type
        if DATA_TYPE.is_seq_type(return_type):
            # ret += ")"
            for i, dim in enumerate(self.return_value.size):
                if (return_type == DATA_TYPE.SEQ_BIT_VAL) and (i == (len(self.return_value.size) - 1)):
                    break
                if i == 0:
                    ret += ")"
                else:
                    ret += "[" + dim.translate()['result'] + "]"
            if return_type == DATA_TYPE.BS_SEQ_INT_VAL:
                ret += "[" + self.return_value.constraints.value + "]"
        return ret

    def translate_body(self, sym_count):
        """Translates statements making up the body of function.

        Args:
        sym_count: Count of temp vars in program"""
        result = {'emit': "", 'result': ""}
        result['result'] += "{ \n"
        for stmt in self.body:
            if stmt.node_type == DATA_TYPE.SBOX_DECL:
                result['emit'] += stmt.translate(sym_count)
            else:
                if stmt.node_type == DATA_TYPE.RETURN_STMT:
                    stmt.return_target = self.return_param
                statement = stmt.translate(sym_count)
                if 'emit' in statement:
                    result['result'] += statement['emit']
                    result['result'] += statement['result']
                else:
                    result['result'] += statement
                if DATA_TYPE.is_op_type(stmt.node_type) or DATA_TYPE.is_operand(stmt.node_type):
                    result['result'] += ";\n"
                # except TypeError:
                    # result['result'] += stmt.translate(sym_count)['emit']
        # print(result)
        return result

    def translate_parameters(self, sym_count, bs_bit_return=None):
        """Translates parameter declarations in function header

        Args:
        sym_count: count of temp vars in program.
        bs_bit_return: True if function returns a bit variable."""

        ret = "("
        if bs_bit_return is not None:
            ret += bs_bit_return + ", "
        for p in self.parameters:
            # print(p.node_type)
            if p.node_type != DATA_TYPE.SBOX_DECL:
                ret += p.translate(sym_count, True)
                ret = ret[:-2]
                ret += ", "
        if len(self.parameters) > 0:
            ret = ret[:-2]
        elif bs_bit_return is not None:
            ret = ret[:-2]
        ret += ")"
        return ret

    def translate_name(self):
        """Translates function name, adding any extra syntax if arrays are being returns."""
        try:
            return_type = self.return_value.ID.type
        except AttributeError:
            return_type = self.return_value
        if DATA_TYPE.is_seq_type(return_type):
            return "(" + "*" + self.ID.translate()["result"]
        elif return_type == DATA_TYPE.INT_VAL or return_type == DATA_TYPE.BIT_VAL or return_type == DATA_TYPE.BS_INT_VAL or return_type == DATA_TYPE.BS_BIT_VAL:
            return self.ID.translate()['result']
        elif return_type == DATA_TYPE.VOID:
            return self.ID.translate()['result']
        else:
            raise ParseException("Internal error: Unknown return type")


class If_stmt(object):
    """Intermediate Representation node that stores if statement"""

    def __init__(self, condition, body=None):
        self._condition = condition
        self._body = []
        self.node_type = DATA_TYPE.IF_STMT

    @property
    def condition(self):
        """Accessor for condition field"""
        return self._condition

    @property
    def body(self):
        """Accessor for body"""
        return self._body

    def add_stmt(self, stmt):
        """Adds stament to function.

        Args:
        stmt:adds new statement to if statement sequentially."""
        self._body.append(stmt)

    def translate(self, sym_count):
        """translates if statement.

        Args:
        sym_count: count of temp vars in program"""
        result = {'emit': "", 'result': ""}
        condition_result = self.condition.translate(sym_count)
        result['emit'] += condition_result['emit']
        result['emit'] += "if" + condition_result['result'] + " { \n"
        result['emit'] += self.translate_body(sym_count)
        result['emit'] += "} \n"
        return result['emit']

    def translate_body(self, sym_count):
        """Translates body of if statement

        Args:
        sym_count: count of temp vars in program."""
        ret = ""
        for stmt in self.body:
            ret += stmt.translate(sym_count)
        return ret


class Element_range(object):
    """Stores element ranges"""

    node_type = DATA_TYPE.INDEX_RANGE

    def __init__(self, start, finish):
        self._start = start
        self._finish = finish
        self.type = None

    @property
    def start(self):
        """Starting element in range"""
        return self._start

    @property
    def finish(self):
        """Ending element in range"""
        return self._finish

    def is_literal(self):
        """Returns true if range is made up of literals"""
        if self.start.node_type == DATA_TYPE.INT_LITERAL and self.finish.node_type == DATA_TYPE.INT_LITERAL:
            return True
        return False

    def translate_size(self, sym_count):
        """translates size of range.

        Args:
        sym_count: Number of temp vars in program."""
        result = {'emit': "", 'result': ""}
        result['result'] = Target_factory.name(sym_count, "rnge_size")
        start = self.start.translate(sym_count)
        end = self.finish.translate(sym_count)
        result['emit'] += "uint32_t " + result['result'] + " = 0;\n"
        result['emit'] += start['emit']
        result['emit'] += end['emit']
        result['emit'] += result['result'] + " = (" + end['result'] + "-" + start['result'] + ") + 1;\n"
        return result


class Cast(object):
    """Stores cast operations and provides helper functions for casting."""

    def __init__(self, c_op, c_target):
        self._cast_target = c_target
        self._cast_op = c_op
        self.node_type = DATA_TYPE.CAST

    def translate(self):
        """Translates cast operation"""
        return self.operation.translate(self.target)

    @property
    def type(self):
        """type of cast"""
        return self._cast_op.type

    @property
    def target(self):
        """Target of cast"""
        return self._cast_target

    @property
    def operation(self):
        """Cast operation node: stores details of cast"""
        return self._cast_op

    @property
    def constraints(self):
        """Any constraints specified in cast"""
        return self._cast_op.constraints

    def bit_seq_to_int_val(target, sym_count):
        """Casts bit sequence to int value.

        Args:
        target: target node for cast.
        sym_count: count of temporary targets in cast."""
        result = {'emit': "", 'result': ""}
        # if target.node_type
        if DATA_TYPE.is_op_type(target.node_type):
            op = target.translate(sym_count)
            result['result'] += op['result']
            result['emit'] += op['emit']
        elif target.node_type == DATA_TYPE.SEQ_VAL:
            Cast.bit_seq_val_to_int_val(result, target, sym_count)
        elif target.type == DATA_TYPE.SEQ_BIT_VAL:
            return target.translate(sym_count)
        else:
            raise InternalException("unimplemented bit sequence cast on " + str(target.node_type))
        return result

    def bit_seq_val_to_int_val(result, target, sym_count):
        """Creates variable to represent bit sequence.

        Args:
        target: target of set.
        sym_count: number of temp vars in sequence"""
        result['result'] += Target_factory.name(sym_count, "casted_bit_seq")
        result['emit'] += Target_factory.type_decl_lookup[Target_factory.round_up_constraints(len(target.value))] + result['result'] + " = 0;\n"
        for pos, bit in enumerate(reversed(target.value)):
            bit_res = bit.translate(sym_count)
            result['emit'] += bit_res['emit']
            if bit_res['result'] == "0x1":
                result['emit'] += result['result'] + " |= 0x1 << " + str(pos) + ";\n"
            elif bit_res['result'] == "0x0":
                pass
            else:
                result['emit'] += "if(" + bit_res['result'] + " == 0x1){\n"
                result['emit'] += result['result'] + " |= 0x1 << " + str(pos) + ";\n"
                result['emit'] += "}\n"
            # else:
            #     raise InternalException("Unknown Value in Bit Sequence " + str(bit_res['result']))

    def int_to_bs_cast(sym_count, target, size=None):
        """Translates integers to bitsliced integers.
        Args:
            sym_count: count of temp vars in program.
            target: target of cast.
            size: bit width of cast."""
        result = {'emit': "", 'result': ""}
        result['result'] = Target_factory.name(sym_count, "casted_bs")
        result['emit'] += "uint32_t " + result['result'] + "[" + size + "]" + ";\n"
        result['emit'] += "int_to_bitsliced(" + result['result'] + ", " + target + ", " + size + ");\n"
        return result

    def bitslice_literal(sym_count, value, size, target=None):
        """Optimised bit-sliced of an integer literal.

        Args:
            sym_count: Count of temporary vars in program.
            value: value to be cast.
            size: size of cast.
            target: target variable for the cast result to be stored."""
        result = {'emit': "", 'result': ""}
        if target is None:
            result['result'] = Target_factory.name(sym_count, "casted_bs")
            result['emit'] = "uint32_t " + result['result'] + "[" + size + "]" + ";\n"
        else:
            result['result'] = target
        for bit in range(0, int(size)):
            if (int(value) >> bit) & 0x1 == 0:
                result['emit'] += result['result'] + "[" + str(bit) + "]" + "= 0;\n"
            elif (int(value) >> bit) & 0x1 == 1:
                result['emit'] += result['result'] + "[" + str(bit) + "]" + "= 0xffffffff;\n"
            else: 
                raise InternalException("Unknown bit val " + str(int(value) >> bit))
        return result

    def bit_to_bs_bit(value, sym_count):
        """Casts standard bit to bit-sliced bit
        Args:
            value: Value to be cast
            sym_count: number of temporary vars in program"""
        result = {'emit': '', 'result': ''}
        val_out = value.translate(sym_count)
        if val_out['result'] == "0x1":
            result['result'] = "0xffffffff"
        elif val_out['result'] == "0x0":
            result['result'] = "0x0"
        else:
            result['result'] = Target_factory.name(sym_count, "casted_bit")
            result['emit'] += val_out['emit']
            result['emit'] += "uint32_t " + result['result'] + " = 0;\n"
            result['emit'] += "if(" + val_out['result'] + " == 0x1){\n"
            result['emit'] += result['result'] + " = 0xffffffff;\n"
            result['emit'] += "} else if(" + val_out['result'] + " != 0x0){\n"
            result['emit'] += 'fprintf(stderr, "Unrecognised bit value to cast.\\n");\n'
            result['emit'] += "exit(1);\n"
            result['emit'] += "}\n"
        # else:
        #     raise ParseException("Internal error: Unknown bit value")
        return result

    def int_val_to_seq_bit(value, sym_count):
        """Casts integer value to sequence of bits
        Args:
            value: value to be cast.
            sym_count: number of temporary vars in progam."""
        return value.translate(sym_count)


class Index_select(object):
    """Node storing index selection operator on targets"""

    def __init__(self, target, indices, output_type=None):
        self.target = target
        self.indices = indices
        self.node_type = DATA_TYPE.INDEX_SELECT
        if output_type is None:
            self._type = self.target.type
        else:
            self._type = output_type

    @property
    def size(self):
        """Size of the index select node target"""
        return self.target.size

    def translate(self, sym_count):
        """Translates index select node as r-value.

        Args:
            sym_count: count of temporary variables in program"""
        result = {'emit': "", 'result': ""}
        if self.target.type == DATA_TYPE.SBOX_DECL:
            sbox_lookup = self.sbox_lookup_translate(sym_count)
            result['emit'] += sbox_lookup['emit']
            result['result'] = sbox_lookup['result']
        else:
            self.run_time_safety_checks(sym_count, result)
            target_result = self.target.translate()
            result['emit'] += target_result['emit']
            extracted_sequence = self.extract_sequence(target_result['result'], sym_count)
            if 'res_size' in extracted_sequence:
                result['res_size'] = extracted_sequence['res_size']
            result['emit'] += extracted_sequence['emit']
            result['result'] = extracted_sequence['result']
        return result

    def run_time_safety_checks(self, sym_count, result):
        """Includes run time safety checks in index ranges for variables that cannot be checked at compile time.

        Args:
            sym_count: Number of temp vars in program.
            result: storage for emitted code."""
        if self.is_range():
            if self.indices[-1][-1].start.node_type != DATA_TYPE.INT_LITERAL or self.indices[-1][-1].finish.node_type != DATA_TYPE.INT_LITERAL:
                start = self.indices[-1][-1].start.translate(sym_count)
                end = self.indices[-1][-1].finish.translate(sym_count)
                if self.indices[-1][-1].start.node_type != DATA_TYPE.INT_LITERAL:
                    self.var_in_bounds(sym_count, self.indices[-1][-1].start, result, self.target.dimension(len(self.indices[-1]) - 1))
                if self.indices[-1][-1].finish.node_type != DATA_TYPE.INT_LITERAL:
                    self.var_in_bounds(sym_count, self.indices[-1][-1].finish, result, self.target.dimension(len(self.indices[-1]) - 1))
                result['emit'] += end['emit']
                result['emit'] += start['emit']
                result['emit'] += "if(" + start['result'] + " > " + end['result'] + "){\n"
                result['emit'] += 'fprintf(stderr, "Start of range cannot be larger than end for index select on ' + self.target.translate()['result']+ ' \\n");\n'
                result['emit'] += "exit(1);\n"
                result['emit'] += "}\n"
        for i, dim in enumerate(self.indices):
            for index in dim:
                if index.node_type != DATA_TYPE.INT_LITERAL and index.node_type != DATA_TYPE.INDEX_RANGE:
                    self.var_in_bounds(sym_count, index, result, self.target.dimension(i))

    def var_in_bounds(self, sym_count, var, result, bound):
        """Checks that given variable is inside bounds of target variable

        Args:
            Sym_count: Number of temp vars in program.
            var: Index variable to be bound checked.
            result: storage for emitted code
            dim: dimension that var relates to."""
        var = var.translate(sym_count)
        result['emit'] += var['emit']
        result['emit'] += "if(" + var['result'] + " >= " + bound + "){\n"
        result['emit'] += 'fprintf(stderr, "Index out of bounds for selection on ' + self.target.translate()['result'] + '\\n");\n'
        result['emit'] += "exit(1);\n"
        result['emit'] += "}\n"


    def sbox_lookup_translate(self, sym_count):
        """Translate sbox lookup, placing bits through boolean functions.

        Args:
            sym_count: count of temp vars in program"""
        result = {'emit': "", 'result': ""}
        assert len(self.indices) == 1, "Sbox looks can only ever be one dimensional"
        index_result = self.indices[-1][-1].translate(sym_count)
        result['result'] = index_result['result']
        result['emit'] += index_result['emit']
        result['emit'] += self.target.translate(sym_count)['result'] + "(" + index_result['result'] + ");\n"
        return result

    def translate_as_lhs(self, sym_count, value):
        """Translted index operator as l-value.

        Args:
            sym_count: Number of temp vars in program
            value: value that index operator target should be set to"""
        result = {'emit': "", 'result': ""}
        index_result = self.translate_selection_dim(sym_count)
        result['emit'] += index_result['emit']
        self.run_time_safety_checks(sym_count, result)
        if self.type == DATA_TYPE.BS_BIT_VAL:
            if 'res_size' in value:
                assert int(value['res_size']) == 1, "Assuming this is only a single element bitsliced integer"
                result['emit'] += self.target.translate()['result'] + index_result['result'] + "[" + self.indices[-1][-1].translate()['result'] + "]" + " = " + value['result'] + "[0];\n"
            else:
                result['emit'] += self.target.translate()['result'] + index_result['result'] + "[" + self.indices[-1][-1].translate()['result'] + "]" + " = " + value['result'] + ";\n"
        elif self.type == DATA_TYPE.SEQ_BS_BIT_VAL:
            self.translate_seq_bit_val_lhs(result, value, sym_count)
        elif self.type == DATA_TYPE.BS_INT_VAL:
            if int(self.constraints.translate()['result']) > 1:
                temp_starting_ele = Target_factory.name(sym_count, "bs_int_start")
                result['emit'] += "uint8_t " + temp_starting_ele + ";\n"
                # selection_dims = self.translate_selection_dim(sym_count)
                # result['emit'] += selection_dims['emit']
                result['emit'] += "for(" + temp_starting_ele + " = 0; " + temp_starting_ele + " < " + self.target.constraints.translate()['result'] + "; " + temp_starting_ele + "++){\n"
                result['emit'] += self.target.translate()['result'] + index_result['result'] + "[" + temp_starting_ele + "]" + " = " + value['result'] + "[" + temp_starting_ele + "];\n"
                result['emit'] += "}\n"
            else:
                #Avoid loop for 1 bit bs int vals
                # selection_dims = self.translate_selection_dim(sym_count)
                # result['emit'] += selection_dims['emit']
                result['emit'] += self.target.translate()['result'] + index_result['result'] + "[0] = " + value['result'] + "[0];\n"       
        elif self.type == DATA_TYPE.BIT_VAL:
            result['emit'] += self.set_int_bit_val(value, sym_count)['emit']
        elif self.type == DATA_TYPE.SEQ_BIT_VAL:
            result['emit'] += self.set_seq_bit_val(value, sym_count)['emit']
        elif self.type == DATA_TYPE.INT_VAL:
            result['emit'] += self.set_seq_int_val(value, sym_count)['emit']
        else:
            raise ParseException("Unsupported extraction on LHS " + str(self.type))
        return result

    def translate_seq_bit_val_lhs(self, result, value, sym_count):
        """Translates seq bit val index operator as l-value.

        Args:
            result: storage for emitted code.
            sym_count: Number of temp vars in program
            value: value that index operator target should be set to"""
        if self.is_range():
            if self.indices[-1][-1].is_literal():
                result['emit'] += self.literal_range_set(value, sym_count)
            else:
                self.list_lhs_seq_bs_bit(result, value, sym_count)
        else:
            selection_dims = self.translate_selection_dim(sym_count)
            result['emit'] += selection_dims['emit']
            for i, index in enumerate(self.indices[-1]):
                ele = index.translate(sym_count)
                result['emit'] += ele['emit']
                result['emit'] += self.target.translate()['result'] + selection_dims['result'] + "[" + ele['result'] + "]" + " = " + value['result'] + "[" + str(i) + "]" + ";\n"

    def list_lhs_seq_bs_bit(self, result, value, sym_count):
        """Translate a list of indexes on bitsliced bit as left hand side.

        Args:
            result:storage for emitted code
            value: value that is to be assigned to.
            sym_count:count of temp vars in program"""
        temp_init = Target_factory.name(sym_count, "init")
        temp_term = self.indices[-1][-1].translate_size(sym_count)
        result['emit'] += "uint8_t " + temp_init + " = 0;\n"
        result['emit'] += temp_term['emit']
        starting_ele = self.indices[-1][-1].start.translate(sym_count)  # Getting translation of starting element of range
        result['emit'] += starting_ele['emit']
        temp_starting_ele = Target_factory.name(sym_count, "rng_start")
        result['emit'] += "uint8_t " + temp_starting_ele + " = " + starting_ele['result'] + ";\n"  # Assigning starting element of range to temp variable for incrementing
        result['emit'] += "for(" + temp_init + " = 0; " + temp_init + " < " + temp_term['result'] + "; " + temp_init + "++, " + temp_starting_ele + "++){\n"
        selection_dims = self.translate_selection_dim(sym_count)
        result['emit'] += selection_dims['emit']
        result['emit'] += self.target.translate()['result'] + selection_dims['result'] + "[" + temp_starting_ele + "] = " + value['result'] + "[" + temp_init + "];\n"
        result['emit'] += "}\n" 

    def set_seq_int_val(self, value, sym_count):
        """Sets a sequence of integers to passed in value.

        Args:
            value: value to set
            sym_count: temp vars in program."""
        result = {'emit': "", 'result': ""}
        selection_dims = self.translate_selection_dim(sym_count)
        result['emit'] += selection_dims['emit']
        if self.is_range():
            raise ParseException("Ranges of int sequences not yet implemented")
        elif len(self.indices[-1]) > 1:
            raise ParseException("Ranges of int sequences not yet implemented")
        else:
            selection = self.indices[-1][-1].translate(sym_count)
            result['emit'] += selection['emit']
            result['emit'] += self.target.translate()['result'] + selection_dims['result'] + "[" + selection['result'] + "]" + " = " + value['result'] + ";\n"
        return result

    def set_seq_bit_val(self, value, sym_count):
        """Sets sequence of bits to passed in value.

        Args:
            value: Value to be set.
            sym_count: count of temp vars in program. """
        result = {'emit': "", 'result': ""}
        selection_dims = self.translate_selection_dim(sym_count)
        result['emit'] += selection_dims['emit']
        if self.is_range():
            self.range_int_bit_set(value, result, selection_dims, sym_count)
        elif len(self.indices[-1]) > 1:
            # Integer value as target
            for i, bit in enumerate(self.indices[-1]):
                self.set_bit(result, self.target.translate()['result'], str(i), bit.translate()['result'], value['result'], selection_dims)
        else:
            # Multi-dimensional Sequence of bits as target
            final_dim = self.indices[-1][-1].translate()
            result['emit'] += final_dim['emit']
            result['emit'] += self.target.translate()['result'] + selection_dims['result'] + "[" + final_dim['result'] + "]" + " = " + value['result'] + " & " + str(int("0b" + int(self.target.size[-1].translate(sym_count)['result']) * "1", 2)) + ";\n"
        return result

    def set_bit(self, result, target, source_bit, target_bit, value, selection_dim):
            """Set a specified bit on target variable from source variable.

            Args:
                result: storage for emitted code.
                target: Target var for setting bit.
                source_bit: bit position that target bit should be set to.
                target_bit: bit position that should be set in target bit.
                value: holds series of bits being copied to target.
                selection_dim: Any requied dimensions to access value"""
            result['emit'] += "if(((" + value + " >> " + source_bit + ") & 0x1) == 0 ){\n"
            result['emit'] += target + selection_dim['result'] + " &= ~(0x1 <<" + target_bit + ");\n"
            result['emit'] += "} else if (((" + value + " >> " + source_bit + ") & 0x1) == 1 ){\n"
            result['emit'] += target + selection_dim['result'] + " |= (0x1 << " + target_bit + ");\n"
            result['emit'] += "}\n"

    def range_int_bit_set(self, value, result, selection_dims, sym_count):
        """Sets bits in an integer range

        Args:
            value: value to set int bit to
            result: for storing code
            selection_dims: any dimensions required to select correct element
            sym_count: temp vars in program"""
        selection_dims = self.translate_selection_dim(sym_count)
        result['emit'] += selection_dims['emit']
        int_start_rng = self.indices[-1][-1].start.translate(sym_count)
        result['emit'] += int_start_rng['emit']
        int_end_rng = self.indices[-1][-1].finish.translate(sym_count)
        result['emit'] += int_end_rng['emit']
        range_size = self.indices[-1][-1].translate_size(sym_count)
        result['emit'] += range_size['emit']
        temp_starting_bit = Target_factory.name(sym_count, "rng_start")
        curr_bit = Target_factory.name(sym_count, "curr_bit")
        result['emit'] += "uint32_t " + curr_bit + ";\n"
        result['emit'] += "uint32_t " + temp_starting_bit + ";\n"
        result['emit'] += "for(" + curr_bit + " = " + int_start_rng['result'] + ", " + temp_starting_bit + " = 0; " + temp_starting_bit  + " < " + range_size['result'] + "; " + temp_starting_bit + "++, " + curr_bit + "++) {\n"
        self.set_bit(result, self.target.translate()['result'], temp_starting_bit, curr_bit, value['result'], selection_dims)
        result['emit'] += "}\n"

    def set_int_bit_val(self, value, sym_count):
        """Sets  bit in standard in.
        Args:
            value: value that int bit is to be set to.
            sym_count: count of vars in program"""
        result = {'emit': "", 'result': ""}
        selection_dims = self.translate_selection_dim(sym_count)
        result['emit'] += selection_dims['emit']
        if value['result'] == '0x1':
            result['emit'] += self.target.translate()['result'] + selection_dims['result'] + " ^= (0x1 << " + self.indices[-1][-1].translate()['result'] + ");\n"
        elif value['result'] == '0x0':
            result['emit'] += self.target.translate()['result'] + selection_dims['result'] + " &= ~(0x1 << " + self.indices[-1][-1].translate()['result'] + ");\n"
        else:
            result['emit'] += "if(" + value['result'] + ") {\n"
            result['emit'] += self.target.translate()['result'] + selection_dims['result'] + " ^= (0x1 << " + self.indices[-1][-1].translate()['result'] + ");\n"
            result['emit'] += "} else if(" + value['result'] + ") {\n"
            result['emit'] += self.target.translate()['result'] + selection_dims['result'] + " &= ~(0x1 << " + self.indices[-1][-1].translate()['result'] + ");\n}\n"
        return result


    def literal_range_set(self, value, sym_count):
        """Optimised set when literals have been used for range selectiong.

        Args:
            value:Value that selection is to be set to
            sym_count: count of temporary variables in program"""
        result = {'emit': "", 'result': ""}
        start_ele = int(self.indices[-1][-1].start.translate()['result'])
        end_ele = int(self.indices[-1][-1].finish.translate()['result']) + 1
        selection_dims = self.translate_selection_dim(sym_count)
        result['emit'] += selection_dims['emit']
        for i, ele in enumerate(range(start_ele, end_ele)):
            result['emit'] += self.target.translate()['result'] + selection_dims['result'] + "[" + str(ele) + "]" + " = " + value['result'] + "[" + str(i) + "];\n"
        return result['emit']

    def extract_sequence(self, target, sym_count):
        """Extracts sequence from target

        Args:
            target: Target that sequence is to be extracted from.
            sym_count: count of temporary variables in program."""
        assert self.target.node_type == DATA_TYPE.ID, "Assumption target is just an ID at this point"
        if self.type == DATA_TYPE.BS_BIT_VAL:
            return self.extract_bs_int_bits(target, sym_count)
        elif self.type == DATA_TYPE.BS_INT_VAL:
            return self.extract_bs_int_val(target, sym_count)
        elif self.type == DATA_TYPE.SEQ_BS_BIT_VAL:
            return self.extract_bs_int_bits(target, sym_count)
        elif self.target.type == DATA_TYPE.SBOX_DECL:
            raise ParseException("Unsupport seq type extraction " + str(self.type) + " from " + str(self.target.type))
        elif (self.target.type == DATA_TYPE.INT_VAL or self.target.type == DATA_TYPE.SEQ_INT_VAL) and (self.type == DATA_TYPE.BIT_VAL or self.type == DATA_TYPE.SEQ_BIT_VAL):
            return self.extract_int_bits(target, sym_count)
        elif self.target.type == DATA_TYPE.SEQ_INT_VAL:
            return self.sequence_select(target, sym_count)
        elif self.target.type == DATA_TYPE.SEQ_BIT_VAL:
            return self.extract_seq_bit(target, sym_count)
        else:
            raise ParseException("Unsupport seq type extraction " + str(self.type) + " from " + str(self.target.type))

    def sequence_select(self, target, sym_count):
        """ Extracts sequence from int sequence

        Args:
            target: target of sequence select.
            sym_count: count of temp vars in program"""
        result = {'emit': "", 'result': ""}
        sel_dim = self.translate_selection_dim(sym_count)
        fin_index = self.indices[-1][-1].translate(sym_count)
        result['emit'] += sel_dim['emit'] + fin_index['emit']
        result['result'] = target + sel_dim['result'] + "[" + fin_index['result'] + "]"
        result['res_size'] = 1
        return result

    def extract_seq_bit(self, target, sym_count):
        """Index operation functionality on sequences of bits

        Args:
            target: target for bit select 
            sym_count: count of temp vars in program"""
        result = {'emit': "", 'result': ""}
        result['result'] += Target_factory.name(sym_count, "bit_extracted")
        result['emit'] += Target_factory.type_decl_lookup[Target_factory.round_up_constraints(len(self.indices[-1]))] + result['result'] + " = 0;\n"
        if self.is_range():
            raise ParseException("Unimplemented extraction on " + str(self.target.type))
        else:
            self.extract_list_bits(result, target, sym_count)
        return result

    def extract_list_bits(self, result, target, sym_count):
        """List or single index extraction

        result: for code emission
        target: Target to extract bits from
        sym_count: list of temp vars in program"""
        selection_dim = self.translate_selection_dim(sym_count)
        result['emit'] += selection_dim['emit']
        for pos, index in enumerate(self.indices[-1]):
            ins_translated = index.translate()
            result['emit'] += ins_translated['emit']
            result['emit'] += result['result'] + " |= ((" + target + selection_dim['result'] + " >> " + ins_translated['result'] + ") & 0x1 ) << " + str(pos) + ";\n"

    def extract_int_bits(self, target, sym_count):
        """extract bits from integers.

        Args:
            target: target for extraction
            sym_count: count of temp vars in program"""
        result = {'emit': "", 'result': ""}
        result['result'] = Target_factory.name(sym_count, "extracted")
        result['emit'] += Target_factory.type_decl_lookup[self.target.constraints.translate()['result']] + " " + result['result'] + " = 0;\n"
        selection_dim = self.translate_selection_dim(sym_count)
        result['emit'] += selection_dim['emit']
        if self.is_range():
            start_range_target = Target_factory.name(sym_count, "int_rng_start")
            end_range_target = Target_factory.name(sym_count, "int_rng_start")
            start_val = self.indices[-1][-1].start.translate()
            end_val = self.indices[-1][-1].finish.translate()
            result['emit'] += start_val['emit']
            result['emit'] += end_val['emit']
            result['emit'] += "uint8_t " + start_range_target + " " + " = " + start_val['result'] + ";\n"
            target_bit = Target_factory.name(sym_count, "target_bit")
            result['emit'] += Target_factory.type_decl_lookup[self.target.constraints.translate()['result']] + " " + target_bit + " = 0;\n"
            result['emit'] += "for(;" + start_range_target + " < " + end_val['result'] + ";" + start_range_target + "++, " + target_bit + "++){\n"
            result['emit'] += result['result'] + " |= " + "((" + target + selection_dim['result']+ " >> " + start_range_target + ") " + " << " + target_bit + ");\n"
            result['emit'] += "}\n"
        elif len(self.indices[-1]) == 1:
            selected_bit = self.indices[-1][-1].translate()
            result['emit'] += selected_bit['emit']
            result['emit'] += result['result'] + " = " + "(" + target + selection_dim['result'] + " >> " + selected_bit['result'] + ") & 0x1;\n"
        else:
            result['emit'] += self.extract_int_bit_seq(target, result['result'], sym_count, selection_dim['result'])
        return result

    def extract_int_bit_seq(self, target, temp_target, sym_count, selection_dim):
        """List index notation on integer values

        Args:
            target: node that holds value for extraction
            temp_target: target for extraction to be stored in
            sym_count: count for number of temp vars in program
            selection_dims: any required selection dimensions for extraction"""
        result = {'emit': "", 'result': ""}
        for i, bit in enumerate(self.indices[-1]):
            index_res = bit.translate(sym_count)
            result['emit'] += index_res['emit']
            result['emit'] += temp_target + " ^= (((" + target + selection_dim + " >> " + index_res['result'] + ") & 0x1) " + "<< " + str(i) + ");\n"
        return result['emit']

    def extract_bs_int_val(self, target, sym_count):
        """Extract entire bitsliced int from a sequence of bs ints.
        
        Args:
            target: target for extraction   
            sym_count: count of temp vars in program."""
        result = {'emit': "", 'result': ""}
        selection_dim = self.translate_selection_dim(sym_count)
        result['emit'] += selection_dim['emit']
        if len(self.indices[-1]) == 1:
            result['result'] = target + selection_dim['result']
        else:
            extracted_seq = Target_factory.name(sym_count, "extracted")
            result['res_size'] = self.target.constraints.translate()['result']
            result['emit'] += "uint32_t " + " " + extracted_seq + "[" + result['res_size'] + "];\n"
            result['result'] = extracted_seq

            for ele in range(int(result['res_size'])):
                result['emit'] += extracted_seq + "[" + str(ele) + "]" + " = " + target + selection_dim['result'] + "[" + str(ele) + "]" + ";\n"
        return result

    def extract_bs_int_bits(self, target, sym_count):
        """Extracting bits from bitsliced Int from single selector, range or list.

        Args:
            target: target for extraction.
            sym_count: count of temp vars in program."""
        result = {'emit': "", 'result': ""}
        if self.is_range():
            result = self.extract_range(sym_count, target)
            # print(result)
            # raise ParseException('extract')
        elif self.is_sequence():         
            extracted_seq = Target_factory.name(sym_count, "extracted")
            result['emit'] += "uint32_t " + " " + extracted_seq + "[" + str(len(self.indices[-1])) + "];\n"
            result['res_size'] = str(len(self.indices[-1]))
            result['result'] = extracted_seq
            selection_dim = self.translate_selection_dim(sym_count)
            result['emit'] += selection_dim['emit']
            for i, index in enumerate(self.indices[-1]):
                index_translation = index.translate(sym_count)
                result['emit'] += index_translation['emit']
                result['emit'] += extracted_seq + "[" + str(i) + "]" + " = " + target + selection_dim['result'] + "[" + index_translation['result'] + "]" + ";\n"
        else:
            selection_dim = self.translate_selection_dim(sym_count)
            result['emit'] += selection_dim['emit']
            index_translation = self.indices[-1][0].translate(sym_count)
            result['emit'] += index_translation['emit']
            result['result'] = target + selection_dim['result'] + "[" + index_translation['result'] + "]"
        return result

    def extract_range(self, sym_count, target):
        """Extract range from passed in value
        Args:
            sym_count: count of temp vars in program.
            target: target node for extraction."""
        if self.type == DATA_TYPE.SEQ_BS_BIT_VAL:
            return self.extract_bs_range(sym_count, target)
        else:
            raise ParseException("Unknown range type to create temporary variable for extraction " + self.type)

    def extract_bs_range(self, sym_count, target):
        """Extracts subset of bits from bitsliced integer.

        Args:
            sym_count: count of temporary variables in program
            target: target node for extraction """
        result = {'emit': "", 'result': "", 'res_size': ""}
        result['result'] = Target_factory.name(sym_count, "rnge")
        range_start = self.indices[-1][0].start.translate(sym_count)
        result['emit'] += range_start['emit']
        range_finish = self.indices[-1][0].finish.translate(sym_count)
        result['emit'] += range_finish['emit']
        result['res_size'] = "(" + range_finish['result'] + " - " + range_start['result'] + ") + 1"
        result['emit'] += Target_factory.type_decl_lookup[self.type] + " " + result['result'] + "[" + result['res_size'] + "]" + ";\n"
        selection_dim = self.translate_selection_dim(sym_count)
        result['emit'] += selection_dim['emit']
        result['emit'] += "extract_bs_range(" + result['result'] + ", " + target + selection_dim['result'] + ", " + range_start['result'] + ", " + range_finish['result'] + ");\n"
        return result

    def is_sequence(self):
        """ returns true if result of node is a sequence"""
        if len(self.indices[-1]) > 1:
            return True
        return False

    def is_range(self):
        """Returns true if  index is a range operation"""
        if self.indices[-1][-1].node_type == DATA_TYPE.INDEX_RANGE:
            assert len(self.indices[-1]) == 1, "Only single range contained in selection"
            return True
        else:
            return False

    def translate_target_size(self, sym_count):
        """Translates the size of the target.

        Args:
            sym_count: count of temp vars in program."""
        result = {'emit': "", 'result': ""}
        if self.indices[-1][-1].node_type == DATA_TYPE.INDEX_RANGE:
            target_start = self.indices[-1][-1].start.translate(sym_count)
            target_end = self.indices[-1][-1].finish.translate(sym_count)
            result['emit'] += target_start['emit']
            result['emit'] += target_end['emit']
            result['result'] = "(" + target_end['result'] + " - " + target_start['result'] + ") + 1"
        else:
            result['result'] = str(len(self.indices[-1]))
        return result

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    def translate_selection_dim(self, sym_count):
        """Translates all indices but the final one that selects element or bit

        Args:
            sym_count: Count of temporary variables in program."""
        result = {"emit": "", "result": ""}
        # print(self.target.type)
        for i, dim in enumerate(self.indices):
            if i == len(self.indices) - 1 and self.type != DATA_TYPE.BS_INT_VAL:
                return result
            # if i == len(self.indices) - 1 and self.target.type == DATA_TYPE.BS_SEQ_INT_VAL:
            #     return result
            dim = dim[0].translate(sym_count)
            result['emit'] += dim['emit']
            result['result'] += "[" + dim['result'] + "]"
        return result

    @property
    def constraints(self):
        """Returns constraints for target"""
        if self.target.node_type == DATA_TYPE.ID:
            return self.target.constraints
        else:
            raise ParseException("Constraints for target " + str(self.target.node_type) + " Not Supported")

    @property
    def name(self):
        assert self.target.node_type == DATA_TYPE.ID, "Should only be being used in set statement.  Only IDs can be set."
        return self.target.name


class Set(object):

    def __init__(self, target, value):
        self._target = target
        # self._ID = Name(var_id, id_type)
        self._value = value
        self.node_type = DATA_TYPE.ID_SET

    @property
    def target(self):
        return self._target

    @property
    def value(self):
        return self._value

    def translate(self, sym_count):
        """translates set node.

        Args:
            sym_count: Count of temp vars in program."""
        result = {'emit': "", 'result': ""}
        if self.target.node_type == DATA_TYPE.INDEX_SELECT:
            if DATA_TYPE.needs_cast(self.target.type, self.value.type):
                value_result = self.implicit_cast(sym_count)
                # result['emit'] += value_result['emit']
            else:
                value_result = self.value.translate(sym_count)
            result['emit'] += value_result['emit']
            assignment_result = self.translate_index_selection_set(sym_count, value_result)
            result['emit'] += assignment_result['emit']
        elif self.target.node_type == DATA_TYPE.ID:
            if self.value.node_type == DATA_TYPE.BITWISE_OP and self.value.can_be_optimised() and (self.value.type == self.target.type):
                result['emit'] += self.translate_optimised_bitwise_set(sym_count)['emit']
            else:
                if DATA_TYPE.needs_cast(self.target.type, self.value.type):
                    value_result = self.implicit_cast(sym_count)
                    result['emit'] += value_result['emit']
                else:
                    value_result = self.value.translate(sym_count)
                    result['emit'] += value_result['emit']
                    # raise ParseException(str(self.value.type) + " being assigned to a  " + str(self.target.type) + " : Cast needed")
                if self.target.type == DATA_TYPE.INT_VAL or self.target.type == DATA_TYPE.BS_BIT_VAL or self.target.type == DATA_TYPE.BIT_VAL:
                    self.translate_integer_set(result, value_result, sym_count)
                elif self.target.type == DATA_TYPE.BS_INT_VAL:
                    self.translate_bs_int_set(result, value_result, sym_count)
                elif self.target.type == DATA_TYPE.BS_SEQ_INT_VAL or self.target.type == DATA_TYPE.SEQ_INT_VAL:
                    pass
                elif self.target.type == DATA_TYPE.SEQ_BIT_VAL:
                    self.translate_seq_seq_bit_val(result, value_result, sym_count)
                else:
                    raise ParseException("Unrecognised Target type " + str(self.target.node_type))
        else:
            raise ParseException("Unrecognised set type " + str(self.target.node_type))
        return result['emit']

    def translate_seq_seq_bit_val(self, result, value_result, sym_count):
        """ID set of integer to bit sequence.

        Args:
        result: Storage for code.
        value_result: Value to set.
        sym_count: Temporary vars in program"""
        if self.value.type == DATA_TYPE.INT_VAL:
            result['emit'] += self.target.translate(sym_count)['result'] + " = " + value_result['result'] + " & " + str(int("0b" + int(self.target.size[-1].translate(sym_count)['result']) * "1", 2)) + ";\n"
        else:
            raise ParseException("Unrecognised bit seq set type: " + str(self.target.type))
        # print(result)


    def translate_optimised_bitwise_set(self, sym_count):
        """Calls an optimised bitwise set on appropriate binary operations."""
        return self.value.optimised_translate(self.target.translate()['result'], sym_count, self.target.constraints.translate()['result'])

    def implicit_cast(self, sym_count):
        """Implicitly casts value"""
        if self.target.type == DATA_TYPE.BS_INT_VAL:
            return self.implicit_cast_to_bs_int(sym_count)
        elif self.target.type == DATA_TYPE.SEQ_BS_BIT_VAL:
            return self.implicit_cast_to_bs_bits(sym_count)
        elif self.target.type == DATA_TYPE.INT_VAL:
            return self.implicit_cast_to_int_val(sym_count)
        elif self.target.type == DATA_TYPE.BS_BIT_VAL:
            return self.implicit_cast_to_bs_bit(sym_count)
        elif self.target.type == DATA_TYPE.SEQ_BIT_VAL:
            return self.implicit_cast_to_int_val(sym_count)
        elif self.target.type == DATA_TYPE.BS_SEQ_INT_VAL:
            return self.implicit_cast_to_bs_seq(sym_count)
        elif self.target.type == DATA_TYPE.SEQ_INT_VAL:
            return self.value.translate(sym_count, {'result': self.target.translate(sym_count)['result'], 'res_size': [int(i.translate(sym_count)['result']) for i in self.target.size]})
        else:
            raise ParseException(str(self.value.type) + " being assigned to a " + str(self.target.type) + " : Cast needed")

    def implicit_cast_to_bs_seq(self, sym_count):
        """Implicitly cast target to bitsliced sequence value"""
        size = []
        for dim in self.target.size:
            size.append(int(dim.translate()['result']))
        size.append(int(self.target.constraints.translate()['result']))
        return self.value.translate_bitsliced_seq_val(sym_count, size, self.target.translate()['result'])


    def implicit_cast_to_int_val(self, sym_count):
        """ """
        if self.value.type == DATA_TYPE.SEQ_BIT_VAL:
            return Cast.bit_seq_to_int_val(self.value, sym_count)
        if self.value.type == DATA_TYPE.INT_VAL:
            return Cast.int_val_to_seq_bit(self.value, sym_count)
        else:
            raise InternalException("Unsupported cast to int val " + str(self.value.type))

    def implicit_cast_to_bs_bit(self, sym_count):
        if self.target.type == DATA_TYPE.BS_BIT_VAL:
            return Cast.bit_to_bs_bit(self.value, sym_count)
        else:
           raise ParseException("Unsupported cast to bs bit of " + str(self.target.type)) 

    def implicit_cast_to_bs_bits(self, sym_count):
        """Cast to bit-sliced range"""
        result = {'emit': "", 'result': ""}
        if self.value.type == DATA_TYPE.SEQ_BIT_VAL or self.value.type == DATA_TYPE.INT_VAL:
            value = self.value.translate(sym_count)   # !Could optimise if this is an int literal
            result['emit'] += value['emit']
            casted_value = Target_factory.name(sym_count, "cast_bs_seq")
            target_size = self.target.translate_target_size(sym_count)
            result['emit'] += target_size['emit']
            result['emit'] += "uint32_t " + casted_value + "[" + target_size['result'] + "]" + ";\n"
            result['emit'] += "int_to_bitsliced(" + casted_value + ", " + value['result'] + ", " + target_size['result'] + ");\n"
            result['result'] = casted_value
        else:
            raise ParseException("Unsupported implicit cast to bs seq: " + str(self.value.type))
        return result

    def implicit_cast_to_bs_int(self, sym_count):
        """Cast to bit-sliced int.  Target is not an index select."""
        result = {'emit': "", 'result': ""}
        if self.value.type == DATA_TYPE.SEQ_BIT_VAL or self.value.type == DATA_TYPE.INT_VAL:
            if self.value.node_type == DATA_TYPE.INT_LITERAL and self.target.node_type == DATA_TYPE.ID:
                # if self.target.node_type == DATA_TYPE.ID:
                    # def bitslice_literal(sym_count, value, size, target = None):
                bitslice_cast = Cast.bitslice_literal(sym_count, self.value.translate(sym_count)['result'], self.target.constraints.translate()['result'], self.target.translate()['result'])
                result['emit'] += bitslice_cast['emit']
                result['result'] += bitslice_cast['result']
            else:
                bitslice_cast = self.run_time_bitslice(sym_count);
                result['emit'] += bitslice_cast['emit']
                result['result'] += bitslice_cast['result']
        else:
            raise ParseException("Unsupported implicit cast to bs int: " + str(self.value.type))
        return result

    def run_time_bitslice(self, sym_count):
        """Bitslice target at runtime"""
        result = {'emit': "", 'result': ""}
        value = self.value.translate(sym_count)
        result['emit'] += value['emit']
        casted_value = Target_factory.make_bs_target(Target_factory.name(sym_count, "cast_bs_val"), self.target.constraints)
        result['emit'] += casted_value['emit']
        result['emit'] += "int_to_bitsliced(" + casted_value['result'] + ", " + value['result'] + ", " + casted_value['res_size'] + ");\n"
        result['result'] = casted_value['result']
        return result

    def translate_index_selection_set(self, sym_count, value):
        """Translate index selection set, translating set as an l-value.

        Args:
            sym_count: count of temp vars in program.
            value: Value that index set is to be set to."""
        result = {'emit': "", 'result': ""}
        # return result and emitted code for assignment
        if self.target.type == DATA_TYPE.BS_BIT_VAL:
            # Single bitslice assignment
            target_result = self.target.translate_as_lhs(sym_count, value)
            result['emit'] += target_result['emit']
        elif self.target.type == DATA_TYPE.SEQ_BS_BIT_VAL:
            result['emit'] += self.target.translate_as_lhs(sym_count, value)['emit']
        elif self.target.type == DATA_TYPE.BS_INT_VAL:
            result['emit'] += self.target.translate_as_lhs(sym_count, value)['emit']
        elif self.target.type == DATA_TYPE.BIT_VAL:
            result['emit'] += self.target.translate_as_lhs(sym_count, value)['emit']
        elif self.target.type == DATA_TYPE.SEQ_BIT_VAL:
            result['emit'] += self.target.translate_as_lhs(sym_count, value)['emit']
        elif self.target.type == DATA_TYPE.INT_VAL:
            result['emit'] += self.target.translate_as_lhs(sym_count, value)['emit']
        else:
            raise ParseException("Unsupported index set : " + str(self.target.type))

        return result

    def translate_bs_int_set(self, result, value_result, sym_count):
        """Sets bitsliced integer value.

        args:
            result: storage for emitted code.
            value_result: Value to be used in set.
            sym_count: count of temp vars in program."""
        target_result = self.target.translate(sym_count)
        result['emit'] += target_result['emit']
        if self.value.node_type == DATA_TYPE.INT_LITERAL:
            return
        for i in range(int(self.target.constraints.value)):
            result['emit'] += target_result['result'] + "[" + str(i) + "]" + " = " + value_result['result'] + "[" + str(i) + "]" + ";\n"

    def translate_integer_set(self, result, value_result, sym_count):
        assert len(value_result) > 0
        target_result = self.target.translate(sym_count)
        result['emit'] += target_result['emit']
        result['emit'] += target_result['result'] + " = " + value_result['result'] + self.translate_index(0, value_result) + ";\n"

    def translate_index(self, ele, result):
        if 'res_size' in result:
            if result['res_size'] is not None:
                return "[" + str(ele) + "]"
        return ""


class Return(object):
    """IR for return statements"""

    def __init__(self, expr):
        self._target = expr
        self._type = expr.type
        self.node_type = DATA_TYPE.RETURN_STMT
        self.return_target = None

    @property
    def target(self):
        return self._target

    @property
    def type(self):
        return self._type

    def translate(self, sym_count):
        """translates return statement"""
        target = self.target.translate(sym_count)
        ret = target['emit']
        if self.return_target is not None:
            # Bitsliced return value needs to be set to passed in var before it goes out of scope
            for bit in range(0, int(self.target.constraints.translate()['result'])):
                ret += self.return_target + "[" + str(bit) + "] = " + target['result'] + "[" + str(bit) + "];\n"
            return ret
        else:
            return "return " + target['result'] + ";\n"


class Seq_decl(object):
    """IR for sequence declarations"""
    def __init__(self, node_type, size, var_id, value=None, constraints=None):
        self._ID = Name(var_id, DATA_TYPE.decl_to_value(node_type), size, constraints)
        self._node_type = node_type
        self._size = size
        self._value = value
        self._constraints = constraints
        if value is not None:
            self._body = Set(self.ID, self.value)
        else:
            self._body = None

    @property
    def body(self):
        return self._body

    @property
    def ID(self):
        return self._ID

    @property
    def node_type(self):
        return self._node_type

    @property
    def size(self):
        return self._size

    @property
    def value(self):
        return self._value

    @property
    def constraints(self):
        return self._constraints

    def translate(self, sym_count, func_param=False):
        """Translates declaration.  Will be translated differently is declaration is a function parameter.

        Args:
            sym_count: count of temp vars in program.
            func_param: true if declaration is a function parameter."""
        result = {'emit': "", 'result': ""}
        if func_param is True:
            self.translate_as_param(sym_count, result)
        else:
            self.translate_declaration(sym_count, result)
        if self.body is not None and self.node_type != DATA_TYPE.SBOX_DECL:
            if self.node_type == DATA_TYPE.BS_SEQ_INT_DECL:
                value = self.value.translate_bitsliced_seq_val(sym_count, self.translate_size_as_list(sym_count), self.ID.translate()['result'])
                result['emit'] += value['emit']
            elif self.value.node_type == DATA_TYPE.SEQ_VAL:
                value = self.value.translate(sym_count, {'result': self.ID.translate()['result'], 'res_size': self.translate_size_as_list(sym_count)})
                result['emit'] += value['emit']
            else:
                return self.body.translate(sym_count)
        return result['emit']

    def translate_as_param(self, sym_count, result):
        """Translates declaration as a parameter"""
        if self.node_type == DATA_TYPE.BS_SEQ_INT_DECL:
            result['emit'] += Target_factory.type_decl_lookup[self.ID.type] + " " + self.ID.translate()['result'] + self.translate_index() + ";\n"
        elif self.node_type == DATA_TYPE.SBOX_DECL:
            raise InternalException("Sbox cannot be function parameter")
        elif self.node_type == DATA_TYPE.SEQ_INT_DECL:
            result['emit'] += Target_factory.type_decl_lookup[self.constraints.translate()['result']] + " " + self.ID.translate()['result'] + self.translate_index() + ";\n"
        elif self.node_type == DATA_TYPE.SEQ_BIT_DECL:
            result['emit'] += Target_factory.type_decl_lookup[Target_factory.round_up_constraints(int(self.size[-1].translate()['result']))] + self.ID.translate()['result'] + self.translate_index() + ";\n"
        else:
            raise ParseException("Translation of Unknown Sequence Type as function parameter attempted: " + str(self.node_type))

    def translate_declaration(self, sym_count, result):
        """Translates sequence declaration as standard declaration"""
        if self.node_type == DATA_TYPE.BS_SEQ_INT_DECL:
            result['emit'] += Target_factory.type_decl_lookup[self.ID.type] + " " + self.ID.translate()['result'] + self.translate_index() + " = " + self.init_value() + ";\n"
        elif self.node_type == DATA_TYPE.SBOX_DECL:
            result['emit'] += self.translate_sbox_decl(sym_count)
        elif self.node_type == DATA_TYPE.SEQ_INT_DECL:
            result['emit'] += Target_factory.type_decl_lookup[self.constraints.translate()['result']] + " " + self.ID.translate()['result'] + self.translate_index() + " = " + self.init_value() + ";\n"
        elif self.node_type == DATA_TYPE.SEQ_BIT_DECL:
                result['emit'] += Target_factory.type_decl_lookup[Target_factory.round_up_constraints(int(self.size[-1].translate()['result']))] + self.ID.translate()['result'] + self.translate_index() + " = " + self.init_value() + ";\n"
        else:
            raise ParseException("Translation of Unknown Sequence Type as declaration attempted: " + str(self.node_type))   

    def translate_size_as_list(self, sym_count):
        """returns translated dimensions as a list of values
        Args:
            sym_count: count of temp vars in program"""
        size = []
        for dim in self.size:
            assert dim.node_type == DATA_TYPE.INT_LITERAL
            size.append(int(dim.translate(sym_count)['result']))
        if self.node_type == DATA_TYPE.BS_SEQ_INT_DECL:
            size.append(int(self.constraints.translate()['result']))
        return size

    def init_value(self):
        """Initializes declared array as per its dimensions"""
        if self.node_type == DATA_TYPE.BS_SEQ_INT_DECL:
            return (len(self.size) + 1) * "{" + " 0 " + (len(self.size) + 1) * "}"
        elif self.node_type == DATA_TYPE.SEQ_BIT_DECL:
            return (len(self.size) - 1) * "{" + " 0 " + (len(self.size) - 1) * "}"
        else:
            return len(self.size) * "{" + " 0 " + len(self.size) * "}"

    def translate_index(self):
        """Translates required dimensions for declaration"""
        index = ""
        for i_num, i in enumerate(self.size):
            if self.node_type == DATA_TYPE.SEQ_BIT_DECL and i_num == len(self.size) - 1:
                return index
            index += "[" + i.translate()['result'] + "]"
        if self.ID.type == DATA_TYPE.BS_SEQ_INT_VAL:
            index += "[" + self.constraints.translate()['result'] + "]"
        return index

    def translate_sbox_decl(self, sym_count):
        """Translates an sbox declaration into boolean functions"""
        result = {'emit': "", 'result': ""}
        v_name = self.ID.translate()["result"]
        p_list = ""
        sbox_output = Target_factory.make_bs_target(Target_factory.name(sym_count, "sbox_out"), self.constraints)
        result['emit'] += "void " + v_name + "(uint32_t input[" + self.constraints.translate()['result'] + "]){\n"
        result['emit'] += sbox_output['emit']
        result['result'] = sbox_output['result']
        # print(Target_factory.make_bs_target(result['result'], self.constraints))
        for i in range(0, int(self.constraints.translate()['result'])):
            for bit in range(0, int(self.constraints.translate()['result'])):
                p_list += "input[" + str(bit) + "], "
            p_list = p_list[:-2]
            result['emit'] += result['result'] + "[" + str(i) + "] = " + v_name + "_" + str(i) + "(" + p_list + ");\n"
            p_list = ""
        for i in range(0, int(self.constraints.translate()['result'])):
            result['emit'] += "input[" + str(i) + "] = " + result['result'] + "[" + str(i) + "];\n"
        result['emit'] += "}\n"
        result['emit'] = self.translate_qm(v_name) + result['emit']
        return result['emit']

    def translate_header(self, sym_count):
        """Translates header for sbox boolean function"""
        res = ""
        name = self.ID.translate()["result"]
        res += "void " + name + "(uint32_t input[" + self.constraints.translate()['result'] + "]);\n"
        for i in range(0, int(self.constraints.translate()['result'])):
            res += "uint32_t " + name + "_" + str(i) + "(uint32_t A, uint32_t B, uint32_t C, uint32_t D);\n"
        return res

    def translate_qm(self, name):
        """Uses QuineMcCluskey implementation to generate required boolean functions"""
        result = ""
        qm = QuineMcCluskey()
        for bit in range(0, 4):
            function = ""
            result += "uint32_t " + name + "_" + str(bit) + "(uint32_t A, uint32_t B, uint32_t C, uint32_t D) {\n"
            boolean_result = qm.simplify(ones=self.get_ones(bit))
            result += "return "
            for term in boolean_result:
                function += self.translate_term(term) + " | "
            function = function[:-3]
            result += "(" + function + ");\n}\n"
        return result

    def translate_term(self, term):
        """Parses quine mccluskey algorithm  output to produce boolean function for single term"""
        result = ""
        for i, bit in enumerate(("D", "C", "B", "A")):
            if term[i] == "1":
                result += bit + " & "
            elif term[i] == "0":
                result += "~" + bit + " & "
            elif term[i] == "-":
                pass
            else:
                raise ParseException("Internal Error: Unknown char in term")
        result = result[:-3]
        return "(" + result + ")"

    def get_ones(self, bit):
        ones = []
        for i, val in enumerate(self.value.value):
            if (int(val.translate()['result']) >> bit) & 0x1:
                ones.append(i)
        return ones

    def translate_bs_int_seq(self, sym_count):
        result = {'emit': "", 'result': ""}
        # target_result += self.translate_type() + self.ID.translate()["result"] + "[" + self.constraints.translate()['result'] + "]" + ";\n"
        # result['emit'] += target_result['emit']
        value_result = self.value.translate(sym_count)
        # target_result = 
        result['emit'] += value_result['emit']
        if DATA_TYPE.needs_cast(self.ID.type, self.value.type):
            if self.value.type == DATA_TYPE.SEQ_INT_VAL:
                self.int_seq_to_bs_int_seq(sym_count, value_result['result'], value_result['res_size'])
            else:
                raise ParseException("Cannot assign " + str(self.value.type) + " to " + str(self.value.node_type))

    def int_seq_to_bs_int_seq(self, sym_count, target, size):
        result = {'emit': "", 'result': ""}
        temp_target = Target_factory.name(sym_count, "bs_cast")
        result['emit'] += Target_factory.type_decl_lookup[self.ID.type] + " " + temp_target + self.size_to_index(size) + "[" + self.constraints.value + "]" + ";\n"
        select_elements = itertools.product(*map(range, size + [int(self.constraints.value)]))
        print(list(select_elements))

    def bitslice_int(self, target, value, size):
        ret = ""
        for bit in range(size):
            ret += target + "[" + str(bit) + "]" + " = " + "(" + value + " >> " + str(bit) + ")" + ";\n"
        return ret

    def size_to_index(self, size):
        index = ""
        for i in size:
            index += "[" + str(i) + "]"
        return index

    def translate_type(self):
        if self.node_type == DATA_TYPE.BS_SEQ_INT_DECL:
            return "uint32_t "
        elif self.node_type == DATA_TYPE.SEQ_BIT_DECL:
            return "uint8_t "
        else:
            if self.constraints.translate()['result'] not in Target_factory.type_decl_lookup:
                raise SemanticException("Custom sized integers not implemented")
            return Target_factory.type_decl_lookup[self.constraints.translate()]

class Seq_val(object):

    def __init__(self, s_type=None, value=None):
        self._value = []
        if value is not None:
            self._value.append(value)
        self.constraints = None
        self._type = s_type
        self.node_type = DATA_TYPE.SEQ_VAL
        self._dim_s = None
        self.indiv_size = []
        self.size = None

    @property
    def dim_s(self):
        return self._dim_s

    @dim_s.setter
    def dim_s(self, value):
        # if value > 1:
        #     self._dim_s = value - 1
        # else:
        self._dim_s = value 

    @property
    def value(self):
        return self._value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    def add_element(self, element):
        self._value.append(element)

    def translate_target_size(self, sym_count):
        return self.constraints.translate()

    def translate_bitsliced_seq_val(self, sym_count, size, target):
        """Translates sequence into bitsliced sequence

        sym_count: number of temp. variable in the program.
        size: size of target.
        target: id of target"""
        result = {'emit': "", 'result': ""}
        bs_perms = list(itertools.product(*map(range, size)))
        perms = list(itertools.product(*map(range, size[0:-1])))
        # print(list(itertools.product(*map(range, size[0:-1]))))

        for i in perms:
            ele = self.get_val(self.value, list(i)).translate(sym_count)
            index_str = ""
            for index in i:
                index_str += "[" + str(index) + "]"
            result['emit'] += ele['emit']
            result['emit'] += "int_to_bitsliced(" + target + index_str + ", " + ele['result'] + ", " + str(size[-1]) + ");\n"
        return result

    def translate(self, sym_count, target=None):
        result = {'emit': "", 'result': "", 'res_size' : None}
        # if self.all_int_literal():
        #     return self.translate_int_literal_seq(sym_count, result)
        if self.type == DATA_TYPE.SEQ_BIT_VAL:
            return self.translate_bit_val_seq(sym_count, target)
        elif self.type == DATA_TYPE.SEQ_INT_VAL:
            return self.int_val_seq(sym_count, target)
        else:
            raise ParseException("Unknown sequence value translation")

    def int_val_seq(self, sym_count, target=None):
        """Translates sequence value either to a given target or to a returns temporary variable
        Args:

        sym_count: number of temporary variables in program.
        target: passed in target for sequence value to be assigned to."""
        result = {'emit': "", 'result': "", 'res_size': None}
        if target is None:
            target = Target_factory.name(sym_count, "seq_val")
            result['result'] = target
            result['emit'] += "uint64_t " + target
            seq_dimension = self.dim_s
            self.get_seq_size(self.value)
            self.indiv_size.reverse()
            result['res_size'] = self.indiv_size
            for i in result['res_size']:
                result['emit'] += "[" + str(i) + "]"
            result['emit'] += ";\n"
            self.set_seq_val_to_target(sym_count, result, result['res_size'], target)     
        else:
            self.set_int_val_target(result, sym_count, target)
        return result

    def set_int_val_target(self, result, sym_count, target):
        self.set_seq_val_to_target(sym_count, result, target['res_size'], target['result'])

    def set_seq_val_to_target(self, sym_count, result, size, target):
        """Sets the current sequence value to a target array.

        Args:
        sym_count: number of temporary variables in program.
        result: Store emitted code and result.
        size: Size of target.
        target: target variable for result"""
        perms = list(itertools.product(*map(range, size)))
        for i in perms:
            index_str = ""
            for index in i:
                index_str += "[" + str(index) + "]"
            ele = self.get_val(self.value, list(i)).translate(sym_count)
            result['emit'] += ele['emit']
            result['emit'] += target + index_str + " = " + ele['result'] + ";\n"

    def translate_bit_val_seq(self, sym_count, target=None):
        """Translates a sequence bit value to variable

        Args:
        Sym_count : Number of temporary variables in program
        Target: target that translated bit sequence should be assigned to"""
        if target is None:
            return Cast.bit_seq_to_int_val(self, sym_count)
        else:
            return self.set_bit_seq_to_target(sym_count, target['res_size'], target['result'])

    def set_bit_seq_to_target(self, sym_count, size, target):
        """Sets sequence value to passed in result
        Args:
        sym_count: Number of temp. vars in program.
        size: size of array to set.
        target: target array to set."""
        perms = list(itertools.product(*map(range, size)))
        result = {'result': "", 'emit': ""}
        for index in perms:
            index_str = ""
            for dim, element in enumerate(index):
                if dim == len(index) - 1:
                    pass
                else:
                    index_str += "[" + str(element) + "]"
            element_res = self.get_val(self.value, list(index)).translate(sym_count)
            result['emit'] += element_res['emit']
            result['emit'] += target + index_str + " |= " + "(" + element_res['result'] + " << " + str(size[-1] - index[-1] - 1) + ");\n"  
        return result

    def get_val(self, target, index):
        if len(index) == 1:
            try:
                return target[index[0]]
            except IndexError:
                return Int_literal('0')
        else:
            try:
                return self.get_val(target[index.pop(0)].value, index)
            except IndexError:
                return Int_literal('0')

    def get_seq_size(self, seq):
        """Returns size of sequence.

        Args:
        Seq: Sequence to analyse"""
        index = None
        for index, ele in enumerate(seq):
            if ele.node_type == DATA_TYPE.SEQ_VAL:
                self.get_seq_size(ele.value)
        self.indiv_size.append(index + 1)

    def list_to_index(self, index_sel):
        index_str = ""
        for ele in index_sel:
            index_str += "[" + str(ele) + "]"
        return index_str


    def get_value(self, seq_value, dimension):
        if len(dimension) == 1:
            return seq_value[dimension[0]]
        else:
            current_dim = dimension.pop(0)
            return self.get_value(seq_value[current_dim], dimension)

    def translate_seq_size(self):
        dimensions = []
        size = 0
        if self.value[0].node_type == DATA_TYPE.SEQ_VAL:
            dimensions += self.value[0].translate_seq_size()
        for ele in self.value:
            size += 1
        dimensions = [size] + dimensions
        return dimensions



    def translate_type(self):
        Target_factory.type_decl_lookup[self.get_constraints()]

    def get_constraints(self):
        biggest = 0
        for ele in self.value:
            ele_width = int(ele.value).bit_length()
            if ele_width > biggest:
                biggest = ele_width
        return Target_factory.round_up_constraints(biggest)

    def all_int_literal(self):
        for ele in self.value:
            if ele.node_type is not DATA_TYPE.INT_LITERAL:
                return False
        return True


class Bit_decl(object):

    def __init__(self, var_id, bit_type, value=None):
        self._ID = var_id
        self._node_type = bit_type
        self._value = value
        if value is not None:
            self._body = Set(self.ID, self.value)
        else:
            self._body = None

    @property
    def body(self):
        return self._body

    @property
    def node_type(self):
        return self._node_type

    @property
    def value(self):
        return self._value

    @property
    def ID(self):
        return self._ID

    def translate_type(self):
        if self.node_type == DATA_TYPE.BS_BIT_DECL:
            return "uint32_t "
        elif self.node_type == DATA_TYPE.BIT_DECL:
            return "uint8_t "
        else:
            raise InternalException("Unknown Bit Val Type")

    def translate(self, sym_count, function_param=False):
        result = {'emit': "", 'result': ""}
        value = self.translate_value(sym_count)
        result['emit'] += value['emit']
        if self.node_type == DATA_TYPE.BS_BIT_DECL:
            if function_param is False:
                result['emit'] += self.translate_type() + self.ID.translate()['result'] + " = 0;\n"
            else:
                result['emit'] += self.translate_type() + self.ID.translate()['result'] + ";\n"
        elif self.node_type == DATA_TYPE.BIT_DECL:
            if function_param is False:
                result['emit'] += self.translate_type() + self.ID.translate()['result'] + " = 0;\n"
            else:
                result['emit'] += self.translate_type() + self.ID.translate()['result'] + ";\n"
        if self.body is not None:
            set_result = self.body.translate(sym_count)
            result['emit'] += set_result
        return result['emit']

    def translate_value(self, sym_count):
        result = {'emit': "", 'result': ""}
        if self.value is None:
            result['result'] = "0"
        else:
            val_result = self.value.translate(sym_count)
            result['emit'] += val_result['emit']
            result['result'] += val_result['result']
        return result
    # def translate_as_parameter(self):
    #     return "bool " + self.ID.translate()


class Int_decl(object):

    type_decl_lookup = {"8": "uint8_t ",
                        "16": "uint16_t ",
                        "32": "uint32_t ",
                        "64": "uint64_t "}

    def __init__(self, n_type, constraints, var_id, value=None):
        self._constraints = constraints
        self._ID = var_id
        self._ID.constraints = constraints
        self._value = value
        self._node_type = n_type
        if value is not None:
            self._body = Set(self._ID, self.value)
        else:
            self._body = None

    @property
    def body(self):
        return self._body

    @property
    def node_type(self):
        return self._node_type

    @property
    def constraints(self):
        return self._constraints

    @property
    def ID(self):
        return self._ID

    @property
    def value(self):
        return self._value

    def translate(self, sym_count, func_param=False):
        result = {'emit': "", 'result': ""}
        if self.node_type == DATA_TYPE.BS_INT_DECL:
            if func_param == False:
                result['emit'] += self.translate_type() + self.ID.translate()["result"] + "[" + self.constraints.translate()['result'] + "]" + " = {0};\n"
            else:
                result['emit'] += self.translate_type() + self.ID.translate()["result"] + "[" + self.constraints.translate()['result'] + "]" + ";\n"
        elif self.node_type == DATA_TYPE.INT_DECL:
            if func_param == False:
                result['emit'] += self.translate_type() + self.ID.translate()["result"] + " = 0;\n"
            else:
                result['emit'] += self.translate_type() + self.ID.translate()["result"] + ";\n"
        if self.value is not None:
            result['emit'] += self.body.translate(sym_count)
            #     value_result = self.value.translate(sym_count)
            #     result['emit'] += value_result['emit']
            #     assignment_result = self.assign_int_val(value_result)
            #     result['emit'] += assignment_result['emit']
        return result['emit']

    def translate_type(self):
        if self.constraints.value in Int_decl.type_decl_lookup or self.node_type == DATA_TYPE.BS_INT_DECL:
            if self.node_type == DATA_TYPE.INT_DECL:
                return Int_decl.type_decl_lookup[self.constraints.value]
            elif self.node_type == DATA_TYPE.BS_INT_DECL:
                return "uint32_t "
        else:
            raise ParseException("Custom Size: Not yet implemented")

    # def translate_as_parameter(self):
    #     # print(self.constraints)
    #     if self.node_type == DATA_TYPE.BS_INT_DECL:
    #         return self.translate_type() + self.ID.name + "[" + self.constraints.translate() + "]"
    #     elif self.node_type == DATA_TYPE.INT_DECL:
    #         return self.translate_type() + self.ID.name


class Int_literal(object):

    def __init__(self, value=None, constraints=None):
        self.value = value
        self.type = DATA_TYPE.INT_VAL
        self.node_type = DATA_TYPE.INT_LITERAL
        self._constraints = constraints

    @property
    def constraints(self):
        return self._constraints

    def translate(self, sym_count=None):
        result = {}
        # target = Target_factory.name(sym_count)
        # result["emit"] = self.translate_type(target) + " = " + self.value + ";\n"
        # result["result"] = target
        result["emit"] = ""
        result["result"] = self.value
        return result

    def translate_target(self, target):
        return Target_factory.type_decl_lookup[self.constraints.value] + " " + target


class Bit_literal(object):

    def __init__(self, value):
        self.value = value
        self.type = DATA_TYPE.BIT_VAL
        self.node_type = DATA_TYPE.BIT_LITERAL

    def translate(self, sym_count=None):
        result = {'emit': "", 'result': ""}
        if self.value == "True":
            result['result'] = "0x1"
        elif self.value == "False":
            result['result'] = "0x0"
        else:
            raise InternalException("Unknown Bit Literal value: " + self.value)
        return result


class Name(object):

    def __init__(self, name, id_type, size=None, constraints=None):
        self._name = name
        self._type = id_type
        self.node_type = DATA_TYPE.ID
        self._constraints = constraints
        self._size = size

    @property
    def size(self):
        return self._size

    @property
    def constraints(self):
        return self._constraints

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @constraints.setter
    def constraints(self, value):
        self._constraints = value

    @size.setter
    def size(self, value):
        self._size = value

    def translate(self, sym_count=None):
        result = {}
        result["emit"] = ""
        result["result"] = self.name
        return result

    def dimension(self, dim):
        if self.type == DATA_TYPE.INT_VAL or self.type == DATA_TYPE.BS_INT_VAL:
            return self.constraints.translate()['result']
        elif self.type == DATA_TYPE.SEQ_INT_VAL or self.type == DATA_TYPE.BS_SEQ_INT_VAL:
            if dim == len(self.size):
                return self.constraints.translate()['result']
            elif dim < len(self.size):
                return self.size[dim].translate()['result']
        elif self.type == DATA_TYPE.SEQ_BIT_VAL or self.type == DATA_TYPE.SEQ_BS_BIT_VAL:
            if dim < len(self.size):
                return self.size[dim].translate()['result']
            else:
                raise ParseException("Internal error: that dimension doesn't exist")
        else:
            raise ParseException("Unsupported bounds check: " + str(self.type))



    # def translate_lhs(self, target):
    #     assert self.type == target.type, "Should always be aligned in type by this point by set operation"
    #     if self.type == DATA_TYPE.BS_INT_VAL:
    #         return self.lhs_bs(target)
    #     elif self.type == DATA_TYPE.INT_VAL:
    #         return self.lhs_int(target)
    #     else:
    #         raise ParseException("Unsupported set operation " + str(self.type))

    # def lhs_int(self, target):
    #     return self.name + "=" + target.translate() + ";\n"

    # def lhs_bs(self, target):
    #     ret = ""
    #     for bit in range(int(self.constraints.translate())):
    #         ret += self.name + "[" + str(bit) + "] = " + target.translate() + "[" + str(bit) + "]" + ";\n"
    #     return ret


class Call(object):

    def __init__(self, f_id, return_type, size, constraints, return_value):
        self._f_id = Name(f_id, return_type, size, constraints)
        self._parameters = []
        self._return_value = return_value
        self.node_type = DATA_TYPE.FUNCTION_CALL

    def add_parameter(self, p):
        self.parameters.append(p)

    @property
    def parameters(self):
        return self._parameters

    @property
    def type(self):
        return self.f_id.type

    @property
    def f_id(self):
        return self._f_id

    @property
    def constraints(self):
        return self._return_value.constraints

    @property
    def size(self):
        return self._return_value.size

    def translate(self, sym_count, value=None):
        result = {'emit': "", 'result': ""}
        function_result = self.call_temp_target(sym_count)
        result['emit'] += function_result['emit']
        params = []
        if self.f_id.type == DATA_TYPE.BIT_VAL or self.f_id.type == DATA_TYPE.BS_BIT_VAL:
            result['emit'] += function_result['result'] + " = "
        for p in self.parameters:
            #Perform declarations required of parametrs
            if p.type != DATA_TYPE.SBOX_DECL:
                param_result = p.translate(sym_count)
                result['emit'] += param_result['emit']
                params.append(param_result['result'])
        result['emit'] += self.f_id.translate()['result'] + "("
        if self.f_id.type == DATA_TYPE.BS_INT_VAL:
            result['emit'] += function_result['result'] + ", "
        for p in params:
                result['emit'] += p + ", "
        if len(params) != 0:
            result['emit'] = result['emit'][:-2]
        result['emit'] += ");\n"
        result['result'] = function_result['result']
        return result

    def call_temp_target(self, sym_count):
        """Create Temporary target for function result"""
        if self.f_id.type == DATA_TYPE.BS_INT_VAL:
            return Target_factory.make_bs_target(Target_factory.name(sym_count, "call"), self.f_id.constraints)
        elif self.f_id.type == DATA_TYPE.VOID:
            return {'emit': "", 'result': ""}
        elif self.f_id.type == DATA_TYPE.BS_BIT_VAL:
            return Target_factory.make_bit_target(Target_factory.name(sym_count, "call"), DATA_TYPE.BS_BIT_VAL)
        else:
            raise ParseException("Unsupported function call type " + str(self.f_id.type))


class Target_factory(object):

    type_decl_lookup = {"8": "uint8_t ",
                        "16": "uint16_t ",
                        "32": "uint32_t ",
                        "64": "uint64_t ",
                        DATA_TYPE.BS_INT_VAL: "uint32_t",
                        DATA_TYPE.BS_SEQ_INT_VAL: "uint32_t",
                        DATA_TYPE.SEQ_BS_BIT_VAL: "uint32_t"}

    def name(sym_count, append=""):
        # name =  "__" + "temp" + "_" + ''.join(random.choice('0123456789ABCDEF') for i in range(4)) + "_" + str(sym_count.count)
        name = "temp" + "_" + str(sym_count.count) + "_" + append
        sym_count.count += 1
        return name

    def round_up_constraints(constraint):
        if constraint <= 8:
            return "8"
        if constraint <= 16:
            return "16"
        if constraint <= 32:
            return "32"
        if constraint <= 64:
            return "64"
        else:
            raise ParseException("Constaint to big : " + str(constraint))

    def make_bit_target(name, bit_type):
        result = {'emit':"", 'result':""}
        result['result'] = name
        if bit_type == DATA_TYPE.BS_BIT_VAL:
            result['emit'] += "uint32_t " + name + ";\n"
        elif bit_type == DATA_TYPE.BIT_VAL:
            result['emit'] += "uint8_t " + name + ";\n"
        return result

    def make_bs_target(name, constraints):
        result = {'emit': "", 'result': "", 'res_size' : constraints.translate()["result"]}
        result['result'] = name
        result['emit'] += Target_factory.type_decl_lookup[DATA_TYPE.BS_INT_VAL] + " " + result['result'] + "[" + result['res_size'] + "]" + ";\n"
        return result


class For_loop(object):

    def __init__(self):
        self._initializer = []
        self._terminator = []
        self._increment = []
        self._body = []
        self._node_type = DATA_TYPE.FOR_LOOP

    @property
    def node_type(self):
        return self._node_type

    @property
    def initializer(self):
        return self._initializer

    @property
    def terminator(self):
        return self._terminator

    @property
    def increment(self):
        return self._increment

    @property
    def body(self):
        return self._body

    def translate(self, sym_count):
        result = {'emit': "", 'result': ""}
        init_result = self.translate_initializer(sym_count)
        term_result = self.translate_terminator(sym_count)
        increment = self.translate_increment(sym_count)
        result['emit'] += init_result['emit']
        result['emit'] += "for(;"
        result['emit'] += term_result['result']
        result['emit'] += ";) { \n"
        result['emit'] += self.translate_body(sym_count)
        result['emit'] += increment['emit']
        result['emit'] += "} \n"
        return result['emit']

    def translate_initializer(self, sym_count):
        result = {'emit': "", 'result': ""}
        for_loop = ""
        for stmt in self.initializer:
            result['emit'] += stmt.translate(sym_count)
        result['emit'] += for_loop
        return result

    def translate_body(self, sym_count):
        ret = ""
        for stmt in self.body:
            try:
                ret += stmt.translate(sym_count)
            except TypeError:
                ret += stmt.translate(sym_count)['emit']
        return ret

    def translate_increment(self, sym_count):
        result = {'emit': "", 'result': ""}
        for expr in self.increment:
            result['emit'] += expr.translate(sym_count)
        return result

    def translate_terminator(self, sym_count):
        result = {'emit': "", 'result': ""}
        if len(self.increment) > 1:
            raise ParseException("Internal Errror: Several stmts in increment in for loop.")
        comparison_result = self.terminator[0].translate(sym_count)
        result['emit'] += comparison_result['emit']
        result['result'] = comparison_result['result']
        return result


class Binary_operation(object):

    operations_lookup = {DATA_TYPE.INT_VAL: lambda self, sym_count, target = None: self.int_int_operation(sym_count, target),
                         DATA_TYPE.BIT_VAL: lambda self, sym_count, target = None: self.int_int_operation(sym_count, target),
                         DATA_TYPE.BS_BIT_VAL: lambda self, sym_count, target = None: self.bs_bit_operation(sym_count, target),
                         DATA_TYPE.BS_INT_VAL: lambda self, sym_count, target = None: self.bs_int_operation(sym_count, target),
                         DATA_TYPE.SEQ_BS_BIT_VAL: lambda self, sym_count, target = None: self.bs_int_operation(sym_count, target),
                         DATA_TYPE.SEQ_BIT_VAL: lambda self, sym_count, target = None: self.seq_bit_val_operation(sym_count, target)}

    bs_op_lookup = {">>>": "rotate_left(",
                    "<<<": "rotate_right(",
                    ">>": "shift_left(",
                    "<<": "shift_right(",
                    "^": "XOR(",
                    "&": "AND(",
                    "|": "OR(",
                    "+": "bitslice_add(",
                    "-": "bitslice_subtract(",
                    "*": "bitslice_mult("}

    def __init__(self, op_type, operator):
        self._node_type = op_type
        self._operator = operator
        self._left = None
        self._right = None
        self._type = None
        self.constraints = None
        self.size = None

    @property
    def node_type(self):
        return self._node_type

    @property
    def operator(self):
        return self._operator

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def right(self):
        return self._right

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self._left = value

    @right.setter
    def right(self, value):
        self._right = value

    @type.setter
    def type(self, value):
        self._type = value

    def seq_bit_val_operation(self, sym_count, target=None):
        result = {'emit': "", 'result': ""}
        operand_1 = self.left.translate(sym_count)
        operand_2 = self.right.translate(sym_count)
        result['emit'] += operand_1['emit']
        result['emit'] += operand_2['emit']
        if self.node_type == DATA_TYPE.SHIFT_OP:
            return self.seq_bit_shift(result, operand_1, operand_2, sym_count)
        elif self.node_type == DATA_TYPE.BITWISE_OP:
            return self.seq_bit_bitwise(result,  operand_1, operand_2, sym_count)
        else:
            raise InternalException("unsupported int seq operator " + self.operator)

    def seq_bit_bitwise(self, result, operand_1, operand_2, sym_count):
        """Translates bitwise operations on sequences of bits"""
        result['result'] += "(" + operand_1['result'] + " " + self.operator + " " + operand_2['result'] + ")"
        return result

    def translate_target_size(self, sym_count):
        return self.constraints.translate(sym_count)

    def seq_bit_shift(self, result, operand_1, operand_2, sym_count):
        """Translates shift or rotate of a subset of bits of an int value"""
        self.target_decl(sym_count, result)
        bit_size = None
        if self.left.node_type == DATA_TYPE.INDEX_SELECT:
            bit_size = self.left.translate_target_size(sym_count)
            result['emit'] += bit_size['emit']
        elif self.left.type == DATA_TYPE.SEQ_BIT_VAL:
            bit_size = self.left.translate_target_size(sym_count)
        else:
            raise InternalException("Unsupported bit seq extraction on " + str(self.left.node_type))
        if self.operator == "<<":
            result['emit'] += result['result'] + " = " + "(" + operand_1['result'] + ")" + " << " + operand_2['result'] + ";\n"
        elif self.operator == ">>":
            result['emit'] += result['result'] + " = " + operand_1['result'] + " >> " + operand_2['result'] + ";\n"
        elif self.operator == ">>>" or self.operator == "<<<":
            self.int_bit_rotate(result, operand_1['result'], operand_2['result'], bit_size['result']) 
        else:
            raise InternalException("Unrecognised shift operator " + self.operator)
        self.mask_shift(result, bit_size['result'], sym_count)
        return result

    def int_bit_rotate(self, result, op_1, op_2, size):
        if self.operator == ">>>":
            result['emit'] += result['result'] + " = " + "(" + "(" + op_1 + ")" + " >> " + op_2 + ") | (" + "(" + op_1\
                + ")" + " << " + "(" + str(size) + " - " + op_2 + "));\n"
        elif self.operator == "<<<":
            result['emit'] += result['result'] + " = " + "(" + "(" + op_1 + ")" + " << " + op_2 + ") | (" + "(" + op_1\
                + ")" + " >> " + "(" + str(size) + " - " + op_2 + "));\n"

    def mask_shift(self, result, bit_size, sym_count):
        init = Target_factory.name(sym_count, "mask_loop_init")
        result['emit'] += "uint32_t " + init + " = " + str(bit_size) + ";\n"
        result['emit'] += "for(; " + init + " < 32; " + init + "++) {\n"
        result['emit'] += result['result'] + " &= ~(0x1 << " + init + ");\n"
        result['emit'] += "}\n"

    def bs_int_operation(self, sym_count, target=None):
        if self.node_type == DATA_TYPE.SHIFT_OP:
            return self.bs_operation(sym_count, self.bs_op_lookup[self.operator])
        if self.node_type == DATA_TYPE.BITWISE_OP:
            return self.bs_operation(sym_count, self.bs_op_lookup[self.operator])
            # self.bitslice_bitwise(sym_count, target)
        if self.node_type == DATA_TYPE.ARITH_OP:
            return self.bs_operation(sym_count, self.bs_op_lookup[self.operator])
        else:
            raise ParseException("unrecognised bs int operation type" + str(self.node_type))

    def can_be_optimised(self):
        if self.operand_can_be_optimised(self.left) and self.operand_can_be_optimised(self.right):
            return True

    def operand_can_be_optimised(self, op):
        if op is None:
            return True
        elif op.node_type == DATA_TYPE.SHIFT_OP:
            return False
        elif op.type == DATA_TYPE.BS_INT_VAL:
            return True
        elif op.node_type == DATA_TYPE.BITWISE_OP and op.type == DATA_TYPE.BS_INT_VAL:
            return op.can_be_optimised()
        elif op.node_type == DATA_TYPE.INT_LITERAL:
            return True
        return False

    def bitslice_bitwise(self, sym_count, target=None):
        result = {'emit': "", 'result': ""}
        if target is not None:
            left = self.left.translate(sym_count)
            right = self.right.translate(sym_count)
            if self.left.node_type == DATA_TYPE.ID and self.right.node_type == DATA_TYPE.ID:
                result['result'] = self.left.translate(sym_count)['result'] + " " 

        raise ParseException("bitsliced bitwise")

    def bs_operation(self, sym_count, function):
        result = {'emit': "", 'result': "", 'res_size_1': None, 'res_size_2': None}
        temp_target = self.target_decl(sym_count)
        result['emit'] += temp_target['emit']
        result['result'] = temp_target['result']
        operand_1 = self.left.translate(sym_count)
        operand_2 = self.right.translate(sym_count)
        result['emit'] += operand_1['emit']
        result['emit'] += operand_2['emit']
        if self.right.type != self.left.type:
            if self.needs_cast(self.left.type, self.right.type):
                #Getting value to cast
                if self.left.type != self.type:
                    cast_target = operand_1['result']
                elif self.right.type != self.type:
                    cast_target = operand_2['result']
                if 'res_size' in temp_target:
                    cast = self.implicit_cast(sym_count, cast_target, temp_target['res_size'])
                else:
                    cast = self.implicit_cast(sym_count, cast_target)
                result['emit'] += cast['emit']
                #setting correct operand to value to cast
                if self.left.type != self.type:
                    operand_1['result'] = cast['result']
                elif self.right.type != self.type:
                    operand_2['result'] = cast['result']
        operation_size = self.get_bs_res_size(operand_1, operand_2)
        result['emit'] += function + temp_target['result'] + ", " + operand_1['result'] + ", " + operand_2['result']\
            + ", " + operation_size + ");\n"
        return result

    def get_bs_res_size(self, oper_1, oper_2):
        if self.node_type == DATA_TYPE.SHIFT_OP:
            if 'res_size' in oper_1:
                return oper_1['res_size']
            else:
                return self.constraints.translate()['result']
        elif self.node_type == DATA_TYPE.BITWISE_OP:
            return self.constraints.translate()['result']
        elif self.node_type == DATA_TYPE.ARITH_OP:
            return self.constraints.translate()['result']

    def int_int_operation(self, sym_count, target=None):
        if self.node_type == DATA_TYPE.COMP_OP:
            return self.int_compare_operation(sym_count)
        elif self.node_type == DATA_TYPE.LOG_OP:
            return self.int_compare_operation(sym_count)
        else:
            return self.int_compute_operation(sym_count)

    def bs_bit_operation(self, sym_count, target=None):
        if self.node_type == DATA_TYPE.COMP_OP:
            return self.int_compare_operation(sym_count)
        elif self.node_type == DATA_TYPE.LOG_OP:
            return self.int_compare_operation(sym_count)
        else:
            return self.bs_bit_compute_operation(sym_count)

    def implicit_cast(self, sym_count, target, size=None):
        """Casts operand to correct value

        Args:
        Sym_count: Temp var count for program
        target: target operand that requires cast."""
        result = {'emit': "", 'result': ""}
        operand_for_cast = self.get_operand_for_cast()
        if self.type == DATA_TYPE.SEQ_BS_BIT_VAL:
            if operand_for_cast.type == DATA_TYPE.SEQ_BIT_VAL:
                cast_res = Cast.int_to_bs_cast(sym_count, target, size)
                result['result'] = cast_res['result']
                result['emit'] = cast_res['emit']
            else:
                raise ParseException("Unsupported implicit cast type required " + str(operand_for_cast.type) + " to " + str(self.type))
        elif self.type == DATA_TYPE.BS_INT_VAL:
            if operand_for_cast.type == DATA_TYPE.INT_VAL:
                cast_res = Cast.int_to_bs_cast(sym_count, target, size)
                result['result'] = cast_res['result']
                result['emit'] = cast_res['emit']
            else:
                raise ParseException("Unsupported implicit cast type required " + str(operand_for_cast.type) + " to " + str(self.type))
        elif self.type == DATA_TYPE.BS_BIT_VAL:
            if operand_for_cast.type == DATA_TYPE.BIT_VAL:
                cast_res = Cast.bit_to_bs_bit(operand_for_cast, sym_count)
                result['result'] = cast_res['result']
                result['emit'] += cast_res['emit']
            else:
                raise ParseException("Unsupported implicit cast type required " + str(operand_for_cast.type) + " to " + str(self.type))
        else:
            raise ParseException("Unsupported implicit cast type required " + str(operand_for_cast.type) + " to " + str(self.type))
        return result

    def get_operand_for_cast(self):
        if self.left.type != self.type:
            return self.left
        elif self.right.type != self.type:
            return self.right

    def needs_cast(self, op_1, op_2):
        if self.node_type == DATA_TYPE.BITWISE_OP:
            return DATA_TYPE.bitwise_op_needs_cast(op_1, op_2)
        elif self.node_type == DATA_TYPE.SHIFT_OP:
            pass
        elif self.node_type == DATA_TYPE.ARITH_OP:
            return DATA_TYPE.arith_op_needs_cast(op_1, op_2)
        else:
            raise ParseException("op type may need cast")

    def int_compare_operation(self, sym_count):
        result = {'emit': "", 'result': ""}
        operand_1 = self.left.translate(sym_count)
        operand_2 = self.right.translate(sym_count)
        result['emit'] += operand_1['emit']
        result['emit'] += operand_2['emit']
        result['result'] = "(" + operand_1['result'] + " " + self.operator + " " + operand_2['result'] + ")"
        return result

    def bs_bit_compute_operation(self, sym_count):
        result = {'emit': "", 'result': ""}
        operand_1 = self.left.translate(sym_count)
        operand_2 = self.right.translate(sym_count)
        if self.needs_cast(self.left.type, self.right.type):
            if self.left.type != self.type:
                cast_target = operand_1['result']
            elif self.right.type != self.type:
                cast_target = operand_2['result']
            cast = self.implicit_cast(sym_count, cast_target)
            result['emit'] += cast['emit']
            if self.left.type != self.type:
                operand_1['result'] = cast['result']
            elif self.right.type != self.type:
                operand_2['result'] = cast['result']
        result['emit'] += operand_1['emit'] + operand_2['emit']
        result['result'] = "(" + operand_1['result'] + " " + self.operator + " " + operand_2['result'] + ")"
        return result

    def int_compute_operation(self, sym_count):
        result = {'emit': "", 'result': "", 'res_size_1': None, 'res_size_2': None}
        temp_target = self.target_decl(sym_count)
        operand_1 = self.left.translate(sym_count)
        operand_2 = self.right.translate(sym_count)
        result['emit'] += operand_1['emit']
        result['emit'] += operand_2['emit']
        if self.right.type != self.left.type and self.needs_cast(self.left.type, self.right.type):
            if 'res_size' in operand_1:
                result['res_size_1'] = operand_1['res_size']

            if 'res_size' in operand_2:
                result['res_size_2'] = operand_2['res_size']

            result['emit'] += temp_target['emit']

            if result['res_size_1'] is not None or result['res_size_2'] is not None:
                # Index select operation
                for i in range(int(self.get_size(result))):
                    result['emit'] += temp_target['result'] + " = " + operand_1['result'] + self.translate_index(i, result['res_size_1']) + " " + self.operator +\
                    " " + operand_2['result'] + self.translate_index(i, result['res_size_2']) + ";\n"
            else:
                result['emit'] += temp_target['result'] + " = " + operand_1['result'] + " " + self.operator + " " + operand_2['result'] + ";\n"
            result['result'] = temp_target['result']
        else:
            result['result'] = "(" + operand_1['result'] + " " + self.operator + " " + operand_2['result'] + ")"
        return result

    def translate_index(self, ele, res_size):
        if res_size is not None:
            return "[" + str(ele) + "]"
        else:
            return ""

    def get_size(self, result):
        if result['res_size_1'] is not None:
            return result['res_size_1']
        if result['res_size_2'] is not None:
            return result['res_size_2']

    def target_decl(self, sym_count, res= None):
        result = {'emit': "", 'result': "", 'res_size': None}
        if self.type == DATA_TYPE.INT_VAL:
            result['result'] += Target_factory.name(sym_count) + "_bin"
            result['emit'] += "uint32_t" + " " + result['result'] + " = 0;\n"
        elif self.type == DATA_TYPE.BIT_VAL:
            result['result'] += Target_factory.name(sym_count) + "_bin"
            result['emit'] += "Bit" + " " + result['result'] + " = 0;\n"
        elif self.type == DATA_TYPE.BS_BIT_VAL:
            result['result'] += Target_factory.name(sym_count) + "_bin"
            result['emit'] += "uint32_t" + " " + result['result'] + " = 0;\n"
        elif self.type == DATA_TYPE.BS_INT_VAL:
            result['result'] += Target_factory.name(sym_count) + "_bin"
            result['emit'] += "uint32_t" + " " + result['result'] + "[" + self.constraints.translate(sym_count)['result'] + "]" + " = {0};\n"
            result['res_size'] = self.constraints.translate(sym_count)['result']
        elif self.type == DATA_TYPE.SEQ_BS_BIT_VAL:
            result['result'] += Target_factory.name(sym_count) + "_bin"
            start_size = self.size['start'].translate()
            result['emit'] += start_size['emit']
            end_size = self.size['finish'].translate()
            result['emit'] += end_size['emit']
            result['res_size'] = "(" + end_size['result'] + " - " + start_size['result'] + ")" + " + 1"
            result['emit'] += "uint32_t" + " " + result['result'] + "[" + result['res_size'] + "]" + " = {0};\n"
        elif self.type == DATA_TYPE.SEQ_BIT_VAL:
            res['result'] += Target_factory.name(sym_count, "bit_seq")
            res['emit'] += "uint32_t " + res['result'] + " = 0x0;\n"
        else:
            raise ParseException("Need Type declaration " + str(self.type))
        return result

    def optimised_bitwise_bitslice(self, target, sym_count, size):
        result = {'emit': "", 'result': ""}
        assert self.type == DATA_TYPE.BS_INT_VAL, "Optimised bitsliced bitwise"
        for bit in range(0, int(size)):
            result['emit'] += (target + "[" + str(bit) + "] = " + self.get_optimised(result, self.left, bit, sym_count) + " " + self.operator + " " + self.get_optimised(result,self.right, bit, sym_count) + ";\n")
        return result


    def get_optimised(self, result, operand, bit, sym_count):
        if operand.node_type == DATA_TYPE.ID:
            return operand.translate()['result'] + "[" + str(bit) + "]"
        elif operand.node_type == DATA_TYPE.INT_LITERAL:
            if((int(operand.translate()['result']) >> bit) & 0x1) == 0x1:
                return "0xffffffff"
            else:
                return "0x0"
            raise InternalException("Int lit opt")
        elif operand.node_type == DATA_TYPE.INDEX_SELECT:
            index_select = operand.translate(sym_count)
            result['emit'] += index_select['emit']
            return index_select['result'] + "[" + str(bit) + "]"
        elif operand.node_type == DATA_TYPE.BITWISE_OP:
            return "(" + self.get_optimised(result, operand.left, bit, sym_count) + " " + operand.operator + " " + self.get_optimised(result, operand.right, bit, sym_count) + ")"
        else:
            raise InternalException("Unexpected operand for optimised operation " + str(operand.node_type))

    def optimised_translate(self, target, sym_count, size):
        if self.node_type == DATA_TYPE.BITWISE_OP:
            return self.optimised_bitwise_bitslice(target, sym_count, size)
        else:
            raise InternalException("Unsupported optimization")

    def translate(self, sym_count, target=None):
        return Binary_operation.operations_lookup[self.type](self, sym_count, target)

class Cast_operation(object):

    def __init__(self, c_type, constraints, size):
        self._type = c_type
        if constraints is not None and constraints.node_type != DATA_TYPE.INT_LITERAL:
            raise ParseException("Can only use literals for word widths casts")
        self._constraints = constraints
        if len(size) > 0:
            self._seq_size = size
        else:
            self._seq_size = None
        self.node_type = DATA_TYPE.CAST_OP

    @property
    def seq_size(self):
        return self._seq_size

    @property
    def constraints(self):
        return self._constraints

    @property
    def type(self):
        return self._type
