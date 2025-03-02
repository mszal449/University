from simulation import Simulation
from task1.state import State
from utils import read_input, position_to_indices, indices_to_position

initial_states = read_input("./zad1_input.txt")
def clear_caches():
    from task1.king import King
    from task1.rook import Rook
    King.moves_cache.clear()
    Rook.moves_cache.clear()

# Run simulation
with open("zad1_output.txt", "w") as file:
    for initial_state in initial_states:
        clear_caches()
        sim = Simulation(initial_state)

        res = sim.find_checkmate()
        if res == -1:
            file.write("INF\n")
        else:
            file.write("{}\n".format(res))


_king_moves = [
    (0, 1),  # right
    (1, 1),  # up-right
    (1, 0),  # up
    (1, -1),  # up-left
    (0, -1),  # left
    (-1, -1),  # down-left
    (-1, 0),  # down
    (-1, 1)  # down-right
]
def check_collision(wk_pos, bk_pos):
    wk_row, wk_col = position_to_indices(wk_pos)
    bk_row, bk_col = position_to_indices(bk_pos)
    turn = "black"

    valid_moves = []

    for dx, dy in _king_moves:
        new_row, new_col = bk_row + dy, bk_col + dx

        # Check boundaries
        if not (0 <= new_col < 8 and 0 <= new_row < 8):
            continue

        new_pos = indices_to_position(new_row, new_col)

        # check if it's occupied
        if new_pos in [wk_pos, bk_pos]:
            continue

        if turn == "black":
            # check white king's attack range
            wk_row, wk_col = position_to_indices(wk_pos)

            if abs(wk_row - new_row) <= 1 and abs(wk_col - new_col) <= 1:
                continue

        else:
            # check black king's attack range
            bk_row, bk_col = position_to_indices(bk_pos)
            if abs(bk_row - new_row) <= 1 and abs(bk_col - new_col) <= 1:
                continue

        valid_moves.append(new_pos)

    return valid_moves

# print(check_collision("h7", "f7"))