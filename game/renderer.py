from PIL import Image, ImageDraw
from config import BOARD_WIDTH, BOARD_HEIGHT, CELL_SIZE, BORDER

class GameRenderer:
    def __init__(self):
        self.img_width = BOARD_WIDTH * CELL_SIZE + BORDER * 2
        self.img_height = BOARD_HEIGHT * CELL_SIZE + BORDER * 2
    
    def create_game_image(self, game):
        """Создает изображение игрового поля"""
        img = Image.new('RGB', (self.img_width, self.img_height), color=(40, 40, 40))
        draw = ImageDraw.Draw(img)
        
        # Рисуем границу
        draw.rectangle([0, 0, self.img_width, self.img_height], outline=(100, 100, 100), width=2)
        
        # Рисуем установленные блоки
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if game.board[y][x]:
                    color = game.board[y][x]
                    self._draw_block(draw, x, y, color)
        
        # Рисуем текущую фигуру
        if not game.game_over:
            for y, row in enumerate(game.current_piece):
                for x, cell in enumerate(row):
                    if cell:
                        self._draw_block(draw, game.piece_x + x, game.piece_y + y, game.piece_color, is_current=True)
        
        return img
    
    def _draw_block(self, draw, x, y, color, is_current=False):
        """Рисует отдельный блок"""
        x1 = BORDER + x * CELL_SIZE
        y1 = BORDER + y * CELL_SIZE
        x2 = BORDER + (x + 1) * CELL_SIZE
        y2 = BORDER + (y + 1) * CELL_SIZE
        
        draw.rectangle([x1, y1, x2, y2], fill=color, outline=(200, 200, 200), width=1)
        
        if is_current:
            # Добавляем свечение для текущей фигуры
            draw.rectangle([x1+2, y1+2, x2-2, y2-2], outline=(255, 255, 255), width=2)