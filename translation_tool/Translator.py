from Parser import Parser, Semantic_analyser
from Data_reader import Data_reader
import sys


class Translator:

    def run(data_in):
        Semantic_analyser.analyse(Parser.parse(data_in))

    def run_test(data_in):
        Semantic_analyser.analyse_test(Parser.parse_test(data_in))

TESTING = 1

if __name__ == "__main__":
    d_in = Data_reader()
    if TESTING == 1:
        Translator.run_test(d_in.read_file(sys.argv[1]))
    else:
        Translator.run(d_in.read_file(sys.argv[1]))
