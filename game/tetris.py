import random
from config import SHAPES, COLORS, BOARD_WIDTH, BOARD_HEIGHT

class TetrisGame:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.next_piece()
    
    def next_piece(self):
        shape_idx = random.randint(0, len(SHAPES) - 1)
        self.current_piece = SHAPES[shape_idx]
        self.piece_color = COLORS[shape_idx]
        self.piece_x = BOARD_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0
        
        if self.check_collision(self.piece_x, self.piece_y, self.current_piece):
            self.game_over = True
    
    def check_collision(self, x, y, piece):
        for i, row in enumerate(piece):
            for j, cell in enumerate(row):
                if cell:
                    if (x + j < 0 or x + j >= BOARD_WIDTH or 
                        y + i >= BOARD_HEIGHT or 
                        (y + i >= 0 and self.board[y + i][x + j])):
                        return True
        return False
    
    def move(self, dx, dy):
        if self.game_over:
            return False
            
        new_x = self.piece_x + dx
        new_y = self.piece_y + dy
        
        if not self.check_collision(new_x, new_y, self.current_piece):
            self.piece_x = new_x
            self.piece_y = new_y
            return True
        return False
    
    def rotate(self):
        if self.game_over:
            return False
            
        rotated = list(zip(*self.current_piece[::-1]))
        rotated = [list(row) for row in rotated]
        
        if not self.check_collision(self.piece_x, self.piece_y, rotated):
            self.current_piece = rotated
            return True
        
        # Попробуем сдвинуть при коллизии
        for dx in [-1, 1, -2, 2]:
            if not self.check_collision(self.piece_x + dx, self.piece_y, rotated):
                self.piece_x += dx
                self.current_piece = rotated
                return True
        return False
    
    def drop(self):
        if self.game_over:
            return False
            
        score_earned = 0
        while self.move(0, 1):
            score_earned += 1
        
        self.score += score_earned  # Бонус за быстрое падение
        self.lock_piece()
        return True
    
    def lock_piece(self):
        for i, row in enumerate(self.current_piece):
            for j, cell in enumerate(row):
                if cell and 0 <= self.piece_y + i < BOARD_HEIGHT:
                    self.board[self.piece_y + i][self.piece_x + j] = self.piece_color
        
        self.clear_lines()
        self.next_piece()
    
    def clear_lines(self):
        lines_to_clear = []
        for i in range(BOARD_HEIGHT):
            if all(self.board[i]):
                lines_to_clear.append(i)
        
        # Удаляем заполненные линии
        for line in sorted(lines_to_clear, reverse=True):
            del self.board[line]
        
        # Добавляем новые пустые линии сверху
        for _ in lines_to_clear:
            self.board.insert(0, [0 for _ in range(BOARD_WIDTH)])
        
        # Начисляем очки
        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            line_scores = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += line_scores.get(len(lines_to_clear), 800)
            self.level = self.lines_cleared // 10 + 1
    
    def get_game_state(self):
        """Возвращает состояние игры для отображения"""
        return {
            'score': self.score,
            'level': self.level,
            'lines_cleared': self.lines_cleared,
            'game_over': self.game_over,
            'next_piece_shape': len(self.current_piece) if hasattr(self, 'current_piece') else 0
        }