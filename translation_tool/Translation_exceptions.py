from DATA_TYPE import DATA_TYPE

class SemanticException(Exception):
    pass


class InternalException(Exception):
    pass

class err_format():

    error = "\033[01;31m{0}\033[00m"
    var = "\033[01;33m{0}\033[00m"
    msg = '\033[01;41m{0}\033[00m'
class Semantic_analysis_errors():

    error_lookup = {DATA_TYPE.INT_DECL: lambda node, error_message: Semantic_analysis_errors.int_decl_error(node, error_message),
                    DATA_TYPE.BIT_DECL: lambda node, error_message: Semantic_analysis_errors.bit_decl_error(node, error_message),
                    DATA_TYPE.ID_SET: lambda node, error_message: Semantic_analysis_errors.set_error(node, error_message),
                    DATA_TYPE.FUNC_DECL: lambda node, error_message: Semantic_analysis_errors.func_decl_error(node, error_message),
                    DATA_TYPE.IF_STMT: lambda node, error_message: Semantic_analysis_errors.if_stmt_error(node, error_message),
                    DATA_TYPE.FOR_LOOP: lambda node, error_message: Semantic_analysis_errors.for_loop_error(node, error_message),
                    DATA_TYPE.SEQ_INT_DECL: lambda node, error_message: Semantic_analysis_errors.word_width_seq_decl_error(node, error_message),
                    DATA_TYPE.SEQ_BIT_DECL: lambda node, error_message: Semantic_analysis_errors.bit_seq_decl_error(node, error_message),
                    DATA_TYPE.BS_SEQ_INT_DECL: lambda node, error_message: Semantic_analysis_errors.word_width_seq_decl_error(node, error_message),
                    DATA_TYPE.BS_INT_DECL: lambda node, error_message: Semantic_analysis_errors.int_decl_error(node, error_message),
                    DATA_TYPE.SBOX_DECL: lambda node, error_message: Semantic_analysis_errors.word_width_seq_decl_error(node, error_message),
                    DATA_TYPE.EXPR: lambda node, error_message: Semantic_analysis_errors.expr_error(node, error_message)}

    def int_decl_error(node, error_message):
        print(err_format.error.format("Error") + " in declaration of Int variable " + err_format.var.format(node.ID) + ":")
        print(err_format.msg.format(error_message))

    def bit_decl_error(node, error_message):
        print(err_format.error.format("Error") + " in declaration of Bit variable " + err_format.var.format(node.ID) + ":")
        print(err_format.msg.format(error_message))

    def set_error(node, error_message):
        target = None
        if node.target.node_type == DATA_TYPE.ID:
            target = node.target.ID
        elif node.target.node_type == DATA_TYPE.INDEX_SELECT:
            if node.target.target.node_type == DATA_TYPE.ID:
                target = node.target.target.ID
            else:
                target = "Cast"

        print(err_format.error.format("Error") + " setting variable " + err_format.var.format(target) + ":")
        print(err_format.msg.format(error_message))

    def func_decl_error(node, error_message):
        print(err_format.error.format("Error") + " in declaration of function " + err_format.var.format(node.ID) + ":")
        print(error_message)

    def if_stmt_error(node, error_message):
        print(err_format.msg.format(error_message))

    def for_loop_error(node, error_message):
        print(err_format.msg.format(error_message))

    def word_width_seq_decl_error(node, error_message):
        print(err_format.error.format("Error") + " in declaration of Sequence " + err_format.var.format(node.ID) + ":")
        print(err_format.msg.format(error_message))

    def bit_seq_decl_error(node, error_message):
        print(err_format.error.format("Error") + " in declaration of Sequence " + err_format.var.format(node.ID) + ":")
        print(err_format.msg.format(error_message))

    def expr_error(node, error_message):
        print(err_format.error.format("Error") + " in expression" + ":")
        print(err_format.msg.format(error_message))

    def semantic_err(node, error_message):
        Semantic_analysis_errors.error_lookup[node.node_type](node, error_message)