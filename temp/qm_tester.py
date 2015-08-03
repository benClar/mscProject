def bit_in(D, C, B, A):
    return (((~D & ~C & ~A) | (~C & ~B & A) | (C & B & ~A) | (D & ~B & A) | (~D & B & ~A) | (~D & C & B)) & 0x1)

def bit_in_0(D, C, B, A):
    return (((C & B & ~A) | (~C & ~B & A) | (~D & ~C & ~B) | (~D & C & B) | (D & ~B & A) | (~D & B & ~A)) & 0x1)

def bit_in_1(D, C, B, A):
    return (((~C & ~B) | (~D & ~C) | (~B & ~A)) & 0x1)

def bit_in_2(D, C, B, A):
    return (((~B & A) | (D & ~B) | (D & C)) & 0x1)

def bit_in_3(D, C, B, A):
    return (((C & ~A) | (~D & ~B) | (D & B & ~A)) & 0x1)

def conv(in_):
    D = in_ >> 3
    C = in_ >> 2
    B = in_ >> 1
    A = in_ >> 0
    return (D, C, B, A)

if __name__ == '__main__':
    for i in range(0, 16):
        print(str(i) + "=> " + str(bit_in_3(*conv(i))))

