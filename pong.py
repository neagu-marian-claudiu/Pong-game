import pygame
import random
import sys

pygame.init()
clock = pygame.time.Clock()


# GoalReset
def reset_ball():
    global ball_speed_x, ball_speed_y, pause, goal
    pause = True
    ball.center = (WIDTH/2, HEIGHT/2)
    ball_speed_x *= random.choice((1, -1))
    ball_speed_y *= random.choice((1, -1))
    goal = True


# Movement
def ball_movement():
    global ball_speed_x, ball_speed_y, player_score, opponent_score
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
    if ball.left <= 0:
        reset_ball()
        opponent_score += 1

    if ball.right >= WIDTH:
        reset_ball()
        player_score += 1

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1


def player_movement():
    global player_speed
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= HEIGHT:
        player.bottom = HEIGHT


def opponent_movement():
    if ball.top > opponent.top:
        opponent.y += 5
    if ball.bottom < opponent.bottom:
        opponent.y -= 6
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= HEIGHT:
        opponent.bottom = HEIGHT


# Screen
WIDTH = 1080
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Variables
ball = pygame.Rect(WIDTH/2 - 15, HEIGHT/2 - 15, 30, 30)
player = pygame.Rect(10, HEIGHT/2 - 70, 10, 140)
opponent = pygame.Rect(WIDTH-20, HEIGHT/2 - 70, 10, 140)
ball_speed_x = 6
ball_speed_y = 6
player_speed = 0
pause = False
goal = False
image = pygame.image.load(r"play.png")
image = pygame.transform.scale(image, (50, 50))
player_score = 0
opponent_score = 0
game_font = pygame.font.SysFont("freesansbolt.ttf", 32)

# GameLoop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 6
            if event.key == pygame.K_UP:
                player_speed -= 6
            if event.key == pygame.K_ESCAPE:
                pause = True
            if event.key == pygame.K_SPACE:
                pause = False
                goal = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 6
            if event.key == pygame.K_UP:
                player_speed += 6

    screen.fill(pygame.Color('grey12'))
    pygame.draw.rect(screen, (200, 200, 200), player)
    pygame.draw.rect(screen, (200, 200, 200), opponent)
    pygame.draw.aaline(screen, (200, 200, 200),
                       (WIDTH/2, 0), (WIDTH/2, HEIGHT))
    pygame.draw.ellipse(screen, (200, 200, 200), ball)
    if pause == False:
        ball_movement()
        player_movement()
        opponent_movement()
        pygame.display.set_caption('Pong...game in progress')

    else:
        if goal == True:
            pygame.display.set_caption('Press SPACE to continue the game')
            screen.blit(goal_text, (480, 40))
        else:
            pygame.display.set_caption('Press SPACE to continue the game')
            screen.blit(image, (WIDTH/2 - 25, HEIGHT/2 - 25))

    player_text = game_font.render(f"{player_score}", False, (200, 200, 200))
    screen.blit(player_text, (500, 10))
    opponent_text = game_font.render(
        f"{opponent_score}", False, (200, 200, 200))
    screen.blit(opponent_text, (570, 10))
    goal_text = game_font.render("GOALLLLL!!!", False, (200, 200, 200))
    if goal == True:
        pause = True

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)
