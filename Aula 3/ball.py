import sys
import pygame

from pygame.locals import *
from random import random, randint
from math import sqrt

WIDTH = 600
HEIGHT = 400

BGCOLOR = (63, 255, 38)
BALLCOLOR = (0, 0, 0)

def random_colour():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return (r, g, b)

class Ball(object):
    def __init__(self, start_x, start_y, radius):
        self.posX = start_x
        self.posY = start_y
        self.velX = 0
        self.velY = 0
        self.radius = radius

    def draw(self, surface):
        pygame.draw.circle(
            surface,
            BALLCOLOR,
            (int(self.posX), int(self.posY)),
            int(self.radius))

    def update(self):
        self.velY += 0.00001
        self.posY += self.velY

ball = Ball(WIDTH / 2, HEIGHT / 2, 30)

class Game(object):
    def __init__(self, surf, score = 0):
        self.surface = surf
        ### Variavel n�o tem ()
        self.score = score
        ### Uma fun��o tem ()
        self.reset()

    def reset(self):
        ball.posX = WIDTH / 2
        ball.posY = 0
        
        ball.velX = 0
        ball.velY = 0
        
        self.score = 0

    def dist(self, p1, p2):
        return sqrt((p1[0] - p2[0])**2 + (p1[1]-p2[1])**2)

    def draw(self):
        self.surface.fill(BGCOLOR)
        ball.draw(self.surface)

    def update(self):
        ball.update()

        if ball.posY > HEIGHT:
            self.reset() 

    def handle_click(self, ev):
        if ev.button == 1:
            posBall = (ball.posX, ball.posY)
            posMouse = ev.pos
            d = self.dist(posBall, posMouse)
            if d <= ball.radius:
                ball.velY = -0.05
            else:
                pass
        elif ev.button == 3:
            pass
            


screen = pygame.display.set_mode((WIDTH, HEIGHT))
game = Game(screen)

while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            sys.exit()
        elif ev.type == MOUSEBUTTONDOWN:
            game.handle_click(ev)
        elif ev.type == KEYDOWN:
            if ev.key == K_u:
                game.reset()

    game.update()
    game.draw()
    pygame.display.update()
