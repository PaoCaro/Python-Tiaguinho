import sys
import pygame

from pygame.locals import *
from random import random, randint
from math import sqrt

from lib import load_png

WIDTH = 600
HEIGHT = 400

def get_random_colour():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return (r, g, b)


def dist(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1]-p2[1])**2)


class Ball(object):
    color = (0, 0, 0)

    def __init__(self, start_x, start_y, radius):
        self.posX = start_x
        self.posY = start_y
        self.velX = 0
        self.velY = 0
        self.radius = radius
        self.img = load_png("data/ball.png")

    def draw(self, surface):
        pos = (int(self.posX), int(self.posY))
        pygame.draw.circle(surface, Ball.color, pos, int(self.radius))

    def update(self, dt):
        self.velY += 100 * dt
        self.posY += self.velY * dt


class Game(object):
    background_color = (63, 255, 38)

    def __init__(self, score=0):
        self.score = score
        self.ball = Ball(WIDTH / 2, HEIGHT / 2, 30)
        self.reset()

    def reset(self):
        self.ball.posX = WIDTH / 2
        self.ball.posY = 0

        self.ball.velX = 0
        self.ball.velY = 0

        self.score = 0

    def draw(self, surface):
        surface.fill(Game.background_color)
        self.ball.draw(surface)

    def update(self, dt):
        self.ball.update(dt)
        if self.ball.posY > HEIGHT:
            self.reset()

    def handle_click(self, ev):
        if ev.button == 1:
            posBall = (self.ball.posX, self.ball.posY)
            posMouse = ev.pos
            d = dist(posBall, posMouse)
            if d <= self.ball.radius:
                self.ball.velY = -100
            else:
                pass
        elif ev.button == 3:
            pass

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
game = Game(screen)
clock = pygame.time.Clock()

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

    dt = clock.tick(60) / 1000
    game.update(dt)
    game.draw(screen)

    pygame.display.update()
