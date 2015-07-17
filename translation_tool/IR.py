from DATA_TYPE import DATA_TYPE
from pyparsing import ParseException
import random
from quine_mccluskey.qm import QuineMcCluskey

class Sym_count(object):

    def __init__(self):
        self.count = 0


class IR(object):

    def __init__(self):
        self._IR = []
        self.sym_count = Sym_count()

    def add(self, node):
        self.IR.append(node)

    @property
    def IR(self):
        return self._IR

    def translate(self):
        ret = ""
        for node in self.IR:
            ret += node.translate(self.sym_count)
        return ret


class Function_decl(object):

    def __init__(self, ID, return_type):
        self._ID = Name(ID, None)
        self._return_value = return_type
        self._parameters = []
        self._body = []
        self._node_type = DATA_TYPE.FUNC_DECL

    @property
    def return_type(self):
        if self._return_value == DATA_TYPE.VOID:
            return DATA_TYPE.VOID
        else:
            return self._return_value.ID.type

    @property
    def return_value(self):
        return self._return_value

    @property
    def parameters(self):
        return self._parameters

    @property
    def body(self):
        return self._body

    @property
    def node_type(self):
        return self._node_type

    @property
    def ID(self):
        return self._ID

    def translate(self, sym_count):
        ret = ""
        ret += self.translate_header()
        ret += self.translate_body(sym_count)
        ret += "}\n"
        return ret

    def translate_header(self):
        if self.return_value == DATA_TYPE.VOID:
            return "void " + self.translate_name()
        else:
            return self.return_value.translate_type() + " " + self.translate_name() + self.translate_parameters() + self.translate_dimensions()

    def translate_dimensions(self):
        ret = ""
        return_type = self.return_value.ID.type
        if DATA_TYPE.is_seq_type(return_type):
            for i, dim in enumerate(self.return_value.size):
                if i == 0:
                    ret += ")"
                else:
                    ret += "[" + dim.translate() + "]"
            ret += ")"
        if return_type == DATA_TYPE.BS_SEQ_INT_VAL:
            ret += "[" + self.return_value.constraints.value + "]"
        if return_type == DATA_TYPE.BS_INT_VAL:
            ret += ")"
        return ret

    def translate_body(self, sym_count):
        ret = "{ \n"
        for stmt in self.body:
            ret += stmt.translate(sym_count)
        return ret

    def translate_parameters(self):
        ret = "("
        for p in self.parameters:
            ret += p.translate()
            ret = ret[:-2]
            ret += ", "
        ret = ret[:-2]
        ret += ")"
        return ret

    def translate_name(self):
        return_type = self.return_value.ID.type
        if DATA_TYPE.is_seq_type(return_type) or return_type == DATA_TYPE.BS_INT_VAL:
            return "(" + "*" + self.ID.translate()["result"]
        elif return_type == DATA_TYPE.INT_VAL or return_type == DATA_TYPE.BIT_VAL:
            return self.ID.translate()
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

    # def translate(self):
    #     ret = ""
    #     ret += "if(" + self.condition.translate() + ") { \n"
    #     ret += self.translate_body()
    #     ret += "} \n"
    #     return ret

    # def translate_body(self):
    #     ret = ""
    #     for stmt in self.body:
    #         ret += stmt.translate()
    #     return ret


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

    # def translate(self, target):
    #     if self.type == DATA_TYPE.SEQ_BIT_VAL:
    #         return self.translate_bit_seq_cast(target)
    #     elif self.type == DATA_TYPE.INT_VAL:
    #         pass
    #     elif self.type == DATA_TYPE.BS_INT_VAL:
    #         return self.translate_bs_int_cast(target)
    #     else:
    #         raise ParseException(str(self.type) + " Cast not yet been done ")

    # def translate_bit_seq_cast(self, target):
    #     if target.type == DATA_TYPE.INT_VAL:
    #         return "int_to_bit_seq(" + target.translate() + ", " + self.size[0].translate() + ")"
    #     elif target.type == DATA_TYPE.BS_INT_VAL:
    #         return target.translate()
    #     else:
    #         raise ParseException("Unknown cast target type for bit seq cast " + str(target.type))

    # def translate_bs_int_cast(self, target):
    #     if target.type == DATA_TYPE.SEQ_BIT_VAL:
    #         return "bit_range_to_bs(" + target.translate() + ", " + self.constraints.translate() + ")"
    #     else:
    #         raise ParseException("Unknown cast target type for bs int cast " + str(target.type))

    @property
    def seq_size(self):
        return self._seq_size

    @property
    def constraints(self):
        return self._constraints

    @property
    def type(self):
        return self._type


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

    def translate(self, sym_count, target=None):
        result = {'emit': "", 'result': ""}
        if target is not None:
            # Assignment
            result['emit'] += self.translate_assignment_target(sym_count, target)
            return result
        else:
            target_result = self.target.translate()
            result['emit'] += target_result['emit']
            extracted_sequence = self.extract_sequence(target_result['result'], sym_count)
            result['res_size'] = extracted_sequence['res_size']
            result['emit'] += extracted_sequence['emit']
            result['result'] = extracted_sequence['result']
            return result
            # result['emit'] += target + self.translate_selection_dim() + "[" + self.indices[-1][0].translate(sym_count) + "]"

    def extract_sequence(self, target, sym_count):
        self.target.node_type == DATA_TYPE.ID, "Assumption target is just an ID at this point"
        result = {'emit': "", 'result': ""}
        if self.target.type == DATA_TYPE.BS_INT_VAL:
            extracted_seq = Target_factory.name(sym_count)
            result['emit'] += "uint32_t " + " " + extracted_seq + "[" + str(len(self.indices[-1])) + "];\n"
            result['res_size'] = str(len(self.indices[-1]))
            result['result'] = extracted_seq
            for i, index in enumerate(self.indices[-1]):
                index_translation = index.translate(sym_count)
                result['emit'] += index_translation['emit']
                result['emit'] += extracted_seq + "[" + str(i) + "]" + " = " + target + self.translate_selection_dim() + "[" + index_translation['result'] + "]" + ";\n"
        return result

    def translate_assignment_target(self, sym_count, target):
        result = {'emit': "", 'result': ""}
        target_result = self.target.translate(sym_count)
        result['emit'] += target_result['emit']
        # return result and emitted code for assignment
        if self.target.node_type == DATA_TYPE.ID:
            if self.target.type == DATA_TYPE.BS_INT_VAL:
                if 'res_size' in target:
                    for i, index in enumerate(self.indices[-1]):
                        index_translation = index.translate(sym_count)
                        result['emit'] += index_translation['emit']
                        result['emit'] += target_result['result'] + "[" + index_translation['result'] + "]" + " = " + target['result'] + "[" + str(i) + "];\n" 
                else:
                    for i, index in enumerate(self.indices[-1]):
                        index_translation = index.translate(sym_count)
                        result['emit'] += index_translation['emit']
                        result['emit'] += target_result['result'] + "[" + index_translation['result'] + "]" + " = " + target['result'] + ";\n" 
        return result['emit']


    # def translate(self):
    #     if self.target.type == DATA_TYPE.INT_VAL and self.type == DATA_TYPE.BIT_VAL:
    #         return self.translate_int_bit_select()
    #     elif self.target.type == DATA_TYPE.SEQ_BIT_VAL and self.type == DATA_TYPE.BIT_VAL:
    #         return self.select_bit_from_bit_seq()
    #     if self.target.type == DATA_TYPE.INT_VAL and self.type == DATA_TYPE.SEQ_BIT_VAL:
    #         if self.is_range():
    #             return self.extract_bit_range()
    #     elif self.target.type == DATA_TYPE.BS_INT_VAL and self.type == DATA_TYPE.BIT_VAL:
    #         return self.translate_BS_int_bit_select()
    #     elif DATA_TYPE.is_seq_type(self.type):
    #         if self.is_range():
    #             return self.extract_range()
    #         if DATA_TYPE.is_op_type(self.target.node_type):
    #             return "(" + self.target.translate() + ")"
    #         return self.target.translate()
    #     elif self.target.type == DATA_TYPE.SEQ_INT_VAL and self.type == DATA_TYPE.INT_VAL:
    #         return self.target.translate() + self.translate_selection_dim() + "[" + self.indices[-1][0].translate() + "]"
    #     elif self.target.type == DATA_TYPE.BS_SEQ_INT_VAL and self.type == DATA_TYPE.BS_INT_VAL:
    #         return self.target.translate() + self.translate_selection_dim() + "[" + self.indices[-1][0].translate() + "]"
    #     else:
    #         raise ParseException("Unsupported index selection on " + self.target.translate() + " attempted selecting " + str(self.type) + " from " + str(self.target.type))

    # def select_bit_from_bit_seq(self):
    #     assert len(self.indices[-1]) == 1, "assuming single int val for bit selection"
    #     return self.target.translate() + self.translate_selection_dim() + "[" + self.indices[-1][0].translate() + "]"

    # def extract_bit_range(self):
    #     """Returns Bit-sliced value from int val range operation"""
    #     return "extract_bit_range(" + self.target.translate() + ", " + self.indices[-1][0].start.translate() + ", " + self.indices[-1][0].finish.translate() + ")"

    # def extract_range(self):
    #     """Returns range of bits from a sequence (Seq bit, seq int, bs int)"""
    #     return "extract_range(" + self.target.translate() + ", " + self.translate_selection_dim() + self.indices[-1][0].start.translate() + ", " + self.indices[-1][0].finish.translate() + ")"

    # def translate_BS_int_bit_select(self):
    #     assert len(self.indices) == 1
    #     assert len(self.indices[0]) == 1
    #     assert self.indices[0][0].type == DATA_TYPE.INT_VAL
    #     ret = ""
    #     ret += self.target.translate() + "[" + self.indices[0][0].translate() + "]"
    #     return ret

    # def translate_int_bit_select(self):
    #     assert len(self.indices) == 1
    #     assert len(self.indices[0]) == 1
    #     assert self.indices[0][0].type == DATA_TYPE.INT_VAL
    #     ret = ""
    #     ret += "(" + "(" + self.target.translate() + " >> " + self.indices[0][0].translate() + ")" + " & 0x1" + ")"
    #     return ret

    # def value_is_list(self):
    #     for dim in self.indices:
    #         for selection in dim:
    #             if selection.node_type == DATA_TYPE.INDEX_RANGE:
    #                 return False
    #     return True

    # def translate_indices(self):
    #     assert len(self.indices) == 1
    #     assert len(self.indices[0]) == 1
    #     return self.indices[0][0].translate()

    # def is_range(self):
    #     if self.indices[-1][0].node_type == DATA_TYPE.INDEX_RANGE:
    #         assert len(self.indices[-1]) == 1, "Only single range contained in selection"
    #         return True
    #     else:
    #         return False

    # def extract_as_sequence(self):
    #     ret = ""
    #     rndm_name = self.random_name()
    #     values = self.translate_list_values(self.indices[-1])
    #     for dim in self.indices:
    #         if self.target.type == DATA_TYPE.INT_VAL:
    #             ret += Int_decl.type_decl_lookup[self.target.constraints.translate()] + " " + rndm_name + "[" + str(len(self.indices[0])) + "]" + "= {" + values + "}"
    #         elif self.target.type == DATA_TYPE.SEQ_INT_VAL:
    #             raise ParseException("Lists for Integer sequences not yet implemented")
    #         elif self.target.type == DATA_TYPE.BS_INT_VAL:
    #             ret += "uint32_t" + " " + rndm_name + "[" + str(len(self.indices[0])) + "]" + "= {" + values + "}"
    #         elif self.target.type == DATA_TYPE.BS_SEQ_INT_VAL:
    #             raise ParseException("Lists for BS INT sequences not yet implemented")
    #         elif self.target.type == DATA_TYPE.SEQ_BIT_VAL:
    #             ret += "bool" + " " + rndm_name + "[" + str(len(self.indices[0])) + "]" + "= {" + values + "}"
    #     return {"temp_seq": ret + "; \n", "name": rndm_name}

    # def translate_list_values(self, dim):
    #     values = ""
    #     if self.target.type == DATA_TYPE.INT_VAL:
    #         for selection in dim:
    #             values += "(" + self.target.translate() + " >> " + selection.translate() + ") & 0x1, "
    #         values = values[:-2]
    #     elif self.target.type == DATA_TYPE.BS_INT_VAL:
    #         for selection in dim:
    #             values += self.target.translate() + self.translate_selection_dim() + "[" + selection.translate() + "]" + ", "
    #         values = values[:-2]
    #     return values

    # def random_name(self):
    #     return ''.join(random.choice('0123456789ABCDEF') for i in range(15))

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    def translate_selection_dim(self):
        ret =""
        for i, dim in enumerate(self.indices):
            if i == len(self.indices) - 1:
                return ret
            ret += "[" + dim[0].translate() + "]"
        return ret

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
            value_result = self.value.translate(sym_count)
            result['emit'] += value_result['emit']
            if DATA_TYPE.needs_cast(self.target.type, self.value.type):
                raise ParseException("Cast needed")
            assignment_result = self.target.translate(sym_count, value_result)
            result['emit'] += assignment_result['emit']
        elif self.target.node_type == DATA_TYPE.ID:
            if DATA_TYPE.needs_cast(self.target.type, self.value.type):
                raise ParseException("Cast needed")
            if self.target.type == DATA_TYPE.INT_VAL or self.target.type == DATA_TYPE.BS_BIT_VAL or self.target.type == DATA_TYPE.BIT_VAL: 
                self.translate_integer_set(result, sym_count)
            elif self.target.type == DATA_TYPE.BS_INT_VAL:
                self.translate_bs_int_set(result, sym_count)
        else:
            raise ParseException("Unrecognised set type " + str(self.target.node_type))
        return result['emit']

    def translate_bs_int_set(self, result, sym_count):
        value_result = self.value.translate(sym_count)
        result['emit'] += value_result['emit']
        target_result = self.target.translate(sym_count)
        result['emit'] += target_result['emit']
        for i in range(int(self.target.constraints.value)):
            result['emit'] += target_result['result'] + "[" + str(i) + "]" + " = " + value_result['result'] + "[" + str(i) + "]" + ";\n"

    def translate_integer_set(self, result, sym_count):
            target_result = self.target.translate(sym_count)
            result['emit'] += target_result['emit']
            value_result = self.value.translate(sym_count)
            result['emit'] += value_result['emit']
            result['emit'] += target_result['result'] + " = " + value_result['result'] + self.translate_index(0, value_result) + ";\n"

    def translate_index(self, ele, result):
        if 'res_size' in result:
            if result['res_size'] is not None:
                return "[" + str(ele) + "]"
        return ""

    # def assign_ID(self, value):
    #     ret = ""
    #     if self.target.type == DATA_TYPE.BS_INT_VAL and self.value.type == DATA_TYPE.BS_INT_VAL:
    #         return self.target.translate_lhs(value)
    #     else:
    #         raise ParseException("Unknown assignment of" + str(self.target.type) + " to " + str(value.type))



    # def translate(self, end=True):
    #     ret = ""
    #     if self.target.node_type == DATA_TYPE.INDEX_SELECT:
    #         if self.target.target.type == DATA_TYPE.BS_INT_VAL and self.value.type == DATA_TYPE.BIT_VAL:
    #             #Setting single bit on BS int
    #             self.value.translate()
    #             ret = self.target.translate() + " = " + self.value.translate()
    #         elif self.target.type == DATA_TYPE.INT_VAL and self.value.type == DATA_TYPE.INT_VAL:
    #             print(self.target.translate())
    #             ret += self.target.translate() + " = " + self.value.translate()
    #         elif self.target.type == DATA_TYPE.BS_INT_VAL and self.value.type == DATA_TYPE.INT_VAL:
    #             ret += "bitslice_assign(" + self.target.translate() + self.target.translate_selection_dim() + ", " + self.value.translate() + ", " + self.target.constraints.translate() + ")"
    #         elif self.target.target.type == DATA_TYPE.INT_VAL and self.target.type == DATA_TYPE.BIT_VAL:
    #             # setting single bit on Int
    #             ret += self.target.target.translate() + " &= " + "(" + self.value.translate() + " << " + self.target.translate_indices() + ")"
    #         elif DATA_TYPE.is_seq_type(self.target.type):
    #             ret += self.translate_set_sequence()
    #         elif self.target.type == DATA_TYPE.BS_INT_VAL and self.value.type == DATA_TYPE.BS_INT_VAL:
    #             ret += self.translate_bs_int_val_set()
    #         else:
    #             raise ParseException("Unknown Index Select assignment of" + str(self.value.type) + " to " + str(self.target.type))
    #     elif self.target.type == DATA_TYPE.INT_VAL and self.value.type == DATA_TYPE.BS_INT_VAL:
    #         return self.value.translate()
    #     elif self.target.type == self.value.type:
    #         ret += self.target.translate() + " = " + self.value.translate()
    #     else:
    #         raise ParseException("Unknown assignment of" + str(self.value.type) + " to " + str(self.target.type))
    #     if end: 
    #         ret += ";\n"
    #     return ret

    # def translate_bs_int_val_set(self):
    #     """Setting BS val to value of another BS val"""
    #     ret = ""
    #     if self.value.node_type == DATA_TYPE.INDEX_SELECT:
    #         ### Bit sliced non integer assignment
    #         assert len(self.target.indices[-1]) == 1, "assuming single bit set.  Not Range/ list"
    #         assert self.target.indices[-1][0].node_type != DATA_TYPE.INDEX_RANGE, "assuming single bit set.  Not Range/ list"
    #         for bit in range(int(self.target.target.constraints.translate())):
    #             ret += self.target.target.name + self.target.translate_selection_dim() + "[" + self.target.indices[-1][0].translate() + "]" + "[" + str(bit) + "]"\
    #             + " = " + self.value.target.name + "[" + self.value.indices[-1][0].translate() + "]" + "[" + str(bit) + "]" + ";\n"
    #         ret = ret[:-2]
    #     elif self.value.node_type == DATA_TYPE.CAST:

    #         ret += self.target.target.name + self.target.translate_selection_dim() + "[" + self.target.indices[-1][0].translate() + "]" + " = " + self.value.translate()
    #     elif DATA_TYPE.is_op_type(self.value.node_type):
    #         ret += self.target.translate() + " = " + self.value.translate()
    #     else:
    #         raise ParseException("Unsupported bitsliced assignment")
    #     return ret

    # def translate_set_sequence(self):
    #     ret = ""
    #     for i, selection in enumerate(self.target.indices[-1]):
    #         if selection.node_type == DATA_TYPE.INDEX_RANGE:
    #             #  Assignment to a range select
    #             ret += self.translate_range_select_assignment(selection, i)
    #                 # ret += "range_assignment(" + self.target.translate() + self.target.translate_selection_dim() + ","\
    #                 #     + self.value.translate() + self.value.translate_selection_dim() + ", " + selection.start.translate() + ", " + selection.finish.translate() + ", " + "); \n"
    #         else:
    #             ret += self.target.translate() + self.target.translate_selection_dim() + "[" + selection.translate() + "]" + "=" +\
    #                 self.value.translate() + self.value.translate_selection_dim() + "[" + str(i) + "]" + "; \n"
    #     return ret

    # def translate_range_select_assignment(self, selection, i):
    #     """Carries out different translation depending on whether sequence value to be assigned is indexed using a list or a range """
    #     ret = ""
    #     if DATA_TYPE.is_op_type(self.value.node_type):
    #         ret += "sequence_assignment(" + self.target.target.name + self.target.translate_selection_dim() + ","\
    #             + self.value.translate() + ", " +\
    #             selection.start.translate() + ", " + selection.finish.translate() +\
    #             ", 0, " + selection.finish.translate() + "-" + selection.start.translate() + ")"
    #     elif self.value.is_range():
    #         ret += "sequence_assignment(" + self.target.target.name + self.target.translate_selection_dim() + ","\
    #             + self.value.translate() + self.value.translate_selection_dim() + ", " + selection.start.translate() + ", " +\
    #             selection.finish.translate() + ", " + self.value.indices[-1][0].start.translate() + ", " +\
    #             self.value.indices[-1][0].finish.translate() + ")"
    #     elif self.value.value_is_list():
    #         extraction = self.value.extract_as_sequence()
    #         ret += extraction["temp_seq"]
    #         ret += "sequence_assignment(" + self.target.target.name + self.target.translate_selection_dim() + self.target.translate_selection_dim() + ","\
    #             + extraction['name'] + ", " + selection.start.translate() + ", " +\
    #             selection.finish.translate() + ", " + selection.start.translate() + ", " +\
    #             selection.finish.translate() + ")"
    #     else:
    #         raise ParseException("Tried to set type of feature not yet implemented....")
    #     return ret


