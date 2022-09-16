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
player2 = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
player1 = pygame.Rect(10, screen_height / 2 - 70, 10, 140)
bg_color = pygame.Color('gray12')
light_grey = (200, 200, 200)

ballspeedx = 6 * random.choice((1, -1))
ballspeedy = 6 * random.choice((1, -1))
player1speed = 0
player2speed = 0
botspeed = 7

font = pygame.font.SysFont('arial.ttf', 40)


def input():
    global gamestate
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
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
    global player1speed
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            player1speed -= 7
        if event.key == pygame.K_q:
            player1speed += 7
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            player1speed += 7
        if event.key == pygame.K_q:
            player1speed -= 7


def player2input(event):
    global player2speed
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_i:
            player2speed -= 7
        if event.key == pygame.K_k:
            player2speed += 7
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_i:
            player2speed += 7
        if event.key == pygame.K_k:
            player2speed -= 7



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

    if ball.colliderect(player1) and ballspeedx < 0:
        if abs(ball.left - player1.right) < 10:
            ballspeedx *= -1
        elif abs(ball.bottom - player1.top) < 10 and ballspeedy > 0:
            ballspeedy *= -1
        elif abs(ball.top - player1.bottom) < 10 and ballspeedy < 0:
            ballspeedy *= -1

    if ball.colliderect(player2) and ballspeedx > 0:
        if abs(ball.right - player2.left) < 10:
            ballspeedx *= -1
        elif abs(ball.bottom - player2.top) < 10 and ballspeedy > 0:
            ballspeedy *= -1
        elif abs(ball.top - player2.bottom) < 10 and ballspeedy < 0:
            ballspeedy *= -1


def ballrestart():
    global ballspeedx, ballspeedy
    ball.center = (screen_width / 2, screen_height / 2)
    ballspeedy *= random.choice((1, -1))
    ballspeedx *= random.choice((1, -1))


def player1movement():
    if player1.top <= 0:
        player1.top = 1
    if player1.bottom >= screen_height:
        player1.bottom = screen_height - 2

    player1.y += player1speed


def player2movement():
    if player2.top <= 0:
        player2.top = 1
    if player2.bottom >= screen_height:
        player2.bottom = screen_height - 2

    player2.y += player2speed

def bot():
    if player2.top < ball.y:
        player2.top += botspeed
    if player2.bottom > ball.y:
        player2.bottom -= botspeed

    if player2.top <= 0:
        player2.top = 0
    if player2.bottom >= screen_height:
        player2.bottom = screen_height


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

    pygame.draw.rect(screen, light_grey, player1)
    pygame.draw.rect(screen, light_grey, player2)
    pygame.draw.ellipse(screen, light_grey, ball)


def drawpaused():
    paused = font.render("PAUSED", True, light_grey, bg_color)
    pausedRect = paused.get_rect()
    pausedRect.center = (screen_width // 2, screen_height//2)
    screen.blit(paused, pausedRect)


def drawmenu():
    menu = font.render("Menu", True, light_grey, bg_color)
    menuRect = menu.get_rect()
    menuRect.center = (screen_width // 2, screen_height//5)
    screen.blit(menu, menuRect)


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
    player1movement()
    player2movement()
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
