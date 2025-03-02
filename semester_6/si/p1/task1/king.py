from typing import List
from task1.state import State
from task1.utils import position_to_indices, indices_to_position


class King:
    moves_cache = {}
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

    def __init__(self, color: str, position: str):
        self.color = color
        self.position = position

    @staticmethod
    def valid_moves(state: State) -> List[str]:
        """
        Returns a list of valid moves for white or black king in regard to game's turn.
        Valid moves are
        """

        # if state.turn == "black" and state.bk == "f7" and state.wr == "h7":
        #     print("HERE")

        if state.turn == "black":
            cache_key = (state.bk, state.wk, state.wr)
        else:
            cache_key = (state.wk, state.wr, state.bk)

        if cache_key in King.moves_cache:
            return King.moves_cache[cache_key]

        king_pos = state.bk if state.turn == "black" else state.wk
        row, col = position_to_indices(king_pos)

        valid_moves = []

        for dx, dy in King._king_moves:
            new_row, new_col = row + dy, col + dx

            # Check boundaries
            if not (0 <= new_col < 8 and 0 <= new_row < 8):
                continue

            new_pos = indices_to_position(new_row, new_col)

            # check if it's occupied
            if new_pos in [state.wk, state.wr, state.bk]:
                continue

            if state.turn == "black":
                # check white king's attack range
                wk_row, wk_col = position_to_indices(state.wk)
                if abs(wk_row - new_row) <= 1 and abs(wk_col - new_col) <= 1:
                    continue

                # check rook's attack
                wr_row, wr_col = position_to_indices(state.wr)
                if new_col == wr_col or new_row == wr_row:
                    # skip if rook has a clear line of attack
                    if not King.is_path_blocked(new_col, new_row, wr_col, wr_row, state):
                        continue

            else:
                # check black king's attack range
                bk_row, bk_col = position_to_indices(state.bk)
                if abs(bk_row - new_row) <= 1 and abs(bk_col - new_col) <= 1:
                    continue

            valid_moves.append(new_pos)

        King.moves_cache[cache_key] = valid_moves
        return valid_moves

    @staticmethod
    def is_path_blocked(x1: int, y1: int, x2: int, y2: int, state: State) -> bool:
        pieces = {state.wk, state.wr, state.bk}

        if x1 == x2:  # Vertical path
            for y in range(min(y1, y2) + 1, max(y1, y2)):
                pos = f"{chr(x1 + ord('a'))}{y + 1}"
                if pos in pieces:
                    return True
        elif y1 == y2:  # Horizontal path
            for x in range(min(x1, x2) + 1, max(x1, x2)):
                pos = f"{chr(x + ord('a'))}{y1 + 1}"
                if pos in pieces:
                    return True

        return False