class Return(object):
    def __init__(self, expr):
        self._target = expr
        self._type = expr.type
        self.node_type = DATA_TYPE.RETURN_STMT

    @property
    def target(self):
        return self._target

    @property
    def type(self):
        return self._type

    def translate(self, sym_count):
        target = self.target.translate()
        ret = target['emit']
        return "return " + target['result'] + ";\n"


class Seq_decl(object):

    def __init__(self, node_type, size, var_id, value=None, constraints=None):
        self._ID = Name(var_id, DATA_TYPE.decl_to_value(node_type))
        self._node_type = node_type
        self._size = size
        self._value = value
        self._constraints = constraints

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

    def translate(self):
        return self.translate_type() + " " + self.ID.translate() + self.translate_size() + "; \n"
        if self.node_type == DATA_TYPE.SEQ_INT_DECL:
            return self.translate_int_seq()
        elif self.node_type == DATA_TYPE.SEQ_BIT_DECL:
            return self.translate_bit_seq()
        elif self.node_type == DATA_TYPE.BS_SEQ_INT_DECL:
            return self.translate_bs_int_seq()
        else:
            raise ParseException("Translation of Unknown Sequence Type attempted")

    # def translate_as_parameter(self):
    #     ret = self.translate_type() + " " + self.ID.translate()
    #     for dim in self.size:
    #         ret += "[" + dim.translate() + "]"
    #     if self.ID.type == DATA_TYPE.BS_SEQ_INT_VAL or self.ID.type == DATA_TYPE.BS_INT_VAL:
    #         ret += "[" + self.constraints.translate() + "]"
    #     return ret
    #     if self.node_type == DATA_TYPE.SEQ_INT_DECL:
    #         return self.translate_int_seq_param()
    #     elif self.node_type == DATA_TYPE.SEQ_BIT_DECL:
    #         return self.translate_bit_seq_param()
    #     elif self.node_type == DATA_TYPE.BS_SEQ_INT_DECL:
    #         return self.translate_bs_int_seq_param()
    #     else:
    #         raise ParseException("Translation of Unknown Sequence Type attempted")

    # def translate_int_seq(self):
    #     if self.size_is_literal():
    #         return self.translate_type() + " " + self.ID.translate() + self.translate_size()
    #     else:
    #         self.translate_variable_size()

    # def translate_size(self):
    #     if self.size_is_literal():
    #         ret = self.translate_constant_size()
    #     else:
    #         ret = self.translate_variable_size()
    #     return ret

    # def translate_variable_size():
    #     raise ParseException("Variable size Arrays not yet supported")

    # def translate_constant_size(self):
    #     ret = ""
    #     for expr in self.size:
    #         ret += "[" + expr.translate() + "]"
    #     if self.node_type == DATA_TYPE.BS_SEQ_INT_DECL:
    #         ret += "[" + self.constraints.translate() + "]"
    #     return ret

    # def size_is_literal(self):
    #     for expr in self.size:
    #         if expr.node_type == DATA_TYPE.INT_LITERAL:
    #             pass
    #         else:
    #             return False
    #     return True

    # def translate_type(self):
    #     if self.node_type == DATA_TYPE.SEQ_INT_DECL or DATA_TYPE.BS_SEQ_INT_DECL:
    #         return "uint32_t"
    #     elif self.node_type == DATA_TYPE.SEQ_BIT_DECL:
    #         return "bool"
    #     else:
    #         raise ParseException("Translation of Unknown sequence type attempted")

    # def translate_bs_int_seq(self):
    #     if self.size_is_literal():
    #         return self.translate_type() + " " + self.ID.translate() + self.translate_size()
    #     else:
    #         self.translate_variable_size()

    # def translate_bit_seq(self):
    #     pass


