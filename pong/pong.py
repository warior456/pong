import random

import pygame, sys

pygame.init()
clock = pygame.time.Clock()

gamestate = 1
playerscore = 0
botscore = 0

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
    global ballspeedx, ballspeedy, botscore, playerscore
    # movement
    ball.x += ballspeedx
    ball.y += ballspeedy
    # collisions

    if ball.top <= 0 or ball.bottom >= screen_height:
        ballspeedy *= -1

    if ball.left <= 0:
        botscore += 1
        ballrestart()

    if ball.right >= screen_width:
        playerscore += 1
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


def drawplaying():
    global playerscore, botscore

    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))
    # scoreboard
    font = pygame.font.SysFont('arial.ttf', 40)
    scoreboard = font.render('SCORE', True, light_grey, bg_color)
    scoreboardRect = scoreboard.get_rect()
    scoreboardRect.center = (screen_width // 2, 20)
    screen.blit(scoreboard, scoreboardRect)

    playerscoredisplay = font.render(str(playerscore), True, light_grey, bg_color)
    playerscoredisplay_rect = playerscoredisplay.get_rect()
    playerscoredisplay_rect.center = (screen_width // 2 - 80, 20)
    screen.blit(playerscoredisplay, playerscoredisplay_rect)

    botscoredisplay = font.render(str(botscore), True, light_grey, bg_color)
    botscoredisplay_rect = botscoredisplay.get_rect()
    botscoredisplay_rect.center = (screen_width // 2 + 80, 20)
    screen.blit(botscoredisplay, botscoredisplay_rect)

    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, bot)
    pygame.draw.ellipse(screen, light_grey, ball)


def drawpaused():
    print("paused")


def drawmenu():
    print("menu")


def game(gamestate):
    if gamestate == 1:
        playing()
    elif gamestate == 2:
        paused()
    elif gamestate == 3:
        menu()


def playing():
    input()
    ballmovement()
    playermovement()
    botmovement()
    drawplaying()


def paused():
    input()
    drawplaying()
    drawpaused()
    print("paused")


def menu():
    input()
    drawmenu()
    print("menu")


while True:
    screen.fill(bg_color)
    game(gamestate)

    pygame.display.flip()
    clock.tick(60)
