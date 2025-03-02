from collections import deque

from task1.board import Board
from task1.state import State


class Simulation:
    def __init__(self, initial_state: State):
        self.initial_board = Board(initial_state)
        self.checked_states = set()
        self.moves_to_reach = {}
        print("Initial state:" + str(initial_state))

    def find_checkmate(self, move_limit=100) -> int:
        queue = deque([(self.initial_board, [])])  # (board, moves_history)

        # Initialize tracking for the initial state
        initial_hash = self._hash_state(self.initial_board.state)
        self.checked_states.add(initial_hash)
        self.moves_to_reach[initial_hash] = 0

        # Add tracking variables
        explored_states = 0
        max_depth = 0

        while queue:
            current_board, moves = queue.popleft()
            current_moves = len(moves)

            # Print progress periodically
            # if explored_states % 1000 == 0:
            #     print(f"Explored: {explored_states}, Queue: {len(queue)}, Max depth: {max_depth}")

            explored_states += 1
            max_depth = max(max_depth, current_moves)

            # Set a limit to prevent infinite loops
            if current_moves >= move_limit:
                continue

            # Check if it's a checkmate
            if current_board.is_checkmate():
                print(f"Found checkmate after exploring {explored_states} states")
                print("Checkmate moves:", moves)
                return current_moves

            # Generate next boards
            next_moves = current_board.get_valid_moves()
            for piece_moves in next_moves:
                for move in piece_moves.moves:
                    new_state = None

                    if current_board.state.turn == "white":
                        # Create new state based on which piece is moving
                        if piece_moves.pawn == "wk":
                            new_state = State(
                                "black",
                                move,  # new king position
                                current_board.state.wr,  # rook stays
                                current_board.state.bk  # black king stays
                            )
                        else:  # wr
                            new_state = State(
                                "black",
                                current_board.state.wk,  # king stays
                                move,  # new rook position
                                current_board.state.bk  # black king stays
                            )
                    else:  # black's turn
                        # Validate black king's move - ensure it's not too close to white king
                        if not self._is_valid_kings_distance(current_board.state.wk, move):
                            continue
                            
                        new_state = State(
                            "white",
                            current_board.state.wk,
                            current_board.state.wr,
                            move  # new black king position
                        )

                    new_board = Board(new_state)
                    state_hash = self._hash_state(new_state)

                    # Process the new board state
                    if state_hash not in self.checked_states:
                        self.checked_states.add(state_hash)
                        self.moves_to_reach[state_hash] = current_moves + 1
                        new_moves = moves + [f"{piece_moves.pawn}{move}"]
                        queue.append((new_board, new_moves))
                    elif self.moves_to_reach.get(state_hash, float('inf')) > current_moves + 1:
                        # Found a shorter path
                        self.moves_to_reach[state_hash] = current_moves + 1
                        new_moves = moves + [f"{piece_moves.pawn}{move}"]
                        queue.append((new_board, new_moves))

        print(f"No solution found after exploring {explored_states} states")
        return -1

    def _is_valid_kings_distance(self, white_king_pos, black_king_pos):
        """Ensure kings are not adjacent (including diagonally)"""
        from task1.utils import position_to_indices

        wk_row, wk_col = position_to_indices(white_king_pos)
        bk_row, bk_col = position_to_indices(black_king_pos)

        # Kings cannot be adjacent horizontally, vertically, or diagonally
        row_diff = abs(wk_row - bk_row)
        col_diff = abs(wk_col - bk_col)

        # If both differences are <= 1, kings are adjacent
        return not (row_diff <= 1 and col_diff <= 1)

    @staticmethod
    def _hash_state(state: State) -> tuple:
        # Using tuples for more efficient hashing
        return (state.turn, state.wk, state.wr, state.bk)
