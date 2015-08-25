from DATA_TYPE import DATA_TYPE
from pyparsing import ParseException
import random
from quine_mccluskey.qm import QuineMcCluskey
import itertools
from Translation_exceptions import SemanticException, InternalException


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
        for node in self.IR:
            try: 
                result['main'] += node.translate(self.sym_count)
            except TypeError:
                result['main'] += node.translate(self.sym_count)['emit']
            if node.node_type == DATA_TYPE.FUNC_DECL:
                result['header'] += node.translate_header(self.sym_count) + ";\n"
            elif node.node_type == DATA_TYPE.SBOX_DECL:
                result['header'] += node.translate_header(self.sym_count)
        return result


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
        return self._node_type

    @property
    def ID(self):
        return self._ID

    def translate(self, sym_count):
        ret = ""
        ret += self.translate_header(sym_count)
        body_result = self.translate_body(sym_count)
        ret = body_result['emit'] + ret
        ret += body_result['result']
        ret += "}\n"
        return ret

    def translate_header(self, sym_count):
        if self.return_value == DATA_TYPE.VOID:
            return "void " + self.translate_name() + self.translate_parameters(sym_count)
        elif self.return_value.node_type == DATA_TYPE.BS_INT_DECL:
            self.return_param = Target_factory.name(sym_count, "bs_return")
            return "void " + " " + self.translate_name() + self.translate_parameters(sym_count, "uint32_t *" + self.return_param) + self.translate_dimensions()
        else:
            return self.return_value.translate_type() + " " + self.translate_name() + self.translate_parameters(sym_count) + self.translate_dimensions()

    def translate_dimensions(self):
        ret = ""
        return_type = self.return_value.ID.type
        if DATA_TYPE.is_seq_type(return_type):
            # ret += ")"
            for i, dim in enumerate(self.return_value.size):
                if i == 0:
                    ret += ")"
                else:
                    ret += "[" + dim.translate()['result'] + "]"
            if return_type == DATA_TYPE.BS_SEQ_INT_VAL:
                ret += "[" + self.return_value.constraints.value + "]"
        return ret

    def translate_body(self, sym_count):
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
                else:
                    result['result'] += statement
                # except TypeError:
                    # result['result'] += stmt.translate(sym_count)['emit']
        return result

    def translate_parameters(self, sym_count, bs_bit_return=None):
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

    def __init__(self, condition, body=None):
        self._condition = condition
        self._body = []
        self.node_type = DATA_TYPE.IF_STMT

    @property
    def condition(self):
        return self._condition

    @property
    def body(self):
        return self._body

    def add_stmt(self, stmt):
        self._body.append(stmt)

    def translate(self, sym_count):
        result = {'emit': "", 'result': ""}
        condition_result = self.condition.translate(sym_count)
        result['emit'] += condition_result['emit']
        result['emit'] += "if(" + condition_result['result'] + ") { \n"
        result['emit'] += self.translate_body(sym_count)
        result['emit'] += "} \n"
        return result['emit']

    def translate_body(self, sym_count):
        ret = ""
        for stmt in self.body:
            ret += stmt.translate(sym_count)
        return ret


