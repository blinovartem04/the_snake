from random import choice, randint
import pygame

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

BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self) -> None:
        """Инициализация объекта и его позиции."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Отрисовка объекта на экране. Переопределён в дочерних классах."""
        pass


class Apple(GameObject):
    """Класс для объекта яблока."""

    def __init__(self):
        """Инициализация яблока и его начальной позиции."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Случайным образом задаёт позицию яблока на поле."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для объекта змеи."""

    def __init__(self):
        """Инициализация змеи, её длины и начального положения."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.score = 0
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = self.direction

    def get_head_position(self):
        """Получение позиции головы змеи."""
        head_x, head_y = self.positions[0]
        return (head_x * GRID_SIZE, head_y * GRID_SIZE)

    def draw(self):
        """Отрисовка змеи на экране."""
        for position in self.positions:
            rect = pygame.Rect((position[0] * GRID_SIZE,
                                position[1] * GRID_SIZE),
                               (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, SNAKE_COLOR, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def move(self):
        """Движение змеи в заданном направлении."""
        curr = self.positions[0]
        x, y = self.direction

        new = (((curr[0] + x) % GRID_WIDTH), ((curr[1] + y) % GRID_HEIGHT))

        if new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        """Сброс параметров змеи до начальных значений."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def update_direction(self):
        """Обновление направления движения змеи на следующее."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(direction):
    """Обработка нажатий клавиш для изменения направления движения змеи."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != DOWN:
                return UP
            elif event.key == pygame.K_DOWN and direction != UP:
                return DOWN
            elif event.key == pygame.K_LEFT and direction != RIGHT:
                return LEFT
            elif event.key == pygame.K_RIGHT and direction != LEFT:
                return RIGHT
    return direction


def main():
    """Основной игровой цикл."""
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.direction = handle_keys(snake.direction)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
