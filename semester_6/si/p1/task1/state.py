class State:
    def __init__(self, turn: str, wk: str, wr: str, bk: str):
        self.turn = turn
        self.wk = wk
        self.wr = wr
        self.bk = bk

    def __str__(self):
        return f"turn: {self.turn} | wk:{self.wk} | wr: {self.wr} | bk: {self.bk}"