class Element_range(object):

    node_type = DATA_TYPE.INDEX_RANGE

    def __init__(self, start, finish):
        self._start = start
        self._finish = finish
        self.type = None

    @property
    def start(self):
        return self._start

    @property
    def finish(self):
        return self._finish

    def is_literal(self):
        if self.start.node_type == DATA_TYPE.INT_LITERAL and self.finish.node_type == DATA_TYPE.INT_LITERAL:
            return True
        return False

    def translate_size(self, sym_count):
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

    def __init__(self, c_op, c_target):
        self._cast_target = c_target
        self._cast_op = c_op
        self.node_type = DATA_TYPE.CAST

    def translate(self):
        return self.operation.translate(self.target)

    @property
    def type(self):
        return self._cast_op.type

    @property
    def target(self):
        return self._cast_target

    @property
    def operation(self):
        return self._cast_op

    @property
    def constraints(self):
        return self._cast_op.constraints

    def bit_seq_to_int_val(target, sym_count):
        result = {'emit': "", 'result': ""}
        # if target.node_type
        if DATA_TYPE.is_op_type(target.node_type):
            pass
        elif target.node_type == DATA_TYPE.SEQ_VAL:
            Cast.bit_seq_val_to_int_val(result, target, sym_count)
        return result

    def bit_seq_val_to_int_val(result, target, sym_count):
        result['result'] += Target_factory.name(sym_count, "casted_bit_seq")
        result['emit'] += Target_factory.type_decl_lookup[Target_factory.round_up_constraints(len(target.value))] + result['result'] + " = 0;\n"
        for pos, bit in enumerate(reversed(target.value)):
            if bit.translate()['result'] == "0x1":
                result['emit'] += result['result'] + " |= 0x1 << " + str(pos) + ";\n"
            elif bit.translate()['result'] == "0x0":
                pass
            else:
                raise InternalException("Unknown Value in Bit Sequence " + str(bit.translate()['result']))

    def int_to_bs_cast(sym_count, target, size=None):
        result = {'emit': "", 'result': ""}
        result['result'] = Target_factory.name(sym_count, "casted_bs")
        result['emit'] += "uint32_t " + result['result'] + "[" + size + "]" + ";\n"
        result['emit'] += "int_to_bitsliced(" + result['result'] + ", " + target + ", " + size + ");\n"
        return result

    def bitslice_literal(sym_count, value, size, target = None):
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
        result = {'emit': '', 'result': ''}
        if value.translate()['result'] == "0x1":
            result['result'] = "0xffffffff"
        elif value.translate()['result'] == "0x0":
            result['result'] = "0x0"
        else:
            raise ParseException("Internal error: Unknown bit value")
        return result


