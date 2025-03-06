from typing import List


def opt_dist(bits, d):
    print("input: {}".format(bits))
    # Special case: no block needed
    if d == 0:
        return sum(bits)

    n = len(bits)

    # If block is larger than list, impossible to place
    if d > n:
        return float('inf')

    min_changes = float('inf')

    # Try all possible placements of the block
    for start in range(n - d + 1):
        # Changes needed to create block of 1s
        block_changes = 0
        for i in range(start, start + d):
            if bits[i] == 0:
                block_changes += 1

        # Changes needed before the block
        before_changes = sum(bits[:start])

        # Changes needed after the block
        after_changes = sum(bits[start + d:])

        # Total changes for this placement
        total_changes = block_changes + before_changes + after_changes

        # Update minimum changes
        min_changes = min(min_changes, total_changes)

    return min_changes


inputs = []
with open("zad4_input.txt", 'r') as file:
    for line in file:
        # Split the line into the bit string and the number
        bits_str, d_str = line.strip().split()

        # Convert bit string to list of integers
        bits = [int(bit) for bit in bits_str]

        # Convert d to integer
        d = int(d_str)

        inputs.append((bits, d))

with open('zad4_output.txt', 'w') as file:
    for (x, y) in inputs:
        file.write(str(opt_dist(x, y)) + "\n")