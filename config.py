import os

# Загружаем .env файл для локальной разработки
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ .env файл загружен для локальной разработки")
except ImportError:
    print("ℹ️  python-dotenv не установлен, используем системные environment variables")

# === СЕКРЕТЫ ИЗ ENVIRONMENT VARIABLES ===
BOT_TOKEN = os.getenv('BOT_TOKEN')

# === НАСТРОЙКИ ИГРЫ (статичные) ===
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_SIZE = 25
BORDER = 5

# ... остальные настройки

# Настройки базы данных
RECORDS_FILE = "tetris_records.json"

# Фигуры Тетриса
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

COLORS = [
    (0, 255, 255),    # Cyan
    (255, 255, 0),    # Yellow
    (128, 0, 128),    # Purple
    (255, 165, 0),    # Orange
    (0, 0, 255),      # Blue
    (0, 255, 0),      # Green
    (255, 0, 0)       # Red
]