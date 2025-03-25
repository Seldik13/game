"""
Модуль для работы с кнопками в игре.
Содержит класс Buttons для создания и управления кнопками.
"""

import sys

import pygame

# Константы для размеров экрана и кнопок
from constants import (
    BUTTON_HEIGHT,
    BUTTON_WIDTH,
    CELL_SIZE,
    COLS,
    OFFSET_X,
    OFFSET_X1,
    OFFSET_X2,
    OFFSET_Y,
    PADDING,
    PADDING_X,
    PADDING_Y,
    SCREEN_WIDTH,
)
from helper import resource_path

# Инициализация Pygame
pygame.init()


class Buttons(pygame.sprite.Sprite):
    """
    Класс для создания кнопок.
    Обрабатывает отрисовку, клики и функциональность кнопок.
    """

    def __init__(
        self,
        name,
        source_path,
        x,
        y,
        width=None,
        height=None,
        pressed_source_path=None,
    ):
        """
        Инициализация кнопки.

        :param name: Имя кнопки.
        :param source_path: Путь к изображению кнопки.
        :param x: Координата X кнопки.
        :param y: Координата Y кнопки.
        :param width: Ширина кнопки (опционально).
        :param height: Высота кнопки (опционально).
        :param pressed_source_path: Путь к изображению кнопки
        при нажатии (опционально).
        """
        super().__init__()
        self.x = x
        self.y = y
        self.name = name
        self.source_path = pygame.image.load(resource_path(source_path))
        self.width, self.height = self.source_path.get_size()
        if width is not None and height is not None:
            self.source_path = pygame.transform.scale(
                self.source_path, (int(width), int(height))
            )
            self.width, self.height = self.source_path.get_size()
        self.rect = self.source_path.get_rect()

        # Загрузка изображения для состояния нажатия
        self.pressed_source_path = None
        if pressed_source_path:
            self.pressed_source_path = pygame.image.load(
                resource_path(pressed_source_path)
            )
            if width is not None and height is not None:
                self.pressed_source_path = pygame.transform.scale(
                    self.pressed_source_path, (int(width), int(height))
                )

        self.is_pressed = (
            False  # Инициализация флага для отслеживания состояния нажатия
        )

    def paint(self, screen):
        """Отрисовка кнопки на экране."""
        if self.is_pressed and self.pressed_source_path:
            screen.blit(self.pressed_source_path, (self.x, self.y))
        else:
            screen.blit(self.source_path, (self.x, self.y))

    def draw_outline(self, screen):
        """Отрисовка обводки вокруг кнопки."""
        outline = 5  # Толщина обводки
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                self.x - outline,
                self.y - outline,
                self.width + 2 * outline,
                self.height + 2 * outline,
            ),
            outline,
        )

    def is_clicked(self, mouse_pos):
        """
        Проверка, была ли кнопка нажата.

        :param mouse_pos: Позиция мыши (x, y).
        :return: True, если кнопка была нажата, иначе False.
        """
        mouse_x, mouse_y = mouse_pos
        return (self.x <= mouse_x <= self.x + self.width) and (
            self.y <= mouse_y <= self.y + self.height
        )

    def funct(self, game_state, screen, backgrounds):
        """
        Обработка функциональности кнопки.

        :param game_state: Текущее состояние игры.
        :param screen: Экран для отрисовки.
        :param backgrounds: Список фоновых изображений.
        """
        # Переключаем кнопку в состояние нажатия
        self.is_pressed = True

        # Отрисовываем весь экран заново с состоянием нажатия
        self.draw_screen(game_state, screen, backgrounds)
        pygame.display.flip()  # Обновляем экран

        # Задержка для анимации нажатия (например, 200 миллисекунд)
        pygame.time.delay(200)

        # Возвращаем кнопку в обычное состояние
        self.is_pressed = False

        # Отрисовываем весь экран заново с обычным состоянием
        self.draw_screen(game_state, screen, backgrounds)
        pygame.display.flip()  # Обновляем экран

        # Выполняем действие в зависимости от имени кнопки
        if self.name == "00.jpeg":  # Кнопка "Start"
            game_state["show_inventory"] = True
        elif self.name == "01.jpeg":  # Кнопка "Quit"
            pygame.quit()
            sys.exit()
        elif self.name == "02.jpeg":  # Кнопка "Settings"
            game_state["show_settings"] = True
        elif self.name == "play_button":  # Кнопка "Play"
            game_state["show_inventory"] = False
            game_state["show_battle_field"] = True
            # Сбрасываем персонажей, чтобы создать новых с выбранными характеристиками
            global player1, player2
            player1 = None
            player2 = None
        elif self.name == "castle.png":  # Выбор фона "Castle"
            game_state["main_background"] = pygame.image.load(
                resource_path("assets/Maps/castle.png")
            )
            game_state["show_settings"] = False
        elif self.name == "dead forest.png":  # Выбор фона "Dead Forest"
            game_state["main_background"] = pygame.image.load(
                resource_path("assets/Maps/dead forest.png")
            )
            game_state["show_settings"] = False
        elif self.name == "terrace.png":  # Выбор фона "Terrace"
            game_state["main_background"] = pygame.image.load(
                resource_path("assets/Maps/terrace.png")
            )
            game_state["show_settings"] = False
        elif self.name == "throne room.png":  # Выбор фона "Throne Room"
            game_state["main_background"] = pygame.image.load(
                resource_path("assets/Maps/throne room.png")
            )
            game_state["show_settings"] = False

    def draw_screen(self, game_state, screen, backgrounds):
        """
        Отрисовка всего экрана в зависимости от состояния игры и кнопки.

        :param game_state: Текущее состояние игры.
        :param screen: Экран для отрисовки.
        """
        # Отрисовка фона
        if game_state["show_battle_field"]:
            screen.blit(game_state["main_background"], (0, 0))
        elif game_state["show_inventory"]:
            screen.blit(backgrounds[3], (0, 0))
        elif game_state["show_settings"]:
            screen.blit(backgrounds[3], (0, 0))
        else:
            screen.blit(backgrounds[1], (0, 0))

        # Отрисовка кнопок
        if game_state["show_inventory"]:
            for button in inventory_buttons:
                button.paint(screen)
        elif game_state["show_settings"]:
            for button in settings_buttons:
                button.paint(screen)
        else:
            for button in menu_buttons:
                button.paint(screen)


