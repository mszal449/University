import random
from tabnanny import check
from typing import List

import random
import time

def read_input(filename: str):
    with open(filename, 'r') as file:

        x, y = file.readline().strip().split(" ")
        rows = [0] * int(x)
        cols = [0] * int(y)

        for i in range(int(x)):
            rows[i] = int(file.readline().strip())

        for i in range(int(y)):
            cols[i] = int(file.readline().strip())

    return x, y, rows, cols




class NonogramSolver:
    def __init__(self, row_specs, col_specs, x_size, y_size):
        """
        Initialize the nonogram solver
        :param row_specs: List of row specifications
        :param col_specs: List of column specifications
        :param x_size: Width of the image
        :param y_size: Height of the image
        """
        self.x_size = x_size
        self.y_size = y_size
        self.row_specs = row_specs
        self.col_specs = col_specs
        self.best_score = float('-inf')
        self.best_grid = None
        self.reset_grid()

    def reset_grid(self, all_zeros=False):
        self.grid = [[0 for _ in range(self.x_size)] for _ in range(self.y_size)]
        if all_zeros:
            # All zero initalization
            return
        else:
            # Smart initialization:
            # For each row try tu place blocks according to specs with random position
            for r in range(self.y_size):
                # 50% chance for smart initialization for each row
                if random.random() < 0.5:
                    block = self.row_specs[r]
                    if block:
                        # Read blocks length (one per row)
                        blocks_len = block[0]

                        # Calculate free space
                        free_space = self.x_size - blocks_len

                        # Choose random position
                        start = random.randint(0, free_space)

                        for i in range(blocks_len):
                            self.grid[r][start] = 1
                            start += 1


        self.current_score = self.calculate_total_score()

    def check_line_score(self, line, spec):
        line_blocks = self._get_blocks(line)

        # Perfect match
        if line_blocks == spec:
            return 100

        # Empty spec should have empty line
        if not spec:
            return 100 - (sum(line) * 10)  # Penalty for non-empty cells

        # Empty line but should have a block
        if not line_blocks:
            return -spec[0] * 5  # Penalty based on missing block size

        # Since we expect only one block per line
        expected_size = spec[0] if spec else 0

        # Too many blocks - major penalty
        if len(line_blocks) > 1:
            return -20 * len(line_blocks)

        # We have exactly one block but wrong size
        actual_size = line_blocks[0]
        size_diff = abs(actual_size - expected_size)

        if size_diff == 0:
            return 80  # Almost perfect (missing points for exact position)
        else:
            return 50 - (size_diff * 10)  # Penalize based on size difference

    def _get_blocks(self, line):
        """Convert line into a list of block lengths"""
        blocks = []
        current_length = 0
        for i in line:
            if i == 1:
                current_length += 1
            else:
                if current_length > 0:
                    blocks.append(current_length)
                    current_length = 0

        if current_length > 0:
            blocks.append(current_length)

        return blocks


    def calculate_row_score(self, row_index):
        row = self.grid[row_index]
        return self.check_line_score(row, self.row_specs[row_index])


    def calculate_col_score(self, col_index):
        col = [self.grid[row][col_index] for row in range(self.y_size)]
        return self.check_line_score(col, self.col_specs[col_index])


    def calculate_total_score(self):
        """Calculate total score for current grid"""

        row_scores = sum(self.calculate_row_score(r) for r in range(self.y_size))
        col_scores = sum(self.calculate_col_score(c) for c in range(self.x_size))

        return row_scores + col_scores

    def is_solved(self):
        """Check if the puzzle is solved"""

        for r in range(self.y_size):
            if not self.check_line_validity(self.grid[r], self.row_specs[r]):
                return False

        for c in range(self.x_size):
            column = [self.grid[r][c] for r in range(self.y_size)]
            if not self.check_line_validity(column, self.col_specs[c]):
                return False

        return True

    def check_line_validity(self, line, spec):
        """Check if a line meets its specification"""

        return self._get_blocks(line) == spec

    def calculate_cell_flip_score_change(self, row_index, col_index):
        """Calculate score change by flipping a specific cell"""

        # Calculate current scores
        old_row_score = self.calculate_row_score(row_index)
        old_col_score = self.calculate_col_score(col_index)

        # Flip the cell
        self.grid[row_index][col_index] = 1 - self.grid[row_index][col_index]

        # Calculate new scores
        new_row_score = self.calculate_row_score(row_index)
        new_col_score = self.calculate_col_score(col_index)

        # Flip back
        self.grid[row_index][col_index] = 1 - self.grid[row_index][col_index]

        # Return score change
        return (new_row_score + new_col_score) - (old_row_score + old_col_score)

    def get_invalid_lines(self):
        """Get list of invalid rows and columns"""

        invalid_rows = []
        for r in range(self.y_size):
            if not self.check_line_validity(self.grid[r], self.row_specs[r]):
                invalid_rows.append(r)

        invalid_cols = []
        for c in range(self.x_size):
            column = [self.grid[r][c] for r in range(self.y_size)]
            if not self.check_line_validity(column, self.col_specs[c]):
                invalid_cols.append(c)

        return invalid_rows, invalid_cols

    def solve(self, max_iterations=200000, timeout=10, noise_prob=0.1, restart_after=1000):
        """Solve the nonogram using modified WalkSat-like algorithm"""
        start_time = time.time()
        best_score = float('-inf')
        iterations_since_improvement = 0

        iteration = 0
        while iteration < max_iterations and time.time() - start_time < timeout:
            iteration += 1

            # Check if solved
            if self.is_solved():
                return True

            # Track iterations without improvement
            if self.current_score > best_score:
                best_score = self.current_score
                self.best_grid = [row[:] for row in self.grid]
                iterations_since_improvement = 0
            else:
                iterations_since_improvement += 1

            # Restart if stuck
            if iterations_since_improvement > restart_after:
                self.reset_grid()
                iterations_since_improvement = 0
                continue

            # Get invalid lines
            invalid_rows, invalid_cols = self.get_invalid_lines()

            # Choose row or column to modify
            if invalid_rows and (not invalid_cols or random.random() < 0.5):
                row_index = random.choice(invalid_rows)
                # Find best cell to flip in this row
                best_cell = None
                best_improvement = float('-inf')

                for col in range(self.x_size):
                    improvement = self.calculate_cell_flip_score_change(row_index, col)
                    if improvement > best_improvement:
                        best_improvement = improvement
                        best_cell = col

                col_index = best_cell
            elif invalid_cols:
                col_index = random.choice(invalid_cols)
                # Find best cell to flip in this column
                best_cell = None
                best_improvement = float('-inf')

                for row in range(self.y_size):
                    improvement = self.calculate_cell_flip_score_change(row, col_index)
                    if improvement > best_improvement:
                        best_improvement = improvement
                        best_cell = row

                row_index = best_cell
            else:
                # No invalid lines, pick random cell
                row_index = random.randint(0, self.y_size - 1)
                col_index = random.randint(0, self.x_size - 1)

            # Sometimes make random move instead of best move
            if random.random() < noise_prob:
                if invalid_rows:
                    row_index = random.choice(invalid_rows)
                else:
                    row_index = random.randint(0, self.y_size - 1)

                if invalid_cols:
                    col_index = random.choice(invalid_cols)
                else:
                    col_index = random.randint(0, self.x_size - 1)

            # Flip the chosen cell
            self.grid[row_index][col_index] = 1 - self.grid[row_index][col_index]

            # Update current score
            self.current_score = self.calculate_total_score()

        # If no solution found, use best grid found
        if self.best_grid and not self.is_solved():
            self.grid = self.best_grid

        return self.is_solved()

    def solve_multiple_attempts(self, max_attempts=5, max_iterations=20000, timeout=10):
        """Make multiple attempts to solve the puzzle"""
        # Try with smart initialization first
        if self.solve(max_iterations, timeout):
            return True

        # Then try with different initializations
        for i in range(max_attempts - 1):
            self.reset_grid(all_zeros=(i == 0))  # Try all zeros for first retry
            if self.solve(max_iterations, timeout):
                return True

        return False

    def save_solution(self, output_file):
        """Save the solution to output file"""
        with open(output_file, 'w') as f:
            for row in self.grid:
                f.write(''.join('#' if cell else '.' for cell in row) + '\n')


