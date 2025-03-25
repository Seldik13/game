"""
константы для работы модулей
"""

# Константы для размеров экрана и инвентаря
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
CELL_SIZE = 80
PADDING = 10
ROWS = 4
COLS = 5
ROWS_1, COLS_1 = 1, 3

# Смещения для инвентаря
OFFSET_X1 = (SCREEN_WIDTH // 2 - (COLS * (CELL_SIZE + PADDING))) // 2
OFFSET_X2 = (
    SCREEN_WIDTH // 2
    + (SCREEN_WIDTH // 2 - (COLS * (CELL_SIZE + PADDING))) // 2
)
OFFSET_Y = (SCREEN_HEIGHT - (ROWS * (CELL_SIZE + PADDING))) // 2

# константы для функций кнопок
BUTTON_WIDTH = 600
BUTTON_HEIGHT = 360
PADDING_X = 100
PADDING_Y = 100
OFFSET_X = (SCREEN_WIDTH - (2 * BUTTON_WIDTH + PADDING_X)) // 2

# переменные для анимации персонажей
FRAME_TIME = 0  # Время для переключения кадров
FRAME_DELAY = 100  # Задержка между кадрами (в миллисекундах)

# Переменные для второго игрока
CURRENT_CHARACTER_INDEX_PLAYER1 = 0  # Индекс текущего персонажа для Player 1
CURRENT_CHARACTER_INDEX_PLAYER2 = 0  # Индекс текущего персонажа для Player 2

# Переменные для первого игрока
CURRENT_CHARACTER_PLAYER1 = "Archer"  # Текущий персонаж для Player 1
CURRENT_ANIMATION_PLAYER1 = "idle"  # Текущая анимация для Player 1
CURRENT_FRAME_PLAYER1 = 0  # Текущий кадр анимации для Player 1

# Переменные для второго игрока
CURRENT_CHARACTER_PLAYER2 = "Archer"  # Текущий персонаж для Player 2
CURRENT_ANIMATION_PLAYER2 = "idle"  # Текущая анимация для Player 2
CURRENT_FRAME_PLAYER2 = 0  # Текущий кадр анимации для Player 2
