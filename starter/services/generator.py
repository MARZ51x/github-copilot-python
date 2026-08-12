from copy import deepcopy
import random
from typing import List, Tuple

from services.solver import generate_full_board, count_solutions

SIZE = 9
EMPTY = 0


DIFFICULTY_RANGES = {
    'Easy': (40, 45),
    'Medium': (30, 39),
    'Hard': (22, 29),
}


def remove_cells_ensure_unique(board: List[List[int]], clues: int, max_attempts: int = 5000) -> List[List[int]]:
    # Start with a filled board and remove cells while keeping unique solution
    b = deepcopy(board)
    cells = [(r, c) for r in range(SIZE) for c in range(SIZE)]
    random.shuffle(cells)
    attempts = 0
    while len([1 for r in range(SIZE) for c in range(SIZE) if b[r][c] != EMPTY]) > clues and attempts < max_attempts:
        attempts += 1
        r, c = cells.pop() if cells else (random.randrange(SIZE), random.randrange(SIZE))
        if b[r][c] == EMPTY:
            continue
        backup = b[r][c]
        b[r][c] = EMPTY
        # ensure uniqueness
        sol_count = count_solutions(b, limit=2)
        if sol_count != 1:
            b[r][c] = backup
    return b


def generate_puzzle(clues: int = 35) -> Tuple[List[List[int]], List[List[int]]]:
    full = generate_full_board()
    solution = deepcopy(full)
    puzzle = remove_cells_ensure_unique(full, clues)
    return puzzle, solution


def generate_by_difficulty(difficulty: str = 'Medium') -> Tuple[List[List[int]], List[List[int]]]:
    rng = DIFFICULTY_RANGES.get(difficulty, DIFFICULTY_RANGES['Medium'])
    clues = random.randint(rng[0], rng[1])
    return generate_puzzle(clues)
