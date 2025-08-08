# sudoku_check.py
def check_move(board, row, col, num):
    # Kiểm tra ô đang nhập có hợp lệ không theo luật Sudoku
    # board là bảng hiện tại
    # num là số muốn nhập
    # row, col là vị trí ô

    # Nếu ô cố định (không phải 0 ban đầu), không cho phép sửa
    if board[row][col] != 0:
        return False

    # Kiểm tra hàng, cột, vùng 3x3
    for i in range(9):
        if board[row][i] == num:
            return False
    for i in range(9):
        if board[i][col] == num:
            return False
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False
    return True
