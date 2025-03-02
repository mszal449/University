from typing import List

class PawnMoves:
    def __init__(self, color: str, pawn: str, moves: List[str]):
        self.moves = moves
        self.color = color
        self.pawn = pawn
