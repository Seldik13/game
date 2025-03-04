"""
Модуль хелпер функций для игры
"""

import os
import sys


def resource_path(relative_path):
    """
    Возвращает правильный путь для ресурсов
    (работает и в .exe, и в обычном запуске).
    """
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS  # pylint: disable=W0212
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))
        print(base_path)
        print(relative_path)

    return os.path.join(base_path, relative_path)
