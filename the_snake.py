import pygame
from random import randint

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    # print('handle_keys')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


# Тут опишите все классы игры.
class GameObject:
    """Класс GameObject"""

    def __init__(self):
        """Конструктор класса GameObject"""
        self.position = (0, 0)
        self.body_color = (0, 0, 0)

    def draw(self):
        """Метод заглушка для наследования"""
        pass


class Apple(GameObject):
    """Класс Apple"""

    def __init__(self):
        """Конструктор класса Apple"""
        super().__init__()
        self.body_color = (255, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        """Задает случайную позицию на сцене для яблока"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовывает объект яблоко на сцене"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс Snake"""

    def __init__(self):
        """Конструктор класса Snake"""
        super().__init__()
        self.length = 1
        x_cord = GRID_WIDTH * GRID_SIZE // 2
        y_cord = GRID_HEIGHT * GRID_SIZE // 2
        self.positions = [(x_cord, y_cord)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (0, 255, 0)
        self.last = None

    def update_direction(self):
        """Обновление направления движения змеи"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Осуществляет передвижение змеи"""
        now_cord = self.positions[-1]
        x_cord = (now_cord[0] + GRID_SIZE * self.direction[0]) % SCREEN_WIDTH,
        y_cord = (now_cord[1] + GRID_SIZE * self.direction[1]) % SCREEN_HEIGHT,
        new_cord = (x_cord, y_cord)
        if new_cord in self.positions:
            raise ValueError("Столкновение змеи с собой")
        else:
            self.positions.append(new_cord)

    @property
    def get_head_position(self):
        """Вовзращает позицию головы змеи"""
        if len(self.positions) > 0:
            return self.positions[-1]
        else:
            return None

    def draw(self):
        """Отрисовывает змею по массиву positions на сцену"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Вызывается при столкновении змеи с собой"""
        if self.last:
            self.positions.append(self.last)
        for elem in self.positions:
            # print(elem, end = '  ')
            last_rect = pygame.Rect(elem, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        self.__init__()


def main():
    """Реализация игры Змейка"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.

    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        try:
            snake.move()
        except ValueError:
            snake.reset()
            continue

        apple.draw()
        snake.draw()

        if snake.get_head_position == apple.position:
            apple.randomize_position()
            snake.length += 1
        else:
            snake.last = snake.positions[0]
            snake.positions.pop(0)
        pygame.display.update()

        # print(snake.length, snake.positions)

        # break


if __name__ == "__main__":
    main()