def parse_input(input_file):
    """Parse input file"""
    with open(input_file, 'r') as f:
        # Read image size
        line = f.readline().strip()
        parts = line.split()
        x_size, y_size = int(parts[0]), int(parts[1])

        # Read row specifications
        row_specs = []
        for _ in range(x_size):
            specs = [int(x) for x in f.readline().strip().split()]
            row_specs.append(specs)

        # Read column specifications
        col_specs = []
        for _ in range(y_size):
            specs = [int(x) for x in f.readline().strip().split()]
            col_specs.append(specs)

    return x_size, y_size, row_specs, col_specs


def main():
    # Input and output file paths
    input_file = 'zad5_input.txt'
    output_file = 'zad5_output.txt'

    try:
        # Parse input
        x_size, y_size, row_specs, col_specs = parse_input(input_file)

        # Create solver
        solver = NonogramSolver(row_specs, col_specs, x_size, y_size)

        # Try to solve
        start_time = time.time()
        solved = solver.solve_multiple_attempts(max_attempts=5)
        end_time = time.time()

        # Save solution
        solver.save_solution(output_file)

        if solved:
            print(f"Solution found in {end_time - start_time:.2f} seconds")
        else:
            print(f"Best approximation saved (not fully solved) in {end_time - start_time:.2f} seconds")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()