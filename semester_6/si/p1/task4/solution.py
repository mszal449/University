from z4 import opt_dist

f_in = open('zad4_input.txt', 'r')
inputs = []
for l in f_in.readlines():
    x, y = l.strip().split()
    inputs.append((x, y))

f_out = open('zad4_output.txt', 'w')

for (x, y) in inputs:
    f_out.write(str(opt_dist([int(n) for n in x], int(y))) + "\n")
