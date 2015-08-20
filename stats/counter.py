import sys
from collections import OrderedDict

def read(file_name):
    vals = []
    with open(file_name, "rU") as f:
        for line in f:
            vals.append(int(line))
    return vals

def group(groups, vals):
    grouped_vals = {}
    for i in groups:
        grouped_vals[i] = []
    for v in vals:
        for g in groups:
            if v < g:
                grouped_vals[g].append(v)
                break
    return grouped_vals

def group_len(grouped_vals):
    sum_ = 0
    for key, value in grouped_vals.items():
        sum_ += len(value)
    grouped_vals['excluded'] = 1000 - sum_
    for key, value in grouped_vals.items():
        try:
            print(str(key) + " :" + str(len(value)))
        except TypeError:
            print(key + " :" + str(value))

if __name__ == '__main__':
    group_len(group([10000, 15000, 20000, 25000, 30000], read(sys.argv[1])))
    
