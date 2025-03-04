from collections import deque
from copy import copy
from typing import List
from tabulate import tabulate

from task1.utils import chess_to_cords, cords_to_chess


class GameState:
    turn: str
    w_king: List[int]
    w_rook: List[int]
    b_king: List[int]

    def __init__(self, turn: str, w_king, w_rook, b_king):
        self.turn = turn

        # Handle both string chess notation and direct coordinate inputs
        if isinstance(w_king, str):
            self.w_king = chess_to_cords(w_king)
        else:
            self.w_king = w_king

        if isinstance(w_rook, str):
            self.w_rook = chess_to_cords(w_rook)
        else:
            self.w_rook = w_rook

        if isinstance(b_king, str):
            self.b_king = chess_to_cords(b_king)
        else:
            self.b_king = b_king

    def __str__(self):
        return f'{self.turn} {cords_to_chess(self.w_king)} {cords_to_chess(self.w_rook)} {cords_to_chess(self.b_king)}'

    def __eq__(self, other):
        if not isinstance(other, GameState):
            return False
        return (self.turn == other.turn and
                self.w_king == other.w_king and
                self.w_rook == other.w_rook and
                self.b_king == other.b_king)

    def __hash__(self):
        return hash((self.turn, tuple(self.w_king), tuple(self.w_rook), tuple(self.b_king)))


def get_rook_fields(pos: List[int]) -> set:
    x, y = pos
    v_fields = {(x, i) for i in range(8)}
    h_fields = {(i, y) for i in range(8)}

    return v_fields.union(h_fields)

def get_king_fields(pos: List[int])-> set:
    x, y = pos
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    return {(x + dx, y + dy) for dx, dy in directions if 0 <= x + dx < 8 and 0 <= y + dy < 8}

def is_checkmate(state: GameState):
    if state.turn == "white":
        return False

    w_king_pos = state.w_king
    rook_pos = state.w_rook
    b_king_pos = state.b_king

    w_king_fields = get_king_fields(w_king_pos)
    rook_fields = get_rook_fields(rook_pos)
    b_king_fields = get_king_fields(b_king_pos)

    # check if black king can escape check by capturing pawn
    if w_king_pos in b_king_fields and not w_king_pos in rook_fields:
        return False

    if rook_pos in b_king_fields and not rook_pos in w_king_fields:
        return False

    # check if black king has moves outside attacked fields
    w_fields = w_king_fields.union(rook_fields)

    for f in b_king_fields:
        if f not in w_fields:
            return False
    return True

def find_next_moves(state: GameState) -> List[GameState]:
    w_king_fields = get_king_fields(state.w_king)
    rook_fields = get_rook_fields(state.w_rook)
    b_king_fields = get_king_fields(state.b_king)

    if state.turn == "white":
        invalid_states = {state}.union(b_king_fields)

        new_king_states = [GameState(
            "black",
            x,
            state.w_rook,
            state.b_king) for x in w_king_fields if x not in invalid_states]

        new_rook_states = [GameState(
            "black",
            state.w_king,
            x,
            state.b_king) for x in rook_fields if x not in invalid_states]

        return new_king_states + new_rook_states

    else:
        invalid_states = {state}.union(w_king_fields).union(rook_fields)
        return [GameState(
            "white",
            state.w_king,
            state.w_rook,
            x
        ) for x in b_king_fields if x not in invalid_states]

def get_move_history(l_state: GameState, checked_moves: dict):
    history = [l_state]
    while True:
        prev = checked_moves[history[-1]]
        if prev:
            history.append(prev)
        else:
            break

    return history

def print_chess_board(state: GameState):
    print(str(state))
    headers = [" ", "a", "b", "c", "d", "e", "f", "g", "h"]
    table = []

    for i in range(8):
        row = [i + 1]
        for j in range(8):
            row.append('')
        table.append(row)

    table[state.w_king[0]][state.w_king[1] + 1] = "W"
    table[state.w_rook[0]][state.w_rook[1] + 1] = "R"
    table[state.b_king[0]][state.b_king[1] + 1] = "B"

    print(tabulate(table, headers, tablefmt="grid"))



def find_ending(start_state: GameState, debug=False, history=False, graphics=True) -> int:
    checked_moves = {}  # Set to store checked states
    move_history = {}   # Moves tree for history retrieval

    initial_state = copy(start_state)
    queue = deque()
    queue.append((initial_state, 0, None))
    min_moves = float('inf')
    ending_move = None

    while queue:
        el = queue.popleft()
        curr = el[0]
        curr_count = el[1]
        prev_state = el[2]

        if not curr in checked_moves:
            if debug:
                print(f'Checking move: {str(curr)}, moves: {curr_count}')

            # Check if checkmate
            if is_checkmate(curr):
                min_moves = curr_count
                ending_move = curr
                move_history[curr] = prev_state
                break

            # Add current state to checked moves and history
            checked_moves[curr] = curr_count
            move_history[curr] = prev_state

            # Find next moves
            next_moves = find_next_moves(curr)

            filtered_moves = [(x, curr_count + 1, curr) for x in next_moves if x not in checked_moves]

            for x in filtered_moves:
                queue.append(x)

    if not ending_move:
        return -1

    if debug:
        print(f"Ending move: {str(ending_move)}")

    if history:
        history = get_move_history(ending_move, move_history)
        print('Moves history:')
        for move in history:
            print(str(move))

    if graphics:
        history = get_move_history(ending_move, move_history)
        print('Moves history:')
        for x in history[::-1]:
            print_chess_board(x)

    return min_moves


# Read data
f_in = open('zad1_input.txt', 'r')
data = f_in.readlines()
inputs = []
for x in data:
    splitted = x.split()
    inputs.append((*splitted, ))

f_out = open('zad1_output.txt', 'w')

for x in inputs:
    res = find_ending(
        GameState(
            x[0],
            x[1],
            x[2],
            x[3]
        )
    )
    if res == -1:
        f_out.write("INF\n")
    else:
        f_out.write(str(res) + '\n')

