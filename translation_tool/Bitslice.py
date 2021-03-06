from Parser import Parser
import sys
from Translation_exceptions import ReadException
from Data_reader import Data_reader


class Bitslice(object):
    """Calls each phase of translation process to produced
    bitsliced output"""
    translation_tool = Parser()

    def translate(file_name):
        """Translates validated program"""
        Bitslice.validate(file_name.split("."))
        print(file_name)
        # with open(file_name, "rU") as f:
        # print(f.read())
        return Bitslice.translation_tool.parse(Data_reader.read_file(file_name))

    def validate(name):
        """Validates DSL input"""
        if len(name) != 2 or name[1] != "dsl":
            raise ReadException("File to translate doesn't have .dsl extension")
        else:
            return name

if __name__ == "__main__":
    if len(sys.argv) > 2 or len(sys.argv) == 1:
        raise ReadException("Please supply single file name for translation")
    else:
        # Bitslice.translate("in/" + sys.argv[1])
        Data_reader.write(sys.argv[1].split(".")[0], Bitslice.translate("in/" + sys.argv[1]))