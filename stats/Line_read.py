def read(file_name):
    vals = []
    with open(file_name, "rU") as f:
        for line in f:
            vals.append(int(line))
    return vals