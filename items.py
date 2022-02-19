import curses
import random
from typing import Callable


class Item:
    def __init__(self, screen_height: int, screen_width: int, callback: Callable):
        self.y = random.randint(0, screen_height)
        self.x = random.randint(0, screen_width)
        self.callback = callback
        self.color_pair = curses.COLOR_GREEN
        self.char = '#'

    def collision_handler(self, *args):
        self.callback(*args)


class Food(Item):
    def __init__(self, screen_height: int, screen_width: int, callback: Callable):
        super().__init__(screen_height, screen_width, callback)
        self.color_pair = 2


class Bomb(Item):
    def __init__(self, screen_height: int, screen_width: int, callback: Callable):
        super().__init__(screen_height, screen_width, callback)
        self.color_pair = 3
        self.char = 'x'
