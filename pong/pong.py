import random
import pygame, sys

pygame.init()
clock = pygame.time.Clock()

screen_width = 1280
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('pong')

ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
bot = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
player = pygame.Rect(10, screen_height / 2 - 70, 10, 140)
bg_color = pygame.Color('gray12')
light_grey = (200, 200, 200)

ballspeedx = 6 * random.choice((1, -1))
ballspeedy = 6 * random.choice((1, -1))
playerspeed = 0
botspeed = 7


def input():
    global playerspeed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                playerspeed += 7
            if event.key == pygame.K_z:
                playerspeed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                playerspeed -= 7
            if event.key == pygame.K_z:
                playerspeed += 7


def ballmovement():
    global ballspeedx, ballspeedy
    # movement
    ball.x += ballspeedx
    ball.y += ballspeedy
    # collisions

    if ball.top <= 0 or ball.bottom >= screen_height:
        ballspeedy *= -1

    if ball.left <= 0 or ball.right >= screen_width:
        ballrestart()

    if ball.colliderect(player) or ball.colliderect(bot):
        ballspeedx *= -1


def ballrestart():
    global ballspeedx, ballspeedy
    ball.center = (screen_width / 2, screen_height / 2)
    ballspeedy *= random.choice((1, -1))
    ballspeedx *= random.choice((1, -1))


def playermovement():
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

    player.y += playerspeed


def botmovement():
    if bot.top < ball.y:
        bot.top += botspeed
    if bot.bottom > ball.y:
        bot.bottom -= botspeed

    if bot.top <= 0:
        bot.top = 0
    if bot.bottom >= screen_height:
        bot.bottom = screen_height


def draw():
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, bot)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))


while True:
    input()

    ballmovement()
    playermovement()
    botmovement()

    # draw the screen
    draw()

    pygame.display.flip()
    clock.tick(60)
