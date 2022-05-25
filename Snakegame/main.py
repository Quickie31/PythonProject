import random
import pygame
import sys
import pygame_menu
from tkinter import *

pygame.init()


background_image = pygame.image.load("background.jpg")
snake_colour = (0, 128, 0)
frame_colour = [0, 250, 210]
size_block = 20
margin = 1
food_colour = (102, 0, 0)
white = (255, 255, 255)
light_cyan = (224, 255, 255)
head_colour = (0, 204, 153)
head_margin = 70
count_blocks = 30
window_size = [size_block * count_blocks + 2 * size_block + margin * count_blocks,
          size_block * count_blocks + 2 * size_block + margin * count_blocks + head_margin]
pygame.display.set_caption("Игра Змейка")
comicsansms = pygame.font.SysFont('comicsansms', 38)
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()


class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def correct_position(self):
        return 0 <= self.x < count_blocks and 0 <= self.y < count_blocks

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def draw_block(colour, row, column):
    pygame.draw.rect(screen, colour, [size_block + column * size_block + margin * (column + 1),
                                      head_margin + size_block + row * size_block + margin * (row + 1),
                                      size_block,
                                      size_block])


def start_the_game():
    def get_random_block():
        x = random.randint(0, count_blocks - 1)
        y = random.randint(0, count_blocks - 1)
        random_block = SnakeBlock(x, y)
        while random_block in snake_blocks:
            random_block.x = random.randint(0, count_blocks - 1)
            random_block.y = random.randint(0, count_blocks - 1)
        return random_block

    def show_number_of_points(points):
        window = Tk()
        window.title("Игра окончена")
        window.geometry('300x50')
        lbl = Label(window, text=f"Ваш результат: {points}", font=("comicsansms", 15))
        lbl.grid(column=0, row=0)
        window.mainloop()

    d_row = buf_row = 0
    d_col = buf_col = 1
    speed = 1
    total_points = 0
    snake_blocks = [SnakeBlock(15, 15), SnakeBlock(15, 16), SnakeBlock(15, 17)]
    food = get_random_block()


    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    buf_row = 1
                    buf_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = 1

        screen.fill(frame_colour)
        pygame.draw.rect(screen, head_colour, [0, 0, window_size[0], head_margin])

        text_total = comicsansms.render(f"Total points: {total_points}", 0, white)
        text_speed = comicsansms.render(f"Speed: {speed}", 0, white)
        screen.blit(text_total, (size_block, size_block))
        screen.blit(text_speed, (size_block + 400, size_block))

        for row in range(count_blocks):
            for column in range(count_blocks):
                if (row + column) % 2 == 0:
                    colour = light_cyan
                else:
                    colour = white
                draw_block(colour, row, column)

        head = snake_blocks[-1]
        if not head.correct_position():
            show_number_of_points(total_points)
            break

        draw_block(food_colour, food.x, food.y)  # рисовка еда

        for block in snake_blocks:
            draw_block(snake_colour, block.x, block.y)

        pygame.display.flip()

        if head == food:
            total_points += 1
            speed = total_points // 5 + 1
            snake_blocks.append(food)
            food = get_random_block()

        d_row = buf_row
        d_col = buf_col
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        if new_head in snake_blocks:
            show_number_of_points(total_points)
            break

        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        clock.tick(4 + speed)


menu = pygame_menu.Menu('Welcome', 350, 250,
                        theme=pygame_menu.themes.THEME_BLUE)

menu.add.button('Играть', start_the_game)
menu.add.button('Выйти', pygame_menu.events.EXIT)

while True:

    screen.blit(background_image, (-10, -10))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()
