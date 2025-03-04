from typing import List

def chess_to_cords(pos: str):
    return int(pos[1]) - 1, ord(pos[0]) - ord("a")

def cords_to_chess(cords: List[int]):
    x, y = cords
    return chr(y + ord("a")) + str(x + 1)
