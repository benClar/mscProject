class Data_reader(object):

    def read_file(self, filename):
        return open(filename).read()

    def write(location, name, output):
        headers = \
        "#include <stdio.h>\n\
#include <string.h>\n\
#include <stdlib.h>\n\
#include <stdint.h>\n\
\n\
#include \"" + name + ".h\""
        with open("../DSL/testing/" + location + "/" + name + ".c", "w") as text_file:
            print(headers, file=text_file)
            print(output, file=text_file)
