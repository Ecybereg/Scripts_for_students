import pygame
import time
import random

pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Set display dimensions
dis_width = 600
dis_height = 400

# Initialize the display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('** MEAN MACHINE **')

# Initialize the clock to control the frame rate
clock = pygame.time.Clock()

# Define the size of each snake block and the initial speed of the snake
snake_block = 10
snake_speed = 10  # Initial speed, can be adjusted

# Set up fonts for displaying score and messages
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


def draw_score(score):
    # Render and display the player's score
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


def draw_snake(snake_list):
    # Draw the snake on the screen
    for segment in snake_list:
        pygame.draw.rect(dis, green, [segment[0], segment[1], snake_block, snake_block])


def draw_message(msg, color):
    # Render and display messages on the screen
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def game_loop():
    global snake_speed  # Declare snake_speed as a global variable

    # Initialize game state variables
    game_over = False
    game_close = False

    # Initialize the snake's head position
    x1 = dis_width / 2
    y1 = dis_height / 2

    # Initialize the snake's movement direction
    x1_change = 0
    y1_change = 0

    # Initialize the snake's body
    snake_list = []
    length_of_snake = 1

    # Initialize the position of the food
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            # Display the message when the game is over
            dis.fill(blue)
            draw_message("You Lost! Press C-Play Again or Q-Quit", red)
            draw_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            # Check if the snake hits the boundaries
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(black)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                # Check if the snake collides with itself
                game_close = True

        draw_snake(snake_list)
        draw_score(length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            # Generate a new position for the food when the snake eats it
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

            # Increase the snake speed by 1 each time it eats
            snake_speed += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


game_loop()
