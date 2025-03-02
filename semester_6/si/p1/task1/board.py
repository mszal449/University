from typing import List

from king import King
from pawn_moves import PawnMoves
from rook import Rook
from state import State
from task1.utils import position_to_indices


class Board:
    def __init__(self, state: State):
        self.state = state

    def is_checkmate(self) -> bool:
        if self.state.turn != "black":
            return False

        # First check if black king has any moves
        if King.valid_moves(self.state):
            return False

        # Then check if black king is under attack from rook
        bk_row, bk_col = position_to_indices(self.state.bk)
        wr_row, wr_col = position_to_indices(self.state.wr)

        # King is in check if rook attacks along row or column
        if bk_row == wr_row or bk_col == wr_col:
            # Check if path is clear (not blocked by white king)
            wk_row, wk_col = position_to_indices(self.state.wk)

            if bk_row == wr_row:  # Same row
                min_col, max_col = min(bk_col, wr_col), max(bk_col, wr_col)
                return not (wk_row == bk_row and min_col < wk_col < max_col)
            else:  # Same column
                min_row, max_row = min(bk_row, wr_row), max(bk_row, wr_row)
                return not (wk_col == bk_col and min_row < wk_row < max_row)

        # King is not attacked by rook
        return False

    def get_valid_moves(self) -> List[PawnMoves]:
        if self.state.turn == "black":
            king_moves = King.valid_moves(self.state)
            return [PawnMoves("black", "bk", king_moves)]
        else:
            king_moves = King.valid_moves(self.state)
            rook_moves = Rook.valid_moves(self.state)
            return [
                PawnMoves("white", "wk", king_moves),
                PawnMoves("white", "wr", rook_moves)
            ]