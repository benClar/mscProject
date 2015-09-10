from Symbol_Table import Symbol_Table
from Stack import Stack
# from IR import IR_Tree, Seq_node, Decl_node, Type_node, Name_node, Literal_node,\
#     Tree
from pyparsing import ParseException
from DATA_TYPE import DATA_TYPE
from IR import Int_literal, Name, Int_decl, Set, Bit_literal, Binary_operation,\
    Cast_operation, Cast, IR, Call, Bit_decl, Seq_decl, Seq_val, If_stmt, For_loop,\
    Function_decl, Index_select, Element_range, Return, Int_literal
import sys
from Translation_exceptions import SemanticException, InternalException, Semantic_analysis_errors

class Semantic_analyser(object):

    node_type_lookup = {DATA_TYPE.INT_DECL: lambda self, node: self.analyse_int_decl(node),
                        DATA_TYPE.BIT_DECL: lambda self, node: self.analyse_bit_decl(node),
                        DATA_TYPE.ID_SET: lambda self, node: self.analyse_ID_set(node),
                        DATA_TYPE.FUNC_DECL: lambda self, node: self.analyse_func_decl(node),
                        DATA_TYPE.IF_STMT: lambda self, node: self.analyse_if_stmt_decl(node),
                        DATA_TYPE.FOR_LOOP: lambda self, node: self.analyse_for_loop_decl(node),
                        DATA_TYPE.SEQ_INT_DECL: lambda self, node: self.analyse_bit_cnst_seq(node),
                        DATA_TYPE.SEQ_BIT_DECL: lambda self, node: self.analyse_bit_seq(node),
                        DATA_TYPE.BS_SEQ_INT_DECL: lambda self, node: self.analyse_bit_cnst_seq(node),
                        DATA_TYPE.BS_INT_DECL: lambda self, node: self.analyse_int_decl(node),
                        DATA_TYPE.SBOX_DECL: lambda self, node: self.analyse_bit_cnst_seq(node),
                        DATA_TYPE.EXPR: lambda self, node: self.analyse_expr(node),
                        DATA_TYPE.BS_BIT_DECL: lambda self, node: self.analyse_bit_decl(node)}
    def __init__(self):
        self._sym_table = Symbol_Table()
        self._IR = IR()

    @property
    def IR(self):
        return self._IR

    @property
    def sym_table(self):
        return self._sym_table

    def convert_base(self, val):
        if len(val) > 1 and val[1] == 'x':
            return int(val, 16)
        elif len(val) > 1 and val[1] == 'b':
            return int(val, 2)
        else:
            return int(val)

    def convert_base_to_str(self, tokens):
        return str(self.convert_base(tokens[0]))

    def convert_to_bin_str(self, val):
        """Converts hex and bin bases to dec

        Args:
        val: Int literal value that has just been parsed"""
        if len(val) > 1 and val[1] == 'x':
            return str(int(val, 16)).zfill((len(val) - 2) - len(int(val, 16)) * 4)
        elif len(val) > 1 and val[1] == 'b':
            return str(int(val, 2)).zfill((len(val) - 2) - len(int(val, 2)))
        else:
            return str(int(val)).zfill((len(val)) - len(int(val)))

    def collect_indices(self, indices):
        """Creates appropriate IR nodes for index operations.

        Args:
        indices: selection of syntax tree nodes representing indices"""
        collected_indices = []
        for i in indices:
            if len(i.expressions) > 1:
                indices_list = []
                for ele in i.expressions:
                    new_ind = self.expr_type_is(ele)
                    if self.allowed_index_range(new_ind.type):
                        indices_list.append(new_ind)
                    else:
                        raise SemanticException("Cannot use " + new_ind.type + " as Lookup value in Sequence")
                collected_indices.append(indices_list)
            else:
                new_ind = self.expr_type_is(i)
                if self.allowed_index_range(new_ind.type):
                    collected_indices.append([new_ind])
                else:
                    raise SemanticException("Cannot use " + str(new_ind.type) + " as Lookup value in Sequence")
        return collected_indices

    def allowed_index_range(self, type_input):
        """List of allowed types to be used as index lookups

        Args:
        type_input: Type being used as index lookup"""
        allowed_index_range = [DATA_TYPE.INT_VAL, DATA_TYPE.BS_INT_VAL, DATA_TYPE.SEQ_BIT_VAL, DATA_TYPE.SEQ_BS_BIT_VAL, None]
        if type_input in allowed_index_range:
            return True
        return False

    def index_set(self, node):
        """Analyses index set statement and produces IR node

        Args:
        node: Syntax tree node to be analysed"""
        id_set = None
        id_set = Set(self.analyse_index_sel(node.target), self.expr_type_is(node.value))
        # if DATA_TYPE.is_seq_type(id_set.target.type) and DATA_TYPE.is_seq_type(id_set.value.type):
        #     pass
        if id_set.target.target.node_type == DATA_TYPE.CAST:
            if self.get_cast_target(id_set.target.target) != DATA_TYPE.ID:
                raise SemanticException("Cannot assign to a " + str(self.get_cast_target(id_set.target.target)))
        if self.can_assign_type(id_set.target.type, id_set.value.type) is False:
            raise SemanticException(str(id_set.value.type) + " Cannot be assigned to " + str(id_set.target.type))
        self.check_set_dimensions(id_set.target, id_set.value)
        return id_set

    def check_set_dimensions(self, target, value):
        """Checks that dimensions make sense for sequence sets.
        Args:
        target: Target node of set.
        value: Value node of set."""
        if target.type == DATA_TYPE.SEQ_BIT_VAL and value.type == DATA_TYPE.INT_VAL:
            if len(target.indices) < len(self.sym_table.id(target.target.name)['size']) - 1:
                raise SemanticException("Cannot Assign " + str(DATA_TYPE.INT_VAL) + " To " + str(DATA_TYPE.SEQ_BIT_VAL) + ('[]' * (len(self.sym_table.id(target.target.name)['size']) - len(target.indices))))


    def get_cast_target(self, target):
        """Returns target that requires cast.

        Args:
        target: node to examine"""
        if target.node_type == DATA_TYPE.CAST:
            return self.get_cast_target(target.target)
        else:
            return target.node_type

    # def analyse_seq_index_set(self, ast_node):
    #     """Analyses index set on a sequence.

    #     Args:
    #     ast_node: Syntax tree node holding statement"""
    #     id_set = Set(self.build_seq_index_ir(ast_node.target, self.collect_indices(ast_node.target.indices)),  self.expr_type_is(ast_node.value))
    #     self.validate_id_seq_set(id_set, ast_node)
    #     return id_set

    # def analyse_int_index_set(self, ast_node):
    #     id_set = Set(Index_select(Name(ast_node.target.ID, self.sym_table.id_type(ast_node.target.ID)), self.collect_indices(ast_node.target.indices)),  self.expr_type_is(ast_node.value))
    #     if self.is_range(id_set.target.indices[0]):
    #         id_set.target.type = DATA_TYPE.SEQ_BIT_VAL
    #     elif len(id_set.target.indices) > 1:
    #         raise SemanticException("Cannot treat Integer value as a 2d bit array")
    #     else:
    #         id_set.target.type = DATA_TYPE.BIT_VAL
    #     if self.value_matches_expected(id_set.value.type, id_set.target.type) is False:
    #         raise SemanticException(str(id_set.value.type) + " cannot be assigned to variable of type " + str(id_set.target.type))

    def check_index_in_limit(self, index_id, indices):
        """Checks that index is inside bounds if it is an integer literal

        Args
        Index_id: ID of target of index.
        indices: indices being used for index select."""
        for dim, index in enumerate(indices):
            for i in index:
                if i.node_type == DATA_TYPE.INT_LITERAL:
                    try:
                        if int(i.value) >= int(self.sym_table.id(index_id)['size'][dim].value):
                            raise SemanticException("Index Selection out of range")
                    except IndexError:
                        pass
                    except TypeError:
                        if self.sym_table.id(index_id)['type'] == DATA_TYPE.BS_INT_VAL or self.sym_table.id(index_id)['type'] == DATA_TYPE.INT_VAL:
                            if int(i.value) > int(self.sym_table.id(index_id)['constraints'].value):
                                raise SemanticException("Index Selection out of variable bit width")

    def can_assign_type(self, target_type, value_type):
        """types that can be assigned to one another.

        Args:
        target_type: type of target of asignment.
        value_type: type of value of assignment"""
        allowed_values = {DATA_TYPE.SEQ_INT_VAL: [DATA_TYPE.SEQ_INT_VAL, DATA_TYPE.BS_SEQ_INT_VAL],
                          DATA_TYPE.BS_SEQ_INT_VAL: [DATA_TYPE.SEQ_INT_VAL, DATA_TYPE.BS_SEQ_INT_VAL],
                          DATA_TYPE.SEQ_BIT_VAL: [DATA_TYPE.SEQ_BIT_VAL, DATA_TYPE.INT_VAL],
                          DATA_TYPE.INT_VAL: [DATA_TYPE.INT_VAL, DATA_TYPE.SEQ_BIT_VAL],
                          DATA_TYPE.BS_INT_VAL: [DATA_TYPE.INT_VAL, DATA_TYPE.BS_INT_VAL, DATA_TYPE.SEQ_BS_BIT_VAL, DATA_TYPE.SEQ_BIT_VAL],
                          DATA_TYPE.BIT_VAL: [DATA_TYPE.BIT_VAL],
                          DATA_TYPE.BS_BIT_VAL: [DATA_TYPE.BS_BIT_VAL, DATA_TYPE.BIT_VAL],
                          DATA_TYPE.SEQ_BS_BIT_VAL: [DATA_TYPE.SEQ_BS_BIT_VAL, DATA_TYPE.BS_INT_VAL, DATA_TYPE.SEQ_BIT_VAL, DATA_TYPE.INT_VAL]}
        if value_type in allowed_values[target_type]:
            return True
        return False

    def is_range(self, indices):
        """Returns true if there is a range operation in indices.

        Args:
        indices to check."""
        if(len(indices) > 1):
            return True
        if indices[0].node_type == DATA_TYPE.INDEX_RANGE:
                return True
        return False

    # def validate_cast_seq_set(self, id_set):
    #     if len(id_set.target.indices) > 1:
    #         raise SemanticException(str(id_set.target.type) + len(id_set.target.indices) * "[]" + " cannot set " + str(id_set.target.type) + "[]")

    # def validate_id_seq_set(self, id_set, node):
    #     if len(id_set.target.indices) == self.sym_table.dimension(node.target.ID):
    #         if self.value_matches_expected(DATA_TYPE.seq_to_index_sel(id_set.target.type), id_set.value.type) is False:
    #             raise SemanticException(str(DATA_TYPE.seq_to_index_sel(id_set.target.type)) + " Cannot be set to " + str(id_set.value.type))
    #     elif len(id_set.target.indices) > self.sym_table.dimension(node.target.ID):
    #         if (id_set.target.type == DATA_TYPE.BS_SEQ_INT_VAL or id_set.target.type == DATA_TYPE.SEQ_INT_VAL) and (len(node.indices) == len(id_set.target.indices) + 1):
    #             pass
    #         else:
    #             raise SemanticException(str(self.sym_table.id(node.target.ID)['type']) + str("[]" * self.sym_table.dimension(node.target.ID)) + " cannot be set to " + "[]" * len(id_set.target.indices))  # NOQA
    #     else:
    #         if self.value_matches_expected(id_set.target.target.type, id_set.value.type) is False:
    #             raise SemanticException(str(id_set.target.target.type) + " Cannot be set to " + str(id_set.value.type))

    def analyse_ID_set(self, node):
        """Analyses ID set statement.

        Args:
        node: syntax tree node containing statement"""
        try:
            if node.target.node_type == DATA_TYPE.ID:
                return self.basic_id_set(node)
            elif node.target.node_type == DATA_TYPE.INDEX_SELECT:
                return self.index_set(node)
            else:
                raise InternalException("Internal Error: Unknown type " + node.target.node_type)
        except SemanticException as details:
            Semantic_analysis_errors.semantic_err(node, details)
            return False

    def basic_id_set(self, node):
        """Set on an id.

        Args:
        node: syntax tree node representing set"""
        id_set = Set(Name(node.target.ID, self.sym_table.id_type(node.target.ID)), self.expr_type_is(node.value))
        id_set.target.constraints = self.sym_table.id(node.target.ID)['constraints']
        id_set.target.size = self.sym_table.id(node.target.ID)['size']
        # print(id_set.value)
        if self.can_assign_type(id_set.target.type, id_set.value.type) is False:
            raise SemanticException(str(id_set.value.type) + " cannot be assigned to variable of type " + str(id_set.target.type))
        return id_set

    def analyse_int_decl(self, node):
        """Anlyses int declaration statement.

        Args:
        node: syntax tree node representing declaration."""
        try:
            if node.value is not None:
                decl = Int_decl(node.node_type, self.expr_type_is(node.bit_constraints), Name(node.ID, DATA_TYPE.decl_to_value(node.node_type)), self.expr_type_is(node.value))
            else:
                decl = Int_decl(node.node_type, self.expr_type_is(node.bit_constraints), Name(node.ID, DATA_TYPE.decl_to_value(node.node_type)))
            if decl.constraints.node_type != DATA_TYPE.INT_LITERAL:
                raise SemanticException("Word Length cannot be variable")
            if node.value is not None and self.can_assign_type(DATA_TYPE.decl_to_value(node.node_type), decl.value.type) is False:  #Should be more specific
                    raise SemanticException(str(decl.value.type) + " Cannot be assigned to " + str(node.node_type) + " assignment")
            if decl.ID.name is not None:
                self.sym_table.add_id(node.ID, DATA_TYPE.decl_to_value(node.node_type))
                self.sym_table.id(node.ID)['constraints'] = decl.constraints
                self.sym_table.id(node.ID)['size'] = None
            return decl
        except SemanticException as details:
            Semantic_analysis_errors.semantic_err(node, details)
            return False

    def validate_scope(self, node):
        if len(self.sym_table._symbols.stack) == 1 and (node.node_type != DATA_TYPE.SBOX_DECL and node.node_type != DATA_TYPE.FUNC_DECL):
            raise SemanticException("Only Sbox declarations are valid at the global scope")

    def analyse_bit_decl(self, node):
        """Anlyses bit declaration statement.

        Args:
        node:syntax tree node representing declaration"""
        try:
            if node.value is not None:
                decl = Bit_decl(Name(node.ID, DATA_TYPE.decl_to_value(node.node_type)), node.node_type, self.expr_type_is(node.value))
            else:
                decl = Bit_decl(Name(node.ID, DATA_TYPE.decl_to_value(node.node_type)), node.node_type)
            if node.value is not None:
                if decl.value.type != DATA_TYPE.BIT_VAL:
                    raise SemanticException("Cannot Assign " + str(decl.value.type) + " in " +  str(DATA_TYPE.BIT_DECL))
            if node.ID is not None:
                self.sym_table.add_bit_id(node.ID, DATA_TYPE.decl_to_value(node.node_type))
                self.sym_table.id(node.ID)['constraints'] = None
                self.sym_table.id(node.ID)['size'] = None
            return decl
        except SemanticException as details:
            Semantic_analysis_errors.semantic_err(node, details)
            return False

    def seq_value_dimension(self, seq_value, dimension=0):
        """Returns dimensions of sequence value.

        Args:
        Seq_value: sequence value to check.
        dimension: current dimension depth"""
        if DATA_TYPE.is_op_type(seq_value.node_type):
            print(seq_value.size)
        dimension += 1
        if DATA_TYPE.is_seq_type(seq_value.value[0].type) is True:
            dimension = self.seq_value_dimension(seq_value.value[0], dimension)
        return dimension

    def seq_expr_dimension(self, expr):
        """Validates and analyses sequence values.

        Args:
        expr: syntax tree node representing value"""
        dimensions = []
        if DATA_TYPE.is_op_type(expr.node_type):
            if DATA_TYPE.is_op_type(expr.left.node_type):
                dimensions.append(self.seq_expr_dimension(expr.left))
            elif DATA_TYPE.is_seq_type(expr.left.type):
                dimensions.append(self.seq_value_dimension(expr.left))
            if DATA_TYPE.is_op_type(expr.right.node_type):
                dimensions.append(self.seq_expr_dimension(expr.right))
            elif DATA_TYPE.is_seq_type(expr.right.type):
                dimensions.append(self.seq_value_dimension(expr.right))
        elif DATA_TYPE.is_seq_type(expr.type):
            dimensions.append(self.seq_value_dimension(expr))
        dimensions = list(set(dimensions))
        if len(dimensions) > 1:
            raise SemanticException("Sequence must be of homogeneous type")
        else:
            return dimensions[0]

    def analyse_return_stmt(self, ast_node, func_decl):
        """Analyses return statement.

        Args:
        ast_node: Node representing return statement.
        func_decl : function declaration node that return statement presides in"""
        # print(self.sym_table.id_type(ast_node.ID))
        ret = Return(self.expr_type_is(ast_node.expr, True))
        if ret.type != func_decl.return_type:
            raise SemanticException("Function " + str(func_decl.ID.name) + " returns " + str(ret.type) +
                                    ". requires return value " + str(func_decl.return_type))
        return ret

    def analyse_bit_cnst_seq(self, node):
        """Analyse Sequences that have bit constraints set on their members and build IR node

        Args:
        node: Node to translate"""
        try:
            if node.value is None:
                if node.node_type == DATA_TYPE.SBOX_DECL:
                    raise SemanticException("Sbox declaractions cannot be unitialised")
                decl = Seq_decl(node.node_type, self.analyse_array_size(node), node.ID, constraints=self.expr_type_is(node.bit_constraints))
            else:
                decl = Seq_decl(node.node_type, self.analyse_array_size(node), node.ID, self.expr_type_is(node.value), self.expr_type_is(node.bit_constraints))
                # decl.value.dim_s = self.seq_expr_dimension(decl.value)
                if DATA_TYPE.is_seq_type(decl.value.node_type) and decl.value.dim_s != len(decl.size):
                    # Checking Dimensions match
                    raise SemanticException((str(decl.value.type) + "[]" * self.seq_value_dimension(decl.value)) +
                                        "Cannot be assigned to " + str(decl.value.type) + ("[]" * len(decl.size)))
                if DATA_TYPE.is_seq_type(decl.value.type) and not DATA_TYPE.is_op_type(decl.value.node_type):
                    # Checking elements in range
                    self.seq_val_matches_dimensions(decl.value.dim_s, decl.size, decl.value)
                if node.node_type == DATA_TYPE.SBOX_DECL:
                    self.sbox_semantics(decl)
            if decl.constraints.node_type != DATA_TYPE.INT_LITERAL:
                raise SemanticException("Must use an Integer literal to declare word length")
            if node.ID is not None:
                self.sym_table.add_id(node.ID, DATA_TYPE.decl_to_value(node.node_type), len(decl.size))
                self.sym_table.id(node.ID)['constraints'] = decl.constraints
                self.sym_table.id(node.ID)['size'] = decl.size
            return decl
        except SemanticException as details:
            Semantic_analysis_errors.semantic_err(node, details)
            return False

    def sbox_semantics(self, node):
        """Implements sbox semantic rules.

        Args:
        node: IR node representing sbox declaration."""
        if len(node.value.value) != int(node.size[-1].value):
            raise SemanticException("Sbox should have " + node.size[-1].value + " members")
        for minterm in node.value.value:
            if minterm.node_type != DATA_TYPE.INT_LITERAL:
                raise SemanticException("Only integer literals can be used as sbox members")
            if len(bin(int(minterm.value))[2:]) > int(node.constraints.value):
                raise SemanticException("Expected width is " + node.constraints.value + ". " + minterm.value + " has a width of " + str(len(bin(int(minterm.value))[2:])))

    def analyse_bit_seq(self, node):
        """Analysing sequence of bits declaration

        Args:
        node: Node to translate and analyse"""
        try:
            if node.value is None:
                decl = Seq_decl(node.node_type, self.analyse_array_size(node), node.ID)
            else:
                decl = Seq_decl(node.node_type, self.analyse_array_size(node), node.ID, self.expr_type_is(node.value))
                if decl.value.node_type == DATA_TYPE.SEQ_BIT_VAL:
                    decl.value.dim_s = self.seq_expr_dimension(decl.value)
                    if decl.value.dim_s != len(decl.size):
                        # Checking Dimensions match
                        raise SemanticException((str(decl.value.type) + "[]" * self.seq_value_dimension(decl.value)) +
                                             " Cannot be assigned to " + str(decl.value.type) + ("[]" * len(decl.size)))
                else:
                    if self.can_assign_type(DATA_TYPE.SEQ_BIT_VAL, decl.value.type) is False:
                        raise SemanticException(str(decl.value.type) + " Cannot be assigned to " + str(decl.node_type))
                    if decl.value.type == DATA_TYPE.INT_VAL:
                        if len(decl.size) > 1:
                            raise SemanticException(str(DATA_TYPE.INT_VAL) + "cannot be assigned to a " + str(DATA_TYPE.SEQ_BIT_VAL) + ("[]" * len(decl.size)))
            if node.ID is not None:
                self.sym_table.add_id(node.ID, decl.ID.type, len(decl.size))
                self.sym_table.id(node.ID)['size'] = decl.size
                self.sym_table.id(node.ID)['constraints'] = decl.size[-1]
            return decl
        except SemanticException as details:
            Semantic_analysis_errors.semantic_err(node, details)
            return False

    def seq_val_matches_dimensions(self, dim, expected_size, seq_val):
        """Verifies that passed in sequence value matches expected size

        Args:
        dim: number of dimensions in sequence.
        expected_size: expected size of each dimension.
        seq_val: Sequence value being validated."""
        for num, seq in enumerate(seq_val.value):
            if num >= int(expected_size[len(expected_size) - dim].value):
                raise SemanticException("Sequence value goes beyond range bounds.  Expected: " + str(expected_size[len(expected_size) - dim].value))
            if dim > 1:
                self.seq_val_matches_dimensions(dim - 1, expected_size, seq)

    def analyse_array_size(self, node):
        size = []
        for size_param in node.size:
            size.append(self.expr_type_is(size_param))
            if size[-1].node_type != DATA_TYPE.INT_LITERAL:
                raise SemanticException("Sequence Size Parameter Must be Literal Integers")
        return size

    def seq_type_is(self, seq_value):
        """Returns sequence type.

        Args:
        Seq_val: sequence value to analyse"""
        values = []
        val = Seq_val()
        for i in seq_value.value:
            curr = self.expr_type_is(i)
            val.add_element(curr)
            values.append(curr.type)
        curr.size =  len(values)
        val.type = self.analyse_seq_val_type(list(set(values)))
        if val.type == DATA_TYPE.SEQ_BIT_VAL:
            val.constraints = Int_literal(value=str(len(values)))
        val.dim_s = self.seq_expr_dimension(val)
        return val

    def analyse_seq_val_type(self, seq_val):
        """analyses result of seq_type_is.

        Args:
        seq_val: reduced list that should contain single type.  If this contains multiple types, it means that
        multiple types of values are in sequence value."""
        if len(seq_val) > 1:
            raise SemanticException("Combined Types in sequence")
        elif seq_val[0] == DATA_TYPE.INT_VAL:
            seq_val = DATA_TYPE.SEQ_INT_VAL
        elif seq_val[0] == DATA_TYPE.BIT_VAL:
            seq_val = DATA_TYPE.SEQ_BIT_VAL
        elif seq_val[0] == DATA_TYPE.SEQ_INT_VAL or seq_val[0] == DATA_TYPE.SEQ_BIT_VAL:
            seq_val = seq_val[0]
        else:
            raise InternalException("Unknown Sequence Type")
        return seq_val

    def get_constraints(self, value):
        """Places in minimum standard size int width possible on int literals"""
        size = int(value).bit_length()
        if size < 8:
            return Int_literal(value="8")
        elif size < 16:
            return Int_literal(value="16")
        elif size < 32:
            return Int_literal(value="32")
        elif size < 64:
            return Int_literal(value="64")

    def analyse_expr(self, value):
        return self.expr_type_is(value)

    def expr_type_is(self, expression, is_return=False):
        """Performs Semantic analysis on expression, building IR node

        Args:
        expression : Expression to analyse.
        is_return: Is true is expression is a return statement: extra scoping rules need to be checked."""
        expr_types = {}
        IR_expression = []
        for i, expr in enumerate(expression.expressions):
            if expr.node_type == DATA_TYPE.INT_VAL:
                expr_types["OPERAND_" + str(len(expr_types))] = DATA_TYPE.INT_VAL
                IR_expression.append(Int_literal(value=expr.value, constraints=self.get_constraints(expr.value)))
            elif expr.node_type == DATA_TYPE.SEQ_VAL:
                IR_expression.append(self.seq_type_is(expr))
                expr_types["OPERAND_" + str(len(expr_types))] = IR_expression[-1].type
            elif expr.node_type == DATA_TYPE.BIT_VAL:
                expr_types["OPERAND_" + str(len(expr_types))] = DATA_TYPE.BIT_VAL
                IR_expression.append(Bit_literal(expr.value))
            elif DATA_TYPE.is_op_type(expr.node_type):  # NOQA
                expr_types["OP"] = expr.node_type
                IR_expression.append(Binary_operation(expr.node_type, expr.operator))
            elif expr.node_type == DATA_TYPE.EXPR:
                IR_expression.append(self.expr_type_is(expr))
                expr_types["OPERAND_" + str(len(expr_types))] = IR_expression[-1].type
            elif expr.node_type == DATA_TYPE.ID:
                IR_expression.append(self.analyse_id(expr, is_return))
                expr_types["OPERAND_" + str(len(expr_types))] = IR_expression[-1].type
            elif expr.node_type == DATA_TYPE.FUNCTION_CALL:
                IR_expression.append(self.analyse_func_call(expr))
                expr_types["OPERAND_" + str(len(expr_types))] = IR_expression[-1].type
            elif expr.node_type == DATA_TYPE.CAST:
                raise SemanticException("Explicit Casts have not been implemented")
                IR_expression.append(self.analyse_cast(expr))
                expr_types["OPERAND_" + str(len(expr_types))] = IR_expression[-1].type
            elif expr.node_type == DATA_TYPE.INDEX_SELECT:
                IR_expression.append(self.analyse_index_sel(expr))
                expr_types["OPERAND_" + str(len(expr_types))] = IR_expression[-1].type
            elif expr.node_type == DATA_TYPE.INDEX_RANGE:
                IR_expression.append(self.analyse_index_range(expr))
            else:
                raise SemanticException(str(expr.node_type) + " Is an unknown type")
            if len(expr_types) == 3:
                if self.sub_expr_valid(expr_types, IR_expression) is True:
                    expr_types = self.reduce_sub_expr(expr_types)
                    self.clean_up_expr(IR_expression, expr_types)
                else:
                    raise SemanticException("cannot combine a " + str(expr_types['OPERAND_0']) + " value with a " +
                                         str(expr_types['OPERAND_2']) + " in " + str(expr_types['OP']) + " Operation")
        if len(IR_expression) != 1:
            raise InternalException("Internal Error with expression")
        return IR_expression[0]

    def analyse_id(self, node, is_return=False):
        """Analyses non-defining instances of IDs.

        Args:
        node: node representing ID.
        is_return: True if the ID is being returned to allow for extra scoping checks."""
        ID = Name(node.ID, self.sym_table.id_type(node.ID))
        node_type = self.sym_table.id_type(node.ID)
        if DATA_TYPE.is_seq_type(node_type):
            # if node_type == DATA_TYPE.BS_SEQ_INT_VAL or node_type == DATA_TYPE.SEQ_INT_VAL:
            ID.constraints = self.sym_table.id(node.ID)['constraints']
            ID.size = self.sym_table.id(node.ID)['size']
        elif DATA_TYPE.is_int_val(node_type):
            ID.constraints = self.sym_table.id(node.ID)['constraints']
        if is_return is True and DATA_TYPE.is_seq_type(node_type):
            if self.sym_table.id(node.ID)['f_param'] is False:
                raise SemanticException("Cannot return out of scope variable " + node.ID)
        return ID

    def analyse_index_range(self, node):
        """Analyses index range.

        Args:
        node: syntax tree node that represents operation"""
        start = self.expr_type_is(node.start)
        finish = self.expr_type_is(node.finish)
        if start.type != DATA_TYPE.INT_VAL or finish.type != DATA_TYPE.INT_VAL:
            raise SemanticException("Can only use integers to select sequence elements")
        return Element_range(self.expr_type_is(node.start), self.expr_type_is(node.finish))

    def analyse_index_sel(self, node):
        """Check result type of index select against target ID, returning IR node

        Args:
        node: syntax tree node that represents operation"""
        ir_indices = self.collect_indices(node.indices)
        if node.target_type != DATA_TYPE.ID:
            # Target of index select is not an ID.  Probably a cast, thus base dimension will always be 1 : Cant cast into multi-dimensional array
            target = self.expr_type_is(node.target)
            index_sel = Index_select(target, ir_indices)
            if(len(ir_indices) > 1):
                raise SemanticException(str(target.type) + ("[]" * len(ir_indices)) + " Cannot be selected from " + str(target.type) + "[]")
            elif len(ir_indices[-1]) > 1 or ir_indices[-1][0].type == DATA_TYPE.INDEX_RANGE:
                # selection is of type sequence
                pass
            else:
                #Selection is single element out of base
                index_sel.type = DATA_TYPE.seq_to_index_sel(index_sel.type)
            return index_sel
        else:
            self.check_index_in_limit(node.ID, ir_indices)
            if DATA_TYPE.is_seq_type(self.sym_table.id(node.ID)['type']):
                # element index select on sequence
                return self.build_seq_index_ir(node, ir_indices)
            elif DATA_TYPE.is_int_val(self.sym_table.id(node.ID)['type']):
                #  Bit index select on int
                return self.build_int_index_ir(node, ir_indices)
            else:
                raise SemanticException("Trying to do index selection on invalid " + str(self.sym_table.id(node.ID)['type']) + " type")

    def build_int_index_ir(self, node, ir_indices):
        """builds node repreenting index select on an integer

        Args:
        node: syntax tree node that represents operation
        ir_indices: ir representation of indices uses for selection"""
        target_id = self.sym_table.id(node.ID)
        select_type = None
        if self.is_range(ir_indices[-1]):
            if target_id['type'] == DATA_TYPE.INT_VAL:
                select_type = DATA_TYPE.SEQ_BIT_VAL
            elif target_id['type'] == DATA_TYPE.BS_INT_VAL:
                select_type = DATA_TYPE.SEQ_BS_BIT_VAL
            else:
                raise InternalException("internal error: Unrecognised type in int index select " + str(target_id['type']))
            index_sel = Index_select(Name(node.ID, target_id['type']), ir_indices, select_type)
            index_sel.target.constraints = self.sym_table.id(node.ID)['constraints']
            return index_sel
        elif len(ir_indices) == 1:
            if target_id['type'] == DATA_TYPE.INT_VAL:
                select_type = DATA_TYPE.BIT_VAL
            elif target_id['type'] == DATA_TYPE.BS_INT_VAL:
                select_type = DATA_TYPE.BS_BIT_VAL
            else:
                raise InternalException("internal error: Unrecognised type in int index select " + str(target_id['type']))
            index_sel = Index_select(Name(node.ID, target_id['type']), ir_indices, select_type)
            index_sel.target.constraints = self.sym_table.id(node.ID)['constraints']
            return index_sel
        elif (len(ir_indices) > 1 and DATA_TYPE.is_int_val(self.sym_table.id(node.ID)['type'])):
            raise SemanticException("Integer cannot be treated as having more than one dimension")

    def build_seq_index_ir(self, node, ir_indices):        
        """builds node repreenting index select on an sequence value

        Args:
        node: syntax tree node that represents operation
        ir_indices: ir representation of indices uses for selection"""
        target_id = self.sym_table.id(node.ID)
        for dim_n, dim in enumerate(self.sym_table.id(node.ID)['size']):
            if dim_n >= len(ir_indices):
                break
            if len(ir_indices[dim_n]) > 1 or ir_indices[dim_n][0].node_type == DATA_TYPE.INDEX_RANGE:
                raise SemanticException("Cannot use lists or ranges on sequences")
        if self.sym_table.dimension(node.ID) > len(ir_indices):
            raise SemanticException("Cannot select multi-dimensional Sequence")
            # return Index_select(Name(node.ID, target_id['type'], size=self.sym_table.id(node.ID)['size'], constraints=target_id['constraints']), ir_indices)
        elif self.sym_table.dimension(node.ID) == len(ir_indices):
            if self.is_range(ir_indices[-1]):
                return Index_select(Name(node.ID, target_id['type'], size=self.sym_table.id(node.ID)['size'],  constraints=target_id['constraints']), ir_indices, target_id['type'])
            else:
                if target_id['type'] == DATA_TYPE.SBOX_DECL:
                    return Index_select(Name(node.ID, target_id['type'], size=self.sym_table.id(node.ID)['size'],  constraints=target_id['constraints']), ir_indices, DATA_TYPE.SEQ_BS_BIT_VAL)
                else:
                    return Index_select(Name(node.ID, target_id['type'], size=self.sym_table.id(node.ID)['size'],  constraints=target_id['constraints']), ir_indices, DATA_TYPE.seq_to_index_sel(target_id['type']))
        elif self.sym_table.dimension(node.ID) < len(ir_indices):
            if (target_id['type'] == DATA_TYPE.BS_SEQ_INT_VAL or target_id['type'] == DATA_TYPE.SEQ_INT_VAL) and (len(ir_indices) == self.sym_table.dimension(node.ID) + 1):
                if self.is_range(ir_indices[-1]):
                    selection_type = None
                    if target_id['type'] == DATA_TYPE.BS_SEQ_INT_VAL:
                        selection_type = DATA_TYPE.SEQ_BS_BIT_VAL
                    elif target_id['type'] == DATA_TYPE.SEQ_INT_VAL:
                        selection_type = DATA_TYPE.SEQ_BIT_VAL
                    return Index_select(Name(node.ID, target_id['type'], size=self.sym_table.id(node.ID)['size'],  constraints=target_id['constraints']), ir_indices, selection_type)
                else:
                    if target_id['type'] == DATA_TYPE.BS_SEQ_INT_VAL:
                        return Index_select(Name(node.ID, target_id['type'], size=self.sym_table.id(node.ID)['size'],  constraints=target_id['constraints']), ir_indices, DATA_TYPE.BS_BIT_VAL)
                    elif target_id['type'] == DATA_TYPE.SEQ_INT_VAL:
                        return Index_select(Name(node.ID, target_id['type'], size=self.sym_table.id(node.ID)['size'],  constraints=target_id['constraints']), ir_indices, DATA_TYPE.BIT_VAL)    # Selecting a bit value of an integer element in an BS integer array
            else:
                raise SemanticException(str(target_id['type']) + "[]" * len(ir_indices) + " cannot be selected from " + str(target_id['type']) + (self.sym_table.dimension(node.ID) * "[]"))


    def clean_up_expr(self, IR_expressions, result_type):
        """Reorders collected expression nodes

        Args:
        IR_expressions: IR nodes making up expression operands.
        result_type: result type of expression and its operands"""
        left = IR_expressions.pop(0)
        right = IR_expressions.pop(1)
        IR_expressions[0].left = left
        IR_expressions[0].right = right
        IR_expressions[0].type = result_type['OPERAND_0']
        self.analyse_operation_type_size(IR_expressions[0])

    def analyse_operation_type_size(self, operation):
        """Analyses and deducts size and bit width information of binary operations

        Args:
        operation: nodes making up operation"""
        if operation.type == DATA_TYPE.INT_VAL:
            operation.constraints = self.largest_int_lit(operation.left.constraints, operation.right.constraints)
        elif operation.type == DATA_TYPE.BIT_VAL:
            operation.constraints = Int_literal("8")
        elif operation.type == DATA_TYPE.BS_INT_VAL:
            operation.constraints = self.largest_int_lit(operation.left.constraints, operation.right.constraints)
        elif operation.type == DATA_TYPE.SEQ_INT_VAL:
            try:
                operation.constraints = self.largest_int_lit(operation.left.constraints, operation.right.constraints)
            except AttributeError:
                if operation.node_type == DATA_TYPE.SHIFT_OP:
                    raise SemanticException("SEQ SHFIT OP")
                else:
                    self.validate_seq_operation(operation.left, operation.right)
                # else:
                #     raise InternalException("Internal Error: Sequence Value does not have constraint " + str(operation.left.node_type) + " " + str(operation.right.node_type))
        elif operation.type == DATA_TYPE.BS_SEQ_INT_VAL:
            pass
        elif operation.type == DATA_TYPE.SEQ_BIT_VAL:
            operation.constraints = Int_literal(self.get_seq_bit_op_width(operation.left, operation.right))
        elif operation.type == DATA_TYPE.BS_BIT_VAL:
            pass
        elif operation.type == DATA_TYPE.SEQ_BS_BIT_VAL:
            if operation.left.type == DATA_TYPE.SEQ_BS_BIT_VAL:
                seq_val = operation.left
            elif operation.right.type == DATA_TYPE.SEQ_BS_BIT_VAL:
                seq_val = operation.right
            assert seq_val.node_type == DATA_TYPE.INDEX_SELECT, "Assuming this type comes from index select operation"
            if seq_val.indices[-1][-1].node_type == DATA_TYPE.INDEX_RANGE:
                operation.size = {'start': seq_val.indices[-1][-1].start, 'finish': seq_val.indices[-1][-1].finish}
                operation.constraints = self.get_operator_of_type(operation.left, operation.right, DATA_TYPE.SEQ_BS_BIT_VAL).constraints
            else:
               raise InternalException("sequence of bitsliced values with unknown size " + str(seq_val.node_type))
        else:
            raise InternalException("Unknown size of binary operation " + str(operation.type))

    def validate_seq_operation(self, op_1, op_2):
        """Validation of operations containing sequence values"""
        if (op_1.node_type != op_2.node_type) and (op_1.node_type == DATA_TYPE.SEQ_VAL or op_2 == DATA_TYPE.SEQ_VAL):
            raise SemanticException("Cannot combine structurally different sequences in expression")
        for left, right in zip(op_1.value, op_2.value):
            if left.node_type == DATA_TYPE.SEQ_VAL:
                raise SemanticException("Cannot combine Sequences of more than a single dimension in an expression")
        if len(op_1.value) != len(op_2.value):
            raise SemanticException("Cannot combine structurally different sequences in expression")
        return True

    def get_seq_bit_op_width(self, op_1, op_2):
        """Returns bit width of sequence operations of bits

        Args:
        op_1: Operand 1 in binary expression
        op_2: operand 2 in binary expression"""
        op_1_size = None
        op_2_size = None
        if op_1.node_type == DATA_TYPE.SEQ_VAL:
            op_1_size = len(op_1.value)
        if op_2.node_type == DATA_TYPE.SEQ_VAL:
            op_2_size = len(op_2.value)
        return self.largest_size(op_1_size, op_2_size)

    def largest_size(self, op_1, op_2):
        """Returns the largest size of two nodes and account for the fact that one operand may exist"""
        if op_1 is None:
            return op_2
        if op_2 is None:
            return op_1
        if op_1 > op_2:
            return op_1
        return op_2

    def get_operator_of_type(self, op_1, op_2, exp_type):
        """Returns the operator that is the type of the result of expression.

        Args:
        exp_type: result type of expression"""
        if op_1.type == exp_type:
            return op_1
        elif op_2.type == exp_type:
            return op_2
        else:
            raise InternalException("Internal Error: Tried to get op type that doesn't exist")

    def largest_int_lit(self, val1, val2):
        """Returns largest int literal node"""
        if int(val1.value) > int(val2.value):
            return val1
        else:
            return val2

    def analyse_cast(self, node):
        """Analyses cast operation"""
        size = []
        cnst = None
        try:
            for i in node.cast_operation.seq_size:
                size.append(self.expr_type_is(i))
        except TypeError:
            pass
        if node.cast_operation.constraints is not None:
            cnst = self.expr_type_is(node.cast_operation.constraints)
        cast = Cast(Cast_operation(node.cast_operation.target_type, cnst, size), self.expr_type_is(node.target))  # NOQA
        return cast

    def return_type_to_IR(self, ID):
        """Converts return type to IR node"""
        ret_type = None
        if ID in self.sym_table.f_table:
            ret_type = self.sym_table.f_table[ID]["return"]['type']
        else:
            raise SemanticException("Attempted to call non-existent function " + ID)
        width = None
        if self.sym_table.f_table[ID]["return"]['constraints'] is not None:
            width = self.expr_type_is(self.sym_table.f_table[ID]["return"]['constraints'])
        size = None
        if self.sym_table.f_table[ID]["return"]['size'] is not None:
            size = []
            for dim in self.sym_table.f_table[ID]["return"]['size']:
                size.append(self.expr_type_is(dim))
        if ret_type == DATA_TYPE.BIT_VAL:
            return Bit_decl(Name(ID, DATA_TYPE.BIT_VAL), DATA_TYPE.BS_BIT_VAL)
        elif ret_type == DATA_TYPE.BS_INT_VAL:
            return Int_decl(DATA_TYPE.BS_INT_DECL, width, Name(ID, DATA_TYPE.BS_INT_VAL))
        elif ret_type == DATA_TYPE.INT_VAL:
            return Int_decl(DATA_TYPE.INT_DECL, width, Name(ID, DATA_TYPE.INT_VAL))
        elif ret_type == DATA_TYPE.SEQ_INT_VAL:
            return Seq_decl(DATA_TYPE.SEQ_INT_DECL, size, Name(ID, DATA_TYPE.SEQ_INT_VAL), constraints=width)
        elif ret_type == DATA_TYPE.SEQ_BIT_VAL:
            return Seq_decl(DATA_TYPE.SEQ_BIT_DECL, size, Name(ID, DATA_TYPE.SEQ_BIT_VAL))
        elif ret_type == DATA_TYPE.SBOX_DECL:
            return Seq_decl(DATA_TYPE.SBOX_DECL, size, width, Name(ID, DATA_TYPE.SBOX_DECL))
        elif ret_type == DATA_TYPE.VOID:
            return DATA_TYPE.VOID
        elif ret_type == DATA_TYPE.BS_BIT_VAL:
           return Bit_decl(Name(ID, DATA_TYPE.BS_BIT_VAL), DATA_TYPE.BS_BIT_DECL)
        else:
            raise InternalException("Internal Error: Unknown Return type")


    def analyse_func_call(self, node):
        """Analyses function call statement and builds IR node if successful"""
        return_ = self.return_type_to_IR(node.ID)
        if return_ != DATA_TYPE.VOID:
            f_call = Call(node.ID, return_.ID.type, return_.ID.size, return_.ID.constraints, return_)
        else:
            f_call = Call(node.ID, return_, None, None, return_)
        if self.get_param_length(node.parameters) != self.get_param_length(self.sym_table.f_table[node.ID]['parameters']):
            raise SemanticException("Incorrect arguments supplied for function " + node.ID + " expected: " + str(len(self.sym_table.f_table[node.ID]['parameters'])))
        if node.parameters is not None:
            for i, p in enumerate(node.parameters):
                f_call.add_parameter(self.expr_type_is(p))
                if self.value_matches_expected(f_call.parameters[i].type, self.sym_table.f_table[node.ID]['parameters'][i]['type']) is False:
                    raise SemanticException(str(f_call.parameters[i].type) + " does not equal " + str(self.sym_table.f_table[node.ID]['parameters'][i]['type']) + " in function call to " + node.ID)
                    return False
        return f_call

    def get_param_length(self, params):
        if params is None:
            return 0
        else:
            return len(params)

    def value_matches_expected(self, result_value, expected_value):
        """Lookup for allowed assignment types.

        Args:
        result_value: Type of result
        expected_value: Expected type of result"""
        # Value type -> Allowed to be [ these value types ]
        allowed_values = {DATA_TYPE.INT_DECL: [DATA_TYPE.INT_VAL, DATA_TYPE.BS_INT_VAL, DATA_TYPE.SEQ_BIT_VAL],
                          DATA_TYPE.BIT_DECL: [DATA_TYPE.BIT_VAL],
                          DATA_TYPE.BS_INT_DECL: [DATA_TYPE.INT_VAL, DATA_TYPE.BS_INT_VAL, DATA_TYPE.SEQ_BS_BIT_VAL],
                          DATA_TYPE.BS_INT_VAL: [DATA_TYPE.INT_VAL, DATA_TYPE.BS_INT_VAL, DATA_TYPE.SEQ_BS_BIT_VAL],
                          DATA_TYPE.INT_VAL: [DATA_TYPE.INT_VAL],
                          DATA_TYPE.BIT_VAL: [DATA_TYPE.BIT_VAL],
                          DATA_TYPE.SEQ_INT_VAL: [DATA_TYPE.SEQ_INT_VAL, DATA_TYPE.BS_SEQ_INT_VAL, DATA_TYPE.INT_VAL],
                          DATA_TYPE.BS_SEQ_INT_VAL: [DATA_TYPE.SEQ_INT_VAL, DATA_TYPE.BS_SEQ_INT_VAL, DATA_TYPE.BS_INT_VAL],
                          DATA_TYPE.SEQ_BIT_VAL: [DATA_TYPE.SEQ_BIT_VAL, DATA_TYPE.SEQ_BS_BIT_VAL, DATA_TYPE.BS_INT_VAL],
                          DATA_TYPE.BS_BIT_VAL: [DATA_TYPE.BS_BIT_VAL],
                          DATA_TYPE.SEQ_BS_BIT_VAL: [DATA_TYPE.BS_INT_VAL, DATA_TYPE.SBOX_DECL, DATA_TYPE.SEQ_BS_BIT_VAL],
                          DATA_TYPE.SBOX_DECL: [DATA_TYPE.SBOX_DECL]}
        if result_value in allowed_values[expected_value]:
            return True
        return False

    def analyse_if_stmt_decl(self, node):
        try:
            self.sym_table.add_scope()
            if len(node.condition) > 1:
                raise InternalException("Internal Error: If stmt has more than one condition token")
            if_stmt = If_stmt(self.expr_type_is(node.condition[0]))
            if if_stmt.condition.type != DATA_TYPE.BIT_VAL:
                raise SemanticException("If conditional is type " + str(if_stmt.condition.type))
            for stmt in node.body:
                if_stmt.add_stmt(self.analyse_sub_stmt(stmt))
            self.sym_table.leave_scope()
            return if_stmt
        except SemanticException as details:
            Semantic_analysis_errors.semantic_err(node, details)
            return False

    def analyse_for_loop_decl(self, node):
        self.sym_table.add_scope()
        for_loop = For_loop()
        try:
            for i in node.initializer:
                for_loop.initializer.append(self.analyse_sub_stmt(i))

            for t in node.terminator:
                for_loop.terminator.append(self.expr_type_is(t))

            for i in node.increment:
                for_loop.increment.append(self.analyse_ID_set(i))

            for stmt in node.body:
                for_loop.body.append(self.analyse_sub_stmt(stmt))

            # self.translator.translate_for_loop(node, self.sym_table)
            self.sym_table.leave_scope()
            return for_loop
        except SemanticException as details:
            Semantic_analysis_errors.semantic_err(node, details)
            return False

    def scope(self):
        return self.call_stack.peek()

    def sub_expr_valid(self, expression, IR_expression):
        """Checks if operands are valid with operator

        Args:
        expression: current expression to be checked.
        IR_expression: IR nodes making up expression."""
        if expression['OP'] is DATA_TYPE.ARITH_OP:
            return self.arith_expr_valid(expression, IR_expression)
        elif expression['OP'] is DATA_TYPE.SHIFT_OP:
            return self.shift_expr_valid(expression, IR_expression)
        elif expression['OP'] is DATA_TYPE.BITWISE_OP:
            return self.bitwise_expr_valid(expression, IR_expression)
        elif expression['OP'] is DATA_TYPE.COMP_OP:
            return self.comp_expr_valid(expression, IR_expression)
        elif expression['OP'] is DATA_TYPE.LOG_OP:
            return self.log_expr_valid(expression)
        else:
            raise InternalException("Internal error: Invalid Operand")

    def log_expr_valid(self, expression):
        if expression['OPERAND_2'] == DATA_TYPE.BIT_VAL or expression['OPERAND_2'] == DATA_TYPE.BIT_VAL:
            return True
        return False

    def comp_expr_valid(self, expression, IR_expressions):
        """Checks if comparison expression is valid.
        Args:
        expression: Types in current expression."""
        valid_operands_types = {DATA_TYPE.BIT_VAL: [DATA_TYPE.BIT_VAL],
                                DATA_TYPE.INT_VAL: [DATA_TYPE.INT_VAL, DATA_TYPE.SEQ_BIT_VAL],
                                DATA_TYPE.SEQ_BIT_VAL: [DATA_TYPE.INT_VAL, DATA_TYPE.SEQ_BIT_VAL]}
        try:
            if expression['OPERAND_0'] in valid_operands_types[expression['OPERAND_2']]:
                if expression['OPERAND_0'] == DATA_TYPE.BIT_VAL:
                    if IR_expressions[1].operator != "!=" and IR_expressions[1].operator != "==":
                        raise SemanticException("Bit values can only be compared for equality, " + IR_expressions[1].operator + " Used")
                return True
        except KeyError:
            return False
        return False

    def bitwise_expr_valid(self, expression, IR_expression):
        """Checks if bitwise expression is valid.
        Args:
        expression: Types in current expression.
        IR_expression: IR nodes making up expression."""
        valid_operands_types = {DATA_TYPE.INT_VAL: [DATA_TYPE.INT_VAL, DATA_TYPE.SEQ_BIT_VAL, DATA_TYPE.BS_INT_VAL, DATA_TYPE.SEQ_BS_BIT_VAL],
                                DATA_TYPE.BS_INT_VAL: [DATA_TYPE.INT_VAL, DATA_TYPE.SEQ_BIT_VAL, DATA_TYPE.BS_INT_VAL, DATA_TYPE.SEQ_BS_BIT_VAL],
                                DATA_TYPE.SEQ_BIT_VAL: [DATA_TYPE.INT_VAL, DATA_TYPE.SEQ_BIT_VAL, DATA_TYPE.BS_INT_VAL, DATA_TYPE.SEQ_BS_BIT_VAL],
                                DATA_TYPE.SEQ_BS_BIT_VAL: [DATA_TYPE.INT_VAL, DATA_TYPE.SEQ_BIT_VAL, DATA_TYPE.BS_INT_VAL, DATA_TYPE.SEQ_BS_BIT_VAL],
                                DATA_TYPE.BS_BIT_VAL: [DATA_TYPE.BS_BIT_VAL, DATA_TYPE.BIT_VAL],
                                DATA_TYPE.BIT_VAL: [DATA_TYPE.BS_BIT_VAL, DATA_TYPE.BIT_VAL]}
        try:
            if DATA_TYPE.is_int_val(expression['OPERAND_0']) and DATA_TYPE.is_int_val(expression['OPERAND_2']):
                self.expr_seq_bit_dims(IR_expression)
                return True
            elif expression['OPERAND_0'] in valid_operands_types[expression['OPERAND_2']]:
                self.expr_seq_bit_dims(IR_expression)
                return True
        except KeyError:
            return False
        return False

    def shift_expr_valid(self, expression, IR_expression):
        """Checks if shift expression is valid.
        Args:
        expression: Types in current expression.
        IR_expression: IR nodes making up expression."""
        valid_shift_operands = [DATA_TYPE.INT_VAL, DATA_TYPE.BS_INT_VAL, DATA_TYPE.SEQ_BS_BIT_VAL, DATA_TYPE.SEQ_BIT_VAL]
        if (expression['OPERAND_2'] == DATA_TYPE.INT_VAL or expression['OPERAND_2'] == DATA_TYPE.BS_INT_VAL) and (expression['OPERAND_0'] in valid_shift_operands):
            self.expr_seq_bit_dims(IR_expression)
            return True
        return False

    def arith_expr_valid(self, expression, IR_expression):
        """Checks if arithmetic expression is valid.
        Args:
        expression: Types in current expression.
        IR_expression: IR nodes making up expression."""
        valid_operands_types = {DATA_TYPE.INT_VAL: [DATA_TYPE.INT_VAL, DATA_TYPE.BS_INT_VAL, DATA_TYPE.SEQ_BIT_VAL, DATA_TYPE.SEQ_BS_BIT_VAL],
                                DATA_TYPE.BS_INT_VAL: [DATA_TYPE.INT_VAL, DATA_TYPE.BS_INT_VAL, DATA_TYPE.SEQ_BIT_VAL],
                                DATA_TYPE.SEQ_BIT_VAL: [DATA_TYPE.INT_VAL, DATA_TYPE.BS_INT_VAL, DATA_TYPE.SEQ_BIT_VAL]}
        try:
            if expression['OPERAND_0'] in valid_operands_types[expression['OPERAND_2']]:
                self.expr_seq_bit_dims(IR_expression)
                self.validate_bs_int_arith(expression, IR_expression)
                return True
        except KeyError:
            return False
        return False

    def validate_bs_int_arith(self, expression, IR_expression):
        if expression['OPERAND_0'] == DATA_TYPE.BS_INT_VAL or expression['OPERAND_2'] == DATA_TYPE.BS_INT_VAL:
            if IR_expression[1].operator == "/" or IR_expression[1].operator == "%":
                raise SemanticException("Cannot use " +  IR_expression[1].operator + " operator on " + str(DATA_TYPE.BS_INT_VAL))

    def expr_seq_bit_dims(self, IR_expression):
        """Validates that the dimensions of the sequence of bits being combined in expression are valid

        Args:
        IR_expressions : IR expression nodes."""
        for op in IR_expression:
            if DATA_TYPE.is_seq_type(op.node_type) and op.dim_s != 1:
                raise SemanticException("Cannot combine " + str(DATA_TYPE.SEQ_BIT_VAL) + (op.dim_s * "[]") + "in " + str(IR_expression[1].node_type))


    def reduce_sub_expr(self, expression):
        """Determines result type of current expression.

        Args:
        expression: Types making up current expression"""
        if expression['OP'] is DATA_TYPE.ARITH_OP:
            return {'OPERAND_0': self.reduce_arith_op(expression)}
        if expression['OP'] is DATA_TYPE.SHIFT_OP:
            return {'OPERAND_0': expression['OPERAND_0']}
        if expression['OP'] is DATA_TYPE.BITWISE_OP:
            return {'OPERAND_0': self.reduce_bitwise_op(expression)}
        if expression['OP'] is DATA_TYPE.COMP_OP:
            return {'OPERAND_0': DATA_TYPE.BIT_VAL}
        if expression['OP'] is DATA_TYPE.LOG_OP:
            return {'OPERAND_0': DATA_TYPE.BIT_VAL}
        else:
            raise InternalException("Unrecognised operator")

    def reduce_arith_op(self, expression):
        if expression['OPERAND_0'] == DATA_TYPE.BS_INT_VAL or expression['OPERAND_2'] == DATA_TYPE.BS_INT_VAL:
            return DATA_TYPE.BS_INT_VAL
        else:
            return DATA_TYPE.INT_VAL

    def reduce_bitwise_op(self, expression):
        if expression['OPERAND_0'] == DATA_TYPE.BS_INT_VAL or expression['OPERAND_2'] == DATA_TYPE.BS_INT_VAL:
            return DATA_TYPE.BS_INT_VAL
        elif expression['OPERAND_0'] == DATA_TYPE.SEQ_BS_BIT_VAL or expression['OPERAND_2'] == DATA_TYPE.SEQ_BS_BIT_VAL:
            return DATA_TYPE.SEQ_BS_BIT_VAL
        else:
            return expression['OPERAND_0']

    def build_ret_val(self, ast_node):
        """Returns IR declaration node for AST return statement"""
        if ast_node == DATA_TYPE.VOID:
            return DATA_TYPE.VOID
        if DATA_TYPE.is_int_val(DATA_TYPE.decl_to_value(ast_node.node_type)):
            return self.analyse_int_decl(ast_node)
        elif ast_node.node_type == DATA_TYPE.SEQ_INT_DECL or ast_node.node_type == DATA_TYPE.BS_SEQ_INT_DECL:
            return self.analyse_bit_cnst_seq(ast_node)
        elif ast_node.node_type == DATA_TYPE.SEQ_BIT_DECL:
            return self.analyse_bit_seq(ast_node)
        elif ast_node.node_type == DATA_TYPE.BIT_DECL:
            return self.analyse_bit_decl(ast_node)
        elif ast_node.node_type == DATA_TYPE.BS_BIT_DECL:
            return self.analyse_bit_decl(ast_node)
        else:
            raise InternalException("Internal Error: Unrecognised return type")

    def analyse_func_decl(self, node):
        """Performs Semantic Analysis on function declaration and body, creating an IR node if successful"""
        try:
            correct = True
            self.sym_table.add_scope()
            ret_val = self.build_ret_val(node.return_value)
            func_decl = Function_decl(node.ID, ret_val)
            ret_pres = False
            for p in node.parameters:
                if p.node_type == DATA_TYPE.SBOX_DECL:
                    raise SemanticException("Sboxes cannot be passed as function parameters")
                func_decl.parameters.append(self.AST_func_param_to_IR(p))
            for s in node.stmts:
                if s.node_type == DATA_TYPE.SBOX_DECL:
                    raise SemanticException("Sboxes must be declared as global variables")
                if s.node_type == DATA_TYPE.RETURN_STMT:
                    ret_pres = True
                    func_decl.body.append(self.analyse_return_stmt(s, func_decl))
                else:
                    try:
                        func_decl.body.append(self.analyse_sub_stmt(s))
                    except SemanticException as details:
                        Semantic_analysis_errors.semantic_err(node, details)
                        correct = False
            if func_decl.return_type != DATA_TYPE.VOID and ret_pres is False:
                raise SemanticException("Function " + str(func_decl.ID.name) + " requires return value " + str(func_decl.return_type))
            self.sym_table.leave_scope()
            if correct is True:
                return func_decl
            return False
        except SemanticException as details:
            Semantic_analysis_errors.semantic_err(node, details)
            return False

    def AST_func_param_to_IR(self, old_decl):
        """Converts AST param node to equivilent IR node"""
        decl = None
        if old_decl.node_type == DATA_TYPE.INT_DECL or old_decl.node_type == DATA_TYPE.BS_INT_DECL:
            decl = Int_decl(old_decl.node_type, self.expr_type_is(old_decl.bit_constraints), Name(old_decl.ID, DATA_TYPE.decl_to_value(old_decl.node_type)))
            self.sym_table.add_id(decl.ID.name, decl.ID.type)
            self.sym_table.id(decl.ID.name)['constraints'] = decl.constraints
            self.sym_table.id(decl.ID.name)['size'] = None
        elif old_decl.node_type == DATA_TYPE.SEQ_BIT_DECL:
            decl = Seq_decl(old_decl.node_type, self.analyse_array_size(old_decl), old_decl.ID)
            self.sym_table.add_id(decl.ID.name, decl.ID.type)
            self.sym_table.id(decl.ID.name)['size'] = decl.size
            self.sym_table.id(decl.ID.name)['constraints'] = None
        elif old_decl.node_type == DATA_TYPE.SEQ_INT_DECL or old_decl.node_type == DATA_TYPE.BS_SEQ_INT_DECL or old_decl.node_type == DATA_TYPE.SBOX_DECL:
            decl = Seq_decl(old_decl.node_type, self.analyse_array_size(old_decl), old_decl.ID, constraints=self.expr_type_is(old_decl.bit_constraints))
            if old_decl.node_type == DATA_TYPE.SBOX_DECL:
                self.sym_table.add_id(decl.ID.name, DATA_TYPE.SBOX_DECL)
            else:
                self.sym_table.add_id(decl.ID.name, decl.ID.type)
            self.sym_table.id(decl.ID.name)['constraints'] = decl.constraints
            self.sym_table.id(decl.ID.name)['size'] = decl.size
        elif old_decl.node_type == DATA_TYPE.BIT_DECL or old_decl.node_type == DATA_TYPE.BS_BIT_DECL:
            decl = Bit_decl(Name(old_decl.ID, DATA_TYPE.BIT_VAL), old_decl.node_type)
            self.sym_table.add_id(decl.ID.name, decl.ID.type)
            self.sym_table.id(decl.ID.name)['constraints'] = None
            self.sym_table.id(decl.ID.name)['size'] = None
        else:
            raise InternalException("Internal Error: Unknown Parameter Type " + str(old_decl.node_type))
        self.sym_table.id(decl.ID.name)['f_param'] = True
        return decl

    def analyse_sub_stmt(self, node):
        stmt = Semantic_analyser.node_type_lookup[node.node_type](self, node)
        if stmt is False:
            raise SemanticException("Error in sub statement")
        return stmt

    def analyse(self, AST, prod=False):
        correct = True
        result = None
        for node in AST.tree:
            try:
                if prod is True:
                    # Disallows global scope declarations on live runs,
                    # allowing testing to work without having to declare functions
                    self.validate_scope(node)
                result = Semantic_analyser.node_type_lookup[node.node_type](self, node)
            except SemanticException as details:
                Semantic_analysis_errors.semantic_err(node, details)
                result = False
            if result is not False:
                self.IR.add(result)
            else:
                correct = False
        return correct