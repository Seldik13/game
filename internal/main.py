"""
Основной модуль игры.
Обрабатывает игровую логику, отрисовку и взаимодействие с пользователем.
"""

import json
import os
import random

import pygame
from buttons import (
    b_left_player1,
    b_left_player2,
    b_play,
    b_right_player1,
    b_right_player2,
    inventory_buttons,
    menu_buttons,
    settings_buttons,
)
from charecters import Player, player1_animations, player2_animations, x
from constants import (
    CELL_SIZE,
    COLS,
    COLS_1,
    CURRENT_ANIMATION_PLAYER1,
    CURRENT_ANIMATION_PLAYER2,
    CURRENT_CHARACTER_PLAYER1,
    CURRENT_CHARACTER_PLAYER2,
    CURRENT_FRAME_PLAYER1,
    CURRENT_FRAME_PLAYER2,
    FRAME_DELAY,
    FRAME_TIME,
    OFFSET_X1,
    OFFSET_X2,
    OFFSET_Y,
    PADDING,
    ROWS,
    ROWS_1,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from helper import resource_path

# Инициализация Pygame
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("candara", 46)

# Настройки экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Инициализация игроков
player1 = None
player2 = None

# Загрузка фоновых изображений
backgrounds = [
    pygame.image.load(resource_path("assets/Maps/castle.png")),
    pygame.image.load(resource_path("assets/Maps/dead forest.png")),
    pygame.image.load(resource_path("assets/Maps/terrace.png")),
    pygame.image.load(resource_path("assets/Maps/throne room.png")),
]

clock = pygame.time.Clock()
RUNNING = True
game_state = {
    "show_inventory": False,
    "show_battle_field": False,
    "mouse_pos": (0, 0),
    "show_settings": False,
    "main_background": backgrounds[1],
}

# Добавляем переменную для отслеживания времени восстановления
REGEN_TIME = pygame.time.get_ticks()


def draw_settings(screen_surface):
    """Отрисовка экрана настроек."""
    label = font.render("Choose battle background", True, (255, 168, 91))
    screen_surface.blit(backgrounds[3], (0, 0))
    screen_surface.blit(label, (SCREEN_WIDTH // 2 - 250, 75))
    for btn in settings_buttons:
        btn.paint(screen_surface)
        btn.draw_outline(screen_surface)


inventory_path = resource_path("inventory.json")

# Если файл не существует, создаём его
if not os.path.exists(inventory_path):
    default_inventory = {
        "player1": {},  # Пустой инвентарь для player1
        "player2": {},  # Пустой инвентарь для player2
        "extra_cells": {  # Добавляем структуру для extra_cells
            "player1": {},  # Пустые дополнительные ячейки для player1
            "player2": {},  # Пустые дополнительные ячейки для player2
        },
    }
    with open(inventory_path, "w", encoding="utf-8") as file:
        json.dump(default_inventory, file, indent=4)


def load_inventory(file_path):
    """Загрузка данных из JSON-файла."""
    with open(file_path, "r", encoding="utf-8") as inventory_file:
        return json.load(inventory_file)


inventory_data = load_inventory(inventory_path)

inventory_player1 = {
    (int(k.split(",")[0]), int(k.split(",")[1])): pygame.image.load(
        resource_path(v)
    )
    for k, v in inventory_data["player1"].items()
}
inventory_player2 = {
    (int(k.split(",")[0]), int(k.split(",")[1])): pygame.image.load(
        resource_path(v)
    )
    for k, v in inventory_data["player2"].items()
}

extra_cells_player1 = {
    (int(k.split(",")[0]), int(k.split(",")[1])): pygame.image.load(
        resource_path(v)
    )
    for k, v in inventory_data["extra_cells"]["player1"].items()
}
extra_cells_player2 = {
    (int(k.split(",")[0]), int(k.split(",")[1])): pygame.image.load(
        resource_path(v)
    )
    for k, v in inventory_data["extra_cells"]["player2"].items()
}


def draw_text(surface, text, size, x, y, color=(255, 255, 255)):
    """Отрисовка текста на экране."""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    # Центрируем текст по горизонтали и устанавливаем верхнюю точку
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_stats_bar(
    surface,
    x,
    y,
    width,
    height,
    current,
    max_value,
    color,
    label,
    player_name,
    is_first_bar=False,
):
    """Отрисовка полоски статистики (HP или защита)."""
    # Рисуем фон полоски
    pygame.draw.rect(surface, (50, 50, 50), (x, y, width, height))

    # Рисуем полоску
    bar_width = int((current / max_value) * width)
    pygame.draw.rect(surface, color, (x, y, bar_width, height))

    # Рисуем рамку
    pygame.draw.rect(surface, (255, 255, 255), (x, y, width, height), 1)

    # Создаем текст с значением
    font = pygame.font.Font(None, 20)
    value_text = f"{current}/{max_value}"
    text_surface = font.render(value_text, True, (0, 0, 0))

    # Вычисляем позицию для текста (по центру полоски)
    text_x = x + (width - text_surface.get_width()) // 2
    text_y = y + (height - text_surface.get_height()) // 2

    # Рисуем текст
    surface.blit(text_surface, (text_x, text_y))

    # Рисуем название полоски в левом углу
    label_font = pygame.font.Font(None, 16)
    label_surface = label_font.render(label, True, (0, 0, 0))
    surface.blit(label_surface, (x + 5, y + 2))

    # Рисуем имя игрока только над первым хотбаром
    if is_first_bar:
        player_font = pygame.font.Font(None, 20)
        player_surface = player_font.render(player_name, True, (255, 255, 255))
        surface.blit(player_surface, (x, y - 20))


def draw_battle_field(screen_surface):
    """Отрисовка поля сражения."""
    global player1, player2
    screen_surface.blit(game_state["main_background"], (0, 0))

    screen_surface.blit(game_state["main_background"], (0, 0))

    # Если персонажи еще не созданы, создаем их
    if player1 is None or player2 is None:
        # Создаем персонажей с базовыми характеристиками
        player1 = Player(
            CURRENT_CHARACTER_PLAYER1,  # character
            200,  # st_x
            SCREEN_HEIGHT - 600,  # st_y
            100,  # hp
            50,  # defend
            10,  # speed_run
            15,  # jump_height
            5,  # speed_walk
            x[CURRENT_CHARACTER_PLAYER1],  # animations
        )

        player2 = Player(
            CURRENT_CHARACTER_PLAYER2,  # character
            SCREEN_WIDTH - 300,  # st_x
            SCREEN_HEIGHT - 600,  # st_y
            100,  # hp
            50,  # defend
            10,  # speed_run
            15,  # jump_height
            5,  # speed_walk
            x[CURRENT_CHARACTER_PLAYER2],  # animations
        )

        # Инициализация кадров анимации
        global \
            CURRENT_FRAME_PLAYER1, \
            CURRENT_FRAME_PLAYER2, \
            CURRENT_ANIMATION_PLAYER1, \
            CURRENT_ANIMATION_PLAYER2
        CURRENT_FRAME_PLAYER1 = 0
        CURRENT_FRAME_PLAYER2 = 0
        CURRENT_ANIMATION_PLAYER1 = "idle"
        CURRENT_ANIMATION_PLAYER2 = "idle"

    # Ограничиваем движение персонажей
    if player1 is not None:
        # Ограничение по X для player1 (только левая граница экрана)
        player1.st_x = max(50, min(player1.st_x, SCREEN_WIDTH - 100))
        # Ограничение по Y для player1
        player1.st_y = max(50, min(player1.st_y, SCREEN_HEIGHT - 100))
        player1.ground_y = (
            SCREEN_HEIGHT - 600
        )  # Обновляем позицию земли для player1

    if player2 is not None:
        # Ограничение по X для player2 (только правая граница экрана)
        player2.st_x = max(50, min(player2.st_x, SCREEN_WIDTH - 100))
        # Ограничение по Y для player2
        player2.st_y = max(50, min(player2.st_y, SCREEN_HEIGHT - 100))
        player2.ground_y = (
            SCREEN_HEIGHT - 600
        )  # Обновляем позицию земли для player2

    # Отрисовываем персонажей с масштабированием
    current_animation_p1 = player1.animations[CURRENT_ANIMATION_PLAYER1]
    # Проверяем и корректируем индекс кадра для player1
    if CURRENT_FRAME_PLAYER1 >= len(current_animation_p1):
        CURRENT_FRAME_PLAYER1 = 0
    frame_p1 = current_animation_p1[CURRENT_FRAME_PLAYER1]
    # Масштабируем спрайт player1 (увеличиваем в 2 раза)
    scaled_frame_p1 = pygame.transform.scale(
        frame_p1, (frame_p1.get_width() * 2, frame_p1.get_height() * 2)
    )
    # Отражаем спрайт player1 по горизонтали, если он движется влево
    if player1.direction == -1:
        scaled_frame_p1 = pygame.transform.flip(scaled_frame_p1, True, False)
    screen_surface.blit(
        scaled_frame_p1,
        (
            player1.st_x - frame_p1.get_width() // 2,
            player1.st_y - frame_p1.get_height() // 2,
        ),
    )
    # Отрисовываем подсказку над первым игроком (центрированную)
    draw_text(
        screen_surface,
        "Player 1",
        24,
        player1.st_x + 50,
        player1.st_y,
        (255, 255, 255),
    )

    current_animation_p2 = player2.animations[CURRENT_ANIMATION_PLAYER2]
    # Проверяем и корректируем индекс кадра для player2
    if CURRENT_FRAME_PLAYER2 >= len(current_animation_p2):
        CURRENT_FRAME_PLAYER2 = 0
    frame_p2 = current_animation_p2[CURRENT_FRAME_PLAYER2]
    # Масштабируем спрайт player2 (увеличиваем в 2 раза)
    scaled_frame_p2 = pygame.transform.scale(
        frame_p2, (frame_p2.get_width() * 2, frame_p2.get_height() * 2)
    )
    # Отражаем спрайт player2 по горизонтали, если он движется вправо
    if player2.direction == -1:
        scaled_frame_p2 = pygame.transform.flip(scaled_frame_p2, True, False)
    screen_surface.blit(
        scaled_frame_p2,
        (
            player2.st_x - frame_p2.get_width() // 2,
            player2.st_y - frame_p2.get_height() // 2,
        ),
    )
    # Отрисовываем подсказку над вторым игроком (центрированную)
    draw_text(
        screen_surface,
        "Player 2",
        24,
        player2.st_x + 50,
        player2.st_y,
        (255, 255, 255),
    )

    # Отрисовываем статистику для первого игрока
    draw_stats_bar(
        screen_surface,
        50,
        50,
        200,
        20,
        player1.hp,
        100,
        (255, 0, 0),
        "HP",
        "Player 1",
        True,
    )
    draw_stats_bar(
        screen_surface,
        50,
        80,
        200,
        20,
        player1.defend,
        50,
        (0, 255, 0),
        "Def",
        "Player 1",
    )
    # Отображаем ману для мага или выносливость для остальных
    if CURRENT_CHARACTER_PLAYER1 == "Wizard":
        draw_stats_bar(
            screen_surface,
            50,
            110,
            200,
            20,
            int(player1.mana),
            100,
            (0, 0, 255),
            "Mana",
            "Player 1",
        )
    else:
        draw_stats_bar(
            screen_surface,
            50,
            110,
            200,
            20,
            int(player1.stamina),
            100,
            (255, 165, 0),
            "Stamina",
            "Player 1",
        )

    # Отрисовываем статистику для второго игрока
    draw_stats_bar(
        screen_surface,
        SCREEN_WIDTH - 250,
        50,
        200,
        20,
        player2.hp,
        100,
        (255, 0, 0),
        "HP",
        "Player 2",
        True,
    )
    draw_stats_bar(
        screen_surface,
        SCREEN_WIDTH - 250,
        80,
        200,
        20,
        player2.defend,
        50,
        (0, 255, 0),
        "Def",
        "Player 2",
    )
    # Отображаем ману для мага или выносливость для остальных
    if CURRENT_CHARACTER_PLAYER2 == "Wizard":
        draw_stats_bar(
            screen_surface,
            SCREEN_WIDTH - 250,
            110,
            200,
            20,
            int(player2.mana),
            100,
            (0, 0, 255),
            "Mana",
            "Player 2",
        )
    else:
        draw_stats_bar(
            screen_surface,
            SCREEN_WIDTH - 250,
            110,
            200,
            20,
            int(player2.stamina),
            100,
            (255, 165, 0),
            "Stamina",
            "Player 2",
        )

    return screen_surface


def draw_inventory_grid(screen_surface, offset_x, inventory, label_text):
    """Отрисовка сетки инвентаря для игрока."""
    label = font.render(label_text, True, (255, 255, 255))
    screen_surface.blit(
        label, (offset_x + (CELL_SIZE * 5 + PADDING * 4) / 2.7, OFFSET_Y - 250)
    )

    for row in range(ROWS):
        for col in range(COLS):
            x = offset_x + col * (CELL_SIZE + PADDING)
            y = OFFSET_Y + row * (CELL_SIZE + PADDING)
            pygame.draw.rect(
                screen_surface,
                (192, 192, 192),
                (x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8),
                2,
            )
            pygame.draw.rect(
                screen_surface,
                (64, 64, 64),
                (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4),
                2,
            )
            pygame.draw.rect(
                screen_surface, (0, 0, 0), (x, y, CELL_SIZE, CELL_SIZE), 2
            )

            if (row, col) in inventory:
                screen_surface.blit(
                    pygame.transform.scale(
                        inventory[(row, col)], (CELL_SIZE, CELL_SIZE)
                    ),
                    (x, y),
                )


def draw_inventory(screen_surface):
    """Отрисовка инвентаря."""
    global CURRENT_FRAME_PLAYER1, CURRENT_FRAME_PLAYER2, FRAME_TIME

    screen_surface.blit(backgrounds[3], (0, 0))

    # Обновление кадра анимации для Player 1 и Player 2
    current_time = pygame.time.get_ticks()
    if current_time - FRAME_TIME > FRAME_DELAY:
        FRAME_TIME = current_time
        CURRENT_FRAME_PLAYER1 = (CURRENT_FRAME_PLAYER1 + 1) % len(
            player1_animations[CURRENT_CHARACTER_PLAYER1][
                CURRENT_ANIMATION_PLAYER1
            ]
        )
        CURRENT_FRAME_PLAYER2 = (CURRENT_FRAME_PLAYER2 + 1) % len(
            player2_animations[CURRENT_CHARACTER_PLAYER2][
                CURRENT_ANIMATION_PLAYER2
            ]
        )

    # Отрисовка персонажа Player 1
    current_animation_player1 = player1_animations[CURRENT_CHARACTER_PLAYER1][
        CURRENT_ANIMATION_PLAYER1
    ]
    character_image_player1 = current_animation_player1[CURRENT_FRAME_PLAYER1]
    # Масштабируем спрайт player1 (увеличиваем в 2 раза)
    scaled_character_image_player1 = pygame.transform.scale(
        character_image_player1,
        (
            character_image_player1.get_width() * 2,
            character_image_player1.get_height() * 2,
        ),
    )
    character_rect_player1 = scaled_character_image_player1.get_rect(
        center=(
            OFFSET_X1 + (COLS * (CELL_SIZE + PADDING)) // 2,
            OFFSET_Y - 150,
        )
    )
    screen_surface.blit(scaled_character_image_player1, character_rect_player1)

    # Отрисовка персонажа Player 2
    current_animation_player2 = player2_animations[CURRENT_CHARACTER_PLAYER2][
        CURRENT_ANIMATION_PLAYER2
    ]
    character_image_player2 = current_animation_player2[CURRENT_FRAME_PLAYER2]
    # Масштабируем спрайт player2 (увеличиваем в 2 раза)
    scaled_character_image_player2 = pygame.transform.scale(
        character_image_player2,
        (
            character_image_player2.get_width() * 2,
            character_image_player2.get_height() * 2,
        ),
    )
    # Отражаем спрайт player2 по горизонтали
    scaled_character_image_player2 = pygame.transform.flip(
        scaled_character_image_player2, True, False
    )
    character_rect_player2 = scaled_character_image_player2.get_rect(
        center=(
            OFFSET_X2 + (COLS * (CELL_SIZE + PADDING)) // 2,
            OFFSET_Y - 150,
        )
    )
    screen_surface.blit(scaled_character_image_player2, character_rect_player2)

    # Отрисовка кнопок переключения персонажей
    b_left_player1.paint(screen_surface)
    b_right_player1.paint(screen_surface)
    b_left_player2.paint(screen_surface)
    b_right_player2.paint(screen_surface)

    # Отрисовка инвентаря игроков
    draw_inventory_grid(
        screen_surface,
        OFFSET_X1,
        inventory_player1,
        "Player 1",
    )
    draw_inventory_grid(
        screen_surface,
        OFFSET_X2,
        inventory_player2,
        "Player 2",
    )

    draw_battle_inventory()
    b_play.paint(screen_surface)


def draw_battle_inventory():
    """Отрисовка инвентаря для боя."""
    if game_state["show_battle_field"]:
        battle_inventory_offset_y = (
            OFFSET_Y + ROWS * (CELL_SIZE + PADDING) + 200
        )
    else:
        battle_inventory_offset_y = (
            OFFSET_Y + ROWS * (CELL_SIZE + PADDING) + 50
        )

    # Смещение для центрирования инвентаря для боя
    center_offset = (COLS - COLS_1) * (CELL_SIZE + PADDING) // 2

    # Отрисовка инвентаря для боя игрока 1
    for row in range(ROWS_1):
        for col in range(COLS_1):
            x = OFFSET_X1 + col * (CELL_SIZE + PADDING) + center_offset
            y = battle_inventory_offset_y + row * (CELL_SIZE + PADDING)
            pygame.draw.rect(
                screen,
                (192, 192, 192),
                (x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8),
                2,
            )
            pygame.draw.rect(
                screen,
                (64, 64, 64),
                (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4),
                2,
            )
            pygame.draw.rect(
                screen, (0, 0, 0), (x, y, CELL_SIZE, CELL_SIZE), 2
            )

            if (row, col) in extra_cells_player1:
                screen.blit(
                    pygame.transform.scale(
                        extra_cells_player1[(row, col)], (CELL_SIZE, CELL_SIZE)
                    ),
                    (x, y),
                )

    # Отрисовка инвентаря для боя игрока 2
    for row in range(ROWS_1):
        for col in range(COLS_1):
            x = OFFSET_X2 + col * (CELL_SIZE + PADDING) + center_offset
            y = battle_inventory_offset_y + row * (CELL_SIZE + PADDING)
            pygame.draw.rect(
                screen,
                (192, 192, 192),
                (x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8),
                2,
            )
            pygame.draw.rect(
                screen,
                (64, 64, 64),
                (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4),
                2,
            )
            pygame.draw.rect(
                screen, (0, 0, 0), (x, y, CELL_SIZE, CELL_SIZE), 2
            )

            if (row, col) in extra_cells_player2:
                screen.blit(
                    pygame.transform.scale(
                        extra_cells_player2[(row, col)], (CELL_SIZE, CELL_SIZE)
                    ),
                    (x, y),
                )


# Игровой цикл
while RUNNING:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

        # Обработка клавиш на поле сражения
        if game_state["show_battle_field"] and player1 and player2:
            if event.type == pygame.KEYDOWN:
                # Обработка нажатий клавиш для Player 1
                if event.key == pygame.K_w:
                    player1.jump()
                    CURRENT_ANIMATION_PLAYER1 = "jump"
                elif event.key == pygame.K_c:
                    # Проверяем наличие стамины/маны для атаки
                    if (
                        CURRENT_CHARACTER_PLAYER1 == "Wizard"
                        and player1.mana >= 5
                    ) or (
                        CURRENT_CHARACTER_PLAYER1 != "Wizard"
                        and player1.stamina >= 5
                    ):
                        # Расходуем стамину/ману
                        if CURRENT_CHARACTER_PLAYER1 == "Wizard":
                            player1.mana -= 5
                        else:
                            player1.stamina -= 5
                        # Случайный выбор анимации атаки в зависимости от персонажа
                        if CURRENT_CHARACTER_PLAYER1 == "Archer":
                            CURRENT_ANIMATION_PLAYER1 = random.choice(
                                ["shot_1", "shot_2"]
                            )
                        elif CURRENT_CHARACTER_PLAYER1 == "Enchantress":
                            CURRENT_ANIMATION_PLAYER1 = random.choice(
                                [
                                    "attack_1",
                                    "attack_2",
                                    "attack_3",
                                    "attack_4",
                                ]
                            )
                        elif CURRENT_CHARACTER_PLAYER1 == "Knight":
                            CURRENT_ANIMATION_PLAYER1 = random.choice(
                                [
                                    "attack_1",
                                    "attack_2",
                                    "attack_3",
                                    "attack_4",
                                ]
                            )
                        elif CURRENT_CHARACTER_PLAYER1 == "Musketeer":
                            CURRENT_ANIMATION_PLAYER1 = random.choice(
                                [
                                    "attack_1",
                                    "attack_2",
                                    "attack_3",
                                    "attack_4",
                                ]
                            )
                        elif CURRENT_CHARACTER_PLAYER1 == "Swordsman":
                            CURRENT_ANIMATION_PLAYER1 = random.choice(
                                ["attack_1", "attack_2", "attack_3"]
                            )
                        elif CURRENT_CHARACTER_PLAYER1 == "Wizard":
                            CURRENT_ANIMATION_PLAYER1 = random.choice(
                                ["attack_1", "attack_2", "attack_3"]
                            )
                        CURRENT_FRAME_PLAYER1 = (
                            0  # Сбрасываем кадр при выборе новой анимации
                        )

                # Обработка нажатий клавиш для Player 2
                if event.key == pygame.K_i:
                    player2.jump()
                    CURRENT_ANIMATION_PLAYER2 = "jump"
                elif event.key == pygame.K_n:
                    # Проверяем наличие стамины/маны для атаки
                    if (
                        CURRENT_CHARACTER_PLAYER2 == "Wizard"
                        and player2.mana >= 5
                    ) or (
                        CURRENT_CHARACTER_PLAYER2 != "Wizard"
                        and player2.stamina >= 5
                    ):
                        # Расходуем стамину/ману
                        if CURRENT_CHARACTER_PLAYER2 == "Wizard":
                            player2.mana -= 5
                        else:
                            player2.stamina -= 5
                        # Случайный выбор анимации атаки в зависимости от персонажа
                        if CURRENT_CHARACTER_PLAYER2 == "Archer":
                            CURRENT_ANIMATION_PLAYER2 = random.choice(
                                ["shot_1", "shot_2"]
                            )
                        elif CURRENT_CHARACTER_PLAYER2 == "Enchantress":
                            CURRENT_ANIMATION_PLAYER2 = random.choice(
                                [
                                    "attack_1",
                                    "attack_2",
                                    "attack_3",
                                    "attack_4",
                                ]
                            )
                        elif CURRENT_CHARACTER_PLAYER2 == "Knight":
                            CURRENT_ANIMATION_PLAYER2 = random.choice(
                                [
                                    "attack_1",
                                    "attack_2",
                                    "attack_3",
                                    "attack_4",
                                ]
                            )
                        elif CURRENT_CHARACTER_PLAYER2 == "Musketeer":
                            CURRENT_ANIMATION_PLAYER2 = random.choice(
                                [
                                    "attack_1",
                                    "attack_2",
                                    "attack_3",
                                    "attack_4",
                                ]
                            )
                        elif CURRENT_CHARACTER_PLAYER2 == "Swordsman":
                            CURRENT_ANIMATION_PLAYER2 = random.choice(
                                ["attack_1", "attack_2", "attack_3"]
                            )
                        elif CURRENT_CHARACTER_PLAYER2 == "Wizard":
                            CURRENT_ANIMATION_PLAYER2 = random.choice(
                                ["attack_1", "attack_2", "attack_3"]
                            )
                        CURRENT_FRAME_PLAYER2 = (
                            0  # Сбрасываем кадр при выборе новой анимации
                        )

            if event.type == pygame.KEYUP:
                # Возвращаем анимацию idle при отпускании клавиш
                if event.key in (pygame.K_a, pygame.K_d):
                    CURRENT_ANIMATION_PLAYER1 = "idle"
                if event.key in (pygame.K_j, pygame.K_l):
                    CURRENT_ANIMATION_PLAYER2 = "idle"

        if event.type == pygame.MOUSEBUTTONDOWN:
            game_state["mouse_pos"] = pygame.mouse.get_pos()

            if game_state["show_inventory"]:
                # Обрабатываем кнопки переключения персонажей Player 1
                if b_left_player1.is_clicked(game_state["mouse_pos"]):
                    # Переключение на предыдущего персонажа для Player 1
                    characters = list(player1_animations.keys())
                    current_index = characters.index(CURRENT_CHARACTER_PLAYER1)
                    CURRENT_CHARACTER_PLAYER1 = characters[
                        (current_index - 1) % len(characters)
                    ]
                    CURRENT_ANIMATION_PLAYER1 = "idle"
                    CURRENT_FRAME_PLAYER1 = 0
                elif b_right_player1.is_clicked(game_state["mouse_pos"]):
                    # Переключение на следующего персонажа для Player 1
                    characters = list(player1_animations.keys())
                    current_index = characters.index(CURRENT_CHARACTER_PLAYER1)
                    CURRENT_CHARACTER_PLAYER1 = characters[
                        (current_index + 1) % len(characters)
                    ]
                    CURRENT_ANIMATION_PLAYER1 = "idle"
                    CURRENT_FRAME_PLAYER1 = 0

                # Обрабатываем кнопки переключения персонажей Player 2
                if b_left_player2.is_clicked(game_state["mouse_pos"]):
                    # Переключение на предыдущего персонажа для Player 2
                    characters = list(player2_animations.keys())
                    current_index = characters.index(CURRENT_CHARACTER_PLAYER2)
                    CURRENT_CHARACTER_PLAYER2 = characters[
                        (current_index - 1) % len(characters)
                    ]
                    CURRENT_ANIMATION_PLAYER2 = "idle"
                    CURRENT_FRAME_PLAYER2 = 0
                elif b_right_player2.is_clicked(game_state["mouse_pos"]):
                    # Переключение на следующего персонажа для Player 2
                    characters = list(player2_animations.keys())
                    current_index = characters.index(CURRENT_CHARACTER_PLAYER2)
                    CURRENT_CHARACTER_PLAYER2 = characters[
                        (current_index + 1) % len(characters)
                    ]
                    CURRENT_ANIMATION_PLAYER2 = "idle"
                    CURRENT_FRAME_PLAYER2 = 0

                # Обрабатываем кнопки инвентаря
                for button in inventory_buttons:
                    if button.is_clicked(game_state["mouse_pos"]):
                        button.funct(game_state, screen, backgrounds)

            elif game_state["show_settings"]:
                # Обрабатываем кнопки настроек
                for button in settings_buttons:
                    if button.is_clicked(game_state["mouse_pos"]):
                        button.funct(game_state, screen, backgrounds)

            elif not game_state[
                "show_battle_field"
            ]:  # Добавляем проверку на поле боя
                # Обрабатываем основные кнопки только если не на поле боя
                for button in menu_buttons:
                    if button.is_clicked(game_state["mouse_pos"]):
                        button.funct(game_state, screen, backgrounds)

    # Обновление состояния персонажей
    if game_state["show_battle_field"] and player1 and player2:
        # Обновление кадров анимации с задержкой
        current_time = pygame.time.get_ticks()

        # Автоматическое восполнение маны/стамины
        if current_time - REGEN_TIME > 1000:  # Каждую секунду
            REGEN_TIME = (
                current_time  # Обновляем время последнего восстановления
            )

            # Восполнение для Player 1
            if CURRENT_CHARACTER_PLAYER1 == "Wizard":
                player1.mana = min(
                    100, player1.mana + 1
                )  # Восполняем 1 ману в секунду
            else:
                player1.stamina = min(
                    100, player1.stamina + 2
                )  # Восполняем 2 стамины в секунду

            # Восполнение для Player 2
            if CURRENT_CHARACTER_PLAYER2 == "Wizard":
                player2.mana = min(
                    100, player2.mana + 1
                )  # Восполняем 1 ману в секунду
            else:
                player2.stamina = min(
                    100, player2.stamina + 2
                )  # Восполняем 2 стамины в секунду

        # Определяем задержку в зависимости от анимации
        NEW_FRAME_DELAY = FRAME_DELAY
        # Замедляем idle_2 для Wizard
        if (
            CURRENT_CHARACTER_PLAYER1 == "Wizard"
            and CURRENT_ANIMATION_PLAYER1 == "idle_2"
        ):
            NEW_FRAME_DELAY = (
                FRAME_DELAY * 4
            )  # Увеличиваем задержку в 500 раз для idle_2 анимации Wizard
        elif (
            CURRENT_CHARACTER_PLAYER2 == "Wizard"
            and CURRENT_ANIMATION_PLAYER2 == "idle_2"
        ):
            NEW_FRAME_DELAY = (
                FRAME_DELAY * 4
            )  # Увеличиваем задержку в 500 раз для idle_2 анимации Wizard

        if current_time - FRAME_TIME > NEW_FRAME_DELAY:
            FRAME_TIME = current_time
            # Обновляем кадры анимации
            CURRENT_FRAME_PLAYER1 = (CURRENT_FRAME_PLAYER1 + 1) % len(
                player1.animations[CURRENT_ANIMATION_PLAYER1]
            )
            CURRENT_FRAME_PLAYER2 = (CURRENT_FRAME_PLAYER2 + 1) % len(
                player2.animations[CURRENT_ANIMATION_PLAYER2]
            )

            # Проверяем завершение анимации атаки или прыжка
            if CURRENT_FRAME_PLAYER1 == 0 and CURRENT_ANIMATION_PLAYER1 in [
                "attack_1",
                "attack_2",
                "attack_3",
                "attack_4",
                "shot_1",
                "shot_2",
                "jump",
            ]:
                # Выбор анимации бездействия
                if (
                    CURRENT_ANIMATION_PLAYER1 == "idle_2"
                    and CURRENT_FRAME_PLAYER1
                    == len(player1.animations["idle_2"]) - 1
                ):
                    CURRENT_ANIMATION_PLAYER1 = "idle"
                    CURRENT_FRAME_PLAYER1 = 0
                elif (
                    CURRENT_ANIMATION_PLAYER1 == "idle"
                    and random.random() < 0.004
                ):  # 0.4% шанс выбора idle_2
                    CURRENT_ANIMATION_PLAYER1 = "idle_2"
                    CURRENT_FRAME_PLAYER1 = 0
                else:
                    CURRENT_ANIMATION_PLAYER1 = "idle"
                CURRENT_FRAME_PLAYER1 = 0

            if CURRENT_FRAME_PLAYER2 == 0 and CURRENT_ANIMATION_PLAYER2 in [
                "attack_1",
                "attack_2",
                "attack_3",
                "attack_4",
                "shot_1",
                "shot_2",
                "jump",
            ]:
                # Выбор анимации бездействия
                if (
                    CURRENT_ANIMATION_PLAYER2 == "idle_2"
                    and CURRENT_FRAME_PLAYER2
                    == len(player2.animations["idle_2"]) - 1
                ):
                    CURRENT_ANIMATION_PLAYER2 = "idle"
                    CURRENT_FRAME_PLAYER2 = 0
                elif (
                    CURRENT_ANIMATION_PLAYER2 == "idle"
                    and random.random() < 0.004
                ):  # 0.4% шанс выбора idle_2
                    CURRENT_ANIMATION_PLAYER2 = "idle_2"
                    CURRENT_FRAME_PLAYER2 = 0
                else:
                    CURRENT_ANIMATION_PLAYER2 = "idle"
                CURRENT_FRAME_PLAYER2 = 0

        # Обработка постоянно зажатых клавиш для Player 1
        keys = pygame.key.get_pressed()
        # Проверяем анимацию атаки в первую очередь, но не отменяем движение
        if CURRENT_ANIMATION_PLAYER1 in [
            "attack_1",
            "attack_2",
            "attack_3",
            "attack_4",
            "shot_1",
            "shot_2",
        ]:
            # Сохраняем движение во время атаки только если персонаж не Archer
            if CURRENT_CHARACTER_PLAYER1 != "Archer":
                if keys[pygame.K_a]:
                    player1.st_x -= player1.speed_walk
                    player1.direction = -1
                elif keys[pygame.K_d]:
                    player1.st_x += player1.speed_walk
                    player1.direction = 1
        elif player1.is_jumping:
            CURRENT_ANIMATION_PLAYER1 = "jump"
            # Сохраняем движение во время прыжка
            if keys[pygame.K_a]:
                player1.st_x -= player1.speed_walk
                player1.direction = -1
            elif keys[pygame.K_d]:
                player1.st_x += player1.speed_walk
                player1.direction = 1
        elif keys[pygame.K_a]:
            player1.move(-1)
            CURRENT_ANIMATION_PLAYER1 = "walk"
        elif keys[pygame.K_d]:
            player1.move(1)
            CURRENT_ANIMATION_PLAYER1 = "walk"
        elif (
            CURRENT_ANIMATION_PLAYER1 == "jump"
            and player1.st_y >= player1.ground_y
        ):
            # Если персонаж достиг земли и анимация прыжка все еще активна, возвращаемся к idle
            CURRENT_ANIMATION_PLAYER1 = "idle"
            CURRENT_FRAME_PLAYER1 = 0
        elif CURRENT_ANIMATION_PLAYER1 not in [
            "attack_1",
            "attack_2",
            "attack_3",
            "attack_4",
            "shot_1",
            "shot_2",
            "jump",
        ]:
            # Выбор анимации бездействия в зависимости от персонажа
            if CURRENT_CHARACTER_PLAYER1 == "Archer":
                CURRENT_ANIMATION_PLAYER1 = (
                    "idle"  # У Archer только одна анимация бездействия
                )
            elif CURRENT_CHARACTER_PLAYER1 == "Wizard":
                # Для Wizard idle_2 проигрывается только один раз и очень редко
                if (
                    CURRENT_ANIMATION_PLAYER1 == "idle_2"
                    and CURRENT_FRAME_PLAYER1
                    == len(player1.animations["idle_2"]) - 1
                ):
                    CURRENT_ANIMATION_PLAYER1 = "idle"
                    CURRENT_FRAME_PLAYER1 = 0
                elif (
                    CURRENT_ANIMATION_PLAYER1 == "idle"
                    and random.random() < 0.004
                ):  # 0.4% шанс выбора idle_2
                    CURRENT_ANIMATION_PLAYER1 = "idle_2"
                    CURRENT_FRAME_PLAYER1 = 0
            else:
                # Проверяем наличие idle_2 анимации
                if "idle_2" in player1.animations:
                    CURRENT_ANIMATION_PLAYER1 = random.choice(
                        ["idle", "idle_2"]
                    )
                else:
                    CURRENT_ANIMATION_PLAYER1 = "idle"

        # Обработка постоянно зажатых клавиш для Player 2
        # Проверяем анимацию атаки в первую очередь, но не отменяем движение
        if CURRENT_ANIMATION_PLAYER2 in [
            "attack_1",
            "attack_2",
            "attack_3",
            "attack_4",
            "shot_1",
            "shot_2",
        ]:
            # Сохраняем движение во время атаки только если персонаж не Archer
            if CURRENT_CHARACTER_PLAYER2 != "Archer":
                if keys[pygame.K_j]:
                    player2.st_x -= player2.speed_walk
                    player2.direction = -1
                elif keys[pygame.K_l]:
                    player2.st_x += player2.speed_walk
                    player2.direction = 1
        elif player2.is_jumping:
            CURRENT_ANIMATION_PLAYER2 = "jump"
            # Сохраняем движение во время прыжка
            if keys[pygame.K_j]:
                player2.st_x -= player2.speed_walk
                player2.direction = -1
            elif keys[pygame.K_l]:
                player2.st_x += player2.speed_walk
                player2.direction = 1
        elif keys[pygame.K_j]:
            player2.move(-1)
            CURRENT_ANIMATION_PLAYER2 = "walk"
        elif keys[pygame.K_l]:
            player2.move(1)
            CURRENT_ANIMATION_PLAYER2 = "walk"
        elif (
            CURRENT_ANIMATION_PLAYER2 == "jump"
            and player2.st_y >= player2.ground_y
        ):
            # Если персонаж достиг земли и анимация прыжка все еще активна, возвращаемся к idle
            CURRENT_ANIMATION_PLAYER2 = "idle"
            CURRENT_FRAME_PLAYER2 = 0
        elif CURRENT_ANIMATION_PLAYER2 not in [
            "attack_1",
            "attack_2",
            "attack_3",
            "attack_4",
            "shot_1",
            "shot_2",
            "jump",
        ]:
            # Выбор анимации бездействия в зависимости от персонажа
            if CURRENT_CHARACTER_PLAYER2 == "Archer":
                CURRENT_ANIMATION_PLAYER2 = (
                    "idle"  # У Archer только одна анимация бездействия
                )
            elif CURRENT_CHARACTER_PLAYER2 == "Wizard":
                # Для Wizard idle_2 проигрывается только один раз и очень редко
                if (
                    CURRENT_ANIMATION_PLAYER2 == "idle_2"
                    and CURRENT_FRAME_PLAYER2
                    == len(player2.animations["idle_2"]) - 1
                ):
                    CURRENT_ANIMATION_PLAYER2 = "idle"
                    CURRENT_FRAME_PLAYER2 = 0
                elif (
                    CURRENT_ANIMATION_PLAYER2 == "idle"
                    and random.random() < 0.004
                ):  # 0.4% шанс выбора idle_2
                    CURRENT_ANIMATION_PLAYER2 = "idle_2"
                    CURRENT_FRAME_PLAYER2 = 0
            else:
                # Проверяем наличие idle_2 анимации
                if "idle_2" in player2.animations:
                    CURRENT_ANIMATION_PLAYER2 = random.choice(
                        ["idle", "idle_2"]
                    )
                else:
                    CURRENT_ANIMATION_PLAYER2 = "idle"

        player1.update()
        player2.update()

    # Отрисовка текущего фона
    if game_state["show_battle_field"]:
        draw_battle_field(screen)  # Отображаем поле сражения
        draw_battle_inventory()

    elif game_state["show_inventory"]:
        draw_inventory(screen)  # Отображаем инвентарь

    elif game_state["show_settings"]:
        draw_settings(screen)  # Отображаем настройки

    else:
        screen.blit(backgrounds[1], (0, 0))  # Отображаем основной фон

    # Отрисовка кнопок в главном меню
    if (
        not game_state["show_inventory"]
        and not game_state["show_battle_field"]
        and not game_state["show_settings"]
    ):
        for button in menu_buttons:
            button.paint(screen)

    # Обновление экрана
    pygame.display.flip()

    # Контроль FPS
    clock.tick(60)

# Завершение
pygame.quit()
