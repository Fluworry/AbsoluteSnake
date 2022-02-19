from items import Food, Bomb


class Snake:
    def __init__(self, length: int, head: str = '0'):
        self.length = length
        self.coords = [[0, i] for i in range(length, 0, -1)]

        self.head = head
        self.body = ['o' for i in range(length - 1)]
        self.body.insert(0, self.head)

        self.alive = True

        self.collision_callbacks = {
            Food: self.eat,
            Bomb: self.die
        }
        # self.register_callback(Food, self.eat)
        # self.register_callback(Bomb, self.die)

        self.direction_keys = {
            "w": 'up', "s": 'down',
            "a": 'left', "d": 'right'
        }
        self.direction = 'right'

        self.menu_keys = {
            'q': self.die
        }

    def key_press(self, key):
        try:
            if key.char in self.direction_keys.keys():
                self.direction = self.direction_keys[key.char]
            elif key.char in self.menu_keys.keys():
                self.menu_keys[key.char]()
        except AttributeError:
            pass
        except KeyError:
            pass

    # def register_callback(self, Item, callback):
    #     self.collision_callbacks[Item] = callback

    def move(self, current_items: list):
        if self.coords[0] in self.coords[1:]:
            self.die()

        for item in current_items.copy():
            if self.coords[0] == [item.y, item.x]:
                # self.eat()
                item.collision_handler()
                current_items.remove(item)
                # self.screen.delch(food.y, food.x)

        new_head = self._update_head()

        self.coords.insert(0, new_head)
        self.coords.pop()

        return self.coords, self.body

    def eat(self):
        self.length += 1

        new_head = self._update_head()

        self.coords.insert(0, new_head)
        self.body.append('o')

    def _update_head(self) -> list:
        new_head = [self.coords[0][0], self.coords[0][1]]

        if self.direction == 'down':
            new_head[0] += 1
        elif self.direction == 'up':
            new_head[0] -= 1
        elif self.direction == 'left':
            new_head[1] -= 1
        elif self.direction == 'right':
            new_head[1] += 1
        return new_head

    def die(self):
        self.alive = False
