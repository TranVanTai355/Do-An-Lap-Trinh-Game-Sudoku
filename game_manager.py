# server/game_manager.py
import time
import copy
from .sudoku_solver import is_valid_move, equals, is_complete
from .sudoku_generator import generate_puzzle

class GameManager:
    def __init__(self, difficulty='easy'):
        self.new_game(difficulty)

    def new_game(self, difficulty='easy'):
        self.difficulty = difficulty
        self.board, self.solution = generate_puzzle(difficulty)
        self.initial = copy.deepcopy(self.board)
        self.hints_used = 0
        self.max_hints = 3
        self.mistakes = 0
        self.max_mistakes = 3
        self.start_time = time.time()
        self.finished = False
        return self.serialize()

    def time_elapsed(self):
        return int(time.time() - self.start_time)

    def is_fixed(self, r, c):
        return self.initial[r][c] != 0

    def apply_move(self, r, c, v):
        """v: 0 để xóa, 1..9 để nhập.
           Trả về dict: {ok, reason, mistakes, board, correct}"""
        if self.finished:
            return {'ok': False, 'reason': 'finished'}
        if not (0 <= r < 9 and 0 <= c < 9):
            return {'ok': False, 'reason': 'out_of_bounds'}
        if self.is_fixed(r, c):
            return {'ok': False, 'reason': 'fixed_cell'}
        try:
            v = int(v)
        except:
            return {'ok': False, 'reason': 'invalid_value'}
        if not (0 <= v <= 9):
            return {'ok': False, 'reason': 'invalid_value'}

        if v == 0:
            self.board[r][c] = 0
            return {'ok': True, 'reason': 'cleared', 'mistakes': self.mistakes, 'board': self.board, 'correct': None}

        # Kiểm tra hợp lệ theo luật Sudoku hiện tại
        tmp = copy.deepcopy(self.board)
        tmp[r][c] = v
        if not is_valid_move(tmp, r, c, v):
            self.mistakes += 1
            return {'ok': False, 'reason': 'invalid_move', 'mistakes': self.mistakes, 'board': self.board, 'correct': False}

        # Kiểm tra đúng theo đáp án
        if self.solution[r][c] == v:
            self.board[r][c] = v
            return {'ok': True, 'reason': 'correct', 'mistakes': self.mistakes, 'board': self.board, 'correct': True}
        else:
            self.mistakes += 1
            return {'ok': False, 'reason': 'wrong_value', 'mistakes': self.mistakes, 'board': self.board, 'correct': False}

    def hint(self):
        if self.hints_used >= self.max_hints:
            return {'ok': False, 'reason': 'no_hints_left'}
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    self.board[r][c] = self.solution[r][c]
                    self.hints_used += 1
                    return {'ok': True, 'r': r, 'c': c, 'v': self.board[r][c], 'hints_left': self.max_hints - self.hints_used}
        return {'ok': False, 'reason': 'board_full'}

    def reset(self):
        self.board = copy.deepcopy(self.initial)
        self.hints_used = 0
        self.mistakes = 0
        self.finished = False
        self.start_time = time.time()
        return self.serialize()

    def finish(self):
        if equals(self.board, self.solution):
            self.finished = True
            score = max(0, 1000 - self.time_elapsed()*2 - self.hints_used*50 - (0 if self.difficulty=='easy' else (50 if self.difficulty=='medium' else 100)))
            return {'ok': True, 'win': True, 'time': self.time_elapsed(), 'score': score}
        else:
            return {'ok': True, 'win': False}

    def lose_if_exceeded(self):
        if self.mistakes >= self.max_mistakes:
            self.finished = True
            return True
        return False

    def serialize(self):
        return {
            'board': self.board,
            'initial': self.initial,
            'hints_used': self.hints_used,
            'mistakes': self.mistakes,
            'max_mistakes': self.max_mistakes,
            'difficulty': self.difficulty,
            'time': self.time_elapsed(),
            'finished': self.finished
        }