class Index_select(object):

    def __init__(self, target, indices, output_type=None):
        self.target = target
        self.indices = indices
        self.node_type = DATA_TYPE.INDEX_SELECT
        if output_type is None:
            self._type = self.target.type
        else:
            self._type = output_type

    # @property
    # def name(self):
    #     if target.type == DATA_TYPE.ID:
    #         return target.type.name
    #     else:
    #         return "result"

    def translate(self, sym_count, value=None):
        result = {'emit': "", 'result': ""}
        if value is not None:
            # Assignment
            result['emit'] += self.translate_assignment_target(sym_count, value)
            return result
        else:
            if self.target.type == DATA_TYPE.SBOX_DECL:
                sbox_lookup = self.sbox_lookup_translate(sym_count)
                result['emit'] += sbox_lookup['emit']
                result['result'] = sbox_lookup['result']
            else:
                target_result = self.target.translate()
                result['emit'] += target_result['emit']
                extracted_sequence = self.extract_sequence(target_result['result'], sym_count)
                if 'res_size' in extracted_sequence:
                    result['res_size'] = extracted_sequence['res_size']
                result['emit'] += extracted_sequence['emit']
                result['result'] = extracted_sequence['result']
            return result
            # result['emit'] += target + self.translate_selection_dim() + "[" + self.indices[-1][0].translate(sym_count) + "]"

    def sbox_lookup_translate(self, sym_count):
        result = {'emit': "", 'result': ""}
        assert len(self.indices) == 1, "Sbox looks can only ever be one dimensional"
        index_result = self.indices[-1][-1].translate(sym_count)
        result['result'] = index_result['result']
        result['emit'] += index_result['emit']
        result['emit'] += self.target.translate(sym_count)['result'] + "(" + index_result['result'] + ");\n"
        return result

    def translate_as_lhs(self, sym_count, value):
        result = {'emit': "", 'result': ""}
        # index_result = self.translate_selection_dim(sym_count)
        # result['emit'] += index_result['emit']
        if self.type == DATA_TYPE.BS_BIT_VAL:
            if 'res_size' in value:
                assert int(value['res_size']) == 1, "Assuming this is only a single element bitsliced integer"
                result['emit'] += self.target.translate()['result'] + self.translate_selection_dim(sym_count)['result'] + "[" + self.indices[-1][-1].translate()['result'] + "]" + " = " + value['result'] + "[0];\n"
            else:
                result['emit'] += self.target.translate()['result'] + self.translate_selection_dim(sym_count)['result'] + "[" + self.indices[-1][-1].translate()['result'] + "]" + " = " + value['result'] + ";\n"
        elif self.type == DATA_TYPE.SEQ_BS_BIT_VAL:
            if self.indices[-1][-1].node_type == DATA_TYPE.INDEX_RANGE and self.indices[-1][-1].is_literal():
                result['emit'] += self.literal_range_set(value, sym_count)
            else:
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
        elif self.type == DATA_TYPE.BS_INT_VAL:
            if int(self.constraints.translate()['result']) > 1:
                temp_starting_ele = Target_factory.name(sym_count, "bs_int_start")
                result['emit'] += "uint8_t " + temp_starting_ele + ";\n"
                selection_dims = self.translate_selection_dim(sym_count)
                result['emit'] += selection_dims['emit']
                result['emit'] += "for(" + temp_starting_ele + " = 0; " + temp_starting_ele + " < " + self.target.constraints.translate()['result'] + "; " + temp_starting_ele + "++){\n"
                result['emit'] += self.target.translate()['result'] + selection_dims['result'] + "[" + temp_starting_ele + "]" + " = " + value['result'] + "[" + temp_starting_ele + "];\n"
                result['emit'] += "}\n"
            else:
                #Avoid loop for 1 bit bs int vals
                selection_dims = self.translate_selection_dim(sym_count)
                result['emit'] += selection_dims['emit']
                result['emit'] += self.target.translate()['result'] + selection_dims['result'] + "[0] = " + value['result'] + "[0];\n"       
        elif self.type == DATA_TYPE.BIT_VAL:
            result['emit'] += self.set_int_bit_val(value, sym_count)['emit']
        elif self.type == DATA_TYPE.SEQ_BIT_VAL:
            result['emit'] += self.set_seq_bit_val(value, sym_count)['emit']
        elif self.type == DATA_TYPE.INT_VAL:
            result['emit'] += self.set_seq_int_val(value, sym_count)['emit']
        else:
            raise ParseException("Unsupported extraction on LHS " + str(self.type))
        return result

    def set_seq_int_val(self, value, sym_count):
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
        result = {'emit': "", 'result': ""}
        selection_dims = self.translate_selection_dim(sym_count)
        result['emit'] += selection_dims['emit']
        if self.is_range():
            self.range_int_bit_set(value, result, selection_dims, sym_count)
        else:
            for i, bit in enumerate(self.indices[-1]):
                self.set_bit(result, self.target.translate()['result'], str(i), bit.translate()['result'], value['result'])
                # result['emit'] += "if(((" + value['result'] + " >> " + str(i) + ") & 0x1) == 0 ){\n"
                # result['emit'] += self.target.translate()['result'] + " &= ~(0x1 <<" + bit.translate()['result'] +");\n"
                # result['emit'] += "} else if (((" + value['result'] + " >> " + str(i) + ") & 0x1) == 1 ){\n"
                # result['emit'] += self.target.translate()['result'] + " |= (0x1 << " + bit.translate()['result'] +");\n"
                # result['emit'] += "}\n"
        return result

    def set_bit(self, result, target, source_bit, target_bit, value):
            """Set a specified bit on target variable from source variable.

            Args:
                result: storage for emitted code.
                target: Target var for setting bit.
                source_bit: bit position that target bit should be set to.
                target_bit: bit position that should be set in target bit.
                value: holds series of bits being copied to target.
            """
            result['emit'] += "if(((" + value + " >> " + source_bit + ") & 0x1) == 0 ){\n"
            result['emit'] += target + " &= ~(0x1 <<" + target_bit + ");\n"
            result['emit'] += "} else if (((" + value + " >> " + source_bit + ") & 0x1) == 1 ){\n"
            result['emit'] += target + " |= (0x1 << " + target_bit + ");\n"
            result['emit'] += "}\n"

    def range_int_bit_set(self, value, result, selection_dims, sym_count):
        """Sets bits in an integer range"""
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
        self.set_bit(result, self.target.translate()['result'], temp_starting_bit, curr_bit, value['result'])
        result['emit'] += "}\n"

    def set_int_bit_val(self, value, sym_count):
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
        result = {'emit': "", 'result': ""}
        range_size = (int(self.indices[-1][-1].finish.translate()['result']) - int(self.indices[-1][-1].start.translate()['result'])) + 1
        start_ele = int(self.indices[-1][-1].start.translate()['result'])
        end_ele = int(self.indices[-1][-1].finish.translate()['result']) + 1
        selection_dims = self.translate_selection_dim(sym_count)
        result['emit'] += selection_dims['emit']
        for i, ele in enumerate(range(start_ele, end_ele)):
            result['emit'] += self.target.translate()['result'] + selection_dims['result'] + "[" + str(ele) + "]" + " = " + value['result'] + "[" + str(i) + "];\n"
        return result['emit']

    def extract_sequence(self, target, sym_count):
        assert self.target.node_type == DATA_TYPE.ID, "Assumption target is just an ID at this point"
        if self.type == DATA_TYPE.BS_BIT_VAL:
            return self.extract_bs_int_bits(target, sym_count)
        elif self.type == DATA_TYPE.BS_INT_VAL:
            return self.extract_bs_int_val(target, sym_count)
        elif self.type == DATA_TYPE.SEQ_BS_BIT_VAL:
            return self.extract_bs_int_bits(target, sym_count)
        elif self.target.type == DATA_TYPE.SBOX_DECL:
            raise ParseException("Unsupport seq type extraction " + str(self.type) + " from " + str(self.target.type))
        elif self.target.type == DATA_TYPE.INT_VAL:
            return self.extract_int_bits(target, sym_count)
        else:
            raise ParseException("Unsupport seq type extraction " + str(self.type) + " from " + str(self.target.type))


    def extract_int_bits(self, target, sym_count):
        result = {'emit': "", 'result': ""}
        result['result'] = Target_factory.name(sym_count, "extracted")
        result['emit'] += Target_factory.type_decl_lookup[self.target.constraints.translate()['result']] + " " + result['result'] + " = 0;\n"
        if self.indices[-1][-1].node_type == DATA_TYPE.INDEX_RANGE:
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
            result['emit'] += result['result'] + " |= " + "((" + target + " >> " + start_range_target + ") " + " << " + target_bit + ");\n"
            result['emit'] += "}\n"
        elif len(self.indices[-1]) == 1:
            selected_bit = self.indices[-1][-1].translate()
            result['emit'] += selected_bit['emit']
            result['emit'] += result['result'] + " = " + "(" + target + " >> " + selected_bit['result'] + ") & 0x1;\n"
        else:
            result['emit'] += self.extract_int_bit_seq(target, result['result'], sym_count)
        return result

    def extract_int_bit_seq(self, target, temp_target, sym_count):
        result = {'emit': "", 'result': ""}
        for i, bit in enumerate(self.indices[-1]):
            index_res = bit.translate(sym_count)
            result['emit'] += index_res['emit']
            result['emit'] += temp_target + " ^= (((" + target + " >> " + index_res['result'] + ") & 0x1) " + "<< " + str(i) + ");\n"
        return result['emit']

    def extract_bs_int_val(self, target, sym_count):
        """Extract entire bitsliced int from a sequence of bs ints"""
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
        """Extracting bits from bitsliced Int from single selector, range or list"""
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

        if self.type == DATA_TYPE.SEQ_BS_BIT_VAL:
            return self.extract_bs_range(sym_count, target)
        else:
            raise ParseException("Unknown range type to create temporary variable for extraction " + self.type)

    def extract_bs_range(self, sym_count, target):
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
        if len(self.indices[-1]) > 1:
            return True
        return False

    def is_range(self):
        if self.indices[-1][0].node_type == DATA_TYPE.INDEX_RANGE:
            assert len(self.indices[-1]) == 1, "Only single range contained in selection"
            return True
        else:
            return False

    def translate_target_size(self, sym_count):
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

    def translate(self, sym_count, end=True):
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
                else:
                    raise ParseException("Unrecognised Target type " + str(self.target.node_type))
        else:
            raise ParseException("Unrecognised set type " + str(self.target.node_type))
        return result['emit']

    def translate_optimised_bitwise_set(self, sym_count):
        return self.value.optimised_translate(self.target.translate()['result'], sym_count, self.target.constraints.translate()['result'])

    def implicit_cast(self, sym_count):
        if self.target.type == DATA_TYPE.BS_INT_VAL:
            return self.implicit_cast_to_bs_int(sym_count)
        elif self.target.type == DATA_TYPE.SEQ_BS_BIT_VAL:
            return self.implicit_cast_to_bs_bits(sym_count)
        elif self.target.type == DATA_TYPE.INT_VAL:
            return self.implicit_cast_to_int_val(sym_count)
        elif self.target.type == DATA_TYPE.BS_BIT_VAL:
            return self.implicit_cast_to_bs_bit(sym_count)
        else:
            raise ParseException(str(self.value.type) + " being assigned to a " + str(self.target.type) + " : Cast needed")

    def implicit_cast_to_int_val(self, sym_count):
        if self.value.type == DATA_TYPE.SEQ_BIT_VAL:
            return Cast.bit_seq_to_int_val(self.value, sym_count)
        else:
            raise InternalException("Unsupported cast to int val")

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
        result = {'emit': "", 'result': ""}
        value = self.value.translate(sym_count)
        result['emit'] += value['emit']
        casted_value = Target_factory.make_bs_target(Target_factory.name(sym_count, "cast_bs_val"), self.target.constraints)
        result['emit'] += casted_value['emit']
        result['emit'] += "int_to_bitsliced(" + casted_value['result'] + ", " + value['result'] + ", " + casted_value['res_size'] + ");\n"
        result['result'] = casted_value['result']
        return result

    def translate_index_selection_set(self, sym_count, value):
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
        target_result = self.target.translate(sym_count)
        result['emit'] += target_result['emit']
        if self.value.node_type == DATA_TYPE.INT_LITERAL:
            return
        for i in range(int(self.target.constraints.value)):
            result['emit'] += target_result['result'] + "[" + str(i) + "]" + " = " + value_result['result'] + "[" + str(i) + "]" + ";\n"

    def translate_integer_set(self, result, value_result, sym_count):
            target_result = self.target.translate(sym_count)
            result['emit'] += target_result['emit']
            result['emit'] += target_result['result'] + " = " + value_result['result'] + self.translate_index(0, value_result) + ";\n"

    def translate_index(self, ele, result):
        if 'res_size' in result:
            if result['res_size'] is not None:
                return "[" + str(ele) + "]"
        return ""

