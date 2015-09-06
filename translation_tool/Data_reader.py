class Data_reader(object):

    def read_file(filename):
        return open(filename).read()

    def write_test(location, name, output):
        if output == False:
            return False
        include_c = \
        "#include <stdio.h>\n\
#include <string.h>\n\
#include <stdlib.h>\n\
#include <stdint.h>\n\
\n\
#include \"" + name + ".h\""
        include_h = "#include \"../../../LIB/BS_LIB.h\"\n"
        with open("../DSL/testing/" + location + "/" + name + ".c", "w") as text_file:
            print(include_c, file=text_file)
            print(output['main'], file=text_file)
        with open("../DSL/testing/" + location + "/" + name + ".h", "w") as text_file:
            print(include_h, file=text_file)
            print(output['header'], file=text_file)
        return True

    def write(name, output):
        if output is None:
            return False
        include_c = \
        "#include <stdio.h>\n\
#include <string.h>\n\
#include <stdlib.h>\n\
#include <stdint.h>\n\
\n\
#include \"" + name + ".h\""
        include_h = "#include \"BS_LIB.h\"\n"
        with open("./out/" + name + ".c", "w") as text_file:
            print(include_c, file=text_file)
            print(output['main'], file=text_file)
        with open("./out/" + name + ".h", "w") as text_file:
            print(include_h, file=text_file)
            print(output['header'], file=text_file)
        return True