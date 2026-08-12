import copy
import random
from typing import List, Optional

SIZE = 9
EMPTY = 0


def find_empty(board: List[List[int]]) -> Optional[tuple]:
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == EMPTY:
                return i, j
    return None


def valid(board: List[List[int]], row: int, col: int, num: int) -> bool:
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def solve(board: List[List[int]]) -> bool:
    pos = find_empty(board)
    if not pos:
        return True
    row, col = pos
    for num in range(1, SIZE + 1):
        if valid(board, row, col, num):
            board[row][col] = num
            if solve(board):
                return True
            board[row][col] = EMPTY
    return False


def count_solutions(board: List[List[int]], limit: int = 2) -> int:
    # Count solutions using backtracking but stop after reaching limit
    b = copy.deepcopy(board)
    count = 0

    def _search():
        nonlocal count
        if count >= limit:
            return
        pos = find_empty(b)
        if not pos:
            count += 1
            return
        r, c = pos
        for n in range(1, SIZE + 1):
            if valid(b, r, c, n):
                b[r][c] = n
                _search()
                b[r][c] = EMPTY
                if count >= limit:
                    return

    _search()
    return count


def generate_full_board() -> List[List[int]]:
    # Generate a full solved board using randomized backtracking
    board = [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]
    nums = list(range(1, SIZE + 1))

    def _fill():
        pos = find_empty(board)
        if not pos:
            return True
        r, c = pos
        random.shuffle(nums)
        for n in nums:
            if valid(board, r, c, n):
                board[r][c] = n
                if _fill():
                    return True
                board[r][c] = EMPTY
        return False

    _fill()
    return board
