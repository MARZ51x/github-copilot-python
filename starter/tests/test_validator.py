import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.validator import find_conflicts


def test_validator_detects_row_conflict():
    b = [[0]*9 for _ in range(9)]
    b[0][0] = 5
    b[0][3] = 5
    conflicts = find_conflicts(b)
    assert (0,0) in conflicts and (0,3) in conflicts


def test_validator_detects_box_conflict():
    b = [[0]*9 for _ in range(9)]
    b[1][1] = 7
    b[2][2] = 7
    conflicts = find_conflicts(b)
    assert (1,1) in conflicts and (2,2) in conflicts
