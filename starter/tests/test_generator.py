import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.generator import generate_puzzle, generate_by_difficulty, DIFFICULTY_RANGES
from services.solver import count_solutions


def test_generate_puzzle_unique_solution():
    puzzle, solution = generate_puzzle(clues=30)
    assert count_solutions(puzzle, limit=2) == 1


def test_generate_by_difficulty_ranges():
    for diff, (lo, hi) in DIFFICULTY_RANGES.items():
        puzzle, _ = generate_by_difficulty(diff)
        filled = sum(1 for r in puzzle for v in r if v != 0)
        assert lo <= filled <= hi
