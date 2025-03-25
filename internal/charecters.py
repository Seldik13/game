"""
Модуль для работы с персонажами в игре.
Содержит класс Player для создания и управления персонажами.
"""

import pygame
from constants import (
    CURRENT_CHARACTER_PLAYER1,
)
from helper import resource_path

animations_path = resource_path("assets")


class Player:
    """
    Класс для создания персонажей.
    Обрабатывает действия и хар-ки персонажей.
    """

    def __init__(
        self,
        character,
        st_x,
        st_y,
        hp,
        defend,
        speed_run,
        jump_height,
        speed_walk,
        animations,
    ):
        """
        Инициализация персонажа.
        """
        self.character = character
        self.st_x = st_x
        self.st_y = st_y
        self.speed_run = speed_run
        self.jump_height = jump_height
        self.speed_walk = speed_walk
        self.hp = hp
        self.defend = defend
        self.animations = animations
        self.is_jumping = False
        self.jump_velocity = 0
        self.gravity = 0.7  # Увеличиваем гравитацию для более быстрого падения
        self.ground_y = st_y  # Начальная позиция Y (земля)
        # Устанавливаем начальное направление в зависимости от игрока
        self.direction = 1 if character == CURRENT_CHARACTER_PLAYER1 else -1
        # Добавляем ману и выносливость
        self.mana = 100 if character == "Wizard" else 0
        self.stamina = 100 if character != "Wizard" else 0

    def move(self, direction, is_running=False):
        """
        Обработка движения персонажа.
        direction: 1 для движения вправо, -1 для движения влево
        is_running: True для бега, False для ходьбы
        """
        self.direction = direction  # Сохраняем направление движения
        speed = self.speed_run if is_running else self.speed_walk
        self.st_x += direction * speed

    def jump(self):
        """Обработка прыжка персонажа."""
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = (
                -self.jump_height
            )  # Возвращаем исходную скорость прыжка

    def update(self):
        """Обновление состояния персонажа."""
        # Обработка прыжка и гравитации
        if self.is_jumping:
            self.st_y += self.jump_velocity
            self.jump_velocity += self.gravity

            # Проверка приземления
            if self.st_y >= self.ground_y:
                self.st_y = self.ground_y
                self.is_jumping = False
                self.jump_velocity = 0

    def attack(self):
        """Обработка атаки персонажа."""
        pass  # Реализация атаки будет добавлена позже

    def take_damage(self, damage):
        """
        Обработка получения урона.
        Учитывает защиту персонажа.
        """
        actual_damage = max(1, damage - self.defend)
        self.hp = max(0, self.hp - actual_damage)
        return self.hp <= 0  # Возвращает True, если персонаж умер


