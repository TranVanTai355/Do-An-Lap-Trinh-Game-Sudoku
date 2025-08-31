# server/sudoku_solver.py
import copy

def is_valid_move(board, row, col, val):
    """Kiểm tra val (1..9) có hợp lệ theo luật Sudoku trên board hiện tại
       (chỉ kiểm tra tính hợp lệ, KHÔNG so với đáp án)."""
    if val == 0:
        return True
    # hàng
    for c in range(9):
        if c != col and board[row][c] == val:
            return False
    # cột
    for r in range(9):
        if r != row and board[r][col] == val:
            return False
    # box 3x3
    br = (row // 3) * 3
    bc = (col // 3) * 3
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            if (r != row or c != col) and board[r][c] == val:
                return False
    return True

def is_complete(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return False
    return True

def solve(board):
    """Backtracking giải Sudoku, trả True nếu giải được (board bị chỉnh tại chỗ)."""
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                for v in range(1, 10):
                    if is_valid_move(board, r, c, v):
                        board[r][c] = v
                        if solve(board):
                            return True
                        board[r][c] = 0
                return False
    return True

def equals(a, b):
    for r in range(9):
        for c in range(9):
            if a[r][c] != b[r][c]:
                return False
    return True
