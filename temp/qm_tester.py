def bit_in_0(D, C, B, A):
    return (((~D & B & ~A) | (D & ~B & A) | (~C & ~B & A) | (~D & ~C & ~A) | (C & B & ~A) | (~D & C & B)) & 0x1)


def bit_in_1(D, C, B, A):
    return (((~B & ~A) | (~C & ~B) | (~D & ~C)) & 0x1)


def bit_in_2(D, C, B, A):
    return (((D & C) | (~B & A) | (D & ~B)) & 0x1)


def bit_in_3(D, C, B, A):
    return (((D & B & ~A) | (~D & ~B) | (C & ~A)) & 0x1)


def conv(in_):
    D = in_ >> 3
    C = in_ >> 2
    B = in_ >> 1
    A = in_ >> 0
    return (D, C, B, A)


def all_in(i):
    return(bit_in_3(*conv(i)), bit_in_2(*conv(i)), bit_in_1(*conv(i)), bit_in_0(*conv(i)))

if __name__ == '__main__':
    for i in range(0, 16):
        print(str(i) + ", " + str(conv(i)) + "=> " + str(all_in(i)))
