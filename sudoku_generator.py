# sudoku_generator.py
import random

def check_valid(board, row, col, num):
    # Kiểm tra hàng
    for i in range(9):
        if board[row][i] == num:
            return False
    # Kiểm tra cột
    for i in range(9):
        if board[i][col] == num:
            return False
    # Kiểm tra vùng 3x3
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if check_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_full_board():
    board = [[0]*9 for _ in range(9)]
    solve_sudoku(board)
    return board

def remove_cells(board, difficulty='easy'):
    # Số ô ẩn theo độ khó
    if difficulty == 'easy':
        remove_count = random.randint(41, 46)  # 35-40 ô có số => 41-46 ô trống
    elif difficulty == 'medium':
        remove_count = random.randint(46, 51)  # 30-34 có số
    else:  # hard
        remove_count = random.randint(51, 56)  # 25-29 có số

    positions = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(positions)
    for i in range(remove_count):
        r, c = positions[i]
        board[r][c] = 0
    return board

def generate_puzzle(difficulty='easy'):
    full_board = generate_full_board()
    puzzle_board = [row[:] for row in full_board]
    puzzle_board = remove_cells(puzzle_board, difficulty)
    return puzzle_board, full_board
