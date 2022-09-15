import random

import pygame, sys

pygame.init()
clock = pygame.time.Clock()

gamestate =1
playerscore = 0
botscore = 0

screen_width = 1280
screen_height = 960
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

font = pygame.font.SysFont('arial.ttf', 40)


def input():
    global gamestate
    global playerspeed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.key == pygame.K_p:  # pause
            if gamestate == 1:
                gamestate = 2
                return
            if gamestate == 2:
                gamestate = 1
                return
        if event.key == pygame.K_ESCAPE:  # menu
            if gamestate == 1 or gamestate == 2:
                gamestate = 3
                return
            if gamestate == 3:
                gamestate = 1
                return

        player1input(event)
        player2input(event)




def player1input(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            playerspeed += 7
        if event.key == pygame.K_q:
            playerspeed -= 7
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            playerspeed -= 7
        if event.key == pygame.K_q:
            playerspeed += 7


def player2input(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_i:
            playerspeed -= 7
        if event.key == pygame.K_k:
            playerspeed += 7
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_i:
            playerspeed -= 7
        if event.key == pygame.K_k:
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

    if ball.colliderect(player) and ballspeedx < 0:
        if abs(ball.left - player.right) < 10:
            ballspeedx *= -1
        elif abs(ball.bottom - player.top) < 10 and ballspeedy > 0:
            ballspeedy *= -1
        elif abs(ball.top - player.bottom) < 10 and ballspeedy < 0:
            ballspeedy *= -1

    if ball.colliderect(bot) and ballspeedx > 0:
        if abs(ball.right - bot.left) < 10:
            ballspeedx *= -1
        elif abs(ball.bottom - bot.top) < 10 and ballspeedy > 0:
            ballspeedy *= -1
        elif abs(ball.top - bot.bottom) < 10 and ballspeedy < 0:
            ballspeedy *= -1


def ballrestart():
    global ballspeedx, ballspeedy
    ball.center = (screen_width / 2, screen_height / 2)
    ballspeedy *= random.choice((1, -1))
    ballspeedx *= random.choice((1, -1))


def player1movement():
    if player.top <= 0:
        player.top = 1
    if player.bottom >= screen_height:
        player.bottom = screen_height - 2

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
    scoreboard = font.render("SCORE", True, light_grey, bg_color)
    scoreboardRect = scoreboard.get_rect()
    scoreboardRect.center = (screen_width // 2, 20)
    screen.blit(scoreboard, scoreboardRect)

    playerscoredisplay = font.render(f"{playerscore}", True, light_grey)
    scoreboardRect.center = (screen_width // 2 - 60, 20)
    screen.blit(playerscoredisplay, scoreboardRect)

    botscoredisplay = font.render(f"{botscore}", True, light_grey)
    scoreboardRect.center = (screen_width // 2 + 140, 20)
    screen.blit(botscoredisplay, scoreboardRect)

    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, bot)
    pygame.draw.ellipse(screen, light_grey, ball)


def drawpaused():
    paused = font.render("PAUSED", True, light_grey, bg_color)
    pausedRect = paused.get_rect()
    pausedRect.center = (screen_width // 2, screen_height//2)
    screen.blit(paused, pausedRect)


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
    drawpaused()
    input()


def menu():
    input()
    drawmenu()


while True:
    screen.fill(bg_color)
    game(gamestate)

    pygame.display.flip()
    clock.tick(60)