class Seq_val(object):

    def __init__(self, s_type=None, value=None):
        self._value = []
        if value is not None:
            self._value.append(value)

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


class Bit_decl(object):

    def __init__(self, var_id, value=None):
        self._ID = var_id
        self._node_type = DATA_TYPE.BIT_DECL
        self._value = value

    @property
    def node_type(self):
        return self._node_type

    @property
    def value(self):
        return self._value

    @property
    def ID(self):
        return self._ID

    # def translate(self):
    #     return "bool " + self.ID.translate() + self.translate_value()

    # def translate_value(self):
    #     if self.value is None:
    #         return ""
    #     else:
    #         return " = " + self.value.translate()

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
        self._value = value
        self._node_type = n_type

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

    def translate(self, sym_count=None):
        result = {'emit': "", 'result': ""}
        if self.node_type == DATA_TYPE.BS_INT_DECL:
            result['emit'] += self.translate_type() + self.ID.translate()["result"] + "[" + self.constraints.translate()['result'] + "]" + ";\n"
        elif self.node_type == DATA_TYPE.INT_DECL:
            result['emit'] += self.translate_type() + self.ID.translate()["result"] + ";\n"
            if self.value is not None:
                value_result = self.value.translate(sym_count)
                result['emit'] += value_result['emit']
                assignment_result = self.assign_int_val(value_result)
                result['emit'] += assignment_result['emit']
        return result['emit']

    def assign_int_val(self, value_result):
        result = {'emit': "", 'result': ""}
        if self.value.type == DATA_TYPE.INT_VAL:
            result['emit'] += self.ID.translate()['result'] + " = " + value_result['result'] + ";\n"  
        return result

    # def translate_value(self):
    #     ret = ""
    #     if self.value is None:
    #         return ""
    #     else:
    #         if self.node_type == DATA_TYPE.BS_INT_DECL:
    #             if self.value.type == DATA_TYPE.INT_VAL:
    #                 return "bitslice_assign(" + self.ID.translate() + ", " + self.value.translate() + ", " + self.constraints.value + ")" 
    #             elif self.value.type == DATA_TYPE.BS_INT_VAL:
    #                 for bit in range(int(self.constraints.translate())):
    #                     ret += self.ID.translate() + "[" + str(bit) + "] = " + self.translate_value_to_bs(bit) + ";\n"
    #                 ret = ret[:-2]
    #                 return ret
    #         else:
    #             return " = " + self.value.translate()

    # def translate_value_to_bs(self, bit):
    #     assert DATA_TYPE.is_int_val(self.value.type), "Value to translate to bs is integer value in Int DECL"
    #     if self.value.type == DATA_TYPE.INT_VAL:
    #         return "(" + self.value.translate() + ")" + ">>" + str(bit) + "& 0x1"
    #     elif self.value.type == DATA_TYPE.BS_INT_VAL:
    #         return self.value.translate() + "[" + str(bit) + "]"

    # def translate_as_stmt(self, sym_count):
    #     ret = ""
    #     if self.node_type == DATA_TYPE.BS_INT_DECL:
    #         ret += self.translate_type() + self.ID.translate() + "[" + self.constraints.translate() + "]" + ";\n"
    #         if self.value is not None:
    #             ret += self.translate_value() + ";\n"
    #     elif self.node_type == DATA_TYPE.INT_DECL:
    #         ret = self.translate_type() + self.ID.translate() + self.translate_value() + ";\n"
    #     return ret

    def translate_type(self):
        if self.constraints.value in Int_decl.type_decl_lookup:
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

    # def translate(self):
    #     return self.value


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

    def __init__(self, f_id, return_type, return_value):
        self._f_id = Name(f_id, return_type)
        self._parameters = []
        self._return_value = return_value

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

    # def translate(self):
    #     ret = ""
    #     ret += self.f_id.translate() + "("
    #     for p in self.parameters:
    #         ret += p.translate() + ", "
    #     ret = ret[:-2]
    #     return ret


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
        result['emit'] += self.translate_initializer(sym_count)
    #     ret += "; "
    #     ret += self.translate_terminator()
    #     ret += "; "
    #     ret += self.translate_increment()
    #     ret += ") { \n"
    #     ret += self.translate_body()
    #     ret += "} \n"
    #     return ret

    def translate_initializer(self, sym_count):
        result = {'emit': "", 'result': ""}
        for_loop = "for("
        for stmt in self.initializer:
            if DATA_TYPE.is_declaration(stmt.node_type):
                result['emit'] += stmt.translate(sym_count)
            else:
                for_loop += stmt.translate(sym_count) + ", "
        if for_loop[-2] == ',':
            for_loop = for_loop[:-2]
        result['emit'] += for_loop
        return result['emit']

    # def translate_body(self):
    #     ret = ""
    #     for stmt in self.body:
    #         ret += stmt.translate()
    #     ret += '\n'
    #     return ret

    # def translate_increment(self):
    #     ret = ""
    #     for expr in self.increment:
    #         ret += expr.translate(False) + ", "
    #     ret = ret[:-2]
    #     return ret

    # def translate_terminator(self):
    #     if len(self.increment) > 1:
    #         raise ParseException("Internal Errror: Several stmts in increment in for loop.")
    #     return self.terminator[0].translate()


