from typing import List

from state import State


def read_input(filename: str) -> List[State]:
    res = []
    with open(filename, 'r') as file:
        line = file.readline()
        line = line.split(" ")
        res.append(State(
            line[0],
            line[1],
            line[2],
            line[3]))

    return res

def position_to_indices(position: str) -> tuple[int, int]:
    col = ord(position[0]) - ord('a')
    row = int(position[1]) - 1
    return row, col

def indices_to_position(row: int, col: int) -> str:
    return f"{chr(col + ord('a'))}{row + 1}"

