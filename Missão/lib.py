import pygame

from math import sqrt
from random import random, randint

def load_png(name):
    """ Load image and return image object"""
    try:
        img = pygame.image.load(name)
    except:
        raise SystemExit('Cannot load image: %s' % name)

    if img.get_alpha() is None:
        img = img.convert()
    else:
        img = img.convert_alpha()

    return img, img.get_rect()


def get_random_colour():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return (r, g, b)


def dist(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1]-p2[1])**2)
