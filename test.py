# SIMPLE SNAKE GAME
from random import randrange
import pygame

# CONSTANTS
grid = 40
fps = 144
windowWidth = 800
windowHeight = 600

# INITIALIZE PYGAME
pygame.init()

# CREATE THE SCREEN
screen = pygame.display.set_mode((windowWidth, windowHeight))

# SET UP TITLE AND ICON
pygame.display.set_caption("Snake")
icon = pygame.image.load('snake.png')
pygame.display.set_icon(icon)


# FRUIT CLASS
class Apple:
    # CONSTRUCTOR
    def __init__(self, px, py):
        self.px = px
        self.py = py

    # RETURNS X POSITION
    def get_px(self):
        return self.px

    # RETURNS Y POSITION
    def get_py(self):
        return self.py

    # SETS NEW RANDOM XY POSITION
    def find_new(self, obj):
        posx = randrange(windowWidth / grid) * grid
        posy = randrange(windowHeight / grid) * grid

        # IF NEW XY POS IN SNAKE FIND NEW
        for node in obj.get_tail():
            if posx == node[0] and posy == node[1]:
                return self.find_new(obj)

        # IF NEW XY NOT IN SNAKE SET THEM FOR FRUIT
        self.px = posx
        self.py = posy

    def eaten(self, obj):
        self.find_new(obj)


# SNAKE CLASS
class Snake:
    # CONSTRUCTOR
    def __init__(self, px, py, vx, vy, length):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.length = length
        for n in range(self.length):
            self.tail.append((self.px, self.py))

    # UPDATES XY WITH VELOCITY
    def update_pos(self):
        self.px += self.vx * grid
        self.py += self.vy * grid

    # UPDATES VELOCITY DEPENDING ON USER INPUT
    def update_vel(self, direction):
        if direction == 0 and self.vx != -1:
            self.vx = 1
            self.vy = 0
        elif direction == 1 and self.vy != -1:
            self.vx = 0
            self.vy = 1
        elif direction == 2 and self.vx != 1:
            self.vx = -1
            self.vy = 0
        elif direction == 3 and self.vy != 1:
            self.vx = 0
            self.vy = -1

    # RETURNS X POSITION
    def get_px(self):
        return self.px

    # RETURNS Y POSITION
    def get_py(self):
        return self.py

    # RETURNS X VELOCITY
    def get_vx(self):
        return self.vx

    # RETURNS Y VELOCITY
    def get_vy(self):
        return self.vy

    # RETURNS SNAKES LENGTH
    def get_length(self):
        return self.length

    # WHEN SNAKE HEAD IS ON FRUIT XY ADD ONE NODE TO TAIL AND INCREMENT LENGTH
    def ate(self):
        self.tail.append((self.px, self.py))
        self.length += 1

    # WHEN SNAKE HEAD IS ON TAIL XY PRINT SCORE AND RESET GAME
    def died(self, obj):
        print(f"Sorry you lost, score: {snake.get_length()}")
        self.px = 0
        self.py = 0
        self.vx = 1
        self.vy = 0
        self.length = 3
        self.tail.clear()
        for n in range(self.length):
            self.tail.append((self.px, self.py))
        obj.eaten(self)

    tail = []

    # RETURNS SNAKES TAIL NODES
    def get_tail(self):
        return self.tail

    # UPDATES SNAKE NODES DUE TO MOVEMENT
    def update_tail(self):
        self.tail.insert(0, (self.px, self.py))
        self.tail.pop()

    # WHEN SNAKE CROSSES BOUND MAKE IT APPEAR ON THE OPPOSITE SIDE
    def check_bounds(self):
        if self.px > windowWidth - grid:
            self.px = 0
        elif self.px < 0:
            self.px = windowWidth - grid

        if self.py > windowHeight - grid:
            self.py = 0
        elif self.py < 0:
            self.py = windowHeight - grid

    # CHECKS FOR SNAKE XY IN FRUIT XY
    def check_apple(self, px, py, obj):
        if self.px == px and self.py == py:
            self.ate()
            obj.eaten(self)

    # CHECKS FOR SNAKE XY IN TAIL NODES XY
    def check_collision(self, obj):
        for n in range(1, len(self.tail) - 1):
            if self.tail[0][0] == self.tail[n][0] and self.tail[0][1] == self.tail[n][1]:
                self.died(obj)
                return 0

    # CHECKS IF THE NUMBER OF NODES IS EQUAL TO MAX GRID SQUARES
    def check_win(self):
        if self.length >= windowWidth/grid * windowHeight/grid - 2:
            print("CONGRATULATIONS YOU WON THE GAME!!!")
            return False
        else:
            return True


# SETUP
running = True
direction = 0
clock = pygame.time.Clock()
snake = Snake(0, 0, 1, 0, 3)
apple = Apple(randrange(windowWidth/grid) * grid, (1 + randrange(windowHeight/grid - 1)) * grid)
count = 0
pressed = False

# GAME LOOP
while running:
    # SET FPS TO 144
    clock.tick(fps)

    # CLEAR SCREEN
    screen.fill((0, 0, 0))

    # CHECK FOR KEY INPUT AND STORE IT IN LIST
    keyinput = pygame.key.get_pressed()

    # CHECK FOR EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # CHECK IF KEYS PRESSED
    if not pressed:
        if keyinput[pygame.K_RIGHT]:
            direction = 0
            pressed = True
        if keyinput[pygame.K_DOWN]:
            direction = 1
            pressed = True
        if keyinput[pygame.K_LEFT]:
            direction = 2
            pressed = True
        if keyinput[pygame.K_UP]:
            direction = 3
            pressed = True

    # UPDATE DATA
    count += 1
    if count >= fps/12:
        snake.update_vel(direction)
        snake.update_pos()
        snake.check_apple(apple.get_px(), apple.get_py(), apple)
        snake.check_bounds()
        snake.update_tail()
        direction = snake.check_collision(apple)
        running = snake.check_win()
        pressed = False
        count = 0

    # DRAW
    for node in snake.get_tail():
        rect = pygame.Rect(node[0], node[1], grid-1, grid-1)
        pygame.draw.rect(screen, (0, 255, 0), rect)

    appleRect = pygame.Rect(apple.get_px(), apple.get_py(), grid-1, grid-1)
    pygame.draw.rect(screen, (255, 0, 0), appleRect)

    pygame.display.update()