# Создание кнопок
b_start = Buttons(
    "00.jpeg",
    resource_path("assets/buttons/00.png"),
    SCREEN_WIDTH // 2 - 125,
    500,
    pressed_source_path="assets/buttons/10.png",
)
b_quit = Buttons(
    "01.jpeg",
    resource_path("assets/buttons/01.png"),
    SCREEN_WIDTH // 2 - 125,
    800,
    pressed_source_path="assets/buttons/11.png",
)
b_settings = Buttons(
    "02.jpeg",
    resource_path("assets/buttons/02.png"),
    SCREEN_WIDTH // 2 - 125,
    650,
    pressed_source_path="assets/buttons/12.png",
)
b_play = Buttons(
    "play_button",
    resource_path("assets/buttons/00.png"),
    (SCREEN_WIDTH - 250) / 2,
    800,
    pressed_source_path="assets/buttons/10.png",
)

# Кнопки фонов с изменённым размером
background_1 = Buttons(
    "castle.png",
    resource_path("assets/Maps/castle.png"),
    OFFSET_X,
    OFFSET_Y,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)
background_2 = Buttons(
    "dead forest.png",
    resource_path("assets/Maps/dead forest.png"),
    OFFSET_X + BUTTON_WIDTH + PADDING_X,
    OFFSET_Y,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)
background_3 = Buttons(
    "terrace.png",
    resource_path("assets/Maps/terrace.png"),
    OFFSET_X,
    OFFSET_Y + BUTTON_HEIGHT + PADDING_Y,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)
background_4 = Buttons(
    "throne room.png",
    resource_path("assets/Maps/throne room.png"),
    OFFSET_X + BUTTON_WIDTH + PADDING_X,
    OFFSET_Y + BUTTON_HEIGHT + PADDING_Y,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)
# Кнопки для переключения персонажей Player 1
b_left_player1 = Buttons(
    "left_button_player1",
    resource_path(
        "assets/buttons2/left.png"
    ),  # Путь к изображению кнопки "влево"
    OFFSET_X1 - 100,  # Позиция слева от персонажа Player 1
    OFFSET_Y - 150,  # Выравнивание по высоте
    width=50,  # Ширина кнопки
    height=50,  # Высота кнопки
)

b_right_player1 = Buttons(
    "right_button_player1",
    resource_path(
        "assets/buttons2/right.png"
    ),  # Путь к изображению кнопки "вправо"
    OFFSET_X1
    + (COLS * (CELL_SIZE + PADDING))
    + 50,  # Позиция справа от персонажа Player 1
    OFFSET_Y - 150,  # Выравнивание по высоте
    width=50,  # Ширина кнопки
    height=50,  # Высота кнопки
)

# Кнопки для переключения персонажей Player 2
b_left_player2 = Buttons(
    "left_button_player2",
    resource_path(
        "assets/buttons2/left.png"
    ),  # Путь к изображению кнопки "влево"
    OFFSET_X2 - 100,  # Позиция слева от персонажа Player 2
    OFFSET_Y - 150,  # Выравнивание по высоте
    width=50,  # Ширина кнопки
    height=50,  # Высота кнопки
)

b_right_player2 = Buttons(
    "right_button_player2",
    resource_path(
        "assets/buttons2/right.png"
    ),  # Путь к изображению кнопки "вправо"
    OFFSET_X2
    + (COLS * (CELL_SIZE + PADDING))
    + 50,  # Позиция справа от персонажа Player 2
    OFFSET_Y - 150,  # Выравнивание по высоте
    width=50,  # Ширина кнопки
    height=50,  # Высота кнопки
)

# Группы кнопок
menu_buttons = pygame.sprite.Group()
menu_buttons.add(b_start, b_quit, b_settings)

inventory_buttons = pygame.sprite.Group()
inventory_buttons.add(b_play)

settings_buttons = pygame.sprite.Group()
settings_buttons.add(background_1, background_2, background_3, background_4)
