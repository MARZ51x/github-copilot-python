from typing import List, Tuple

SIZE = 9
EMPTY = 0


def find_conflicts(board: List[List[int]]) -> List[Tuple[int, int]]:
    conflicts = set()
    # Rows
    for r in range(SIZE):
        seen = {}
        for c in range(SIZE):
            v = board[r][c]
            if v == EMPTY:
                continue
            if v in seen:
                conflicts.add((r, c))
                conflicts.add((r, seen[v]))
            else:
                seen[v] = c
    # Columns
    for c in range(SIZE):
        seen = {}
        for r in range(SIZE):
            v = board[r][c]
            if v == EMPTY:
                continue
            if v in seen:
                conflicts.add((r, c))
                conflicts.add((seen[v], c))
            else:
                seen[v] = r
    # Boxes
    for br in range(0, SIZE, 3):
        for bc in range(0, SIZE, 3):
            seen = {}
            for r in range(br, br + 3):
                for c in range(bc, bc + 3):
                    v = board[r][c]
                    if v == EMPTY:
                        continue
                    if v in seen:
                        conflicts.add((r, c))
                        conflicts.add(seen[v])
                    else:
                        seen[v] = (r, c)
    return sorted(list(conflicts))
