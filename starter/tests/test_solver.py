import copy
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.solver import generate_full_board, solve, count_solutions


def test_generate_full_board_is_solvable():
    board = generate_full_board()
    b = copy.deepcopy(board)
    assert solve(b) is True


def test_count_solutions_stops_at_limit():
    # empty board has many solutions; ensure count_solutions stops at limit
    empty = [[0]*9 for _ in range(9)]
    assert count_solutions(empty, limit=2) == 2
