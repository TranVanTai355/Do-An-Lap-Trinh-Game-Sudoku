# server/sudoku_generator.py
import random
import copy
from .sudoku_solver import is_valid_move, solve

def generate_full_board():
    """Sinh 1 board đầy đủ (đáp án)."""
    board = [[0] * 9 for _ in range(9)]
    nums = list(range(1, 10))

    def fill():
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    random.shuffle(nums)
                    for v in nums:
                        if is_valid_move(board, r, c, v):
                            board[r][c] = v
                            if fill():
                                return True
                            board[r][c] = 0
                    return False
        return True

    fill()
    return board

def dig_holes(full_board, clues):
    """Tạo puzzle bằng cách xóa ngẫu nhiên để còn 'clues' ô giữ lại."""
    puzzle = copy.deepcopy(full_board)
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    to_remove = 81 - clues
    for r, c in cells:
        if to_remove <= 0:
            break
        if puzzle[r][c] != 0:
            saved = puzzle[r][c]
            puzzle[r][c] = 0
            # (Đơn giản) bỏ qua kiểm tra uniqueness để dễ chạy/nhanh
            to_remove -= 1
    return puzzle

def generate_puzzle(difficulty):
    """difficulty: 'easy' | 'medium' | 'hard'"""
    clues_map = {
        'easy': random.randint(35, 40),
        'medium': random.randint(30, 34),
        'hard': random.randint(25, 29),
    }
    clues = clues_map.get(difficulty, 35)
    full = generate_full_board()
    puzzle = dig_holes(full, clues)
    return puzzle, full
