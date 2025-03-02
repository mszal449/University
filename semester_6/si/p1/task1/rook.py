from typing import List
from task1.state import State
from task1.utils import position_to_indices


class Rook:
    moves_cache = {}
    _directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # right, left, down, up

    def __init__(self, color: str, position: str):
        self.color = color
        self.position = position


    @staticmethod
    def valid_moves(state: State, maintain_attack=True) -> List[str]:
        if state.turn == "black":
            return []

        cache_key = (state.wk, state.wr, state.bk)
        if cache_key in Rook.moves_cache:
            return Rook.moves_cache[cache_key]

        valid_moves = []
        row, col = position_to_indices(state.wr)

        for dx, dy in Rook._directions:
            new_col, new_row = col + dx, row + dy

            while 0 <= new_col < 8 and 0 <= new_row < 8:
                new_pos = f"{chr(new_col + ord('a'))}{new_row + 1}"

                # stop if the new position is occupied (can not move through pieces)
                if new_pos in [state.wk, state.wr, state.bk]:
                    break

                #
                bk_row, bk_col = position_to_indices(state.bk)
                if new_row == bk_row or new_col == bk_col:
                    if maintain_attack:
                        if not Rook.is_king_attacked(new_row, new_col, bk_row, bk_col, state.wk):
                            continue

                new_col += dx
                new_row += dy

                valid_moves.append(new_pos)

        Rook.moves_cache[cache_key] = valid_moves
        return valid_moves

    @staticmethod
    def is_king_attacked(rook_row: int, rook_col: int, king_row: int, king_col: int, wk_pos: str) -> bool:
        """Check if rook attacks black king and path isn't blocked by white king"""
        if rook_row == king_row:
            wk_row, wk_col = position_to_indices(wk_pos)
            return not (wk_row == rook_row and
                        min(rook_col, king_col) < wk_col < max(rook_col, king_col))
        if rook_col == king_col:
            wk_row, wk_col = position_to_indices(wk_pos)
            return not (wk_col == rook_col and
                        min(rook_row, king_row) < wk_row < max(rook_row, king_row))
        return False
