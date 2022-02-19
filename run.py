import curses
import time
import random
from pynput import keyboard
from typing import Callable

from snake import Snake
from items import Food, Bomb


class Game:
    def __init__(self):
        self.screen = curses.initscr()
        self.screen_height, self.screen_width = self.screen.getmaxyx()

        curses.start_color()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

        self.screen.bkgd(' ', curses.color_pair(1))

        # self.is_running = True

        self.snake = Snake(3)
        self.current_items = []

        # If no food and only bombs, items number can be bigger
        self.max_items = 4

        self.listener = keyboard.Listener(
            on_press=self.snake.key_press,
            suppress=True
        )
        self.listener.start()

    def update(self) -> None:
        if not self.snake.alive:
            curses.endwin()
            exit()

        if not self.current_items or not any(isinstance(item, Food) for item in self.current_items):
            items = self._random_items(self.screen_height, self.screen_width)
            self.current_items.extend(items)

        snake_coords, snake_body = self.snake.move(self.current_items)

        for item in self.current_items.copy():
            try:
                self.screen.addch(item.y, item.x, item.char, curses.color_pair(item.color_pair))
            except:
                pass

        for i in range(len(snake_coords)):
            try:
                self.screen.addch(snake_coords[i][0], snake_coords[i][1], snake_body[i])
            except curses.error:
                self.snake.die()

        self.screen.refresh()
        self.screen.clear()

    def _random_items(self, *args):
        return map(
            lambda item: item(*args, callback=self.snake.collision_callbacks[item]),
            random.choices(
                list(self.snake.collision_callbacks.keys()),
                k=random.randint(1, self.max_items)
                )
            )


if __name__ == "__main__":
    game = Game()

    while True:
        time.sleep(0.1)
        game.update()
