# Imports
import pygame
import os
import random

# Initializing components
pygame.init()
pygame.font.init()

# Setting up the window
screen_width = 800
screen_height = 600
fps = 60
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Robo Dash')
pygame.display.set_icon(pygame.image.load(os.path.join('Assets', 'Player_Image.png')))

# Game values
score = 0

vel = 5
jump_vel = vel * 2

player_width, player_height = 50, 100
obstacle_width, obstacle_height = 50, 50
ground_y = 500
ground_width, ground_height = screen_width, 100

jump_height = ground_y - player_height - 150

# Game states
jumping = False

game_over = False

# Initializing colours
white = (255, 255, 255)
black = (0, 0, 0)

# Setting up fonts
score_font = pygame.font.SysFont('comicsans', 25)
game_over_font = pygame.font.SysFont('comicsans', 100)

# Loading images
player_img = pygame.image.load(os.path.join('Assets', 'Player_Image.png'))
obstacle_img = pygame.image.load(os.path.join('Assets', 'Obstacle_Image.png'))
sky_img = pygame.image.load(os.path.join('Assets', 'Sky_Image.png'))
ground_img = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Ground_Image.png')),
                                    (ground_width, ground_height))


# Controls the movement of the player
def move_player(player, keys_pressed):
    global jumping
    if (keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]) and not jumping and player.y + player_height >= ground_y:
        jumping = True
    elif jumping:
        if player.y > jump_height:
            player.y -= jump_vel
        elif player.y <= jump_height:
            jumping = False


# Makes the player fall to the ground if in the air
def manage_gravity(player):
    if player.y + player_height < ground_y - vel and not jumping:
        player.y += vel
    elif player.y + player_height < ground_y and not jumping:
        player.y += ground_y - (player.y + player_height)


# Moves the sky and ground to give the illusion of the player moving
def move_screen(obstacles, skies, grounds):
    for sky in skies:
        if sky.x + screen_width <= 0:
            sky.x = screen_width - vel
        else:
            sky.x -= vel
    for ground in grounds:
        if ground.x + ground_width <= 0:
            ground.x = screen_width - vel
        else:
            ground.x -= vel
    for obstacle in obstacles:
        if obstacle.x + obstacle_width <= 0:
            obstacles.remove(obstacle)
            obstacles.append(pygame.Rect((random.randint(screen_width - obstacle_width,
                                                         screen_width + screen_width // 2), ground_y - obstacle_height),
                                         (obstacle_width, obstacle_height)))
        else:
            obstacle.x -= vel


# Checks if the player has collided with any obstacles
def obstacle_collision(player, obstacles):
    for obstacle in obstacles:
        if (player.x >= obstacle.x and player.x + player_width <= obstacle.x + obstacle_width and player.y + player_height >= obstacle.y) or (player.colliderect(obstacle)):
            finish_game()


# Manages the end of the game after the player has collided with an obstacle
def finish_game():
    global game_over
    game_over_text = game_over_font.render('Game Over!', True, black)
    win.blit(game_over_text, (
        screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
    score_text = score_font.render(f'Score: {str(int(score // 1))}', True, black)
    win.blit(score_text, (screen_width // 2 - score_text.get_width() // 2,
                          screen_height // 2 - game_over_text.get_height() // 2 + game_over_text.get_height() + 25))
    pygame.display.update()
    pygame.time.wait(1000)
    game_over = True


# Draws the window
def draw_window(player, obstacles, skies, grounds):
    for sky in skies:
        win.blit(sky_img, (sky.x, sky.y))
    for ground in grounds:
        win.blit(ground_img, (ground.x, ground.y))
    for obstacle in obstacles:
        win.blit(obstacle_img, (obstacle.x, obstacle.y))
    win.blit(player_img, (player.x, player.y))
    score_text = score_font.render(str(int(score // 1)), True, black)
    win.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 0))
    pygame.display.update()


# The main function that runs the game
def main():
    global score
    global game_over

    run = True
    clock = pygame.time.Clock()

    # The entities
    skies = [pygame.Rect((0, 0), (screen_width, screen_height)),
             pygame.Rect((screen_width, 0), (screen_width, screen_height))]
    player = pygame.Rect((100, 400), (player_width, player_height))
    grounds = [pygame.Rect((0, ground_y), (ground_width, ground_height)),
               pygame.Rect((ground_width, ground_y), (ground_width, ground_height))]
    obstacles = [
        pygame.Rect((screen_width - obstacle_width, ground_y - obstacle_height), (obstacle_width, obstacle_height))]

    # The game loop
    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                pass

        keys_pressed = pygame.key.get_pressed()

        if game_over:
            game_over = False
            break

        obstacle_collision(player, obstacles)
        move_player(player, keys_pressed)
        manage_gravity(player)
        move_screen(obstacles, skies, grounds)

        draw_window(player, obstacles, skies, grounds)
        score += 0.2  # The score counter
    main()


if __name__ == '__main__':
    main()