# Создание переменной x для загрузки персонажей
x = {
    "Archer": {
        "attack": [
            pygame.image.load(
                resource_path(f"assets/characters/Archer/attack/{i}0.png")
            )
            for i in range(0, 4)
        ],
        "dead": [
            pygame.image.load(
                resource_path(f"assets/characters/Archer/dead/{i}0.png")
            )
            for i in range(0, 3)
        ],
        "idle": [
            pygame.image.load(
                resource_path(f"assets/characters/Archer/idle/{i}0.png")
            )
            for i in range(0, 6)
        ],
        "jump": [
            pygame.image.load(
                resource_path(f"assets/characters/Archer/jump/{i}0.png")
            )
            for i in range(0, 9)
        ],
        "run": [
            pygame.image.load(
                resource_path(f"assets/characters/Archer/run/{i}0.png")
            )
            for i in range(0, 8)
        ],
        "shot_1": [
            pygame.image.load(
                resource_path(f"assets/characters/Archer/shot_1/{i}0.png")
            )
            for i in range(0, 14)
        ],
        "shot_2": [
            pygame.image.load(
                resource_path(f"assets/characters/Archer/shot_2/{i}0.png")
            )
            for i in range(0, 13)
        ],
        "walk": [
            pygame.image.load(
                resource_path(f"assets/characters/Archer/walk/{i}0.png")
            )
            for i in range(0, 8)
        ],
        "idle_2": [
            pygame.image.load(
                resource_path(f"assets/characters/Archer/idle/{i}0.png")
            )
            for i in range(0, 3)
        ],
    },
    "Enchantress": {
        "attack_1": [
            pygame.image.load(
                resource_path(
                    f"assets/characters/Enchantress/attack_1/{i}0.png"
                )
            )
            for i in range(0, 6)
        ],
        "attack_2": [
            pygame.image.load(
                resource_path(
                    f"assets/characters/Enchantress/attack_2/{i}0.png"
                )
            )
            for i in range(0, 3)
        ],
        "attack_3": [
            pygame.image.load(
                resource_path(
                    f"assets/characters/Enchantress/attack_3/{i}0.png"
                )
            )
            for i in range(0, 3)
        ],
        "attack_4": [
            pygame.image.load(
                resource_path(
                    f"assets/characters/Enchantress/attack_4/{i}0.png"
                )
            )
            for i in range(0, 10)
        ],
        "dead": [
            pygame.image.load(
                resource_path(f"assets/characters/Enchantress/dead/{i}0.png")
            )
            for i in range(0, 5)
        ],
        "hurt": [
            pygame.image.load(
                resource_path(f"assets/characters/Enchantress/hurt/{i}0.png")
            )
            for i in range(0, 2)
        ],
        "idle": [
            pygame.image.load(
                resource_path(f"assets/characters/Enchantress/idle/{i}0.png")
            )
            for i in range(0, 5)
        ],
        "jump": [
            pygame.image.load(
                resource_path(f"assets/characters/Enchantress/jump/{i}0.png")
            )
            for i in range(0, 8)
        ],
        "run": [
            pygame.image.load(
                resource_path(f"assets/characters/Enchantress/run/{i}0.png")
            )
            for i in range(0, 8)
        ],
        "walk": [
            pygame.image.load(
                resource_path(f"assets/characters/Enchantress/walk/{i}0.png")
            )
            for i in range(0, 8)
        ],
    },
    "Knight": {
        "attack_1": [
            pygame.image.load(
                resource_path(f"assets/characters/Knight/attack_1/{i}0.png")
            )
            for i in range(0, 5)
        ],
        "attack_2": [
            pygame.image.load(
                resource_path(f"assets/characters/Knight/attack_2/{i}0.png")
            )
            for i in range(0, 2)
        ],
        "attack_3": [
            pygame.image.load(
                resource_path(f"assets/characters/Knight/attack_3/{i}0.png")
            )
            for i in range(0, 5)
        ],
        "attack_4": [
            pygame.image.load(
                resource_path(f"assets/characters/Knight/attack_4/{i}0.png")
            )
            for i in range(0, 5)
        ],
        "dead": [
            pygame.image.load(
                resource_path(f"assets/characters/Knight/dead/{i}0.png")
            )
            for i in range(0, 4)
        ],
        "hurt": [
            pygame.image.load(
                resource_path(f"assets/characters/Knight/hurt/{i}0.png")
            )
            for i in range(0, 3)
        ],
        "idle": [
            pygame.image.load(
                resource_path(f"assets/characters/Knight/idle/{i}0.png")
            )
            for i in range(0, 6)
        ],
        "jump": [
            pygame.image.load(
                resource_path(f"assets/characters/Knight/jump/{i}0.png")
            )
            for i in range(0, 6)
        ],
        "run": [
            pygame.image.load(
                resource_path(f"assets/characters/Knight/run/{i}0.png")
            )
            for i in range(0, 7)
        ],
        "walk": [
            pygame.image.load(
                resource_path(f"assets/characters/Knight/walk/{i}0.png")
            )
            for i in range(0, 8)
        ],
    },
    "Musketeer": {
        "attack_1": [
            pygame.image.load(
                resource_path(f"assets/characters/Musketeer/attack_1/{i}0.png")
            )
            for i in range(0, 5)
        ],
        "attack_2": [
            pygame.image.load(
                resource_path(f"assets/characters/Musketeer/attack_2/{i}0.png")
            )
            for i in range(0, 4)
        ],
        "attack_3": [
            pygame.image.load(
                resource_path(f"assets/characters/Musketeer/attack_3/{i}0.png")
            )
            for i in range(0, 6)
        ],
        "attack_4": [
            pygame.image.load(
                resource_path(f"assets/characters/Musketeer/attack_4/{i}0.png")
            )
            for i in range(0, 5)
        ],
        "dead": [
            pygame.image.load(
                resource_path(f"assets/characters/Musketeer/dead/{i}0.png")
            )
            for i in range(0, 4)
        ],
        "hurt": [
            pygame.image.load(
                resource_path(f"assets/characters/Musketeer/hurt/{i}0.png")
            )
            for i in range(0, 2)
        ],
        "idle": [
            pygame.image.load(
                resource_path(f"assets/characters/Musketeer/idle/{i}0.png")
            )
            for i in range(0, 5)
        ],
        "jump": [
            pygame.image.load(
                resource_path(f"assets/characters/Musketeer/jump/{i}0.png")
            )
            for i in range(0, 7)
        ],
        "run": [
            pygame.image.load(
                resource_path(f"assets/characters/Musketeer/run/{i}0.png")
            )
            for i in range(0, 8)
        ],
        "walk": [
            pygame.image.load(
                resource_path(f"assets/characters/Musketeer/walk/{i}0.png")
            )
            for i in range(0, 8)
        ],
    },
    "Swordsman": {
        "attack_1": [
            pygame.image.load(
                resource_path(f"assets/characters/Swordsman/attack_1/{i}0.png")
            )
            for i in range(0, 6)
        ],
        "attack_2": [
            pygame.image.load(
                resource_path(f"assets/characters/Swordsman/attack_2/{i}0.png")
            )
            for i in range(0, 3)
        ],
        "attack_3": [
            pygame.image.load(
                resource_path(f"assets/characters/Swordsman/attack_3/{i}0.png")
            )
            for i in range(0, 4)
        ],
        "dead": [
            pygame.image.load(
                resource_path(f"assets/characters/Swordsman/dead/{i}0.png")
            )
            for i in range(0, 3)
        ],
        "hurt": [
            pygame.image.load(
                resource_path(f"assets/characters/Swordsman/hurt/{i}0.png")
            )
            for i in range(0, 3)
        ],
        "idle": [
            pygame.image.load(
                resource_path(f"assets/characters/Swordsman/idle/{i}0.png")
            )
            for i in range(0, 8)
        ],
        "idle_2": [
            pygame.image.load(
                resource_path(f"assets/characters/Swordsman/idle/{i}0.png")
            )
            for i in range(0, 3)
        ],
        "jump": [
            pygame.image.load(
                resource_path(f"assets/characters/Swordsman/jump/{i}0.png")
            )
            for i in range(0, 3)
        ],
        "run": [
            pygame.image.load(
                resource_path(f"assets/characters/Swordsman/run/{i}0.png")
            )
            for i in range(0, 8)
        ],
        "walk": [
            pygame.image.load(
                resource_path(f"assets/characters/Swordsman/walk/{i}0.png")
            )
            for i in range(0, 8)
        ],
    },
    "Wizard": {
        "attack_1": [
            pygame.image.load(
                resource_path(f"assets/characters/Wizard/attack_1/{i}0.png")
            )
            for i in range(0, 10)
        ],
        "attack_2": [
            pygame.image.load(
                resource_path(f"assets/characters/Wizard/attack_2/{i}0.png")
            )
            for i in range(0, 4)
        ],
        "attack_3": [
            pygame.image.load(
                resource_path(f"assets/characters/Wizard/attack_3/{i}0.png")
            )
            for i in range(0, 7)
        ],
        "dead": [
            pygame.image.load(
                resource_path(f"assets/characters/Wizard/dead/{i}0.png")
            )
            for i in range(0, 4)
        ],
        "hurt": [
            pygame.image.load(
                resource_path(f"assets/characters/Wizard/hurt/{i}0.png")
            )
            for i in range(0, 4)
        ],
        "idle": [
            pygame.image.load(
                resource_path(f"assets/characters/Wizard/idle/{i}0.png")
            )
            for i in range(0, 6)
        ],
        "idle_2": [
            pygame.image.load(
                resource_path(f"assets/characters/Wizard/idle_2/{i}0.png")
            )
            for i in range(0, 5)
        ],
        "jump": [
            pygame.image.load(
                resource_path(f"assets/characters/Wizard/jump/{i}0.png")
            )
            for i in range(0, 11)
        ],
        "run": [
            pygame.image.load(
                resource_path(f"assets/characters/Wizard/run/{i}0.png")
            )
            for i in range(0, 8)
        ],
        "walk": [
            pygame.image.load(
                resource_path(f"assets/characters/Wizard/walk/{i}0.png")
            )
            for i in range(0, 7)
        ],
    },
}

# Загрузка анимаций для игроков Player 1  Player 2
player2_animations = x
player1_animations = x