class Binary_operation(object):

    # operations_lookup = {DATA_TYPE.COMP_OP: lambda self: self.translate_comparisons(),
    #                      DATA_TYPE.ARITH_OP: lambda self, sym_count: self.translate_arithmetic(sym_count),
    #                      DATA_TYPE.BITWISE_OP: lambda self, sym_count: self.translate_bitwise(sym_count),
    #                      DATA_TYPE.SHIFT_OP: lambda self, sym_count: self.translate_shift(sym_count),
    #                      DATA_TYPE.LOG_OP: lambda self: self.translate_logical()}

    operations_lookup = {DATA_TYPE.INT_VAL: lambda self, sym_count: self.int_int_operation(sym_count),
                         DATA_TYPE.BIT_VAL: lambda self, sym_count: self.int_int_operation(sym_count),
                         DATA_TYPE.BS_BIT_VAL: lambda self, sym_count: self.int_int_operation(sym_count),
                         DATA_TYPE.BS_INT_VAL: lambda self, sym_count: self.bs_int_operation(sym_count)}

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

    def bs_int_operation(self, sym_count):

        if self.node_type == DATA_TYPE.SHIFT_OP:
            return self.bs_shift_operation(sym_count)

    def bs_shift_operation(self, sym_count):
        result = {'emit': "", 'result': "", 'res_size_1': None, 'res_size_2': None}
        temp_target = self.target_decl(sym_count)
        result['emit'] += temp_target['emit']
        result['result'] = temp_target['result']
        operand_1 = self.left.translate(sym_count)
        operand_2 = self.right.translate(sym_count)
        result['emit'] += operand_1['emit']
        result['emit'] += operand_2['emit']
        assert self.right.type == DATA_TYPE.INT_VAL, "Righthand side of shift needs to be integer"
        result['emit'] += "bitslice_shift(" + temp_target['result'] + ", " + operand_1['result'] + ", " + operand_2['result']\
            + ", " + self.constraints.translate()['result'] + ", " + "\"" + self.operator + "\"" + ");\n"
        return result

    # def translate_shift(self, target, sym_count):
    #     assert self.right.type == DATA_TYPE.INT_VAL, "Shift input should always be integer value"
    #     if self.left.type == DATA_TYPE.INT_VAL:
    #         ret = self.translate_int_shift()
    #     elif self.left.type == DATA_TYPE.BS_INT_VAL:
    #         ret = self.translate_bs_shift(target, sym_count)
    #     return ret

    # def determine_result_size(self):
    #     if self.right.constraints is not None and self.left.constraints is not None:
    #         if int(self.right.constraints) >= int(self.left.constraints):
    #             self.constraints = self.right.constraints
    #             return self.right.constraints
    #         else:
    #             self.constraints = self.left.constraints
    #             return self.left.constraints
    #     raise ParseException("Target Has no constraints")

    # def translate_operand(self, operand):
    #     if operand.node_type == DATA_TYPE.ID:
    #         return {"target": operand.translate()}
    #     elif operand.node_type == DATA_TYPE.INT_LITERAL:
    #         return {"target": operand.translate()}
    #     elif operand.node_type == DATA_TYPE.INDEX_SELECT:
    #         return {"target": operand.translate()}
    #     else:
    #         raise ParseException("Trying to translate unknown operand " + str(operand.node_type))

    # def translate_int_shift(self):
    #     ret = ""
    #     ret += self.left.translate() + " " + self.operator + " " + self.left.translate()
    #     return ret

    # def translate_int_val_bitwise(self):
    #     ret = ""
    #     cnst = None
    #     if int(self.left.constraints.translate()) > int(self.right.constraints.translate()):
    #         cnst = self.left.constraints.translate()
    #     else:
    #         cnst = self.right.constraints.translate()
    #     if self.left.type == DATA_TYPE.BS_INT_VAL and self.right.type != DATA_TYPE.BS_INT_VAL:
    #         ret += "bitwise_bs(" + self.left.translate() + ", " + "bitslice(" + self.right.translate() + ", " + self.right.constraints.translate() +\
    #             "), \"" + self.operator + "\"" + ", " + cnst+ ")"
    #     elif self.left.type != DATA_TYPE.BS_INT_VAL and self.right.type == DATA_TYPE.BS_INT_VAL:
    #         ret += "bitwise_bs(" + "bitslice(" + self.left.translate() + "," + self.left.constraints.translate() + "), "\
    #             + self.right.translate() + ", \"" + self.operator + "\"" + ", " + cnst + ")"
    #     elif self.left.type != DATA_TYPE.BS_INT_VAL and self.right.type != DATA_TYPE.BS_INT_VAL:
    #         ret += self.left.translate() + " \"" + self.operator + "\" " + self.right.translate()
    #     else:
    #         ret += "bitwise_bs(" + self.left.translate() + ", " + self.right.translate() + ", \"" + self.operator + "\"" + ", " + cnst + ")"
    #     return ret

    # def translate_bit_seq_bitwise(self):
    #     return "seq_bitwise(" + self.left.translate() + ", " + self.right.translate() + ", " + "\"" + self.operator + "\"" + ")"

    def int_int_operation(self, sym_count):
        result = {'emit': "", 'result': "", 'res_size_1': None, 'res_size_2': None}
        temp_target = self.target_decl(sym_count)
        operand_1 = self.left.translate(sym_count)
        operand_2 = self.right.translate(sym_count)
        if 'res_size' in operand_1:
            result['res_size_1'] = operand_1['res_size']

        if 'res_size' in operand_2:
            result['res_size_2'] = operand_2['res_size']
        result['emit'] += temp_target['emit']
        result['emit'] += operand_1['emit']
        result['emit'] += operand_2['emit']

        if result['res_size_1'] is not None or result['res_size_2'] is not None:
            # Index select operation
            for i in range(int(self.get_size(result))):
                result['emit'] += temp_target['result'] + " = " + operand_1['result'] + self.translate_index(i, result['res_size_1']) + " " + self.operator +\
                " " + operand_2['result'] + self.translate_index(i, result['res_size_2']) + ";\n"
        else:
            result['emit'] += temp_target['result'] + " = " + operand_1['result'] + " " + self.operator + " " + operand_2['result'] + ";\n"
        result['result'] = temp_target['result']
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


    # def translate_bitwise(self, sym_count):
    #     result = {'emit': "", 'result': ""}
    #     temp_target = self.target_decl(sym_count)
    #     operand_1 = self.left.translate(sym_count)
    #     operand_2 = self.right.translate(sym_count)
    #     result['emit'] += temp_target['emit']
    #     result['emit'] += operand_1['emit']

    #     result['emit'] += operand_2['emit']
    #     result['emit'] += temp_target['result'] + " = " + operand_1['result'] + " " + self.operator + " " + operand_2['result'] + ";\n"
    #     result['result'] = temp_target['result']
    #     return result

    def target_decl(self, sym_count):
        result = {'emit': "", 'result': "", 'res_size': None}
        if self.type == DATA_TYPE.INT_VAL:
            result['result'] += Target_factory.name(sym_count) + "_bin"
            result['emit'] += Target_factory.type_decl_lookup[self.constraints.translate()['result']] + " " + result['result'] + ";\n"
        elif self.type == DATA_TYPE.BIT_VAL:
            result['result'] += Target_factory.name(sym_count) + "_bin"
            result['emit'] += "Bit" + " " + result['result'] + ";\n"
        elif self.type == DATA_TYPE.BS_BIT_VAL:
            result['result'] += Target_factory.name(sym_count) + "_bin"
            result['emit'] += "uint32_t" + " " + result['result'] + ";\n"
        elif self.type == DATA_TYPE.BS_INT_VAL:
            result['result'] += Target_factory.name(sym_count) + "_bin"
            result['emit'] += "uint32_t" + " " + result['result'] + "[" + self.constraints.translate(sym_count)['result'] + "]" + ";\n"
            result['res_size'] = self.constraints.translate(sym_count)['result']
        else:
            raise ParseException("Need Type declaration " + str(self.type))
        return result

    # def translate_comparisons(self):
    #     if DATA_TYPE.is_int_val(self.right.type) and DATA_TYPE.is_int_val(self.left.type):
    #         return self.translate_int_val_compare()
    #     if self.left.type == DATA_TYPE.BIT_VAL and self.right.type == DATA_TYPE.BIT_VAL:
    #         return self.translate_bit_compare()

    # def translate_bit_compare(self):
    #     return self.left.translate() + " " + self.operator + " " + self.right.translate()

    # def translate_bs_shift(self, target, sym_count):
    #     ret, left_result, right_result = self.translate_children(target, sym_count)
    #     ret += target.translate()
    #     ret += "shift_bs(" + target.ID.name + ", " + left_result['target'].translate() + ", " + target.constraints.translate() + ", " + right_result['target'].translate() + ", " + "\"" + self.operator + "\"" + ")" + ";\n"
    #     return {"code": ret, "target": Target_factory().decl_to_id(target)}

    # def translate_bit_val_bitwise(self, target, sym_count):
    #     ret, left_result, right_result = self.translate_children(target, sym_count)
    #     ret += target.translate()
    #     ret = left_result['target'].translate() + " " + self.operator + " " + right_result['target'].translate()
    #     ret = "(" + ret + ")"
    #     print(ret)
    #     return {"code": ret, "target": Target_factory().decl_to_id(target)}

    # def translate_children(self, target, sym_count):
    #     ret = ""
    #     left_result = {}
    #     right_result = {}
    #     if DATA_TYPE.is_op_type(self.left.node_type):
    #         left_result = self.left.translate_rhs(Target_factory().make_temp_target(self.left, target.ID.name[:-2], sym_count), sym_count)
    #         ret += left_result['code']
    #     else:
    #         left_result['target'] = self.left
    #     if DATA_TYPE.is_op_type(self.right.node_type):
    #         right_result = self.left.translate_rhs(Target_factory().make_temp_target(self.right, target.ID.name[:-2], sym_count), sym_count)
    #         ret += right_result['code']
    #     else:
    #         right_result['target'] = self.right
    #     return (ret, left_result, right_result)

    # def translate_logical(self):
    #     return "(" + self.left.translate() + " " + self.operator + " " + self.right.translate() + ")"

    # def translate_int_val_arithmetic(self):
    #     if self.right.type == DATA_TYPE.BS_INT_VAL and self.left.type != DATA_TYPE.BS_INT_VAL:
    #         ret = "arith_bs(bitslice(" + self.left.translate() + "," + self.left.constraints.translate() + ")," + self.right.translate() + "," + self.operator + ")"
    #     elif self.left.type == DATA_TYPE.BS_INT_VAL and self.right.type != DATA_TYPE.BS_INT_VAL:
    #         ret = "arith_bs(" + self.left.translate() + "," + "bitslice(" + self.right.translate() + "," + self.right.constraints.translate() + ")" + "," + self.operator + ")"
    #     elif self.left.type == DATA_TYPE.BS_INT_VAL and self.right.type == DATA_TYPE.BS_INT_VAL:
    #         ret = "arith_bs(" + self.left.translate() + "," + self.right.constraints() + "," + self.operator + ")"
    #     else:
    #         ret = self.left.translate() + " " + self.operator + " " + self.right.translate()
    #     return ret

    # def translate_int_val_compare(self):
    #     if self.right.type == DATA_TYPE.BS_INT_VAL and self.left.type != DATA_TYPE.BS_INT_VAL:
    #         ret = "compare_bs(bitslice(" + self.left.translate() + "," + self.left.constraints.translate() + ")," + self.right.translate() + "," + self.operator + ")"
    #     elif self.left.type == DATA_TYPE.BS_INT_VAL and self.right.type != DATA_TYPE.BS_INT_VAL:
    #         ret = "compare_bs(" + self.left.translate() + "," + "bitslice(" + self.right.translate() + "," + self.right.constraints.translate() + ")" + "," + self.operator + ")"
    #     else:
    #         ret = self.left.translate() + " " + self.operator + " " + self.right.translate()
    #     return ret

    # def translate_rhs(self, target, sym_count):
    #     return Binary_operation.operations_lookup[self.node_type](self, target, sym_count)

    def translate(self, sym_count):
        # return Binary_operation.operations_lookup[self.node_type](self, sym_count)
        return Binary_operation.operations_lookup[self.type](self, sym_count)


