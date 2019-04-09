import sys
import pygame
from pygame.locals import *
from random import random, randint
from math import sqrt


class Painter(object):
    def __init__(self, surf):
        self.surface = surf
        self.start_line = None
        self.start_right = None
        self.width = 5

    def random_colour(self):
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        return (r, g, b)

    def increment_width(self):
        self.width += 1

    def decrement_width(self):
        self.width -= 1
        if self.width < 1:
            self.width = 1

    def clear_canvas(self):
        """Clears the canvas and fills it with a random colour"""
        c = self.random_colour()
        self.surface.fill(c)
        pass

    def dist(self, p1, p2):
        return sqrt((p1[0] - p2[0])**2 + (p1[1]-p2[1])**2)

    def handle_click(self, ev):
        if ev.button == 1:
            if self.start_line is None:
                self.start_line = ev.pos
            else:
                pygame.draw.line(
                    self.surface,
                    self.random_colour(),
                    self.start_line,
                    ev.pos,
                    self.width)
                self.start_line = None
        elif ev.button == 3:
            if self.start_right is None:
                self.start_right = ev.pos
            elif random() < 0.5:
                # draw a circle
                radius = round(self.dist(ev.pos, self.start_right))
                pygame.draw.circle(
                    self.surface,
                    self.random_colour(),
                    self.start_right,
                    radius,
                    self.width)
                self.start_right = None
            else:
                w = abs(self.start_right[0]-ev.pos[0])
                h = abs(self.start_right[1]-ev.pos[1])
                l = min(self.start_right[0], ev.pos[0])
                t = min(self.start_right[1], ev.pos[1])
                r = pygame.Rect(l, t, w, h)
                pygame.draw.rect(self.surface,
                                 self.random_colour(),
                                 r,
                                 self.width)
                self.start_right = None

WIDTH = 600
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))

painter = Painter(screen)

while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            sys.exit()
        elif ev.type == MOUSEBUTTONDOWN:
            painter.handle_click(ev)
        elif ev.type == KEYDOWN:
            if ev.key == K_0:
                painter.clear_canvas()
            elif ev.key == K_UP:
                painter.increment_width()
            elif ev.key == K_DOWN:
                painter.decrement_width()

    pygame.display.update()
