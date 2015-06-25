expr = ['a', 'b', 'c', 'd', 'e']

for i, letter in enumerate(expr):
    print(i)
    print(letter)
    if letter == 'c':
        expr = expr[:i]
        break