class Return(object):
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
        target = self.target.translate(sym_count)
        ret = target['emit']
        if self.return_target is not None:
            for bit in range(0, int(self.target.constraints.translate()['result'])):
                ret += self.return_target + "[" + str(bit) + "] = " + target['result'] + "[" + str(bit) + "];\n"
            return ret
        else:
            return "return " + target['result'] + ";\n"


class Seq_decl(object):

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
        result = {'emit': "", 'result': ""}
        if self.node_type == DATA_TYPE.BS_SEQ_INT_DECL:
            if func_param is True:
                result['emit'] += Target_factory.type_decl_lookup[self.ID.type] + " " + self.ID.translate()['result'] + self.translate_index() + ";\n"
            else:
                result['emit'] += Target_factory.type_decl_lookup[self.ID.type] + " " + self.ID.translate()['result'] + self.translate_index() + " = " + self.init_value() + ";\n"
        elif self.node_type == DATA_TYPE.SBOX_DECL:
            result['emit'] += self.translate_sbox_decl(sym_count)
        elif self.node_type == DATA_TYPE.SEQ_INT_DECL:
            if func_param is True:
                result['emit'] += Target_factory.type_decl_lookup[self.constraints.translate()['result']] + " " + self.ID.translate()['result'] + self.translate_index() + ";\n"
            else:
                result['emit'] += Target_factory.type_decl_lookup[self.constraints.translate()['result']] + " " + self.ID.translate()['result'] + self.translate_index() + " = " + self.init_value() + ";\n"
        else:
            raise ParseException("Translation of Unknown Sequence Type attempted: " + str(self.node_type))
        if self.body is not None and self.node_type != DATA_TYPE.SBOX_DECL:
            result['emit'] += self.body.translate(sym_count)
        return result['emit']

    def init_value(self):
        if self.node_type == DATA_TYPE.BS_SEQ_INT_DECL:
            return (len(self.size) + 1) * "{" + " 0 " + (len(self.size) + 1) * "}"
        else:
            return len(self.size) * "{" + " 0 " + len(self.size) * "}"

    def translate_index(self):
        index = ""
        for i in self.size:
            index += "[" + i.translate()['result'] + "]"
        if self.ID.type == DATA_TYPE.BS_SEQ_INT_VAL:
            index += "[" + self.constraints.translate()['result'] + "]"
        return index

    def translate_sbox_decl(self, sym_count):
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
        res = ""
        name = self.ID.translate()["result"]
        res += "void " + name + "(uint32_t input[" + self.constraints.translate()['result'] + "]);\n"
        for i in range(0, int(self.constraints.translate()['result'])):
            res += "uint32_t " + name + "_" + str(i) + "(uint32_t A, uint32_t B, uint32_t C, uint32_t D);\n"
        return res

    def translate_qm(self, name):
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

    def translate(self, sym_count):
        result = {'emit': "", 'result': "", 'res_size' : None}
        if self.all_int_literal():
            return self.translate_int_literal_seq(sym_count, result)
        if self.type == DATA_TYPE.SEQ_BIT_VAL:
            return self.translate_bit_val_seq(sym_count)
        else:
            raise ParseException("Unknown sequence value translation")

    def translate_bit_val_seq(self, sym_count):
        return Cast.bit_seq_to_int_val(self, sym_count)
        # result = {'emit': "", 'result': "", 'res_size': None}
        # result['result'] += Target_factory.name(sym_count, "seq_bit_val")
        # result['emit'] += "uint8_t " + result['result'] + " = 0;\n"
        # result['res_size'] = len(self.value)
        # for i, element in enumerate(self.value):
        #     result['emit'] += result['result'] + " |= (" + element.translate()['result'] + " << (" + str(len(self.value) - 1) + " - " + str(i) + "));\n"
        # return result


    def translate_int_literal_seq(self, sym_count, result):
        temp_name = Target_factory.name(sym_count, "seq_val")
        seq_dimension = self.translate_seq_size()
        temp_dimension = ""
        for dim in seq_dimension:
            temp_dimension += "[" + str(dim) + "]"
        result['emit'] += Target_factory.type_decl_lookup[self.get_constraints()] + " " + temp_name + temp_dimension + ";\n"
        select_elements = itertools.product(*map(range, seq_dimension))
        for element in select_elements:
            element_l = list(element)
            result['emit'] += temp_name + self.list_to_index(element_l) + " = " + self.get_value(self.value, element_l).translate()['result'] + ";\n"
        result['result'] = temp_name
        result['res_size'] = seq_dimension
        return result

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

    # def translate_sequence_assignment(self, sym_count, dimension):
    #     for ele in self.value:



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

    def translate(self, sym_count):
        result = {'emit': "", 'result': ""}
        value = self.translate_value(sym_count)
        result['emit'] += value['emit']
        if self.node_type == DATA_TYPE.BS_BIT_DECL:
            result['emit'] += self.translate_type() + self.ID.translate()['result'] + ";\n"
        elif self.node_type == DATA_TYPE.BIT_DECL:
            result['emit'] += self.translate_type() + self.ID.translate()['result'] + ";\n"
        if self.body is not None:
            set_result = self.body.translate(sym_count)
            result['emit'] += set_result
        return result

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
                    "-": "bitslice_subtract("}

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
        if self.node_type == DATA_TYPE.SHIFT_OP:
            return self.seq_bit_shift(sym_count)
        else:
            raise InternalException("unsupported int seq operator " + self.operator)

    def seq_bit_shift(self, sym_count):
        """Translates shift or rotate of a subset of bits of an int value"""
        result = {'emit': "", 'result': ""}
        operand_1 = self.left.translate(sym_count)
        operand_2 = self.right.translate(sym_count)
        result['emit'] += operand_1['emit']
        result['emit'] += operand_2['emit']
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
            result['emit'] += result['result'] + " = " + operand_1['result'] + " << " + operand_2['result'] + ";\n"
        elif self.operator == ">>":
            result['emit'] += result['result'] + " = " + operand_1['result'] + " >> " + operand_2['result'] + ";\n"
        elif self.operator == ">>>":
            result['emit'] += result['result'] + " = " + "(" + operand_1['result'] + " >> " + operand_2['result'] + ") | (" + operand_1['result']\
                + " << " + "(" + bit_size['result'] + " - " + operand_2['result'] + "));\n"
        elif self.operator == "<<<":
            result['emit'] += result['result'] + " = " + "(" + operand_1['result'] + " << " + operand_2['result'] + ") | (" + operand_1['result']\
                + " >> " + "(" + bit_size['result'] + " - " + operand_2['result'] + "));\n"
        else:
            raise InternalException("Unrecognised shift operator " + self.operator)
        self.mask_shift(result, bit_size['result'], sym_count)
        return result

    def mask_shift(self, result, bit_size, sym_count):
        init = Target_factory.name(sym_count, "mask_loop_init")
        result['emit'] += "uint32_t " + init + " = " + bit_size + ";\n"
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
            # print(left)
            # print(right)
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
        # assert self.right.type == DATA_TYPE.INT_VAL, "Righthand side of shift needs to be integer"
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
        result = {'emit': "", 'result': ""}
        operand_for_cast = self.get_operand_for_cast()
        if self.type == DATA_TYPE.SEQ_BS_BIT_VAL:
            # print(operand_for_cast.type)
            if operand_for_cast.type == DATA_TYPE.SEQ_BIT_VAL:
                cast_res = Cast.int_to_bs_cast(sym_count, target, size)
                # result['result'] = Target_factory.name(sym_count, "casted_bs")
                # result['emit'] += "uint32_t " + result['result'] + "[" + size + "]" + "= {0};\n"
                # result['emit'] += "int_to_bitsliced(" + result['result'] + ", " + target + ", " + size + ");\n"
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
        result['result'] = operand_1['result'] + " " + self.operator + " " + operand_2['result']
        return result

    def bs_bit_compute_operation(self, sym_count):
        result = {'emit': "", 'result': ""}
        operand_1 = self.left.translate(sym_count)
        operand_2 = self.right.translate(sym_count)
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

# if __name__ == "__main__":
#     print(Target_factory.name(1))