class Target_factory(object):

    type_decl_lookup = {"8": "uint8_t ",
                        "16": "uint16_t ",
                        "32": "uint32_t ",
                        "64": "uint64_t "}

    def name(sym_count):
        # name =  "__" + "temp" + "_" + ''.join(random.choice('0123456789ABCDEF') for i in range(4)) + "_" + str(sym_count.count)
        name = "__" + "temp" + "_" + str(sym_count.count)
        sym_count.count += 1
        return name

#     def make_temp_target(self, target, name, sym_count):
#         pre = self.construct_prefix(name)
#         if target.node_type == DATA_TYPE.ID:
#             if DATA_TYPE.is_int_val(target.type):
#                 temp = Int_decl(DATA_TYPE.val_to_decl(target.type), target.constraints, Name(pre + name + "_" + str(sym_count.count), target.type))
#         elif target.node_type == DATA_TYPE.INDEX_SELECT:
#             if target.type == DATA_TYPE.BIT_VAL and target.target.node_type == DATA_TYPE.ID:
#                 temp = Bit_decl(Name(pre + name + "_" + str(sym_count.count), target.type))
#         elif target.node_type == DATA_TYPE.BITWISE_OP:
#             if target.type == DATA_TYPE.BIT_VAL:
#                 temp = Bit_decl(Name(pre + name + "_" + str(sym_count.count), target.type))
#         else:
#             raise ParseException("Tried to make copy of unknown type " + str(target.node_type))
#         sym_count.count += 1
#         return temp

#     def construct_prefix(self, name):
#         if name[0] == "_" and name[1] == "_":
#             return ""
#         else:
#             return "__"

#     def decl_to_id(self, decl):
#         node_type = DATA_TYPE.decl_to_value(decl.node_type)
#         if DATA_TYPE.is_int_val(node_type):
#             return Name(decl.ID.translate(), node_type, constraints=decl.constraints)
#         elif node_type == DATA_TYPE.BIT_VAL:
#             return Name(decl.ID.translate(), node_type)
#         else:
#             raise ParseException("Tried to transform unknown type " + str(node_type))


# if __name__ == "__main__":
#     print(Target_factory.name(1))
