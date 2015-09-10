class Data_reader(object):
    """Reads and writes I/O for translation tool"""

    def read_file(filename):
        """Reads in file.

        Args:
            filename: Name of file."""
        return open(filename).read()

    def write_test(location, name, output):
        """Writes test output.

        Args:
            location: location that file should be written.
            name: Name of file.
            output: Whether write should continue(will be false if there has been an error)"""
        if output is False:
            return False
        include_c = \
            "#include <stdio.h>\n\
#include <string.h>\n\
#include <stdlib.h>\n\
#include <stdint.h>\n\
\n\
#include \"" + name + ".h\""
        include_h = "#include \"../../out/BS_LIB.h\"\n"
        with open("./test_output/" + location + "/" + name + ".c", "w") as text_file:
            print(include_c, file=text_file)
            print(output['main'], file=text_file)
        with open("./test_output/" + location + "/" + name + ".h", "w") as text_file:
            print(include_h, file=text_file)
            print(output['header'], file=text_file)
        return True

    def write(name, output):
        """Prod write output.

        Args:
            name: name of file.
            output: Whether write should continue(will be false if there has been an error)"""

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